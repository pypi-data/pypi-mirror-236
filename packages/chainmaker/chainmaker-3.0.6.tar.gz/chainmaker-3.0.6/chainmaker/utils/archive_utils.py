#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   archive_utils.py
# @Function     :   归档实用工具方法

import logging
from datetime import datetime
from typing import Union

import pymysql

from chainmaker.chain_client import ChainClient
from chainmaker.keys import SystemContractName
from chainmaker.protos.common.block_pb2 import Block
from chainmaker.protos.common.transaction_pb2 import Transaction
from chainmaker.protos.store.store_pb2 import BlockWithRWSet
from chainmaker.sdk_config import ArchiveConfig
from chainmaker.utils import sm3, common, result_utils


def get_hmac(chain_id: str, block_height: int, full_block_data: bytes, secret_key: str) -> str:
    """
    实际上使用的sm3生成摘要-与hmac无关
    :param chain_id: 链ID
    :param block_height: 区块高度
    :param full_block_data: 完整区块二进制数据，通过BlockWithRWSet对象SerializeToString()得到
    :param secret_key: 密钥，来自sdk_config.yml中的配置
    :return: 16进制字符串
    """
    data = b''
    data += chain_id.encode()
    data += common.uint64_to_bytes(block_height)
    data += full_block_data
    data += secret_key.encode()
    return sm3.sm3_hash(data)


class ArchiveUtils:
    def __init__(self, cc: ChainClient, archive_config: ArchiveConfig):
        self.cc = cc  # 必须为admin用户
        self.archive_config = archive_config
        self.db = 'cm_archived_chain_%s' % cc.chain_id
        self.table_name = 't_block_info_1'

        self.conn = self.get_conn_and_init_database()
        self.cursor = self.conn.cursor()

    def get_conn_and_init_database(self):
        """连接数据库并返回数据库连接-数据库不存在则创建数据库"""
        dest = self.archive_config.dest or ''
        try:
            user, password, host, port = dest.split(":")
        except ValueError:
            raise ValueError('archive["dest"]格式错误, 应为<db_user>:<db_pwd>:<db_host>:<db_port>格式')
        conn = pymysql.connect(host=host, port=port, user=user, password=password,
                               charset='utf8mb4')
        conn.cursor().execute('CREATE DATABASE IF NOT EXISTS %s;' % self.db)
        conn.select_db(self.db)
        self.create_locks_table()
        self.create_sys_infos_table()
        self.create_block_info_table()
        return conn

    def query(self, sql: str, get_all=False):
        self.cursor.execute(sql)
        if get_all is True:
            return self.cursor.fetchall()
        return self.cursor.fetchone()

    def execute(self, sql: str):
        self.cursor.execute(sql)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def is_table_exists(self, table_name: str) -> bool:
        """
        检查表是否存在
        :param table_name: 表明
        :return: 存在返回True，否则返回False
        """
        sql = f'''
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{table_name}';
        '''
        data = self.query(sql)
        return True if data else False

    def create_locks_table(self):
        sql = '''
        CREATE TABLE `locks` (
          `id` int unsigned NOT NULL AUTO_INCREMENT,
          `created_at` timestamp NOT NULL,
          `updated_at` timestamp NULL DEFAULT NULL,
          `expired_at` timestamp NOT NULL,
          `holder` varchar(191) NOT NULL,
          PRIMARY KEY (`id`),
          UNIQUE KEY `holder` (`holder`)
        ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        '''
        self.execute(sql)

    def create_sys_infos_table(self):
        """
        创建sysinfos表
        """
        sql = '''
        CREATE TABLE `sysinfos` (
          `Fid` int unsigned NOT NULL AUTO_INCREMENT,
          `Fcreate_time` timestamp NULL DEFAULT NULL,
          `Fmodify_time` timestamp NULL DEFAULT NULL,
          `Fdelete_time` timestamp NULL DEFAULT NULL,
          `random_key` varchar(64) NOT NULL,
          `v` varchar(64) NOT NULL,
          PRIMARY KEY (`Fid`),
          UNIQUE KEY `random_key` (`random_key`),
          KEY `idx_sysinfos_created_at` (`Fcreate_time`)
        ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        '''
        self.execute(sql)

    def create_block_info_table(self):
        """创建表区块信息表"""
        sql = f'''
        CREATE TABLE IF NOT EXISTS `{self.table_name}` (
          `Fid` int unsigned NOT NULL AUTO_INCREMENT,
          `Fcreate_time` timestamp NULL DEFAULT NULL,
          `Fmodify_time` timestamp NULL DEFAULT NULL,
          `Fdelete_time` timestamp NULL DEFAULT NULL,
          `Fchain_id` varchar(64) NOT NULL,
          `Fblock_height` int unsigned NOT NULL,
          `Fblock_with_rwset` longblob NOT NULL,
          `Fhmac` varchar(64) NOT NULL,
          `Fis_archived` tinyint(1) NOT NULL DEFAULT '0',
          PRIMARY KEY (`Fid`),
          UNIQUE KEY `idx_blockheight` (`Fblock_height`),
          KEY `idx_t_block_info_new_created_at` (`Fcreate_time`)
        ) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        '''
        self.execute(sql)

    def query_db_archive_block_data(self, block_height: int):
        sql = f'''
        SELECT `Fblock_with_rwset`, `Fhmac`
        FROM `{self.table_name}`
        WHERE `Fblock_height`= {block_height};
        '''
        return self.query(sql)

    def insert_db_archive_block_data(self, block_height: int):
        create_time = modify_time = datetime.now().strftime('%Y-%m-%s %H:%M:%S')
        full_block_data = self.cc.get_full_block_by_height(block_height).SerializeToString()
        secret_key = self.archive_config.secret_key
        hmac = get_hmac(self.cc.chain_id, block_height, full_block_data, secret_key)
        sql = f'''
INSERT INTO `{self.table_name}` (Fcreate_time,Fmodify_time,Fchain_id,Fblock_height,Fblock_with_rwset,Fhmac,Fis_archived)
VALUES ({create_time},{modify_time},{block_height},{full_block_data},{hmac},1);'''
        self.execute(sql)

    def get_db_archive_block_data(self, block_height: int) -> tuple:
        sql = f'SELECT Fblock_with_rwset, Fhmac from {self.table_name} WHERE Fblock_height={block_height};'
        return self.query(sql)

    def get_db_archive_block_is_archived(self, block_height: int) -> Union[bool, None]:
        sql = f'SELECT Fis_archived from {self.table_name} WHERE Fblock_height={block_height};'
        data = self.query(sql)
        if not data:
            return None
        return data == 1

    def update_db_archive_block_data_is_archived(self, block_height, is_archived=True):
        is_archived = 1 if is_archived is True else 0
        sql = f'UPDATE {self.table_name} SET Fis_archived = {is_archived}  WHERE Fblock_height={block_height}'
        self.execute(sql)

    def archive_block(self, block_height: int):
        payload = self.cc.create_archive_block_payload(block_height)
        tx_response = self.cc.send_manage_request(payload, with_sync_result=True)
        result_utils.check_response(tx_response)

    def restore_block(self, full_block_data: bytes):
        """发送回复区块数据请求"""
        payload = self.cc.create_restore_block_payload(full_block_data)
        tx_response = self.cc.send_manage_request(payload, with_sync_result=True)
        result_utils.check_response(tx_response)

    def get_db_archived_block_height(self):
        sql = 'SELECT v FROM sysinfos WHERE random_key="archived_block_height";'
        return self.query(sql)

    def update_db_archived_block_height(self, block_height: int):
        sql = f'UPDATE sysinfos SET v = {block_height} WHERE random_key="archived_block_height";'
        self.execute(sql)

    def increase_db_archived_block_height(self):
        """数据库归档区块高度+1"""
        db_archived_block_height = self.get_db_archived_block_height() or 0
        assert isinstance(db_archived_block_height, int), '原归档高度必须为int类型'
        self.update_db_archive_block_data_is_archived(db_archived_block_height + 1)

    def decrease_db_archived_block_height(self):
        """数据库归档高度-1"""
        db_archived_block_height = self.get_db_archived_block_height()
        if db_archived_block_height > 0:
            self.update_db_archived_block_height(db_archived_block_height - 1)

    def calc_target_height_by_time(self):
        pass

    def check_archive_target_block_height(self, target_block_height: int):
        """检查归档条件"""
        chain_current_block_height = self.cc.get_current_block_height()
        if chain_current_block_height < target_block_height:
            raise ValueError('required current block height >= target block height')

        chain_archived_block_height = self.cc.get_archived_block_height()
        if target_block_height <= chain_archived_block_height:
            raise ValueError('target block height already archived')

        db_archived_block_height = self.get_db_archived_block_height()
        if chain_archived_block_height != db_archived_block_height:
            raise ValueError('required archived block height off-chain == archived block height on-chain')

    def archive(self, target_block_height: int):
        """
        归档数据到数据库
        :param target_block_height: 目标区块高度
        :return:
        """
        self.check_archive_target_block_height(target_block_height)

        try:
            is_archived = self.get_db_archive_block_is_archived(target_block_height)
            if is_archived is None:
                self.insert_db_archive_block_data(target_block_height)

            elif is_archived is False:
                self.update_db_archive_block_data_is_archived(target_block_height, is_archived=True)

            self.archive_block(target_block_height)
            self.increase_db_archived_block_height()
            self.commit()
        except Exception as ex:
            logging.error(f'归档区块 {target_block_height} 出错')
            logging.exception(ex)
            self.rollback()
        finally:
            self.close()

    def batch_archive(self, start_block_height: int, end_block_height: int):
        """
        批量归档区块，包含start_block_height和end_block_height（前闭后闭区间）
        :param start_block_height: 归档开始区块高度
        :param end_block_height: 归档截止区块高度
        """
        assert start_block_height <= end_block_height, '起始区块高度应小于终止区块高度'
        current_block_height = start_block_height
        while current_block_height <= end_block_height:
            self.archive(current_block_height)
            current_block_height += 1

    def check_restore_target_block_height(self, target_block_height: int):
        chain_archived_block_height = self.cc.get_archived_block_height()
        if target_block_height > chain_archived_block_height:
            raise ValueError('restore start block height is not archived')

    def is_config_block(self, block: Block) -> bool:
        if block is None or len(block.txs) == 0:
            return False
        tx = block.txs[0]
        return self.is_valid_config_tx(tx)

    def is_valid_config_tx(self, tx: Transaction) -> bool:
        if tx.result is None or tx.result.contract_result is None or tx.result.contract_result.result is None:
            return False
        if not self.is_config_tx(tx):
            return False
        if tx.result.code != 0:  # TxStatusCode_SUCCESS
            return False
        return True

    @staticmethod
    def is_config_tx(tx: Transaction):
        if tx is None:
            return False
        return SystemContractName.CHAIN_CONFIG == tx.payload.contract_name

    def restore(self, target_block_height: int):
        """
        回复数据到链上
        :param target_block_height: 目标区块高度
        :return:
        """
        self.check_restore_target_block_height(target_block_height)
        try:
            # _verify hmac
            secret_key = self.archive_config.secret_key
            data = self.get_db_archive_block_data(target_block_height)
            if data is None:
                raise ValueError(f'target block height {target_block_height} not in {self.db}.{self.table_name}')
            full_block_data, hmac = data
            excepted_hmac = get_hmac(self.cc.chain_id, target_block_height, full_block_data, secret_key)
            assert excepted_hmac == hmac, f'invalid HMAC signature, recalculate: {excepted_hmac} from_db: {hmac}'

            # 更新数据库当前区块信息已归档状态为0
            self.update_db_archive_block_data_is_archived(target_block_height, is_archived=False)
            # 更新归档区块高度 -1
            self.decrease_db_archived_block_height()
            # only restore Not-Config-Block
            block_with_rwset = BlockWithRWSet()
            block_with_rwset.ParseFromString(full_block_data)
            block = block_with_rwset.block
            if not self.is_config_block(block):
                self.restore_block(full_block_data)
            self.commit()
        except Exception as ex:
            logging.error(f'恢复区块数据 {target_block_height} 出错')
            logging.exception(ex)
        finally:
            self.close()

    def batch_restore(self, start_block_height, end_block_height):
        """
        批量归档区块
        :param start_block_height: 起始区块高度（包含）
        :param end_block_height: 结束区块高度（包含）
        """
        assert start_block_height <= end_block_height, '起始区块高度应小于终止区块高度'
        current_block_height = start_block_height
        while current_block_height <= end_block_height:
            self.restore(current_block_height)
            current_block_height += 1
