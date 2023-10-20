#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   archive.py
# @Function     :   ChainMaker 归档接口

from typing import Callable

import pymysql

from chainmaker.apis.base_client import BaseClient
from chainmaker.archive_service import (ArchiveCenterGrpcClient, ArchiveCenterHttpClient, ArchiveMysqlClient,
                                        ArchiveService)
from chainmaker.exceptions import ChainClientException
from chainmaker.keys import (ArchiveDB, ArchiveManageMethod, ArchiveType, ChainQueryMethod, ParamKey,
                             SystemContractName)
from chainmaker.protos.common.block_pb2 import BlockInfo
from chainmaker.protos.common.request_pb2 import Payload
from chainmaker.protos.common.result_pb2 import TxResponse
from chainmaker.protos.store.store_pb2 import ArchiveProcess, ArchiveStatus, BlockWithRWSet
from chainmaker.utils.common import uint64_to_bytes


class ArchiveMixIn(BaseClient):
    _archive_service = None

    def create_archive_block_payload(self, target_block_height: int) -> Payload:
        """
        构造数据归档区块Payload
        :param target_block_height: 归档目标区块高度
        :return: 待签名Payload
        """
        self._debug("create [ArchiveBlock] to be signed payload")
        params = {ParamKey.BLOCK_HEIGHT.name: uint64_to_bytes(target_block_height)}
        return self._payload_builder.create_archive_payload(
            SystemContractName.ARCHIVE_MANAGE.name,
            ArchiveManageMethod.ARCHIVE_BLOCK.name,
            params,
        )

    def create_restore_block_payload(self, full_block: bytes) -> Payload:
        """
        构造归档数据恢复Payload
        :param full_block: 完整区块数据（对应结构：store.BlockWithRWSet）
        :return: 待签名Payload
        """
        self._debug("create [RestoreBlock] to be signed payload")
        params = {ParamKey.FULL_BLOCK.name: full_block}
        return self._payload_builder.create_archive_payload(
            SystemContractName.ARCHIVE_MANAGE.name,
            ArchiveManageMethod.RESTORE_BLOCK.name,
            params,
        )

    @staticmethod
    def sign_archive_payload(payload: Payload) -> Payload:  # do nothing
        return payload

    def send_archive_block_request(
            self, payload: Payload, timeout: int = None
    ) -> TxResponse:
        """
        发送归档请求
        :param payload: 归档待签名Payload
        :param timeout: 超时时间
        :return: 交易响应TxResponse
        :raise: 已归档抛出InternalError
        """
        return self.send_request(payload, timeout=timeout)

    def send_restore_block_request(self, payload, timeout: int = None):
        return self.send_request(payload, timeout=timeout)

    def get_archived_full_block_by_height(self, block_height: int) -> BlockWithRWSet:
        """
        根据区块高度，查询已归档的完整区块（包含合约event info）
        :param block_height: 区块高度
        :return: 区块详情 BlockInfo
        :raises RequestError: 请求失败
        """
        full_block = self.get_from_archive_store(block_height)
        return full_block

    def get_archived_block_by_height(
            self, block_height: int, with_rwset: bool = False
    ) -> BlockInfo:
        """
        根据区块高度，查询已归档的区块
        :param block_height: 区块高度
        :param with_rwset: 是否包含读写集
        :return: 区块详情 BlockInfo
        :raises RequestError: 请求失败
        """
        full_block = self.get_from_archive_store(block_height)
        block_info = BlockInfo(
            block=full_block.block,
        )
        if with_rwset:
            block_info.rwset_list = full_block.TxRWSets

        return block_info

    def get_archived_block_by_hash(
            self, block_hash: str, with_rwset: bool = False
    ) -> BlockInfo:
        """
        根据区块hash查询已归档的区块
        :param block_hash: 区块hash
        :param with_rwset: 是否包含读写集
        :return: 区块详情 BlockInfo
        :raises RequestError: 请求失败
        """
        block_height = self.get_block_height_by_hash(block_hash)
        return self.get_archived_block_by_height(block_height, with_rwset)

    def get_archived_block_by_tx_id(
            self, tx_id: str, with_rwset: bool = False
    ) -> BlockInfo:
        """
        根据交易id查询已归档的区块
        :param tx_id: 交易ID
        :param with_rwset: 是否包含读写集
        :return: 区块详情 BlockInfo
        :raises RequestError: 请求失败
        """
        block_height = self.get_block_height_by_tx_id(tx_id)
        return self.get_archived_block_by_height(block_height, with_rwset)

    def get_archived_tx_by_tx_id(self, tx_id: str):
        """
        根据交易id查询已归档的交易
        :param tx_id: 交易id
        :return: 交易详情
        :raises RequestError: 请求失败
        """
        block_info = self.get_archived_block_by_tx_id(tx_id)
        for tx in block_info.block.txs:
            if tx.payload.tx_id == tx_id:
                return tx

    @property
    def archive_service(self) -> ArchiveService:
        """
        获取归档服务
        v2.3.2 新增
        :return: 归档服务对象
        """
        if self._archive_service is None:
            if self._archive_config is None:
                raise ChainClientException("archive config is not set")
            if self._archive_config.type == ArchiveType.mysql.name:
                self._archive_service = ArchiveMysqlClient(self, self._archive_config)
            elif self._archive_config.type == ArchiveType.archivecenter.name:
                if self.archive_center_config is None:
                    raise ChainClientException("archive center config is not set")
                if self.archive_center_config.rpc_address:
                    self._archive_service = ArchiveCenterGrpcClient(self, self.archive_center_config)

                elif self.archive_center_config.archive_center_http_url:
                    self._archive_service = ArchiveCenterHttpClient(self, self.archive_center_config)
                else:
                    raise ChainClientException("neither rpc_address nor archive_center_http_url nor is set")
            else:
                raise ChainClientException("unsupported archive type")
        return self._archive_service

    def get_from_archive_store(self, block_height: int, archive_type: str = None):
        archive_type = archive_type or self._archive_config.type or "mysql"
        if archive_type.lower() == "mysql":
            return self.get_archived_block_from_mysql(block_height)
        raise NotImplementedError("目前仅支持MySQL数据库")

    def get_archived_block_from_mysql(self, block_height: int):
        dest = self._archive_config.dest or ""
        try:
            db_user, db_pwd, db_host, db_port = dest.split(":")
        except ValueError:
            raise ValueError(
                'archive["dest"]格式错误, 应为<db_user>:<db_pwd>:<db_host>:<db_port>格式'
            )

        db_name = "%s_%s" % (ArchiveDB.MysqlDBNamePrefix, self.chain_id)
        table_sn = int(block_height / ArchiveDB.RowsPerBlockInfoTable.value) + 1
        table_name = "%s_%s" % (ArchiveDB.MysqlTableNamePrefix, table_sn)
        query_sql = ArchiveDB.QUERY_FULL_BLOCK_BY_HEIGHT_SQL % (
            table_name,
            block_height,
        )

        with pymysql.Connection(
                host=db_host, port=int(db_port), user=db_user, password=db_pwd, db=db_name
        ) as conn:
            cursor = conn.cursor()
            cursor.execute(query_sql)
            block_with_rwset_bytes, hmac = cursor.fetchone()

        # TODO 校验 hmac
        block_with_rwset = BlockWithRWSet()
        block_with_rwset.ParseFromString(block_with_rwset_bytes)

        return block_with_rwset

    def get_archive_status(self) -> ArchiveStatus:
        """
        获取归档状态
        :return:
        """
        self._debug("get_archive_status")
        payload = self._payload_builder.create_query_payload(SystemContractName.CHAIN_QUERY.name,
                                                             ChainQueryMethod.GET_ARCHIVE_STATUS.name)
        response = self.send_request(payload)
        archive_status = ArchiveStatus()
        archive_status.ParseFromString(response.contract_result.result)
        return archive_status

    def archive_blocks(self, archive_height: int, notice: Callable = None) -> None:
        """
        批量归档区块到MySQL或归档中心
        :param archive_height: 目标归档高度
        :param notice: 回调函数 eg: def print_err(block_height, exception): ...
        :return:
        """
        try:
            archive_status = self.get_archive_status()
            if archive_status.process != ArchiveProcess.Normal:
                raise ChainClientException("peer archive is in process")

            begin_height, end_height = 0, archive_height
            if archive_status.archive_pivot > begin_height:
                begin_height = archive_status.archive_pivot
            if end_height > archive_status.max_allow_archive_height:
                end_height = archive_status.max_allow_archive_height

            archive_service = self.archive_service
            archived_status_resp = archive_service.get_archived_status()
            if "chain genesis not exists" in archived_status_resp.message:
                genesis = self.get_block_by_height(0, with_rw_set=True)
                archive_service.register(genesis)

            if archived_status_resp.in_archive:
                raise ChainClientException('archive service is in process')

            archived_height = archived_status_resp.archived_height
            if begin_height > archived_height:
                raise ChainClientException(f'peer archive begin height: {begin_height}, '
                                           f'archive service height: {archived_height} not match')

            begin_height = archived_height
            blocks = (self.get_block_by_height(block_height, True)
                      for block_height in range(begin_height, end_height + 1))
            archive_service.archive_blocks(blocks, notice)
        except Exception as e:
            self._logger.exception(e)
            raise ChainClientException(f"archive blocks fail: {e}")

    def restore_blocks(self, restore_height, notice: Callable = None) -> None:
        """
        批量恢复区块到链上
        :param restore_height: 恢复到的高度，eg: 0
        :param notice: 回调函数 eg: def print_info(block_height, exception=None): ...
        :return:
        """
        try:
            archive_status = self.get_archive_status()
            if archive_status.process != ArchiveProcess.Normal:
                raise ChainClientException(f"chain is restoring or archiving, , retry later !"
                                           f" [process={archive_status.process}]")
            if restore_height > archive_status.archive_pivot:
                raise ChainClientException("not block needs restore")
            begin_height, end_height = archive_status.archive_pivot, restore_height
            archive_service = self.archive_service
            for block_height in range(end_height, begin_height - 1, -1):
                if callable(notice):
                    notice(block_height, None)
                if self._is_height_in_restore_range(block_height, archive_status.file_ranges_list):
                    continue

                block_info = archive_service.get_block_by_height(block_height, with_rw_set=True)
                self._restore_block(block_info)
                if block_height == 0:
                    break

        except Exception as e:
            self._logger.exception(e)
            raise ChainClientException(f"restores block fail: {e}")

    def _restore_block(self, block_info: BlockInfo):
        full_block = block_info.SerializeToString()  # todo check
        payload = self.create_restore_block_payload(full_block)
        try:
            tx_response = self.send_restore_block_request(payload)
            if tx_response.code != 0:
                raise ChainClientException(f"SendRestoreBlockRequest get error : code={tx_response.code}")
        except Exception as e:
            raise ChainClientException(f"SendRestoreBlockRequest get error : {e}")

    @staticmethod
    def _is_height_in_restore_range(block_height: int, file_ranges) -> bool:
        for file_range in file_ranges:
            if file_range.start <= block_height <= file_range.end:
                return True


class ArchiveWithEndorsers(BaseClient):
    def archive_block(self, target_block_height: int, timeout: int = None) -> TxResponse:
        """
        归档区块
        :param target_block_height: 目标区块高度
        :param timeout: RPC请求超时时间
        :return: 请求响应
        """
        payload = self.create_archive_block_payload(target_block_height)
        return self.send_archive_block_request(payload, timeout=timeout)

    # 10-01 恢复区块
    def restore_block(self, full_block: bytes, timeout: int = None) -> TxResponse:
        """
        恢复区块
        :param full_block: 完整区块数据
        :param timeout: RPC请求超时时间
        :return: 请求响应
        """
        payload = self.create_restore_block_payload(full_block)
        return self.send_archive_block_request(payload, timeout=timeout)
