#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   private_contract_api.py
# @Function     :   ChainMaker 隐私系统合约接口-待实现
import json
from typing import List

from chainmaker.apis.base_client import BaseClient
from chainmaker.protos.common.request_pb2 import Payload
from chainmaker.protos.common.result_pb2 import PrivateGetContract, TxResponse
from chainmaker.user import ClientUser
from chainmaker.keys import ParamKey, SystemContractName, PrivateComputeMethod


class PrivateComputeMixIn(BaseClient):
    """隐私计算"""

    # 06-00 获取合约代码
    def get_contract(self, contract_name: str, code_hash: str) -> PrivateGetContract:
        """
        获取合约代码
        :param contract_name: 合约名称
        :param code_hash: 代码哈希
        :return: 隐私合约
        """
        self._debug('begin to get contract')
        params = {
            ParamKey.contract_name.name: contract_name,
            ParamKey.code_hash.name: code_hash,
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.GET_CONTRACT.name, params)
        response = self.send_request(payload)
        data = response.contract_result.reslut
        private_get_contract = PrivateGetContract()
        private_get_contract.ParseFromString(data)
        return private_get_contract

    # 06-01 获取隐私数据
    def get_data(self, contract_name: str, key: str) -> bytes:
        """
        获取隐私数据
        :param contract_name: 合约名称
        :param key: 键名
        :return: 键对应的数据
        """
        self._debug('begin to get data')
        params = {
            ParamKey.contract_name.name: contract_name,
            ParamKey.key.name: key,
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.GET_DATA.name, params)
        response = self.send_request(payload)
        return response.contract_result.reslut

    # 06-02 保存可信执行环境证书
    def save_enclave_ca_cert(self, enclave_ca_cert: str,
                             tx_id: str = None, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        保存可信执行环境根证书
        :param enclave_ca_cert: 可信执行环境根证书
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 交易响应
        """
        self._debug('begin to save ca cert')

        payload = self.create_save_enclave_ca_cert_payload(enclave_ca_cert, tx_id)
        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 06-03 保存隐私数据目录
    def save_dir(self, order_id: str, private_dir: list,
                 tx_id: str = None, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        保存隐私数据目录
        :param order_id: 序号
        :param private_dir: 隐私数据目录
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 交易响应
        """
        self._debug('begin to save dir')
        params = {
            ParamKey.order_id.name: order_id,
            ParamKey.private_dir.name: json.dumps(private_dir)
        }
        payload = self._payload_builder.create_invoke_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                              PrivateComputeMethod.SAVE_DIR.name, params, tx_id=tx_id)
        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 06-04 保存隐私计算结果数据
    def save_data(self, contract_name: str, contract_version: str, is_deployment: bool, code_hash: bytes,
                  report_hash: bytes, result: dict,
                  code_header: bytes, rwset: dict, sign: bytes, events: list, private_req: bytes,
                  tx_id: str = None, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        保存隐私计算结果数据
        :param contract_name: 合约名称
        :param contract_version: 合约版本
        :param is_deployment: 是否部署
        :param code_hash:
        :param code_header:
        :param report_hash:
        :param result:
        :param events: 事件列表
        :param rwset: 读写集
        :param sign: 签名数据
        :param private_req:
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 交易响应
        """
        self._debug('begin to save data')
        params = {
            ParamKey.contract_name.name: contract_name,
            ParamKey.version.name: contract_version,
            ParamKey.code_header.name: code_header,
            ParamKey.code_hash.name: code_hash,
            ParamKey.is_deploy.name: is_deployment,
            ParamKey.rw_set.name: json.dumps(rwset),
            ParamKey.events.name: json.dumps(events),
            ParamKey.report_hash.name: report_hash,
            ParamKey.result.name: json.dumps(result),
            ParamKey.sign.name: sign,
        }
        payload = self._payload_builder.create_invoke_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                              PrivateComputeMethod.SAVE_DATA.name, params, tx_id=tx_id)
        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 06-05 获取可信执行环境报告
    def save_enclave_report(self, enclave_id: str, report: str,
                            tx_id: str = None, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        获取可信执行环境报告
        :param enclave_id: 可信执行环境Id
        :param report: 报告数据
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 交易响应
        """
        self._debug('begin to save enclave report')
        payload = self.create_save_enclave_report_payload(enclave_id, report, tx_id)
        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 06-06 获取可信执行环境证明
    def get_enclave_proof(self, enclave_id: str) -> bytes:
        """
        获取可信执行环境证明
        :param enclave_id: 可信执行环境Id
        :return:
        """
        self._debug('begin to get enclave proof')
        params = {
            ParamKey.enclave_id.name: enclave_id,
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.GET_ENCLAVE_PROOF.name, params)
        return self.send_request(payload)

    # 06-07 获取可信执行环境证书
    def get_enclave_ca_cert(self) -> bytes:
        """
        获取可信执行环境证书
        :return: 证书二进制数据
        """
        self._debug('begin to get ca cert')
        params = {}
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.GET_CA_CERT.name, params)
        return self.send_request(payload)

    # 06-08 获取隐私数据目录
    def get_dir(self, order_id: str) -> bytes:
        """
        获取隐私数据目录
        :param order_id: 序号
        :return: 数据目录二进制内容
        """
        self._debug('begin to get dir')
        params = {
            ParamKey.order_id.name: order_id
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.GET_DIR.name, params)
        return self.send_request(payload)

    # 06-09 检查调用者证书授权
    def check_caller_cert_auth(self, payload: str, org_ids: List[str], sign_pairs: dict) -> TxResponse:
        """
        检查调用者证书授权
        :param payload: 待签名Payload
        :param org_ids: 序号列表
        :param sign_pairs: 签名对
        :return: 交易响应
        """
        self._debug('begin to check caller cert auth')
        params = {
            ParamKey.payload.name: payload,
            ParamKey.order_ids.name: json.dumps(org_ids),
            ParamKey.sign_pairs.name: json.dumps(sign_pairs),
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.CHECK_CALLER_CERT_AUTH.name, params)
        return self.send_request(payload)

    # 06-10 获取可信执行环境加密公钥
    def get_enclave_encrypt_pubkey(self, enclave_id: str) -> bytes:
        """
        获取可信执行环境加密公钥
        :param enclave_id: 可信执行环境Id
        :return: 公钥二进制数据
        """
        self._debug('begin to get enclave encrypt pubkey')
        params = {
            ParamKey.enclave_id.name: enclave_id
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.GET_ENCLAVE_ENCRYPT_PUB_KEY.name,
                                                             params)
        return self.send_request(payload)

    # 06-11 获取可信执行环境验证公钥
    def get_enclave_verification_pubkey(self, enclave_id: str) -> bytes:
        """
        获取可信执行环境验证公钥
        :param enclave_id: 可信执行环境Id
        :return: 公钥二进制数据
        """
        self._debug('begin to get enclave verification pubkey')
        params = {
            ParamKey.enclave_id.name: enclave_id
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.GET_ENCLAVE_VERIFICATION_PUB_KEY.name,
                                                             params)
        return self.send_request(payload)

    # 06-12 获取可信执行环境报告
    def get_enclave_report(self, enclave_id: str) -> bytes:
        """
        获取可信执行环境报告
        :param enclave_id: 可信执行环境Id
        :return: 报告二进制数据
        """
        self._debug('begin to get enclave report')
        params = {
            ParamKey.enclave_id.name: enclave_id
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.GET_ENCLAVE_REPORT.name,
                                                             params)
        return self.send_request(payload)

    # 06-13 获取可信执行环境挑战
    def get_enclave_challenge(self, enclave_id: str) -> bytes:
        """
        获取可信执行环境挑战
        :param enclave_id: 可信执行环境Id
        :return: 挑战二进制数据
        """
        self._debug('begin to get enclave challenge')
        params = {
            ParamKey.enclave_id.name: enclave_id
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.GET_ENCLAVE_CHALLENGE.name,
                                                             params)
        return self.send_request(payload)

    # 06-14 获取可信执行环境签名
    def get_enclave_signature(self, enclave_id: str) -> bytes:
        """
        获取可信执行环境签名
        :param enclave_id: 可信执行环境Id
        :return: 签名二进制数据
        """
        self._debug('begin to get enclave signature')
        params = {
            ParamKey.enclave_id.name: enclave_id
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                             PrivateComputeMethod.GET_ENCLAVE_SIGNATURE.name,
                                                             params)
        return self.send_request(payload)

    # 06-15 保存远端认证证明
    def save_remote_attestation_proof(self, proof: str,
                                      tx_id: str = None, timeout: int = None,
                                      with_sync_result: bool = None) -> TxResponse:
        """
        保存远端认证证明
        :param proof: 证明数据
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 交易响应
        """
        self._debug('begin to save remote attestation proof')
        params = {
            ParamKey.proof.name: proof,
        }
        payload = self._payload_builder.create_invoke_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                              PrivateComputeMethod.SAVE_REMOTE_ATTESTATION.name, params,
                                                              tx_id=tx_id)
        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 创建保存可信执行环境根证书待签名Payload
    def create_save_enclave_ca_cert_payload(self, enclave_ca_cert: str, tx_id: str = None) -> Payload:
        """
        创建保存可信执行环境根证书待签名Payload
        :param enclave_ca_cert: 可信执行环境根证书
        :param tx_id: 指定交易Id
        :return: 待签名Payload
        """
        self._debug('begin create [PRIVATE_COMPUTE-SAVE_CA_CERT] to be signed payload')
        params = {
            ParamKey.ca_cert.name: enclave_ca_cert,
        }
        payload = self._payload_builder.create_invoke_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                              PrivateComputeMethod.SAVE_CA_CERT.name, params,
                                                              tx_id=tx_id)
        return payload

    # 06-创建可信执行环境报告待签名Payload
    def create_save_enclave_report_payload(self, enclave_id: str, report: str, tx_id: str = None) -> Payload:
        """
        创建可信执行环境报告待签名Payload
        :param enclave_id: 可信执行环境Id
        :param report: 报告数据
        :param tx_id: 指定交易Id
        :return: 待签名Payload
        """
        self._debug('begin to create [PRIVATE_COMPUTE-SAVE_ENCLAVE_REPORT] to be signed payload')
        params = {
            ParamKey.enclave_id.name: enclave_id,
            ParamKey.report.name: report
        }
        return self._payload_builder.create_invoke_payload(SystemContractName.PRIVATE_COMPUTE.name,
                                                           PrivateComputeMethod.SAVE_ENCLAVE_REPORT.name, params,
                                                           tx_id=tx_id)

    def send_multi_signing_request(self, payload: Payload, endorsers: List[ClientUser] = None,
                                   timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        发送多签请求
        :param payload: 待签名Payload
        :param endorsers: 背书用户列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 交易响应
        """

        endorsers = self._create_endorsers(payload, endorsers)

        return self.send_request_with_sync_result(payload, endorsers, timeout, with_sync_result)
