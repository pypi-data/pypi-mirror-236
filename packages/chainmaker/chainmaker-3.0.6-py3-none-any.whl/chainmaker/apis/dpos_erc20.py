#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   dpos.py
# @Function     :   ChainMaker DPOS ERC20 / DPOS Stake 等操作接口

from chainmaker.apis.base_client import BaseClient
from chainmaker.keys import (SystemContractName, DposErc20Method, ParamKey)
from chainmaker.protos.common.request_pb2 import Payload

from chainmaker.protos.common.result_pb2 import TxResponse


class DPosErc20MixIn(BaseClient):
    """DPos ERC20操作"""

    # 07-00 查询归属人
    def owner(self) -> str:  # ✅
        """
        查询归属人
        <07-00-DPOS_ERC20-GET_OWNER>
        """
        self._debug('begin to get owner')
        payload = self._create_account_manager_payload(DposErc20Method.GET_OWNER.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return data.decode()

    # 07-01 查询ERC20合约的精度
    def decimals(self) -> int:  # ✅
        """
        查询ERC20合约的精度
        <07-01-DPOS_ERC20-GET_DECIMALS>
        :return: 合约精度
        """
        self._debug('begin to get decimals')
        payload = self._create_account_manager_payload(DposErc20Method.GET_DECIMALS.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data.decode()) if data else 0

    # 07-02 创建转账待签名Payload
    def create_transfer_payload(self, address: str, amount: int) -> Payload:
        """
        创建转账待签名Payload
        <07-02-DPOS_ERC20-TRANSFER>
        :param address: 接收Token的地址
        :param amount: 转账数量
        :return: 待签名Payload
        """
        self._debug('begin to create [DPOS_ERC20-TRANSFER] to be signed payload')
        params = {
            ParamKey.to.name: address,
            ParamKey.value.name: amount
        }
        return self._create_account_manager_payload(DposErc20Method.TRANSFER.name, params)

    # 07-03 创建从某个地址转账待签名Payload
    def create_transfer_from_payload(self, _from: str, to: str, amount: int) -> Payload:
        """
        创建从某个地址转账待签名Payload
        <07-03-DPOS_ERC20-TRANSFER_FROM>
        :param _from: 转出Token的地址
        :param to: 转入Token的地址
        :param amount: 转账数量
        :return: 待签名Payload
        """
        self._debug('begin to create [DPOS_ERC20-TRANSFER_FROM] to be signed payload')
        params = {
            ParamKey._from.name: _from,
            ParamKey.to.name: to,
            ParamKey.value.name: amount
        }

        return self._create_account_manager_payload(DposErc20Method.TRANSFER_FROM.name, params)

    # 07-04 查询账户余额
    def balance_of(self, address: str) -> int:  # ✅
        """
        查询账户余额
        <07-04-DPOS_ERC20-GET_BALANCEOF>
        :param address: 账户地址
        :return: 账户余额
        """
        self._debug('begin to get balance of [address:%s]' % address)
        params = {
            ParamKey.owner.name: address,
        }
        payload = self._create_account_manager_payload(DposErc20Method.GET_BALANCEOF.name, params)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data)

    # 07-05 创建转账证明待签名Payload
    def create_approve_payload(self, _from: str, to: str, amount: int) -> Payload:  # todo
        """
        创建转账证明待签名Payload
        <07-05-DPOS_ERC20-APPROVE>
        :param _from: 转出Token的地址
        :param to: 转入Token的地址
        :param amount: 转账数量
        :return: 待签名Payload
        """
        self._debug('begin to create [DPOS_ERC20-TRANSFER_FROM] to be signed payload')
        params = {
            ParamKey._from.name: _from,
            ParamKey.to.name: to,
            ParamKey.value.name: amount
        }

        return self._create_account_manager_payload(DposErc20Method.APPROVE.name, params)

    # 07-07 创建消耗Token待签名Payload
    def create_burn_payload(self, address: str, amount: int) -> Payload:  # todo
        """
        创建消耗Token待签名Payload
        <07-07-DPOS_ERC20-BURN>
        :param address: 接收Token的地址
        :param amount: 发行数量
        :return: 待签名Payload
        """
        self._debug('begin to create [DPOS_ERC20-BURN] to be signed payload')
        params = {
            ParamKey.to.name: address,
            ParamKey.value.name: amount
        }

        return self._create_account_manager_payload(DposErc20Method.BURN.name, params)

    # 07-08 创建发行Token待签名Payload
    def create_mint_payload(self, address: str, amount: int) -> Payload:
        """
        创建发行Token待签名Payload
        <07-08-DPOS_ERC20-MINT>
        :param address: 接收Token的地址
        :param amount: 发行数量
        :return: 待签名Payload
        """
        self._debug('begin to create [DPOS_ERC20-MINT] to be signed payload')
        params = {
            ParamKey.to.name: address,
            ParamKey.value.name: amount
        }
        return self._create_account_manager_payload(DposErc20Method.MINT.name, params)

    # 07-09 创建转移归属权待签名Payload
    def create_transfer_ownership_payload(self, address: str):
        """
        创建转移归属权待签名Payload
        <07-09-DPOS_ERC20-TRANSFER_OWNERSHIP>
        :param address: 接收资产地址
        :return: 待签名Payload
        """
        self._debug('begin to create [DPOS_ERC20-TRANSFER_OWNERSHIP] ownership payload')
        params = {
            ParamKey.to.name: address,
        }
        payload = self._create_account_manager_payload(DposErc20Method.TRANSFER_OWNERSHIP.name, params)

        return payload

    # 07-10 查询Token总供应量
    def total(self) -> int:  # ✅
        """
        查询Token总供应量
        <07-10-DPOS_ERC20-GET_TOTAL_SUPPLY>
        :return:
        """
        self._debug('begin to get total supply')
        payload = self._create_account_manager_payload(DposErc20Method.GET_TOTAL_SUPPLY.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data)

    def _create_account_manager_payload(self, method: str, params: dict = None) -> Payload:
        """
        创建账户管理员(Gas管理)待签名Payload
        :param method: DposErc20Method
        :param params: 参数
        :return: 待签名Payload
        """
        return self._payload_builder.create_query_payload(SystemContractName.DPOS_ERC20.name, method, params)


class DPosErc20WithEndorsers(BaseClient):

    # 07-02 转账
    def transfer(self, address: str, amount: int, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        转账
        :param address: 接收Token的地址
        :param amount: 转账数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 请求响应
        """
        payload = self.create_transfer_payload(address, amount)
        response = self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 07-03 从某个地址转账
    def transfer_from(self, _from: str, to: str, amount: int, timeout: int = None,
                      with_sync_result: bool = None) -> TxResponse:
        """
        从某个地址转账
        :param _from: 装出账户地址
        :param to: 转入账户地址
        :param amount: 转账数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 请求响应
        """

        payload = self.create_transfer_from_payload(_from, to, amount)
        response = self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response
        # 07-04 查询账户余额

    # 07-05 转账证明
    def approve(self, _from: str, to: str, amount: int,
                timeout: int = None, with_sync_result: bool = None):
        payload = self.create_approve_payload(_from, to, amount)
        response = self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 07-07 消耗Token
    def burn(self, address: str, amount: int,
             timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        Burn Token
        :param address: 接收Token的地址
        :param amount: 发行数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 请求响应
        """
        payload = self.create_burn_payload(address, amount)
        response = self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 07-08 发行Token
    def mint(self, address: str, amount: int,
             timeout: int = None, with_sync_result: bool = None) -> TxResponse:  # fixme 轮询不到结果
        """
        发行Token
        :param address: 接收Token的地址
        :param amount: 发行数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 请求响应
        """
        payload = self.create_mint_payload(address, amount)
        response = self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 07-09 转移管理员权限
    def transfer_ownership(self, address: str, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        转移管理员权限
        :param address: 接收资产地址
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 请求响应
        """
        payload = self.create_transfer_ownership_payload(address)
        response = self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

