#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   chain_manager.py
# @Function     :   ChainMaker管理操作接口(带背书客户端)
import functools
import json
import os
import random
import time
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

from hostz import Host

from chainmaker import User
from chainmaker.chain_client import ChainClientWithEndorsers
from chainmaker.keys import (AddrType, ChainConfigMethod, ContractManageMethod, ContractStatus, ParamKey,
                             RechargeGasItem, ResourceName, Role, Rule, RuntimeType, SystemContractName, TxStage,
                             TxType)
from chainmaker.protos.common.request_pb2 import Payload

from chainmaker.sdk_config import DefaultConfig
from chainmaker.utils import (address_utils, cmc_utils, common, crypto_config_utils, crypto_utils, file_utils,
                              result_utils, server_utils)
from chainmaker.utils.common import ensure_enum
from chainmaker.utils.file_utils import load_byte_code


def with_user_endorsers(method):
    @functools.wraps(method)
    def _method(self, *args, **kwargs):
        user = kwargs.pop('user') if 'user' in kwargs else None
        endorsers = kwargs.pop('endorsers') if 'endorsers' in kwargs else None
        endorsers_cnt = kwargs.pop('endorsers_cnt') if 'endorsers_cnt' in kwargs else None
        conn_node = kwargs.pop('conn_node') if 'conn_node' in kwargs else None
        alias = kwargs.pop('alias') if 'alias' in kwargs else None
        enable_cert_hash = kwargs.pop('enable_cert_hash') if 'enable_cert_hash' in kwargs else None
        payer = kwargs.pop('payer') if 'payer' in kwargs else None

        if user:
            chain_id = self._cc.chain_id
            cc = self._crypto_config.new_chain_client(user, endorsers=endorsers, endorsers_cnt=endorsers_cnt,
                                                      conn_node=conn_node, alias=alias,
                                                      enable_cert_hash=enable_cert_hash, chain_id=chain_id)
            if payer:
                cc.payer = self._crypto_config.get_user(payer)

            if hasattr(self, '_logger'):
                setattr(cc, '_logger', getattr(self, '_logger'))

            self._origin_cc, self._cc = self._cc, cc
            try:
                res = method(self, *args, **kwargs)
                if isinstance(res, Payload):
                    return res
                self._debug(f'执行结果 {res}')
                return result_utils.msg_to_dict(res)
            except Exception as ex:
                # self._debug(f'抛出异常 {ex}')
                self._exception(ex)
                return str(ex)
            finally:
                self._cc = self._origin_cc
                cc.stop()
                delattr(self, '_origin_cc')
        else:
            try:
                res = method(self, *args, **kwargs)
                if isinstance(res, Payload):
                    return res
                self._debug(f'执行结果 {res}')
                return result_utils.msg_to_dict(res)
            except Exception as ex:
                # self._debug(f'抛出异常 {ex}')
                self._exception(ex)
                return str(ex)

    return _method


class BaseOps:
    def __init__(self, cc: ChainClientWithEndorsers, crypto_config: crypto_config_utils.CryptoConfig = None):
        self._crypto_config = crypto_config
        self._cc = cc or self._crypto_config.new_chain_client()

    def _get_client(self, user: str = None, endorsers: List[str] = None, endorsers_cnt: int = None,
                    conn_node: Union[str, int] = None, alias: str = None, enable_cert_hash: bool = False,
                    chain_id=DefaultConfig.chain_id):
        if user:
            return self._crypto_config.new_chain_client(user, endorsers, endorsers_cnt, conn_node, alias,
                                                        enable_cert_hash, chain_id=chain_id)
        return self._cc

    def _debug(self, msg: str):
        self._cc._debug(msg)

    def _info(self, msg: str):
        self._cc._info(msg)

    def _warn(self, msg: str):
        self._cc._warn(msg)

    def _exception(self, msg: str):
        self._cc._exception(msg)

    def _error(self, msg: str):
        self._cc._error(msg)

    def _critical(self, msg: str):
        self._cc._critical(msg)


# 00
class ChainConfigOps(BaseOps):
    """带背书链客户端"""

    @property
    def version(self):
        return self._cc.chain_config.version

    @property
    def block(self):
        return self._cc.chain_config.block

    @property
    def core(self):
        return self._cc.chain_config.core

    @property
    def consensus(self):
        return self._cc.chain_config.consensus

    @property
    def trust_roots(self):
        return self._cc.chain_config.trust_roots

    @property
    def trust_members(self):
        return self._cc.chain_config.trust_members

    @property
    def vm(self):
        return self._cc.chain_config.vm

    @property
    def account_config(self):
        return self._cc.chain_config.account_config

    @property
    def resource_policies(self):
        return self._cc.chain_config.resource_policies

    @property
    def contract(self):
        return self._cc.chain_config.contract

    # =========================  带背书链配置信任组织根证书操作 =========================
    # 00-00 获取链配置
    @with_user_endorsers
    def get_chain_config(self) -> dict:
        """
        获取链配置
        <00-00-CHAIN_CONFIG-GET_CHAIN_CONFIG>
        :return: ChainConfig
        :raises RequestError: 请求失败
        """
        self._info('获取链配置')
        return self._cc.chain_config

    @with_user_endorsers
    def get_enable_gas_status(self) -> bool:
        return self._cc.enable_alias()

    @with_user_endorsers
    def get_default_gas(self) -> int:
        return self._cc.default_gas

    @with_user_endorsers
    def get_addr_type(self) -> AddrType:
        return self._cc.addr_type

    @with_user_endorsers
    def get_resource_policies(self):
        return self._cc.chain_config.resource_policies

    @with_user_endorsers
    def get_block_config(self, key: str) -> Any:
        """获取区块指定配置"""
        self._info(f'获取区块 {key} 配置 ')
        return getattr(self._cc.chain_config.block, key)

    @with_user_endorsers
    def get_core_config(self, key: str) -> Any:
        """获取Core指定配置"""
        self._info(f'获取Core {key} 配置 ')
        return getattr(self._cc.chain_config.core, key)

    # 00-01 通过指定区块高度查询最近链配置
    @with_user_endorsers
    def get_chain_config_by_block_height(self, block_height: int) -> dict:
        """
        通过指定区块高度查询最近链配置
        如果当前区块就是配置块，直接返回当前区块的链配置
        <00-01-CHAIN_CONFIG-GET_CHAIN_CONFIG_AT>
        :param block_height: 块高
        :return: ChainConfig
        :raises RequestError: 请求失败
        """
        self._info(f'通过指定区块高度 {block_height} 查询最近链配置')
        return self._cc.get_chain_config_by_block_height(block_height)

    # 00-02 更新链配置Core配置
    @with_user_endorsers
    def core_update(self, tx_scheduler_timeout: int = None, tx_scheduler_validate_timeout: int = None,
                    timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        更新链配置Core配置
        <00-02-CHAIN_CONFIG-CORE_UPDATE>
        :param tx_scheduler_timeout: 交易调度器从交易池拿到交易后, 进行调度的时间，其值范围为[0, 60]，若无需修改，请置为-1
        :param tx_scheduler_validate_timeout: 交易调度器从区块中拿到交易后, 进行验证的超时时间，其值范围为[0, 60]，若无需修改，请置为-1
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错

        默认配置为：
        tx_scheduler_timeout: 10
        tx_scheduler_validate_timeout: 10
        consensus_turbo_config {}
        enable_conflicts_bit_window: true
        """
        _msg = '更新链配置Core配置'
        if tx_scheduler_timeout:
            _msg += f' tx_scheduler_timeout: {self.core.tx_scheduler_timeout}->{tx_scheduler_timeout}'
        if tx_scheduler_validate_timeout:
            _msg += f' tx_scheduler_validate_timeout: {self.core.tx_scheduler_validate_timeout}->' \
                    f'{tx_scheduler_validate_timeout}'
        self._info(_msg)

        payload = self._cc.create_chain_config_core_update_payload(tx_scheduler_timeout, tx_scheduler_validate_timeout)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-03 更新链配置区块配置
    @with_user_endorsers
    def block_update(self, tx_timestamp_verify: bool = None, tx_timeout: int = None,
                     block_tx_capacity: int = None,
                     block_size: int = None, block_interval: int = None, tx_parameter_size: int = None,
                     timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        更新链配置区块配置
        <00-03-CHAIN_CONFIG-BLOCK_UPDATE>
        :param tx_timestamp_verify: 是否需要开启交易时间戳校验
        :param tx_timeout: 交易时间戳的过期时间(秒)，其值范围为[600, +∞)（若无需修改，请置为-1）
        :param block_tx_capacity: 区块中最大交易数，其值范围为(0, +∞]（若无需修改，请置为-1）
        :param block_size: 区块最大限制，单位MB，其值范围为(0, +∞]（若无需修改，请置为-1）
        :param block_interval: 出块间隔，单位:ms，其值范围为[10, +∞]（若无需修改，请置为-1）
        :param tx_parameter_size: 交易参数大小
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错

        默认配置为：
        tx_timestamp_verify: true
        tx_timeout: 600
        block_tx_capacity: 100
        block_size: 10
        block_interval: 10
        """
        _msg = '更新链配置区块配置'
        if tx_timestamp_verify:
            _msg += f' tx_timestamp_verify: {self.block.tx_timestamp_verify}->{tx_timestamp_verify}'
        if tx_timeout:
            _msg += f' tx_timeout: {self.block.tx_timeout}->{tx_timeout}'
        if block_tx_capacity:
            _msg += f' block_tx_capacity: {self.block.block_tx_capacity}->{block_tx_capacity}'
        if block_size:
            _msg += f' block_size: {self.block.block_size}->{block_size}'
        if block_interval:
            _msg += f' block_interval: {self.block.block_interval}->{block_interval}'
        if tx_parameter_size:
            _msg += f' tx_parameter_size: {self.block.tx_parameter_size}->{tx_parameter_size}'

        self._info(_msg)
        payload = self._cc.create_chain_config_block_update_payload(tx_timestamp_verify, tx_timeout, block_tx_capacity,
                                                                    block_size, block_interval, tx_parameter_size)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    @with_user_endorsers
    def trust_root_check(self, org_id: str, trust_root_crts: List[str] = None):
        """
        检查信任组织根证书是否上链
        :param org_id: 组织Id
        :param trust_root_crts: 信任根证书列表
        :return:
        """
        self._info('检查信任组织根证书是否上链')
        trust_roots = self._cc.chain_config.trust_roots

        trust_root_orgs = [item.org_id for item in trust_roots]
        if org_id in trust_root_orgs:
            trust_root_certs = []
            for item in trust_roots:
                trust_root_certs.extend(item.root)
            if trust_root_crts in trust_root_certs:
                return True
        return False

    # 00-04 添加信任组织根证书
    @with_user_endorsers
    def trust_root_add(self, org_id: str, trust_root_crts: List[str],
                       timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        添加信任组织根证书
        <00-04-CHAIN_CONFIG-TRUST_ROOT_ADD>
        :param str org_id: 组织Id
        :param trust_root_crts: 根证书列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info("添加信任组织根证书")
        payload = self._cc.create_chain_config_trust_root_add_payload(org_id, trust_root_crts)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-05 更新信任组织根证书
    @with_user_endorsers
    def trust_root_update(self, org_id: str, trust_root_crts: List[str],
                          timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        更新信任组织根证书
        <00-05-CHAIN_CONFIG-TRUST_ROOT_UPDATE>
        :param str org_id: 组织Id
        :param trust_root_crts: 根证书列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"更新信任组织根证书 org_id: {org_id} trust_root_crts: {trust_root_crts}")
        payload = self._cc.create_chain_config_trust_root_update_payload(org_id, trust_root_crts)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-06 删除信任组织根证书
    @with_user_endorsers
    def trust_root_delete(self, org_id: str,
                          timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        删除信任组织根证书
        <00-06-CHAIN_CONFIG-TRUST_ROOT_DELETE>
        :param str org_id: 组织Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"删除信任组织根证书 org_id: {org_id}")
        payload = self._cc.create_chain_config_trust_root_delete_payload(org_id)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-07 添加共识节点地址
    @with_user_endorsers
    def node_addr_add(self, org_id: str, node_addrs: List[str], timeout: int = None,
                      with_sync_result: bool = None) -> dict:
        """
        添加节点地址
        <00-07-CHAIN_CONFIG-NODE_ADDR_ADD>
        :param org_id: 节点组织Id
        :param node_addrs: 节点地址列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"添加共识节点地址 org_id: {org_id}")
        payload = self._cc.create_chain_config_node_addr_add_payload(org_id, node_addrs)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-08 更新共识节点地址
    @with_user_endorsers
    def node_addr_update(self, org_id: str, node_old_addr: str, node_new_addr: str,
                         timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        更新节点地址
        <00-08-CHAIN_CONFIG-NODE_ADDR_UPDATE>
        :param org_id: 节点组织Id
        :param node_old_addr: 原节点地址
        :param node_new_addr: 新节点地址
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"更新共识节点地址 org_id: {org_id}")
        payload = self._cc.create_chain_config_node_addr_update_payload(org_id, node_old_addr, node_new_addr)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-09 删除共识节点地址
    @with_user_endorsers
    def node_addr_delete(self, org_id: str, node_addr: str,
                         timeout: int = None, with_sync_result: bool = None):
        """
        删除节点地址
        <00-09-CHAIN_CONFIG-NODE_ADDR_DELETE>
        :param org_id: 节点组织Id
        :param node_addr: 节点地址
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"删除共识节点地址 org_id: {org_id}")
        payload = self._cc.create_chain_config_node_addr_delete_payload(org_id, node_addr)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    @with_user_endorsers
    def node_org_check(self, org_id: str) -> bool:
        self._info(f"检查共识节点组织 org_id: {org_id}")
        consensus_nodes = self._cc.chain_config.consensus.nodes
        consensus_orgs = [item.org_id for item in consensus_nodes]
        return org_id in consensus_orgs

    # 00-10 添加共识节点组织
    @with_user_endorsers
    def node_org_add(self, org_id: str, node_ids: List[str],
                     timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        添加共识节点组织
        :param org_id: 节点组织Id
        :param node_ids: 节点Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"添加共识节点组织 org_id: {org_id} node_ids: {node_ids}")
        payload = self._cc.create_chain_config_consensus_node_org_add_payload(org_id, node_ids)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-11 更新共识节点组织
    @with_user_endorsers
    def node_org_update(self, org_id: str, node_ids: List[str],
                        timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        更新共识节点组织
        :param org_id: 节点组织Id
        :param node_ids: 节点Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 添加共识、更新共识组织的交易响应或None
        :raises RequestError: 请求出错
        """
        self._info(f"更新共识节点组织 org_id: {org_id} node_ids: {node_ids}")
        self._info('begin to switch_branch consensus org')
        payload = self._cc.create_chain_config_consensus_node_org_update_payload(org_id, node_ids)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-12 删除共识节点组织
    @with_user_endorsers
    def node_org_delete(self, org_id: str,
                        timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        删除共识节点组织
        :param org_id: 节点组织Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"删除共识节点组织 org_id: {org_id}")
        payload = self._cc.create_chain_config_consensus_node_org_delete_payload(org_id)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    @with_user_endorsers
    def consensus_ext_check(self, key: str, value: str = None) -> bool:
        """检查共识扩展key是否存在及key-value是否相同"""
        self._info(f"检查共识扩展参数 {key}")
        ext_config = self._cc.get_chain_config().consensus.ext_config
        consensus_ext = {item.key: item.value for item in ext_config}
        if value is None:
            return consensus_ext.get(key) is not None
        return consensus_ext.get(key) == value

    # 00-13 添加共识扩展参数
    @with_user_endorsers
    def consensus_ext_add(self, params: dict,
                          timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        添加共识扩展参数
        :param params: 字段key、value对
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"添加共识扩展参数 {params}")
        payload = self._cc.create_chain_config_consensus_ext_add_payload(params)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-14 更新共识扩展参数
    @with_user_endorsers
    def consensus_ext_update(self, params: dict, timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        更新共识扩展参数
        :param dict params: 字段key、value对
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"更新共识扩展参数 {params}")
        payload = self._cc.create_chain_config_consensus_ext_update_payload(params)

        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-15 删除共识扩展参数
    @with_user_endorsers
    def consensus_ext_delete(self, keys: List[str], timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        删除共识扩展参数
        :param keys: 待删除字段
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"删除共识扩展参数 {keys}")
        payload = self._cc.create_chain_config_consensus_ext_delete_payload(keys)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    @with_user_endorsers
    def permission_check(self, permission_resource_name: Union[ResourceName, str]) -> bool:
        """
        检查权限是否存在
        :param permission_resource_name:
        :return:
        """
        self._info(f"检查权限是否存在 {permission_resource_name}")
        permission_resource_names = [item.resource_name for item in self._cc.chain_config.resource_policies]
        return permission_resource_name in permission_resource_names

    # 00-16 添加权限配置
    @with_user_endorsers
    def permission_add(self, permission_resource_name: Union[ResourceName, str], rule: Union[Rule, str],
                       role_list: List[Role] = None, org_list: List[str] = None,
                       timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        添加权限配置
        :param permission_resource_name: 权限名
        :param rule: 权限规则
        :param org_list: 权限适用组织列表
        :param role_list: 权限适用角色列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        if org_list:
            self._info(f"添加权限配置 {permission_resource_name}-{rule}-{role_list or '[]'}-{org_list or '[]'}")
        else:
            self._info(f"添加权限配置 {permission_resource_name}-{rule}-{role_list or '[]'}")
        policy = self._cc.create_policy(rule, role_list=role_list, org_list=org_list)
        payload = self._cc.create_chain_config_permission_add_payload(permission_resource_name, policy)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-17 更新权限配置
    @with_user_endorsers
    def permission_update(self, permission_resource_name: Union[ResourceName, str], rule: Union[Rule, str],
                          role_list: List[Role] = None, org_list: List[str] = None,
                          timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        更新权限配置
        :param str permission_resource_name: 权限名
        :param rule: 权限规则
        :param org_list: 权限适用组织列表
        :param role_list: 权限适用角色列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        if org_list:
            self._info(f"更新权限配置 {permission_resource_name}-{rule}-{role_list}-{org_list}")
        else:
            self._info(f"更新权限配置 {permission_resource_name}-{rule}-{role_list}")
        policy = self._cc.create_policy(rule, role_list=role_list, org_list=org_list)
        payload = self._cc.create_chain_config_permission_update_payload(permission_resource_name, policy)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def permission_add_or_update(self, permission_resource_name: Union[ResourceName, str], rule: Union[Rule, str],
                                 role_list: List[Role] = None, org_list: List[str] = None,
                                 timeout: int = None, with_sync_result: bool = None) -> dict:
        if self.permission_check(permission_resource_name):
            return self.permission_update(permission_resource_name, rule, role_list, org_list, timeout,
                                          with_sync_result)
        return self.permission_add(permission_resource_name, rule, role_list, org_list, timeout, with_sync_result)

    # 00-18 删除权限配置
    @with_user_endorsers
    def permission_delete(self, permission_resource_name: Union[ResourceName, str],
                          timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        删除权限配置
        :param str permission_resource_name: 权限名
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"删除权限配置 {permission_resource_name}")
        payload = self._cc.create_chain_config_permission_delete_payload(permission_resource_name)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    @with_user_endorsers
    def node_id_check(self, org_id: str, node_id: str) -> bool:
        """
        检查共识节点Id
        :param org_id:
        :param node_id:
        :return:
        """
        self._info(f"检查共识节点Id org_id: {org_id} node_id: {node_id}")
        consensus_nodes = self._cc.chain_config.consensus.nodes
        for item in consensus_nodes:
            if org_id == item.org_id and node_id in item.node_id:
                return True
        return False

    # 00-19 添加共识节点Id
    @with_user_endorsers
    def node_id_add(self, org_id: str, node_ids: List[str],
                    timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        添加共识节点Id
        :param str org_id: 节点组织Id
        :param node_ids: 节点Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info("添加共识节点Id")
        payload = self._cc.create_chain_config_consensus_node_id_add_payload(org_id, node_ids)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-20 更新共识节点Id
    @with_user_endorsers
    def node_id_update(self, org_id: str, node_old_id: str, node_new_id: str,
                       timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        更新共识节点Id
        :param str org_id: 节点组织Id
        :param node_old_id: 节点原Id
        :param node_new_id: 节点新Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"更新共识节点Id org_id: {org_id} node_id: {node_old_id}->{node_new_id}")
        payload = self._cc.create_chain_config_consensus_node_id_update_payload(org_id, node_old_id, node_new_id)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-21 删除共识节点Id
    @with_user_endorsers
    def node_id_delete(self, org_id: str, node_id: str,
                       timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        删除共识节点Id
        :param str org_id: 节点组织Id
        :param node_id: 节点Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"删除共识节点Id org_id: {org_id} node_id: {node_id}")
        payload = self._cc.create_chain_config_consensus_node_id_delete_payload(org_id, node_id)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    @with_user_endorsers
    def trust_member_check(self, org_id: str, trust_member_info: str = None) -> bool:
        """
        检查信任第三方组织是否上链
        :param org_id: 组织Id
        :param trust_member_info: 信任第三方根证书
        :return: 已上链返回True，否则返回False
        """
        self._info(f"检查信任第三方组织 org_id: {org_id} trust_member_info: {trust_member_info}")
        trust_members = self._cc.chain_config.trust_members
        trust_member_org_ids = [item.org_id for item in trust_members]
        if org_id in trust_member_org_ids:
            trust_member_infos = [item.member_info for item in trust_members]
            if trust_member_info in trust_member_infos:
                return True
        return False

    # 00-22 添加信任第三方组织
    @with_user_endorsers
    def trust_member_add(self, org_id: str, trust_member_node_id: str, trust_member_info: str,
                         trust_member_role: Union[Role, str],
                         timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        添加信任第三方组织
        :param org_id: 组织Id
        :param trust_member_node_id: 节点ID
        :param trust_member_info: 节点信息
        :param trust_member_role: 节点角色
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"添加信任第三方组织 org_id: {org_id} trust_member_role: {trust_member_role}")
        payload = self._cc.create_chain_config_trust_member_add_payload(org_id, trust_member_node_id, trust_member_info,
                                                                        trust_member_role)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-23 更新信任第三方组织
    @with_user_endorsers
    def trust_member_update(self, trust_member_org_id: str, trust_member_node_id: str, trust_member_info: str,
                            trust_member_role: Union[Role, str],
                            timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        更新信任第三方组织
        :param trust_member_org_id: 组织Id
        :param trust_member_node_id: 节点ID
        :param trust_member_info: 节点信息
        :param trust_member_role: 节点角色
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"更新信任第三方组织 org_id: {trust_member_org_id} trust_member_role: {trust_member_role}")
        payload = self._cc.create_chain_config_trust_member_update_payload(trust_member_org_id, trust_member_node_id,
                                                                           trust_member_info, trust_member_role)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-24 删除信任第三方组织
    @with_user_endorsers
    def trust_member_delete(self, trust_member_info: str,
                            timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        删除信任第三方组织
        :param trust_member_info: 节点证书信息
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._info(f"删除信任第三方组织 {trust_member_info}")
        payload = self._cc.create_chain_config_trust_member_delete_payload(trust_member_info)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-25 变更地址类型
    @with_user_endorsers
    def alter_addr_type(self, addr_type: Union[AddrType, str, int],
                        timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        创建链配置变更地址类型待签名Payload
        <00-25-CHAIN_CONFIG-ALTER_ADDR_TYPE>
        :param addr_type: 地址类型
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        addr_type = result_utils.ensure_enum(addr_type, AddrType)
        current_addr_type = self._cc.addr_type
        self._info(f"变更地址类型 {current_addr_type}->{addr_type}")
        payload = self._cc.create_chain_config_alter_addr_type_payload(addr_type)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout,
                                                          with_sync_result=with_sync_result)

    # 00-26 启用或禁用Gas
    @with_user_endorsers
    def enable_or_disable_gas(self, enable_gas: bool = None,
                              timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        启用或禁用Gas
        :param enable_gas: 是否启用Gas, 为None时直接切换
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        if enable_gas is None or (enable_gas is not self._cc.enabled_gas):
            if enable_gas is None:
                self._info("启用或禁用Gas")
            elif enable_gas is False:
                self._info("禁用Gas")
            else:
                self._info("启用Gas")
            payload = self._cc.create_chain_config_enable_or_disable_gas_payload()
            return self._cc._send_chain_config_update_request(payload, timeout=timeout,
                                                              with_sync_result=with_sync_result)

    @with_user_endorsers
    def enable_gas(self) -> dict:
        """启用Gas"""
        return self.enable_or_disable_gas(True)

    @with_user_endorsers
    def disable_gas(self) -> dict:
        """
        禁用Gas
        :return:
        """
        return self.enable_or_disable_gas(False)

    # 00-27 设置合约调用基础Gas消耗
    @with_user_endorsers
    def set_invoke_base_gas(self, amount: int, timeout: int = None, with_sync_result: bool = None):
        """
        设置合约调用基础Gas消耗
        :param amount: 设置待基础Gas消耗数量
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        self._info(f"设置合约调用基础Gas消耗 {amount}")
        params = {ParamKey.set_invoke_base_gas.name: amount}
        payload = self._cc._create_chain_config_manage_payload(ChainConfigMethod.SET_INVOKE_BASE_GAS.name,
                                                               params)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-28 设置Gas管理员地址
    @with_user_endorsers
    def set_account_manager_admin(self, address: str = None, timeout: int = None,
                                  with_sync_result: bool = None) -> dict:
        """
        设置Gas管理员地址
        :param address: 用户地址-为None时为当前用户地址
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        if address is None:
            address = self._cc.address
        self._info(f"设置Gas管理员地址 {address}")

        payload = self._cc.create_chain_config_set_account_manager_admin_payload(address)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def set_gas_admin(self, address: str = None, timeout: int = None,
                      with_sync_result: bool = None) -> dict:
        """
        设置Gas管理员地址
        :param address: 用户地址-为None时为当前用户地址
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        return self.set_account_manager_admin(address, timeout, with_sync_result)

    def optimize_charge_gas(self, enable: bool = True) -> dict:
        """
        开启或关闭链配置Gas优化
        :param enable: 是否启用
        :return: 待签名Payload
        """
        if enable is True:
            self._info("启用Gas优化")
        else:
            self._info("关闭Gas优化")
        return self._cc.chain_config_optimize_charge_gas(enable)

    def enable_multi_sign_manual_run(self) -> dict:
        """启用多签手动运行"""
        self._info('启用多签手动运行')
        return self._cc.chain_config_enable_multi_sign_manual_run(enable=True)

    def disable_multi_sign_manual_run(self) -> dict:
        """启用多签手动运行"""
        self._info('禁用多签手动运行')
        return self._cc.chain_config_enable_multi_sign_manual_run(enable=False)

    def check_multi_sign_manual_run(self) -> bool:
        """启用多签手动运行"""
        self._info('检查是否多签手动运行')
        return self._cc.get_chain_config().vm.native.multisign.enable_manual_run

    def enable_optimize_charge_gas(self):
        """开启链配置Gas优化"""
        return self.optimize_charge_gas(True)

    def disable_optimize_charge_gas(self):
        """关闭链配置Gas优化"""
        return self.optimize_charge_gas(False)

    def check_optimize_charge_gas(self) -> bool:
        """检查是否开启了Gas优化"""
        self._info('检查是否开启了Gas优化')
        return self._cc.get_chain_config().core.enable_optimize_charge_gas

    # 00-29 获取链配置权限列表
    @with_user_endorsers
    def get_permission_list(self) -> dict:
        """
        获取链配置权限列表
        <00-29-CHAIN_CONFIG-PERMISSION_LIST>
        :return: 权限列表
        """
        self._info("获取链配置权限列表")
        return self._cc.get_chain_config_permission_list()

    # 00-32 更新DPos共识节点Id
    @with_user_endorsers
    def dpos_node_id_update(self, node_ids: List[str],
                            timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        更新DPos共识节点Id
        :param node_ids: 节点Id列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._info(f"更新DPos共识节点Id {node_ids}")
        payload = self._cc.create_chain_config_dpos_node_id_update_payload(node_ids)
        return self._cc._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    @with_user_endorsers
    def _send_chain_config_update_request(self, payload: Payload,
                                          timeout: int = None,
                                          with_sync_result: bool = None) -> dict:
        """
        发送链配置更新请求
        :param payload: 待签名链配置更新请求Payload
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮交易结果
        :return: 交易响应信息
        """
        response = self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        # 更新缓存的chain_config
        setattr(self, '_cached_chain_config', None)
        return response


# 01
class ChainQueryOps(BaseOps):
    # ========================== 链查询操作 ==================================

    # 01-00 通过交易Id获取交易所在区块信息
    @with_user_endorsers
    def get_block_by_tx_id(self, tx_id: str, with_rw_set: bool = False) -> dict:
        """
        通过交易Id获取交易所在区块信息
        <01-00-CHAIN_QUERY-GET_BLOCK_BY_TX_ID>
        :param tx_id: 交易Id
        :param with_rw_set: 是否返回读写集数据
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        self._info(f"通过交易Id {tx_id} 获取交易所在区块信息")
        return self._cc.get_block_by_tx_id(tx_id, with_rw_set)

    # 01-01 通过交易Id获取交易信息
    @with_user_endorsers
    def get_tx_by_tx_id(self, tx_id: str) -> dict:
        """
        通过交易Id获取交易信息
        <01-01-CHAIN_QUERY-GET_TX_BY_TX_ID>
        :param tx_id: 交易Id，类型为字符串
        :return: Result
        :raises RequestError: 请求失败
        """
        self._info(f"通过交易Id {tx_id} 获取交易信息")
        return self._cc.get_tx_by_tx_id(tx_id)

    # 01-02 通过区块高度获取区块信息
    @with_user_endorsers
    def get_block_by_height(self, block_height: int, with_rw_set: bool = False) -> dict:
        """
        通过区块高度获取区块信息
        <01-02-CHAIN_QUERY-GET_BLOCK_BY_HEIGHT>
        :param block_height: 区块高度
        :param with_rw_set: 是否返回读写集数据, 默认不返回。
        :return: 区块信息BlockInfo对象
        :raises RequestError: 请求失败，块已归档是抛出ContractFile
        """

        if with_rw_set:
            self._info(f"通过区块高度 {block_height} 获取带读写集区块信息")
            return self._cc.get_block_with_txrwsets_by_height(block_height)
        self._info(f"通过区块高度 {block_height} 获取区块信息")
        return self._cc.get_block_by_height(block_height)

    # 01-03 获取链信息
    @with_user_endorsers
    def get_chain_info(self) -> dict:
        """
        获取链信息
        <01-03-CHAIN_QUERY-GET_CHAIN_INFO>
        :return: ChainInfo
        :raises RequestError: 请求失败
        """
        self._info("获取链信息")
        return self._cc.get_chain_info()

    # 01-04 获取最新的配置块
    @with_user_endorsers
    def get_last_config_block(self, with_rw_set: bool = False) -> dict:
        """
        获取最新配置块
        <01-04-CHAIN_QUERY-GET_LAST_CONFIG_BLOCK>
        :param with_rw_set: 是否返回读写集数据
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        self._info("获取最新配置块")
        return self._cc.get_last_config_block(with_rw_set)

    # 01-05 通过区块哈希获取区块信息
    @with_user_endorsers
    def get_block_by_hash(self, block_hash: str, with_rw_set: bool = False) -> dict:
        """
        通过区块哈希获取区块信息
        <01-05-CHAIN_QUERY-GET_BLOCK_BY_HASH>
        :param block_hash: 区块Hash, 二进制hash.hex()值，
                           如果拿到的block_hash字符串是base64值, 需要用 base64.b64decode(block_hash).hex()
        :param with_rw_set: 是否返回读写集数据
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        if with_rw_set:
            self._info(f"通过区块哈希 {block_hash} 获取带读写集区块信息")
            return self._cc.get_block_with_txrwsets_by_hash(block_hash)
        self._info(f"通过区块哈希 {block_hash} 获取区块信息")
        return self._cc.get_block_by_hash(block_hash)

    # 01-06 获取节点加入的链列表
    @with_user_endorsers
    def get_node_chain_list(self) -> dict:
        """
        获取节点加入的链列表
        <01-06-CHAIN_QUERY-GET_NODE_CHAIN_LIST>
        :return: 链Id列表
        :raises RequestError: 请求失败
        """
        self._info("获取节点加入的链列表")
        return self._cc.get_node_chain_list()

    # 01-07 获取统治合约
    @with_user_endorsers
    def get_governance_contract(self):
        """
        获取统治合约
        <01-07-CHAIN_QUERY-GET_GOVERNANCE_CONTRACT>
        :return:
        """
        self._info("获取统治合约")
        return self._cc.get_governance_contract()

    # 01-08 通过区块高度获取带读写集区块信息
    @with_user_endorsers
    def get_block_with_txrwsets_by_height(self, block_height: int) -> dict:
        """
        通过区块高度获取带读写集区块信息
        <01-08-CHAIN_QUERY-GET_BLOCK_WITH_TXRWSETS_BY_HEIGHT>
        :param block_height: 区块高度
        :return: 带读写集区块信息
        """
        self._info(f"通过区块高度 {block_height} 获取带读写集区块信息")
        return self._cc.get_block_with_txrwsets_by_height(block_height)

    # 01-09 通过区块哈希获取带读写集区块信息
    @with_user_endorsers
    def get_block_with_txrwsets_by_hash(self, block_hash: str) -> dict:
        """
        通过区块哈希获取带读写集区块信息
         <01-09-CHAIN_QUERY-GET_BLOCK_WITH_TXRWSETS_BY_HASH>
        :param block_hash: 区块哈希
        :return: 带读写集区块信息
        """
        self._info(f"通过区块哈希 {block_hash} 获取带读写集区块信息")
        return self._cc.get_block_with_txrwsets_by_hash(block_hash)

    # 01-10 获取最新区块信息
    @with_user_endorsers
    def get_last_block(self, with_rw_set: bool = False) -> dict:
        """
        获取最新区块信息
        <01-10-CHAIN_QUERY-GET_LAST_BLOCK>
        :param with_rw_set: 是否返回读写集数据
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        self._info("获取最新区块信息")
        return self._cc.get_last_block(with_rw_set)

    # 01-11 通过区块高度获取完整区块信息
    @with_user_endorsers
    def get_full_block_by_height(self, block_height: int) -> dict:
        """
        通过区块高度获取完整区块信息
        <01-11-CHAIN_QUERY-GET_FULL_BLOCK_BY_HEIGHT>
        :param block_height: 区块高度
        :return: BlockInfo
        :raises RequestError: 请求失败
        """
        self._info(f"通过区块高度 {block_height} 获取完整区块信息")
        return self._cc.get_full_block_by_height(block_height)

    # 01-12 通过交易Id获取区块高度
    @with_user_endorsers
    def get_block_height_by_tx_id(self, tx_id: str) -> int:
        """
        通过交易Id获取区块高度
        <01-12-CHAIN_QUERY-GET_BLOCK_HEIGHT_BY_TX_ID>
        :param tx_id: 交易Id
        :return: 区块高度
        :raises RequestError: 请求失败
        """
        self._info(f"通过交易Id {tx_id} 获取区块高度")
        return self._cc.get_block_height_by_tx_id(tx_id)

    # 01-13 通过区块哈希获取区块高度
    @with_user_endorsers
    def get_block_height_by_hash(self, block_hash: str) -> int:
        """
        通过区块哈希获取区块高度
        <01-13-CHAIN_QUERY-GET_BLOCK_HEIGHT_BY_HASH>
        :param block_hash: 区块Hash 二进制hash.hex()值,
               如果拿到的block_hash字符串是base64值, 需要用 base64.b64decode(block_hash).hex()
        :return: 区块高度
        :raises RequestError: 请求失败
        """
        self._info(f"通过区块哈希 {block_hash} 获取区块高度")
        return self._cc.get_block_height_by_hash(block_hash)

    # 01-14 通过高度获取区块头
    @with_user_endorsers
    def get_block_header_by_height(self, block_height: int) -> dict:
        """
        通过高度获取区块头
        <01-14-CHAIN_QUERY-GET_BLOCK_HEADER_BY_HEIGHT>
        :param block_height: 区块高度
        :return: 区块头
        """
        self._info(f"通过高度 {block_height} 获取区块头")
        return self._cc.get_block_header_by_height(block_height)

    # 01-15 获取已归档的区块高度
    @with_user_endorsers
    def get_archived_block_height(self) -> int:
        """
        获取已归档的区块高度
         <01-15-CHAIN_QUERY-GET_ARCHIVED_BLOCK_HEIGHT>
        :return: 区块高度
        :raises RequestError: 请求失败
        """
        self._info("获取已归档的区块高度")
        return self._cc.get_archived_block_height()

    # 01-16 获取全部合约信息
    # @with_user_endorsers
    # def get_all_contracts(self) -> List[Contract]:
    #     """
    #     获取全部合约列表
    #     <01-16-CHAIN_QUERY-GET_ALL_CONTRACTS>
    #     :return: 合约Contract对象列表
    #     :raise: RequestError: 请求出错
    #     :raise: AssertionError: 响应code不为0,检查响应时抛出断言失败
    #     :raise: 当数据不是JSON格式时，抛出json.decoder.JSONDecodeError
    #     """
    #     self._info("获取全部合约列表")
    #     return self._cc.get_all_contracts()

    # 01-17 查询交易存在性证明
    @with_user_endorsers
    def get_merkle_path_by_tx_id(self, tx_id: str) -> bool:
        """
        查询交易存在性证明
        <01-17-CHAIN_QUERY-GET_MERKLE_PATH_BY_TX_ID>
        :param tx_id: 交易Id
        :return: Merkle树路径
        """
        self._info(f"通过交易Id {tx_id} 获取Merkle树路径")
        return self._cc.get_merkle_path_by_tx_id(tx_id)

    @with_user_endorsers
    def get_current_block_height(self) -> int:
        """
        获取当前区块高度
        :return: 区块高度
        """
        self._info('获取当前区块高度')
        return self._cc.get_current_block_height()

    @with_user_endorsers
    def get_block_height(self, tx_id: str = None, block_hash: str = None) -> int:
        """
        通过交易Id或区块hash获取区块高度
        :param tx_id: 交易Id
        :param block_hash: 区块hash
        :return: 区块高度
        """
        if tx_id:
            self._info(f'通过交易Id {tx_id} 获取当前区块高度')
        if block_hash:
            self._info(f'通过区块哈希 {block_hash} 获取当前区块高度')
        return self._cc.get_block_height(tx_id, block_hash)

    @with_user_endorsers
    def get_chainmaker_server_version(self) -> str:
        """获取chainmaker服务版本号"""
        self._info(f'获取chainmaker服务版本号')
        return self._cc.get_chainmaker_server_version()

    # 补充查询api
    def get_block_timestamp_by_height(self, block_height: int = None) -> int:
        """
        通过区块高度获取区块时间戳
        :param block_height: 区块高度
        :return: 区块时间戳
        """
        self._info(f'通过区块高度 {block_height} 获取区块时间戳')
        if block_height is None:
            block_height = self._cc.get_current_block_height()
        return self._cc.get_block_header_by_height(block_height).block_timestamp

    def get_block_hash_by_height(self, block_height: int) -> str:
        """
        通过区块高度查询区块哈希
        :param block_height: 区块高度
        :return: 区块哈希
        """
        self._info(f'通过区块高度 {block_height} 查询区块哈希')
        block_info = self._cc.get_block_by_height(block_height)
        return block_info.block.header.block_hash.hex()

    def get_last_block_hash(self) -> str:
        """
        获取最新区块哈希
        :return: 最新区块哈希
        """
        self._info('获取最新区块哈希')
        block_info = self._cc.get_last_block()
        return block_info.block.header.block_hash.hex()

    def get_last_block_tx_ids(self) -> List[str]:
        """
        获取最新区块交易Id列表
        :return: 交易Id列表
        """
        self._info('获取最新区块交易Id列表')
        block_info = self._cc.get_last_block()
        txs = block_info.block.txs
        return [tx.payload.tx_id for tx in txs]

    def get_any_tx_id(self) -> str:
        """
        获取链上存在的任意交易Id
        :return: 链上某一交易Id
        """
        self._info('获取链上存在的任意交易Id')
        block_height = self.get_any_block_height()
        block_info = self._cc.get_block_by_height(block_height)
        tx = random.choice(block_info.block.txs)
        return tx.payload.tx_id

    def get_any_block_height(self) -> int:
        """
        获取链上存在的任意区块高度
        :return: 链上某一区块高度
        """
        self._info('获取链上存在的任意区块高度')
        current_block_height = self._cc.get_current_block_height()
        if current_block_height == 0:
            return current_block_height
        return random.choice(list(range(current_block_height)))

    def get_any_block_hash(self) -> str:
        """
        获取链上存在的任意区块哈希
        :return: 区块哈希
        """
        self._info('获取链上存在的任意区块哈希')
        block_height = self.get_any_block_height()
        return self.get_block_hash_by_height(block_height)

    def get_tx_count(self, start_block: int, end_block: int = None) -> int:
        """
        获取交易数量
        :param start_block: 起始区块高度(包括)
        :param end_block: 结束区块高度(包括), 为None是为当前区块高度
        :return: 交易数量
        """
        self._info(f'获取区块高度 {start_block} 到 {end_block} 之间交易数量 ')
        current_block_height = self._cc.get_current_block_height()
        if end_block is None:
            end_block = current_block_height
            assert end_block >= start_block, '[SDK] 结束区块高度应大于等于起始区块高度'
            assert end_block <= current_block_height, '[SDK] 结束区块高度应小于等于当前区块高度'
        total = 0
        for block_height in range(start_block + 1, end_block + 1):
            block_header = self._cc.get_block_header_by_height(block_height)
            total += block_header.tx_count
        return total

    def get_tx_statistic_data(self, start_block: int, end_block: int = None) -> dict:
        """
        获取交易性能统计数据
        :param start_block: 起始区块高度(包括)
        :param end_block: 结束区块高度(包括), 为None是为当前区块高度
        :return: 交易数量
        """
        self._info(f'获取区块高度 {start_block} 到 {end_block} 之间交易性能统计数据')
        start_timestamp = self.get_block_timestamp_by_height(start_block)

        tx_count = 0
        last_block_timestamp = start_timestamp
        tps_list = []
        for block_height in range(start_block + 1, end_block + 1):
            block_header = self._cc.get_block_header_by_height(block_height)
            block_timestamp = block_header.block_timestamp
            current_block_elapsed = block_timestamp - last_block_timestamp
            current_tx_count = block_header.tx_count
            if current_tx_count != 0:
                current_tps = current_tx_count / current_block_elapsed
                tps_list.append(current_tps)

            tx_count += current_tx_count
            last_block_timestamp = block_timestamp

        end_timestamp = last_block_timestamp

        total_block = end_block - start_block
        elapsed = end_timestamp - start_timestamp
        tx_avg = tx_count / total_block if total_block else None
        tps_avg = sum(tps_list) / len(tps_list)

        return dict(start_block=start_block, end_block=end_block, total_block=total_block, elapsed=elapsed,
                    tx_count=tx_count, tx_avg=tx_avg, tps_avg=tps_avg)


# 02
class CertManageOps(BaseOps):
    """证书管理"""

    @with_user_endorsers
    def check_cert_hash(self, cert_hash: str = None) -> bool:
        """
        检查证书哈希是否上链
        :param cert_hash: 证书哈希
        :return: 已上链返回True，否则返回False
        """
        self._info(f"检查证书哈希 {cert_hash} 是否上链")
        cert_hashes = [cert_hash] if cert_hash is not None else None
        return self._cc.query_cert(cert_hashes) is not None

    @with_user_endorsers
    def check_cert(self, cert_bytes_or_file_path: Union[Path, str, bytes] = None):
        """
        检查用户证书是否已上链
        :param cert_bytes_or_file_path: 证书二进制内容或证书文件路径
        :return: 已上链返回True，否则返回False
        """
        if cert_bytes_or_file_path is None:
            return self._cc.query_cert() is not None

        cert_bytes = cert_bytes_or_file_path
        self._info(f"检查用户证书 {cert_bytes} 是否已上链")

        if isinstance(cert_bytes_or_file_path, (Path, str)):
            cert_bytes = file_utils.read_file_bytes(cert_bytes_or_file_path)
        cert = crypto_utils.load_pem_cert(cert_bytes)
        cert_hash = crypto_utils.get_cert_hash_bytes(cert).hex()
        return self._cc.query_cert([cert_hash]) is not None

    # 02-00 添加证书
    @with_user_endorsers
    def add_cert(self, cert_hashes: List[str] = None, timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        添加证书
        <02-00-CERT_MANAGE-CERT_ADD>
        :param cert_hashes:
        :param timeout: 设置请求超时时间
        :param with_sync_result: 同步返回请求结果
        :return: 交易响应
        :raises RequestError: 请求失败
        """
        self._info(f"添加证书 {cert_hashes}")
        if cert_hashes is None:
            cert_hashes = [self._cc.user.cert_hash]
        return self._cc.add_cert(cert_hashes, timeout, with_sync_result)

    # 02-01 删除证书
    @with_user_endorsers
    def delete_cert(self, cert_hashes: List[str] = None,
                    timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        删除证书
        <02-01-CERT_MANAGE-CERTS_DELETE>
        :param cert_hashes: 证书hash列表, 每个证书hash应转为hex字符串
        :param timeout: 超时时长
        :param with_sync_result: 是否同步返回请求结果
        :return: Response
        :raises RequestError: 请求失败
        """
        self._info(f"删除证书 {cert_hashes}")
        payload = self._cc.create_cert_delete_payload(cert_hashes)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 02-02 根据证书哈希查询证书
    @with_user_endorsers
    def query_cert(self, cert_hashes: Union[list, str] = None, timeout: int = None) -> dict:
        """
        查询证书的hash是否已经上链
        <02-02-CERT_MANAGE-CERTS_QUERY>
        :param cert_hashes: 证书hash列表(List)，每个证书hash应转为hex字符串, 为None时查询当前用户证书
        :param timeout: 请求超时时间
        :return: CertInfos
        :raises 查询不到证书抛出 RequestError
        """
        self._info(f"查询证书 {cert_hashes}")
        return self._cc.query_cert(cert_hashes, timeout)

    # 02-03 冻结证书
    @with_user_endorsers
    def freeze_cert(self, certs: List[str], timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        冻结证书
        <02-03-CERT_MANAGE-CERTS_FREEZE>
        :param certs: 证书内容列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._info(f"冻结证书 {certs}")
        payload = self._cc.create_cert_freeze_payload(certs)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 02-04 解冻证书
    @with_user_endorsers
    def unfreeze_cert(self, certs: List[str], timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        解冻证书
        <02-04-CERT_MANAGE-CERTS_UNFREEZE>
        :param certs: 证书内容
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._info(f"解冻证书 {certs}")
        payload = self._cc.create_cert_unfreeze_payload(certs)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 02-05 吊销证书
    @with_user_endorsers
    def revoke_cert(self, cert_bytes_or_file_path: Union[Path, str, bytes] = None,
                    ca_key_bytes_or_file_path: Union[Path, str, bytes] = None,
                    ca_cert_bytes_or_file_path: Union[Path, str, bytes] = None,
                    cert_crl: bytes = None,
                    timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        吊销证书
         <02-05-CERT_MANAGE-CERTS_REVOKE>
        :param cert_bytes_or_file_path: 证书文件路径
        :param ca_key_bytes_or_file_path: 所属组织ca证书文件路径
        :param ca_cert_bytes_or_file_path: 所属组织ca私钥文件路径
        :param cert_crl: 指定吊销证书文件二进制内容
        :param timeout: RCP请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._info(f"吊销证书 {cert_bytes_or_file_path}")
        cert_crl = cert_crl or (crypto_utils.create_crl_bytes(cert_bytes_or_file_path, ca_key_bytes_or_file_path,
                                                              ca_cert_bytes_or_file_path) if cert_bytes_or_file_path else b'')

        payload = self._cc.create_cert_revoke_payload(cert_crl.decode())
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def check_cert_alias(self, alias=None) -> bool:
        if alias is None:
            alias = self._cc.alias
        self._info(f'检查证书别名 {alias} 是否上链')
        return self._cc.check_alias(alias)

    # 02-06 添加证书别名
    @with_user_endorsers
    def add_cert_alias(self, alias: str = None) -> dict:  # MemberType must be MemberType_CERT
        """
        添加证书别名
        <02-06-CERT_MANAGE-CERT_ALIAS_ADD>
        :return: 响应信息
        """
        self._info(f"添加证书别名 {alias}")
        return self._cc.add_alias(alias)

    # 02-07 通过别名更新证书
    @with_user_endorsers
    def update_cert_by_alias(self, alias: str, new_cert_pem: str,
                             timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        通过别名更新证书
        :param alias: 用户别名
        :param new_cert_pem: 新证书文件内容
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        self._info(f"通过别名 {alias} 更新证书为 {new_cert_pem}")
        payload = self._cc.create_update_cert_by_alias_payload(alias, new_cert_pem)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 02-08 删除证书别名
    @with_user_endorsers
    def delete_cert_alias(self, aliases: List[str], timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        删除证书别名
        :param aliases: 别名列表
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        self._info(f"删除证书别名 {aliases}")
        payload = self._cc.create_delete_cert_alias_payload(aliases)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 02-09 查询证书别名
    @with_user_endorsers
    def query_cert_alias(self, aliases: List[str] = None) -> dict:
        """
        查询证书别名
        <02-09-CERT_MANAGE-CERTS_ALIAS_QUERY>
        :param aliases: 证书别名列表
        :return: 仅当所有别名存在时返回别名信息列表，否则返回None，建议单个别名查询
        """
        self._info(f'查询证书别名 {aliases}')
        return self._cc.query_cert_alias(aliases)

    @staticmethod
    def gen_random_alias(prefix='alias_') -> str:
        """
        生成随机别名
        :param prefix: 别名前缀
        :return: 别名字符串
        """
        return '%s%s' % (prefix, str(uuid.uuid4()).replace('-', '_'))


# 04
class MultiSignOps(BaseOps):
    """多签管理"""

    # 04-00 发起多签请求
    @with_user_endorsers
    def req(self, params: Union[list, dict], tx_id: str = None, timeout: int = None,
            with_sync_result: bool = None) -> dict:
        """
        发起多签请求
        <04-00-MULTI_SIGN-REQ>
        :param params: 多签请求参数
        :param tx_id: 指定交易Id
        :param timeout: 请求超时时间
        :param with_sync_result: 是否同步获取交易结果
        :return: 交易响应或交易信息
        """
        self._info(f"发起多签请求 {params}")
        payload = self._cc.create_multi_sign_req_payload(params, tx_id)
        tx_response = self._cc.multi_sign_req(payload, timeout=timeout, with_sync_result=with_sync_result)
        return tx_response

    # 04-01 对多签请求Payload进行投票
    @with_user_endorsers
    def vote(self, tx_id: str, is_agree: bool = True, endorser: User = None,
             timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        根据交易Id对多签请求进行投票
        :param tx_id: 交易Id
        :param endorser: 投票用户对象
        :param is_agree: 是否同意，true为同意，false则反对
        :param timeout: 请求超时时间
        :param with_sync_result: 是否同步获取交易结果
        :return: 交易响应或交易信息
        """
        self._info(f"对多签请求 {tx_id} 进行投票")
        return self._cc.multi_sign_vote_by_tx_id(tx_id, endorser, is_agree, timeout, with_sync_result)

    # 04-02 查询多签状态
    @with_user_endorsers
    def query(self, tx_id: str, timeout: int = None) -> dict:
        """
        查询多签状态
        <04-02-MULTI_SIGN-QUERY>
        :param tx_id: 交易ID
        :param timeout: RPC请求超时时间
        :return: 多签信息
        """
        self._info(f"查询交易 {tx_id} 多签状态 ")
        return self._cc.multi_sign_query(tx_id, timeout=timeout)

    @with_user_endorsers
    def trig(self, tx_id: str, gas_limit: int = None, timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        发送线上多签触发请求到节点 v2.3.1新增
        :param gas_limit:
        :param tx_id: 多签请求交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易相应
        """
        self._info("触发多签执行")
        # tx = self._cc.get_tx_by_tx_id(tx_id)
        # multi_sign_req_payload = tx.transaction.payload
        return self._cc.multi_sign_trig(tx_id=tx_id, gas_limit=gas_limit,
                                        timeout=timeout, with_sync_result=with_sync_result)

    @with_user_endorsers
    def create_contract_req(self, contract_name: str, byte_code_path: Union[Path, str],
                            runtime_type: Union[RuntimeType, str], version: str = '1.0') -> dict:
        byte_code = load_byte_code(byte_code_path)
        runtime_type = ensure_enum(runtime_type, RuntimeType).name
        params = {'SYS_CONTRACT_NAME': 'CONTRACT_MANAGE',
                  'SYS_METHOD': 'INIT_CONTRACT',
                  'CONTRACT_NAME': contract_name,
                  'CONTRACT_VERSION': version,
                  'CONTRACT_BYTECODE': byte_code,
                  'CONTRACT_RUNTIME_TYPE': runtime_type
                  }
        return self.req(params)


# 05
class ContractManageOps(BaseOps):
    # ================================ 合约管理 ===============================================
    # 05-00 获取合约信息
    @with_user_endorsers
    def get_contract_info(self, contract_name: str) -> Union[dict, None]:
        """
        获取合约信息
        <05-00-CONTRACT_MANAGE-GET_CONTRACT_INFO> # todo
        :param contract_name: 合约名称或合约地址
        :return: 合约存在则返回合约信息Contract对象，合约不存在抛出ContractFail
        :raise: RequestError: 请求出错
        :raise: AssertionError: 响应code不为0,检查响应时抛出断言失败
        :raise: 当数据不是JSON格式时，抛出json.decoder.JSONDecodeError
        """
        self._info(f"获取合约 {contract_name} 信息")
        return self._cc.get_contract_info(contract_name)

    @with_user_endorsers
    def get_contract_address(self, contract_name: str) -> Union[str, None]:
        """
        获取合约地址
        :param contract_name: 合约名称或合约地址
        :return:
        """
        self._info(f"获取合约 {contract_name} 地址")
        contract = self._cc.get_contract_info(contract_name)
        if contract:
            return contract.address

    @with_user_endorsers
    def get_contract_status(self, contract_name: str) -> Union[ContractStatus, None]:
        """
        获取合约状态
        :param contract_name: 合约名称或合约地址
        :return: 合约状态
        """
        self._info(f"获取合约 {contract_name} 状态")
        contract = self._cc.get_contract_info(contract_name)
        if contract:
            return ContractStatus(contract.status)

    # 05-01 获取合约ByteCode
    @with_user_endorsers
    def get_contract_byte_code(self, contract_name: str) -> bytes:  # todo
        """
        获取合约ByteCode
        <05-01-CONTRACT_MANAGE-GET_CONTRACT_BYTECODE> # todo
        :param contract_name: 用户合约名称
        :return: 合约存在则返回合约信息Contract对象，合约不存在抛出ContractFail
        :raise: RequestError: 请求出错
        :raise: AssertionError: 响应code不为0,检查响应时抛出断言失败
        :raise: 当数据不是JSON格式时，抛出json.decoder.JSONDecodeError
        """
        self._info(f"获取合约 {contract_name} ByteCode源码")
        return self._cc.get_contract_byte_code(contract_name)

    # 05-02 获取链上全部合约列表
    @with_user_endorsers
    def get_contract_list(self, runtime_type: RuntimeType = None, status: ContractStatus = None) -> List[dict]:
        """
        获取链上全部合约列表
        <05-02-CONTRACT_MANAGE-GET_CONTRACT_LIST> # todo
        :param: runtime_type 指定合约类型
        :param: status 指定合约状态
        :return: 合约Contract对象列表
        :raise: RequestError: 请求出错
        :raise: AssertionError: 响应code不为0,检查响应时抛出断言失败
        :raise: 当数据不是JSON格式时，抛出json.decoder.JSONDecodeError
        """
        _msg = '获取链上合约列表'
        if runtime_type is not None:
            _msg += f' runtime_type: {runtime_type}'
        if status is not None:
            _msg += f' status: {status}'
        self._info(_msg)

        contract_list = self._cc.get_contract_list()
        if runtime_type is not None:
            contract_list = [contract for contract in contract_list if contract.runtime_type == runtime_type.value]
        if status is not None:
            contract_list = [contract for contract in contract_list if contract.status == status.value]
        return contract_list

    # 05-03 获取禁用系统合约名称列表
    @with_user_endorsers
    def get_disabled_native_contract_list(self) -> List[str]:
        """
        获取禁用系统合约名称列表
        <05-03-CONTRACT_MANAGE-GET_DISABLED_CONTRACT_LIST> # todo
        :return: 禁用合约名称列表
        """
        self._info('获取禁用系统合约名称列表')
        return self._cc.get_disabled_native_contract_list()

    @with_user_endorsers
    def check_contract(self, contract_name: str) -> bool:
        """
        检查合约是否已创建
        :param contract_name: 合约名称
        :return: 合约存在返回True, 否则返回False
        """
        self._info(f'检查合约 {contract_name} 是否已创建')
        contract = self._cc.get_contract_info(contract_name)
        return contract is not None

    # 05-00 创建合约
    @with_user_endorsers
    def create_contract(self, contract_name: str, byte_code_path: str, runtime_type: Union[RuntimeType, str],
                        params: dict = None, version: str = None, gas_limit: int = None, tx_id: str = None,
                        timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        创建合约
        :param contract_name: 合约名
        :param version: 合约版本
        :param byte_code_path: 合约字节码：可以是字节码；合约文件路径；或者 hex编码字符串；或者 base64编码字符串。
        :param runtime_type: contract_pb2.RuntimeType.WASMER
        :param params: 合约参数，dict类型，key 和 value 尽量为字符串
        :param gas_limit: Gas限制
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises ValueError: 如果 byte_code 不能转成合约字节码
        :raises: RequestError: 请求失败
        """
        # runtime_type = ensure_enum(runtime_type, RuntimeType)
        self._info(f'创建{runtime_type}合约 {contract_name}')
        payload = self._cc.create_contract_create_payload(contract_name, version, byte_code_path, runtime_type,
                                                          params, gas_limit, tx_id)

        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    @with_user_endorsers
    def invoke_contract(self, contract_name: str, method: str, params: dict = None,
                        gas_limit: int = None, tx_id: str = None, result_type: str = None,
                        timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        调用合约
        :param contract_name: 合约名
        :param method: 合约方法名
        :param params: 合约方法参数
        :param gas_limit: 交易Gas限制
        :param tx_id: 指定交易Id
        :param result_type: 结果类型, 用于解析响应中的result
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步交易执行结果。如果不同步，返回tx_id，供异步查询; 同步则循环等待，返回交易的执行结果。
        :return: TxResponse
        :raises RequestError: 请求失败
        """
        if params:
            self._info(f'调用合约 {contract_name} method: {method} params: {params}')
        else:
            self._info(f'调用合约 {contract_name} method: {method}')
        response = self._cc.invoke_contract(contract_name, method, params, tx_id, gas_limit, timeout, with_sync_result)
        return response if result_type is None else result_utils.parse_result(response, result_type)

    @with_user_endorsers
    def query_contract(self, contract_name: str, method: str, params: Union[dict, list] = None, result_type: str = None,
                       timeout: int = None) -> dict:
        """
        查询用户合约
        :param contract_name: 合约名
        :param method: 调用合约方法名
        :param params: 调用参数，参数类型为dict
        :param result_type: 解析结果类型支持 STRING / INT / JSON / HEX
        :param timeout: RPC请求超时时间
        :return: TxResponse, 结果不存在时返回None
        :raises RequestError: 请求失败
        """
        if params:
            self._info(f'查询合约 {contract_name} method: {method} params: {params}')
        else:
            self._info(f'查询合约 {contract_name} method: {method}')
        response = self._cc.query_contract(contract_name, method, params, timeout=timeout)
        return response if result_type is None else result_utils.parse_result(response, result_type)

    # 05-01 升级合约
    @with_user_endorsers
    def upgrade_contract(self, contract_name: str, byte_code_path: str, runtime_type: Union[RuntimeType, str],
                         params: dict = None, version: str = None, gas_limit: int = None, tx_id: str = None,
                         timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        升级合约
        :param contract_name: 合约名
        :param version: 合约版本
        :param byte_code_path: 合约字节码：可以是字节码；合约文件路径；或者 hex编码字符串；或者 base64编码字符串。
        :param runtime_type: contract_pb2.RuntimeType.WASMER
        :param params: 合约参数，dict类型，key 和 value 尽量为字符串
        :param gas_limit: 交易Gas限制
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises ValueError: 如果 byte_code 不能转成合约字节码
        :raises: RequestError: 请求失败
        """
        if version is None:
            version = self.gen_new_contract_version(contract_name)
        self._info(f'升级{runtime_type}合约 {contract_name} version: {version}')
        payload = self._cc.create_contract_upgrade_payload(contract_name, version, byte_code_path, runtime_type,
                                                           params, gas_limit, tx_id)

        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-02 冻结合约
    @with_user_endorsers
    def freeze_contract(self, contract_name: str, tx_id: str = None, timeout: int = None,
                        with_sync_result: bool = None) -> dict:
        """
        冻结合约
        :param contract_name: 合约名称
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求失败
        """
        self._info(f'冻结合约 {contract_name}')
        payload = self._cc._create_contract_manage_payload(ContractManageMethod.FREEZE_CONTRACT.name, contract_name,
                                                           tx_id=tx_id)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-03 解冻合约
    @with_user_endorsers
    def unfreeze_contract(self, contract_name: str, tx_id: str = None, timeout: int = None,
                          with_sync_result: bool = None) -> dict:
        """
        解冻合约
        :param contract_name: 合约名称
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求失败
        """
        self._info(f'解冻合约 {contract_name}')
        payload = self._cc._create_contract_manage_payload(ContractManageMethod.UNFREEZE_CONTRACT.name, contract_name,
                                                           tx_id=tx_id)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-04 吊销合约
    @with_user_endorsers
    def revoke_contract(self, contract_name: str, tx_id=None, timeout: int = None,
                        with_sync_result: bool = None) -> dict:
        """
        吊销合约
        :param contract_name: 合约名称
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求失败
        """
        self._info(f'吊销合约 {contract_name}')
        payload = self._cc._create_contract_manage_payload(ContractManageMethod.REVOKE_CONTRACT.name, contract_name,
                                                           tx_id=tx_id)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def gen_new_contract_version(self, contract_name: str, increase: float = 1.0) -> str:
        """
        查询合约当前版本，并生成合约新版本号
        :param contract_name: 合约名称
        :param increase: 在原版本基础上增加值，默认原版本+1
        :return: 合约版本
        """
        self._info(f'为合约 {contract_name} 生成合约新版本号')
        version = self._cc.get_contract_info(contract_name).version
        return str(float(version) + increase)

    def calc_contract_address(self, contract_name: str) -> str:
        """
        通过合约名称计算合约地址
        :param contract_name: 合约名称
        :return: 合约地址
        """
        self._info(f'根据合约名 {contract_name} 生成合约地址')
        return address_utils.name2addr(contract_name, addr_type=self._cc.addr_type)

    def gen_random_tx_id(self):
        """生成随机交易Id"""
        tx_id = common.gen_rand_tx_id()
        self._info(f'生成随机交易Id {tx_id}')
        return tx_id

    def gen_random_contract_name(self, prefix='contract_'):
        """生成随机合约名"""
        contract_name = common.gen_rand_contract_name(prefix)
        self._info(f'生成随机合约名 {contract_name}')
        return contract_name

    def parse_result(self, response: dict, result_type: str = 'STRING'):
        self._info('解析响应结果')
        return result_utils.parse_result(response, result_type)

    def check_response(self, response: dict) -> bool:
        self._info('检查响应是否成功')
        return result_utils.result_is_ok(response)

    @with_user_endorsers
    def invoke_system_contract(self, contract_name: str, method: str, params: Dict[str, Union[str, int, bool]] = None,
                               tx_id: str = None, gas_limit: int = None,
                               timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        调用系统合约
        :param contract_name: 系统合约名称
        :param method: 系统合约方法
        :param params: 系统合约方法所需的参数
        :param tx_id: 指定交易Id，默认为空是生成随机交易Id
        :param gas_limit: Gas交易限制
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应信息
        """
        self._info(f'调用系统合约 {contract_name}-{method} params: {params}')
        if timeout is None:
            timeout = DefaultConfig.rpc_send_tx_timeout
        if gas_limit is None:
            gas_limit = self._cc._default_gas_limit

        payload = self._cc._payload_builder.create_invoke_payload(contract_name, method, params, tx_id,
                                                                  gas_limit=gas_limit)
        response = self._cc.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 05-06 授权访问系统合约
    @with_user_endorsers
    def grant_native_contract_access(self, contract_list: List[str],
                                     timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        授权访问系统合约
        :param contract_list: 待授权访问的系统合约列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._info(f'授权访问系统合约 {contract_list}')
        params = {ParamKey.NATIVE_CONTRACT_NAME.name: json.dumps(contract_list)}
        payload = self._cc._payload_builder.create_invoke_payload(SystemContractName.CONTRACT_MANAGE.name,
                                                                  ContractManageMethod.GRANT_CONTRACT_ACCESS.name,
                                                                  params)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-06 吊销系统合约访问授权
    @with_user_endorsers
    def revoke_native_contract_access(self, contract_list: List[str],
                                      timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        吊销系统合约访问授权
        :param contract_list: 待吊销访问带系统合约列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._info(f'吊销系统合约访问授权 {contract_list}')
        params = {ParamKey.NATIVE_CONTRACT_NAME.name: json.dumps(contract_list)}
        payload = self._cc._payload_builder.create_invoke_payload(SystemContractName.CONTRACT_MANAGE.name,
                                                                  ContractManageMethod.REVOKE_CONTRACT_ACCESS.name,
                                                                  params)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-07 验证系统合约访问授权
    @with_user_endorsers
    def verify_native_contract_access(self, contract_list: List[Union[SystemContractName, str]],
                                      timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        验证系统合约是否可访问
        :param contract_list: 待验证合约列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._info(f'验证系统合约访问授权 {contract_list}')
        params = {ParamKey.NATIVE_CONTRACT_NAME.name: json.dumps(contract_list)}
        payload = self._cc._payload_builder.create_invoke_payload(SystemContractName.CONTRACT_MANAGE.name,
                                                                  ContractManageMethod.VERIFY_CONTRACT_ACCESS.name,
                                                                  params)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 05-08 创建新的系统合约
    # @with_user_endorsers
    # def init_new_native_contract(self, contract_name: str, version: str,
    #                              byte_code_path: str,
    #                              runtime_type: Union[RuntimeType, str],
    #                              params: Dict[str, Union[str, int, bool]] = None,
    #                              gas_limit: int = None) -> Payload:
    #     """
    #     创建新的系统合约
    #     :param contract_name: 合约名
    #     :param version: 合约版本
    #     :param byte_code_path: 合约字节码：可以是字节码；合约文件路径；或者 hex编码字符串；或者 base64编码字符串。
    #     :param runtime_type: contract_pb2.RuntimeType.WASMER
    #     :param params: 合约参数，dict类型，key 和 value 尽量为字符串
    #     :param gas_limit: Gas交易限制
    #     :return: Payload
    #     :raises ValueError: 如果 byte_code 不能转成合约字节码
    #     """
    #     self._info(f'创建新的系统合约 {contract_name}')
    #     raise NotImplementedError('待实现')


# 06
class PrivateComputeOps(BaseOps):
    """隐私计算操作"""

    # 06-02 保存可信执行环境证书
    @with_user_endorsers
    def save_ca_cert(self, enclave_ca_cert: str,
                     tx_id: str = None, timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        保存可信执行环境根证书
        :param enclave_ca_cert: 可信执行环境根证书
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 交易响应
        """
        self._info(f'保存可信执行环境证书 {enclave_ca_cert}')
        return self._cc.save_enclave_ca_cert(enclave_ca_cert, tx_id, timeout, with_sync_result)

    # 06-05 获取可信执行环境报告
    @with_user_endorsers
    def save_enclave_report(self, enclave_id: str, report: str,
                            tx_id: str = None, timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        获取可信执行环境报告
        :param enclave_id: 可信执行环境Id
        :param report: 报告数据
        :param tx_id: 指定交易Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 交易响应
        """
        self._info(f'获取可信执行环境 {enclave_id} 报告 {report}')
        return self._cc.save_enclave_report(enclave_id, report, tx_id, timeout, with_sync_result)


# 07
class DposErc20Ops(BaseOps):
    """DPOS共识下ERC20操作"""

    # 07-00 查询归属人
    @with_user_endorsers
    def owner(self) -> str:  # todo get_owner
        """
        查询归属人
        <07-00-DPOS_ERC20-GET_OWNER>
        """
        self._info('查询归属人')
        return self._cc.owner()

    # 07-01 查询ERC20合约的精度
    @with_user_endorsers
    def decimals(self) -> int:
        """
        查询ERC20合约的精度
        <07-01-DPOS_ERC20-GET_DECIMALS>
        :return: 合约精度
        """
        self._info('查询ERC20合约的精度')
        return self._cc.decimals()

    # 07-02 转账
    @with_user_endorsers
    def transfer(self, address: str, amount: int, timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        转账
        :param address: 接收Token的地址
        :param amount: 转账数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 请求响应
        """
        self._info(f'转账 address: {address} amount: {amount}')
        payload = self._cc.create_transfer_payload(address, amount)
        response = self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 07-03 从某个地址转账
    @with_user_endorsers
    def transfer_from(self, _from: str, to: str, amount: int, timeout: int = None,
                      with_sync_result: bool = None) -> dict:
        """
        从某个地址转账
        :param _from: 转出账户地址
        :param to: 转如账户地址
        :param amount: 转出数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 请求响应
        """
        self._info(f'从 {_from} 转账到 {to} amount: {amount}')
        payload = self._cc.create_transfer_from_payload(_from, to, amount)
        response = self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 07-04 查询账户余额
    @with_user_endorsers
    def balance_of(self, address: str) -> int:
        """
        查询账户余额
        <07-04-DPOS_ERC20-GET_BALANCEOF>
        :param address: 账户地址
        :return: 账户余额
        """
        self._info(f'查询账户 {address} 余额')
        return self._cc.balance_of(address)

    # 07-05 转账证明
    @with_user_endorsers
    def approve(self, _from: str, to: str, amount: int,
                timeout: int = None, with_sync_result: bool = None):
        self._info(f'证明从 {_from} 转账到 {to} amount: {amount}')
        payload = self._cc.create_approve_payload(_from, to, amount)
        response = self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 07-07 消耗Token
    @with_user_endorsers
    def burn(self, address: str, amount: int,
             timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        Burn Token
        :param address: 接收Token的地址
        :param amount: 发行数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 请求响应
        """
        self._info(f'消耗Token address: {address} amount: {amount}')
        payload = self._cc.create_burn_payload(address, amount)
        response = self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 07-08 发行Token
    @with_user_endorsers
    def mint(self, address: str, amount: int,
             timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        发行Token
        :param address: 接收Token的地址
        :param amount: 发行数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 请求响应
        """
        self._info(f'发行Token address: {address} amount: {amount}')
        payload = self._cc.create_mint_payload(address, amount)
        response = self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 07-09 转移归属
    @with_user_endorsers
    def transfer_ownership(self, address: str, timeout: int = None, with_sync_result: bool = None):
        """
        转移归属
        :param address: 接收资产地址
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮训交易结果
        :return: 请求响应
        """
        self._info(f'转移归属至 {address}')
        payload = self._cc.create_transfer_ownership_payload(address)
        response = self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 07-10 查询Token总供应量
    @with_user_endorsers
    def total(self) -> int:
        """
        查询Token总供应量
        <07-10-DPOS_ERC20-GET_TOTAL_SUPPLY>
        :return:
        """
        self._info('查询Token总供应量')
        return self._cc.total()


# 08 DPOS共识权益操作
class DposStakeOps(BaseOps):
    """DPOS共识权益操作"""

    # 08-00 查询所有的候选人
    @with_user_endorsers
    def get_all_candidates(self) -> dict:
        """
        查询所有的候选人
        <08-00-DPOS_STAKE-GET_ALL_CANDIDATES>
        :return: 候选人列表
        """
        self._info('查询所有的候选人')
        return self._cc.get_all_candidates()

    # 08-01 通过地址获取验证人的信息
    @with_user_endorsers
    def get_validator_by_address(self, address: str):
        """
        通过地址获取验证人的信息
        <08-01-DPOS_STAKE-GET_VALIDATOR_BY_ADDRESS>
        :param address:
        :return:
        """
        self._info(f'通过地址 {address} 获取验证人的信息')
        return self._cc.get_validator_by_address(address)

    # 08-02 抵押权益到验证人
    @with_user_endorsers
    def delegate(self, address: str, amount: int) -> dict:  # todo 确认是否需要轮训
        """
        抵押权益到验证人
        <08-02-DPOS_STAKE-DELEGATE>
        :param address:
        :param amount:
        :return:
        """
        self._info(f'抵押权益到验证人 address: {address} amount: {amount}')
        return self._cc.delegate(address, amount)

    # 08-03 查询指定地址的抵押信息
    @with_user_endorsers
    def get_delegations_by_address(self, address: str) -> dict:
        """
        查询指定地址的抵押信息
        <08-03-DPOS_STAKE-GET_DELEGATIONS_BY_ADDRESS>
        :param address:
        :return:
        """
        self._info(f'查询指定地址 {address} 的抵押信息')
        return self._cc.get_delegations_by_address(address)

    # 08-04 查询指定地址的抵押信息
    @with_user_endorsers
    def get_user_delegation_by_validator(self, delegator: str, validator: str) -> dict:
        """
        查询指定地址的抵押信息
        <08-04-DPOS_STAKE-GET_USER_DELEGATION_BY_VALIDATOR>
        :param delegator:
        :param validator:
        :return:
        """
        self._info(f'查询指定地址的抵押信息 delegator: {delegator} validator: {validator}')
        return self._cc.get_user_delegation_by_validator(delegator, validator)

    # 08-04 从验证人解除抵押的权益
    @with_user_endorsers
    def undelegate(self, address: str, amount: int) -> dict:
        """
        从验证人解除抵押的权益
        <08-05-DPOS_STAKE-UNDELEGATE>
        :param address:
        :param amount:
        :return:
        """
        self._info(f'从验证人解除抵押的权益 address: {address} amount: {amount}')
        return self._cc.undelegate(address, amount)

    # 08-06 查询指定世代信息
    @with_user_endorsers
    def get_epoch_by_id(self, epoch_id: str) -> dict:
        """
        查询指定世代信息
        <08-06-DPOS_STAKE-READ_EPOCH_BY_ID>
        :param epoch_id:
        :return:
        """
        self._info(f'查询世代 {epoch_id} 信息')
        return self._cc.get_epoch_by_id(epoch_id)

    # 08-07 查询当前世代信息
    @with_user_endorsers
    def get_last_epoch(self) -> dict:
        """
        查询当前世代信息
        <08-07-DPOS_STAKE-READ_LATEST_EPOCH>
        :return:
        """
        return self._cc.get_last_epoch()

    # 08-08 Stake合约中设置验证人的NodeId
    @with_user_endorsers
    def set_node_id(self, node_id: str) -> str:
        """
        Stake合约中设置验证人的NodeId
        <08-08-DPOS_STAKE-SET_NODE_ID>
        :param node_id:
        :return:
        """
        self._info(f'设置验证人的NodeId {node_id}')
        return self._cc.set_node_id(node_id)

    # 08-09 Stake合约中查询验证人的NodeId
    @with_user_endorsers
    def get_node_id(self, address: str) -> str:
        """
        Stake合约中查询验证人的NodeId
        <08-09-DPOS_STAKE-GET_NODE_ID>
        :param address:
        :return:
        """
        self._info(f'查询验证人 {address} 的NodeId')
        return self._cc.get_node_id(address)

    # 08-10
    @with_user_endorsers
    def set_min_self_delegation(self, min_self_delegation: int, timeout: int = None,
                                with_sync_result: bool = None) -> dict:
        """
        <08-10-DPOS_STAKE-UPDATE_MIN_SELF_DELEGATION>
        :return:
        """
        self._info('更新验证人节点的最少自我抵押数量')
        return self._cc.set_min_self_delegation(min_self_delegation, timeout, with_sync_result)

    # 08-11
    @with_user_endorsers
    def get_min_self_delegation(self) -> int:
        """
        <08-11-DPOS_STAKE-READ_MIN_SELF_DELEGATION>
        :return:
        """
        self._info('获取验证人节点的最少自我抵押数量')
        return self._cc.get_min_self_delegation()

    # 08-12
    @with_user_endorsers
    def set_epoch_validator_number(self, epoch_validator_number: int, timeout: int = None,
                                   with_sync_result: bool = None) -> dict:
        """
        <08-12-DPOS_STAKE-UPDATE_EPOCH_VALIDATOR_NUMBER>
        :return:
        """
        self._info('更新世代中的验证人数量')
        return self._cc.set_epoch_validator_number(epoch_validator_number, timeout, with_sync_result)

    # 08-13
    @with_user_endorsers
    def get_epoch_validator_number(self) -> int:
        """
        <08-13-DPOS_STAKE-READ_EPOCH_VALIDATOR_NUMBER>
        :return:
        """
        self._info('获取世代中的验证人数量')
        return self._cc.get_epoch_validator_number()

    # 08-14
    @with_user_endorsers
    def set_epoch_block_number(self, epoch_block_number: int, timeout: int = None,
                               with_sync_result: bool = None) -> dict:
        """
        <08-14-DPOS_STAKE-UPDATE_EPOCH_BLOCK_NUMBER>
        :return:
        """
        self._info('更新世代中的区块数量')
        return self._cc.set_epoch_block_number(epoch_block_number, timeout, with_sync_result)

    # 08-15
    @with_user_endorsers
    def get_epoch_block_number(self) -> int:
        """
        <08-15-DPOS_STAKE-READ_EPOCH_BLOCK_NUMBER>
        :return:
        """
        self._info('获取世代中的区块数量')
        return self._cc.get_epoch_block_number()

    # 08-16 查询收到解质押退款间隔的世代数
    @with_user_endorsers
    def get_unbounding_interval_epoch_number(self) -> int:
        """
        查询收到解质押退款间隔的世代数
         <08-16-DPOS_STAKE-READ_COMPLETE_UNBOUNDING_EPOCH_NUMBER>
        :return:
        """
        self._info('查询收到解质押退款间隔的世代数')
        return self._cc.get_unbounding_interval_epoch_number()

    # 08-17 查询Stake合约的系统地址
    @with_user_endorsers
    def get_stake_contract_address(self) -> str:
        """
        查询Stake合约的系统地址
        <08-18-DPOS_STAKE-READ_SYSTEM_CONTRACT_ADDR>
        :return:
        """
        self._info('查询Stake合约的系统地址')
        return self._cc.get_stake_contract_address()

    # 08-19
    @with_user_endorsers
    def unbounding(self):
        """
        <08-19-DPOS_STAKE-UNBOUNDING>
        :return:
        """
        self._info('反质押')
        raise NotImplementedError("待实现")

    # 08-20
    @with_user_endorsers
    def create_epoch(self):
        """
        <08-20-DPOS_STAKE-CREATE_EPOCH>
        :return:
        """
        self._info('创建新的世代')
        raise NotImplementedError("待实现")

    # 08-21
    @with_user_endorsers
    def set_epoch_validator_number_and_epoch_block_number(self, epoch_block_number: int, epoch_validator_number: int,
                                                          timeout: int = None, with_sync_result: bool = None):
        """
        <08-21-DPOS_STAKE-UPDATE_EPOCH_VALIDATOR_NUMBER_AND_EPOCH_BLOCK_NUMBER>
        :return:
        """
        return self._cc.set_epoch_validator_number_and_epoch_block_number(epoch_block_number, epoch_validator_number,
                                                                          timeout, with_sync_result)


# 09 订阅管理操作
class SubscribeManageOps(BaseOps):
    """订阅管理操作"""

    # 09-00 订阅区块
    @with_user_endorsers
    def subscribe_block(self, start_block: int, end_block: int, with_rw_set=False, only_header=False,
                        timeout: int = None, callback: Callable = None):
        """
        订阅区块
        :param start_block: 订阅的起始区块
        :param end_block: 订阅的结束区块
        :param with_rw_set: 是否包含读写集
        :param only_header: 是否只订阅区块头
        :param timeout: 订阅尚未产生区块的等待超时时间, 默认60s
        :param callback: 回调函数
        :return 回调函数返回值
        """
        self._info(f"订阅区块 {start_block}->{end_block}")
        self._cc.subscribe_block(start_block, end_block, with_rw_set, only_header, timeout, callback)

    # 09-01 订阅交易
    @with_user_endorsers
    def subscribe_tx(self, contract_name: str = None, tx_ids: List[str] = None, start_block: int = None,
                     end_block: int = None,
                     timeout: int = None, callback: Callable = None):
        """
        订阅交易
        :param start_block: 订阅的起始区块
        :param end_block: 订阅的结束区块
        :param contract_name: 交易所属合约名称
        :param tx_ids: 指定交易Id列表进行订阅
        :param timeout: RPC请求超时时间
        :param callback: 回调函数
        :return 回调函数返回值
        """
        self._info(f"订阅交易 start_block:contract_name: {contract_name} tx_ids: {tx_ids} {start_block}->{end_block}")
        self._cc.subscribe_tx(start_block, end_block, contract_name, tx_ids, timeout, callback)

    # 09-02 订阅合约事件
    @with_user_endorsers
    def subscribe_contract_event(self, topic: str, contract_name: str = None, start_block: int = None,
                                 end_block: int = None,
                                 timeout: int = None, callback: Callable = None) -> None:
        """
        订阅合约事件
        :param start_block: 订阅的起始区块
        :param end_block: 订阅的结束区块
        :param topic: 订阅待事件主题
        :param contract_name: 事件所属合约名称
        :param timeout: RPC请求超时时间
        :param callback: 回调函数
        :return 回调函数返回值
        """
        self._info(f"订阅合约事件 topic: {topic} contract_name: {contract_name} {start_block}->{end_block}")
        self._cc.subscribe_contract_event(start_block, end_block, topic, contract_name, timeout, callback)


# 10 归档管理操作
class ArchiveManageOps(BaseOps):
    """归档管理操作"""

    # 10-00 归档区块
    @with_user_endorsers
    def archive_block(self, target_block_height: int, timeout: int = None) -> dict:
        """
        归档区块
        :param target_block_height: 目标区块高度
        :param timeout: RPC请求超时时间
        :return: 请求响应
        """
        self._info(f'归档区块 {target_block_height}')
        payload = self._cc.create_archive_block_payload(target_block_height)
        return self._cc.send_archive_block_request(payload, timeout=timeout)

    # 10-01 恢复区块
    @with_user_endorsers
    def restore_block(self, full_block: bytes, timeout: int = None) -> dict:
        """
        恢复区块
        :param full_block: 完整区块数据
        :param timeout: RPC请求超时时间
        :return: 请求响应
        """
        self._info(f'恢复区块')
        payload = self._cc.create_restore_block_payload(full_block)
        return self._cc.send_archive_block_request(payload, timeout=timeout)


# 12 公钥管理操作
class PubkeyManageOps(BaseOps):
    """公钥管理操作"""

    @with_user_endorsers
    def check_pubkey(self, pubkey: str, timeout: int = None) -> bool:  # todo
        self._info(f'检查公钥是否上链')
        try:
            self._cc.query_pubkey(pubkey, timeout)
            return True
        except Exception:
            return False

    # 12-00 添加公钥
    @with_user_endorsers
    def add_pubkey(self, pubkey: str, org_id: str, role: Union[Role, str], timeout: int = None,
                   with_sync_result: bool = True) -> dict:
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
        self._info(f'添加公钥 pubkey: {pubkey} org_id: {org_id} role: {role}')
        payload = self._cc.create_pubkey_add_payload(pubkey, org_id, role)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 12-01 删除公钥
    @with_user_endorsers
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
        self._info(f'删除公钥 pubkey: {pubkey} org_id: {org_id}')
        payload = self._cc.create_pubkey_delete_payload(pubkey, org_id)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 12-02 查询公钥
    @with_user_endorsers
    def query_pubkey(self, pubkey: str, timeout: int = None) -> dict:
        """
        查询公钥
        <12-02-PUBKEY_MANAGE-PUBKEY_QUERY>
        :param pubkey:公钥文件内容
        :param timeout: RPC请求超时时间
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        self._info(f'查询公钥 {pubkey}')
        return self._cc.query_pubkey(pubkey, timeout)


# 13 Gas管理操作
class AccountManagerOps(BaseOps):
    """Gas管理操作"""

    @with_user_endorsers
    def check_gas_admin(self, address: str = None) -> bool:
        """
        检查当前客户端用户是否Gas管理员
        :return: 当前客户端用户是Gas管理员返回True, 否则返回False
        """
        if address is None:
            self._info(f'检查当前用户是否Gas管理员')
            address = self._cc.user.address
        else:
            self._info(f'检查用户 {address} 是否Gas管理员')
        return address == self._cc.get_gas_admin()

    # 13-00 设置Gas管理员地址
    @with_user_endorsers
    def set_admin(self, address: str = None, timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        设置Gas管理员地址
        :param address: 用户地址-为None时为当前用户地址
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        if address is None:
            address = self._cc.sender_address
        self._info(f'设置Gas管理员地址 {address}')
        payload = self._cc.create_set_gas_admin_payload(address)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-01 查询Gas管理员地址
    @with_user_endorsers
    def get_admin(self) -> str:
        """
        查询Gas管理员地址
        <13-01-ACCOUNT_MANAGER-GET_ADMIN>
        :return: Gas管理员账户地址
        """
        self._info(f'查询Gas管理员地址')
        return self._cc.get_gas_admin()

    # 13-02 Gas充值
    @with_user_endorsers
    def recharge_gas(self, address: str = None, amount: int = None,
                     timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        Gas充值
        :param address: 充值账户地址
        :param amount: 重置数量
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        if address is None:
            address = self._cc.address
        self._info(f'Gas充值 address: {address} amount: {amount}')
        recharge_gas_list = [RechargeGasItem(address, amount)]
        payload = self._cc.create_recharge_gas_payload(recharge_gas_list)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-03 获取Gas账户余额
    @with_user_endorsers
    def get_gas_balance(self, address: str = None) -> int:
        """
        获取Gas账户余额
        <13-03-ACCOUNT_MANAGER-GET_BALANCE>
        :param str address: 账户地址
        :return: 账户余额
        """
        if address is None:
            address = self._cc.address
        self._info(f'获取Gas账户 {address} 余额')
        return self._cc.get_gas_balance(address)

    # 13-04 Gas收费
    @with_user_endorsers
    def charge_gas(self, recharge_gas_list: List[RechargeGasItem],
                   timeout: int = None, with_sync_result: bool = None):  # todo 待验证
        """
        Gas收费
        :param recharge_gas_list:
        :param timeout:
        :param with_sync_result:
        :return:
        """
        self._info(f'Gas收费')
        payload = self._cc.create_charge_gas_payload(recharge_gas_list)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-05 冻结Gas账户
    @with_user_endorsers
    def freeze_gas_account(self, address: str, timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        冻结Gas账户
        :param address: 待冻结账户地址
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        self._info(f'冻结Gas账户 {address}')
        payload = self._cc.create_frozen_gas_account_payload(address)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-06 解冻Gas账户
    @with_user_endorsers
    def unfreeze_gas_account(self, address: str, timeout: int = None, with_sync_result: bool = None) -> dict:
        """
        解冻Gas账户
        :param address: 待冻结账户地址
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        self._info(f'解冻Gas账户 {address}')
        payload = self._cc.create_unfrozen_gas_account_payload(address)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-07 查询Gas账户状态
    @with_user_endorsers
    def get_gas_account_status(self, address: str = None) -> bool:
        """
        查询Gas账户状态
        <13-07-ACCOUNT_MANAGER-ACCOUNT_STATUS>
        :param str address: 账户地址
        :return: 正常是返回True, 冻结返回False
        """
        if address is None:
            address = self._cc.address
        self._info(f'查询Gas账户状态 {address}')
        return self._cc.get_gas_account_status(address)

    # 13-08 Gas退款
    @with_user_endorsers
    def refund_gas(self, address: str = None, amount: int = None, timeout: int = None,
                   with_sync_result: bool = None) -> dict:
        """
        Gas退款
        :param address: 退款账户地址
        :param amount: 退款金额
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        if address is None:
            address = self._cc.address
        self._info(f'Gas退款 address: {address} amount: {amount}')
        payload = self._cc.create_refund_gas_payload(address, amount)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 12-09 Gas VM退款
    @with_user_endorsers
    def refund_gas_vm(self, address: str, amount: int, timeout: int = None,
                      with_sync_result: bool = None) -> dict:  # todo 待验证
        """

        :param address:
        :param amount:
        :param timeout:
        :param with_sync_result:
        :return:
        """
        self._info(f'GasVM退款 address: {address} amount: {amount}')
        payload = self._cc.create_refund_gas_vm_payload(address, amount)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 13-10 Gas多账户收费
    @with_user_endorsers
    def charge_gas_for_multi_account(self, charge_gas_list: List[tuple],
                                     timeout: int = None, with_sync_result: bool = None):  # todo 待验证
        """

        :param charge_gas_list:
        :param timeout:
        :param with_sync_result:
        :return:
        """
        self._info(f'Gas多账户收费')
        payload = self._cc.create_charge_gas_for_multi_account_payload(charge_gas_list)
        return self._cc.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)


# 14 DPOS共识奖励操作
class DposDistributionOps(BaseOps):
    """DPOS共识奖励操作"""

    # 14-00 奖励
    def reward(self, timeout: int = None, with_sync_result: bool = None) -> dict:  # todo
        """
        奖励
        <14-00-DPOS_DISTRIBUTION-REWARD>
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        raise NotImplementedError("待实现")

    # 14-01 根据世代Id获取奖励
    def get_distribution_by_epoch_id(self, epoch_id: str) -> dict:
        """
        <14-01-DPOS_DISTRIBUTION-GET_DISTRIBUTION_DETAIL>
        :return:
        """
        return self._cc.get_distribution_by_epoch_id(epoch_id)

    # 14-02 设置每个区块奖励数量
    def set_distribution_per_block(self, distribution_per_block: int, timeout: int = None,
                                   with_sync_result: bool = None) -> dict:
        """
        设置每个区块奖励数量
        <14-02-DPOS_DISTRIBUTION-SET_DISTRIBUTION_PER_BLOCK>
        :param distribution_per_block:
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._info("设置每个区块奖励数量为 %d" % distribution_per_block)
        return self._cc.set_distribution_per_block(distribution_per_block, timeout, with_sync_result)

    # 14-03 获取每个区块奖励数量
    def get_distribution_per_block(self) -> int:
        """
        获取每个区块奖励数量
        <14-03-DPOS_DISTRIBUTION-GET_DISTRIBUTION_PER_BLOCK>
        :return:
        """
        self._info("获取每个区块奖励数量")
        return self._cc.get_distribution_per_block()

    # 14-04 设置从惩罚而来的奖励数量
    def set_distribution_from_slashing(self, slashing_per_block: int, timeout: int = None,
                                       with_sync_result: bool = None) -> dict:
        """
        设置惩罚数量
        <14-04-DPOS_DISTRIBUTION-SET_DISTRIBUTION_FROM_SLASHING>
        :param slashing_per_block:
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        raise NotImplementedError("待实现")

    # 14-05 获取从惩罚而来的奖励数量
    def get_distribution_from_slashing(self) -> str:
        """
        <14-05-DPOS_DISTRIBUTION-GET_DISTRIBUTION_FROM_SLASHING>
        :return:
        """
        raise NotImplementedError("待实现")

    # 14-06 设置Gas转换率
    def set_gas_exchange_rate(self, gas_exchange_rate: int, timeout: int = None,
                              with_sync_result: bool = None) -> dict:
        """
        设置Gas转换率
        <14-06-DPOS_DISTRIBUTION-SET_GAS_EXCHANGE_RATE>
        :param gas_exchange_rate:
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._info("设置Gas转换率为 %d" % gas_exchange_rate)
        return self._cc.set_gas_exchange_rate(gas_exchange_rate, timeout, with_sync_result)

    # 14-07 获取Gas转换率
    def get_gas_exchange_rage(self) -> int:
        """
        <14-07-DPOS_DISTRIBUTION-SET_GAS_EXCHANGE_RATE>
        :return:
        """
        self._info("获取Gas转换率")
        return self._cc.get_gas_exchange_rage()


# 15 DPOS共识惩罚操作
class DposSlashingOps(BaseOps):
    """DPOS共识惩罚操作"""

    # 15-00 惩罚
    def punish(self, timeout: int = None, with_sync_result: bool = None) -> dict:  # todo 参数
        """
        惩罚
        <15-00-DPOS_SLASHING-PUNISH>
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        raise NotImplementedError("待实现")

    # 15-02 设置区块惩罚数量
    def set_slashing_per_block(self, slashing_per_block: int, timeout: int = None,
                               with_sync_result: bool = None) -> dict:
        """
        设置区块惩罚数量
        <15-02-DPOS_SLASHING-SET_SLASHING_PER_BLOCK>
         :param slashing_per_block:
         :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._info("设置区块惩罚数量为 %d" % slashing_per_block)
        return self._cc.set_slashing_per_block(slashing_per_block, timeout, with_sync_result)

    # 15-03 获取区块惩罚数量
    def get_slashing_per_block(self) -> int:
        """
        获取区块惩罚数量
        <15-03-DPOS_SLASHING-GET_SLASHING_PER_BLOCK>
        :return:
        """
        self._info("获取区块惩罚数量")
        return self._cc.get_slashing_per_block()

    # 15-04 查询惩罚账户余额
    def get_slashing_balance(self) -> int:
        """
        查询惩罚账户余额
        <15-04-DPOS_SLASHING-GET_SLASHING_ADDRESS_BALANCE>
        :return:
        """
        self._info('查询惩罚账户余额')
        return self._cc.get_slashing_balance()

    # 15-05 通过世代Id获取惩罚数据
    def get_slashing_by_epoch_id(self, epoch_id: str) -> dict:
        """
        通过世代Id获取惩罚数据
        <15-05-DPOS_SLASHING-GET_SLASHING_DETAIL>
        :return:
        """
        self._info('通过世代Id获取惩罚数据')
        return self._cc.get_slashing_by_epoch_id(epoch_id)


class TxPoolOps(BaseOps):
    @with_user_endorsers
    def get_pool_status(self) -> dict:
        """
        获取交易池状态
        :return:
        """
        self._info("获取交易池状态")
        return self._cc.get_pool_status()

    @with_user_endorsers
    def get_tx_ids_by_type_and_stage(self, tx_type: Union[TxType, str, int] = None,
                                     tx_stage: Union[TxStage, str, int] = None) -> List[str]:
        """
        获取不同交易类型和阶段中的交易Id列表。
        :param tx_type: 交易类型 在pb的txpool包中进行了定义
        :param tx_stage: 交易阶段 在pb的txpool包中进行了定义
        :return: 交易Id列表
        """
        self._info(f"获取交易类型 {tx_type} 和阶段 {tx_stage} 中的交易Id列表")
        return self._cc.get_tx_ids_by_type_and_stage(tx_type, tx_stage)

    @with_user_endorsers
    def get_txs_in_pool_by_tx_ids(self, tx_ids: List[str]) -> (List[dict], List[str]):
        """
        根据txIds获取交易池中存在的txs，并返回交易池缺失的tx的txIds
        :param tx_ids: 交易Id列表
        :return: [交易池中存在的txs, 交易池缺失的tx的txIds]
        """
        self._info(f"根据tx_ids {tx_ids} 获取交易池中存在的txs")
        return self._cc.get_txs_in_pool_by_tx_ids(tx_ids)

    def get_tx_status(self, tx_id: str):
        self._info(f"获取交易池中交易 {tx_id} 状态")
        return self._cc.get_tx_status(tx_id)


class ConsensusOps(BaseOps):
    """共识状态操作"""

    def get_consensus_validators(self) -> List[str]:
        """
        获取所有共识节点的身份标识
        :return: 共识节点身份标识
        :exception: 当查询的节点非共识节点时或共识节点内部查询中出现错误，返回error
        """
        self._info("获取所有共识节点的身份标识")
        return self._cc.get_consensus_validators()

    def get_consensus_height(self) -> int:
        """
        获取节点正在共识的区块高度
        :return:
        """
        self._info("获取节点正在共识的区块高度")
        return self._cc.get_consensus_height()

    def get_consensus_state_json(self) -> dict:
        """
        获取共识节点的状态
        :return: 查询的共识节点状态
        """
        self._info("获取共识节点的状态")
        return self._cc.get_consensus_state_json()


class NodeSyncCheckOps(BaseOps):
    def _get_node_clients(self, nodes: List[str] = None):
        if nodes is None:
            nodes = ['node1', 'node2', 'node3', 'node4']
        clients = [self._crypto_config.new_chain_client(conn_node=node) for node in
                   nodes]
        return clients

    def check_block_sync(self, block_heights: list = None, tx_ids: list = None,
                         nodes: list = None):
        nodes = self._get_node_clients(nodes)

        if len(nodes) <= 0:
            raise RuntimeError('无可用节点')

        target_node = nodes[0]
        if block_heights:
            for block_height in block_heights:
                target_node_block_check_key = target_node.get_block_by_height(
                    block_height).block.header
                for i in range(1, len(nodes)):
                    if target_node_block_check_key != nodes[i].get_block_by_height(
                            block_height).block.header:
                        return False
        elif tx_ids:
            for tx_id in tx_ids:
                target_node_block_check_key = target_node.get_block_by_tx_id(tx_id=tx_id).block.header
                for i in range(1, len(nodes)):
                    if target_node_block_check_key != nodes[i].get_block_by_tx_id(tx_id=tx_id).block.header:
                        return False
        else:
            target_node_block_check_key = target_node.get_last_block().block.header
            for i in range(1, len(nodes)):
                if target_node_block_check_key != nodes[i].get_last_block().block.header:
                    return False
        return True

    def check_tx_sync(self, tx_ids: list, nodes: list = None) -> bool:
        """
        检查一批交易结果是否同步
        :param tx_ids: 指定的交易列表
        :param nodes: 指定的节点列表，为None时检查所有节点
        :return: 一致返回True, 不一致返回False
        """
        nodes = self._get_node_clients(nodes)
        if len(nodes) <= 0:
            raise RuntimeError('无可用节点')
        target_node = nodes[0]
        for tx_id in tx_ids:
            target_node_tx_check_key = target_node.get_tx_by_tx_id(tx_id).transaction.result
            for i in range(1, len(nodes)):
                if target_node_tx_check_key != nodes[i].get_tx_by_tx_id(tx_id).transaction.result:
                    return False
        return True

    def check_contract_sync(self, contract_name: str, method: str, params: dict = None,
                            nodes: list = None) -> bool:
        """
        检查多个节点合约查询结果是否一致
        :param contract_name: 合约名称
        :param method: 合约方法
        :param params: 合约参数
        :param nodes: 指定节点列表，，为None时检查所有节点
        :return: 一致返回True, 不一致返回False
        """
        nodes = self._get_node_clients(nodes)
        if len(nodes) <= 0:
            raise RuntimeError('无可用节点')
        target_node = nodes[0]
        target_node_query_contract_result = target_node.query_contract(contract_name, method,
                                                                       params).contractResult.result
        for i in range(1, len(nodes)):
            if target_node_query_contract_result != \
                    nodes[i].query_contract(contract_name, method, params).contractResult.result:
                return False
        return True

    def wait_block_sync(self, timeout: int = 20, interval: int = 1, block_heights: list = None,
                        tx_ids: list = None, nodes: list = None) -> bool:
        """
        等待区块同步
        :param block_heights: 块高度列表，等待多个高度区块同步
        :param tx_ids: 交易列表，等待多笔交易区块同步
        :param nodes: 指定检查的节点列表，列表元素支持节点index，名称或节点对象
        :param timeout: 超时时间，默认20秒
        :param interval: 检查间隔，默认1秒
        :return: 节点区块达到同步状态返回True, 超时未达到同步状态返回False
        """
        start = time.time()
        while 1:
            if time.time() - start > timeout:
                return False
            if self.check_block_sync(block_heights, tx_ids, nodes) is True:
                return True
            time.sleep(interval)


class ChainManager:
    """链管理客户端"""

    def __init__(self, crypto_config: crypto_config_utils.CryptoConfig, server_config: dict = None):
        self.crypto_config = crypto_config
        self.server_config = server_config

        self._cc = crypto_config.new_chain_client()

        self.chain_config = ChainConfigOps(self._cc, self.crypto_config)  # 00
        self.chain_query = ChainQueryOps(self._cc, self.crypto_config)  # 01

        self.cert_manage = CertManageOps(self._cc, self.crypto_config)  # 02
        self.multi_sign = MultiSignOps(self._cc, self.crypto_config)  # 04
        self.contract_manage = ContractManageOps(self._cc, self.crypto_config)  # 05
        
        self.private_compute = PrivateComputeOps(self._cc, self.crypto_config)  # 06

        self.dpos_erc20 = DposErc20Ops(self._cc, self.crypto_config)  # 07
        self.dpos_stake = DposStakeOps(self._cc, self.crypto_config)  # 08
        self.subscribe_manage = SubscribeManageOps(self._cc, self.crypto_config)  # 09
        self.archive_manage = ArchiveManageOps(self._cc, self.crypto_config)  # 10
        self.pubkey_manage = PubkeyManageOps(self._cc, self.crypto_config)  # 12
        self.account_manager = AccountManagerOps(self._cc, self.crypto_config)  # 13
        self.dpos_slashing = DposSlashingOps(self._cc, self.crypto_config)  # 15
        self.dpos_distribution = DposDistributionOps(self._cc, self.crypto_config)

        self.txpool = TxPoolOps(self._cc, self.crypto_config)
        self.consensus = ConsensusOps(self._cc, self.crypto_config)

        self.node_sync = NodeSyncCheckOps(self._cc, self.crypto_config)

        self.cmc = cmc_utils.Cmc(auth_type=self._cc.auth_type)

        self._cluster = None

    @property
    def cluster(self) -> Union[server_utils.ChainMakerCluster, None]:
        if self._cluster is None and self.server_config:
            self._cluster = server_utils.ChainMakerCluster.from_conf(self.server_config)
        return self._cluster

    @classmethod
    def from_host_conf(cls, host_config: dict, crypto_config_path: str = './crypto-config',
                       rpc_start_port: int = 12301):
        host = Host(**host_config)  # todo local
        chainmaker_go_path = f'{host.workspace}/chainmaker-go'
        if not os.path.exists(crypto_config_path):
            host.get_dir(f'{chainmaker_go_path}/build/crypto-config', crypto_config_path)
        return cls.from_crypto_config(crypto_config_path, host=host_config['host'],
                                      rpc_start_port=rpc_start_port, server_config=dict(host=host_config))

    @classmethod
    def from_crypto_config(cls, crypto_config_path: Union[Path, str], host: str, rpc_start_port: int = 12301,
                           server_config: dict = None):
        crypto_config = crypto_config_utils.load_crypto_config(crypto_config_path, host=host,
                                                               rpc_start_port=rpc_start_port)
        return cls(crypto_config=crypto_config, server_config=server_config)
