#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   conftest.py
# @Function     :   pytest框架测试配置
import uuid
from datetime import datetime
from pathlib import Path

import pytest

from chainmaker.chain_client import ChainClient, ChainClientWithEndorsers
from chainmaker.keys import SystemContractName, ContractManageMethod, ParamKey
from chainmaker.utils import common
from chainmaker.utils import file_utils
from chainmaker.utils.common import gen_rand_contract_name
from chainmaker.utils.contract_utils import Contract
from chainmaker.utils.crypto_config_utils import CryptoConfig, load_crypto_config
from chainmaker.utils.result_utils import assert_success


NOW = datetime.now()


def pytest_configure(config):
    """Pytest初始化配置钩子函数"""
    root_dir = config.rootpath  # 获取项目根目录

    # 获取pytest.ini文件中的log_file配置项
    log_file = config.getini('log_file')
    if log_file:  # 如果存在该配置项2
        # 修改命令行选项中的log-file参数为日志绝对路径
        config.option.log_file = root_dir / NOW.strftime(log_file)


@pytest.fixture(scope='session')
def data_dir(request):
    return request.config.rootdir / 'testdata'


@pytest.fixture(scope='session')
def sdk_config_path(data_dir) -> Path:
    return data_dir / 'sdk_config.yml'


@pytest.fixture(scope='session')
def crypto_config_path(data_dir):
    """返回crypto-config文件路径"""
    return data_dir / 'crypto-config'


@pytest.fixture(scope='session')
def host():
    return "9.134.217.247"

#
# @pytest.fixture(scope='session')
# def host_config(env_vars):
#     return {'host': env_vars.get('host'),
#             'port': env_vars.get('port', 22),
#             'user': env_vars.get('user', 'root'),
#             'password': env_vars.get('password'),
#             'workspace': env_vars.get('workspace')}


@pytest.fixture(scope='session')
def crypto_config(crypto_config_path, host, env_vars) -> CryptoConfig:
    start_rpc_port = env_vars.get('rpc_start_port', 12301)
    return load_crypto_config(crypto_config_path, host=host, rpc_start_port=start_rpc_port)



@pytest.fixture(scope='module')
def cc(sdk_config_path) -> ChainClientWithEndorsers:
    cc = ChainClientWithEndorsers.from_conf(sdk_config_path)
    yield cc
    cc.stop()


@pytest.fixture(scope='session')
def endorsers_config(crypto_config_path):
    return [{'org_id': 'wx-org1.chainmaker.org',
             'user_sign_crt_file_path': f'{crypto_config_path}/wx-org1.chainmaker.org/user/admin1/admin1.sign.crt',
             'user_sign_key_file_path': f'{crypto_config_path}/wx-org1.chainmaker.org/user/admin1/admin1.sign.key'},
            {'org_id': 'wx-org2.chainmaker.org',
             'user_sign_crt_file_path': f'{crypto_config_path}/wx-org2.chainmaker.org/user/admin1/admin1.sign.crt',
             'user_sign_key_file_path': f'{crypto_config_path}/wx-org2.chainmaker.org/user/admin1/admin1.sign.key'},
            {'org_id': 'wx-org3.chainmaker.org',
             'user_sign_crt_file_path': f'{crypto_config_path}/wx-org3.chainmaker.org/user/admin1/admin1.sign.crt',
             'user_sign_key_file_path': f'{crypto_config_path}/wx-org3.chainmaker.org/user/admin1/admin1.sign.key'},
            {'org_id': 'wx-org4.chainmaker.org',
             'user_sign_crt_file_path': f'{crypto_config_path}/wx-org4.chainmaker.org/user/admin1/admin1.sign.crt',
             'user_sign_key_file_path': f'{crypto_config_path}/wx-org4.chainmaker.org/user/admin1/admin1.sign.key'},
            ]


@pytest.fixture()
def fact(data_dir, cc):
    """rust-fact存证合约"""
    contract_name = 'fact'
    byte_code_path = data_dir / 'byte_codes/rust-fact-2.0.0.wasm'
    runtime_type = 'WASMER'
    if not cc.check_contract(contract_name):
        res = cc.create_contract(contract_name, byte_code_path, runtime_type)
        assert_success(res)
    return contract_name
#
#
# @pytest.fixture()
# def rust_api(data_dir, cc):
#     """rust-fact存证合约"""
#     contract_name = 'rust_api'
#     byte_code_path = data_dir / 'byte_codes/rust-api-2.0.0.wasm'
#     runtime_type = 'WASMER'
#     if not cc.check_contract(contract_name):
#         res = cc.create_contract(contract_name, byte_code_path, runtime_type)
#         assert_success(res)
#     return contract_name

#
# @pytest.fixture()
# def rust_fvt(data_dir, cc):
#     """rust-fact存证合约"""
#     contract_name = 'rust_fvt'
#     byte_code_path = data_dir / 'byte_codes/rust-fvt.wasm'
#     runtime_type = 'WASMER'
#     if not cc.check_contract(contract_name):
#         res = cc.create_contract(contract_name, byte_code_path, runtime_type)
#         assert_success(res)
#     return contract_name


@pytest.fixture()
def counter(data_dir, cc):
    """rust-counter合约"""
    contract_name = 'counter'
    byte_code_path = data_dir / 'byte_codes/rust-counter-2.0.0.wasm'
    runtime_type = 'WASMER'
    if not cc.check_contract(contract_name):
        res = cc.create_contract(contract_name, byte_code_path, runtime_type)
        assert_success(res)
    return contract_name


# @pytest.fixture()
# def asset(data_dir, cc):
#     """rust-asset转账合约"""
#     contract_name = 'asset'
#     byte_code_path = data_dir / 'byte_codes/rust-asset-2.0.0.wasm'
#     runtime_type = 'WASMER'
#     params = {"issue_limit": "100000000", "total_supply": "100000000"}
#     if not cc.check_contract(contract_name):
#         res = cc.create_contract(contract_name, byte_code_path, runtime_type, params=params)
#         assert_success(res)
#     return contract_name


@pytest.fixture()
def balance(data_dir, cc):
    """evm ledger-balance合约"""
    contract_name = 'balance'
    byte_code_path = data_dir / 'byte_codes/ledger_balance.bin'
    runtime_type = 'EVM'
    if not cc.check_contract(contract_name):
        res = cc.create_contract(contract_name, byte_code_path, runtime_type)
        assert_success(res)
    return contract_name


# @pytest.fixture()
# def evm_counter(data_dir, cc):
#     contract_name = 'evm_counter'
#     byte_code_path = data_dir / 'byte_codes/counter_evm.bin'
#     runtime_type = 'EVM'
#     if not cc.check_contract(contract_name):
#         res = cc.create_contract(contract_name, byte_code_path, runtime_type)
#         assert_success(res)
#     return contract_name
#
#
# @pytest.fixture()
# def tinygo_counter(data_dir, cc):
#     contract_name = 'tinygo_counter'
#     byte_code_path = data_dir / 'byte_codes/counter_tinygo.wasm'
#     runtime_type = 'GASM'
#     if not cc.check_contract(contract_name):
#         res = cc.create_contract(contract_name, byte_code_path, runtime_type)
#         assert_success(res)
#     return contract_name

#
# @pytest.fixture()
# def cpp_counter(data_dir, cc):
#     contract_name = 'cpp_counter'
#     byte_code_path = data_dir / 'byte_codes/cpp_counter.wasm'
#     runtime_type = 'WXWM'
#     if not cc.check_contract(contract_name):
#         res = cc.create_contract(contract_name, byte_code_path, runtime_type)
#         assert_success(res)
#     return contract_name

#
# @pytest.fixture()
# def tinygo_api(data_dir, cc):
#     """rust-fact存证合约"""
#     contract_name = 'tinygo_api'
#     byte_code_path = data_dir / 'byte_codes/tinygo-api.wasm'
#     runtime_type = 'GASM'
#     if not cc.check_contract(contract_name):
#         res = cc.create_contract(contract_name, byte_code_path, runtime_type)
#         assert_success(res)
#     return contract_name


# @pytest.fixture()
# def tinygo_fvt(data_dir, cc):
#     """rust-fact存证合约"""
#     contract_name = 'tinygo_fvt'
#     byte_code_path = data_dir / 'byte_codes/tinygo-fvt.wasm'
#     runtime_type = 'GASM'
#     if not cc.check_contract(contract_name):
#         res = cc.create_contract(contract_name, byte_code_path, runtime_type)
#         assert_success(res)
#     return contract_name

#
# @pytest.fixture()
# def docker_go_api_230(data_dir, cc):
#     contract_name = 'docker_go_api_230'
#     byte_code_path = data_dir / 'byte_codes/docker-go-api-2.3.0.7z'
#     runtime_type = 'DOCKER_GO'
#     if not cc.check_contract(contract_name):
#         res = cc.create_contract(contract_name, byte_code_path, runtime_type)
#         assert_success(res)
#     return contract_name
#
#
# @pytest.fixture()
# def docker_go_api_223(data_dir, cc):
#     contract_name = 'docker_go_api_223'
#     byte_code_path = data_dir / 'byte_codes/docker-go-api-2.2.3.7z'
#     runtime_type = 'DOCKER_GO'
#     if not cc.check_contract(contract_name):
#         res = cc.create_contract(contract_name, byte_code_path, runtime_type)
#         assert_success(res)
#     return contract_name



@pytest.fixture()
def send_tx(cc, fact):
    """发送N笔交易"""

    def invoke_fact_save(count=1, with_sync_result=True, tx_id=None):
        contract_name = 'fact'
        method = 'save'
        params = {"file_name": "name007", "file_hash": "ab3456df5799b87c77e7f88", "time": "6543234"}
        results = []
        for i in range(count):
            res = cc.invoke_contract(contract_name, method, params, tx_id=tx_id, with_sync_result=with_sync_result)
            results.append(res)
        return results

    return invoke_fact_save


@pytest.fixture()
def last_block_tx_id(cc: ChainClient, fact):
    """获取最新区块的交易id"""
    res = cc.get_last_block()
    tx_id = res.block.txs[0].payload.tx_id
    print(f'tx_id: {tx_id}')
    return tx_id


@pytest.fixture()
def last_block_hash(cc: ChainClient):
    """获取最新区块hash值"""
    res = cc.get_last_block()
    block_hash = res.block.header.block_hash.hex()  # 要转为hex
    print('block_hash:', block_hash)
    return block_hash


@pytest.fixture()
def random_contract_name():
    return common.gen_rand_contract_name()


@pytest.fixture()
def random_alias():
    return str(uuid.uuid4()).replace('-', '_')


@pytest.fixture()
def multi_sign_tx_id(cc, counter):
    # byte_code_path = fact.byte_code_path
    counter.contract_name = gen_rand_contract_name()
    params = {
        ParamKey.SYS_CONTRACT_NAME: SystemContractName.CONTRACT_MANAGE,
        ParamKey.SYS_METHOD: ContractManageMethod.INIT_CONTRACT,
        ParamKey.CONTRACT_NAME: counter.contract_name,
        ParamKey.CONTRACT_VERSION: counter.version,
        ParamKey.CONTRACT_BYTECODE: file_utils.read_file_bytes(counter.byte_code_path),
        ParamKey.CONTRACT_RUNTIME_TYPE: counter.runtime_type,
    }

    payload = cc.create_multi_sign_req_payload(params)
    res = cc.send_request_with_sync_result(payload, with_sync_result=True)
    return res.tx_id


@pytest.fixture()
def contracts(cc, endorsers_config, data_dir):
    contracts_ini_file = data_dir / 'contracts.ini'
    return Contract.load_contracts_from_ini(cc, contracts_ini_file, contract_dir=data_dir)
#
#
# @pytest.fixture()
# def send_tx(cc, fact):
#     """发送N笔交易"""
#     def invoke_fact_save(count=1, with_sync_result=True, tx_id=None):
#         contract_name = 'fact'
#         method = 'save'
#         params = {"file_name": "name007", "file_hash": "ab3456df5799b87c77e7f88", "time": "6543234"}
#         results = []
#         for i in range(count):
#             res = cc.invoke_contract(contract_name, method, params, tx_id=tx_id, with_sync_result=with_sync_result)
#             results.append(res)
#         return results
#
#     return invoke_fact_save

#
# @pytest.fixture()
# def last_block_tx_id(cc: ChainClient, fact):
#     """获取最新区块的交易id"""
#     res = cc.get_last_block()
#     tx_id = res.block.txs[0].payload.tx_id
#     print(f'tx_id: {tx_id}')
#     return tx_id

#
# @pytest.fixture()
# def last_block_hash(cc: ChainClient):
#     """获取最新区块hash值"""
#     res = cc.get_last_block()
#     block_hash = res.block.header.block_hash.hex()  # 要转为hex
#     print('block_hash:', block_hash)
#     return block_hash
#
#
# @pytest.fixture()
# def random_contract_name():
#     return gen_rand_contract_name()

#
# @pytest.fixture()
# def random_alias():
#     return str(uuid.uuid4()).replace('-', '_')

#
# @pytest.fixture()
# def multi_sign_tx_id(cc, counter):
#     # byte_code_path = fact.byte_code_path
#     counter.contract_name = gen_rand_contract_name()
#     params = {
#         ParamKey.SYS_CONTRACT_NAME: SystemContractName.CONTRACT_MANAGE,
#         ParamKey.SYS_METHOD: ContractManageMethod.INIT_CONTRACT,
#         ParamKey.CONTRACT_NAME: counter.contract_name,
#         ParamKey.CONTRACT_VERSION: counter.version,
#         ParamKey.CONTRACT_BYTECODE: file_utils.read_file_bytes(counter.byte_code_path),
#         ParamKey.CONTRACT_RUNTIME_TYPE: counter.runtime_type,
#     }
#     payload = cc.create_multi_sign_req_payload(params)
#     res = cc.send_request_with_sync_result(payload, with_sync_result=True)
#     return res.tx_id


@pytest.fixture()
def org4_org_id():
    return 'wx-org4.chainmaker.org'


@pytest.fixture()
def org4_consensus1_node_id(crypto_config_path, org4_org_id):
    node_id_file = f'{crypto_config_path}/{org4_org_id}/node/consensus1/consensus1.nodeid'
    with open(node_id_file, encoding='utf-8') as f:
        return f.read().strip()


@pytest.fixture()
def org4_ca_cert_pem(crypto_config_path, org4_org_id):
    ca_cert_file = f'{crypto_config_path}/{org4_org_id}/ca/ca.crt'
    with open(ca_cert_file, encoding='utf-8') as f:
        return f.read().strip()
