#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   payload.py
# @Function     :   ChainMaker生成Payload


import time
from typing import Union, Dict

from chainmaker.protos.common.request_pb2 import Payload, TxType, Limit
from chainmaker.sdk_config import DefaultConfig
from chainmaker.utils import common


class PayloadBuilder:
    """Payload构建者"""

    def __init__(self, chain_id):
        self.chain_id = chain_id

    def create_invoke_payload(self, contract_name: str, method: str, params: Dict[str, Union[str, int, bool]] = None,
                              tx_id="", seq=0,
                              gas_limit: int = None) -> Payload:
        return self._create_payload(TxType.INVOKE_CONTRACT, contract_name, method, params, tx_id, seq, gas_limit)

    def create_query_payload(self, contract_name: str, method: str, params: Dict[str, Union[str, int, bool]] = None,
                             tx_id="", seq=0) -> Payload:
        return self._create_payload(TxType.QUERY_CONTRACT, contract_name, method, params, tx_id, seq)

    def create_subscribe_payload(self, contract_name: str, method: str, params: Dict[str, Union[str, int, bool]] = None,
                                 tx_id="", seq=0) -> Payload:
        return self._create_payload(TxType.SUBSCRIBE, contract_name, method, params, tx_id, seq)

    def create_archive_payload(self, contract_name: str, method: str,
                               params: Dict[str, Union[str, int, bool, bytes]] = None,
                               tx_id: str = "", seq: int = 0) -> Payload:
        return self._create_payload(TxType.ARCHIVE, contract_name, method, params, tx_id, seq)

    def _create_payload(self, tx_type: TxType, contract_name: str, method: str, params: Union[dict, list] = None,
                        tx_id="", seq=0, gas_limit: int = None) -> Payload:
        tx_id = tx_id or common.gen_rand_tx_id()
        kv_pairs = common.params_map_kv_pairs(params)
        if gas_limit is None:
            gas_limit = DefaultConfig.gas_limit
        return Payload(chain_id=self.chain_id, tx_type=tx_type, tx_id=tx_id, timestamp=int(time.time()),
                       contract_name=contract_name, method=method, parameters=kv_pairs, sequence=seq,
                       limit=Limit(gas_limit=gas_limit))

    def create_payload(self, tx_type: TxType, contract_name: str, method: str, params: Union[dict, list] = None,
                        tx_id="", seq=0, gas_limit: int = None):
        return self._create_payload(tx_type, contract_name, method, params, tx_id, seq, gas_limit)
