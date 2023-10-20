#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   conn_pool.py
# @Function     :   ChainMaker 链接池
import random
import time
from typing import List

import grpc

from chainmaker.node import ClientNode
from chainmaker.exceptions import ERR_MSG_MAP, RpcConnectError
from chainmaker.protos.api.rpc_node_pb2_grpc import RpcNodeStub
from chainmaker.protos.common.request_pb2 import TxRequest
from chainmaker.protos.common.result_pb2 import TxResponse
from chainmaker.sdk_config import DefaultConfig, DEFAULT_RPC_CLIENT_CONFIG


class ConnectionPool:
    def __init__(self, user, nodes: List[ClientNode], rpc_client_config=None, conn_node: int = None, logger=None):
        self.user = user
        self.nodes = nodes
        self.rpc_client_config = rpc_client_config or DEFAULT_RPC_CLIENT_CONFIG
        self.node_cnt = len(nodes)
        self.conn_node = conn_node
        self._logger = logger

        self.pool = self.init_channels()  # 结构为二位列表 [[channel1, channel2],[channel3, channel4]]
        if isinstance(self.conn_node, int) and self.conn_node < len(self.nodes):
            self._node = self.nodes[self.conn_node]
        else:
            self._node = nodes[0]  # 当前连接节点, 默认为节点1

    def init_channels(self):
        if isinstance(self.conn_node, int) and self.conn_node < len(self.nodes):
            node = self.nodes[self.conn_node]
            return [[self.get_channel(node) for _ in range(node.conn_cnt)]]
        return [[self.get_channel(node) for _ in range(node.conn_cnt)] for node in self.nodes]

    def get_channel(self, node: ClientNode) -> grpc.Channel:
        """
        根据节点获取连接
        :param node: 连接节点
        :return: Node桩
        """
        max_send_message_size = self.rpc_client_config.max_send_message_size \
                                or DefaultConfig.rpc_max_send_message_length
        max_receive_message_size = self.rpc_client_config.max_receive_message_size \
                                   or DefaultConfig.rpc_max_receive_message_length
        opts = [
            ('grpc.max_send_message_length', max_send_message_size * 1024 * 1024),
            ('grpc.max_receive_message_length', max_receive_message_size * 1024 * 1024)
        ]

        # todo grpc.WithKeepaliveParams(kacp),
        # 	var kacp = keepalive.ClientParameters{
        # 		Time:                10 * time.Second, // send pings every 10 seconds if there is no activity
        # 		Timeout:             time.Second,      // wait 1 second for ping ack before considering the connection dead
        # 		PermitWithoutStream: true,             // send pings even without active streams
        # 	}

        if node.enable_tls is True:
            # 创建 双向tls 的 secure channel
            # credential = grpc.metadata_call_credentials()
            credential = grpc.ssl_channel_credentials(root_certificates=node.trust_roots,
                                                      private_key=self.user.tls_key_bytes,
                                                      certificate_chain=self.user.tls_cert_bytes)

            # 如果启用了tls_host_name, 则以tls_host_name来验证tls连接。
            if node.tls_host_name:
                opts.append(('grpc.ssl_target_name_override', node.tls_host_name))

            channel = grpc.secure_channel(node.node_addr, credential, options=opts)
        else:
            # 创建 insecure channel
            channel = grpc.insecure_channel(node.node_addr, options=opts)
        return channel

    @staticmethod
    def _check_server_identity(host, cert):
        return True

    #     authContext = newAuthContextFromPem(cert)
    #     if authContext.name != expectedName or authContext.environment != myEnvironment:
    #         return False
    #     return True

    def _get_random_channel(self) -> (ClientNode, grpc.Channel):
        conn_node = random.randint(0, len(self.pool) - 1)
        return self.nodes[conn_node], random.choice(self.pool[conn_node])

    def _get_node_random_channel(self, conn_node: int) -> (ClientNode, grpc.Channel):
        # if not 0 <= conn_node < len(self.pool):
        #     raise ValueError(f'conn_node: {conn_node} 应大于0并小于节点长度 {len(self.nodes)}')
        if conn_node < len(self.nodes):
            index = conn_node
        else:
            index = 0
        return self.nodes[index], random.choice(self.pool[index])

    @property
    def node(self) -> ClientNode:
        """当前连接节点"""
        return self._node

    def _get_channel(self, conn_node: int = None) -> grpc.Channel:
        if conn_node is None:
            self._node, channel = self._get_random_channel()
        else:
            self._node, channel = self._get_node_random_channel(conn_node)
        return channel

    def get_client(self, conn_node: int = None) -> RpcNodeStub:
        """
        根据策略或去连接
        :param conn_node: 节点索引
        :return:
        """
        # for i in range(DefaultConfig.rpc_retry_limit):
        #     channel = self._get_channel(conn_node)
        # if channel.get_state() == grpc.ChannelConnectivity.READY:
        #     break
        channel = self._get_channel(conn_node)
        # self._logger.debug(f'[Sdk] get channel for node {self.node.node_addr}')
        stub = RpcNodeStub(channel)
        return stub

    def send_rpc_request(self, tx_request: TxRequest, timeout: int, conn_node: int = None,
                         retry_limit: int = None, retry_interval: int = None) -> TxResponse:
        """
        发送带重连的RPC请求
        :param tx_request: 请求体
        :param timeout: RPC请求超时时间
        :param conn_node: 节点索引
        :param retry_limit: 重连次数限制
        :param retry_interval: 重连间隔时间，单位毫秒
        :return: 交易响应TxResponse对象
        :raise 重连超过retry_limit限制仍无法成功时抛出 RpcConnectError
        """
        '''
        if ok && (statusErr.Code() == codes.DeadlineExceeded ||
                // desc = "transport: Error while dialing dial tcp 127.0.0.1:12301: connect: connection refused"
                statusErr.Code() == codes.Unavailable) {

                resp.Code = common.TxStatusCode_TIMEOUT
                errMsg = fmt.Sprintf("call [%s] meet network error, try to connect another node if has, %s",
                    client.ID, err.Error())

                cc.logger.Errorf(sdkErrStringFormat, errMsg)
                ignoreAddrs[client.ID] = struct{}{}
                continue
            }

            cc.logger.Errorf("statusErr.Code() : %s", statusErr.Code())

            resp.Code = common.TxStatusCode_INTERNAL_ERROR
            errMsg = fmt.Sprintf("client.call failed, %+v", err)
            cc.logger.Errorf(sdkErrStringFormat, errMsg)
            return resp, fmt.Errorf(errMsg)
        '''
        if retry_limit is None:
            retry_limit = DefaultConfig.rpc_retry_limit
        if retry_interval is None:
            retry_interval = DefaultConfig.rpc_retry_interval

        err_msg = ''
        for i in range(retry_limit):
            try:
                return self.get_client(conn_node).SendRequest(tx_request, timeout=timeout)
            except grpc.RpcError as ex:
                # todo 处理 DeadlineExceeded
                err_msg = ERR_MSG_MAP.get(ex.details(), ex.details())
                # self._logger.exception(ex)
                time.sleep(retry_interval // 1000)  # 毫秒
                self._logger.debug('[Sdk] retry to send rpc request to %s' % self.node.node_addr)

        else:
            raise RpcConnectError(
                '[Sdk] rpc service<%s enable_tls=%s> not available: %s' % (
                    self.node.node_addr, self.node.enable_tls, err_msg))

    def close(self):
        [channel.close() for channels in self.pool for channel in channels]
