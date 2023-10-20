#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   archive_mysql_client.py
# @Function     :   归档服务MySQL客户端
# v2.3.2 新增

from datetime import datetime
from typing import Callable, Iterator, Optional, Union

import pymysql
from chainmaker.utils.gm import sm3

from chainmaker.keys import ArchiveDB
from chainmaker.sdk_config import ArchiveConfig
from chainmaker.protos.common.block_pb2 import BlockInfo, BlockType
from chainmaker.protos.common.transaction_pb2 import Transaction, TransactionInfo, TransactionInfoWithRWSet
from chainmaker.protos.config.chain_config_pb2 import ChainConfig
from chainmaker.protos.store.store_pb2 import BlockWithRWSet
from chainmaker.utils.common import uint64_to_bytes
from .archive_service import ArchiveService
from ..exceptions import ChainClientException
from ..protos.archivecenter.archivecenter_pb2 import ArchiveStatusResp


def get_block_info_table(block_height: int) -> str:
    """
    根据区块高度获取分表的表名
    :param block_height:
    :return:
    """
    n = block_height // ArchiveDB.RowsPerBlockInfoTable + 1
    return '%s_%d' % (ArchiveDB.MysqlTableNamePrefix, n)


def get_hmac(
        chain_id: str, block_height: int, full_block_data: bytes, secret_key: str
) -> str:
    """
    实际上使用的sm3生成摘要(与haslib.hmac无关)
    hmac SM3(Fchain_id+Fblock_height+Fblock_with_rwset+key)
    :param chain_id: 链ID
    :param block_height: 区块高度
    :param full_block_data: 完整区块二进制数据，通过BlockWithRWSet对象SerializeToString()得到
    :param secret_key: 密钥，来自sdk_config.yml中的配置
    :return: 16进制字符串
    """
    data = b"".join([chain_id.encode(), uint64_to_bytes(block_height), full_block_data, secret_key.encode()])
    return sm3.sm3_hash(data)


class ArchiveMysqlClient(ArchiveService):
    def __init__(self, cc, archive_config: ArchiveConfig):
        super().__init__(cc)
        self.archive_config = archive_config

        self.db = '%s_%s' % (ArchiveDB.MysqlDBNamePrefix, self.chain_id)
        self.sys_info_table = ArchiveDB.MysqlSysInfoTable
        self.charset = ArchiveDB.MysqlTableCharset
        self.collate = ArchiveDB.MySqlTableCollate

        self.conn = self._get_conn_and_init_database()
        self.curser = self.conn.cursor()

    def get_tx_by_tx_id(self, tx_id: str) -> TransactionInfo:
        self.logger.debug("[SDK] begin to GetTxByTxId from mysql, [tx_id:%s]", tx_id)
        block_height = self.cc.get_block_height_by_tx_id(tx_id)
        return self._get_tx_info_from_db(block_height, tx_id)

    def get_tx_with_rwset_by_tx_id(self, tx_id: str) -> TransactionInfoWithRWSet:
        self.logger.debug("[SDK] begin to GetTxWithRWSetByTxId from mysql, [tx_id:%s]", tx_id)
        block_height = self.cc.get_block_height_by_tx_id(tx_id)
        return self._get_tx_info_from_db(block_height, tx_id, with_rw_set=True)

    def get_block_by_height(self, block_height: int, with_rw_set: bool = False) -> BlockInfo:
        self.logger.debug(
            "[SDK] begin to GetBlockByHeight from mysql, [block_height:%d]/[with_rw_set:%s]",
            block_height,
            with_rw_set,
        )
        sql = "SELECT Fblock_with_rwset FROM t_block_info_1 WHERE Fblock_height = %d;" % block_height
        result = self._query(sql)

        if not result or len(result) < 1:
            raise Exception('Could not get block form mysql')
        return self._get_block_info_from_full_block_data(result[0], with_rw_set)

    def get_block_by_hash(self, block_hash: str, with_rw_set: bool = False) -> BlockInfo:
        self.logger.debug(
            "[SDK] begin to GetBlockByHash from mysql, [block_hash:%s]/[with_rw_set:%s]",
            block_hash,
            with_rw_set,
        )

        block_height = self.cc.get_block_height_by_hash(block_hash)
        return self.get_block_by_height(block_height, with_rw_set)

    def get_block_by_tx_id(self, tx_id: str, with_rw_set: bool = False) -> BlockInfo:
        self.logger.debug(
            "[SDK] begin to GetBlockByTxId from mysql, [tx_id:%s]/[with_rw_set:%s]",
            tx_id,
            with_rw_set,
        )
        block_height = self.cc.get_block_height_by_tx_id(tx_id)
        return self.get_block_by_height(block_height, with_rw_set)

    def get_chain_config_by_block_height(self, block_height: int) -> ChainConfig:
        self.logger.debug(
            "[SDK] begin to get chain config by block height from mysql [%d]", block_height
        )
        archive_status_resp = self.get_archived_status()
        archived_height = archive_status_resp.archived_height
        # 目标高度小于已归档高度
        if block_height <= archived_height:
            block_info = self.get_block_by_height(block_height)
            header = block_info.block.header
            if header.block_type == BlockType.CONFIG_BLOCK:
                tx = block_info.block.tx[0]
                return self._get_chain_config_from_tx(tx)
            else:
                pre_conf_height = header.pre_conf_height
                block_info = self.get_block_by_height(pre_conf_height)
                tx = block_info.block.txs[0]
                return self._get_chain_config_from_tx(tx)

    def register(self, genesis: BlockInfo) -> None:
        self.logger.debug('[SDK] create table sysinfo')
        self._create_sys_infos_table()

        self.logger.debug("[SDK] begin to register genesis block to mysql")
        self._init_archived_status_data()

        self.logger.debug('[SDK] create table t_block_info_1')
        self._create_block_info_table()

    def archive_block(self, block: BlockInfo) -> None:
        block_height = block.block.header.block_height
        self.logger.debug("[SDK] begin to archive block %d to mysql" % block_height)
        if block_height == 0:
            self._create_block_info_table()

        is_archived = self._get_db_archive_block_is_archived(block_height)
        if is_archived is None:
            self._insert_db_archive_block_data(block_height)
        elif is_archived is False:
            self._update_db_archive_block_data_is_archived(block_height)
        self._update_db_archived_block_height(block_height)

    def archive_blocks(self, blocks: Iterator, notice: Callable = None) -> None:
        count = 0
        for block in blocks:
            block_height = block.block.header.block_height
            try:
                self.archive_block(block)
            except Exception as ex:
                notice(block_height, ex)
            else:
                count += 1
                notice(block_height, None)
        if count == 0:
            raise Exception('no block to archive')

    def get_archived_status(self) -> ArchiveStatusResp:
        self.logger.debug("[SDK] get archived status from mysql")
        try:
            archived_height = self._get_db_archived_block_height()
        except Exception as ex:
            self.logger.exception(ex)
            # raise ChainClientException('chain genesis not exists')
            return ArchiveStatusResp(archived_height=0, in_archive=False, code=0, message='chain genesis not exists')

        return ArchiveStatusResp(archived_height=archived_height, in_archive=False, code=0, message=None)

    def _get_conn_and_init_database(self):
        """连接数据库并返回数据库连接-数据库不存在则创建数据库"""
        dest = self.archive_config.dest or ""
        try:
            user, password, host, port = dest.split(":")
            port = int(port)
        except ValueError:
            raise ChainClientException(
                'archive["dest"]格式错误, 应为<db_user>:<db_pwd>:<db_host>:<db_port>格式'
            )

        conn = pymysql.connect(
            host=host, port=port, user=user, password=password, charset=self.charset
        )
        conn.cursor().execute("CREATE DATABASE IF NOT EXISTS %s;" % self.db)
        conn.select_db(self.db)
        return conn

    def _init_archived_status_data(self) -> None:
        """InitArchiveStatusData"""
        sql = f'SELECT v FROM {self.sys_info_table} WHERE k="archived_block_height";'
        result = self._query(sql)
        if result is None:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = f"""INSERT INTO `{self.sys_info_table}` (Fcreate_time,Fmodify_time,k,v) 
            VALUES ('{now}','{now}','archived_block_height', 0);"""
            self._execute(sql)

    def _query(self, sql: str, get_all=False) -> Optional[tuple]:
        self.curser.execute(sql)
        if get_all is True:
            return self.curser.fetchall()
        return self.curser.fetchone()

    def _execute(self, sql: str, *args):
        try:
            self.curser.execute(sql, *args)
            self.conn.commit()
        except Exception as ex:
            self.logger.exception(ex)
            self.conn.rollback()

    def _close(self):
        self.curser.close()
        self.conn.close()

    def _create_sys_infos_table(self):
        """
        创建sysinfo表
        """
        sql = f"""
            CREATE TABLE IF NOT EXISTS `{self.sys_info_table}` (
              `Fid` int unsigned NOT NULL AUTO_INCREMENT,
              `Fcreate_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
              `Fmodify_time` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              `Fdelete_time` timestamp NULL DEFAULT NULL,
              `k` varchar(64) NOT NULL,
              `v` varchar(64) NOT NULL,
              PRIMARY KEY (`Fid`),
              UNIQUE KEY `k` (`k`),
              KEY `idx_sysinfo_created_at` (`Fcreate_time`)
            ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET={self.charset} COLLATE={self.collate};
            """
        self._execute(sql)

    def _create_block_info_table(self, block_height: int = 0):
        """创建表区块信息表"""
        block_info_table = get_block_info_table(block_height)
        sql = f"""
            CREATE TABLE IF NOT EXISTS `{block_info_table}` (
              `Fid` int unsigned NOT NULL AUTO_INCREMENT,
              `Fcreate_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
              `Fmodify_time` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              `Fdelete_time` timestamp NULL DEFAULT NULL,
              `Fchain_id` varchar(64) NOT NULL,
              `Fblock_height` int unsigned NOT NULL,
              `Fblock_with_rwset` longblob NOT NULL,
              `Fhmac` varchar(64) NOT NULL,
              `Fis_archived` tinyint(1) NOT NULL DEFAULT '0',
              PRIMARY KEY (`Fid`),
              UNIQUE KEY `idx_blockheight` (`Fblock_height`),
              KEY `idx_t_block_info_new_created_at` (`Fcreate_time`)
            ) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET={self.charset} COLLATE={self.collate};
            """
        self._execute(sql)

    def _query_db_archive_block_data(self, block_height: int):
        block_info_table = get_block_info_table(block_height)
        sql = f"""
            SELECT `Fblock_with_rwset`, `Fhmac`
            FROM `{block_info_table}`
            WHERE `Fblock_height`= {block_height};
            """
        return self._query(sql)

    def _insert_db_archive_block_data(self, block_height: int):
        block_info_table = get_block_info_table(block_height)
        self._create_block_info_table(block_height)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_block_data = self.cc.get_full_block_by_height(
            block_height
        ).SerializeToString()
        secret_key = self.archive_config.secret_key
        hmac = get_hmac(self.cc.chain_id, block_height, full_block_data, secret_key)
        # full_block_data_base64 = base64.b64encode(full_block_data).decode()
        sql = f"""
            INSERT INTO `{block_info_table}` 
            (Fcreate_time,Fmodify_time,Fchain_id,Fblock_height,Fblock_with_rwset,Fhmac,Fis_archived)
            VALUES ('{now}','{now}','{self.chain_id}',{block_height},%s,'{hmac}',1);
            """
        self._execute(sql, (full_block_data,))

    def get_db_archive_block_data(self, block_height: int) -> tuple:
        block_info_table = get_block_info_table(block_height)
        sql = f"SELECT Fblock_with_rwset, Fhmac from {block_info_table} WHERE Fblock_height={block_height};"
        return self._query(sql)

    def _get_db_archive_block_is_archived(self, block_height: int) -> Optional[bool]:
        """

        :param block_height:
        :return:
        """
        block_info_table = get_block_info_table(block_height)
        sql = f"SELECT Fis_archived from {block_info_table} WHERE Fblock_height={block_height};"
        data = self._query(sql)
        if not data:
            return None
        return data == 1

    def _update_db_archive_block_data_is_archived(self, block_height: int, is_archived: bool = True):
        """更新block_info表对应区块改的is_archived状态"""
        block_info_table = get_block_info_table(block_height)
        is_archived = 1 if is_archived is True else 0
        sql = f"UPDATE {block_info_table} SET Fis_archived = {is_archived}  WHERE Fblock_height={block_height}"
        self._execute(sql)

    def _get_db_archived_block_height(self) -> Optional[int]:
        """查询MySQL数据库已归档区块高度"""
        sql = f'SELECT v FROM {self.sys_info_table} WHERE k="archived_block_height";'
        try:
            result = self._query(sql)
            return int(result[0]) if result else 0
        except Exception as ex:
            self.logger.exception(ex)

    def _update_db_archived_block_height(self, block_height: int) -> None:
        """更新sysinfo表归档区块高度"""
        self._create_sys_infos_table()
        self._init_archived_status_data()
        sql = f'UPDATE {self.sys_info_table} SET v = {block_height} WHERE k="archived_block_height";'
        self._execute(sql)

    def _get_tx_info_from_db(self, block_height: int, tx_id: str, with_rw_set: bool = False) -> \
            Union[TransactionInfo, TransactionInfoWithRWSet]:
        block_info = self.get_block_by_height(block_height, with_rw_set=with_rw_set)
        block_timestamp = block_info.block.header.block_timestamp
        block_hash = block_info.block.header.block_hash
        txs = block_info.block.txs

        for index, item in enumerate(txs):
            if tx_id == item.payload.tx_id:
                data = dict(transaction=item, block_height=block_height,
                            block_hash=block_hash,
                            block_timestamp=block_timestamp,
                            tx_index=index)
                if with_rw_set is True and block_info.rwset_list:
                    data.update(rw_set=block_info.rwset_list[index])
                    return TransactionInfoWithRWSet(**data)
                return TransactionInfo(**data)

        raise Exception("tx_id not found in MySQL database")

    @staticmethod
    def _get_chain_config_from_tx(tx: Transaction) -> ChainConfig:
        chain_config = ChainConfig()
        chain_config.ParseFromString(tx.result.contract_result.result)
        return chain_config

    @staticmethod
    def _get_block_info_from_full_block_data(full_block_data: bytes, with_rw_set: bool = False) -> BlockInfo:
        block_with_rw_set = BlockWithRWSet()
        block_with_rw_set.ParseFromString(full_block_data)
        block_info = BlockInfo(block=block_with_rw_set.block)
        if with_rw_set is True:
            block_info.rwset_list.extend(block_with_rw_set.txRWSets)
        return block_info
