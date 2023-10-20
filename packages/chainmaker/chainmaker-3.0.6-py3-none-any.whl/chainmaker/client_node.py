#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   node.py
# @Function     :   ChainMaker客户端连接节点
import warnings
# from functools import cached_property
from typing import List, Union

from chainmaker.sdk_config import DefaultConfig
from chainmaker.utils import crypto_utils


class ClientNode(object):
    """客户端链接节点"""
    def __init__(self, node_addr: str, conn_cnt: int = None,
                 enable_tls: bool = False, trust_cas: Union[bytes, List[bytes]] = None, tls_host_name=None):
        """
        客户端连接节点
        :param node_addr: 必须, 节点RPC地址，eg. 127.0.0.1:12301
        :param conn_cnt: 创建连接数量，默认为1
        :param enable_tls: 是否启用tls
        :param trust_root_paths: ca证书二进制内容列表，或ca证书二进制列表连接成的byte字符串
        :param tls_host_name: tls服务器名称
        """
        self.node_addr = node_addr
        self.conn_cnt = conn_cnt or DefaultConfig.conn_cnt

        self.enable_tls = enable_tls
        self.trust_roots = b''.join(trust_cas)  if isinstance(trust_cas, list) else trust_cas
        self.tls_host_name = tls_host_name

    def __repr__(self):
        if self.node_addr:
            return f'<ClientNode %s>' % self.node_addr
        return '<ClientNode>'

    def __eq__(self, other):
        if hasattr(other, 'node_addr'):
            return self.node_addr == other.node_addr
        return False

    def add_trust_roots(self, trust_root_paths: List[str]):
        """
        添加信任CA
        :param trust_root_paths: CA目录(需包含ca.key和ca.crt)
        """
        new_trust_roots = crypto_utils.merge_cert_pems(trust_root_paths) if trust_root_paths else b''
        self.trust_roots = b''.join([self.trust_roots, new_trust_roots])

    def update_trust_roots(self, trust_root_paths: List[str]):
        """
        更新信任CA
        :param trust_root_paths: CA目录(需包含ca.key和ca.crt)
        """
        self.trust_roots = crypto_utils.merge_cert_pems(trust_root_paths) if trust_root_paths else b''

    #
    # @cached_property
    # def addr(self):
    #     warnings.warn('请使用node.node_addr', DeprecationWarning)
    #     return self.node_addr

    # @cached_property
    # def index(self):
    #     warnings.warn('请使用node.conn_node', DeprecationWarning)
    #     return self.conn_node

    # @cached_property
    # def trusted_ca_bytes(self):
    #     return crypto_utils.merge_cert_pems(self.trust_root_paths) if self.trust_root_paths else b''

    @classmethod
    def from_conf(cls, node_addr, conn_cnt=None,
                  enable_tls=False, trust_root_paths: List[str] = None, tls_host_name: str = None):
        trust_roots = crypto_utils.merge_cert_pems(trust_root_paths) if trust_root_paths else b''
        return cls(node_addr=node_addr, conn_cnt=conn_cnt,
                   enable_tls=enable_tls, trust_cas=trust_roots, tls_host_name=tls_host_name)
