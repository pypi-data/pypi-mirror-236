#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   archive_center_http_client.py
# @Function     :   归档中心HTTP客户端
# v2.3.2 新增

from enum import Enum
from typing import Callable

import requests

from chainmaker.archive_service.archive_service import ArchiveService
from chainmaker.sdk_config import ArchiveCenterConfig
from chainmaker.protos.archivecenter.archivecenter_pb2 import ArchiveStatusResp
from chainmaker.protos.common.block_pb2 import BlockInfo
from chainmaker.protos.common.transaction_pb2 import TransactionInfo, TransactionInfoWithRWSet
from chainmaker.protos.config.chain_config_pb2 import ChainConfig


class ArchiveCenterHttpApi(Enum):
    GetArchiveStatus = '/get_archive_status'
    GetArchivedHeight = '/get_archived_height'
    GetChainInfos = '/get_chains_infos'
    GetMerklePathByTxId = '/get_merklepath_by_txid'
    GetTruncateBlockByHeight = '/get_truncate_block_by_height'
    GetTruncateBlockByTxId = '/get_truncate_block_by_txid'
    GetFullBlockByHeight = '/get_full_block_by_height'
    GetBlockInfoByHash = '/get_block_info_by_hash'
    GetBlockInfoByTxId = '/get_block_info_by_txid'
    GetBlockInfoByHeight = '/get_block_info_by_height'  # TODO check
    GetTxByTxId = 'get_full_transaction_info_by_txid'
    GetChainCompress = '/get_chain_compress'
    GetHashHexByHashByte = '/get_hashhex_by_hashbyte'
    AddCA = '/admin/add_ca'
    CompressUnderHeight = '/admin/compress_under_height'


class ArchiveCenterHttpClient(ArchiveService):
    def __init__(self, cc, archive_center_config: ArchiveCenterConfig):
        super().__init__(cc)
        self.archive_center_config = archive_center_config
        self.session = requests.Session()
        self.session.headers = {'x-token': ''}
        self.chain_genesis_hash = self.archive_center_config.chain_genesis_hash
        self.base_url = self.archive_center_config.archive_center_http_url
        if not self.base_url.startswith('http:'):
            self.base_url = 'http://%s' % self.base_url
        if not self.base_url.endswith('/'):
            self.base_url = '%s/' % self.base_url

    def get_tx_by_tx_id(self, tx_id: str) -> TransactionInfo:
        self.logger.debug("[SDK] begin to GetTxByTxId rom archive center by http, [tx_id:%s]", tx_id)

    def get_tx_with_rwset_by_tx_id(self, tx_id: str, with_rw_set: bool = True) -> TransactionInfoWithRWSet:
        self.logger.debug("[SDK] begin to GetTxWithRWSetByTxId from archive center by http, [tx_id:%s]", tx_id)

    def get_block_by_height(self, block_height: int, with_rw_set: bool = False) -> BlockInfo:
        self.logger.debug(
            "[SDK] begin to GetBlockByHeight from archive center by http, [block_height:%d]/[with_rw_set:%s]",
            block_height,
            with_rw_set,
        )

    def get_block_by_hash(self, block_hash: str, with_rw_set: bool = False) -> BlockInfo:
        self.logger.debug(
            "[SDK] begin to GetBlockByHash from archive center by http, [block_hash:%s]/[with_rw_set:%s]",
            block_hash,
            with_rw_set,
        )

    def get_block_by_tx_id(self, tx_id: str, with_rw_set: bool = False) -> BlockInfo:
        self.logger.debug(
            "[SDK] begin to GetBlockByTxId from archive center by http, [tx_id:%s]/[with_rw_set:%s]",
            tx_id,
            with_rw_set,
        )

    def get_chain_config_by_block_height(self, block_height: int) -> ChainConfig:
        self.logger.debug(
            "[SDK] begin to get chain config by block height from archive center by http [%d]", block_height
        )

    def register(self, genesis: BlockInfo) -> None:
        raise NotImplementedError('http is a read only api, not implement Register')

    def archive_block(self, block: BlockInfo) -> None:
        raise NotImplementedError('http is a read only api, not implement ArchiveBlock')

    def archive_blocks(self, blocks, notice: Callable = None) -> None:
        raise NotImplementedError('http is a read only api, not implement ArchiveBlocks')

    def get_archived_status(self) -> ArchiveStatusResp:
        raise NotImplementedError('http is a read only api, not implement GetArchivedStatus')

    def _compress_under_height(self, height: int):
        """
        压缩链归档数据接口
        :param height: 区块高度
        :return:
        """
        url = ArchiveCenterHttpApi.CompressUnderHeight.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
            "height": height
        }
        resp = self._post(url, payload)
        return resp

    def _get_archive_status(self):
        url = ArchiveCenterHttpApi.GetArchiveStatus.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
        }
        resp = self._post(url, payload)
        return resp

    def _get_archived_height(self):
        url = ArchiveCenterHttpApi.GetArchivedHeight.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
        }
        resp = self._post(url, payload)
        return resp

    def _get_chain_compress(self):
        url = ArchiveCenterHttpApi.GetChainCompress.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
        }
        resp = self._post(url, payload)
        return resp

    def _add_ca(self, ca_name: str) -> None:
        url = ArchiveCenterHttpApi.AddCA.value
        payload = {
            "ca_name": ca_name,
        }
        resp = self._post(url, payload)
        print(resp)

    def _get_chains_infos(self):
        url = ArchiveCenterHttpApi.GetChainInfos.value
        payload = {
        }
        resp = self._post(url, payload)
        return resp

    def _get_hashhex_by_hashbyte(self, block_hash: str):
        url = ArchiveCenterHttpApi.GetHashHexByHashByte.value
        payload = {
            'block_hash': block_hash
        }
        resp = self._post(url, payload)
        return resp

    def _get_full_block_by_height(self, height: int):
        url = ArchiveCenterHttpApi.GetFullBlockByHeight.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
            "height": height
        }
        resp = self._post(url, payload)
        return resp

    def _get_block_info_by_hash(self, block_hash: str):
        url = ArchiveCenterHttpApi.GetBlockInfoByHash.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
            "block_hash": block_hash
        }
        resp = self._post(url, payload)
        return resp

    def _get_block_info_by_tx_id(self, tx_id: str):
        url = ArchiveCenterHttpApi.GetBlockInfoByTxId.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
            "tx_id": tx_id
        }
        resp = self._post(url, payload)
        return resp

    def _get_full_transaction_info_by_txid(self, tx_id: str):
        url = ArchiveCenterHttpApi.GetTxByTxId.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
            "tx_id": tx_id
        }
        resp = self._post(url, payload)
        return resp

    def _get_truncate_tx_by_txid(self, tx_id: str, with_rwset: bool = False, truncate_length: int = 0,
                                 truncate_model: str = "hash"):
        """

        :param tx_id:
        :param with_rwset:
        :param truncate_length:
        :param truncate_model: hash/truncate/empty
        :return:
        """
        url = ArchiveCenterHttpApi.GetTruncateBlockByTxId.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
            "tx_id": tx_id,
            "with_rwset": with_rwset,
            "truncate_length": truncate_length,
            "truncate_model": truncate_model
        }
        resp = self._post(url, payload)
        return resp

    def _get_merklepath_by_txid(self, tx_id: str):
        url = ArchiveCenterHttpApi.GetMerklePathByTxId.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
            "tx_id": tx_id
        }
        resp = self._post(url, payload)
        return resp

    def _get_truncate_block_by_height(self, height: int, with_rwset: bool = False, truncate_length: int = 0,
                                      truncate_model: str = "hash"):
        """

        :param tx_id:
        :param with_rwset:
        :param truncate_length:
        :param truncate_model: hash/truncate/empty
        :return:
        """
        url = ArchiveCenterHttpApi.GetTruncateBlockByHeight.value
        payload = {
            "chain_genesis_hash": self.chain_genesis_hash,
            "height": height,
            "with_rwset": with_rwset,
            "truncate_length": truncate_length,
            "truncate_model": truncate_model
        }
        resp = self._post(url, payload)
        return resp

    def _post(self, path: str, payload: dict) -> dict:
        url = '%s%s' % (self.base_url, path)
        resp = self.session.post(url, json=payload)
        return resp.json()
