#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   chain_config.py
# @Function     :   ChainMaker 链配置接口
import json
import warnings
from typing import List, Union, Dict

from chainmaker.apis.base_client import BaseClient
from chainmaker.exceptions import InvalidParametersError
from chainmaker.keys import (AddrType, ParamKey, PolicyRule, ResourceName, PolicyRole, ConsensusType, Role, Rule,
                             AuthType)
from chainmaker.keys import SystemContractName, ChainConfigMethod
from chainmaker.protos.accesscontrol.policy_pb2 import Policy
from chainmaker.protos.common.request_pb2 import EndorsementEntry, Payload
from chainmaker.protos.common.result_pb2 import TxResponse
from chainmaker.protos.config.chain_config_pb2 import ChainConfig, ResourcePolicy
from chainmaker.utils.common import (ensure_enum, ensure_str, ensure_list_str)


class _TrustRootMixIn(BaseClient):
    """链配置-信任组织根证书管理操作"""

    # 00-04 创建信任组织根证书添加待签名Payload
    def create_chain_config_trust_root_add_payload(self, trust_root_org_id: str,
                                                   trust_root_crts: List[str]) -> Payload:
        """
        创建信任组织根证书添加待签名Payload
         <00-04-CHAIN_CONFIG-TRUST_ROOT_ADD>
        :param str trust_root_org_id: 组织Id  eg. 'wx-or5.chainmaker.org'
        :param List[str] trust_root_crts: 根证书文件内容列表
           eg. [open('./testdata/crypto-config/wx-org5.chainmaker.org/ca/ca.crt').read()]
        :return: 待签名Payload
        :raises RequestError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-TRUST_ROOT_ADD] to be signed payload")
        params = {
            ParamKey.org_id.name: str(trust_root_org_id),
            ParamKey.root.name: ','.join(trust_root_crts)
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.TRUST_ROOT_ADD.name, params)

    # 00-05 创建信任组织根证书更新待签名Payload
    def create_chain_config_trust_root_update_payload(self, trust_root_org_id: str,
                                                      trust_root_crts: List[str]) -> Payload:
        """
        创建信任组织根证书更新待签名Payload
         <00-05-CHAIN_CONFIG-TRUST_ROOT_UPDATE>
        :param str trust_root_org_id: 组织Id
        :param List[str] trust_root_crts: 根证书内容列表
        :return: 待签名Payload
        :raises RequestError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-TRUST_ROOT_UPDATE] to be signed payload")

        params = {
            ParamKey.org_id.name: str(trust_root_org_id),
            ParamKey.root.name: ','.join(trust_root_crts)
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.TRUST_ROOT_UPDATE.name, params)

    # 00-06 创建信任组织根证书删除待签名Payload
    def create_chain_config_trust_root_delete_payload(self, org_id: str) -> Payload:
        """
        创建信任组织根证书删除待签名Payload
        <00-06-CHAIN_CONFIG-TRUST_ROOT_DELETE>
        :param org_id: 组织Id
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-TRUST_ROOT_DELETE] to be signed payload")

        params = {
            ParamKey.org_id.name: str(org_id),
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.TRUST_ROOT_DELETE.name, params)


class _NodeAddrMixIn(BaseClient):  # todo
    """链配置-共识节点地址管理操作"""

    # 00-07 创建链配置节点地址添加待签名Payload
    def create_chain_config_node_addr_add_payload(self, org_id: str, node_addrs: List[str]) -> Payload:
        """
        创建链配置节点地址添加待签名Payload
        <00-07-CHAIN_CONFIG-NODE_ADDR_ADD>
        :param org_id: 节点组织Id
        :param node_addrs: 节点地址列表
        :return: 待签名Payload
        """
        self._debug("begin to create [CHAIN_CONFIG-NODE_ADDR_ADD] to be signed payload")
        params = {
            ParamKey.org_id.name: org_id,
            ParamKey.node_addrs.name: ",".join(node_addrs),
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.NODE_ADDR_ADD.name, params)

    # 00-08 创建链配置节点地址更新待签名Payload
    def create_chain_config_node_addr_update_payload(self, org_id: str, node_old_addr: str,
                                                     node_new_addr: str) -> Payload:  # todo
        """
        创建链配置节点地址更新待签名Payload
        <00-08-CHAIN_CONFIG-NODE_ADDR_UPDATE>
        :param org_id: 节点组织Id
        :param node_old_addr: 原节点地址
        :param node_new_addr: 新节点地址
        :return: 待签名Payload
        """
        self._debug("begin to create [CHAIN_CONFIG-NODE_ADDR_UPDATE] to be signed payload")
        params = {
            ParamKey.org_id.name: org_id,
            ParamKey.node_addr.name: node_old_addr,
            ParamKey.new_node_addr.name: node_new_addr,
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.NODE_ADDR_UPDATE.name, params)

    # 00-09 创建链配置节点地址删除待签名Payload
    def create_chain_config_node_addr_delete_payload(self, org_id: str, node_addr: str) -> Payload:  # todo
        """
        创建链配置节点地址删除待签名Payload
        <00-09-CHAIN_CONFIG-NODE_ADDR_DELETE>
        :param org_id: 节点组织Id
        :param node_addr: 节点地址
        :return: 待签名Payload
        """
        self._debug("begin to create [CHAIN_CONFIG-NODE_ADDR_DELETE] to be signed payload")
        params = {
            ParamKey.org_id.name: org_id,
            ParamKey.node_addr.name: node_addr,
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.NODE_ADDR_DELETE.name, params)


class _NodeOrgMixIn(BaseClient):
    """链配置-共识组织管理操作"""

    # 00-10 创建链配置共识组织添加待签名Payload
    def create_chain_config_consensus_node_org_add_payload(self, node_org_id: str,
                                                           node_ids: List[str]) -> Payload:
        """
        创建链配置共识组织添加待签名Payload
        <00-10-CHAIN_CONFIG-NODE_ORG_ADD>
        :param node_org_id: 节点组织Id
        :param node_ids: 节点Id
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-NODE_ORG_ADD] to be signed payload")

        params = {
            ParamKey.org_id.name: node_org_id,
            ParamKey.node_ids.name: ",".join(node_ids),
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.NODE_ORG_ADD.name, params)

    # 00-11 创建链配置共识节点更新待签名Payload
    def create_chain_config_consensus_node_org_update_payload(self, node_org_id: str,
                                                              node_ids: List[str]) -> Payload:
        """
        创建链配置共识节点更新待签名Payload
        <00-11-CHAIN_CONFIG-NODE_ORG_UPDATE>
        :param node_org_id: 节点组织Id
        :param node_ids: 节点Id
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-NODE_ORG_UPDATE] to be signed payload")
        params = {
            ParamKey.org_id.name: node_org_id,
            ParamKey.node_ids.name: ",".join(node_ids),
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.NODE_ORG_UPDATE.name, params)

    # 00-12 创建链配置共识节点删除待签名Payload
    def create_chain_config_consensus_node_org_delete_payload(self, node_org_id: str) -> Payload:
        """
        创建链配置共识节点删除待签名Payload
        <00-12-CHAIN_CONFIG-NODE_ORG_DELETE>
        :param node_org_id: 节点组织Id
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-NODE_ORG_DELETE] to be signed payload")
        params = {
            ParamKey.org_id.name: node_org_id,
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.NODE_ORG_DELETE.name, params)


class _ConsensusExtMixIn(BaseClient):
    """链配置-共识扩展参数管理操作"""

    # 00-13 创建链配置共识扩展参数添加待签名Payload
    def create_chain_config_consensus_ext_add_payload(self, params: dict) -> Payload:
        """
        创建链配置共识扩展参数添加待签名Payload
        <00-13-CHAIN_CONFIG-CONSENSUS_EXT_ADD>
        :param params: 字段key、value对
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-CONSENSUS_EXT_ADD] to be signed payload")

        return self._create_chain_config_manage_payload(ChainConfigMethod.CONSENSUS_EXT_ADD.name, params)

    # 00-14 创建链配置共识扩展参数更新待签名Payload
    def create_chain_config_consensus_ext_update_payload(self, params: dict) -> Payload:
        """
        创建链配置共识扩展参数更新待签名Payload
        <00-14-CHAIN_CONFIG-CONSENSUS_EXT_UPDATE>
        :param params: 字段key、value对
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-CONSENSUS_EXT_UPDATE] to be signed payload")

        return self._create_chain_config_manage_payload(ChainConfigMethod.CONSENSUS_EXT_UPDATE.name, params)

    # 00-15 创建链配置删除共识扩展参数删除待签名Payload
    def create_chain_config_consensus_ext_delete_payload(self, keys: List[str]) -> Payload:
        """
        创建链配置删除共识扩展参数删除待签名Payload
        <00-15-CHAIN_CONFIG-CONSENSUS_EXT_DELETE>
        :param keys: 待删除字段
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-CONSENSUS_EXT_DELETE] to be signed payload")
        params = {key: "" for key in keys}
        return self._create_chain_config_manage_payload(ChainConfigMethod.CONSENSUS_EXT_DELETE.name, params)


class _PermissionMixIn(BaseClient):
    """链配置-权限配置管理操作"""

    # 00-16 创建链配置权限配置添加待签名Payload
    def create_chain_config_permission_add_payload(self, permission_resource_name: Union[ResourceName, str],
                                                   policy: Policy) -> Payload:
        """
        创建链配置权限配置添加待签名Payload
        <00-16-CHAIN_CONFIG-PERMISSION_ADD>
        :param permission_resource_name: 权限名
        :param policy: 权限规则
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        if isinstance(permission_resource_name, ResourceName):
            permission_resource_name = permission_resource_name.name
        self._debug("begin to create [CHAIN_CONFIG-PERMISSION_ADD] to be signed payload")
        params = {
            permission_resource_name: policy.SerializeToString(),
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.PERMISSION_ADD.name, params)

    # 00-17 创建链配置权限配置更新待签名Payload
    def create_chain_config_permission_update_payload(self, permission_resource_name: Union[ResourceName, str],
                                                      policy: Policy) -> Payload:  # todo policy->dict
        """
        创建链配置权限配置更新待签名Payload
        <00-17-CHAIN_CONFIG-PERMISSION_UPDATE>
        :param permission_resource_name: 权限名
        :param policy: 权限规则
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        permission_resource_name = ensure_str(permission_resource_name)

        self._debug("begin to create [CHAIN_CONFIG-PERMISSION_UPDATE] to be signed payload")

        params = {
            permission_resource_name: policy.SerializeToString(),
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.PERMISSION_UPDATE.name, params)

    # 00-18 创建权限配置删除待签名Payload
    def create_chain_config_permission_delete_payload(self,
                                                      permission_resource_name: Union[ResourceName, str]) -> Payload:
        """
        创建权限配置删除待签名Payload
        <00-18-CHAIN_CONFIG-PERMISSION_DELETE>
        :param permission_resource_name: 权限名
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        if isinstance(permission_resource_name, ResourceName):
            permission_resource_name = permission_resource_name.name
        self._debug("begin to create [CHAIN_CONFIG-PERMISSION_DELETE] to be signed payload")
        params = {
            permission_resource_name: "",
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.PERMISSION_DELETE.name, params)

    # 00-29 获取链配置权限列表
    def get_chain_config_permission_list(self) -> ResourcePolicy:
        """
        获取链配置权限列表
        <00-29-CHAIN_CONFIG-PERMISSION_LIST>
        :return: 权限列表
        """
        self._debug("begin to get chain config permission list")
        payload = self._payload_builder.create_query_payload(SystemContractName.CHAIN_CONFIG.name,
                                                             ChainConfigMethod.PERMISSION_LIST.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        chain_config = ChainConfig()
        chain_config.ParseFromString(data)
        return chain_config.resource_policies

    @staticmethod
    def create_policy(rule: Union[PolicyRule, str], org_list: List[str] = None, role_list: List[PolicyRole] = None):
        rule = ensure_str(rule)
        role_list = ensure_list_str(role_list) if role_list else None

        return Policy(
            rule=rule,
            org_list=org_list,
            role_list=role_list
        )


class _NodeIdMixIn(BaseClient):
    """链配置-共识节点Id管理操作"""

    # 00-19 创建链配置共识节点Id添加待签名Payload
    def create_chain_config_consensus_node_id_add_payload(self, org_id: str, node_ids: List[str]) -> Payload:
        """
        创建链配置共识节点Id添加待签名Payload
        <00-19-CHAIN_CONFIG-NODE_ID_ADD>
        :param org_id: 节点组织Id eg. 'wx-org5.chainmaker.org'
        :param node_ids: 节点Id列表 eg. ['QmcQHCuAXaFkbcsPUj7e37hXXfZ9DdN7bozseo5oX4qiC4']
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-NODE_ID_ADD] to be signed payload")
        params = {
            ParamKey.org_id.name: org_id,
            ParamKey.node_ids.name: ",".join(node_ids),
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.NODE_ID_ADD.name, params)

    # 00-20 创建链配置共识节点Id更新待签名Payload
    def create_chain_config_consensus_node_id_update_payload(self, org_id: str, node_old_id: str,
                                                             node_new_id: str) -> Payload:
        """
        创建链配置共识节点Id更新待签名Payload
        <00-20-CHAIN_CONFIG-NODE_ID_UPDATE>
        :param org_id: 节点组织Id
        :param node_old_id: 节点原Id
        :param node_new_id: 节点新Id
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-NODE_ID_UPDATE] to be signed payload")
        params = {
            ParamKey.org_id.name: org_id,
            ParamKey.node_id.name: node_old_id,
            ParamKey.new_node_id.name: node_new_id,
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.NODE_ID_UPDATE.name, params)

    # 00-21 创建链配置共识节点Id删除待签名Payload
    def create_chain_config_consensus_node_id_delete_payload(self, node_org_id: str,
                                                             node_id: str) -> Payload:
        """
        创建链配置共识节点Id删除待签名Payload
         <00-21-CHAIN_CONFIG-NODE_ID_DELETE>
        :param node_org_id: 节点组织Id
        :param node_id: 节点Id
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-NODE_ID_DELETE] to be signed payload")

        params = {
            ParamKey.org_id.name: node_org_id,
            ParamKey.node_id.name: node_id
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.NODE_ID_DELETE.name, params)

    # 00-32 创建链配置DPOS共识节点Id更新待签名Payload
    def create_chain_config_dpos_node_id_update_payload(self, node_ids: List[str]) -> Payload:
        """
        创建链配置DPOS共识节点Id更新待签名Payload
        <00-32-CHAIN_CONFIG-DPOS_NODE_ID_UPDATE>
        :param node_ids: 节点Id列表
        :return: 待签名Payload
        """
        self._debug("begin to create [CHAIN_CONFIG-DPOS_NODE_ID_UPDATE] to be signed payload")
        params = {
            ParamKey.node_ids.name: node_ids
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.DPOS_NODE_ID_UPDATE.name, params)


class _TrustMemberMixIn(BaseClient):
    """链配置-信任第三方管理操作"""

    # 00-22 创建链配置信任三方添加待签名Payload
    def create_chain_config_trust_member_add_payload(self, trust_member_org_id: str, trust_member_node_id: str,
                                                     trust_member_info: str, trust_member_role: str,
                                                     ) -> Payload:
        """
        创建链配置信任三方添加待签名Payload
         <00-22-CHAIN_CONFIG-TRUST_MEMBER_ADD>
        :param trust_member_org_id: 组织Id
        :param trust_member_node_id: 节点ID
        :param trust_member_info: 节点信息
        :param trust_member_role: 节点角色
        :return: 待签名Payload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-TRUST_MEMBER_ADD] to be signed payload")
        params = {
            ParamKey.org_id.name: trust_member_org_id,
            ParamKey.node_id.name: trust_member_node_id,
            ParamKey.member_info.name: trust_member_info,
            ParamKey.role.name: trust_member_role,
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.TRUST_MEMBER_ADD.name, params)

    # 00-23 创建链配置信任三方更新待签名Payload
    def create_chain_config_trust_member_update_payload(self, trust_member_org_id: str, trust_member_node_id: str,
                                                        trust_member_info: str, trust_member_role: str,
                                                        ) -> Payload:
        """
        创建链配置信任三方更新待签名Payload
         <00-23-CHAIN_CONFIG-TRUST_MEMBER_UPDATE>
        :param trust_member_org_id: 组织Id
        :param trust_member_node_id: 节点ID
        :param trust_member_info: 节点信息
        :param trust_member_role: 节点角色
        :return: 待签名Payload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-TRUST_MEMBER_UPDATE] to be signed payload")
        params = {
            ParamKey.org_id.name: trust_member_org_id,
            ParamKey.node_id.name: trust_member_node_id,
            ParamKey.member_info.name: trust_member_info,
            ParamKey.role.name: trust_member_role,
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.TRUST_MEMBER_UPDATE.name, params)

    # 00-24 创建链配置创建信任三方删除待签名Payload
    def create_chain_config_trust_member_delete_payload(self, trust_member_info: str) -> Payload:
        """
        创建链配置创建信任三方删除待签名Payload
         <00-24-CHAIN_CONFIG-TRUST_MEMBER_DELETE>
        :param trust_member_info: 节点证书信息
        :return: 待签名Payload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-TRUST_MEMBER_DELETE] to be signed payload")
        params = {
            ParamKey.member_info.name: trust_member_info,
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.TRUST_MEMBER_DELETE.name, params)


class _GasMixIn(BaseClient):
    """链配置-Gas管理操作"""

    # 00-26 创建链配置切换启用禁用Gas待签名Payload
    def create_chain_config_enable_or_disable_gas_payload(self) -> Payload:
        """
        创建链配置切换启用禁用Gas待签名Payload
        <0026 CHAIN_CONFIG-ENABLE_OR_DISABLE_GAS>
        :return: 待签名Payload
        """
        self._debug("begin to create [EnableOrDisable] to be signed payload")
        return self._create_chain_config_manage_payload(ChainConfigMethod.ENABLE_OR_DISABLE_GAS.name)

    # 00-27 创建链配置设置合约调用基础Gas消耗待签名Payload
    def create_chain_config_set_invoke_base_gas_payload(self, amount: int) -> Payload:
        """
        创建链配置设置合约调用基础Gas消耗待签名Payload
        <00-27 CHAIN_CONFIG-SET_INVOKE_BASE_GAS>
        :param amount: 设置待基础Gas消耗数量
        :return: 待签名Payload
        """
        self._debug("begin CreateSetInvokeBaseGasPayload")
        assert isinstance(amount, int) and amount >= 0, '[Sdk] amount should be int and >= 0'
        params = {ParamKey.set_invoke_base_gas.name: amount}  # todo test
        return self._create_chain_config_manage_payload(ChainConfigMethod.SET_INVOKE_BASE_GAS.name, params)

    # 00-28 创建链配置设置账户管理员Payload
    def create_chain_config_set_account_manager_admin_payload(self, address) -> Payload:
        """
        创建链配置设置账户管理员Payload
        <00-28 CHAIN_CONFIG-SET_ACCOUNT_MANAGER_ADMIN>
        :return: 待签名Payload
        """
        self._debug("begin to create [SetAccountManagerAdmin] to be signed payload")
        params = {ParamKey.address_key.name: address}
        return self._create_chain_config_manage_payload(ChainConfigMethod.SET_ACCOUNT_MANAGER_ADMIN.name, params)

    def create_chain_config_optimize_charge_gas_payload(self, enable: bool) -> Payload:  # fixme
        """
        开启或关闭链配置的Gas优化待签名Payload
        :param enable: 是否启用
        :return: 待签名Payload
        """
        self._debug("begin to create [ChainConfigOptimizeChargeGas] to be signed payload")
        params = {
            ParamKey.enable_optimize_charge_gas.name: enable
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.CORE_UPDATE.name, params)

    def create_set_invoke_base_gas_payload(self, amount: int) -> Payload:  # todo remove
        """
        创建设置invoke基础Gas消耗待签名Payload
        :param amount: 设置待基础Gas消耗数量
        :return: 待签名Payload
        """
        warnings.warn('please use create_chain_config_set_invoke_base_gas_payload instead', DeprecationWarning)
        self._debug("begin CreateSetInvokeBaseGasPayload")
        return self.create_chain_config_set_invoke_base_gas_payload(amount)


class ChainConfigMixIn(_TrustRootMixIn, _NodeAddrMixIn, _NodeOrgMixIn, _ConsensusExtMixIn, _PermissionMixIn,
                       _NodeIdMixIn, _TrustMemberMixIn, _GasMixIn):
    """链配置操作"""

    def _get_chain_config(self) -> ChainConfig:
        """
        获取链配置
        <00-00-CHAIN_CONFIG-GET_CHAIN_CONFIG>
        :return: ChainConfig
        :raises RequestError: 请求失败
        """
        payload = self._payload_builder.create_query_payload(SystemContractName.CHAIN_CONFIG.name,
                                                             ChainConfigMethod.GET_CHAIN_CONFIG.name)
        response = self.send_request(payload)

        data = response.contract_result.result
        chain_config = ChainConfig()
        chain_config.ParseFromString(data)

        return chain_config

    # 00-00 获取链配置
    def get_chain_config(self) -> ChainConfig:
        """
        获取链配置
        <00-00-CHAIN_CONFIG-GET_CHAIN_CONFIG>
        :return: ChainConfig
        :raises RequestError: 请求失败
        """
        self._debug("begin to get chain config")
        return self._get_chain_config()

    # 00-01 通过指定区块高度查询最近链配置
    def get_chain_config_by_block_height(self, block_height: int) -> ChainConfig:
        """
        通过指定区块高度查询最近链配置
        如果当前区块就是配置块，直接返回当前区块的链配置
        <00-01-CHAIN_CONFIG-GET_CHAIN_CONFIG_AT>
        :param block_height: 块高
        :return: ChainConfig
        :raises RequestError: 请求失败
        """
        self._debug("begin to get chain config by block height [%s]" % block_height)
        if self.archive_center_query_first is True:
            try:
                return self.archive_service.get_chain_config_by_block_height(block_height)
            except Exception as ex:
                self._logger.exception(ex)

        params = {ParamKey.block_height.name: block_height}
        payload = self._create_chain_config_manage_payload(ChainConfigMethod.GET_CHAIN_CONFIG_AT.name, params)
        response = self.send_request(payload)

        data = response.contract_result.result
        chain_config = ChainConfig()
        chain_config.ParseFromString(data)

        return chain_config

    # 00-02 创建链配置Core配置更新待签名Payload
    def create_chain_config_core_update_payload(self, tx_scheduler_timeout: int = None,
                                                tx_scheduler_validate_timeout: int = None) -> Payload:
        """
        创建链配置Core配置更新待签名Payload
        <00-02-CHAIN_CONFIG-CORE_UPDATE>
        :param tx_scheduler_timeout: 交易调度器从交易池拿到交易后, 进行调度的时间，其值范围为[0, 60]，若无需修改，请置为-1
        :param tx_scheduler_validate_timeout: 交易调度器从区块中拿到交易后, 进行验证的超时时间，其值范围为[0, 60]，若无需修改，请置为-1
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-CORE_UPDATE] to be signed payload")

        if tx_scheduler_timeout and tx_scheduler_timeout > 60:
            raise InvalidParametersError("[tx_scheduler_timeout] should be [0,60]")
        if tx_scheduler_validate_timeout and tx_scheduler_validate_timeout > 60:
            raise InvalidParametersError("[tx_scheduler_validate_timeout] should be [0,60]")

        if tx_scheduler_timeout < 0 and tx_scheduler_validate_timeout < 0:
            raise InvalidParametersError("update nothing")

        params = {}
        if tx_scheduler_timeout:
            params[ParamKey.tx_scheduler_timeout.name] = tx_scheduler_timeout
        if tx_scheduler_validate_timeout:
            params[ParamKey.tx_scheduler_validate_timeout.name] = tx_scheduler_validate_timeout

        return self._create_chain_config_manage_payload(ChainConfigMethod.CORE_UPDATE.name, params)

    # 00-03 创建链配置区块配置更新待签名Payload
    def create_chain_config_block_update_payload(self, tx_timestamp_verify: bool = None, tx_timeout: int = None,
                                                 block_tx_capacity: int = None, block_size: int = None,
                                                 block_interval: int = None, tx_parameter_size=None) -> Payload:
        """
        创建链配置区块配置更新待签名Payload
        <00-03-CHAIN_CONFIG-BLOCK_UPDATE>
        :param tx_timestamp_verify: 是否需要开启交易时间戳校验
        :param tx_timeout: 交易时间戳的过期时间(秒)，其值范围为[600, +∞)（若无需修改，请置为-1）
        :param block_tx_capacity: 区块中最大交易数，其值范围为(0, +∞]（若无需修改，请置为-1）
        :param block_size: 区块最大限制，单位MB，其值范围为(0, +∞]（若无需修改，请置为-1）
        :param block_interval: 出块间隔，单位:ms，其值范围为[10, +∞]（若无需修改，请置为-1）
        :param tx_parameter_size: 交易参数大小
        :return: request_pb2.SystemContractPayload
        :raises InvalidParametersError: 无效参数
        """
        self._debug("begin to create [CHAIN_CONFIG-BLOCK_UPDATE] to be signed payload")

        if tx_timeout and tx_timeout < 600:
            raise InvalidParametersError("[tx_timeout] should be [600, +∞)")
        if block_tx_capacity and block_tx_capacity < 1:
            raise InvalidParametersError("[block_tx_capacity] should be (0, +∞]")
        if block_size and block_size < 1:
            raise InvalidParametersError("[block_size] should be (0, +∞]")
        if block_interval and block_interval < 10:
            raise InvalidParametersError("[block_interval] should be [10, +∞]")
        if tx_parameter_size and tx_parameter_size < 1:
            raise InvalidParametersError("[tx_parameter_size] should be (0, +∞]")

        params = {}
        if tx_timestamp_verify is not None:
            params[ParamKey.tx_timestamp_verify.name] = tx_timestamp_verify
        if tx_timeout:
            params[ParamKey.tx_timeout.name] = tx_timeout
        if block_tx_capacity:
            params[ParamKey.block_tx_capacity.name] = block_tx_capacity
        if block_size:
            params[ParamKey.block_size.name] = block_size
        if block_interval:
            params[ParamKey.block_interval.name] = block_interval
        if tx_parameter_size:
            params[ParamKey.tx_parameter_size.name] = tx_parameter_size

        return self._create_chain_config_manage_payload(ChainConfigMethod.BLOCK_UPDATE.name, params)

    # 00-25 创建链配置变更地址类型待签名Payload
    def create_chain_config_alter_addr_type_payload(self, addr_type: Union[AddrType, str, int]) -> Payload:
        """
        创建链配置变更地址类型待签名Payload
        <00-25-CHAIN_CONFIG-ALTER_ADDR_TYPE>
        :param addr_type: 地址类型
        :return: 待签名Payload
        """
        addr_type = ensure_enum(addr_type, AddrType)
        # assert addr_type in [0, 1, 2], "addr type only support: 0-ChainMaker; 1-ZXL; 2-ETHEREUM"
        self._debug("begin to create [CHAIN_CONFIG-ALTER_ADDR_TYPE] to be signed payload")

        params = {ParamKey.addr_type.name: addr_type.value}
        return self._create_chain_config_manage_payload(ChainConfigMethod.ALTER_ADDR_TYPE.name, params)

    # 00-30 创建链配置版本更新待签名Payload
    def create_chain_config_update_version_payload(self, block_version: str) -> Payload:
        """
        创建链配置版本更新待签名Payload
        <00-30-CHAIN_CONFIG-UPDATE_VERSION>
        :return: 待签名Payload
        """
        self._debug("begin to create [CHAIN_CONFIG-UPDATE_VERSION] to be signed payload")
        params = {ParamKey.block_version.name: block_version}
        return self._create_chain_config_manage_payload(ChainConfigMethod.UPDATE_VERSION.name, params)

    # 00-31 创建链配置版本更新待签名Payload
    def create_chain_config_consensus_switch_payload(self, origin_consensus: Union[ConsensusType, str, int],
                                                     target_consensus: Union[ConsensusType, str, int],
                                                     ext_config: dict) -> Payload:
        """
        创建链配置版本更新待签名Payload
        <00-31-CHAIN_CONFIG-CONSENSUS_SWITCH>
        :param origin_consensus:
        :param target_consensus:
        :param ext_config:
        :return: 待签名Payload
        """
        _from = ensure_enum(origin_consensus, ConsensusType).value
        _to = ensure_enum(target_consensus, ConsensusType).value
        self._debug("begin to create [CHAIN_CONFIG-CONSENSUS_SWITCH] to be signed payload")
        params = {
            ParamKey._from.value: _from,
            ParamKey.to.name: _to,
            ParamKey.ext_config.name: json.dumps(ext_config),
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.CONSENSUS_SWITCH.name, params)

    def create_chain_config_enable_multi_sign_manual_run_payload(self, enable: bool = True) -> Payload:
        """
        创建链配置多签手动运行待签名Payload
        :param enable: 是否启用多签手动运行
        :return: 待签名Payload
        """
        self._debug('begin to create [CHAIN_CONFIG-MULTI_SIGN_ENABLE_MANUAL_RUN] to be signed payload')
        params = {
            ParamKey.multi_sign_enable_manual_run.name: enable
        }
        return self._create_chain_config_manage_payload(ChainConfigMethod.MULTI_SIGN_ENABLE_MANUAL_RUN.name, params)

    def create_tbft_to_raft_payload(self, ext_config: dict) -> Payload:
        """
        生成链配置更新链配置版本Payload
        :return: 待签名Payload
        """
        self._debug("begin to create [TbftToRaft] to be signed payload")
        return self.create_chain_config_consensus_switch_payload(ConsensusType.TBFT, ConsensusType.RAFT, ext_config)

    def create_raft_to_tbft_payload(self, ext_config: dict) -> Payload:
        """
        生成链配置更新链配置版本Payload
        :return: 待签名Payload
        """
        self._debug("begin to create [RaftToTbft] to be signed payload")
        return self.create_chain_config_consensus_switch_payload(ConsensusType.RAFT, ConsensusType.TBFT, ext_config)

    def sign_chain_config_payload(self, payload_bytes: bytes) -> Payload:
        """
        对链配置的Payload进行签名
        如果当前区块就是配置块，直接返回当前区块的链配置
        :param payload_bytes: payload.SerializeToString() 序列化后的payload bytes数据
        :return: 签名的背书
        :raises
        """
        return self.user.sign(payload_bytes)

    def send_chain_config_update_request(self, payload: Payload, endorsers: List[EndorsementEntry], timeout: int = None,
                                         with_sync_result: bool = None) -> TxResponse:
        """
        发送链配置更新请求
        :param payload: 待签名链配置更新请求Payload
        :param endorsers: 背书列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮交易结果
        :return: 交易响应信息
        """
        response = self.send_request_with_sync_result(payload, endorsers=endorsers,
                                                      timeout=timeout, with_sync_result=with_sync_result)
        setattr(self, '_cached_chain_config', None)
        return response

    def _get_chain_config_sequence(self) -> int:
        """
        获取最新链配置序号
        :return: 最新配置序号
        :raises RequestError: 请求失败
        """
        # self._debug("begin to get chain config sequence")
        chain_config = self._get_chain_config()
        return int(chain_config.sequence)

    def _create_chain_config_manage_payload(self, method: str,
                                            params: Dict[str, Union[str, int, bool]] = None) -> Payload:
        """创建链配置管理(更新)待签名Payload"""
        seq = self._get_chain_config_sequence()
        return self._payload_builder.create_invoke_payload(SystemContractName.CHAIN_CONFIG.name, method, params,
                                                           seq=seq + 1)

    def create_chain_config_enable_only_creator_update_payload(self) -> Payload:
        """
        创建链配置启用仅允许创建者升级合约待签名Payload
        v2.3.2 新增
        :return:
        """
        self._debug(
            "begin to create [ENABLE_ONLY_CREATOR_UPGRADE] to be signed payload"
        )
        params = {}
        return self._create_chain_config_manage_payload(
            ChainConfigMethod.ENABLE_ONLY_CREATOR_UPGRADE.name, params
        )

    def create_chain_config_disable_only_creator_update_payload(self) -> Payload:
        """
        创建链配置关闭仅允许创建者升级合约待签名Payload
        v2.3.2 新增
        :return:
        """
        self._debug(
            "begin to create [DISABLE_ONLY_CREATOR_UPGRADE] to be signed payload"
        )
        params = {}
        return self._create_chain_config_manage_payload(
            ChainConfigMethod.DISABLE_ONLY_CREATOR_UPGRADE.name, params
        )


class ChainConfigWithEndorsers(BaseClient):
    # 00-02 更新链配置Core配置
    def chain_config_core_update(self, tx_scheduler_timeout: int = None, tx_scheduler_validate_timeout: int = None,
                                 timeout: int = None, with_sync_result: bool = None) -> TxResponse:
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
        self._debug(f'begin to update chain config core [tx_scheduler_timeout:{tx_scheduler_timeout}]/'
                    f'[tx_scheduler_validate_timeout:{tx_scheduler_validate_timeout}]')
        payload = self.create_chain_config_core_update_payload(tx_scheduler_timeout, tx_scheduler_validate_timeout)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-03 更新链配置区块配置
    def chain_config_block_update(self, tx_timestamp_verify: bool = None, tx_timeout: int = None,
                                  block_tx_capacity: int = None,
                                  block_size: int = None, block_interval: int = None, tx_parameter_size: int = None,
                                  timeout: int = None, with_sync_result: bool = None) -> TxResponse:
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
        self._debug(f'begin to update chain config block [tx_timestamp_verify:{tx_timestamp_verify}]'
                    f'/[tx_timeout:{tx_timeout}]/'
                    f'[block_tx_capacity:{block_tx_capacity}]/[block_size:{block_size}]'
                    f'/[block_interval:{block_interval}]')
        payload = self.create_chain_config_block_update_payload(tx_timestamp_verify, tx_timeout, block_tx_capacity,
                                                                block_size, block_interval, tx_parameter_size)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def chain_config_trust_root_check(self, org_id: str, trust_root_crt: str = None) -> bool:
        """
        检查信任组织根证书是否上链
        :param org_id: 组织Id
        :param trust_root_crt: 信任根证书
        :return:
        """
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to check trust root [org_id:%s]' % org_id)
        trust_roots = self.chain_config.trust_roots

        trust_root_orgs = [item.org_id for item in trust_roots]
        if org_id in trust_root_orgs:
            trust_root_crts = []
            for item in trust_roots:
                trust_root_crts.extend(item.root)
            if trust_root_crt in trust_root_crts:
                return True
        return False

    # 00-04 添加信任组织根证书
    def chain_config_trust_root_add(self, org_id: str, trust_root_crts: List[str],
                                    timeout: int = None, with_sync_result: bool = None) -> TxResponse:
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
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug("begin to add trust root [org_id:%s]" % org_id)
        payload = self.create_chain_config_trust_root_add_payload(org_id, trust_root_crts)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-05 更新信任组织根证书
    def chain_config_trust_root_update(self, org_id: str, trust_root_crts: List[str],
                                       timeout: int = None, with_sync_result: bool = None) -> TxResponse:
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
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug("begin to update trust root [org_id:%s]" % org_id)
        payload = self.create_chain_config_trust_root_update_payload(org_id, trust_root_crts)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-06 删除信任组织根证书
    def chain_config_trust_root_delete(self, org_id: str,
                                       timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        删除信任组织根证书
        <00-06-CHAIN_CONFIG-TRUST_ROOT_DELETE>
        :param str org_id: 组织Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug("begin to delete trust root [org_id:%s]" % org_id)
        payload = self.create_chain_config_trust_root_delete_payload(org_id)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-07 添加共识节点地址
    def chain_config_consensus_node_addr_add(self, org_id: str, node_addrs: List[str], timeout: int = None,
                                             with_sync_result: bool = None) -> TxResponse:
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
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to add consensus node addr [org_id:%s]/[node_addrs:%s]' % (org_id, node_addrs))
        payload = self.create_chain_config_node_addr_add_payload(org_id, node_addrs)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-08 更新共识节点地址
    def chain_config_consensus_node_addr_update(self, org_id: str, node_old_addr: str, node_new_addr: str,
                                                timeout: int = None, with_sync_result: bool = None) -> TxResponse:
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
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to update consensus node addr [org_id:%s]/[%s->%s]' % (org_id, node_old_addr, node_new_addr))
        payload = self.create_chain_config_node_addr_update_payload(org_id, node_old_addr, node_new_addr)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-09 删除共识节点地址
    def chain_config_consensus_node_addr_delete(self, org_id: str, node_addr: str,
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
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to delete consensus node addr [org_id:%s]/[node_addr:%s]' % (org_id, node_addr))
        payload = self.create_chain_config_node_addr_delete_payload(org_id, node_addr)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def chain_config_consensus_node_org_check(self, org_id: str) -> bool:
        """
        检查节点组织是否共识组织
        :param org_id:
        :return:
        """
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        consensus_nodes = self.chain_config.consensus.nodes
        consensus_orgs = [item.org_id for item in consensus_nodes]
        return org_id in consensus_orgs

    ## 00-10 添加共识节点组织
    def chain_config_consensus_node_org_add(self, org_id: str, node_ids: List[str],
                                            timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        添加共识节点组织
        :param org_id: 节点组织Id
        :param node_ids: 节点Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to add consensus org [org_id:%s]/[node_ids:%s]' % (org_id, node_ids))
        payload = self.create_chain_config_consensus_node_org_add_payload(org_id, node_ids)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-11 更新共识节点组织
    def chain_config_consensus_node_org_update(self, org_id: str, node_ids: List[str],
                                               timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        更新共识节点组织
        :param org_id: 节点组织Id
        :param node_ids: 节点Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 添加共识、更新共识组织的交易响应或None
        :raises RequestError: 请求出错
        """
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to update consensus org [org_id:%s]/[node_ids:%s]' % (org_id, node_ids))
        payload = self.create_chain_config_consensus_node_org_update_payload(org_id, node_ids)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-12 删除共识节点组织
    def chain_config_consensus_node_org_delete(self, org_id: str,
                                               timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        删除共识节点组织
        :param org_id: 节点组织Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to delete consensus org [org_id:%s]' % org_id)
        payload = self.create_chain_config_consensus_node_org_delete_payload(org_id)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def chain_config_consensus_ext_check(self, key: str, value: str = None) -> bool:
        """检查共识扩展参数是否存在"""
        self._debug('begin to check consensus ext [key:%s]/[value:%s]' % (key, value))
        consensus_ext = self.consensus_ext
        if key in consensus_ext.keys():
            if value is None:
                return True
            else:
                return value == consensus_ext.get(key)
        return False

    # 00-13 添加共识扩展参数
    def chain_config_consensus_ext_add(self, params: dict,
                                       timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        添加共识扩展参数
        :param params: 字段key、value对
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._debug('begin to add consensus ext [params:%s]' % params)
        payload = self.create_chain_config_consensus_ext_add_payload(params)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-14 更新共识扩展参数
    def chain_config_consensus_ext_update(self, params: dict, timeout: int = None,
                                          with_sync_result: bool = None) -> TxResponse:
        """
        更新共识扩展参数
        :param dict params: 字段key、value对
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._debug('begin to update consensus ext [params:%s]' % params)
        payload = self.create_chain_config_consensus_ext_update_payload(params)

        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-15 删除共识扩展参数
    def chain_config_consensus_ext_delete(self, keys: List[str], timeout: int = None,
                                          with_sync_result: bool = None) -> TxResponse:
        """
        删除共识扩展参数
        :param keys: 待删除字段
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._debug('begin to delete consensus ext [keys:%s]' % keys)
        payload = self.create_chain_config_consensus_ext_delete_payload(keys)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def chain_config_permission_check(self, permission_resource_name: Union[ResourceName, str]) -> bool:
        """
        检查链配置权限是否存在
        :param permission_resource_name:
        :return:
        """
        self._debug(
            'begin to check chain config resource policies [permission_resource_name:%s]' % permission_resource_name)
        permission_resource_names = [item.resource_name for item in self.chain_config.resource_policies]
        return permission_resource_name in permission_resource_names

    # 00-16 链配置添加权限配置
    def chain_config_permission_add(self, permission_resource_name: Union[ResourceName, str], rule: Union[Rule, str],
                                    role_list: List[Role] = None, org_list: List[str] = None,
                                    timeout: int = None, with_sync_result: bool = None) -> TxResponse:
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
        self._debug('begin to add permission [permission_resource_name:%s]/[role:%s]/[role_list:%s]' % (
            permission_resource_name, rule, role_list))
        policy = self.create_policy(rule, role_list=role_list, org_list=org_list)
        payload = self.create_chain_config_permission_add_payload(permission_resource_name, policy)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-17 链配置更新权限配置
    def chain_config_permission_update(self, permission_resource_name: Union[ResourceName, str], rule: Union[Rule, str],
                                       role_list: List[Role] = None, org_list: List[str] = None,
                                       timeout: int = None, with_sync_result: bool = None) -> TxResponse:
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
        self._debug('begin to update permission [permission_resource_name:%s]/[role:%s]/[role_list:%s]' % (
            permission_resource_name, rule, role_list))
        policy = self.create_policy(rule, role_list=role_list, org_list=org_list)
        payload = self.create_chain_config_permission_update_payload(permission_resource_name, policy)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-18 链配置删除链权限配置
    def chain_config_permission_delete(self, permission_resource_name: Union[ResourceName, str],
                                       timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        删除权限配置
        :param str permission_resource_name: 权限名
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._debug('begin to delete permission [permission_resource_name:%s]' % permission_resource_name)
        payload = self.create_chain_config_permission_delete_payload(permission_resource_name)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def chain_config_consensus_node_id_check(self, org_id: str, node_id: str) -> bool:
        """
        链配置检查共识节点是否存在
        :param org_id:
        :param node_id:
        :return:
        """
        self._debug('begin to check consensus node id [org_id:%s]/[node_id:%s]' % (org_id, node_id))
        consensus_nodes = self.chain_config.consensus.nodes
        for item in consensus_nodes:
            if node_id in item.node_id:
                return True
            # if org_id == item.org_id and node_id in item.node_id:
            #     return True
        return False

    # 00-19 链配置添加共识节点Id
    def chain_config_consensus_node_id_add(self, org_id: str, node_ids: List[str],
                                           timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        添加共识节点Id
        :param str org_id: 节点组织Id
        :param node_ids: 节点Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to add consensus node [org_id:%s]/[node_ids:%s]' % (org_id, node_ids))
        payload = self.create_chain_config_consensus_node_id_add_payload(org_id, node_ids)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-20 链配置更新共识节点Id
    def chain_config_consensus_node_id_update(self, org_id: str, node_old_id: str, node_new_id: str,
                                              timeout: int = None, with_sync_result: bool = None) -> TxResponse:
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
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to update consensus node [org_id:%s]/[%s->%s]' % (org_id, node_old_id, node_new_id))
        payload = self.create_chain_config_consensus_node_id_update_payload(org_id, node_old_id, node_new_id)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-21 链配置删除共识节点Id
    def chain_config_consensus_node_id_delete(self, org_id: str, node_id: str,
                                              timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        删除共识节点Id
        :param str org_id: 节点组织Id
        :param node_id: 节点Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to delete consensus node [org_id:%s]' % org_id)
        payload = self.create_chain_config_consensus_node_id_delete_payload(org_id, node_id)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def chain_config_trust_member_check(self, org_id: str, trust_member_info: str = None) -> bool:
        """
        检查信任第三方组织是否上链
        :param org_id: 组织Id
        :param trust_member_info: 信任第三方根证书
        :return: 已上链返回True，否则返回False
        """
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        trust_members = self.chain_config.trust_members
        trust_member_org_ids = [item.org_id for item in trust_members]
        if org_id in trust_member_org_ids:
            trust_member_infos = [item.member_info for item in trust_members]
            if trust_member_info in trust_member_infos:
                return True
        return False

    # 00-22 添加信任第三方组织
    def chain_config_trust_member_add(self, org_id: str, trust_member_node_id: str, trust_member_info: str,
                                      trust_member_role: Union[Role, str],
                                      timeout: int = None, with_sync_result: bool = None) -> TxResponse:
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
        if self.auth_type == AuthType.Public:
            org_id = 'public'
        self._debug('begin to add trust member [org_id:%s]/[node_id:%s]/[role:%s]' % (
            org_id, trust_member_node_id, trust_member_role))
        payload = self.create_chain_config_trust_member_add_payload(org_id, trust_member_node_id, trust_member_info,
                                                                    trust_member_role)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-23 更新信任第三方组织
    def chain_config_trust_member_update(self, trust_member_org_id: str, trust_member_node_id: str,
                                         trust_member_info: str, trust_member_role: Union[Role, str],
                                         timeout: int = None, with_sync_result: bool = None) -> TxResponse:
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

        if self.auth_type == AuthType.Public:
            trust_member_org_id = 'public'
        self._debug('begin to update trust member [org_id:%s]/[node_id:%s]/[role:%s]' % (
            trust_member_org_id, trust_member_node_id, trust_member_role))
        payload = self.create_chain_config_trust_member_update_payload(trust_member_org_id, trust_member_node_id,
                                                                       trust_member_info, trust_member_role)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-24 删除信任第三方组织
    def chain_config_trust_member_delete(self, trust_member_info: str,
                                         timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        删除信任第三方组织
        :param trust_member_info: 节点证书信息
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        # if self.auth_type == AuthType.Public:
        #     trust_member_org_id = 'public'
        self._debug('begin to delete trust member [trust_member_info:%s]' % trust_member_info)
        payload = self.create_chain_config_trust_member_delete_payload(trust_member_info)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-25 变更地址类型
    def chain_config_alter_addr_type(self, addr_type: Union[AddrType, str, int],
                                     timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        创建链配置变更地址类型待签名Payload
        <00-25-CHAIN_CONFIG-ALTER_ADDR_TYPE>
        :param addr_type: 地址类型
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._debug('begin to alter addr type [addr_type:%s]' % addr_type)
        payload = self.create_chain_config_alter_addr_type_payload(addr_type)
        return self._send_chain_config_update_request(payload, timeout=timeout,
                                                      with_sync_result=with_sync_result)

    # 00-26 启用或禁用Gas
    def chain_config_enable_or_disable_gas(self, enable_gas: bool = None, timeout: int = None,
                                           with_sync_result: bool = None) -> TxResponse:
        """
        启用或禁用Gas
        :param enable_gas: 是否启用Gas, 为None时直接切换
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        if enable_gas is None or (enable_gas is not self.enabled_gas):
            self._debug('begin to enable or disable gas [enable_gas:%s]' % enable_gas)
            payload = self.create_chain_config_enable_or_disable_gas_payload()
            return self._send_chain_config_update_request(payload, timeout=timeout,
                                                          with_sync_result=with_sync_result)

    def chain_config_enable_multi_sign_manual_run(self, enable: bool = True, timeout: int = None,
                                                  with_sync_result: bool = None) -> TxResponse:
        """
        启用或禁用多签手动运行模式
        :param enable: 启用或禁用多签手动运行模式
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        if enable is True:
            self._debug('begin to enable multi sign manual run')
        else:
            self._debug('begin to disable multi sign manual run')
        payload = self.create_chain_config_enable_multi_sign_manual_run_payload(enable)
        return self._send_chain_config_update_request(payload, timeout=timeout,
                                                      with_sync_result=with_sync_result)

    def chain_config_check_multi_sign_manual_run(self) -> bool:
        """
        检查是否启用多签手动运行
        :return:
        """
        self._info('检查是否多签手动运行')
        return self.get_chain_config().vm.native.multisign.enable_manual_run

    # 00-27 设置合约调用基础Gas消耗
    def chain_config_set_invoke_base_gas(self, amount: int, timeout: int = None, with_sync_result: bool = None):
        """
        设置合约调用基础Gas消耗
        :param amount: 设置待基础Gas消耗数量
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        self._debug('begin to set invoke base gas [amount:%d]' % amount)
        params = {ParamKey.set_invoke_base_gas.name: amount}
        payload = self._create_chain_config_manage_payload(ChainConfigMethod.SET_INVOKE_BASE_GAS.name,
                                                           params)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-28 设置Gas管理员地址
    def chain_config_set_account_manager_admin(self, address: str, timeout: int = None,
                                               with_sync_result: bool = None) -> TxResponse:
        """
        设置Gas管理员地址
        :param address: 用户地址-为None时为当前用户地址
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        self._debug('begin to set gas admin [address:%s]' % address)
        payload = self.create_chain_config_set_account_manager_admin_payload(address)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def chain_config_optimize_charge_gas(self, enable: bool, timeout: int = None,
                                         with_sync_result: bool = None) -> TxResponse:
        """
        开启或关闭链配置的Gas优化
        :param enable: 是否启用
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        self._debug('begin to optimize charge gas [enable:%s]' % enable)
        payload = self.create_chain_config_optimize_charge_gas_payload(enable)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 00-29 获取链配置权限列表
    def get_permission_list(self) -> ResourcePolicy:
        """
        获取链配置权限列表
        <00-29-CHAIN_CONFIG-PERMISSION_LIST>
        :return: 权限列表
        """
        return self.get_chain_config_permission_list()

    # 00-32 更新DPOS共识节点Id
    def chain_config_dpos_node_id_update(self, node_ids: List[str],
                                         timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        更新DPOS共识节点Id
        :param node_ids: 节点Id列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises RequestError: 请求出错
        """
        self._debug('begin to update dpos node ids [node_ids:%s]' % node_ids)
        payload = self.create_chain_config_dpos_node_id_update_payload(node_ids)
        return self._send_chain_config_update_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    def _send_chain_config_update_request(self, payload: Payload,
                                          timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        发送链配置更新请求
        :param payload: 待签名链配置更新请求Payload
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮交易结果
        :return: 交易响应信息
        """
        response = self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
        # 更新缓存的chain_config
        setattr(self, '_cached_chain_config', None)
        return response

    def enable_disable_only_creator_update(self, enable: bool = True, timeout: int = None,
                                           with_sync_result: bool = None) -> TxResponse:
        if enable is True:
            payload = self.create_chain_config_enable_only_creator_update_payload()
        else:
            payload = self.create_chain_config_disable_only_creator_update_payload

        return self._send_chain_config_update_request(payload, timeout, with_sync_result)

    def tbft_to_raft(self, ext_config: dict, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        生成链配置更新链配置版本Payload
        :return: 待签名Payload
        """
        payload = self.create_chain_config_consensus_switch_payload(ConsensusType.TBFT, ConsensusType.RAFT, ext_config)
        return self._send_chain_config_update_request(payload, timeout, with_sync_result)

    def raft_to_tbft(self, ext_config: dict, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        生成链配置更新链配置版本Payload
        :return: 待签名Payload
        """
        payload = self.create_chain_config_consensus_switch_payload(ConsensusType.RAFT, ConsensusType.TBFT, ext_config)
        return self._send_chain_config_update_request(payload, timeout, with_sync_result)
