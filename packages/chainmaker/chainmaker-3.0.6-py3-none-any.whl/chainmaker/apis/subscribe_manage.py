#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   subscribe.py
# @Function     :   ChainMaker 订阅接口
from typing import List, Callable, Iterable, Union, Dict

from chainmaker.apis.base_client import BaseClient
from chainmaker.keys import ParamKey, SystemContractName, SubscribeManageMethod
from chainmaker.protos.common.block_pb2 import BlockInfo, BlockHeader
from chainmaker.protos.common.request_pb2 import Payload
from chainmaker.protos.common.result_pb2 import ContractEventInfoList
from chainmaker.protos.common.transaction_pb2 import Transaction
from chainmaker.protos.store.store_pb2 import BlockWithRWSet
from chainmaker.sdk_config import DefaultConfig
from chainmaker.utils import common


class SubscribeManageMixIn(BaseClient):
    """订阅管理操作"""

    # 09-00 订阅区块
    def subscribe_block(self, start_block: int, end_block: int, with_rw_set=False, only_header=False,
                        timeout: int = None, callback: Callable = None) -> None:
        """
        订阅区块
        :param start_block: 订阅的起始区块
        :param end_block: 订阅的结束区块
        :param with_rw_set: 是否包含读写集
        :param only_header: 是否只订阅区块头
        :param timeout: 订阅尚未产生区块的等待超时时间, 默认60s
        :param callback: 回调函数
        :return 回调函数返回值
        """
        callback = callback or self._callback
        self._debug("begin to SubscribeBlock, [start_block:%s]/[end_block:%s]" % (
            start_block, end_block))
        payload = self._create_subscribe_block_payload(start_block, end_block, with_rw_set, only_header)
        if timeout is None:
            timeout = None
        response_iterator = self._get_subscribe_stream(payload, timeout)
        for response in response_iterator:
            if only_header is True:
                msg_obj = BlockHeader()
            elif with_rw_set is True:
                msg_obj = BlockWithRWSet()
            else:
                msg_obj = BlockInfo()

            msg_obj.ParseFromString(response.data)

            callback(msg_obj)
            # yield msg_obj

    # 09-01 订阅交易
    def subscribe_tx(self, start_block: int, end_block: int, contract_name: str = None, tx_ids: List[str] = None,
                     timeout: int = None, callback: Callable = None) -> None:
        """
        订阅交易
        :param start_block: 订阅的起始区块
        :param end_block: 订阅的结束区块
        :param contract_name: 交易所属合约名称
        :param tx_ids: 指定交易Id列表进行订阅
        :param timeout: RPC请求超时时间
        :param callback: 回调函数
        :return 回调函数返回值
        """
        callback = callback or self._callback
        self._debug("begin to SubscribeTx, [contract_name:%s]/[tx_ids:%s]" % (contract_name, tx_ids))
        payload = self._create_subscribe_tx_payload(start_block, end_block, contract_name, tx_ids)
        response_iterator = self._get_subscribe_stream(payload, timeout)
        for response in response_iterator:
            transaction = Transaction()
            transaction.ParseFromString(response.data)
            callback(transaction)

    # 09-02 订阅合约事件
    def subscribe_contract_event(self, start_block, end_block, topic: str, contract_name: str,
                                 timeout: int = None, callback: Callable = None) -> None:
        """
        订阅合约事件
        :param start_block: 订阅的起始区块
        :param end_block: 订阅的结束区块
        :param topic: 订阅待事件主题
        :param contract_name: 事件所属合约名称
        :param timeout: RPC请求超时时间
        :param callback: 回调函数
        :return 回调函数返回值
        """
        callback = callback or self._callback
        self._debug("begin to SubscribeContractEvent, [contract_name:%s]/[topic:%s]" % (
            contract_name, topic))
        payload = self._create_subscribe_contract_event_payload(start_block, end_block, contract_name, topic)
        response_iterator = self._get_subscribe_stream(payload, timeout)

        for response in response_iterator:
            contract_event_info_list = ContractEventInfoList()
            contract_event_info_list.ParseFromString(response.data)
            # yield contract_event_info_list
            callback(contract_event_info_list)

    def subscribe(self, payload: Payload, timeout: int = None,
                  callback: Callable = None) -> None:
        """
        订阅区块、交易、合约事件
        :param payload: 订阅Payload
        :param timeout: 订阅待产生区块等待超时时间
        :param callback: 回调函数，默认为self._callback
        :return 回调函数返回值
        """
        callback = callback or self._callback
        response_iterator = self._get_subscribe_stream(payload, timeout)
        for response in response_iterator:
            callback(response.data)

    def _create_subscribe_payload(self, method: str, params: Dict[str, Union[str, int, bool]] = None) -> Payload:
        return self._payload_builder.create_subscribe_payload(SystemContractName.SUBSCRIBE_MANAGE.name, method, params)

    def _create_subscribe_block_payload(self, start_block: int, end_block: int, with_rw_set=False,
                                        only_header=False) -> Payload:
        """
        创建订阅区块请求负荷
        :param start_block: 订阅的起始区块
        :param end_block: 订阅的结束区块
        :param with_rw_set: 是否包含读写集
        :param only_header: 是否只订阅区块头
        :return: 请求负荷
        """
        params = {
            ParamKey.START_BLOCK.name: common.int64_to_bytes(start_block),
            ParamKey.END_BLOCK.name: common.int64_to_bytes(end_block),
            ParamKey.WITH_RWSET.name: with_rw_set,
            ParamKey.ONLY_HEADER.name: only_header,
        }
        return self._create_subscribe_payload(SubscribeManageMethod.SUBSCRIBE_BLOCK.name, params)

    def _create_subscribe_tx_payload(self, start_block: int, end_block: int, contract_name: str,
                                     tx_ids: List[str]) -> Payload:
        """
        创建订阅区块交易请求负荷
        :param start_block: 订阅的起始区块
        :param end_block: 订阅的结束区块
        :param contract_name: 合约名称
        :param tx_ids: 交易id列表
        :return:
        """
        tx_ids = tx_ids or []
        contract_name = contract_name or ''
        params = {
            ParamKey.START_BLOCK.name: common.int64_to_bytes(start_block),
            ParamKey.END_BLOCK.name: common.int64_to_bytes(end_block),
            ParamKey.CONTRACT_NAME.name: contract_name,
            ParamKey.TX_IDS.name: ','.join(tx_ids),
        }
        return self._create_subscribe_payload(SubscribeManageMethod.SUBSCRIBE_TX.name, params)

    def _create_subscribe_contract_event_payload(self, start_block: int, end_block: int,
                                                 contract_name: str, topic: str) -> Payload:
        """
        创建订阅合约事件请求负荷
        :param start_block: 订阅的起始区块
        :param end_block: 订阅的结束区块
        :param contract_name: 合约名称
        :param topic: 主题
        :return: 请求负荷
        """
        params = {
            ParamKey.START_BLOCK.name: common.int64_to_bytes(start_block),
            ParamKey.END_BLOCK.name: common.int64_to_bytes(end_block),
            ParamKey.TOPIC.name: topic,
            ParamKey.CONTRACT_NAME.name: contract_name,
        }
        return self._create_subscribe_payload(SubscribeManageMethod.SUBSCRIBE_CONTRACT_EVENT.name, params)

    def _get_subscribe_stream(self, payload: Payload, timeout: int = None) -> Iterable:
        """
        获取可迭代的订阅流数据
        :param payload: 请求负荷
        :return: 可迭代的订阅流数据 grpc._channel._MultiThreadedRendezvous对象, 已知所有订阅信息产生(达到集合点)后才返回全部数据
        """
        if timeout is None:
            timeout = DefaultConfig.subscribe_timeout
        request = self._generate_tx_request(payload)
        response_iterator = self._get_client(conn_node=self._conn_node).Subscribe(request, timeout)
        return response_iterator

    @staticmethod
    def _callback(data: bytes):
        """示例回调方法"""
        print('receive data', data)
