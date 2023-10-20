#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   dpos.py
# @Function     :   ChainMaker DPOS ERC20 / DPOS Stake 等操作接口
import json
from typing import Union

from chainmaker.apis.base_client import BaseClient
from chainmaker.keys import (SystemContractName, ParamKey, DposSlashingMethod)
from chainmaker.protos.common.request_pb2 import Payload
from chainmaker.protos.common.result_pb2 import TxResponse


class DPosSlashingMixIn(BaseClient):
    """DPos共识惩罚操作"""

    # 15-00 创建惩罚待签名Payload
    # def create_punish_payload(self) -> Payload:  # todo 参数
    #     """
    #     创建惩罚待签名Payload
    #     <15-00-DPOS_SLASHING-PUNISH>
    #     :return:
    #     """
    #     raise NotImplementedError("待实现")
    #     self._debug('begin to create [DPOS_SLASHING-PUNISH] to be signed payload')
    #     payload = self._payload_builder.create_invoke_payload(SystemContractName.DPOS_SLASHING.name,
    #                                                           DposSlashingMethod.PUNISH.name)
    #     return payload

    # 15-02 创建设置区块惩罚数量待签名Payload
    def create_set_slashing_per_block_payload(self, slashing_per_block: int) -> Payload:
        """
        创建设置区块惩罚数量待签名Payload
        <15-02-DPOS_SLASHING-SET_SLASHING_PER_BLOCK>
        :return:
        """
        self._debug('begin to create [DPOS_SLASHING-SET_SLASHING_PER_BLOCK] to be signed payload')
        params = {
            ParamKey.slashing_per_block.name: slashing_per_block
        }
        payload = self._payload_builder.create_invoke_payload(SystemContractName.DPOS_SLASHING.name,
                                                              DposSlashingMethod.SET_SLASHING_PER_BLOCK.name, params)
        return payload

    # 15-03 获取区块惩罚数量
    def get_slashing_per_block(self) -> int:
        """
        获取区块惩罚数量
        <15-03-DPOS_SLASHING-GET_SLASHING_PER_BLOCK>
        :return:
        """
        self._debug('begin to get slashing per block')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_SLASHING.name,
                                                             DposSlashingMethod.GET_SLASHING_PER_BLOCK.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data) if data else 0

    # 15-04 查询惩罚账户余额
    def get_slashing_balance(self) -> int:
        """
        查询惩罚账户余额
        <15-04-DPOS_SLASHING-GET_SLASHING_ADDRESS_BALANCE>
        :return:
        """
        self._debug('begin to get slashing balance')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_SLASHING.name,
                                                             DposSlashingMethod.GET_SLASHING_ADDRESS_BALANCE.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data) if data else 0

    # 15-05 通过世代Id获取惩罚数据
    def get_slashing_by_epoch_id(self, epoch_id: str) -> Union[dict, None]:
        """
        通过世代Id获取惩罚数据
        <15-05-DPOS_SLASHING-GET_SLASHING_DETAIL>
        :return:
        """
        self._debug('begin to get slashing detail')
        params = {
            ParamKey.epoch_id.name: epoch_id
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_SLASHING.name,
                                                             DposSlashingMethod.GET_SLASHING_DETAIL.name,
                                                             params)
        response = self.send_request(payload)
        data = response.contract_result.result
        return json.loads(data) if data else None

    # 15-06 查询惩罚账户地址
    def get_slashing_address(self) -> str:
        """
        <15-06-DPOS_SLASHING-GET_SLASHING_ADDRESS>
        :return:
        """
        self._debug('begin to get slashing contract address')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_SLASHING.name,
                                                             DposSlashingMethod.GET_SLASHING_ADDRESS.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return data.decode()


class DPosSlashingWithEndorsers(BaseClient):
    # 15-00 惩罚
    # def punish(self, timeout: int = None, with_sync_result: bool = None) -> TxResponse:  # todo 参数
    #     """
    #     惩罚
    #     <15-00-DPOS_SLASHING-PUNISH>
    #     :param timeout: RPC请求超时时间
    #     :param with_sync_result: 是否同步轮询交易结果
    #     :return: 交易响应
    #     """
    #     raise NotImplementedError("待实现")
    #     payload = self.create_punish_payload()
    #     tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
    #     return tx_response

    # 15-01 设置区块惩罚数量
    def set_slashing_per_block(self, slashing_per_block: int, timeout: int = None,
                               with_sync_result: bool = None) -> TxResponse:
        """
        设置区块惩罚数量
        <15-02-DPOS_SLASHING-SET_SLASHING_PER_BLOCK>
         :param slashing_per_block:
         :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        payload = self.create_set_slashing_per_block_payload(slashing_per_block)
        tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return tx_response
