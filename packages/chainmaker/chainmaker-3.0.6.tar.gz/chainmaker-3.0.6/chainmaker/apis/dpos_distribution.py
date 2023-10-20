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
from chainmaker.keys import (SystemContractName, ParamKey, DposDistributionMethod)
from chainmaker.protos.common.request_pb2 import Payload
from chainmaker.protos.common.result_pb2 import TxResponse


class DPosDistributionMixIn(BaseClient):
    """DPos共识奖励操作"""

    # 14-00 奖励
    def create_reward_payload(self) -> Payload:  # todo
        """
        <14-00-DPOS_DISTRIBUTION-REWARD>
        :return:
        """
        self._debug('begin to create [DPOS_DISTRIBUTION-REWARD] to be signed payload')
        payload = self._payload_builder.create_invoke_payload(SystemContractName.DPOS_DISTRIBUTION.name,
                                                              DposDistributionMethod.REWARD.name)
        return payload

    # 14-01 根据世代Id获取奖励
    def get_distribution_by_epoch_id(self, epoch_id: str) -> Union[dict, None]:
        """
        <14-01-DPOS_DISTRIBUTION-GET_DISTRIBUTION_DETAIL>
        :return:
        """
        self._debug('begin to get distribution detail')
        params = {
            ParamKey.epoch_id.name: epoch_id
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_DISTRIBUTION.name,
                                                             DposDistributionMethod.GET_DISTRIBUTION_DETAIL.name,
                                                             params)
        response = self.send_request(payload)
        data = response.contract_result.result
        return json.loads(data) if data else None

    # 14-02 创建设置每个区块奖励数量待签名Payload
    def create_set_distribution_per_block_payload(self, distribution_per_block: int) -> Payload:
        """
        创建设置每个区块奖励数量待签名Payload
        <14-02-DPOS_DISTRIBUTION-SET_DISTRIBUTION_PER_BLOCK>
        :return:
        """
        self._debug('begin to create [DPOS_DISTRIBUTION-SET_DISTRIBUTION_PER_BLOCK] to be signed payload')
        params = {
            ParamKey.distribution_per_block.name: distribution_per_block
        }
        payload = self._payload_builder.create_invoke_payload(SystemContractName.DPOS_DISTRIBUTION.name,
                                                              DposDistributionMethod.SET_DISTRIBUTION_PER_BLOCK.name,
                                                              params)
        return payload

    # 14-03 获取每个区块奖励数量
    def get_distribution_per_block(self) -> int:
        """
        获取每个区块奖励数量
        <14-03-DPOS_DISTRIBUTION-GET_DISTRIBUTION_PER_BLOCK>
        :return:
        """
        self._debug('begin to get distribution per block')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_DISTRIBUTION.name,
                                                             DposDistributionMethod.GET_DISTRIBUTION_PER_BLOCK.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data) if data else 0

    # 14-04 创建设置从惩罚而来的奖励数量待签名Payload
    # def create_set_distribution_from_slashing_payload(self, distribution_from_slashing: int) -> Payload:
    #     """
    #     <14-04-DPOS_DISTRIBUTION-SET_DISTRIBUTION_FROM_SLASHING>
    #     :return:
    #     """
    #     raise NotImplementedError("待实现")
    #     self._debug('begin to create [DPOS_DISTRIBUTION-SET_DISTRIBUTION_FROM_SLASHING] to be signed payload')
    #     params = {
    #         ParamKey.slashing_per_block.name: slashing_per_block
    #     }
    #     payload = self._payload_builder.create_invoke_payload(SystemContractName.DPOS_DISTRIBUTION.name,
    #                                                           DposDistributionMethod.SET_DISTRIBUTION_FROM_SLASHING.name,
    #                                                           params)
    #     return payload

    # 14-05 获取从惩罚而来的奖励数量
    # def get_distribution_from_slashing(self) -> str:  # todo  sdk-go无该方法
    #     """
    #     <14-05-DPOS_DISTRIBUTION-GET_DISTRIBUTION_FROM_SLASHING>
    #     :return:
    #     """
    #     raise NotImplementedError("待实现")
    #     self._debug('begin to get distribution for slashing')
    #     payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_DISTRIBUTION.name,
    #                                                          DposDistributionMethod.GET_DISTRIBUTION_FROM_SLASHING.name)
    #     response = self.send_request(payload)
    #     data = response.contract_result.result
    #     return data.decode

    # 14-06 创建设置Gas转换率待签名Payload
    def create_set_gas_exchange_rate_payload(self, gas_exchange_rate: int) -> Payload:
        """
        <14-06-DPOS_DISTRIBUTION-SET_GAS_EXCHANGE_RATE>
        :return:
        """
        self._debug('begin to create [DPOS_DISTRIBUTION-GET_GAS_EXCHANGE_RATE] to be signed payload')
        params = {
            ParamKey.gas_exchange_rate.name: gas_exchange_rate
        }
        payload = self._payload_builder.create_invoke_payload(SystemContractName.DPOS_DISTRIBUTION.name,
                                                              DposDistributionMethod.SET_GAS_EXCHANGE_RATE.name, params)
        return payload

    # 14-07 获取Gas转换率
    def get_gas_exchange_rage(self) -> int:
        """
        <14-07-DPOS_DISTRIBUTION-SET_GAS_EXCHANGE_RATE>
        :return:
        """
        self._debug('begin to get gas exchange rage')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_DISTRIBUTION.name,
                                                             DposDistributionMethod.GET_GAS_EXCHANGE_RATE.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data) if data else 0


class DPosDistributionWithEndorsers(BaseClient):
    # 14-00 奖励
    # def reward(self, timeout: int = None, with_sync_result: bool = None) -> TxResponse:  # todo
    #     """
    #     奖励
    #     <14-00-DPOS_DISTRIBUTION-REWARD>
    #     :param timeout: RPC请求超时时间
    #     :param with_sync_result: 是否同步轮询交易结果
    #     :return: 交易响应
    #     """
    #     raise NotImplementedError("待实现")
    #     payload = self.create_reward_payload()
    #     tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
    #     return tx_response

    # 14-02 设置每个区块奖励数量
    def set_distribution_per_block(self, distribution_per_block: int, timeout: int = None,
                                   with_sync_result: bool = None) -> TxResponse:
        """
        设置每个区块奖励数量
        <14-02-DPOS_DISTRIBUTION-SET_DISTRIBUTION_PER_BLOCK>
        :param distribution_per_block:
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        payload = self.create_set_distribution_per_block_payload(distribution_per_block)
        tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return tx_response

    # 14-04 设置从惩罚而来的奖励数量
    def set_distribution_from_slashing(self, slashing_per_block: int, timeout: int = None,
                                       with_sync_result: bool = None) -> TxResponse:
        """
        设置惩罚数量
        <14-04-DPOS_DISTRIBUTION-SET_DISTRIBUTION_FROM_SLASHING>
        :param slashing_per_block:
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        payload = self.create_set_distribution_for_slashing_payload(slashing_per_block)
        tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return tx_response

    # 14-06 设置Gas转换率
    def set_gas_exchange_rate(self, gas_exchange_rate: int, timeout: int = None,
                              with_sync_result: bool = None) -> TxResponse:
        """
        设置Gas转换率
        <14-06-DPOS_DISTRIBUTION-SET_GAS_EXCHANGE_RATE>
        :param gas_exchange_rate:
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        payload = self.create_set_gas_exchange_rage_payload(gas_exchange_rate)
        tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return tx_response
