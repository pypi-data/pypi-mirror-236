#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   archive_service.py
# @Function     :   归档服务抽象接口

import abc
from typing import Callable, Iterable

from chainmaker.protos.archivecenter.archivecenter_pb2 import ArchiveStatusResp
from chainmaker.protos.common.block_pb2 import BlockInfo
from chainmaker.protos.common.transaction_pb2 import TransactionInfo, TransactionInfoWithRWSet
from chainmaker.protos.config.chain_config_pb2 import ChainConfig


class ArchiveService(metaclass=abc.ABCMeta):
    def __init__(self, cc):
        self.cc = cc  # 必须为admin用户
        self.chain_id = self.cc.chain_id
        self.logger = cc.logger

    @abc.abstractmethod
    def get_tx_by_tx_id(self, tx_id: str) -> TransactionInfo:
        """
        根据交易id获取交易
        :param tx_id: 交易id
        :return: 交易
        """

    @abc.abstractmethod
    def get_tx_with_rwset_by_tx_id(self, tx_id: str) -> TransactionInfoWithRWSet:
        """
        根据交易id获取包含rwset的交易
        :param tx_id: 交易Id
        :return: 包含rwset的交易
        """

    @abc.abstractmethod
    def get_block_by_height(self, block_height: int, with_rw_set: bool = False) -> BlockInfo:
        """
        根据区块高度获取区块
        :param block_height:
        :param with_rw_set: 是否包含读写集
        :return: 区块信息
        """

    @abc.abstractmethod
    def get_block_by_hash(self, block_hash: str, with_rw_set: bool = False) -> BlockInfo:
        """
        根据区块哈希获取区块
        :param block_hash: 区块哈希
        :param with_rw_set: 是否包含读写集
        :return: 区块信息
        """

    @abc.abstractmethod
    def get_block_by_tx_id(self, tx_id: str, with_rw_set: bool = False) -> BlockInfo:
        """
        根据交易id获取区块
        :param tx_id: 交易id
        :param with_rw_set: 是否包含读写集
        :return: 区块信息
        """

    @abc.abstractmethod
    def get_chain_config_by_block_height(self, block_height: int) -> ChainConfig:
        """
        根据区块高度获取链配置
        :param block_height:
        :return: 区块信息
        """

    @abc.abstractmethod
    def register(self, genesis: BlockInfo) -> None:
        """
        注册区块
        :param genesis: 链的第一个区块
        :return: None
        """

    @abc.abstractmethod
    def archive_block(self, block: BlockInfo) -> None:
        """
        归档单个区块
        :param block:
        :return: None
        """

    @abc.abstractmethod
    def archive_blocks(self, blocks: Iterable, notice: Callable = None) -> None:
        """
        批量归档区块
        :param blocks: 区块迭代器
        :param notice:
        :return: None
        """

    @abc.abstractmethod
    def get_archived_status(self) -> ArchiveStatusResp:
        """
        获取归档状态
        :return:
        """
