#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   chainmaker_server.py
# @Function     :   ChainMaker系统合约(链查询相关)接口
from typing import Callable, List, Union

from chainmaker.apis.base_client import BaseClient
from chainmaker.keys import TxStage, TxType
from chainmaker.protos.common.transaction_pb2 import Transaction
from chainmaker.protos.txpool.transaction_pool_pb2 import (GetPoolStatusRequest, GetTxIdsByTypeAndStageRequest,
                                                           GetTxStatusRequest, GetTxsInPoolByTxIdsRequest, TxPoolStatus)
from chainmaker.utils.common import ensure_enum


class TxPoolMixIn(BaseClient):
    """交易池状态操作"""
    _get_client: Callable

    def get_pool_status(self) -> TxPoolStatus:
        """
        获取交易池状态
        :return:
        """
        self._debug("begin to get txpool status")
        req = GetPoolStatusRequest(chain_id=self.chain_id)
        return self._get_client().GetPoolStatus(req)

    def get_tx_ids_by_type_and_stage(self, tx_type: Union[TxType, str, int] = None,
                                     tx_stage: Union[TxStage, str, int] = None) -> List[str]:
        """
        获取不同交易类型和阶段中的交易Id列表。
        :param tx_type: 交易类型 在pb的txpool包中进行了定义
        :param tx_stage: 交易阶段 在pb的txpool包中进行了定义
        :return: 交易Id列表
        """
        if tx_type is None:
            tx_type = TxType.ALL_TYPE
        if tx_stage is None:
            tx_stage = TxStage.ALL_STAGE
        tx_type, tx_stage = ensure_enum(tx_type, TxType), ensure_enum(tx_stage, TxStage)
        self._debug("begin to get tx_ids by type and stage: [tx_type:%s]/[tx_stage:%s]" % (tx_type, tx_stage))
        req = GetTxIdsByTypeAndStageRequest(chain_id=self.chain_id,
                                            tx_type=tx_type.value,
                                            tx_stage=tx_stage.value)
        res = self._get_client().GetTxIdsByTypeAndStage(req)
        return res.tx_ids

    def get_txs_in_pool_by_tx_ids(self, tx_ids: List[str]) -> (List[Transaction], List[str]):
        """
        根据txIds获取交易池中存在的txs，并返回交易池缺失的tx的txIds
        :param tx_ids: 交易Id列表
        :return: [交易池中存在的txs, 交易池缺失的tx的txIds]
        """
        self._debug("begin to get transactions in txpool by tx_ids: %s" % tx_ids)

        req = GetTxsInPoolByTxIdsRequest(chain_id=self.chain_id,
                                         tx_ids=tx_ids)
        res = self._get_client().GetTxsInPoolByTxIds(req)
        return res.txs, res.tx_ids

    def get_tx_status(self, tx_id: str):
        self._debug("begin to get transaction status in txpool: %s" % tx_id)
        req = GetTxStatusRequest(chain_id=self.chain_id, tx_id=tx_id)
        res = self._get_client().GetTxStatus(req)
        return res.tx_status
