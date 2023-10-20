#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   contract_utils.py
# @Function     :   常用合约操作封装
import logging
import os
import time
from configparser import ConfigParser
from pathlib import Path
from typing import Union, Dict

from chainmaker import ChainClient, ChainClientWithEndorsers
from chainmaker.keys import RuntimeType, ContractResultType
from chainmaker.protos.common import contract_pb2
from chainmaker.utils import evm_utils, file_utils
from chainmaker.utils.common import gen_rand_contract_name, ensure_enum
from chainmaker.utils.result_utils import check_response, parse_result, msg_to_dict

DEFAULT_INIT_CONTRACT_VERSION = '1.0'
DEFAULT_UPGRADE_CONTRACT_VERSION = '2.0'


class Contract(object):
    """长安链合约基础类"""
    _logger = logging.getLogger(__name__)

    def __init__(self, cc: ChainClientWithEndorsers, byte_code_path: str, runtime_type: Union[RuntimeType, str] = None,
                 contract_name: str = None, params: dict = None, version: str = None,
                 upgrade_byte_code_path: str = None, methods: list = None, init=False) -> None:
        self._cc = cc
        self.contract_name = contract_name or gen_rand_contract_name()
        self.byte_code_path = byte_code_path
        self.runtime_type = ensure_enum(runtime_type, RuntimeType)
        self.params = params
        self.version = version or '1.0'
        self.upgrade_byte_code_path = upgrade_byte_code_path or self.byte_code_path
        self.methods = methods

        self._contract_address = None

        self._should_calc_evm_contract_name = False  # todo 2.2.1版本以下需要转换evm合约名称
        if init is True:
            self.create()

    def __repr__(self):
        return '<Contract %s runtime_type=%s>' % (self.contract_name, self.runtime_type)

    @property
    def exists(self):
        return self._cc.get_contract_info(self.contract_name) is not None

    @property
    def contract_info(self) -> contract_pb2.Contract:
        """链上合约信息"""
        return msg_to_dict(self._cc.get_contract_info(self.contract_name))

    @property
    def creator_info(self):
        contract_info = self.contract_info
        if contract_info:
            return contract_info['creator']
        return None

    @property
    def contract_address(self) -> Union[str, None]:
        """链上合约地址"""
        if self._contract_address is None:
            contract_info = self.contract_info
            if contract_info:
                self._contract_address = self.contract_info['address']
        return self._contract_address

    @property
    def contract_version(self) -> Union[str, None]:
        """链上合约版本"""
        contract_info = self.contract_info
        if contract_info:
            return contract_info['version']

    def _gen_new_contract_version(self, increase: float = 1.0) -> str:
        """生成合约信版本号，默认原版本+1"""
        version = self.contract_version
        return str(float(version) + increase)

    def init(self, contract_name: str = None, runtime_type=None, params=None, version=None, gas_limit: int = None,
             with_sync_result=None) -> "Contract":
        """
        创建合约
        :param params:
        :param runtime_type:
        :param version:
        :param with_sync_result:
        :param contract_name: 指定合约名
        :param gas_limit: Gas交易限制
        :return: 合约对象本身
        """
        if contract_name is not None:
            self.contract_name = contract_name

        if runtime_type is None:
            runtime_type = self.runtime_type

        if version is None:
            version = self.version

        if params is None:
            params = self.params

        if not self.exists:
            res = self._cc.create_contract(self.contract_name, self.byte_code_path,
                                           runtime_type, params, version=version, gas_limit=gas_limit,
                                           with_sync_result=with_sync_result)
            check_response(res)
            if with_sync_result is False:
                for i in range(self._cc._retry_limit):
                    if self.exists:
                        break
                    time.sleep(self._cc._retry_interval)
        return self

    def create(self, contract_name: str = None, runtime_type=None, params=None, version=None, gas_limit: int = None,
               with_sync_result=None) -> "Contract":
        """
         创建合约
        :param params:
        :param with_sync_result:
        :param version:
        :param runtime_type:
        :param contract_name: 指定合约名
        :param gas_limit: Gas交易限制
        :return: 合约对象本身
        """
        return self.init(contract_name, runtime_type, params, version, gas_limit, with_sync_result)

    def upgrade(self, byte_code_path: str = None, runtime_type: RuntimeType = None,
                params=None, version: str = None, gas_limit: int = None) -> Union["Contract"]:
        """
        升级合约
        :param gas_limit:
        :param byte_code_path: 升级使用的byte_code文件路径
        :param version: 升级后的版本，为None时自动在当前版本上加1.0
        :param runtime_type: 合约类型，为None时，使用原有合约类型，支持升级为其他合约类型
        :param params: 合约参数，为None使用原有合约参数，支持升级为其他合约类型
        :return: 响应信息
        """
        upgrade_byte_code_path = byte_code_path or self.upgrade_byte_code_path or self.byte_code_path
        new_version = version or self._gen_new_contract_version()
        runtime_type = runtime_type or self.runtime_type
        params = params or self.params
        assert self._cc.endorsers is not None, '客户端缺少背书endorsers配置'
        res = self._cc.upgrade_contract(self.contract_name, upgrade_byte_code_path,
                                        runtime_type, params, version=new_version, gas_limit=gas_limit)
        check_response(res)
        return self

    def invoke(self, method, params=None, gas_limit: int = None,
               result_type: ContractResultType = ContractResultType.STRING,
               by_address=False, only_message=False, with_sync_result=True):
        """调用合约方法"""
        if self.runtime_type == RuntimeType.EVM:
            method, params = evm_utils.calc_evm_method_params(method, params)
        contract_name = self.contract_address if by_address is True else self.contract_name

        res = self._cc.invoke_contract(contract_name, method, params, gas_limit=gas_limit,
                                       with_sync_result=with_sync_result)
        if only_message:
            return res.contract_result.message
        # check_response(res)
        return parse_result(res, result_type)

    def query(self, method, params=None, result_type: ContractResultType = ContractResultType.STRING, by_address=False):
        """查询合约方法"""
        if self.runtime_type == RuntimeType.EVM:
            method, params = evm_utils.calc_evm_method_params(method, params)
        contract_name = self.contract_address if by_address is True else self.contract_name
        res = self._cc.query_contract(contract_name, method, params)
        # check_response(res)
        return parse_result(res, result_type)

    def freeze(self):
        """冻结合约"""
        res = self._cc.freeze_contract(self.contract_name)
        check_response(res)
        return self

    def unfreeze(self):
        """解冻合约"""
        res = self._cc.unfreeze_contract(self.contract_name)
        check_response(res)
        return self

    def revoke(self):
        res = self._cc.revoke_contract(self.contract_name)
        check_response(res)
        return self

    def freeze_and_unfreeze(self):
        self.freeze()
        self.unfreeze()
        return self

    @classmethod
    def from_conf(cls, cc: ChainClient, contract_config: dict,
                  contract_dir: str = None) -> "Contract":
        """
        从合约配置中加载合约
        :param cc:
        :param contract_config: 链配置
            {'byte_code_path': '', runtime_type: '', 'contact_name': '', 'params': '', 'version': '', ....}
        :param contract_dir: 合约文件基础路径
        :return: 合约对象
        """
        byte_code_path = contract_config.get('byte_code_path')
        upgrade_byte_code_path = contract_config.get('upgrade_byte_code_path')
        if contract_dir is not None:
            contract_config['byte_code_path'] = os.path.abspath(os.path.join(contract_dir, byte_code_path))
            if upgrade_byte_code_path:
                contract_config['upgrade_byte_code_path'] = os.path.abspath(
                    os.path.join(contract_dir, upgrade_byte_code_path))
        contract = cls(cc, **contract_config)

        return contract

    @classmethod
    def load_contracts_from_yaml(cls, cc: ChainClient, contracts_yml_file: Union[Path, str],
                                 contract_dir: str = None) -> Dict[str, "Contract"]:
        """
        加载合约配置文件
        :param cc: 链客户端
        :param contracts_yml_file: YAML格式合约配置文件炉具
        :param contract_dir: 合约byte_code文件基础路径
        :return: 合约对象列表
        """
        contracts_config = file_utils.load_yaml(contracts_yml_file)
        return {key: cls.from_conf(cc, contract_config, contract_dir) for key, contract_config in
                contracts_config.items()}

    @classmethod
    def load_contracts_from_ini(cls, cc: ChainClient, contracts_ini_file: Union[Path, str],
                                contract_dir: str = None) -> Dict[str, "Contract"]:
        """加载合约配置文件"""
        contracts = {}
        contracts_config = ConfigParser()
        contracts_config.read(contracts_ini_file)

        for section in contracts_config.sections():
            contract_config = dict(contracts_config.items(section))
            contract = cls.from_conf(cc, contract_config, contract_dir)
            contracts[section] = contract
        return contracts

