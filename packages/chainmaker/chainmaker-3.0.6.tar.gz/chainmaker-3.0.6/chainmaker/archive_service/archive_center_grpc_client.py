#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   archive_center_grpc_client.py
# @Function     :   归档中心gRPC客户端
# v2.3.2 新增
from typing import Callable, Iterable

import grpc

from chainmaker.archive_service.archive_service import ArchiveService
from chainmaker.exceptions import ChainClientException
from chainmaker.protos.archivecenter.archivecenter_pb2 import ArchiveBlockRequest, ArchiveStatusRequest, \
    ArchiveStatusResp, \
    BlockByHashRequest, BlockByHeightRequest, BlockByTxIdRequest, OperationByHeight
from chainmaker.protos.archivecenter.archivecenter_pb2_grpc import ArchiveCenterServerStub
from chainmaker.protos.common.block_pb2 import BlockInfo
from chainmaker.protos.common.transaction_pb2 import TransactionInfo, TransactionInfoWithRWSet
from chainmaker.protos.config.chain_config_pb2 import ChainConfig
from chainmaker.sdk_config import ArchiveCenterConfig
from chainmaker.utils.crypto_utils import merge_cert_pems


class ArchiveCenterGrpcClient(ArchiveService):
    def __init__(self, cc, archive_center_config: ArchiveCenterConfig):
        super().__init__(cc)
        self.archive_center_config = archive_center_config
        self.chain_genesis_hash = self.archive_center_config.chain_genesis_hash
        self.rpc_address = self.archive_center_config.rpc_address

    def get_tx_by_tx_id(self, tx_id: str) -> TransactionInfo:
        self.logger.debug("[SDK] begin to GetTxByTxId rom archive center by grpc, [tx_id:%s]", tx_id)
        request = BlockByTxIdRequest(chain_unique=self.chain_genesis_hash, tx_id=tx_id)
        transaction_resp = self._get_client().GetTxByTxId(request)
        print(transaction_resp)
        transaction = transaction_resp.transaction
        tx_info = TransactionInfo(transaction=transaction)  # todo  block height etc
        return tx_info

    def get_tx_with_rwset_by_tx_id(self, tx_id: str) -> TransactionInfoWithRWSet:
        self.logger.debug("[SDK] begin to GetTxWithRWSetByTxId from archive center by grpc, [tx_id:%s]", tx_id)
        request = BlockByTxIdRequest(chain_unique=self.chain_genesis_hash, tx_id=tx_id)
        transaction_resp = self._get_client().GetTxByTxId(request)
        tx_rw_set_resp = self._get_client().GetTxRWSetByTxId(request)
        tx_info_with_rw_set = TransactionInfoWithRWSet(transaction=transaction_resp.transaction,
                                                       rw_set=tx_rw_set_resp.tx_rw_set_resp)  # todo block height etc
        return tx_info_with_rw_set

    def get_block_by_height(self, block_height: int, with_rw_set: bool = False) -> BlockInfo:
        self.logger.debug(
            "[SDK] begin to GetBlockByHeight from archive center by grpc, [block_height:%d]/[with_rw_set:%s]",
            block_height,
            with_rw_set,
        )
        request = BlockByHeightRequest(chain_unique=self.chain_genesis_hash, height=block_height,
                                       operation=OperationByHeight.OperationGetBlockByHeight)
        block_with_rw_set_resp = self._get_client().GetBlockByHeight(request)
        block_info = block_with_rw_set_resp.block_data
        return block_info

    def get_block_by_hash(self, block_hash: str, with_rw_set: bool = False) -> BlockInfo:
        self.logger.debug(
            "[SDK] begin to GetBlockByHash from archive center by grpc, [block_hash:%s]/[with_rw_set:%s]",
            block_hash,
            with_rw_set,
        )

        request = BlockByHashRequest(chain_unique=self.chain_genesis_hash, block_hash=block_hash,
                                     operation=OperationByHeight.OperationGetBlockByHeight)
        block_with_rw_set_resp = self._get_client().GetBlockByHash(request)
        block_info = block_with_rw_set_resp.block_data
        return block_info

    def get_block_by_tx_id(self, tx_id: str, with_rw_set: bool = False) -> BlockInfo:
        self.logger.debug(
            "[SDK] begin to GetBlockByTxId from archive center by grpc, [tx_id:%s]/[with_rw_set:%s]",
            tx_id,
            with_rw_set,
        )

        request = BlockByTxIdRequest(chain_unique=self.chain_genesis_hash, tx_id=tx_id)
        block_with_rw_set_resp = self._get_client().GetBlockByTxId(request)
        block_info = block_with_rw_set_resp.block_data
        return block_info

    def get_chain_config_by_block_height(self, block_height: int) -> ChainConfig:
        self.logger.debug(
            "[SDK] begin to get chain config by block height from archive center by grpc [%d]", block_height
        )

    def register(self, genesis: BlockInfo) -> None:
        self.logger.debug(
            "[SDK] begin to register genesis block to archive center by grpc",
        )
        request = ArchiveStatusRequest(chain_unique=self.chain_genesis_hash)
        try:
            response = self._get_client().Register(request)
        except Exception as ex:
            self.logger.exception(ex)
            raise ChainClientException('register genesis hash failed: %s' % ex)

        if response.code != 0:
            genesis_hash = genesis.block.header.block_hash.hex()
            request = ArchiveBlockRequest(chain_unique=genesis_hash, block=genesis)
            try:
                response = self._get_client().Register(request)
            except Exception as ex:
                self.logger.exception(ex)
                raise ChainClientException('register genesis hash with block failed: %s' % ex)
            if response.code != 0:
                raise ChainClientException('register genesis hash with block failed: [code: %d]' % response.code)

    def archive_block(self, block: BlockInfo) -> None:
        block_height = block.block.header.block_height
        self.logger.debug(
            "[SDK] begin to archive block %d to archive center by grpc" % block_height,
        )
        request = ArchiveBlockRequest(chain_unique=self.chain_genesis_hash, block=block)
        try:
            response = self._get_client().Register(request)
        except Exception as ex:
            self.logger.exception(ex)
            raise ChainClientException('archive block %d to archive center failed: %s' % (block_height, ex))
        if response.code != 0:
            raise ChainClientException(
                'archive block %d to archive center failed: [code: %d]' % (block_height, response.code))

    def archive_blocks(self, blocks: Iterable, notice: Callable = None) -> None:
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
        self.logger.debug("[SDK] get archived status from archive center by grpc")
        request = ArchiveStatusRequest(chain_unique=self.chain_genesis_hash)
        response = self._get_client().GetArchivedStatus(request)
        return response

    def _get_client(self) -> ArchiveCenterServerStub:
        tls_enable = self.archive_center_config.tls_enable
        tls = self.archive_center_config.tls
        rpc_address = self.archive_center_config.rpc_address
        opts = []

        if tls_enable:
            root_certificates = merge_cert_pems(ca_paths=tls.trust_ca_list)
            with open(tls.priv_key_file, 'rb') as f:
                private_key = f.read()
            with open(tls.cert_file, 'rb') as f:
                certificate_chain = f.read()
            credential = grpc.ssl_channel_credentials(root_certificates=root_certificates,
                                                      private_key=private_key,
                                                      certificate_chain=certificate_chain)
            if tls.server_name:
                opts.append(('grpc.ssl_target_name_override', tls.server_name))
            channel = grpc.secure_channel(rpc_address, credential, options=opts)

        else:
            channel = grpc.insecure_channel(rpc_address, options=opts)

        return ArchiveCenterServerStub(channel=channel)
