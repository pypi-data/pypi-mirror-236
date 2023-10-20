#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   system_contract.py
# @Function     :   ChainMaker系统合约(链获取相关)接口
import random
from typing import Dict, Union, List

from chainmaker.apis.base_client import BaseClient
from chainmaker.keys import (ParamKey, SystemContractName, ChainQueryMethod)
from chainmaker.protos.common.block_pb2 import BlockHeader, BlockInfo
from chainmaker.protos.common.contract_pb2 import Contract
from chainmaker.protos.common.request_pb2 import Payload
from chainmaker.protos.common.result_pb2 import TxResponse
from chainmaker.protos.common.transaction_pb2 import (
    TransactionInfo,
    TransactionInfoWithRWSet, )
from chainmaker.protos.discovery.discovery_pb2 import ChainInfo, ChainList
from chainmaker.protos.store.store_pb2 import BlockWithRWSet


class ChainQueryMixIn(BaseClient):
    """链查询操作"""
    # 01-00 通过交易Id获取交易所在区块信息
    def get_block_by_tx_id(self, tx_id: str, with_rw_set: bool = False) -> BlockInfo:
        """
        通过交易Id获取交易所在区块信息
        <01-00-CHAIN_QUERY-GET_BLOCK_BY_TX_ID>
        :param tx_id: 交易Id
        :param with_rw_set: 是否返回读写集数据
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        self._debug("begin to GetBlockByTxId, [tx_id:%s]/[with_rw_set:%s]" % (tx_id, with_rw_set))
        if self.archive_center_query_first is True:
            try:
                return self.archive_service.get_block_by_tx_id(tx_id, with_rw_set)
            except Exception as ex:
                self._logger.exception(ex)

        params = {ParamKey.txId.name: tx_id,
                  ParamKey.withRWSet.name: with_rw_set}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_BLOCK_BY_TX_ID.name, params)

        response = self.send_request(payload)
        return self._parse_block_info(response)

    def _get_tx_by_tx_id(self, tx_id: str) -> TransactionInfo:
        """
        通过交易Id获取交易信息
        <01-01-CHAIN_QUERY-GET_TX_BY_TX_ID>
        :param tx_id: 交易Id，类型为字符串
        :return: Result
        :raises RequestError: 请求失败
        """
        params = {ParamKey.txId.name: tx_id}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_TX_BY_TX_ID.name, params)

        tx_response = self.send_request(payload)
        data = tx_response.contract_result.result

        transaction_info = TransactionInfo()
        transaction_info.ParseFromString(data)
        return transaction_info

    # 01-01 通过交易Id获取交易信息
    def get_tx_by_tx_id(self, tx_id: str) -> TransactionInfo:
        """
        通过交易Id获取交易信息
        <01-01-CHAIN_QUERY-GET_TX_BY_TX_ID>
        :param tx_id: 交易Id，类型为字符串
        :return: Result
        :raises RequestError: 请求失败
        """
        self._debug("begin to get tx by tx id, [tx_id:%s]" % tx_id)
        if self.archive_center_query_first is True:
            try:
                return self.archive_service.get_tx_by_tx_id(tx_id)
            except Exception as ex:
                self._logger.exception(ex)
        return self._get_tx_by_tx_id(tx_id)

    # 01-02 通过区块高度获取区块信息
    def get_block_by_height(self, block_height: int, with_rw_set: bool = False) -> BlockInfo:
        """
        通过区块高度获取区块信息
        <01-02-CHAIN_QUERY-GET_BLOCK_BY_HEIGHT>
        :param block_height: 区块高度
        :param with_rw_set: 是否返回读写集数据, 默认不返回。
        :return: 区块信息BlockInfo对象
        :raises RequestError: 请求失败，块已归档是抛出ContractFile
        """

        self._debug("begin to get block by height, [block_height:%s]/[with_rw_set:%s]" % (block_height, with_rw_set))
        if self.archive_center_query_first is True:
            try:
                return self.archive_service.get_block_by_height(block_height, with_rw_set)
            except Exception as ex:
                self._logger.exception(ex)

        params = {
            ParamKey.blockHeight.name: block_height,
            ParamKey.withRWSet.name: with_rw_set
        }
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_BLOCK_BY_HEIGHT.name, params)
        response = self.send_request(payload)
        return self._parse_block_info(response)

    # 01-03 获取链信息
    def get_chain_info(self) -> ChainInfo:
        """
        获取链信息
        <01-03-CHAIN_QUERY-GET_CHAIN_INFO>
        :return: ChainInfo
        :raises RequestError: 请求失败
        """
        self._debug('begin to GetChainInfo')
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_CHAIN_INFO.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        chain_info = ChainInfo()
        chain_info.ParseFromString(data)
        return chain_info

    def get_tx_with_rwset_by_tx_id(self, tx_id: str) -> TransactionInfoWithRWSet:
        """
        通过交易Id获取带读写集交易信息
        :param tx_id: 交易Id，类型为字符串
        :return: Result
        :raises RequestError: 请求失败
        """
        self._debug("begin to get tx with rwset by tx id [tx_id:%s]" % tx_id)
        if self.archive_center_query_first is True:
            try:
                return self.archive_service.get_tx_with_rwset_by_tx_id(tx_id)
            except Exception as ex:
                self._logger.exception(ex)

        params = {ParamKey.txId.name: tx_id,
                  ParamKey.withRWSet.name: True}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_TX_BY_TX_ID.name, params)

        response = self.send_request(payload)

        data = response.contract_result.result
        transaction_info = TransactionInfoWithRWSet()
        transaction_info.ParseFromString(data)

        return transaction_info

    # 01-04 获取最新的配置块
    def get_last_config_block(self, with_rw_set: bool = False) -> BlockInfo:
        """
        获取最新的配置块
        <01-04-CHAIN_QUERY-GET_LAST_CONFIG_BLOCK>
        :param with_rw_set: 是否返回读写集数据
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        self._debug("begin to get last config block [with_rw_set:%s]" % with_rw_set)

        params = {ParamKey.withRWSet.name: with_rw_set}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_LAST_CONFIG_BLOCK.name, params)
        response = self.send_request(payload)
        return self._parse_block_info(response)

    # 01-05 通过区块哈希获取区块信息
    def get_block_by_hash(self, block_hash: str, with_rw_set: bool = False) -> BlockInfo:
        """
        通过区块哈希获取区块信息
        <01-05-CHAIN_QUERY-GET_BLOCK_BY_HASH>
        :param block_hash: 区块Hash, 二进制hash.hex()值，
                           如果拿到的block_hash字符串是base64值, 需要用 base64.b64decode(block_hash).hex()
        :param with_rw_set: 是否返回读写集数据
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        self._debug("begin to get block by hash [block_hash:%s]/[with_rw_set:%s]" % (block_hash, with_rw_set))
        if self.archive_center_query_first is True:
            try:
                return self.archive_service.get_block_by_hash(block_hash, with_rw_set)
            except Exception as ex:
                self._logger.exception(ex)

        params = {ParamKey.blockHash.name: block_hash,
                  ParamKey.withRWSet.name: with_rw_set}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_BLOCK_BY_HASH.name,
                                                   params)

        response = self.send_request(payload)
        return self._parse_block_info(response)

    # 01-06 获取节点加入的链列表
    def get_node_chain_list(self) -> ChainList:
        """
        获取节点加入的链列表
        <01-06-CHAIN_QUERY-GET_NODE_CHAIN_LIST>
        :return: 链Id列表
        :raises RequestError: 请求失败
        """
        self._debug("begin to get node chain list")

        payload = self._create_chain_query_payload(ChainQueryMethod.GET_NODE_CHAIN_LIST.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        chain_list = ChainList()
        chain_list.ParseFromString(data)
        return chain_list

    # 01-07 获取统治合约
    def get_governance_contract(self):
        """
        获取统治合约
        <01-07-CHAIN_QUERY-GET_GOVERNANCE_CONTRACT>
        :return:
        """
        raise NotImplementedError('the method does not found')
        # self._debug("begin to GetGovernanceContract")
        #
        # payload = self._create_chain_query_payload(ChainQueryMethod.GET_GOVERNANCE_CONTRACT.name)
        # response = self.send_request(payload)
        #
        # data = response.contract_result.result
        # contract_data = json.loads(data)
        # return self._parse_contract(contract_data)

    # 01-08 通过区块高度获取带读写集区块信息
    def get_block_with_txrwsets_by_height(self, block_height: int) -> BlockWithRWSet:
        """
        通过区块高度获取带读写集区块信息
        <01-08-CHAIN_QUERY-GET_BLOCK_WITH_TXRWSETS_BY_HEIGHT>
        :param block_height: 区块高度
        :return: 带读写集区块信息
        """
        self._debug("begin to get block with rwsets by height [block_height:%s]" % block_height)
        params = {ParamKey.blockHeight.name: block_height}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_BLOCK_WITH_TXRWSETS_BY_HEIGHT.name, params)
        response = self.send_request(payload)
        data = response.contract_result.result
        block_info_with_rw_set = BlockWithRWSet()
        block_info_with_rw_set.ParseFromString(data)
        return block_info_with_rw_set

    # 01-09 通过区块哈希获取带读写集区块信息
    def get_block_with_txrwsets_by_hash(self, block_hash: str) -> BlockWithRWSet:
        """
        通过区块哈希获取带读写集区块信息
         <01-09-CHAIN_QUERY-GET_BLOCK_WITH_TXRWSETS_BY_HASH>
        :param block_hash: 区块哈希
        :return: 带读写集区块信息
        """
        self._debug("begin to get block with tx rwsets by hash [block_hash:%s]" % block_hash)

        params = {ParamKey.blockHash.name: block_hash}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_BLOCK_WITH_TXRWSETS_BY_HASH.name, params)

        response = self.send_request(payload)
        data = response.contract_result.result
        block_info_with_rw_set = BlockWithRWSet()
        block_info_with_rw_set.ParseFromString(data)
        return block_info_with_rw_set

    def _get_last_block(self, with_rw_set: bool = False) -> BlockInfo:
        """
        获取最新区块信息
        <01-10-CHAIN_QUERY-GET_LAST_BLOCK>
        :param with_rw_set: 是否返回读写集数据
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        params = {ParamKey.withRWSet.name: with_rw_set}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_LAST_BLOCK.name, params)
        response = self.send_request(payload)
        return self._parse_block_info(response)

    # 01-10 获取最新区块信息
    def get_last_block(self, with_rw_set: bool = False) -> BlockInfo:
        """
        获取最新区块信息
        <01-10-CHAIN_QUERY-GET_LAST_BLOCK>
        :param with_rw_set: 是否返回读写集数据
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        self._debug("begin to get last block [with_rw_set:%s]" % with_rw_set)
        return self._get_last_block(with_rw_set)

    # 01-11 通过区块高度获取完整区块信息
    def get_full_block_by_height(self, block_height: int) -> BlockWithRWSet:
        """
        通过区块高度获取完整区块信息
        <01-11-CHAIN_QUERY-GET_FULL_BLOCK_BY_HEIGHT>
        :param block_height: 区块高度
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        self._debug("begin to get full block by height [block_height:%s]" % block_height)

        params = {ParamKey.blockHeight.name: str(block_height)}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_FULL_BLOCK_BY_HEIGHT.name, params)
        response = self.send_request(payload)

        block_with_rw_set = BlockWithRWSet()
        block_with_rw_set.ParseFromString(response.contract_result.result)
        return block_with_rw_set

    # 01-12 通过交易Id获取区块高度
    def get_block_height_by_tx_id(self, tx_id: str) -> int:
        """
        通过交易Id获取区块高度
        <01-12-CHAIN_QUERY-GET_BLOCK_HEIGHT_BY_TX_ID>
        :param tx_id: 交易Id
        :return: 区块高度
        :raises RequestError: 请求失败
        """
        self._debug("begin to get block height by tx id [tx_id:%s]" % tx_id)

        params = {ParamKey.txId.name: tx_id}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_BLOCK_HEIGHT_BY_TX_ID.name, params)
        response = self.send_request(payload)

        block_height = response.contract_result.result

        return int(block_height)

    # 01-13 通过区块哈希获取区块高度
    def get_block_height_by_hash(self, block_hash: str) -> int:
        """
        通过区块哈希获取区块高度
        <01-13-CHAIN_QUERY-GET_BLOCK_HEIGHT_BY_HASH>
        :param block_hash: 区块Hash 二进制hash.hex()值,
               如果拿到的block_hash字符串是base64值, 需要用 base64.b64decode(block_hash).hex()
        :return: 区块高度
        :raises RequestError: 请求失败
        """
        self._debug("begin to get block height by hash [block_hash:%s]" % block_hash)

        params = {ParamKey.blockHash.name: block_hash}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_BLOCK_HEIGHT_BY_HASH.name, params)
        response = self.send_request(payload)
        block_height = response.contract_result.result
        return int(block_height)

    # 01-14 通过高度获取区块头
    def get_block_header_by_height(self, block_height: int) -> BlockHeader:
        """
        通过高度获取区块头
        <01-14-CHAIN_QUERY-GET_BLOCK_HEADER_BY_HEIGHT>
        :param block_height: 区块高度
        :return: 区块头
        """
        params = {ParamKey.blockHeight.name: block_height}
        self._debug("begin to get block header by height [block_height:%s]" % block_height)

        payload = self._create_chain_query_payload(ChainQueryMethod.GET_BLOCK_HEADER_BY_HEIGHT.name, params)
        response = self.send_request(payload)
        data = response.contract_result.result
        block_header = BlockHeader()
        block_header.ParseFromString(data)
        return block_header

    # 01-15 获取已归档的区块高度
    def get_archived_block_height(self) -> int:
        """
        获取已归档的区块高度
         <01-15-CHAIN_QUERY-GET_ARCHIVED_BLOCK_HEIGHT>
        :return: 区块高度
        :raises RequestError: 请求失败
        """
        self._debug("begin to get archived block height")
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_ARCHIVED_BLOCK_HEIGHT.name)
        response = self.send_request(payload)
        block_height = response.contract_result.result
        return int(block_height)

    # 01-16 获取全部合约信息
    # def get_all_contracts(self) -> List[Contract]:
    #     """
    #     获取全部合约信息
    #     <01-16-CHAIN_QUERY-GET_ALL_CONTRACTS>
    #     :return: 合约Contract对象列表
    #     :raise: RequestError: 请求出错
    #     :raise: AssertionError: 响应code不为0,检查响应时抛出断言失败
    #     :raise: 当数据不是JSON格式时，抛出json.decoder.JSONDecodeError
    #     """
    #     raise NotImplementedError('the method does not found')
        # self._debug("begin to GetAllContracts")
        # payload = self._create_chain_query_payload(ChainQueryMethod.GET_ALL_CONTRACTS.name)
        #
        # response = self.send_request(payload)
        # contract_list = json.loads(response.contract_result.result)
        # contracts = [self._parse_contract(contract_data) for contract_data in contract_list]
        # return contracts

    # 01-17 获取交易存在性证明
    def get_merkle_path_by_tx_id(self, tx_id: str) -> bool:
        """
        获取交易存在性证明
        <01-17-CHAIN_QUERY-GET_MERKLE_PATH_BY_TX_ID>
        :param tx_id: 交易Id
        :return: 交易是否存在
        """
        self._debug("begin to get merkle path by tx id [tx_id:%s]" % tx_id)
        params = {ParamKey.txId.name: tx_id}
        payload = self._create_chain_query_payload(ChainQueryMethod.GET_MERKLE_PATH_BY_TX_ID.name, params)
        response = self.send_request(payload)
        return True if response.contract_result.result else False

    def get_block_height(self, tx_id: str = None, block_hash: str = None) -> int:  # todo
        """
        通过交易Id或区块hash获取区块高度
        :param tx_id: 交易Id
        :param block_hash: 区块hash
        :return: 区块高度
        """
        if tx_id is None and block_hash is None:
            raise ValueError('[Sdk] tx_id or block_hash can not be empty')
        return self.get_block_height_by_tx_id(tx_id) if tx_id else self.get_block_height_by_hash(block_hash)

    def get_current_block_height(self) -> int:
        """
        获取当前区块高度
        :return: 区块高度
        """
        self._debug("begin to get current block height")
        return self._get_last_block(with_rw_set=False).block.header.block_height

    def _create_chain_query_payload(self, method: str, params: Dict[str, Union[str, int, bool]] = None) -> Payload:
        """
        创建链获取待签名请求
        :param method: 链获取方法
        :param params: 获取参数
        :return: 待签名Payload
        """
        return self._payload_builder.create_query_payload(SystemContractName.CHAIN_QUERY.name, method, params)

    @staticmethod
    def _parse_block_info(response: TxResponse) -> BlockInfo:
        data = response.contract_result.result
        block_info = BlockInfo()
        block_info.ParseFromString(data)
        return block_info


class ChainQueryExtras(BaseClient):
    def get_block_timestamp_by_height(self, block_height: int = None) -> int:
        """
        通过区块高度获取区块时间戳
        :param block_height: 区块高度
        :return: 区块时间戳
        """
        if block_height is None:
            block_height = self.get_current_block_height()
        self._debug('begin to get block timestamp by height [block_height:%s]' % block_height)
        return self.get_block_header_by_height(block_height).block_timestamp

    def get_block_hash_by_height(self, block_height: int) -> str:
        """
        通过区块高度查询区块哈希
        :param block_height: 区块高度
        :return: 区块哈希
        """
        self._debug('begin to get block hash by height [block_height:%s]' % block_height)
        block_info = self.get_block_by_height(block_height)
        return block_info.block.header.block_hash.hex()

    def get_last_block_hash(self) -> str:
        """
        获取最新区块哈希
        :return: 最新区块哈希
        """
        self._debug('begin to get last block hash')
        block_info = self.get_last_block()
        return block_info.block.header.block_hash.hex()

    def get_last_block_tx_ids(self) -> List[str]:
        """
        获取最新区块交易Id列表
        :return: 交易Id列表
        """
        self._debug('begin to get last block tx ids')
        block_info = self.get_last_block()
        txs = block_info.block.txs
        return [tx.payload.tx_id for tx in txs]

    def get_any_tx_id(self) -> str:
        """
        获取链上存在的任意交易Id
        :return: 链上某一交易Id
        """
        self._debug('begin to get any available tx id on chain')
        block_height = self.get_any_block_height()
        block_info = self.get_block_by_height(block_height)
        tx = random.choice(block_info.block.txs)
        return tx.payload.tx_id

    def get_any_block_height(self) -> int:
        """
        获取链上存在的任意区块高度
        :return: 链上某一区块高度
        """
        self._debug('begin to get any available block height on chain')
        current_block_height = self.get_current_block_height()
        if current_block_height == 0:
            return current_block_height
        return random.choice(list(range(current_block_height)))

    def get_any_block_hash(self) -> str:
        """
        获取链上存在的任意区块哈希
        :return: 区块哈希
        """
        self._debug('begin to get any available block hash on chain')
        block_height = self.get_any_block_height()
        return self.get_block_hash_by_height(block_height)

    def get_tx_count(self, start_block: int, end_block: int = None) -> int:
        """
        获取交易数量
        :param start_block: 起始区块高度(包括)
        :param end_block: 结束区块高度(包括), 为None是为当前区块高度
        :return: 交易数量
        """
        self._debug('begin to get tx count [start_block:%s]/[end_block:%s]' % (start_block, end_block))
        current_block_height = self.get_current_block_height()
        if end_block is None:
            end_block = current_block_height
            assert end_block >= start_block, '[SDK] 结束区块高度应大于等于起始区块高度'
            assert end_block <= current_block_height, '[SDK] 结束区块高度应小于等于当前区块高度'
        sum = 0
        for block_height in range(start_block + 1, end_block + 1):
            block_header = self.get_block_header_by_height(block_height)
            sum += block_header.tx_count
        return sum

    def get_tx_statistic_data(self, start_block: int, end_block: int = None) -> dict:
        """
        获取交易数量
        :param start_block: 起始区块高度(包括)
        :param end_block: 结束区块高度(包括), 为None是为当前区块高度
        :return: 交易数量
        """
        start_timestamp = self.get_block_timestamp_by_height(start_block)

        tx_count = 0
        last_block_timestamp = start_timestamp
        tps_list = []
        for block_height in range(start_block + 1, end_block + 1):
            block_header = self.get_block_header_by_height(block_height)
            block_timestamp = block_header.block_timestamp
            current_block_elapsed = block_timestamp - last_block_timestamp
            current_tx_count = block_header.tx_count
            if current_tx_count != 0:
                current_tps = current_tx_count / current_block_elapsed
                tps_list.append(current_tps)

            tx_count += current_tx_count
            last_block_timestamp = block_timestamp

        end_timestamp = last_block_timestamp

        total_block = end_block - start_block
        elapsed = end_timestamp - start_timestamp
        tx_avg = tx_count / total_block if total_block else None
        tps_avg = sum(tps_list) / len(tps_list)

        return dict(start_block=start_block, end_block=end_block, total_block=total_block, elapsed=elapsed,
                    tx_count=tx_count, tx_avg=tx_avg, tps_avg=tps_avg)
