#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   base_client.py
# @Function     :   ChainMaker链客户端基类

import logging
from typing import Callable, List, Optional, Union

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec, rsa

from chainmaker.archive_service import ArchiveService
from chainmaker.conn_pool import ConnectionPool
from chainmaker.keys import (AuthType, )
from chainmaker.node import Node
from chainmaker.payload import PayloadBuilder
from chainmaker.sdk_config import ArchiveCenterConfig, ArchiveConfig, DefaultConfig, Pkcs11Config, RpcClientConfig
from chainmaker.user import User


class BaseClient(object):
    # common config 常规配置
    chain_id: str  # 链id
    user: User
    nodes: List[Node]
    node_cnt: int

    _conn_node: int

    _logger: logging.Logger  # 日志对象
    _poll: ConnectionPool  # 连接池
    _payload_builder: PayloadBuilder

    # archive config 归档配置
    _archive_config: ArchiveConfig
    # rpc客户端配置
    _rpc_client_config: RpcClientConfig
    _pkcs11_config: Pkcs11Config

    # additional 额外部分(在go-sdk之上增加的部分控制属性)
    _timeout: int  # rpc call 超时时间，请求超时太短会导致Deadline Exceeded
    _with_sync_result: bool  # 是否同步获取交易结果
    _tx_check_interval: int  # 交易轮询间隔
    _tx_check_timeout: int  # 交易轮询超时时间
    # retry config 重试配置
    _retry_limit: int  # rpc重试次数, 默认为5
    _retry_interval: int  # rpc重试间隔, 默认为0.5s
    _default_gas_limit: int  # 默认gas_limit值

    endorsers: List[User]  # 默认背书用户列表

    # 动态属性
    org_id: str  # 组织id
    hash_type: str  # 用户密钥/证书哈希类型，默认为 SHA256
    auth_type: AuthType  # 权限类型，默认为 AuthType.PermissionedWithCert
    sender_address: str  # 用户账户地址地址

    user_crt_bytes: bytes  # 用户PEM证书二进制内容  # todo remove
    user_crt: x509.Certificate  # 用户证书对象     # todo remove
    private_key: Union[ec.EllipticCurvePrivateKey, rsa.RSAPrivateKey]  # 用户私钥  # todo remove
    public_key: Union[ec.EllipticCurvePublicKey, rsa.RSAPublicKey]  # 用户公钥对象  # todo remove
    public_bytes: bytes  # 用户公钥二进制  # todo remove

    # cert_or_cert_bytes hash config  证书哈希配置
    enabled_cert_hash: bool = DefaultConfig.enable_cert_hash  # 是否以启用证书哈希
    # user_crt_hash: bytes = b''  # 对应的user.sign_cert_hash     # todo remove
    cert_hash: str
    cert_hash_bytes: bytes

    # cert_or_cert_bytes alias config 证书别名配置
    # enabled_alias: bool = DefaultConfig.enable_alias  # 是否已启用证书别名
    alias: str = None  # 用户证书别名  # todo remove

    # default TimestampKey , true NormalKey support
    enable_normal_key: bool

    archive_center_query_first: Optional[bool] = None
    archive_center_config: Optional[ArchiveCenterConfig] = None
    archive_service: Optional[ArchiveService]
    enabled_gas: bool
    retry_on_txpool_full: bool = False

    send_request_with_sync_result: Callable
    _create_chain_config_manage_payload: Callable
    _create_cert_manage_payload: Callable
    send_request: Callable

    def _debug(self, msg: str, *args):
        self._logger.debug('[Sdk] %s' % msg, *args)
        # self._logger.debug('[Sdk] [%s] %s' % (self.node.node_addr, msg), *args)

    def _info(self, msg: str, *args):
        self._logger.info('[Sdk] %s' % msg, *args)
        # self._logger.info('[Sdk] [%s] %s' % (self.node.node_addr, msg), *args)

    def _warn(self, msg: str, *args):
        self._logger.warning('[Sdk] %s' % msg, *args)

    def _exception(self, ex):
        self._logger.exception(ex)

    def _error(self, msg: str, *args):
        self._logger.error('[Sdk] %s' % msg, *args)
        # self._logger.error('[Sdk] [%s] %s' % (self.node.node_addr, msg), *args)

    def _critical(self, msg: str, *args):
        self._logger.critical('[Sdk] %s' % msg, *args)

