#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   chainmaker_server.py
# @Function     :   ChainMaker系统合约(链查询相关)接口
import json
import time
from typing import List
from typing import Union

import grpc

from chainmaker.apis.base_client import BaseClient
from chainmaker.exceptions import ERR_MSG_MAP, RpcConnectError, ContractFail
from chainmaker.keys import TxType, TxStage
from chainmaker.protos.common.request_pb2 import TxRequest

from chainmaker.protos.common.result_pb2 import Result
from chainmaker.protos.txpool.transaction_pool_pb2 import GetTxStatusRequest
from chainmaker.sdk_config import DefaultConfig
from chainmaker.utils.common import ensure_enum


class ChainMakerServerMixIn(BaseClient):
    """ChainMaker服务操作"""

    def get_chainmaker_server_version(self) -> str:
        """获取chainmaker服务版本号"""
        self._debug('begin to get chainmaker server version')
        tx_request = TxRequest()

        retry_limit = DefaultConfig.rpc_retry_limit
        retry_interval = DefaultConfig.rpc_retry_interval

        err_msg = ''
        for i in range(retry_limit):
            try:
                return self._get_client().GetChainMakerVersion(tx_request).version
            except grpc._channel._InactiveRpcError as ex:
                # todo 处理 DeadlineExceeded
                err_msg = ERR_MSG_MAP.get(ex.details(), ex.details())
                # self._logger.exception(ex)
                time.sleep(retry_interval // 1000)  # 毫秒
                self._logger.debug('[Sdk] %s, retry to send rpc request to %s' % (ex.details(), self.node.node_addr))
        else:
            raise RpcConnectError(
                '[Sdk] rpc service<%s enable_tls=%s> not available: %s' % (
                    self.node.node_addr, self.node.enable_tls, err_msg))


class CanonicalTxResultMixIn(BaseClient):
    """权威交易结果"""

    def sync_canonical_tx_result(self, tx_id: str) -> Result:
        """
         同步获取权威的公认的交易结果，即超过半数共识的交易
        :param tx_id:
        :return:
        """

    def _canonical_polling_tx_result(self, ctx, pool):
        pass

    def _canonical_get_tx_by_tx_id(self, tx_id):
        # params = {ParamKey.txId.name: tx_id}
        # payload = self._payload_builder.create_query_payload(SystemContractName.CHAIN_QUERY.name,
        #                                                      ChainQueryMethod.GET_TX_BY_TX_ID.name,
        #                                                      params)
        # tx_request = self._generate_tx_request(payload)
        for i in range(self.node_cnt):
            self._node_index = i
            try:
                return self.get_tx_by_tx_id(tx_id)
            except ContractFail:
                pass
