#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   transaction_manager.py
# @Function     :   ChainMaker交易黑名单管理接口

from typing import Callable, List

from chainmaker.apis.base_client import BaseClient
from chainmaker.keys import SystemContractName, TransactionManagerMethod
from chainmaker.protos.common.result_pb2 import TxResponse


class TransactionManagerMixIn(BaseClient):
    invoke_system_contract: Callable
    query_system_contract: Callable

    def add_black_list_tx_ids(self, tx_ids: List[str]) -> TxResponse:
        params = {'txIds': ','.join(tx_ids)}

        return self.invoke_system_contract(
            contract_name=SystemContractName.TRANSACTION_MANAGER.name,
            method=TransactionManagerMethod.ADD_BLACKLIST_TX_IDS.name,
            params=params,
            with_sync_result=True
        )

    def delete_black_list_tx_ids(self, tx_ids: List[str]) -> TxResponse:
        params = {'txIds': ','.join(tx_ids)}

        return self.invoke_system_contract(
            contract_name=SystemContractName.TRANSACTION_MANAGER.name,
            method=TransactionManagerMethod.DELETE_BLACKLIST_TX_IDS.name,
            params=params,
            with_sync_result=True
        )

    def get_black_list_tx_ids(self, tx_ids: List[str]) -> TxResponse:
        params = {'txIds': ','.join(tx_ids)}

        return self.query_system_contract(
            contract_name=SystemContractName.TRANSACTION_MANAGER.name,
            method=TransactionManagerMethod.DELETE_BLACKLIST_TX_IDS.name,
            params=params,
        )
