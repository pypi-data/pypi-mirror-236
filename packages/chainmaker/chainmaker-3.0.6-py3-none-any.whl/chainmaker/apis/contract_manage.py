#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   user_contract.py
# @Function     :   ChainMaker用户合约接口
import json
import warnings
from typing import List, Union

from chainmaker.apis.base_client import BaseClient
from chainmaker.exceptions import RequestError
from chainmaker.keys import (ParamKey, RuntimeType, SystemContractName, ContractManageMethod, ContractQueryMethod)
from chainmaker.protos.common.contract_pb2 import Contract
from chainmaker.protos.common.request_pb2 import EndorsementEntry, Payload, TxRequest
from chainmaker.protos.common.result_pb2 import TxResponse, TxStatusCode
from chainmaker.sdk_config import DefaultConfig
from chainmaker.user import User
from chainmaker.utils import common, file_utils
from chainmaker.utils.evm_utils import calc_evm_params, calc_evm_method_params


class ContractQueryMixIn(BaseClient):
    # 05-00 获取合约信息
    def get_contract_info(self, contract_name: str) -> Union[Contract, None]:
        """
        获取合约信息
        <05-00-CONTRACT_MANAGE-GET_CONTRACT_INFO> # todo
        :param contract_name: 用户合约名称
        :return: 合约存在则返回合约信息Contract对象，合约不存在抛出ContractFail
        :raise: RequestError: 请求出错
        :raise: AssertionError: 响应code不为0,检查响应时抛出断言失败
        :raise: 当数据不是JSON格式时，抛出json.decoder.JSONDecodeError
        """
        self._debug("begin to get contract info [contract_name:%s]" % contract_name)

        params = {ParamKey.CONTRACT_NAME.name: contract_name}
        payload = self._create_contract_query_payload(ContractQueryMethod.GET_CONTRACT_INFO.name, params)
        try:
            response = self.send_request(payload)
        except RequestError:
            return None

        # result_utils.check_response(tx_response)
        data = response.contract_result.result
        contract_data = json.loads(data)
        return self._parse_contract(contract_data)

    # 05-01 获取合约ByteCode
    def get_contract_byte_code(self, contract_name: str) -> bytes:  # todo
        """
        获取合约ByteCode
        <05-01-CONTRACT_MANAGE-GET_CONTRACT_BYTECODE> # todo
        :param contract_name: 用户合约名称
        :return: 合约存在则返回合约信息Contract对象，合约不存在抛出ContractFail
        :raise: RequestError: 请求出错
        :raise: AssertionError: 响应code不为0,检查响应时抛出断言失败
        :raise: 当数据不是JSON格式时，抛出json.decoder.JSONDecodeError
        """
        raise NotImplementedError('the method does not found')
        # self._debug("begin to GetContractByteCode, [contract_name:%s]" % contract_name)
        # params = {ParamKey.CONTRACT_NAME.name: contract_name}
        # payload = self._create_contract_query_payload(ContractQueryMethod.GET_CONTRACT_BYTECODE.name, params)
        # response = self.send_request(payload)
        # return response

    # 05-02 获取合约列表
    def get_contract_list(self) -> List[Contract]:
        """
        获取合约列表(包括系统合约和用户合约)
        <05-02-CONTRACT_MANAGE-GET_CONTRACT_LIST> # todo
        :return: 合约Contract对象列表
        :raise: RequestError: 请求出错
        :raise: AssertionError: 响应code不为0,检查响应时抛出断言失败
        :raise: 当数据不是JSON格式时，抛出json.decoder.JSONDecodeError
        """
        self._debug("begin to get contract list")
        payload = self._create_contract_query_payload(ContractQueryMethod.GET_CONTRACT_LIST.name)

        response = self.send_request(payload)
        contract_list = json.loads(response.contract_result.result)
        contracts = [self._parse_contract(contract_data) for contract_data in contract_list]
        return contracts

    # def get_user_contract_list(self) -> List[Contract]:  # todo remove
    #     """
    #     获取用户合约列表
    #     :return: 合约列表
    #     """
    #     return [contract for contract in self.get_contract_list() if contract.runtime_type != 1]  # 1-NATIVE

    # 05-03 获取禁用系统合约名称列表
    def get_disabled_native_contract_list(self) -> List[str]:
        """
        获取禁用系统合约名称列表
        <05-03-CONTRACT_MANAGE-GET_DISABLED_CONTRACT_LIST> # todo
        :return: 禁用合约名称列表
        """
        self._debug("begin to get disabled native contact list")
        payload = self._create_contract_query_payload(ContractQueryMethod.GET_DISABLED_CONTRACT_LIST.name)

        response = self.send_request(payload)
        return json.loads(response.contract_result.result) or []

    def _create_contract_query_payload(self, method: str, params: Union[dict, list] = None):
        """
        创建合约查询待签名Payload
        :param method: 合约查询方法
        :param params: 方法参数
        :return: 待签名Payload
        """
        return self._payload_builder.create_query_payload(SystemContractName.CONTRACT_MANAGE.name, method, params)

    @staticmethod
    def _parse_contract(contract_data: dict) -> Contract:
        """
        将二进制格式合约数据解析成合约结构体
        :param dict contract_data: 合约数据
        :return: 合约Contract对象
        :raise: 当数据不是JSON格式时，抛出json.decoder.JSONDecodeError
        """
        if contract_data.get('creator', {}).get('member_info'):
            contract_data['creator']['member_info'] = contract_data['creator']['member_info'].encode()
        contract = Contract(**contract_data)
        return contract


class UserContractMixIn(BaseClient):
    """用户合约操作"""

    # 05-00 创建创建用户合约待签名Payload
    def create_contract_create_payload(self, contract_name: str, version: str, byte_code_path: str,
                                       runtime_type: Union[RuntimeType, str],
                                       params: Union[dict, list] = None,
                                       gas_limit: int = None, tx_id: str = None) -> Payload:
        """
        创建创建用户合约待签名Payload
        <05-00-CONTRACT_MANAGE-INIT_CONTRACT>
        :param contract_name: 合约名
        :param version: 合约版本
        :param byte_code_path: 合约字节码：可以是字节码；合约文件路径；或者 hex编码字符串；或者 base64编码字符串。
        :param runtime_type: 合约类型
            eg. 'INVALID', 'NATIVE', 'WASMER', 'WXVM', 'GASM', 'EVM', 'DOCKER_GO', 'DOCKER_JAVA'
        :param params: 合约参数，dict类型，key 和 value 尽量为字符串
        :param gas_limit: Gas交易限制
        :param tx_id: 指定交易Id
        :return: 待签名Payload
        :raises ValueError: 如果 byte_code 不能转成合约字节码
        """

        self._debug("begin to create [CONTRACT_MANAGE-INIT_CONTRACT] to be signed payload "
                    "[contract_name:%s] " % contract_name)
        runtime_type = common.ensure_str(runtime_type) if runtime_type else ''
        byte_code = file_utils.load_byte_code(byte_code_path) if byte_code_path else b''
        return self._create_contract_manage_payload(ContractManageMethod.INIT_CONTRACT.name,
                                                    contract_name, version, byte_code,
                                                    runtime_type, params, gas_limit, tx_id=tx_id)

    # 05-01 创建升级用户合约待签名Payload
    def create_contract_upgrade_payload(self, contract_name: str, version: str, byte_code_path: str,
                                        runtime_type: Union[RuntimeType, str],
                                        params: Union[dict, list] = None, gas_limit: int = None,
                                        tx_id: str = None) -> Payload:
        """
        创建升级用户合约待签名Payload
        <05-01-CONTRACT_MANAGE-UPGRADE_CONTRACT>
        :param contract_name: 合约名
        :param version: 合约版本
        :param byte_code_path: 合约字节码：可以是字节码；合约文件路径；或者 hex编码字符串；或者 base64编码字符串。
        :param runtime_type: 合约类型
            eg. 'INVALID', 'NATIVE', 'WASMER', 'WXVM', 'GASM', 'EVM', 'DOCKER_GO', 'DOCKER_JAVA'
        :param params: 合约参数，dict类型，key 和 value 尽量为字符串
        :param gas_limit: Gas交易限制
        :param tx_id: 指定交易Id
        :return: 待签名Payload
        :raises ValueError: 如果 byte_code 不能转成合约字节码
        """
        self._debug("begin to create [CONTRACT_MANAGE-UPGRADE_CONTRACT] to be signed payload "
                    "[contract_name:%s]" % contract_name)
        runtime_type = common.ensure_str(runtime_type) if runtime_type else ''
        byte_code = file_utils.load_byte_code(byte_code_path) if byte_code_path else b''
        return self._create_contract_manage_payload(ContractManageMethod.UPGRADE_CONTRACT.name,
                                                    contract_name, version, byte_code,
                                                    runtime_type, params, gas_limit, tx_id=tx_id)

    # 05-02 创建冻结合约待签名Payload
    def create_contract_freeze_payload(self, contract_name: str, tx_id: str = None) -> Payload:
        """
        创建冻结合约待签名Payload
        <05-02-CONTRACT_MANAGE-FREEZE_CONTRACT>
        :param contract_name: 合约名
        :param tx_id: 指定交易Id
        :return: 待签名Payload
        """
        self._debug("begin to create [CONTRACT_MANAGE-FREEZE_CONTRACT] to be signed payload "
                    "[contract_name:%s]" % contract_name)

        return self._create_contract_manage_payload(ContractManageMethod.FREEZE_CONTRACT.name, contract_name,
                                                    tx_id=tx_id)

    # 05-03 创建解冻合约待签名Payload
    def create_contract_unfreeze_payload(self, contract_name: str, tx_id: str = None) -> Payload:
        """
        创建解冻合约待签名Payload
        <05-03-CONTRACT_MANAGE-UNFREEZE_CONTRACT>
        :param contract_name: 合约名
        :param tx_id: 指定交易Id
        :return: 待签名Payload
        """
        self._debug("begin to create [CONTRACT_MANAGE-UNFREEZE_CONTRACT] to be signed payload "
                    "[contract_name:%s] " % contract_name)

        return self._create_contract_manage_payload(ContractManageMethod.UNFREEZE_CONTRACT.name, contract_name,
                                                    tx_id=tx_id)

    # 05-04 创建吊销合约待签名Payload
    def create_contract_revoke_payload(self, contract_name: str, tx_id: str = None) -> Payload:
        """
        创建吊销合约待签名Payload
        <05-04-CONTRACT_MANAGE-REVOKE_CONTRACT>
        :param contract_name: 合约名
        :param tx_id: 指定交易Id
        :return: 待签名Payload
        """
        self._debug("begin to create [CONTRACT_MANAGE-REVOKE_CONTRACT] to be signed payload"
                    " [contract_name:%s] " % contract_name)

        return self._create_contract_manage_payload(ContractManageMethod.REVOKE_CONTRACT.name, contract_name,
                                                    tx_id=tx_id)

    def invoke_contract(self, contract_name: str, method: str, params: Union[dict, list] = None,
                        tx_id: str = None, gas_limit: int = None, timeout: int = None,
                        with_sync_result: bool = None, signer: User = None, payer: User = None) -> TxResponse:
        """
        调用合约
        :param contract_name: 合约名
        :param method: 调用合约方法名
        :param params: 调用参数，参数类型为dict
        :param tx_id: 交易id，如果交易id为空/空字符串，则创建新的tx_id
        :param gas_limit: 交易Gas限制
        :param signer: 指定签名用户
        :param payer: 指定Gas代扣用户
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步交易执行结果。如果不同步，返回tx_id，供异步查询; 同步则循环等待，返回交易的执行结果。
        :return: TxResponse
        :raises RequestError: 请求失败
        """
        if isinstance(params, list):
            method, params = calc_evm_method_params(method, params)

        self._debug("begin to invoke contract, [contract_name:%s]/[method:%s]/[tx_id:%s]/[params:%s]" % (
            contract_name, method, tx_id, params))
        if gas_limit is None:
            gas_limit = self._default_gas_limit

        payload = self._payload_builder.create_invoke_payload(contract_name, method, params, tx_id=tx_id,
                                                              gas_limit=gas_limit)

        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result,
                                                  signer=signer, payer=payer)

    def invoke_contract_with_limit(self, contract_name: str, method: str, params: Union[dict, list] = None,
                                   tx_id: str = None, gas_limit: int = None,
                                   timeout: int = None, with_sync_result: bool = None,
                                   signer: User = None, payer: User = None) -> TxResponse:  # todo remove
        """
        带Gas限制调用合约
        :param contract_name: 合约名
        :param method: 调用合约方法名
        :param params: 调用参数，参数类型为dict
        :param tx_id: 交易id，如果交易id为空/空字符串，则创建新的tx_id
        :param timeout: 超时时间，默认为 3s
        :param with_sync_result: 是否同步交易执行结果。如果不同步，返回tx_id，供异步查询; 同步则循环等待，返回交易的执行结果。
        :param gas_limit: Gas交易限制
        :param signer: 指定签名用户
        :param payer: 指定Gas代扣用户
        :return: TxResponse
        :raises RequestError: 请求失败
        """
        warnings.warn('user invoke_contract instead', DeprecationWarning)
        if isinstance(params, list):
            method, params = calc_evm_method_params(method, params)
        self._debug("begin to invoke contract, [contract_name:%s]/[method:%s]/[tx_id:%s]/[params:%s]" % (
            contract_name, method, tx_id, params))

        payload = self._payload_builder.create_invoke_payload(contract_name, method, params, tx_id)
        if gas_limit is not None:
            payload.gas_limit = gas_limit
        elif self.get_chain_config().account_config.enable_gas:
            payload.gas_limit = self.estimate_gas(payload)  # TODO
        # self.attach_gas_limit(payload, gas_limit)
        # payload = self.attach_gas_limit(payload, gas_limit)

        response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result,
                                                      signer=signer, payer=payer)
        return response

    def query_contract(self, contract_name: str, method: str, params: Union[dict, list] = None,
                       timeout: int = None, signer: User = None) -> TxResponse:
        """
        查询用户合约
        :param contract_name: 合约名
        :param method: 调用合约方法名
        :param params: 调用参数，参数类型为dict
        :param timeout: 超时时间，默认为 3s
        :param signer: 指定签名用户
        :return: TxResponse, 结果不存在时返回None
        :raises RequestError: 请求失败
        """
        if isinstance(params, list):
            method, params = calc_evm_method_params(method, params)
        self._debug("begin to query contract, [contract_name:%s]/[method:%s]/[params:%s]" % (
            contract_name, method, params))
        payload = self._payload_builder.create_query_payload(contract_name, method, params)
        response = self.send_request(payload, timeout=timeout, signer=signer)

        return response

    def sign_contract_manage_payload(self, payload: Payload) -> bytes:
        """对 合约管理的 payload 字节数组进行签名，返回签名后待签名Payload字节数组
        :param payload: 交易 payload
        :return: 待签名Payload 的字节数组
        :raises DecodeError: 如果 byte_code 解码失败
        """
        warnings.warn('no use for this method', DeprecationWarning)
        return self.user.sign(payload)

    def send_contract_manage_request(self, payload: Payload, endorsers: List[EndorsementEntry], timeout: int = None,
                                     with_sync_result: bool = None) -> TxResponse:
        """发送合约管理的请求
        :param endorsers: 背书列表
        :param payload: 请求的 payload
        :param timeout: 超时时间
        :param with_sync_result: 是否同步交易执行结果。如果不同步，返回tx_id，供异步查询; 同步则循环等待，返回交易的执行结果。
        :return: TxResponse
        :raises RequestError: 请求失败
        """
        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result,
                                                  endorsers=endorsers)

    def get_tx_request(self, contract_name: str, method: str, params: Union[dict, list] = None,
                       tx_id: str = None) -> TxRequest:
        """
        获取交易请求体
        :param contract_name: 合约名
        :param method: 调用合约方法名
        :param params: 调用参数，参数类型为dict
        :param tx_id: 交易id，如果交易id为空/空字符串，则创建新的tx_id
        :return: Request
        """
        self._debug("begin to create TxRequest, [contract_name:%s]/[method:%s]/[tx_id:%s]/[params:%s]" % (
            contract_name, method, tx_id, params))
        if not tx_id:
            tx_id = common.gen_rand_tx_id()

        payload = self._payload_builder.create_invoke_payload(contract_name, method, params, tx_id)

        return self._generate_tx_request(payload)

    def send_tx_request(self, tx_request, timeout=None, with_sync_result=None) -> TxResponse:
        """发送请求
        :param tx_request: 请求体
        :param timeout: 超时时间
        :param with_sync_result: 是否同步交易执行结果。如果不同步，返回tx_id，供异步查询; 同步则循环等待，返回交易的执行结果。
        :return: Response
        :raises RequestError: 请求失败
        """
        response = self._get_client().SendRequest(tx_request, timeout=timeout)

        # 判断结果是否正确
        if response.code == TxStatusCode.SUCCESS:
            if with_sync_result:
                response = self.get_sync_result(tx_request.payload.tx_id)
            return response
        else:
            raise RequestError(err_code=response.code, err_msg=TxStatusCode.Name(response.code) + response.message)

    def _create_contract_manage_payload(self, method: str, contract_name: str = None, version: str = None,
                                        byte_code: bytes = None, runtime_type: str = None,
                                        params: Union[dict, list] = None,
                                        gas_limit: int = None, tx_id: str = None):
        params = params or {}
        if runtime_type == RuntimeType.EVM.name:  # EMV byte_code需要转为hex
            byte_code = bytes.fromhex(byte_code.decode())
            if isinstance(params, list):
                params = calc_evm_params(params)

        _params = {
            ParamKey.CONTRACT_NAME.name: contract_name,
            ParamKey.CONTRACT_VERSION.name: version,
            ParamKey.CONTRACT_RUNTIME_TYPE.name: runtime_type,
            ParamKey.CONTRACT_BYTECODE.name: byte_code
        }
        if isinstance(params, dict):
            _params.update(params)

        return self._payload_builder.create_invoke_payload(SystemContractName.CONTRACT_MANAGE.name, method, _params,
                                                           gas_limit=gas_limit, tx_id=tx_id)


class SystemContractMixIn(BaseClient):
    """系统合约操作"""

    def invoke_system_contract(self, contract_name: str, method: str, params: Union[dict, list] = None,
                               tx_id: str = None, gas_limit: int = None,
                               timeout: int = None, with_sync_result: bool = False) -> TxResponse:
        """
        调用系统合约
        :param contract_name: 系统合约名称
        :param method: 系统合约方法
        :param params: 系统合约方法所需的参数
        :param tx_id: 指定交易Id，默认为空是生成随机交易Id
        :param gas_limit: Gas交易限制
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应信息
        """
        self._debug("begin to invoke system contract [contract_name:%s]/[method:%s]/[params:%s]" % (
            contract_name, method, params))
        if timeout is None:
            timeout = DefaultConfig.rpc_send_tx_timeout
        payload = self._payload_builder.create_invoke_payload(contract_name, method, params, tx_id)
        if gas_limit is not None:
            self.attach_gas_limit(payload, gas_limit)
        response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    def query_system_contract(self, contract_name: str, method: str, params: Union[dict, list] = None,
                              tx_id: str = None, timeout: int = None) -> TxResponse:
        """
        查询系统合约
        :param contract_name: 系统合约名称
        :param method: 系统合约方法
        :param params: 系统合约方法所需的参数
        :param tx_id: 指定交易Id，默认为空是生成随机交易Id
        :param timeout: RPC请求超时时间
        :return: 交易响应信息
        """
        self._debug("begin to query system contract [contract_name:%s]/[method:%s]/[params:%s]" % (
            contract_name, method, params))
        if timeout is None:
            timeout = DefaultConfig.rpc_send_tx_timeout
        payload = self._payload_builder.create_query_payload(contract_name, method, params, tx_id=tx_id)
        response = self.send_request(payload, timeout=timeout)
        return response

    # 05-05 生成系统合约授权访问待签名Payload
    def create_native_contract_access_grant_payload(self, grant_contract_list: List[str]) -> Payload:
        """
        生成系统合约授权访问待签名Payload
        <05-05-CONTRACT_MANAGE-GRANT_CONTRACT_ACCESS>
        :param List[str] grant_contract_list: 授予权限的访问系统合约名称列表 # TODO 确认 合约状态必须是FROZEN
        :return: 待签名Payload
        """
        self._debug("begin to create [CONTRACT_MANAGE-GRANT_CONTRACT_ACCESS] to be signed payload")

        return self._create_native_contract_access_payload(ContractManageMethod.GRANT_CONTRACT_ACCESS.name,
                                                           grant_contract_list)

    # 05-06 生成原生合约吊销授权访问待签名Payload
    def create_native_contract_access_revoke_payload(self, revoke_contract_list: List[str]) -> Payload:
        """
        生成原生合约吊销授权访问待签名Payload
        <05-06-CONTRACT_MANAGE-REVOKE_CONTRACT_ACCESS>
        :param revoke_contract_list: 吊销授予权限的访问合约列表
        :return: 待签名Payload
        """
        self._debug("begin to create [CONTRACT_MANAGE-REVOKE_CONTRACT_ACCESS] to be signed payload")
        return self._create_native_contract_access_payload(ContractManageMethod.REVOKE_CONTRACT_ACCESS.name,
                                                           revoke_contract_list)

    # 05-07 生成原生合约验证授权访问待签名Payload
    def create_native_contract_access_verify_payload(self, contract_list: List[str]) -> Payload:
        """
        生成原生合约验证授权访问待签名Payload
        <05-07-CONTRACT_MANAGE-VERIFY_CONTRACT_ACCESS>
        :param contract_list: 验证授予权限的访问合约列表
        :return: 待签名Payload
        """
        self._debug("begin to create [CONTRACT_MANAGE-VERIFY_CONTRACT_ACCESS] to be signed payload")
        return self._create_native_contract_access_payload(ContractManageMethod.VERIFY_CONTRACT_ACCESS.name,
                                                           contract_list)

    # 05-08 创建创建新系统合约待签名Payload
    def create_init_new_native_contract_payload(self, contract_name: str, version: str,
                                                byte_code_path: str,
                                                runtime_type: Union[RuntimeType, str],
                                                params: Union[dict, list] = None,
                                                gas_limit: int = None, tx_id: str = None) -> Payload:  # todo
        """
        创建创建新系统合约待签名Payload
        <05-08-CONTRACT_MANAGE-INIT_NEW_NATIVE_CONTRACT>
        :param contract_name: 合约名
        :param version: 合约版本
        :param byte_code_path: 合约字节码：可以是字节码；合约文件路径；或者 hex编码字符串；或者 base64编码字符串。
        :param runtime_type: contract_pb2.RuntimeType.WASMER
        :param params: 合约参数，dict类型，key 和 value 尽量为字符串
        :param gas_limit: Gas交易限制
        :param tx_id: 指定交易Id
        :return: 待签名Payload
        :raises ValueError: 如果 byte_code 不能转成合约字节码
        """

        if gas_limit is None:
            gas_limit = self._default_gas_limit
        runtime_type = common.ensure_str(runtime_type)

        byte_code = file_utils.load_byte_code(byte_code_path)
        if not byte_code:
            raise ValueError("[Sdk] can't get contract bytes code from byte_code param")
        return self._create_contract_manage_payload(ContractManageMethod.INIT_NEW_NATIVE_CONTRACT.name,
                                                    contract_name, version, byte_code,
                                                    runtime_type, params, gas_limit, tx_id=tx_id)

    def _create_native_contract_access_payload(self, method: str,
                                               access_contract_list: List[str]) -> Payload:
        """
        内部方法: 生成原生合约访问待签名Payload
        :param method: 合约方法
        :param access_contract_list: 访问合约列表
        :return: 待签名Payload
        """

        params = {ParamKey.NATIVE_CONTRACT_NAME.name: json.dumps(access_contract_list)}
        payload = self._payload_builder.create_invoke_payload(SystemContractName.CONTRACT_MANAGE.name, method, params)
        return payload


class ContractManageWithEndorsers(BaseClient):
    def check_contract(self, contract_name: str) -> bool:
        """
        检查合约是否存在
        :param contract_name: 合约名称
        :return: 合约存在返回True, 否则返回False
        """
        contract = self.get_contract_info(contract_name)
        return contract is not None

    # 05-00 创建合约
    def create_contract(self, contract_name: str, byte_code_path: str, runtime_type: Union[RuntimeType, str],
                        params: Union[dict, list] = None, version: str = None, gas_limit: int = None, tx_id: str = None,
                        timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        创建合约
        :param contract_name: 合约名
        :param version: 合约版本
        :param byte_code_path: 合约字节码：可以是字节码；合约文件路径；或者 hex编码字符串；或者 base64编码字符串。
        :param runtime_type: contract_pb2.RuntimeType.WASMER
        :param params: 合约参数，dict类型，key 和 value 尽量为字符串
        :param gas_limit: Gas限制
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises ValueError: 如果 byte_code 不能转成合约字节码
        :raises: RequestError: 请求失败
        """
        payload = self.create_contract_create_payload(contract_name, version, byte_code_path, runtime_type,
                                                      params, tx_id=tx_id)

        if gas_limit is not None:
            payload.gas_limit = gas_limit
        elif self.get_chain_config().account_config.enable_gas:
            payload.gas_limit = self.estimate_gas(payload) + 3000

        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-01 升级合约
    def upgrade_contract(self, contract_name: str, byte_code_path: str, runtime_type: Union[RuntimeType, str],
                         params: Union[dict, list] = None, version: str = None, gas_limit: int = None,
                         tx_id: str = None,
                         timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        升级合约
        :param contract_name: 合约名
        :param version: 合约版本
        :param byte_code_path: 合约字节码：可以是字节码；合约文件路径；或者 hex编码字符串；或者 base64编码字符串。
        :param runtime_type: contract_pb2.RuntimeType.WASMER
        :param params: 合约参数，dict类型，key 和 value 尽量为字符串
        :param gas_limit: 交易Gas限制
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises ValueError: 如果 byte_code 不能转成合约字节码
        :raises: RequestError: 请求失败
        """
        payload = self.create_contract_upgrade_payload(contract_name, version, byte_code_path, runtime_type,
                                                       params, tx_id=tx_id)

        if gas_limit is not None:
            payload.gas_limit = gas_limit
        elif self.get_chain_config().account_config.enable_gas:
            payload.gas_limit = self.estimate_gas(payload) + 3000

        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-02 冻结合约
    def freeze_contract(self, contract_name: str, tx_id: str = None, timeout: int = None,
                        with_sync_result: bool = None) -> TxResponse:
        """
        冻结合约
        :param contract_name: 合约名称
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求失败
        """
        payload = self._create_contract_manage_payload(ContractManageMethod.FREEZE_CONTRACT.name, contract_name,
                                                       tx_id=tx_id)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-03 解冻合约
    def unfreeze_contract(self, contract_name: str, tx_id: str = None, timeout: int = None,
                          with_sync_result: bool = None) -> TxResponse:
        """
        解冻合约
        :param contract_name: 合约名称
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求失败
        """
        payload = self._create_contract_manage_payload(ContractManageMethod.UNFREEZE_CONTRACT.name, contract_name,
                                                       tx_id=tx_id)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-04 吊销合约
    def revoke_contract(self, contract_name: str, tx_id=None, timeout: int = None,
                        with_sync_result: bool = None) -> TxResponse:
        """
        吊销合约
        :param contract_name: 合约名称
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求失败
        """
        payload = self._create_contract_manage_payload(ContractManageMethod.REVOKE_CONTRACT.name, contract_name,
                                                       tx_id=tx_id)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def _gen_new_contract_version(self, contract_name: str, increase: float = 1.0) -> str:
        """
        查询合约当前版本，并生成合约新版本号
        :param contract_name: 合约名称
        :param increase: 在原版本基础上增加值，默认原版本+1
        :return: 合约版本
        """
        version = self.get_contract_info(contract_name).version
        return str(float(version) + increase)

    def invoke_system_contract(self, contract_name: str, method: str, params: Union[dict, list] = None,
                               tx_id: str = None, gas_limit: int = None,
                               timeout: int = None, with_sync_result: bool = False) -> TxResponse:
        """
        调用系统合约
        :param contract_name: 系统合约名称
        :param method: 系统合约方法
        :param params: 系统合约方法所需的参数
        :param tx_id: 指定交易Id，默认为空是生成随机交易Id
        :param gas_limit: Gas交易限制
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应信息
        """
        if timeout is None:
            timeout = DefaultConfig.rpc_send_tx_timeout
        if gas_limit is None:
            gas_limit = self._default_gas_limit

        payload = self._payload_builder.create_invoke_payload(contract_name, method, params, tx_id, gas_limit=gas_limit)
        response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 05-06 授权访问系统合约
    def grant_native_contract_access(self, contract_list: List[str],
                                     timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        授权访问系统合约
        :param contract_list: 待授权访问的系统合约列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        params = {ParamKey.NATIVE_CONTRACT_NAME.name: json.dumps(contract_list)}
        payload = self._payload_builder.create_invoke_payload(SystemContractName.CONTRACT_MANAGE.name,
                                                              ContractManageMethod.GRANT_CONTRACT_ACCESS.name,
                                                              params)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-06 吊销系统合约访问授权
    def revoke_native_contract_access(self, contract_list: List[str],
                                      timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        吊销系统合约访问授权
        :param contract_list: 待吊销访问带系统合约列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        params = {ParamKey.NATIVE_CONTRACT_NAME.name: json.dumps(contract_list)}
        payload = self._payload_builder.create_invoke_payload(SystemContractName.CONTRACT_MANAGE.name,
                                                              ContractManageMethod.REVOKE_CONTRACT_ACCESS.name,
                                                              params)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-07 验证系统合约访问授权
    def verify_native_contract_access(self, contract_list: List[Union[SystemContractName, str]],
                                      timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        验证系统合约是否可访问
        :param contract_list: 待验证合约列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        params = {ParamKey.NATIVE_CONTRACT_NAME.name: json.dumps(contract_list)}
        payload = self._payload_builder.create_invoke_payload(SystemContractName.CONTRACT_MANAGE.name,
                                                              ContractManageMethod.VERIFY_CONTRACT_ACCESS.name,
                                                              params)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-08 创建新的系统合约
    def init_new_native_contract(self, contract_name: str, version: str,
                                 byte_code_path: str,
                                 runtime_type: Union[RuntimeType, str],
                                 params: Union[dict, list] = None,
                                 gas_limit: int = None) -> Payload:
        """
        创建新的系统合约
        :param contract_name: 合约名
        :param version: 合约版本
        :param byte_code_path: 合约字节码：可以是字节码；合约文件路径；或者 hex编码字符串；或者 base64编码字符串。
        :param runtime_type: contract_pb2.RuntimeType.WASMER
        :param params: 合约参数，dict类型，key 和 value 尽量为字符串
        :param gas_limit: Gas交易限制
        :return: Payload
        :raises ValueError: 如果 byte_code 不能转成合约字节码
        """
        raise NotImplementedError('待实现')

    def send_txs(self, count=1, contract_name='counter', method='increase', gas_limit=None,
                 with_sync_result: bool = None) -> list:
        results = []
        for i in range(count):
            result = self.invoke_contract(contract_name, method, gas_limit=gas_limit, with_sync_result=with_sync_result)
            # check_response(result)
            results.append(result)
        return results
