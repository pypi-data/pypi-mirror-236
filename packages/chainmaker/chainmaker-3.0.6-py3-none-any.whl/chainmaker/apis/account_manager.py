#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   gas_manage.py
# @Function     :   ChainMaker Gas计费管理接口
from typing import Callable, Union, List, Dict

from chainmaker.apis.base_client import BaseClient
from chainmaker.keys import ChainConfigMethod, SystemContractName, AccountManagerMethod, ParamKey, RechargeGasItem
from chainmaker.protos.common.request_pb2 import Payload, TxType
from chainmaker.protos.common.result_pb2 import Result, TxResponse
from chainmaker.protos.syscontract.account_manager_pb2 import (
    RechargeGas,
    RechargeGasReq,
)


class AccountManagerMixIn(BaseClient):
    """账户管理员(Gas管理)操作"""

    # 13-00 创建设置Gas管理员待签名Payload
    def create_set_gas_admin_payload(self, address: str) -> Payload:
        """
        创建设置Gas管理员待签名Payload
        <13-00-ACCOUNT_MANAGER-SET_ADMIN>
        :param address: 管理员账户地址
        :return: 待签名Payload
        """
        self._debug("begin to create [ACCOUNT_MANAGER-SET_ADMIN] to be signed payload, [address:%s]" % address)
        params = {ParamKey.address_key.name: address}
        return self._create_account_manage_payload(AccountManagerMethod.SET_ADMIN.name, params)

    # 13-01 查询Gas管理员地址
    def get_gas_admin(self) -> str:
        """
        查询Gas管理员地址
        <13-01-ACCOUNT_MANAGER-GET_ADMIN>
        :return: Gas管理员账户地址
        """
        self._debug("begin to get gas admin")

        payload = self._create_account_query_request(AccountManagerMethod.GET_ADMIN.name)
        res = self.send_request(payload)
        return res.contract_result.result.decode()

    # 13-02 创建Gas充值待签名Payload
    def create_recharge_gas_payload(self, recharge_gas_list: List[RechargeGasItem]) -> Payload:
        """
        创建Gas充值待签名Payload
        <13-02-ACCOUNT_MANAGER-RECHARGE_GAS>
        :param recharge_gas_list: 充值列表
        :return: 待签名Payload
        """
        self._debug("begin to create [ACCOUNT_MANAGER-RECHARGE_GAS] to be signed payload, [recharge_gas_list:%s]"
                    % recharge_gas_list)

        batch_recharge_gas = [RechargeGas(address=item.address, gas_amount=item.amount) for item in recharge_gas_list]
        recharge_gas_req = RechargeGasReq(batch_recharge_gas=batch_recharge_gas).SerializeToString()

        params = {ParamKey.batch_recharge.name: recharge_gas_req}  # Fixme

        return self._create_account_manage_payload(AccountManagerMethod.RECHARGE_GAS.name, params)

    # 13-03 获取Gas账户余额
    def get_gas_balance(self, address: str = None) -> int:
        """
        获取Gas账户余额
        <13-03-ACCOUNT_MANAGER-GET_BALANCE>
        :param str address: 账户地址
        :return: 账户余额
        """
        self._debug("begin to get gas gas balance [address:%s]" % address)
        if address is None:
            address = self.sender_address
        params = {ParamKey.address_key.name: address}
        payload = self._create_account_query_request(AccountManagerMethod.GET_BALANCE.name, params)
        res = self.send_request(payload)
        balance = int(res.contract_result.result.decode())
        return balance

    # 13-04 创建Gas收费待签名Payload
    def create_charge_gas_payload(self, recharge_gas_list: List[RechargeGasItem]) -> Payload:  # todo
        """
        创建Gas收费待签名Payload
        <13-04-ACCOUNT_MANAGER-CHARGE_GAS>
        :param recharge_gas_list: 充值列表
        :return: 待签名Payload
        """
        self._debug("begin to create [ACCOUNT_MANAGER-CHARGE_GAS] to be signed payload [recharge_gas_list:%s]"
                    % recharge_gas_list)

        batch_recharge_gas = [RechargeGas(address=item.address, gas_amount=item.amount) for item in recharge_gas_list]
        recharge_gas_req = RechargeGasReq(batch_recharge_gas=batch_recharge_gas).SerializeToString()

        params = {ParamKey.batch_recharge.name: recharge_gas_req}  # Fixme

        return self._create_account_manage_payload(AccountManagerMethod.CHARGE_GAS.name, params)

    # 13-05 创建冻结账户待签名Payload
    def create_frozen_gas_account_payload(self, address: str) -> Payload:
        """
        创建冻结账户待签名Payload
        <13-05-ACCOUNT_MANAGER-FROZEN_ACCOUNT>
        :param address: 账户地址
        :return: 待签名Payload
        """
        self._debug("begin to create [ACCOUNT_MANAGER-FROZEN_ACCOUNT] to be signed payload [address:%s]" % address)

        params = {ParamKey.address_key.name: address}
        return self._create_account_manage_payload(AccountManagerMethod.FROZEN_ACCOUNT.name, params)

    # 13-06 创建解冻账户待签名Payload
    def create_unfrozen_gas_account_payload(self, address: str) -> Payload:
        """
        创建解冻账户待签名Payload
        <13-06-ACCOUNT_MANAGER-UNFROZEN_ACCOUNT>
        :param address: 账户地址
        :return: 待签名Payload
        """
        self._debug("begin to create [ACCOUNT_MANAGER-UNFROZEN_ACCOUNT] to be signed payload [address:%s]" % address)

        params = {ParamKey.address_key.name: address}
        return self._create_account_manage_payload(AccountManagerMethod.UNFROZEN_ACCOUNT.name, params)

    # 13-07 查询Gas账户状态
    def get_gas_account_status(self, address: str = None) -> bool:
        """
        查询Gas账户状态
        <13-07-ACCOUNT_MANAGER-ACCOUNT_STATUS>
        :param str address: 账户地址
        :return: 正常是返回True, 冻结返回False
        """
        self._debug("begin to get gas account status [address:%s]" % address)
        if address is None:
            address = self.sender_address
        params = {ParamKey.address_key.name: address}
        payload = self._create_account_query_request(AccountManagerMethod.ACCOUNT_STATUS.name, params)
        res = self.send_request(payload)
        return b'0' == res.contract_result.result

    # 13-08 创建Gas退款待签名Payload
    def create_refund_gas_payload(self, address: str, amount: int) -> Payload:
        """
        创建Gas退款待签名Payload
        <13-08-ACCOUNT_MANAGER-REFUND_GAS>
        :param address: 账户地址
        :param amount: 退款额度
        :return: 待签名Payload
        """
        self._debug(
            "begin to create [ACCOUNT_MANAGER-REFUND_GAS] to be signed payload [address:%s]/[amount:%s]" % (address,
                                                                                                            amount))
        # if amount <= 0:
        #     raise ValueError('amount must > 0')

        params = {ParamKey.address_key.name: address,
                  ParamKey.charge_gas_amount.name: amount}

        return self._create_account_manage_payload(AccountManagerMethod.REFUND_GAS.name, params)

    # 13-09 创建Gas VM退款待签名Payload
    def create_refund_gas_vm_payload(self, address: str, amount: int) -> Payload:  # todo
        """
        创建Gas退款待签名Payload
        <13-09-ACCOUNT_MANAGER-REFUND_GAS_VM>
        :param address: 账户地址
        :param amount: 退款额度
        :return: 待签名Payload
        """
        self._debug(
            "begin to create [ACCOUNT_MANAGER-REFUND_GAS_VM] to be signed payload [address:%s]/[amount:%s]" % (address,
                                                                                                               amount))
        # if amount <= 0:
        #     raise ValueError('amount must > 0')

        params = {ParamKey.address_key.name: address,
                  ParamKey.charge_gas_amount.name: amount}

        return self._create_account_manage_payload(AccountManagerMethod.REFUND_GAS.name, params)

    # 13-10 创建Gas退款待签名Payload
    def create_charge_gas_for_multi_account_payload(self, address: str, amount: int) -> Payload:  # todo
        """
        创建Gas多账户收费待签名Payload
        <13-10-ACCOUNT_MANAGER-CHARGE_GAS_FOR_MULTI_ACCOUNT>
        :param address: 账户地址
        :param amount: 退款额度
        :return: 待签名Payload
        """
        self._debug("begin to create [ACCOUNT_MANAGER-CHARGE_GAS_FOR_MULTI_ACCOUNT] to be signed payload,"
                    " [address:%s]/[amount:%s]" % (address, amount))
        # if amount <= 0:
        #     raise ValueError('amount must > 0')

        params = {ParamKey.address_key.name: address,
                  ParamKey.charge_gas_amount.name: amount}

        return self._create_account_manage_payload(AccountManagerMethod.CHARGE_GAS_FOR_MULTI_ACCOUNT.name, params)

    @staticmethod
    def attach_gas_limit(payload: Payload, gas_limit: int) -> Payload:
        """
        设置Gas转账限制
        :param payload: Payload
        :param gas_limit: Gas交易限制
        :return: Payload
        """
        payload.limit.gas_limit = gas_limit
        return payload

    def estimate_gas(self, payload: Payload) -> int:
        """
        估计请求Gas消耗
        :param payload: 待发送请求payload
        :return: Gas数量
        """
        self._debug("begin estimate gas")
        payload.TxType = TxType.QUERY_CONTRACT.name

        response = self.send_request(payload)
        return response.ContractResult.GasUsed

    def create_set_invoke_base_gas_payload(
            self, amount: int
    ) -> Payload:
        """
        创建设置invoke合约Gas价格待签名Payload
        v2.3.2 新增
        :param amount: 设置待基础Gas消耗数量
        :return: 待签名Payload
        """
        self._debug("begin CreateSetInvokeBaseGasPayload")
        assert (
                isinstance(amount, int) and amount >= 0
        ), "[Sdk] amount should be int and >= 0"
        params = {ParamKey.set_invoke_base_gas.name: amount}
        return self._create_chain_config_manage_payload(
            ChainConfigMethod.SET_INVOKE_BASE_GAS.name, params
        )

    def create_set_invoke_gas_price_payload(
            self, amount: int
    ) -> Payload:
        """
        创建设置invoke合约Gas价格待签名Payload
        v2.3.2 新增
        :param amount: 设置待基础Gas消耗数量
        :return: 待签名Payload
        """
        self._debug("begin CreateSetInvokeGasPricePayload")
        assert (
                isinstance(amount, int) and amount >= 0
        ), "[Sdk] amount should be int and >= 0"
        params = {ParamKey.set_invoke_gas_price.name: amount}
        return self._create_chain_config_manage_payload(
            ChainConfigMethod.SET_INVOKE_GAS_PRICE.name, params
        )

    def create_set_install_base_gas_payload(
            self, amount: int
    ) -> Payload:
        """
        创建设置install合约基础Gas消耗待签名Payload
        v2.3.2 新增
        :param amount: 设置待基础Gas消耗数量
        :return: 待签名Payload
        """
        self._debug("begin CreateSetInstallGasPricePayload")
        assert (
                isinstance(amount, int) and amount >= 0
        ), "[Sdk] amount should be int and >= 0"
        params = {ParamKey.set_install_base_gas.name: amount}
        return self._create_chain_config_manage_payload(
            ChainConfigMethod.SET_INSTALL_BASE_GAS.name, params
        )

    def create_set_install_gas_price_payload(
            self, amount: int
    ) -> Payload:
        """
        创建设置install合约Gas价格待签名Payload
        v2.3.2 新增
        :param amount: 设置待基础Gas消耗数量
        :return: 待签名Payload
        """
        self._debug("begin CreateSetInstallGasPricePayload")
        assert (
                isinstance(amount, int) and amount >= 0
        ), "[Sdk] amount should be int and >= 0"
        params = {ParamKey.set_install_gas_price: amount}
        return self._create_chain_config_manage_payload(
            ChainConfigMethod.SET_INSTALL_GAS_PRICE, params
        )

    def _create_account_manage_payload(self, method: str, params: Dict[str, Union[str, int, bool]] = None) -> Payload:
        """

        :param method:
        :param params:
        :return:
        """
        return self._payload_builder.create_invoke_payload(SystemContractName.ACCOUNT_MANAGER.name, method, params)

    def _create_account_query_request(self, method: str, params: Dict[str, Union[str, int, bool]] = None) -> Payload:
        """

        :param method:
        :param params:
        :return:
        """
        return self._payload_builder.create_query_payload(SystemContractName.ACCOUNT_MANAGER.name, method, params)

    def send_gas_manage_request(self, payload: Payload, endorsers: list, timeout: int = None,
                                with_sync_result: bool = True) -> Union[TxResponse, Result]:
        """
        发送Gas管理请求
        :param payload: Payload
        :param endorsers: 背书列表
        :param timeout: 超时时间
        :param with_sync_result: 是否同步轮询结果
        :return: 响应信息
        """
        return self.send_request_with_sync_result(payload, endorsers, timeout, with_sync_result)


class AccountManagerWithEndorsers(BaseClient):
    get_gas_admin: Callable
    create_set_gas_admin_payload: Callable
    send_manage_request: Callable

    def check_gas_admin(self) -> bool:
        """
        检查当前客户端用户是否Gas管理员
        :return: 当前客户端用户是Gas管理员返回True, 否则返回False
        """
        return self.user.address == self.get_gas_admin()

    # 13-00
    def set_gas_admin(self, address: str = None, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        设置Gas管理员地址
        :param address: 用户地址-为None时为当前用户地址
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        if address is None:
            address = self.sender_address
        payload = self.create_set_gas_admin_payload(address)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

        # 13-01 查询Gas管理员地址

    # 13-02 Gas充值
    def recharge_gas(self, recharge_gas_list: List[RechargeGasItem],
                     timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        Gas充值
        :param recharge_gas_list: 充值列表 [(address, amount)] 格式
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        payload = self.create_recharge_gas_payload(recharge_gas_list)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-04 Gas收费
    def charge_gas(self, recharge_gas_list: List[RechargeGasItem],
                   timeout: int = None, with_sync_result: bool = None):  # todo 待验证
        """
        Gas收费
        :param recharge_gas_list:
        :param timeout:
        :param with_sync_result:
        :return:
        """
        payload = self.create_charge_gas_payload(recharge_gas_list)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-05 冻结Gas账户
    def freeze_gas_account(self, address: str, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        冻结Gas账户
        :param address: 待冻结账户地址
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        payload = self.create_frozen_gas_account_payload(address)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-06 解冻Gas账户
    def unfreeze_gas_account(self, address: str, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        解冻Gas账户
        :param address: 待冻结账户地址
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        payload = self.create_unfrozen_gas_account_payload(address)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-07 查询Gas账户状态
    def get_gas_account_status(self, address: str = None) -> bool:
        """
        查询Gas账户状态
        <13-07-ACCOUNT_MANAGER-ACCOUNT_STATUS>
        :param str address: 账户地址
        :return: 正常是返回True, 冻结返回False
        """
        return super().get_gas_account_status(address)

    # 13-08 Gas退款
    def refund_gas(self, address: str, amount: int, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        Gas退款
        :param address: 退款账户地址
        :param amount: 退款金额
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        payload = self.create_refund_gas_payload(address, amount)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 12-09 Gas VM 退款
    def refund_gas_vm(self, address: str, amount: int, timeout: int = None,
                      with_sync_result: bool = None) -> TxResponse:  # todo 待验证
        """

        :param address:
        :param amount:
        :param timeout:
        :param with_sync_result:
        :return:
        """
        payload = self.create_refund_gas_vm_payload(address, amount)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-10 Gas多账户收费
    def charge_gas_for_multi_account(self, charge_gas_list: List[tuple],
                                     timeout: int = None, with_sync_result: bool = None):  # todo 待验证
        """

        :param charge_gas_list:
        :param timeout:
        :param with_sync_result:
        :return:
        """
        payload = self.create_charge_gas_for_multi_account_payload(charge_gas_list)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
