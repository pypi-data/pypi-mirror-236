#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   cmc_utils.py
# @Function     :   cmc命令生成实用方法

import json
import re
from functools import wraps
from typing import List, Union

from chainmaker.keys import AddrType, AuthType
from chainmaker.utils.common import ensure_enum

NODE_CNT = 3


def _handle_params(params, is_evm: bool = False):
    """将字典/列表格式的value转为字符串"""
    if params is None:
        return '"[]"' if is_evm else '"{}"'
    if params is True:
        return 'true'
    if params is False:
        return 'false'

    if isinstance(params, str):
        return params

    if isinstance(params, list) or isinstance(params, dict):
        return '"' + json.dumps(params).replace(' ', '').replace('"', '\\"') + '"'

    return str(params)


def with_endorsers(func):
    """背书装饰器，用于添加sync_result=true --admin-key-file-paths 及 -admin-crt-file-paths参数"""

    @wraps(func)
    def _func(self, *args, **kwargs):
        admin_key_file_paths = ','.join(
            [f'./testdata/crypto-config/wx-org{i}.chainmaker.org/user/admin1/admin1.sign.key'
             for i in range(1, NODE_CNT + 1)])
        admin_crt_file_paths = ','.join(
            [f'./testdata/crypto-config/wx-org{i}.chainmaker.org/user/admin1/admin1.sign.crt'
             for i in range(1, NODE_CNT + 1)])
        pk_admin_key_file_paths = ','.join(['./testdata/crypto-config/node1/admin/admin1/admin1.key',
                                            './testdata/crypto-config/node1/admin/admin2/admin2.key',
                                            './testdata/crypto-config/node1/admin/admin3/admin3.key'])
        if self.auth_type == AuthType.PermissionedWithCert:
            kwargs['admin_crt_file_paths'] = kwargs.get('admin_crt_file_paths', admin_crt_file_paths)
            kwargs['admin_key_file_paths'] = kwargs.get('admin_key_file_paths', admin_key_file_paths)
        elif self.auth_type == AuthType.PermissionedWithCert:
            kwargs['admin_org_ids'] = 'wx-org1.chainmaker.org,wx-org2.chainmaker.org,wx-org3.chainmaker.org'
            kwargs['admin_key_file_paths'] = kwargs.get('admin_key_file_paths', admin_key_file_paths)
        else:
            kwargs['admin_key_file_paths'] = kwargs.get('admin_key_file_paths', pk_admin_key_file_paths)

        kwargs['sync_result'] = kwargs.get('sync_result', 'true')
        return func(self, *args, **kwargs)

    return _func


class BaseCmc:
    # PARENT_CMD: str

    def __init__(self, chain_id='chain1', auth_type: AuthType = AuthType.PermissionedWithCert):
        self.chain_id = chain_id
        self.auth_type = auth_type
        self.inline = False
        self.default_params = {'sdk_conf_path': self._get_sdk_config_path(auth_type)}

    @staticmethod
    def _get_sdk_config_path(auth_type):
        if auth_type == AuthType.PermissionedWithCert:
            sdk_config_file = './testdata/sdk_config.yml'
        elif auth_type == AuthType.PermissionedWithKey:
            sdk_config_file = './testdata/sdk_config_pwk.yml'
        else:
            sdk_config_file = './testdata/sdk_config_pk.yml'
        return sdk_config_file

    def _assemble_cmd(self, sub_command: str, *args, **kwargs) -> str:
        """
        组装cmc命令，组装除了self对象、sub_command自命令，和inline是否一行之外的所有关键字参数
        kwargs中所有关键字参数要求和命令参数一致，使用下划线连接方式
        eg. 如参数中的contract_name='fact' 会拼装成 ' --contract-name=fact'
        :param sub_command: cmc子命令，承接父命令PARENT_CMD， 如create
        :param inline: 是否一行显示，默认断行
        :param kwargs: 要组装的参数
        :return: 组装的命令
        """
        sep = ' ' if self.inline else ' \\\n'
        kwargs.update(self.default_params)
        _args = [str(arg) for arg in args]
        _kwargs = [f"--{key.replace('_', '-')}={_handle_params(value)}" for key, value in kwargs.items()
                   if key is not self and value is not None]
        cmd = sep.join([f'./cmc {sub_command}', *_args, *_kwargs])
        return cmd

    # def _perform_cmd(self, sub_command: str, *args, **items) -> str:
    #     """组装并执行命令"""
    #     cmd = self._assemble_cmd(sub_command, *args, **items)
    #     result = self._host.execute(cmd, workspace=self.cmc_dir)
    #     return result

    def execute(self, sub_command, *args, **kwargs):
        cmc = '%s/cmc' % self.cmc_dir

        # build_cmc
        if not self._host.exists(cmc):
            self._host.execute('go build', workspace=self.cmc_dir)
        cmc_crypto_config_path = '%s/testdata/crypto-config' % self.cmc_dir

        # 软链crypto-config
        if not self._host.exists(cmc_crypto_config_path):
            crypto_config_path = '%s/build/crypto-config' % self._chainmaker_go_path
            self._host.execute(f'ln -s {crypto_config_path} {cmc_crypto_config_path}')

        cmd = self._assemble_cmd(sub_command, *args, **kwargs)
        result = self._host.execute(cmd, workspace=self.cmc_dir)
        err_msg, = re.findall('Error: (.*)', result) or [None]

        return err_msg or result


class CmcChainConfig(BaseCmc):
    def get_chain_config(self):
        """
        查询链配置
        :return:
        """
        return self._assemble_cmd('client chainconfig query')

    def get_permission_list(self):
        return self._assemble_cmd('client chainconfig permission list')

    @with_endorsers
    def chain_config_block_update(self, tx_parameter_size=None, block_interval=None, **kwargs):
        """更新交易参数最大值限制及出块时间"""
        kwargs.pop('sync_result')
        if tx_parameter_size is not None:
            return self._assemble_cmd('client chainconfig block updatetxparametersize',
                                      tx_parameter_size=tx_parameter_size,
                                      org_id='wx-org1.chainmaker.org', **kwargs)
        if block_interval is not None:
            return self._assemble_cmd('client chainconfig block updateblockinterval', block_interval=block_interval,
                                      org_id='wx-org1.chainmaker.org', **kwargs)

    @with_endorsers
    def chain_config_core_update(self):  # todo
        pass

    @with_endorsers
    def chain_config_consensus_node_id_add(self, node_org_id, node_id, **kwargs):
        """
        增加共识节点
        :return: consensusnodeid response message:"OK"
                 tx_id:"e49ef243f54a4f07934341525b8cfd1585e71eb9f50144219378ed57d7703c3c"
        """
        kwargs.pop('sync_result')
        return self._assemble_cmd('client chainconfig consensusnodeid add', node_id=node_id,
                                  node_org_id=node_org_id, **kwargs)

    @with_endorsers
    def chain_config_consensus_node_id_delete(self, node_org_id, node_id, **kwargs):
        """
        移除共识节点
        :return: consensusnodeid response message:"OK"
                 tx_id:"e49ef243f54a4f07934341525b8cfd1585e71eb9f50144219378ed57d7703c3c"
        """
        kwargs.pop('sync_result')
        return self._assemble_cmd('client chainconfig consensusnodeid remove', node_id=node_id,
                                  node_org_id=node_org_id, **kwargs)

    @with_endorsers
    def chain_config_consensus_node_id_update(self, node_org_id, node_id_old, node_id, **kwargs):
        """
        升级共识节点
        :return: consensusnodeid response message:"OK"
                 tx_id:"e49ef243f54a4f07934341525b8cfd1585e71eb9f50144219378ed57d7703c3c"
        """
        kwargs.pop('sync_result')
        return self._assemble_cmd('client chainconfig consensusnodeid update', node_org_id=node_org_id,
                                  node_id_old=node_id_old,
                                  node_id=node_id, **kwargs)

    @with_endorsers
    def chain_config_consensus_node_org_add(self, node_org_id: str, node_ids: list, **kwargs):  # fixme
        """
        升级共识节点
        :return: consensusnodeid response message:"OK"
                 tx_id:"e49ef243f54a4f07934341525b8cfd1585e71eb9f50144219378ed57d7703c3c"
        """
        kwargs.pop('sync_result')
        node_ids = ','.join(node_ids)
        return self._assemble_cmd('client chainconfig consensusnodeorg add',
                                  node_org_id=node_org_id, node_ids=node_ids,
                                  **kwargs)

    @with_endorsers
    def chain_config_consensus_node_org_delete(self, node_org_id, **kwargs):  # fixme
        """
        升级共识节点
        :return: consensusnodeid response message:"OK"
                 tx_id:"e49ef243f54a4f07934341525b8cfd1585e71eb9f50144219378ed57d7703c3c"
        """
        kwargs.pop('sync_result')
        return self._assemble_cmd('client chainconfig consensusnodeorg remove', node_org_id=node_org_id, **kwargs)

    @with_endorsers
    def chain_config_consensus_node_org_update(self, node_org_id, node_ids,
                                               **kwargs):  # fixme
        """
        升级共识节点
        :return: consensusnodeid response message:"OK"
                 tx_id:"e49ef243f54a4f07934341525b8cfd1585e71eb9f50144219378ed57d7703c3c"
        """
        kwargs.pop('sync_result')
        return self._assemble_cmd('client chainconfig consensusnodeorg update', node_org_id=node_org_id,
                                  node_ids=node_ids, **kwargs)

    @with_endorsers
    def chain_config_trust_root_add(self, trust_root_org_id: str, trust_root_path: Union[List[str], str], **kwargs):
        if isinstance(trust_root_path, list):
            trust_root_path = ','.join(trust_root_path)

        kwargs.pop('sync_result')
        return self._assemble_cmd('client chainconfig trustroot add', trust_root_org_id=trust_root_org_id,
                                  trust_root_path=trust_root_path, **kwargs)

    @with_endorsers
    def chain_config_trust_root_delete(self, trust_root_org_id, **kwargs):
        kwargs.pop('sync_result')
        return self._assemble_cmd('client chainconfig trustroot remove', trust_root_org_id=trust_root_org_id,
                                  **kwargs)

    @with_endorsers
    def chain_config_trust_member_add(self, trust_member_org_id, trust_member_path, trust_member_role,
                                      trust_member_node_id, **kwargs):
        kwargs.pop('sync_result')
        kwargs['org_id'] = 'wx-org1.chainmaker.org'
        return self._assemble_cmd('client chainconfig trustmember add', trust_member_org_id=trust_member_org_id,
                                  trust_member_path=trust_member_path, trust_member_role=trust_member_role,
                                  trust_member_node_id=trust_member_node_id, **kwargs)

    @with_endorsers
    def chain_config_trust_root_update(self, trust_root_org_id, trust_root_path: list, **kwargs):
        trust_root_path = ','.join(trust_root_path)
        kwargs.pop('sync_result')
        return self._assemble_cmd('client chainconfig trustroot update', trust_root_org_id=trust_root_org_id,
                                  trust_root_path=trust_root_path,
                                  **kwargs)

    @with_endorsers
    def chain_config_trust_member_delete(self, trust_member_path, **kwargs):
        kwargs.pop('sync_result')
        kwargs['org_id'] = 'wx-org1.chainmaker.org'
        return self._assemble_cmd('client chainconfig trustmember remove', trust_member_path=trust_member_path,
                                  **kwargs)

    @with_endorsers
    def chain_config_enable_or_disable_gas(self, enable_gas: bool = True, **kwargs):
        kwargs.pop('sync_result')
        return self._assemble_cmd('client gas', gas_enable=_handle_params(enable_gas), **kwargs)

    @with_endorsers
    def chain_config_enable_multi_sign_manual_run(self, multi_sign_enable_manual_run: bool = False, **kwargs):
        multi_sign_enable_manual_run = 'true' if multi_sign_enable_manual_run is True else 'false'
        return self._assemble_cmd('client chainconfig enable-manual-run',
                                  multi_sign_enable_manual_run=multi_sign_enable_manual_run, **kwargs)

    @with_endorsers
    def chain_config_set_invoke_base_gas(self, amount: int, **kwargs):
        kwargs.pop('sync_result')
        return self._assemble_cmd('gas set-base-gas', amount=amount, **kwargs)

    @with_endorsers
    def chain_config_alter_addr_type(self, addr_type: Union[AddrType, str, int], **kwargs):
        kwargs.pop('sync_result')
        address_type = ensure_enum(addr_type, AddrType).value
        return self._assemble_cmd('client chainconfig alter-addr-type', address_type=address_type, **kwargs)

    @with_endorsers
    def chain_config_update_version(self, block_version: str):
        return self.invoke_contract()  # todo

    @with_endorsers
    def chain_config_permission_add(self, permission_resource_name: str, rule: str, role_list: list = None,
                                    org_list: list = None, **kwargs):
        # kwargs.pop('sync_result')
        if isinstance(role_list, list):
            role_list = ','.join(role_list)
        if isinstance(org_list, list):
            org_list = ','.join(org_list)
        return self._assemble_cmd('client chainconfig permission add',
                                  permission_resource_name=permission_resource_name,
                                  permission_resource_policy_rule=rule,
                                  permission_resource_policy_roleList=role_list,
                                  permission_resource_policy_orgList=org_list,
                                  **kwargs)

    @with_endorsers
    def chain_config_permission_update(self, permission_resource_name: str, rule: str, role_list: list = None,
                                       org_list: list = None, **kwargs):
        if isinstance(role_list, list):
            role_list = ','.join(role_list)
        if isinstance(org_list, list):
            org_list = ','.join(org_list)
        return self._assemble_cmd('client chainconfig permission update',
                                  permission_resource_name=permission_resource_name,
                                  permission_resource_policy_rule=rule,
                                  permission_resource_policy_roleList=role_list,
                                  permission_resource_policy_orgList=org_list,
                                  **kwargs)

    @with_endorsers
    def chain_config_permission_delete(self, permission_resource_name: str, **kwargs):
        return self._assemble_cmd('client chainconfig permission delete',
                                  permission_resource_name=permission_resource_name, **kwargs)


class CmcChainQuery(BaseCmc):
    def get_block_by_height(self, height: int) -> str:
        """
        根据区块高度获取区块
        :param height: 高度
        :return:
        """
        result = self._assemble_cmd(f'query block-by-height {height}', chain_id=self.chain_id)
        return result

    def get_block_by_hash(self, hash: str):
        result = self._assemble_cmd(f'query block-by-hash {hash}', chain_id=self.chain_id)
        return result

    def get_block_by_tx_id(self, tx_id):
        result = self._assemble_cmd(f'query block-by-txid {tx_id}', chain_id=self.chain_id)
        return result

    def get_tx_by_tx_id(self, tx_id):
        result = self._assemble_cmd(f'query tx {tx_id}', chain_id=self.chain_id)
        return result

    def get_archived_block_height(self):
        return self._assemble_cmd('query archived-height', chain_id=self.chain_id)


class CmcCertManage(BaseCmc):
    # 不需要sdk_config_path
    def gen_crl(self, ca_cert_path, ca_key_path, crt_path, crl_path='./client1.crl'):
        """
        生成crl(Certificate Revocation List)列表
        :param ca_cert_path:
        :param ca_key_path:
        :param crt_path:
        :param crl_path:
        :return:
        """
        return self._assemble_cmd('cert crl', ca_cert_path=ca_cert_path, ca_key_path=ca_key_path, crl_path=crl_path,
                                  crt_path=crt_path)

    @with_endorsers
    def revoke_crt(self, cert_crl_path):
        return self._assemble_cmd('client certmanage revoke', cert_crl_path=cert_crl_path)


class CmcCertAliasManage(BaseCmc):
    def query_cert_alias(self, cert_alias, **kwargs):
        return self._assemble_cmd('client certalias query', cert_alias=cert_alias, **kwargs)

    @with_endorsers
    def update_cert_by_alias(self, cert_alias, new_cert_path, **kwargs):
        return self._assemble_cmd('client certalias update', cert_alias=cert_alias, new_cert_path=new_cert_path,
                                  **kwargs)

    @with_endorsers
    def delete_cert_alias(self, cert_alias, **kwargs):
        return self._assemble_cmd('client certalias delete', cert_alias=cert_alias, **kwargs)


class CmcPubkeyManage(BaseCmc):
    @with_endorsers
    def add_pubkey(self, pubkey_file_path: str, key_org_id: str, role: str = 'client'):
        return self._assemble_cmd('pubkey add', chain_id=self.chain_id, pubkey_file_path=pubkey_file_path,
                                  key_org_id=key_org_id, role=role)

    def query_pubkey(self, pubkey_file_path: str):
        return self._assemble_cmd('pubkey query', chain_id=self.chain_id, pubkey_file_path=pubkey_file_path)

    @with_endorsers
    def delete_pubkey(self, pubkey_file_path: str, key_org_id: str):
        return self._assemble_cmd('pubkey del', chain_id=self.chain_id, pubkey_file_path=pubkey_file_path,
                                  key_org_id=key_org_id)


class CmcUserContract(BaseCmc):
    @with_endorsers
    def create_contract(self, contract_name: str, byte_code_path: str, runtime_type: str = 'WASMER',
                        version: str = '1.0.0', params: Union[dict, list] = None, **kwargs) -> str:
        """
        创建合约
        :param contract_name: 合约名称
        :param byte_code_path: 合约文件路径
        :param params: 创建合约参数
        :param runtime_type: 合约类型 (str)
        :param version: 合约版本
        :param kwargs: 合约参数
        :return: 命令执行结果 response: message:"OK" contract_result:<result:"\n(ddb9a2acbefac7ff56a9213fac26e3a9b038e423
        \022\0031.0\030\005*<\n\026wx-org1.chainmaker.org\020\001\032 \3375\2313\226\215W\013k\206\035\356\377\177\224
        \276\033\177`\261J@\304\257\261\262\262\301\3064\344\026" message:"OK" >
        tx_id:"7a75e8202ba34a0d9785bd14c368cfbff401aa39042b496f850dd42091454945"

        """
        if runtime_type == 'EVM':
            if 'abi_file_path' not in kwargs:
                kwargs['abi_file_path'] = byte_code_path.replace('.bin', '.abi')
            params = _handle_params(params, is_evm=True)
        else:
            params = _handle_params(params)
        return self._assemble_cmd('client contract user create', contract_name=contract_name,
                                  byte_code_path=byte_code_path,
                                  runtime_type=runtime_type, params=_handle_params(params), version=version,
                                  **kwargs)

    def query_contract(self, contract_name: str, method: str, params: Union[dict, list] = None, abi_file_path='',
                       **kwargs):
        """
        查询合约
        :param abi_file_path:
        :param contract_name: 合约名称
        :param method: 合约方法
        :param params: 合约参数
        :return: 命令执行结果 QUERY contract resp: message:"SUCCESS" contract_result:<result:"{\"file_hash\":
        \"ab3456df5799b87c77e7f88\",\"file_name\":\"name007\",\"time\":6543234}" gas_used:20688172 >
        tx_id:"988f1647ddb5491087994903982349c248bc398362e44709b0e6777f8187189b"
        """

        if abi_file_path:
            return self._assemble_cmd('client contract user get', contract_name=contract_name, method=method,
                                      params=_handle_params(params, is_evm=True), abi_file_path=abi_file_path, **kwargs)
        else:
            return self._assemble_cmd('client contract user get', contract_name=contract_name, method=method,
                                      params=_handle_params(params), **kwargs)

    def invoke_contract(self, contract_name: str, method: str, params: Union[dict, list] = None, abi_file_path='',
                        **kwargs):
        """
        调用合约
        :param abi_file_path:
        :param contract_name: 合约名称
        :param method: 合约方法
        :param params: 合约参数
        :return: 命令执行结果 INVOKE contract resp, [code:0]/[msg:OK]/[contractResult:<nil>]/
        [txId:bcfeb08299cd44bfbbc30a15017b64b04537f8b7680649178e92aec229a389c3]
        panic: runtime error: invalid memory address or nil pointer dereference
        """
        kwargs['sync_result'] = kwargs.get('sync_result', 'true')
        if abi_file_path:
            return self._assemble_cmd('client contract user invoke', contract_name=contract_name, method=method,
                                      params=_handle_params(params, is_evm=True), abi_file_path=abi_file_path, **kwargs)
        else:
            return self._assemble_cmd('client contract user invoke', contract_name=contract_name, method=method,
                                      params=_handle_params(params), abi_file_path=abi_file_path, **kwargs)

    @with_endorsers
    def upgrade_contract(self, contract_name: str, byte_code_path: str,
                         runtime_type: str = 'WASMER', params: Union[dict, list] = None,
                         version: str = '2.0', **kwargs):
        """
        升级合约
        :param contract_name: 合约名称
        :param byte_code_path: 合约文件路径
        :param params: 合约参数
        :param runtime_type: 合约类型
        :param version: 合约版本
        :param kwargs: 命令执行结果
        :return:  命令执行结果 upgrade user contract params:[] upgrade contract resp: message:"OK" contract_result:<result:"\n\005fact2\022\0032.0\030\002*<\n\026wx-org1.chainmaker.org\020\001\032 \3375\2313\226\215W\013k\206\035\356\377\177\224\276\033\177`\261J@\304\257\261\262\262\301\3064\344\026" message:"OK" > tx_id:"e5559d5be1fd40688e30a00983b17c489e8ad8d365834074b89422cb4996375a"

        """
        if runtime_type == 'EVM':
            if 'abi_file_path' not in kwargs:
                kwargs['abi_file_path'] = byte_code_path.replace('.bin', '.abi')
            params = _handle_params(params, is_evm=True)
        else:
            params = _handle_params(params)
        return self._assemble_cmd('client contract user upgrade', contract_name=contract_name,
                                  byte_code_path=byte_code_path,
                                  params=_handle_params(params), runtime_type=runtime_type, version=version,
                                  **kwargs)

    @with_endorsers
    def freeze_contract(self, contract_name: str, **kwargs):
        """
        冻结合约
        :param contract_name: 合约名称
        :return: 命令执行结果 freeze contract resp: message:"OK" contract_result:<result:"{\"name\":\"fact2\",\"version\":\"2.0\",\"runtime_type\":2,\"status\":1,\"creator\":{\"trust_root_org_id\":\"wx-org1.chainmaker.org\",\"member_type\":1,\"trust_member_info\":\"3zWZM5aNVwtrhh3u/3+Uvht/YLFKQMSvsbKywcY05BY=\"}}" message:"OK" > tx_id:"4c916288ef5b4752bc1bf65201f0a9907bc33865190847a0bcfd7cb59cf77d27"
        """
        kwargs['org_id'] = 'wx-org1.chainmaker.org'
        return self._assemble_cmd('client contract user freeze', contract_name=contract_name, **kwargs)

    @with_endorsers
    def unfreeze_contract(self, contract_name: str, **kwargs):
        """
        解冻合约
        :param contract_name: 合约名称
        :return: 命令执行结果 unfreeze contract resp: message:"OK" contract_result:<result:"{\"name\":\"fact2\",
        \"version\":\"2.0\",\"runtime_type\":2,\"creator\":{\"trust_root_org_id\":\"wx-org1.chainmaker.org\",
        \"member_type\":1,\"trust_member_info\":\"3zWZM5aNVwtrhh3u/3+Uvht/YLFKQMSvsbKywcY05BY=\"}}" message:"OK" >
        tx_id:"bc345e183b284eb3a3117a5674ad57a5ca395bcb6f9048f58094eb5cefa4cde5"
        """
        kwargs['org_id'] = 'wx-org1.chainmaker.org'
        return self._assemble_cmd('client contract user unfreeze', contract_name=contract_name, **kwargs)

    @with_endorsers
    def revoke_contract(self, contract_name: str, **kwargs):
        """
        解冻合约
        :param contract_name: 合约名称
        :return: 命令执行结果 revoke contract resp: message:"OK" contract_result:<result:"{\"name\":\"fact2\",
        \"version\":\"2.0\",\"runtime_type\":2,\"status\":2,\"creator\":{\"trust_root_org_id\":
        \"wx-org1.chainmaker.org\",\"member_type\":1,\"trust_member_info\":
        \"3zWZM5aNVwtrhh3u/3+Uvht/YLFKQMSvsbKywcY05BY=\"}}" message:"OK" >
        tx_id:"3059fe7451ed407781a3f218b8a21642102ce4dc35e34e78bb2ec6d1c5c9ed82"
        """
        kwargs['org_id'] = 'wx-org1.chainmaker.org'
        return self._assemble_cmd('client contract user revoke', contract_name=contract_name, **kwargs)

    @staticmethod
    def contract_name_to_address(contract_name: str, address_type: int = 0):
        return f'./cmc client contract name-to-addr {contract_name} --address-type={address_type}'


class CmcSystemContract(BaseCmc):
    @with_endorsers
    def grant_native_contract_access(self, grant_contract_list: list, **kwargs):
        kwargs.pop('sync_result')
        grant_contract_list = ','.join(grant_contract_list)
        return self._assemble_cmd('client contract system manage access-grant',
                                  grant_contract_list=grant_contract_list, **kwargs)

    @with_endorsers
    def revoke_native_contract_access(self, revoke_contract_list: list, **kwargs):
        kwargs.pop('sync_result')
        revoke_contract_list = ','.join(revoke_contract_list)
        return self._assemble_cmd('client contract system manage access-revoke',
                                  revoke_contract_list=revoke_contract_list, **kwargs)

    def get_disable_native_contract_list(self, **kwargs):
        return self._assemble_cmd('client contract system manage access-query')


class CmcMultiSign(BaseCmc):
    def multi_sign_req(self, params: list, **kwargs):
        return self._assemble_cmd('client contract system multi-sign req', params=_handle_params(params), **kwargs)

    def multi_sign_vote(self, tx_id, admin_key_file_paths, admin_crt_file_paths, is_agree=True,
                        **kwargs):
        is_agree = 'true' if is_agree else 'false'
        return self._assemble_cmd('client contract system multi-sign vote', tx_id=tx_id,
                                  admin_key_file_paths=admin_key_file_paths, admin_crt_file_paths=admin_crt_file_paths,
                                  is_agree=is_agree, **kwargs)

    def multi_sign_trig(self, tx_id, **kwargs):
        return self._assemble_cmd('client contract system multi-sign trig', tx_id=tx_id, **kwargs)

    def multi_sign_query(self, tx_id: str, **kwargs):
        return self._assemble_cmd('client contract system multi-sign query', tx_id=tx_id, **kwargs)


class CmcPrivateKeyManage(BaseCmc):
    def gen_key(self, algo, name, path='./'):
        """
        生成私钥
        :param algo: SM2 / ECC_P256
        :param name: ca.key
        :param path:
        :return:
        """
        return self._assemble_cmd('key gen', algo=algo, name=name, path=path)


class CmcArchive(BaseCmc):

    def archive_block(self, type='mysql', dest='root:password:localhost:3306', target='', blocks=10000,
                      secret_key='password'):
        """

        :param type:
        :param dest:
        :param target: "2021-06-01 15:01:41" / 100
        :param blocks:
        :param secret_key:
        :return:
        """
        return self._assemble_cmd('archive dump', type=type, dest=dest, target=repr(target), blocks=blocks,
                                  chain_id=self.chain_id,
                                  secret_key=secret_key)

    def restore_block(self, type='mysql', dest='root:password:localhost:3306', start_block_height: int = 0,
                      secret_key='password'):
        """

        :param start_block_height:
        :param type:
        :param dest:
        :param secret_key:
        :return:
        """
        return self._assemble_cmd('archive restore', type=type, dest=dest, start_block_height=start_block_height,
                                  chain_id=self.chain_id, secret_key=secret_key)

    def get_archived_block_by_height(self, block_height: int, type='mysql', dest='root:password:localhost:3306'):
        return self._assemble_cmd('archive query block-by-height %s' % block_height, type=type, dest=dest,
                                  chain_id=self.chain_id)

    def get_archived_block_by_hash(self, hash: str, type='mysql', dest=''):
        return self._assemble_cmd('archive query block-by-hash %s' % hash, type=type, dest=dest,
                                  chain_id=self.chain_id)

    def get_archived_block_by_tx_id(self, tx_id: str, type='mysql', dest=''):
        return self._assemble_cmd('archive query block-by-txid %s' % tx_id, type=type, dest=dest,
                                  chain_id=self.chain_id)

    def get_archived_tx_by_tx_id(self, tx_id: str, type='mysql', dest=''):
        return self._assemble_cmd('archive query tx %s' % tx_id, type=type, dest=dest,
                                  chain_id=self.chain_id)


class CmcTxPool(BaseCmc):
    """"""

    def get_pool_status(self):
        return self._assemble_cmd('txpool status')

    def get_tx_ids_by_type_and_stage(self, type: int = 3, stage: int = 3):
        return self._assemble_cmd('txpool txids', type=type, stage=stage)

    def get_txs_in_pool_by_tx_ids(self, tx_ids: list):
        tx_ids = ','.join(tx_ids)
        return self._assemble_cmd('txpool txs', tx_ids=tx_ids)


class CmcGasManage(BaseCmc):
    """"""

    def get_gas_admin(self):
        return self._assemble_cmd('gas get-admin')

    def get_account_status(self, address: str):
        return self._assemble_cmd('gas account-status', address=address)

    def get_balance(self, address: str):
        return self._assemble_cmd('gas get-balance', address=address)

    @with_endorsers
    def set_gas_admin(self, address: str = None, **kwargs):
        if address:
            return self._assemble_cmd('gas set-admin', address=address, **kwargs)
        else:
            return self._assemble_cmd('gas set-admin', **kwargs)

    def recharge_gas(self, address: str, amount: int, **kwargs):
        return self._assemble_cmd('gas recharge', address=address, amount=amount, **kwargs)

    def refund_gas(self, address: str, amount: int, **kwargs):
        return self._assemble_cmd('gas refund', address=address, amount=amount, **kwargs)

    def freeze_gas_account(self, address: str, **kwargs):
        return self._assemble_cmd('gas frozen', address=address, **kwargs)

    def unfreeze_gas_account(self, address: str, **kwargs):
        return self._assemble_cmd('gas unfrozen', address=address, **kwargs)


class CmcAddressUtil(BaseCmc):
    @staticmethod
    def pk_to_addr(cert_file_path: str, hash_type: int = 0):
        return f'./cmc address pk-to-addr {cert_file_path} --hash-type={hash_type}'

    @staticmethod
    def cert_to_addr(cert_file_path: str):
        return f'./cmc address cert-to-addr {cert_file_path}'

    @staticmethod
    def hex_to_addr(hex: str, hash_type: int = 0):
        return f'./cmc address hex-to-addr {hex} --hash-type={hash_type}'

    @staticmethod
    def name_to_addr(name: str):
        return f'./cmc address name-to-addr {name}'


class CmcKeyUtil(BaseCmc):
    @staticmethod
    def gen_private_key(name: str, algo: str = 'ECC_P256', path='./'):
        return f'./cmc key gen -a {algo} -n {name} -p {path}'


class CmcPerfTest(BaseCmc):
    @staticmethod
    def parallel_invoke(contract_name: str = 'counter', method: str = 'invoke', params: Union[dict, list] = None,
                        loop_num: int = 1, thread_num: int = 1, timeout: int = 100000, sleep_time: int = 1000,
                        climb_time: int = 5, hosts="127.0.0.1:12301",
                        auth_type: int = 3, hash_algorithm='SHA256', gas_limit: int = None):
        pairs = ''
        if isinstance(params, dict):
            pairs = json.dumps([{'key': key, 'value': value, 'unique': False} for key, value in params.items()])
            pairs = pairs.replace(' ', '').replace('"', '\\"')

        cmd = f'''./cmc parallel invoke \
    --contract-name={contract_name} \
    --method={method} \
    --pairs="{pairs}" \
    --loopNum={loop_num} \
    --threadNum={thread_num} \
    --timeout={timeout} \
    --sleepTime={sleep_time} \
    --climbTime={climb_time} \
    --hosts="{hosts}" \
    --printTime=5 \
    --use-tls=true \
    --showKey=false \
    --org-ids=wx-org1.chainmaker.org \
    --org-IDs=wx-org1.chainmaker.org \
    --user-keys=./testdata/crypto-config/wx-org1.chainmaker.org/user/client1/client1.tls.key \
    --user-crts=./testdata/crypto-config/wx-org1.chainmaker.org/user/client1/client1.tls.crt \
    --sign-keys=./testdata/crypto-config/wx-org1.chainmaker.org/user/client1/client1.sign.key \
    --sign-crts=./testdata/crypto-config/wx-org1.chainmaker.org/user/client1/client1.sign.crt \
    --ca-path="./testdata/crypto-config/wx-org1.chainmaker.org/ca"
        '''
        return cmd


class CmcDPosUtil(BaseCmc):
    def dpos_cert_to_addr(self, pubkey_cert_path: str):
        """用户公钥计算出用户的地址"""
        return self._assemble_cmd('cert userAddr', pubkey_cert_path=pubkey_cert_path)

    @staticmethod
    def get_nid(node_pk_path: str):
        """用户公钥计算出用户的地址"""
        return f'./cmc cert nid --node-pk-path={node_pk_path}'


class CmcDPosErc20(BaseCmc):
    def owner(self):
        return self._assemble_cmd('client contract system owner',
                                  chain_id=self.chain_id)

    def decimals(self):
        return self._assemble_cmd('client contract system decimals',
                                  chain_id=self.chain_id)

    def total(self):
        return self._assemble_cmd('client contract system total',
                                  chain_id=self.chain_id)

    def balance_of(self, address: str):
        return self._assemble_cmd('client contract system balance-of', address=address,
                                  chain_id=self.chain_id)

    def mint(self, address: str, amount: int):
        """增发Token"""
        return self._assemble_cmd('client contract system mint', address=address, amount=amount, chain_id=self.chain_id)

    def transfer(self, address: str, amount: int):
        """转账"""
        return self._assemble_cmd('client contract system transfer', address=address, amount=amount,
                                  chain_id=self.chain_id)


class CmcDPosStake(BaseCmc):
    def get_all_candidates(self):
        return self._assemble_cmd('client contract system all-candidates', chain_id=self.chain_id)

    def get_validator(self, address: str):
        return self._assemble_cmd('client contract system get-validator', address=address, chain_id=self.chain_id)

    def delegate(self, address: str, amount: int):
        """抵押权益到验证人"""
        return self._assemble_cmd('client contract system delegate', address=address, amount=amount,
                                  chain_id=self.chain_id, sync_result='true')

    def get_delegations_by_address(self, address: str):
        """查询指定地址的抵押信息"""
        return self._assemble_cmd('client contract system get-delegations-by-address', address=address,
                                  chain_id=self.chain_id)

    def get_user_delegation_by_validator(self, delegator: str, validator: str):
        """查询指定验证人的抵押信息"""
        return self._assemble_cmd('client contract system get-user-delegation-by-validator', delegator=delegator,
                                  validator=validator, chain_id=self.chain_id)

    def undelegate(self, address: str, amount: int):
        """从验证人解除抵押的权益"""
        return self._assemble_cmd('client contract system undelegate', address=address, amount=amount,
                                  chain_id=self.chain_id, sync_result='true')

    def get_epoch_by_id(self, epoch_id: int):
        """查询指定世代信息"""
        return self._assemble_cmd('client contract system read-epoch-by-id', epoch_id=epoch_id, chain_id=self.chain_id)

    def get_last_epoch(self):
        """查询当前世代信息"""
        return self._assemble_cmd('client contract system read-latest-epoch',
                                  chain_id=self.chain_id)

    def get_node_id(self, address: str):
        """Stake合约中查询验证人的NodeID"""
        return self._assemble_cmd('client contract system get-node-id', address=address,
                                  chain_id=self.chain_id)

    def set_node_id(self, node_id: str):
        """Stake合约中设置验证人的NodeID"""
        return self._assemble_cmd('client contract system set-node-id', node_id=node_id,
                                  chain_id=self.chain_id, sync_result='true')

    def get_min_self_delegation(self):
        """查询验证人节点的最少自我抵押数量"""
        return self._assemble_cmd('client contract system min-self-delegation',
                                  chain_id=self.chain_id)

    def get_epoch_validator_number(self):
        """查询世代中的验证人数"""
        return self._assemble_cmd('client contract system validator-number',
                                  chain_id=self.chain_id)

    def get_epoch_block_number(self):
        """查询世代中的区块数量"""
        return self._assemble_cmd('client contract system epoch-block-number',
                                  chain_id=self.chain_id)

    def get_stake_contract_address(self):
        """查询Stake合约的系统地址"""
        return self._assemble_cmd('client contract system system-address',
                                  chain_id=self.chain_id)

    def get_unbounding_epoch_number(self):
        """查询收到解质押退款间隔的世代数"""
        return self._assemble_cmd('client contract system unbonding-epoch-number',
                                  chain_id=self.chain_id)


class Cmc(CmcChainConfig, CmcChainQuery, CmcCertManage, CmcCertAliasManage, CmcUserContract, CmcSystemContract,
          CmcMultiSign, CmcPrivateKeyManage, CmcArchive, CmcTxPool, CmcGasManage, CmcAddressUtil, CmcKeyUtil,
          CmcDPosUtil, CmcDPosErc20, CmcDPosStake):

    def get_cmc_from_method(self, method: str, *args, **kwargs):
        if hasattr(self, method):
            return getattr(self, method)(*args, **kwargs)


if __name__ == '__main__':
    print(Cmc().contract_name_to_address('counter', address_type=2))
    # print(Cmc().chain_config_enable_or_disable_gas(False))
