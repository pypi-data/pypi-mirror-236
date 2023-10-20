#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   pubkey_manage.py
# @Function     :   ChainMaker 公钥管理接口
from typing import Callable, Dict, Union

from chainmaker.apis.base_client import BaseClient
from chainmaker.keys import SystemContractName, PubkeyManageMethod, ParamKey, Role
from chainmaker.protos.common.request_pb2 import Payload
from chainmaker.protos.common.result_pb2 import TxResponse


class PubkeyManageMixIn(BaseClient):
    """公钥管理操作"""

    # 12-00 创建公钥添加待签名Payload
    def create_pubkey_add_payload(self, pubkey: str, org_id: str, role: Union[Role, str]) -> Payload:
        """
        创建公钥添加待签名Payload
        <12-00-PUBKEY_MANAGE-PUBKEY_ADD>
        :param pubkey: 公钥文件内容
        :param org_id: 组织ID
        :param role: 角色
        :return: 待签名Payload
        """
        self._debug('begin to create [PUBKEY_MANAGE-PUBKEY_ADD] to be signed payload')
        params = {
            ParamKey.pubkey.name: pubkey,
            ParamKey.org_id.name: org_id,
            ParamKey.role.name: role
        }
        return self._create_pubkey_manage_payload(PubkeyManageMethod.PUBKEY_ADD.name, params)

    # 12-01 创建公钥删除待签名Payload
    def create_pubkey_delete_payload(self, pubkey: str, org_id: str) -> Payload:
        """
        创建公钥删除待签名Payload
        <12-01-PUBKEY_MANAGE-PUBKEY_DELETE>
        :param pubkey: 公钥
        :param org_id: 组织id
        :return: 待签名Payload
        """
        self._debug('begin to create [PUBKEY_MANAGE-PUBKEY_DELETE] to be signed payload')
        params = {
            ParamKey.pubkey.name: pubkey,
            ParamKey.org_id.name: org_id,
        }
        return self._create_pubkey_manage_payload(PubkeyManageMethod.PUBKEY_DELETE.name, params)

    # 12-02 查询公钥
    def query_pubkey(self, pubkey: str, timeout: int = None) -> TxResponse:
        """
        查询公钥
        <12-02-PUBKEY_MANAGE-PUBKEY_QUERY>
        :param pubkey:公钥文件内容
        :param timeout: RPC请求超时时间
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        self._debug('begin to query pubkey')
        params = {
            ParamKey.pubkey.name: pubkey,
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.PUBKEY_MANAGE.name,
                                                             PubkeyManageMethod.PUBKEY_QUERY.name, params)
        return self.send_request(payload, timeout=timeout)

    def send_pubkey_manage_request(self, payload, endorsers: list = (), timeout: int = None,
                                   with_sync_result: bool = False) -> TxResponse:
        """
        发送公钥管理请求
        :param payload: 公钥管理payload
        :param endorsers: 背书列表
        :param timeout: 超时时间
        :param with_sync_result: 是否同步结果
        :return: 交易响应或事务交易信息
        """
        return self.send_request_with_sync_result(payload, endorsers, timeout, with_sync_result)

    def _create_pubkey_manage_payload(self, method: str, params: Dict[str, Union[str, int, bool]] = None) -> Payload:
        """
        私有方法-创建公钥管理Payload
        :param method: 对应的公钥管理方法
        :param params: 相关参数
        :return: 生成的payload
        """
        payload = self._payload_builder.create_invoke_payload(SystemContractName.PUBKEY_MANAGE.name, method, params)
        return payload


class PubkeyManageWithEndorsers(BaseClient):
    create_pubkey_add_payload: Callable
    create_pubkey_delete_payload: Callable
    send_manage_request: Callable

    # 12-00 添加公钥
    def add_pubkey(self, pubkey: str, org_id: str, role: Union[Role, str], timeout: int = None,
                   with_sync_result: bool = True) -> TxResponse:
        """
        添加公钥
        :param pubkey: 公钥文件内容
        :param org_id: 组织ID
        :param role: 角色
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        payload = self.create_pubkey_add_payload(pubkey, org_id, role)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 12-01 删除公钥
    def delete_pubkey(self, pubkey: str, org_id: str, timeout: int = None, with_sync_result: bool = True):
        """
        删除公钥
        :param pubkey: 公钥文件内容
        :param org_id: 组织ID
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        payload = self.create_pubkey_delete_payload(pubkey, org_id)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
