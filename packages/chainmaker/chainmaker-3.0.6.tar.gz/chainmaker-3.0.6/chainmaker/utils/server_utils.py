#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   node_server_utils.py
# @Function     :   chainmaker节点服务实用方法
import os
import re
import shutil
import threading
import time
from pathlib import Path
from typing import List, Union

from chainmaker.chain_client import ChainClientWithEndorsers
from chainmaker.keys import (ConsensusType, AddrType, DbProvider, DbType, CryptoEngine, NetProvider, RpcTlsMode,
                             TxFilterType, AuthType)
from chainmaker.utils.common import ensure_enum
from chainmaker.utils.crypto_config_utils import CryptoConfig, load_crypto_config
from chainmaker.utils.result_utils import assert_success, wait_chainmaker_is_ok

try:
    from hostz import Host, Local
except ImportError:
    print('please install hostz: pip install hostz')
    raise

try:
    from logz import log
except ImportError:
    print('please install logz: pip install logz')
    raise

DEFAULT_NODES = ('node1', 'node2', 'node3', 'node4')
DEFAULT_DNS = 'root:password@tcp(127.0.0.1:3306)/'
DEFAULT_TIKV_URL = '127.0.0.1:2379'
MODIFY_DB_LIST = ('blockdb', 'statedb', 'historydb', 'resultdb')  # contract_eventdb 不修改


def get_release_paths_by_chainmaker_go_path(host: Host, chainmaker_go_path: str):
    """从标准chainmaker-go/build/release目录得到有序的节点release路径列表"""
    build_release_path = f'{chainmaker_go_path}/build/release'
    result = host.execute('ls -d */', workspace=build_release_path)
    if 'No such file or directory' in result:
        raise Exception('No release packages in chainmaker-go/build')
    result = result.split()
    if 'node' in result[0]:
        release_dirs = sorted(result, key=lambda x: int(x.split('-')[2].lstrip('node').rstrip('/') or 0))
    else:
        release_dirs = sorted(result, key=lambda x: int(x.split('-')[3].lstrip('org').rstrip('.chainmaker.org/') or 0))
    release_paths = [f'{build_release_path}/{item}' for item in release_dirs]
    return release_paths


def download_crypto_config(host: Host, chainmaker_go_path: str, crypto_config_path: str, force: bool = True):
    """下载crypto-config到本地"""
    if os.path.exists(crypto_config_path):
        if force is True:
            shutil.rmtree(crypto_config_path, ignore_errors=True)
    else:
        host.get(f'{chainmaker_go_path}/build/crypto-config', crypto_config_path)


class ChainMakerNode:
    """长安链服务节点"""

    def __init__(self, index: int, host: Host, release_path: str, rpc_port: int = None, p2p_port: int = None,
                 crypto_config: CryptoConfig = None, cc: ChainClientWithEndorsers = None):
        self.index = index
        self.host = host
        self.release_path = release_path.rstrip('/')
        self.name = f'node{index + 1}'
        self.org_id = self._guess_org_id_from_release_path(self.release_path)
        if self.org_id == 'public':
            self.org_id = f'node{index + 1}'

        self.rpc_port = rpc_port or (12301 + index)
        self.p2p_port = p2p_port or (11301 + index)
        self.crypto_config = crypto_config
        self.crypto_config_node = crypto_config.get_node(f'org{index + 1}consensus1') or crypto_config.get_node(
            f'node{index + 1}')
        self.cc = cc
        self._logger = log

        self._bin_path = '%s/bin' % self.release_path
        self._bc1_yml_path = '%s/config/%s/chainconfig/bc1.yml' % (self.release_path, self.org_id)
        self._bc1_yml_bak_path = self._bc1_yml_path.replace('bc1.yml', 'bc1_bak.yml')
        self._chainmaker_yml_path = '%s/config/%s/chainmaker.yml' % (self.release_path, self.org_id)
        self._chainmaker_yml_bak_path = self._chainmaker_yml_path.replace('chainmaker.yml', 'chainmaker_bak.yml')
        self._log_yml_path = '%s/config/%s/log.yml' % (self.release_path, self.org_id)
        self._log_yml_bak_path = self._log_yml_path.replace('log.yml', 'log_bak.yml')
        self._cached_bc1_config = None
        self._cached_chainmaker_config = None

    def __repr__(self):
        return '<ChainMakerNode %s>' % self.name

    def _info(self, msg: str):
        self._logger.info('[Sdk] %s' % msg)

    @property
    def node_id(self) -> str:
        return self.crypto_config_node.node_id

    @property
    def sign_key_bytes(self) -> bytes:
        return self.crypto_config_node.sign_key_bytes

    @property
    def sign_cert_bytes(self) -> bytes:
        return self.crypto_config_node.sign_cert_bytes

    @property
    def tls_key_bytes(self) -> bytes:
        return self.crypto_config_node.tls_key_bytes

    @property
    def tls_cert_bytes(self) -> bytes:
        return self.crypto_config_node.tls_cert_bytes

    @property
    def org_ca_cert_bytes(self) -> bytes:
        return self.crypto_config_node.org_ca_cert_bytes

    @property
    def trust_root_crt(self) -> str:
        return self.crypto_config_node.trust_root_crt

    @property
    def org_ca_key_bytes(self) -> bytes:
        return self.crypto_config_node.org_ca_key_bytes

    @property
    def pid(self) -> Union[None, int]:
        result = self.host.run("lsof -n -i :%s | grep LISTEN | awk '{print $2}'" % self.rpc_port)
        if result:
            return int(result)

    @property
    def is_active(self) -> bool:
        return self.pid is not None

    @property
    def bc1_config(self) -> dict:
        """
        {'account_config': {'default_gas': 0, 'enable_gas': False, 'gas_count': 0},
         'auth_type': 'permissionedWithCert',
         'block': {'block_interval': 10,
                   'block_size': 10,
                   'block_tx_capacity': 100,
                   'tx_timeout': 600,
                   'tx_timestamp_verify': True},
         'chain_id': 'chain1',
         'consensus': {'ext_config': None,
                       'nodes': [{'node_id': ['QmRw3HFFtfKTQ9pXcYGTuSQzsCFLQpNNmmP4bf9txBPYQP'],
                                  'org_id': 'wx-org1.chainmaker.org'},
                                 {'node_id': ['QmVcufiGxrwzjjM7hH96ZsRPxmDEXxBKHPzk4bQRJnvo4s'],
                                  'org_id': 'wx-org2.chainmaker.org'},
                                 {'node_id': ['QmRCztSr9YsWaaWRSjXAodKwXKPcgAvLPnLDKrtoHRjN4u'],
                                  'org_id': 'wx-org3.chainmaker.org'},
                                 {'node_id': ['QmVt7fkkdTDU2mZuWKFxwt3P7hAdEDkCTK1Yme3EwdgNVM'],
                                  'org_id': 'wx-org4.chainmaker.org'}],
                       'type': 3},
         'contract': {'enable_sql_support': False},
         'core': {'enable_conflicts_bit_window': True,
                  'enable_sender_group': False,
                  'tx_scheduler_timeout': 10,
                  'tx_scheduler_validate_timeout': 10},
         'crypto': {'hash': 'SHA256'},
         'disabled_native_contract': None,
         'resource_policies': [{'policy': {'org_list': None,
                                           'role_list': ['admin'],
                                           'rule': 'SELF'},
                                'resource_name': 'CHAIN_CONFIG-NODE_ID_UPDATE'},
                               {'policy': {'org_list': None,
                                           'role_list': ['admin'],
                                           'rule': 'MAJORITY'},
                                'resource_name': 'CHAIN_CONFIG-TRUST_ROOT_ADD'},
                               {'policy': {'org_list': None,
                                           'role_list': ['admin'],
                                           'rule': 'ANY'},
                                'resource_name': 'CHAIN_CONFIG-CERTS_FREEZE'},
                               {'policy': {'org_list': None,
                                           'role_list': None,
                                           'rule': 'ANY'},
                                'resource_name': 'CONTRACT_MANAGE-INIT_CONTRACT'}],
         'sequence': 0,
         'trust_roots': [{'org_id': 'wx-org4.chainmaker.org',
                          'root': ['../config/wx-org1.chainmaker.org/certs/ca/wx-org4.chainmaker.org/ca.crt']},
                         {'org_id': 'wx-org3.chainmaker.org',
                          'root': ['../config/wx-org1.chainmaker.org/certs/ca/wx-org3.chainmaker.org/ca.crt']},
                         {'org_id': 'wx-org2.chainmaker.org',
                          'root': ['../config/wx-org1.chainmaker.org/certs/ca/wx-org2.chainmaker.org/ca.crt']},
                         {'org_id': 'wx-org1.chainmaker.org',
                          'root': ['../config/wx-org1.chainmaker.org/certs/ca/wx-org1.chainmaker.org/ca.crt']}],
         'version': '2040000',
         'vm': {'addr_type': 2,
                'support_list': ['wasmer', 'gasm', 'evm', 'dockergo', 'wxvm']}}
        :return:
        """
        if self._cached_bc1_config is None:
            self._cached_bc1_config = self.host.load_yaml(self._bc1_yml_path)
        return self._cached_bc1_config

    @property
    def chainmaker_config(self) -> dict:
        """
        {'auth_type': 'permissionedWithCert',
         'blockchain': [{'chainId': 'chain1',
                         'genesis': '../config/wx-org1.chainmaker.org/chainconfig/bc1.yml'}],
         'consensus': {'raft': {'async_wal_save': True, 'snap_count': 10, 'ticker': 1}},
         'crypto_engine': 'tjfoc',
         'log': {'config_file': '../config/wx-org1.chainmaker.org/log.yml'},
         'monitor': {'enabled': False, 'port': 14321},
         'net': {'listen_addr': '/ip4/0.0.0.0/tcp/11301',
                 'provider': 'LibP2P',
                 'seeds': ['/ip4/127.0.0.1/tcp/11301/p2p/QmRw3HFFtfKTQ9pXcYGTuSQzsCFLQpNNmmP4bf9txBPYQP',
                           '/ip4/127.0.0.1/tcp/11302/p2p/QmVcufiGxrwzjjM7hH96ZsRPxmDEXxBKHPzk4bQRJnvo4s',
                           '/ip4/127.0.0.1/tcp/11303/p2p/QmRCztSr9YsWaaWRSjXAodKwXKPcgAvLPnLDKrtoHRjN4u',
                           '/ip4/127.0.0.1/tcp/11304/p2p/QmVt7fkkdTDU2mZuWKFxwt3P7hAdEDkCTK1Yme3EwdgNVM'],
                 'tls': {'cert_enc_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.enc.crt',
                         'cert_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.crt',
                         'enabled': True,
                         'priv_enc_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.enc.key',
                         'priv_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.key'}},
         'node': {'cert_cache_size': 1000,
                  'cert_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.sign.crt',
                  'fast_sync': {'enabled': True, 'min_full_blocks': 10},
                  'kms': {'address': 'kms.tencentcloudapi.com',
                          'enabled': False,
                          'ext_params': '',
                          'is_public': True,
                          'region': 'ap-guangzhou',
                          'sdk_scheme': 'https',
                          'secret_id': '',
                          'secret_key': ''},
                  'org_id': 'wx-org1.chainmaker.org',
                  'pkcs11': {'enabled': False,
                             'hash': 'SHA256',
                             'label': 'HSM',
                             'library': '/usr/local/lib64/pkcs11/libupkcs11.so',
                             'password': 11111111,
                             'session_cache_size': 10,
                             'type': 'pkcs11'},
                  'priv_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.sign.key'},
         'pprof': {'enabled': False, 'port': 24321},
         'rpc': {'blacklist': {'addresses': None},
                 'check_chain_conf_trust_roots_change_interval': 60,
                 'gateway': {'enabled': False, 'max_resp_body_size': 16},
                 'max_recv_msg_size': 100,
                 'max_send_msg_size': 100,
                 'port': 12301,
                 'provider': 'grpc',
                 'ratelimit': {'enabled': False,
                               'token_bucket_size': -1,
                               'token_per_second': -1,
                               'type': 0},
                 'subscriber': {'ratelimit': {'token_bucket_size': 100,
                                              'token_per_second': 100}},
                 'tls': {'cert_enc_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.enc.crt',
                         'cert_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.crt',
                         'mode': 'twoway',
                         'priv_enc_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.enc.key',
                         'priv_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.key'}},
         'scheduler': {'rwset_log': False},
         'storage': {'bigfilter_config': {'fp_rate': 1e-09,
                                          'redishosts_port': '127.0.0.1:6300,127.0.0.1:6301',
                                          'redis_password': 'abcpass',
                                          'tx_capacity': 1000000000},
                     'blockdb_config': {'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/block'},
                                        'provider': 'leveldb'},
                     'contract_eventdb_config': {'provider': 'sql',
                                                 'sqldb_config': {'dsn': 'root:password@tcp(127.0.0.1:3306)/',
                                                                  'sqldb_type': 'mysql'}},
                     'disable_block_file_db': False,
                     'disable_contract_eventdb': True,
                     'enable_bigfilter': False,
                     'enable_rwc': True,
                     'historydb_config': {'disable_account_history': True,
                                          'disable_contract_history': True,
                                          'disable_key_history': False,
                                          'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/history'},
                                          'provider': 'leveldb'},
                     'logdb_segment_async': False,
                     'logdb_segment_size': 128,
                     'resultdb_config': {'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/result'},
                                         'provider': 'leveldb'},
                     'rolling_window_cache_capacity': 55000,
                     'state_cache_config': {'clean_window': 1000000000,
                                            'hard_max_cache_size': 1024,
                                            'life_window': 3000000000000,
                                            'max_entry_size': 500},
                     'statedb_config': {'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/state'},
                                        'provider': 'leveldb'},
                     'store_path': '../data/wx-org1.chainmaker.org/ledgerData1',
                     'unarchive_block_height': 300000,
                     'write_block_type': 0},
         'tx_filter': {'birds_nest': {'cuckoo': {'bits_per_item': 11,
                                                 'key_type': 1,
                                                 'max_num_keys': 2000000,
                                                 'table_type': 0,
                                                 'tags_per_bucket': 2},
                                      'length': 10,
                                      'rules': {'absolute_expire_time': 172800},
                                      'snapshot': {'block_height': {'interval': 10},
                                                   'path': '../data/wx-org1.chainmaker.org/tx_filter',
                                                   'serialize_interval': 10,
                                                   'timed': {'interval': 10},
                                                   'type': 0}},
                       'sharding': {'birds_nest': {'cuckoo': {'bits_per_item': 11,
                                                              'key_type': 1,
                                                              'max_num_keys': 2000000,
                                                              'table_type': 0,
                                                              'tags_per_bucket': 2},
                                                   'length': 10,
                                                   'rules': {'absolute_expire_time': 172800}},
                                    'length': 5,
                                    'snapshot': {'block_height': {'interval': 10},
                                                 'path': '../data/wx-org1.chainmaker.org/tx_filter',
                                                 'serialize_interval': 10,
                                                 'timed': {'interval': 10},
                                                 'type': 0},
                                    'timeout': 60},
                       'type': 0},
         'txpool': {'batch_create_timeout': 50,
                    'batch_max_size': 100,
                    'common_queue_num': 8,
                    'is_dump_txs_in_queue': True,
                    'max_config_txpool_size': 10,
                    'max_txpool_size': 50000,
                    'pool_type': 'normal'},
         'vm': {'go': {'contract_engine': {'host': '127.0.0.1',
                                           'max_connection': 5,
                                           'port': 22351},
                       'data_mount_path': '../data/wx-org1.chainmaker.org/go',
                       'dial_timeout': 10,
                       'enable': False,
                       'log_in_console': False,
                       'log_level': None,
                       'log_mount_path': '../log/wx-org1.chainmaker.org/go',
                       'max_concurrency': 20,
                       'max_recv_msg_size': 100,
                       'max_send_msg_size': 100,
                       'protocol': None,
                       'runtime_server': {'port': 32351}}}}
        :return:
        """
        if self._cached_chainmaker_config is None:
            self._cached_chainmaker_config = self.host.load_yaml(self._chainmaker_yml_path)
        return self._cached_chainmaker_config

    @property
    def is_trust_root_on_chain(self) -> bool:
        if self.cc.auth_type == AuthType.Public:
            return True  # pk模式不管trust root
        return self.cc.chain_config_trust_root_check(self.org_id, self.trust_root_crt)

    @property
    def is_common_node(self) -> bool:
        return self.is_trust_root_on_chain and not self.cc.chain_config_consensus_node_id_check(self.org_id,
                                                                                                self.node_id)

    @property
    def is_consensus_node(self) -> bool:
        return self.is_trust_root_on_chain and self.cc.chain_config_consensus_node_id_check(self.org_id, self.node_id)

    @property
    def is_off_chain_node(self):
        return not self.is_trust_root_on_chain

    def start(self):
        """
        启动节点
        :return: 命令行输出结果
        """
        cmd = 'sh stop.sh full && sh start.sh full -y'
        output = self.host.run(cmd, workspace=self._bin_path)
        # time.sleep(2)  # 必须等待2秒, 不然重新使用会报错
        return output

    def stop(self, clean=False, stop_vm_container=True):
        """
        停止节点
        :return: 命令行输出结果
        """

        if stop_vm_container is True:
            self.host.run('sh stop.sh full', workspace=self._bin_path)
        else:
            self.host.run('sh stop.sh alone', workspace=self._bin_path)
        if clean is True:
            self._clean()

    def restart(self, clean=False, duration: int = None):
        """
        重启节点
        :param clean: 清理节点数据及日志  # todo 清理sql数据库
        :param duration: 节点停止后等待时间
        """
        if duration is None:
            if clean:
                self._clean()
            self.host.run('sh restart.sh full', workspace=self._bin_path)
        else:
            self.stop(clean)
            time.sleep(duration)
            self.start()

    def download_system_log(self, *keywords, output='system.log'):
        """下载system.log"""
        log_file = system_log_path = '%s/log/system.log' % self.release_path
        if keywords:
            keyword = '\|'.join(keywords)
            log_file = '/tmp/system.log'
            self.host.execute("grep '%s' %s > %s" % (keyword, system_log_path, log_file))
        self.host.get(log_file, output)

    def download_panic_log(self, output='panic.log'):
        """下载panic.log"""
        panic_log_path = '%s/panic.log' % self._bin_path
        self.host.get(panic_log_path, output)

    def restart_vm_go(self):
        container_name = f'VM-GO-{self.org_id}'
        container_id = self.host.run(f"docker stop docker ps | grep {container_name} | awk '{{print $1}}'")
        self.host.run(f'docker stop {container_id} && docker start {container_id}')

    def get_crypto_engine(self) -> CryptoEngine:
        crypto_engine = self.chainmaker_config.get('crypto_engine')
        return CryptoEngine[crypto_engine]

    def set_crypto_engine(self, crypto_engine: Union[CryptoEngine, str]):
        if isinstance(crypto_engine, CryptoEngine):
            crypto_engine = CryptoEngine.name
        self.modify_chainmaker_yml(crypto_engine=crypto_engine)

    def get_enable_docker_go(self) -> bool:
        return self.chainmaker_config.get('vm', {}).get('go', {}).get('enable')

    def set_enable_docker_go(self, enable: bool):
        self.modify_chainmaker_yml(vm={'go': {'enable': enable}})
        return self

    def get_enable_docker_vm(self) -> bool:
        return self.chainmaker_config.get('vm', {}).get('docker_go', {}).get('enable_dockervm')

    def set_enable_docker_vm(self, enable: bool):
        docker_go = {'enable_dockervm': enable,
                     'dockervm_mount_path': f'../data/{self.org_id}/docker-go',
                     'dockervm_log_path': f'../log/{self.org_id}/docker-go',
                     'log_in_console': True,
                     'log_level': 'DEBUG',
                     'uds_open': True,
                     'docker_vm_host': '127.0.0.1',
                     'docker_vm_port': 22451 + self.index,
                     'max_send_msg_size': 20,
                     'max_recv_msg_size': 20,
                     'max_connection': 5}

        self.modify_chainmaker_yml(vm={'docker_go': docker_go})
        return self

    def get_net_provider(self) -> NetProvider:
        net_provider = self.chainmaker_config.get('net', {}).get('provider')
        return NetProvider[net_provider]

    def set_net_provider(self, net_provider: Union[NetProvider, str]):
        if isinstance(net_provider, NetProvider):
            net_provider = net_provider.name
        self.modify_chainmaker_yml(net={'provider': net_provider})
        return self

    def get_enable_fast_sync(self) -> bool:
        return self.chainmaker_config.get('node', {}).get('fast_sync', {}).get('enabled')

    def set_enable_fast_sync(self, enable: bool):
        self.modify_chainmaker_yml(node={'fast_sync': {'enabled': enable}})
        return self

    def get_enable_pkcs11(self) -> bool:
        return self.chainmaker_config.get('pkcs11', {}).get('enabled')

    def set_enable_pkcs11(self, enable: bool):
        self.modify_chainmaker_yml(node={'pkcs11': {'enabled': enable}})
        return self

    def get_enable_tls(self) -> bool:
        return self.chainmaker_config.get('net', {}).get('tls', {}).get('enabled')

    def set_enable_tls(self, enable: bool, rpc_tls_mode: Union[RpcTlsMode, str] = None):
        if isinstance(rpc_tls_mode, RpcTlsMode):
            rpc_tls_mode = rpc_tls_mode.name
        tls_config = {'enabled': enable}
        if rpc_tls_mode:
            tls_config['mode'] = rpc_tls_mode
        self.modify_chainmaker_yml(net={'tls': tls_config})
        return self

    def get_rpc_tls_mode(self) -> RpcTlsMode:
        rpc_tls_mode = self.chainmaker_config.get('rpc', {}).get('tls', {}).get('mode')
        return RpcTlsMode[rpc_tls_mode]

    def set_rpc_tls_mode(self, rpc_tls_mode: Union[RpcTlsMode, str]):
        if isinstance(rpc_tls_mode, RpcTlsMode):
            rpc_tls_mode = rpc_tls_mode.name
        self.modify_chainmaker_yml(rpc={'tls': {'mode': rpc_tls_mode}})
        return self

    def get_tx_filter_type(self) -> TxFilterType:
        tx_filter_type = self.chainmaker_config.get('tx_filter', {}).get('type')
        return TxFilterType(tx_filter_type)

    def set_tx_filter_type(self, tx_filter_type: Union[TxFilterType, str, int]):  # todo 增加多种类型
        tx_filter_type = ensure_enum(tx_filter_type, TxFilterType)
        self.modify_chainmaker_yml(tx_filter={'type': tx_filter_type.value})
        return self

    def get_enable_big_filter(self) -> bool:
        return self.chainmaker_config.get('storage', {}).get('enable_bigfilter')

    def set_enable_big_filter(self, enable: bool):
        self.modify_chainmaker_yml(storage={'enable_bigfilter': enable})
        return self

    def get_enable_block_file_db(self) -> bool:
        disable_block_file_db = self.chainmaker_config.get('storage', {}).get('disable_block_file_db')
        return not disable_block_file_db

    def set_enable_block_file_db(self, enable: bool):
        self.modify_chainmaker_yml(storage={'disable_block_file_db': not enable})
        return self

    def get_db_provider(self, db_type: Union[DbType, str]) -> DbProvider:
        """
        获取chainmaker.yml指定数据的provider类型
        :param db_type:
        :return:
        """
        if isinstance(db_type, DbType):
            db_type = db_type.name
        db_config = '%s_config' % db_type
        db_provider = self.chainmaker_config.get('storage', {}).get(db_config, {}).get('provider')
        if db_provider == 'sql':
            db_provider = self.chainmaker_config.get('storage', {}).get(db_config, {}).get('sqldb_config', {}).get(
                'sqldb_type')
        return DbProvider[db_provider]

    def set_db_provider(self, db_provider: Union[DbProvider, str], dns: str = DEFAULT_DNS,
                        db_types: List[Union[DbType, str]] = MODIFY_DB_LIST):
        """
        设置chainmaker.yml指定数据库引擎类型
        :param db_provider: 指定的数据库引擎类型
        :param dns: mysql数据库类型是需指定
        :param db_types: 要修改的数据库列表
        :return:
        """
        storage = {}
        for db_type in db_types:
            storage.update(self._get_db_config(db_type, db_provider, dns))
        self.modify_chainmaker_yml(storage=storage)

    def modify_bc1_yml(self, chain_id: str = None, version: str = None, sequence: int = None, auth_type: str = None,
                       crypto: dict = None, contract: dict = None, vm: dict = None, block: dict = None,
                       core: dict = None, account_config: dict = None, snapshot: dict = None, scheduler: dict = None,
                       consensus: dict = None, trust_roots: List[dict] = None,
                       resource_policies: List[dict] = None, disabled_native_contract: List[str] = None) -> None:
        """
        修改节点bc1.yml配置
        :param chain_id: 链id eg. chain1
        :param version: 链版本 eg. v2.3.0
        :param sequence: 配置序号 eg. 0
        :param auth_type: 授权类型 eg. permissionedWithCert
        :param crypto: 加密配置 eg. {'hash': 'SHA256'}
        :param contract: 合约配置 eg. {'enable_sql_support': False}
        :param vm: 虚拟机配置 eg. {'addr_type': 2, support_list: ['wasmer', 'gasm', 'evm', 'dockergo', 'wxvm']}
        :param block: 区块配置 eg. {'tx_timestamp_verify': True, 'tx_timeout': 600, 'block_tx_capacity': 100,
                                  'block_size': 10, 'block_interval': 10}
        :param core: 核心配置 eg. {'tx_scheduler_timeout':10 , 'tx_scheduler_validate_timeout': 10,
                                 'enable_sender_group': False, 'enable_conflicts_bit_window': True}
        :param account_config: Gas账户配置 eg. {'enable_gas': False, 'gas_count': 0, 'default_gas': 0}
        :param snapshot: 快照配置 eg. {'enable_evidence': False}
        :param scheduler: 调度器配置 eg. {'enable_evidence': False}
        :param consensus: 共识配置 eg. {'type': 3, 'nodes': [{'org_id': 'wx-org1.chainmaker.org',
                                                            'node_id': ['QmTTayzjbQqzzarWMo9HQSZsnZWLAQz2oefogKZuhbMnfD']}, ...],
                                       'ext_config': None}
        :param trust_roots: 信任组织根证书配置 eg. [{'org_id': 'wx-org1.chainmaker.org',
                                                  'root': ['../config/wx-org1.chainmaker.org/certs/ca/wx-org1.chainmaker.org/ca.crt']}]
        :param resource_policies: 权限配置 eg. [{'resource_name': 'CHAIN_CONFIG-NODE_ID_UPDATE',
                                                'policy': {'rule': 'SELF', org_list: None, role_list: ['admin']}, ...]
        :param disabled_native_contract: 禁用系统合约配置 eg. None
        """
        if chain_id:
            self.bc1_config['chain_id'] = chain_id
        if version:
            self.bc1_config['version'] = version
        if sequence:
            self.bc1_config['sequence'] = sequence
        if auth_type:
            self.bc1_config['auth_type'] = auth_type
        if crypto:
            self.bc1_config['crypto'].update(crypto)
        if contract:
            self.bc1_config['contract'].update(contract)
        if vm:
            self.bc1_config['vm'].update(vm)
        if block:
            self.bc1_config['block'].update(block)
        if core:
            self.bc1_config['core'].update(core)
        if account_config:
            self.bc1_config['account_config'].update(account_config)
        if snapshot:
            self.bc1_config['snapshot'] = snapshot
        if scheduler:
            self.bc1_config['scheduler'] = scheduler
        if consensus:
            self.bc1_config['consensus'].update(consensus)
        if trust_roots:
            self.bc1_config['trust_roots'] = trust_roots
        if resource_policies:
            self.bc1_config['resource_policies'] = resource_policies
        if disabled_native_contract:
            self.bc1_config['disabled_native_contract'] = disabled_native_contract

        if not self.host.exists(self._bc1_yml_bak_path):
            self.host.run(f'cp {self._bc1_yml_path} {self._bc1_yml_bak_path}')
        self.host.save_yaml(self.bc1_config, self._bc1_yml_path)
        self._cached_bc1_config = None

    def modify_chainmaker_yml(self, auth_type: str = None, log: dict = None, crypto_engine: str = None,
                              blockchain: List[dict] = None, node: dict = None, net: dict = None, txpool: dict = None,
                              rpc: dict = None, tx_filter: dict = None, monitor: dict = None, pprof: dict = None,
                              consensus: dict = None, scheduler: dict = None, storage: dict = None, vm: dict = None):
        """
        修改节点chainmaker.yml配置
        :param auth_type: 节点授权模式 eg. permissionedWithCert
        :param log: 节点日志配置 eg. {'config_file': '../config/wx-org1.chainmaker.org/log.yml'}
        :param crypto_engine: 节点国密引擎配置, 支持gmssl,tencentsm和tjfoc eg. tjfoc
        :param blockchain: 节点链配置 eg. [{'chainId: 'chain1', 'genesis': '../config/wx-org1.chainmaker.org/chainconfig/bc1.yml'}]
        :param node: 节点配置 eg. {'org_id': 'wx-org1.chainmaker.org', 'priv_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.sign.key',
                                  'cert_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.sign.crt',
                                  'cert_cache_size': 1000, 'cert_key_usage_check': True,
                                  'fast_sync': {'enabled: True, 'min_full_blocks': 10},
                                  'pkcs11': {'enabled': False, 'type': 'pkcs11', 'library': '/usr/local/lib64/pkcs11/libupkcs11.so',
                                             'label': 'HSM', 'password': '11111111', 'session_cache_size': 10, 'hash': 'SHA256'}}
        :param net: 节点网络配置 eg. {'provider': 'LibP2P','listen_addr': '/ip4/0.0.0.0/tcp/11301',
                                    'seeds': ['/ip4/127.0.0.1/tcp/11301/p2p/QmTTayzjbQqzzarWMo9HQSZsnZWLAQz2oefogKZuhbMnfD', ...],
                                    'tls': {'enabled': True, 'priv_key_file': '...', 'cert_file': '...', 'priv_enc_key_file': '...',
                                            'cert_enc_file': '...'}}
        :param txpool: 节点交易池配置 eg. {'pool_type': 'normal', 'max_txpool_size': 50000, 'max_config_txpool_size': 10,
                                         'is_dump_txs_in_queue': true, 'common_queue_num': 8, 'batch_max_size': 100,
                                         'batch_create_timeout': 50}
        :param rpc: 节点rpc配置 eg. {'blacklist': {'addresses': None},
                                    'check_chain_conf_trust_roots_change_interval': 60,
                                    'gateway': {'enabled': False, 'max_resp_body_size': 16},
                                    'max_recv_msg_size': 100,'max_send_msg_size': 100, 'port': 12301,'provider': 'grpc',
                                    'ratelimit': {'enabled': False,'token_bucket_size': -1,'token_per_second': -1,'type': 0},
                                    'subscriber': {'ratelimit': {'token_bucket_size': 100,'token_per_second': 100}},
                                    'tls': {'cert_enc_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.enc.crt',
                                            'cert_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.crt',
                                            'mode': 'twoway',
                                            'priv_enc_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.enc.key',
                                            'priv_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.key'}}
        :param tx_filter: 节点交易过滤器配置 eg. {'birds_nest': {'cuckoo': {'bits_per_item': 11, 'key_type': 1, 'max_num_keys': 2000000,'table_type': 0,'tags_per_bucket': 2},
                                               'length': 10,'rules': {'absolute_expire_time': 172800},
                                               'snapshot': {'block_height': {'interval': 10}, 'path': '../data/wx-org1.chainmaker.org/tx_filter',
                                                             'serialize_interval': 10,'timed': {'interval': 10}, 'type': 0}},
                                               'sharding': {'birds_nest': {'cuckoo': {'bits_per_item': 11,'key_type': 1,
                                                                        'max_num_keys': 2000000,'table_type': 0,'tags_per_bucket': 2},
                                                             'length': 10,'rules': {'absolute_expire_time': 172800}},
                                               'length': 5,
                                               'snapshot': {'block_height': {'interval': 10},
                                                           'path': '../data/wx-org1.chainmaker.org/tx_filter',
                                                           'serialize_interval': 10,
                                                           'timed': {'interval': 10},
                                                           'type': 0},'timeout': 60},
                                               'type': 0}
        :param monitor: 节点monitor配置 eg. {'enabled': False, 'port': 14321}
        :param pprof: 节点pprof配置 eg. {'enabled': False, 'port': 24321}
        :param consensus: 共识扩展配置 eg. {'raft': {'snap_count': 10, 'async_wal_save': True, 'ticker': 1}
        :param scheduler: 节点调度器配置 eg {'rwset_log': False}
        :param storage: 节点存储配置 eg. {'bigfilter_config': {'fp_rate': 1e-09, 'redis_hosts_port': '127.0.0.1:6300,127.0.0.1:6301','redis_password': 'abcpass','tx_capacity': 1000000000},
                                         'blockdb_config': {'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/block'},
                                                            'provider': 'leveldb'},
                                         'contract_eventdb_config': {'provider': 'sql',
                                                                     'sqldb_config': {'dsn': 'root:password@tcp(127.0.0.1:3306)/',
                                                                                      'sqldb_type': 'mysql'}},
                                         'disable_block_file_db': False,'disable_contract_eventdb': True,'enable_bigfilter': False,'enable_rwc': True,
                                         'historydb_config': {'disable_account_history': True, 'disable_contract_history': True,
                                                              'disable_key_history': False,
                                                              'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/history'},
                                                              'provider': 'leveldb'},
                                         'logdb_segment_async': False,
                                         'logdb_segment_size': 128,
                                         'resultdb_config': {'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/result'},
                                                             'provider': 'leveldb'},
                                         'rolling_window_cache_capacity': 55000,
                                         'state_cache_config': {'clean_window': 1000000000,'hard_max_cache_size': 1024,
                                                                'life_window': 3000000000000,'max_entry_size': 500},
                                         'statedb_config': {'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/state'},
                                                            'provider': 'leveldb'},
                                         'store_path': '../data/wx-org1.chainmaker.org/ledgerData1',
                                         'unarchive_block_height': 300000,'write_block_type': 0}
        :param vm: 节点虚拟机配置 eg. {'go': {'contract_engine': {'host': '127.0.0.1', 'max_connection': 5, 'port': 22351},
                            'data_mount_path': '../data/wx-org1.chainmaker.org/go', 'dial_timeout': 10,'enable': False,
                            'log_in_console': False, 'log_level': 'INFO','log_mount_path': '../log/wx-org1.chainmaker.org/go',
                            'max_concurrency': 20,'max_recv_msg_size': 100,
                            'max_send_msg_size': 100,'protocol': 'tcp','runtime_server': {'port': 32351}}}
        :return:
        """
        if auth_type:
            self.chainmaker_config['auth_type'] = auth_type
        if log:
            self.chainmaker_config['log'].update(log)
        if crypto_engine:
            self.chainmaker_config['crypto_engine'] = crypto_engine
        if blockchain:
            self.chainmaker_config['blockchain'] = blockchain
        if node:
            self.chainmaker_config['node'].update(node)
        if net:
            self.chainmaker_config['net'].update(net)
        if txpool:
            self.chainmaker_config['txpool'].update(txpool)
        if rpc:
            self.chainmaker_config['rpc'].update(rpc)
        if tx_filter:
            self.chainmaker_config['tx_filter'].update(tx_filter)
        if monitor:
            self.chainmaker_config['monitor'].update(monitor)
        if pprof:
            self.chainmaker_config['pprof'].update(pprof)
        if consensus:
            self.chainmaker_config['consensus'].update(consensus)
        if scheduler:
            self.chainmaker_config['scheduler'].update(scheduler)
        if storage:
            self.chainmaker_config['storage'].update(storage)
        if vm:
            self.chainmaker_config['vm'].update(vm)

        if not self.host.exists(self._chainmaker_yml_bak_path):
            self.host.run(f'cp {self._chainmaker_yml_path} {self._chainmaker_yml_bak_path}')
        self.host.save_yaml(self.chainmaker_config, self._chainmaker_yml_path)
        self._cached_chainmaker_config = None

    def modify_log_level(self, log_level: str = 'DEBUG', origin_log_level: str = 'INFO'):
        if not self.host.exists(self._log_yml_bak_path):
            self.host.run(f'cp {self._log_yml_path} {self._log_yml_bak_path}')
        self.host.run(f'sed -i "s/{origin_log_level}/{log_level}/g" {self._log_yml_path}')

    def change_to_consensus_node(self):
        if not self.is_consensus_node:
            if not self.is_trust_root_on_chain:
                result = self.cc.chain_config_trust_root_add(self.org_id, [self.trust_root_crt])
                assert_success(result)

            if not self.cc.chain_config_consensus_node_org_check(self.org_id):
                result = self.cc.chain_config_consensus_node_org_add(self.org_id, [self.node_id])
                assert_success(result)
            elif not self.cc.chain_config_consensus_node_id_check(self.org_id, self.node_id):
                result = self.cc.chain_config_consensus_node_id_add(self.org_id, [self.node_id])
                assert_success(result)
            wait_chainmaker_is_ok(self.crypto_config)

    def change_to_common_node(self):
        if not self.is_common_node:
            if self.cc.chain_config_consensus_node_id_check(self.org_id, self.node_id):
                result = self.cc.chain_config_consensus_node_id_delete(self.org_id, self.node_id)
                assert_success(result)

            if not self.is_trust_root_on_chain:
                result = self.cc.chain_config_trust_root_add(self.org_id, [self.trust_root_crt])
                assert_success(result)
            wait_chainmaker_is_ok(self.crypto_config)

    def change_to_off_chain_node(self):
        if not self.is_off_chain_node:
            if self.cc.chain_config_consensus_node_org_check(self.org_id):
                result = self.cc.chain_config_consensus_node_org_delete(self.org_id)
                assert_success(result)

            if self.is_trust_root_on_chain:
                result = self.cc.chain_config_trust_root_delete(self.org_id)
                assert_success(result)

        wait_chainmaker_is_ok(self.crypto_config)

    def change_node_type(self, node_type: str):
        if node_type == 'consensus':
            return self.change_to_consensus_node()
        elif node_type == 'common':
            return self.change_to_common_node()
        else:
            return self.change_to_off_chain_node()

    @staticmethod
    def _check_db_provider(db_type: str, db_provider: str):
        """检查数据库使用provider是否允许"""
        if db_type == 'blockdb':
            assert db_provider in ['leveldb', 'sql', 'badgerdb',
                                   'tikvdb', 'sqlkv'], 'blockdb仅支持leveldb/mysql/badgerdb/tikvdb/sqlkv'  # todo文件存储
        elif db_type == 'statedb':
            assert db_provider in ['leveldb', 'sql', 'badgerdb',
                                   'tikvdb', 'sqlkv'], 'statedb仅支持leveldb/mysql/badgerdb/tikvdb/sqlkv'
        elif db_type == 'historydb':
            assert db_provider in ['leveldb', 'sql', 'badgerdb', 'tikvdb', 'sqlkv',
                                   'disable'], 'historydb仅支持leveldb/mysql/badgerdb/tikvdb/sqlkv/disable'
        elif db_type == 'resultdb':
            assert db_provider in ['leveldb', 'sql', 'badgerdb', 'tikvdb', 'sqlkv',
                                   'disable'], 'resultdb仅支持leveldb/mysql/badgerdb/tikvdb/sqlkv/disable'
        elif db_type == 'contract_eventdb':
            assert db_provider in ['sql', 'disable'], 'contract_eventdb仅支持leveldb/mysql/badgerdb/tikvdb/sqlkv'

    def _get_db_config(self, db_type: Union[DbType, str], db_provider: Union[DbProvider, str],
                       dns: str = DEFAULT_DNS, tikv_url: str = DEFAULT_TIKV_URL) -> dict:
        """修改chainmaker.yml指定数据的provider类型"""
        if isinstance(db_type, DbType):
            db_type = db_type.name
        if isinstance(db_provider, DbProvider):
            db_provider = DbProvider.name

        self._check_db_provider(db_type, db_provider)

        db_config = '%s_config' % db_type
        origin_db_provider = self.get_db_provider(db_type).name
        if origin_db_provider == 'mysql':
            origin_db_provider = 'sqldb'
        if db_provider == DbProvider.mysql:
            dns = dns or DEFAULT_DNS
            return {db_config: {'provider': 'sql', 'sqldb_config': {'sqldb_type': 'mysql', 'dsn': dns}}}
        elif db_provider == DbProvider.tikvdb:
            return {db_config: {'provider': 'tikvdb', 'tikvdb_config': {
                'db_prefix': f'{self.name}_',
                'endpoints': tikv_url,
                'max_batch_count': 128,
                'grpc_connection_count': 16,
                'grpc_keep_alive_time': 10,
                'grpc_keep_alive_timeout': 3,
                'write_batch_size': 128,
            }}}
        else:
            origin_store_path = self.chainmaker_config['storage'][db_config][f'{origin_db_provider}_config']
            return {db_config: {'provider': db_provider, '%s_config' % db_provider: origin_store_path}}

    def _clean(self, clean_log: bool = True):
        """清空节点数据及日志"""
        if clean_log is True:
            return self.host.run('rm -rf data/* ; rm -rf log/*', workspace=self.release_path)
        return self.host.run('rm -rf data', workspace=self.release_path)

    def _kill(self) -> str:
        """
        杀掉节点进程
        :return: 命令行输出结果
        """
        return self.host.kill(self.pid)

    def reset_config(self):
        """重置bc1.yml和chainmaker.yml配置"""
        if self.host.exists(self._bc1_yml_bak_path):
            # self.host.run(f'rm -rf {self._bc1_yml_path}')
            self.host.run(f'cp {self._bc1_yml_bak_path} {self._bc1_yml_path}')
            self._cached_bc1_config = None

        if self.host.exists(self._chainmaker_yml_bak_path):
            # self.host.run(f'rm -rf {self._chainmaker_yml_path}')
            self.host.run(f'cp {self._chainmaker_yml_bak_path} {self._chainmaker_yml_path}')
            self._cached_chainmaker_config = None

        if self.host.exists(self._log_yml_bak_path):
            # self.host.run(f'rm -rf {self._log_yml_path}')
            self.host.run(f'cp {self._log_yml_bak_path} {self._log_yml_path}')

    @staticmethod
    def _guess_org_id_from_release_path(release_path: str):
        # if 'node' in release_path:
        #     org_id, = (re.findall(r'node\d+', release_path) or ['public'])
        # else:
        #     org_id, = (re.findall(r'wx-org\d+\.chainmaker\.org', release_path) or [''])
        # return org_id
        if re.search(r'node\d+', release_path):
            return 'public'
        matched = re.search(r'wx-org\d+\.chainmaker\.org', release_path)
        if matched:
            return matched.group()
        matched = re.search(r'wx-org\.chainmaker\.org', release_path)
        if matched:
            return matched.group()
        raise Exception('guess org_id from release_path: %s failed' % release_path)


class ChainMakerCluster:
    """长安链服务器集群"""

    def __init__(self, nodes: List[ChainMakerNode],
                 crypto_config: CryptoConfig = None, cc: ChainClientWithEndorsers = None):
        self.nodes = nodes
        self.crypto_config = crypto_config
        self.cc = cc or self.crypto_config.new_chain_client(endorsers_cnt=self.crypto_config.org_or_node_cnt,
                                                            conn_node=0) if crypto_config else None
        self._logger = log

    def _info(self, msg: str):
        self._logger.info('[Sdk] %s' % msg)

    @property
    def active_node_cnt(self):
        """
        活动节点数量
        :return:
        """
        count = 0
        for node in self.nodes:
            if node.is_active:
                count += 1
        return count

    def start_nodes(self, nodes: List[str] = None):
        """
        启动多个节点
        :param nodes: 指定节点列表, eg. ['node1', 'node2']
        :return:
        """
        self._info(f'启动节点 {", ".join(nodes or DEFAULT_NODES)}')
        node_list = self._get_nodes(nodes)
        threads = []
        for node in node_list:
            threads.append(threading.Thread(target=node.start))
        [t.start() for t in threads]
        [t.join() for t in threads]

        wait_chainmaker_is_ok(self.crypto_config)

    def stop_nodes(self, nodes: List[str] = None, clean: bool = False):
        """
        停止对多个节点
        :param nodes: 指定节点列表, eg. ['node1', 'node2']
        :param clean: 是否清理节点数据及日志
        :return:
        """
        self._info(f'停止节点 {", ".join(nodes or DEFAULT_NODES)}')
        node_list = self._get_nodes(nodes)
        threads = []
        for node in node_list:
            threads.append(threading.Thread(target=node.stop, args=(clean,)))
        [t.start() for t in threads]
        [t.join() for t in threads]

    def restart_nodes(self, nodes: List[str] = None, clean: bool = False, duration: int = None):
        """
        重启多个节点
        :param nodes: 指定节点列表, eg. ['node1', 'node2']
        :param clean: 是否清理节点数据及日志
        :param duration: 重启间隔时间
        :return:
        """
        if duration:
            self._info(f'重启节点 {", ".join(nodes or DEFAULT_NODES)} 等待时间 {duration}')
        else:
            self._info(f'重启节点 {", ".join(nodes or DEFAULT_NODES)}')
        node_list = self._get_nodes(nodes)
        threads = []
        for node in node_list:
            threads.append(threading.Thread(target=node.restart, args=(clean, duration)))
        [t.start() for t in threads]
        [t.join() for t in threads]
        wait_chainmaker_is_ok(self.crypto_config)

    def clean_nodes(self, nodes: List[str] = None, clean_log: bool = True):
        node_list = self._get_nodes(nodes)
        threads = []
        for node in node_list:
            threads.append(threading.Thread(target=node._clean, args=(clean_log,)))
        [t.start() for t in threads]
        [t.join() for t in threads]

    def restart_vm_go(self, nodes: List[str] = None):
        self._info(f'重启节点 {", ".join(nodes or DEFAULT_NODES)} VM-GO 容器')
        node_list = self._get_nodes(nodes)
        threads = []
        for node in node_list:
            threads.append(threading.Thread(target=node.restart_vm_go))
        [t.start() for t in threads]
        [t.join() for t in threads]

        wait_chainmaker_is_ok(self.crypto_config)

    def start(self):
        """启动集群"""
        self.start_nodes()

    def stop(self, clean: bool = False):
        """停止集群"""
        self.stop_nodes(clean=clean)

    def restart(self, clean: bool = False):
        """重启集群"""
        return self.restart_nodes(clean=clean)

    def reset(self, nodes: List[str] = None):
        """重置集群"""
        node_list = self._get_nodes(nodes)
        self._info(f'重置节点 {", ".join(nodes or DEFAULT_NODES)} 配置')
        for node in node_list:
            node.reset_config()
        self.restart_nodes(clean=True)

        if len(self.nodes) > len(DEFAULT_NODES):
            _to_stop_nodes = [f'node{i + 1}' for i in range(len(DEFAULT_NODES), len(self.nodes))]
            self.stop_nodes(_to_stop_nodes, clean=True)

    def reset_env(self, node_cnt: int, consensus_type: ConsensusType = None, addr_type: AddrType = None):
        """
        重置环境为N节点环境
        :param node_cnt: 节点数量
        :param addr_type: 地址类型
        :param consensus_type: 共识类型
        :return:
        """
        _msg = f'重置为 {node_cnt} 共识节点环境'
        if consensus_type is not None:
            _msg += f' consensus_type: {consensus_type.name}'
        if addr_type is not None:
            _msg += f' addr_type: {addr_type.name}'

        self._info(_msg)
        # todo pk
        self.stop_nodes(clean=True)

        # 修改bc1.yml配置
        for node in self.nodes:
            trust_roots = [{'org_id': self.nodes[i].org_id,
                            'root': [f'../config/{node.org_id}/certs/ca/{self.nodes[i].org_id}/ca.crt']}
                           for i in range(node_cnt)]
            consensus = {'nodes': [{'org_id': self.nodes[i].org_id, 'node_id': [self.nodes[i].node_id]}
                                   for i in range(node_cnt)]}
            if consensus_type:
                consensus['type'] = consensus_type.value

            node.modify_bc1_yml(trust_roots=trust_roots, consensus=consensus)

        # 修改chainmaker.yml配置
        net = {'seeds': [f'/ip4/127.0.0.1/tcp/{self.nodes[i].p2p_port}/p2p/{self.nodes[i].node_id}'
                         for i in range(node_cnt)]}

        vm = {'addr_type': addr_type.value} if addr_type is not None else {}
        self.modify_chainmaker_yml(net=net, vm=vm)

        # 启动节点
        self.start_nodes([f'node{i + 1}' for i in range(node_cnt)])

    def add_consensus_nodes(self, nodes: List[str], start_nodes=True):
        """
        添加共识节点
        :param nodes:
        :param start_nodes:
        :return:
        """
        self._info(f'添加多个共识节点 {", ".join(nodes)}')
        node_list = self._get_nodes(nodes)
        for node in node_list:
            self._info(f'添加共识节点 {node.name}')
            node.change_to_consensus_node()
        if start_nodes is True:
            self.start_nodes(nodes)

    def delete_consensus_nodes(self, nodes: List[str], stop_nodes=True):
        """
        移除共识节点
        :param nodes:
        :param stop_nodes:
        :return:
        """
        self._info(f'移除多个共识节点 {", ".join(nodes)}')
        node_list = self._get_nodes(nodes)
        for node in node_list:
            self._info(f'移除共识节点 {node.name}')
            node.change_to_common_node()
        if stop_nodes is True:
            self.stop_nodes(nodes)

    def add_common_nodes(self, nodes: List[str], start_nodes=True):
        """
        添加同步节点
        :param nodes:
        :param start_nodes:
        :return:
        """
        self._info(f'添加多个同步节点 {", ".join(nodes)}')
        node_list = self._get_nodes(nodes)
        for node in node_list:
            self._info(f'添加同步节点 {node.name}')
            node.change_to_common_node()
        if start_nodes is True:
            self.start_nodes(nodes)

    def change_to_common_nodes(self, nodes: List[str]):
        """
        修改为同步节点
        :param nodes:
        :return:
        """
        node_list = self._get_nodes(nodes)
        for node in node_list:
            node.change_to_common_node()

    def delete_common_nodes(self, nodes: List[str], stop_nodes=True):
        """
        移除同步节点
        :param nodes:
        :param stop_nodes:
        :return:
        """
        self._info(f'移除同步节点 {", ".join(nodes)}')
        node_list = self._get_nodes(nodes)
        for node in node_list:
            node.change_to_off_chain_node()
        if stop_nodes is True:
            self.stop_nodes(nodes)

    def modify_bc1_yml(self, chain_id: str = None, version: str = None, sequence: int = None, auth_type: str = None,
                       crypto: dict = None, contract: dict = None, vm: dict = None, block: dict = None,
                       core: dict = None,
                       account_config: dict = None, consensus: dict = None, trust_roots: List[dict] = None,
                       resource_policies: List[dict] = None, disabled_native_contract: List[str] = None,
                       nodes: List[str] = None, restart: bool = False):
        """
        修改节点bc1.yml配置
        :param chain_id: 链id eg. chain1
        :param version: 链版本 eg. v2.3.0
        :param sequence: 配置序号 eg. 0
        :param auth_type: 授权类型 eg. permissionedWithCert
        :param crypto: 加密配置 eg. {'hash': 'SHA256'}
        :param contract: 合约配置 eg. {'enable_sql_support': False}
        :param vm: 虚拟机配置 eg. {'addr_type': 2, support_list: ['wasmer', 'gasm', 'evm', 'dockergo', 'wxvm']}
        :param block: 区块配置 eg. {'tx_timestamp_verify': True, 'tx_timeout': 600, 'block_tx_capacity': 100,
                                  'block_size': 10, 'block_interval': 10}
        :param core: 核心配置 eg. {'tx_scheduler_timeout':10 , 'tx_scheduler_validate_timeout': 10,
                                 'enable_sender_group': False, 'enable_conflicts_bit_window': True}
        :param account_config: Gas账户配置 eg. {'enable_gas': False, 'gas_count': 0, 'default_gas': 0}
        :param consensus: 共识配置 eg. {'type': 3, 'nodes': [{'org_id': 'wx-org1.chainmaker.org',
                                                            'node_id': ['QmTTayzjbQqzzarWMo9HQSZsnZWLAQz2oefogKZuhbMnfD']}, ...],
                                       'ext_config': None}
        :param trust_roots: 信任组织根证书配置 eg. [{'org_id': 'wx-org1.chainmaker.org',
                                                  'root': ['../config/wx-org1.chainmaker.org/certs/ca/wx-org1.chainmaker.org/ca.crt']}]
        :param resource_policies: 权限配置 eg. [{'resource_name': 'CHAIN_CONFIG-NODE_ID_UPDATE',
                                                'policy': {'rule': 'SELF', org_list: None, role_list: ['admin']}, ...]
        :param disabled_native_contract: 禁用系统合约配置 eg. None
        :param nodes: 指定要修改的节点
        :param restart: 修改后是否重启集群
        """
        _nodes = self._get_nodes(nodes)
        for node_obj in _nodes:
            node_obj.modify_bc1_yml(chain_id, version, sequence, auth_type, crypto, contract, vm, block, core, None,
                                    None, account_config, consensus, trust_roots, resource_policies,
                                    disabled_native_contract)
        if restart:
            self.restart_nodes(nodes)

    def modify_chainmaker_yml(self, auth_type: str = None, log: dict = None, crypto_engine: str = None,
                              blockchain: List[dict] = None, node: dict = None, net: dict = None, txpool: dict = None,
                              rpc: dict = None, tx_filter: dict = None, monitor: dict = None, pprof: dict = None,
                              consensus: dict = None, scheduler: dict = None, storage: dict = None, vm: dict = None,
                              nodes: List[str] = None, restart: bool = False):
        """
        修改节点chainmaker.yml配置

        :param auth_type: 节点授权模式 eg. permissionedWithCert
        :param log: 节点日志配置 eg. {'config_file': '../config/wx-org1.chainmaker.org/log.yml'}
        :param crypto_engine: 节点国密引擎配置, 支持gmssl,tencentsm和tjfoc eg. tjfoc
        :param blockchain: 节点链配置 eg. [{'chainId: 'chain1', 'genesis': '../config/wx-org1.chainmaker.org/chainconfig/bc1.yml'}]
        :param node: 节点配置 eg. {'org_id': 'wx-org1.chainmaker.org', 'priv_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.sign.key',
                                  'cert_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.sign.crt',
                                  'cert_cache_size': 1000, 'cert_key_usage_check': True,
                                  'fast_sync': {'enabled: True, 'min_full_blocks': 10},
                                  'pkcs11': {'enabled': False, 'type': 'pkcs11', 'library': '/usr/local/lib64/pkcs11/libupkcs11.so',
                                             'label': 'HSM', 'password': '11111111', 'session_cache_size': 10, 'hash': 'SHA256'}}
        :param net: 节点网络配置 eg. {'provider': 'LibP2P','listen_addr': '/ip4/0.0.0.0/tcp/11301',
                                    'seeds': ['/ip4/127.0.0.1/tcp/11301/p2p/QmTTayzjbQqzzarWMo9HQSZsnZWLAQz2oefogKZuhbMnfD', ...],
                                    'tls': {'enabled': True, 'priv_key_file': '...', 'cert_file': '...', 'priv_enc_key_file': '...',
                                            'cert_enc_file': '...'}}
        :param txpool: 节点交易池配置 eg. {'pool_type': 'normal', 'max_txpool_size': 50000, 'max_config_txpool_size': 10,
                                         'is_dump_txs_in_queue': true, 'common_queue_num': 8, 'batch_max_size': 100,
                                         'batch_create_timeout': 50}
        :param rpc: 节点rpc配置 eg. {'blacklist': {'addresses': None},
                                    'check_chain_conf_trust_roots_change_interval': 60,
                                    'gateway': {'enabled': False, 'max_resp_body_size': 16},
                                    'max_recv_msg_size': 100,'max_send_msg_size': 100, 'port': 12301,'provider': 'grpc',
                                    'ratelimit': {'enabled': False,'token_bucket_size': -1,'token_per_second': -1,'type': 0},
                                    'subscriber': {'ratelimit': {'token_bucket_size': 100,'token_per_second': 100}},
                                    'tls': {'cert_enc_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.enc.crt',
                                            'cert_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.crt',
                                            'mode': 'twoway',
                                            'priv_enc_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.enc.key',
                                            'priv_key_file': '../config/wx-org1.chainmaker.org/certs/node/consensus1/consensus1.tls.key'}}
        :param tx_filter: 节点交易过滤器配置 eg. {'birds_nest': {'cuckoo': {'bits_per_item': 11, 'key_type': 1, 'max_num_keys': 2000000,'table_type': 0,'tags_per_bucket': 2},
                                               'length': 10,'rules': {'absolute_expire_time': 172800},
                                               'snapshot': {'block_height': {'interval': 10}, 'path': '../data/wx-org1.chainmaker.org/tx_filter',
                                                             'serialize_interval': 10,'timed': {'interval': 10}, 'type': 0}},
                                               'sharding': {'birds_nest': {'cuckoo': {'bits_per_item': 11,'key_type': 1,
                                                                        'max_num_keys': 2000000,'table_type': 0,'tags_per_bucket': 2},
                                                             'length': 10,'rules': {'absolute_expire_time': 172800}},
                                               'length': 5,
                                               'snapshot': {'block_height': {'interval': 10},
                                                           'path': '../data/wx-org1.chainmaker.org/tx_filter',
                                                           'serialize_interval': 10,
                                                           'timed': {'interval': 10},
                                                           'type': 0},'timeout': 60},
                                               'type': 0}
        :param monitor: 节点monitor配置 eg. {'enabled': False, 'port': 14321}
        :param pprof: 节点pprof配置 eg. {'enabled': False, 'port': 24321}
        :param consensus: 共识扩展配置 eg. {'raft': {'snap_count': 10, 'async_wal_save': True, 'ticker': 1}
        :param scheduler: 节点调度器配置 eg {'rwset_log': False}
        :param storage: 节点存储配置 eg. {'bigfilter_config': {'fp_rate': 1e-09, 'redis_hosts_port': '127.0.0.1:6300,127.0.0.1:6301','redis_password': 'abcpass','tx_capacity': 1000000000},
                                         'blockdb_config': {'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/block'},
                                                            'provider': 'leveldb'},
                                         'contract_eventdb_config': {'provider': 'sql',
                                                                     'sqldb_config': {'dsn': 'root:password@tcp(127.0.0.1:3306)/',
                                                                                      'sqldb_type': 'mysql'}},
                                         'disable_block_file_db': False,'disable_contract_eventdb': True,'enable_bigfilter': False,'enable_rwc': True,
                                         'historydb_config': {'disable_account_history': True, 'disable_contract_history': True,
                                                              'disable_key_history': False,
                                                              'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/history'},
                                                              'provider': 'leveldb'},
                                         'logdb_segment_async': False,
                                         'logdb_segment_size': 128,
                                         'resultdb_config': {'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/result'},
                                                             'provider': 'leveldb'},
                                         'rolling_window_cache_capacity': 55000,
                                         'state_cache_config': {'clean_window': 1000000000,'hard_max_cache_size': 1024,
                                                                'life_window': 3000000000000,'max_entry_size': 500},
                                         'statedb_config': {'leveldb_config': {'store_path': '../data/wx-org1.chainmaker.org/state'},
                                                            'provider': 'leveldb'},
                                         'store_path': '../data/wx-org1.chainmaker.org/ledgerData1',
                                         'unarchive_block_height': 300000,'write_block_type': 0}
        :param vm: 节点虚拟机配置 eg. {'go': {'contract_engine': {'host': '127.0.0.1', 'max_connection': 5, 'port': 22351},
                            'data_mount_path': '../data/wx-org1.chainmaker.org/go', 'dial_timeout': 10,'enable': False,
                            'log_in_console': False, 'log_level': 'INFO','log_mount_path': '../log/wx-org1.chainmaker.org/go',
                            'max_concurrency': 20,'max_recv_msg_size': 100,
                            'max_send_msg_size': 100,'protocol': 'tcp','runtime_server': {'port': 32351}}}
        :param nodes: 指定要修改的节点
        :param restart: 修改后是否重启集群
        :return:
        """
        _nodes = self._get_nodes(nodes)
        for node_obj in _nodes:
            node_obj.modify_chainmaker_yml(auth_type, log, crypto_engine, blockchain, node, net, txpool, rpc, tx_filter,
                                           monitor, pprof, consensus, scheduler, storage, vm)
        if restart:
            self.restart_nodes(nodes)

    def modify_log_level(self, log_level: str = 'DEBUG', origin_log_level: str = 'INFO', nodes: List[str] = None,
                         restart: bool = False):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.modify_log_level(log_level, origin_log_level)

        if restart:
            self.restart_nodes(nodes, clean=True)

    def enable_sql_support(self, dns=DEFAULT_DNS, nodes: List[str] = None, restart: bool = True):
        """修改所有节点bc1.yml及chainmaker.yml配置"""
        self.modify_bc1_yml(contract={'enable_sql_support': True})
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.modify_chainmaker_yml(
                storage={'db_prefix': f'org{node.index + 1}_',
                         'statedb_config': {'provider': 'sql', 'sqldb_config': {'sqldb_type': 'mysql', 'dns': dns}}})
        if restart:
            self.restart_nodes(nodes, clean=True)

    def enable_archive_block(self, unarchive_block_height: int = 10, nodes: List[str] = None, restart: bool = True):
        """启动归档区块(需要disable_block_file_db并清数据重启)"""
        self.modify_chainmaker_yml(storage={'unarchive_block_height': unarchive_block_height,
                                            'disable_block_file_db': True}, nodes=nodes)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_crypto_engine(self, node: str = 'node1') -> CryptoEngine:
        node = self._get_node(node)
        return node.get_crypto_engine()

    def change_crypto_engine(self, crypto_engine: Union[CryptoEngine, str], nodes: List[str] = None,
                             restart: bool = True):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_crypto_engine(crypto_engine)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_enable_docker_go(self, node: str = 'node1') -> bool:
        node = self._get_node(node)
        return node.get_enable_docker_go()

    def change_enable_docker_go(self, enable: bool = True, nodes: List[str] = None, restart: bool = True):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_enable_docker_go(enable)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_enable_docker_vm(self, node: str = 'node1') -> bool:
        node = self._get_node(node)
        return node.get_enable_docker_vm()

    def change_enable_docker_vm(self, enable: bool = True, nodes: List[str] = None, restart: bool = True):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_enable_docker_vm(enable)
        if restart:
            self.restart(clean=True)

    def get_net_provider(self, node: str = 'node1') -> NetProvider:
        node = self._get_node(node)
        return node.get_net_provider()

    def change_net_provider(self, net_provider: Union[NetProvider, str], nodes: List[str] = None, restart: bool = True):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_net_provider(net_provider)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_enable_fast_sync(self, node: str = 'node1') -> bool:
        node = self._get_node(node)
        return node.get_enable_fast_sync()

    def change_enable_fast_sync(self, enable: bool, nodes: List[str] = None, restart: bool = True):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_enable_fast_sync(enable)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_enable_pkcs11(self, node: str = 'node1') -> bool:
        node = self._get_node(node)
        return node.get_enable_pkcs11()

    def change_enable_pkcs11(self, enable: bool, nodes: List[str] = None, restart: bool = True):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_enable_pkcs11(enable)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_enable_tls(self, node: str = 'node1') -> bool:
        node = self._get_node(node)
        return node.get_enable_tls()

    def change_enable_tls(self, enable: bool, rpc_tls_mode: Union[RpcTlsMode, str] = None, nodes: List[str] = None,
                          restart: bool = True):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_enable_tls(enable, rpc_tls_mode=rpc_tls_mode)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_rpc_tls_mode(self, node: str = 'node1') -> RpcTlsMode:
        node = self._get_node(node)
        return node.get_rpc_tls_mode()

    def change_rpc_tls_mode(self, rpc_tls_mode: Union[RpcTlsMode, str], nodes: List[str] = None, restart: bool = True):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_rpc_tls_mode(rpc_tls_mode)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_tx_filter_type(self, node: str = 'node1') -> TxFilterType:
        node = self._get_node(node)
        return node.get_tx_filter_type()

    def change_tx_filter_type(self, tx_filter_type: Union[TxFilterType, str, int], nodes: List[str] = None,
                              restart: bool = True):  # todo 增加多种类型
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_tx_filter_type(tx_filter_type)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_enable_big_filter(self, node: str = 'node1') -> bool:
        node = self._get_node(node)
        return node.get_enable_big_filter()

    def change_enable_big_filter(self, enable: bool, nodes: List[str] = None, restart: bool = True):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_enable_big_filter(enable)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_enable_block_file_db(self, node: str = 'node1') -> bool:
        node = self._get_node(node)
        return node.get_enable_block_file_db()

    def change_enable_block_file_db(self, enable: bool, nodes: List[str] = None, restart: bool = True):
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_enable_block_file_db(enable)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def get_db_provider(self, db_type: Union[DbType, str], node: str = 'node1') -> DbProvider:
        """
        获取chainmaker.yml指定数据的provider类型
        :param node:
        :param db_type:
        :return:
        """
        node = self._get_node(node)
        return node.get_db_provider(db_type)

    def change_db_providers(self, db_provider: Union[DbProvider, str], dns=DEFAULT_DNS,
                            db_types: List[Union[DbType, str]] = MODIFY_DB_LIST,
                            nodes: List[str] = None, restart: bool = True):
        """修改指定节点blockdb/statedb/historydb/resultdb引擎类型"""
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            node.set_db_provider(db_provider, dns, db_types)
        if restart:
            self.restart_nodes(nodes, clean=True)

    def download_system_log(self, *keywords, output_dir: str, nodes: List[str] = ('node1',)):
        """
        下载所有节点system.log日志(每个日志名会在output文件名加上如"node1_"前缀)
        :param nodes:
        :param output_dir:
        :param keywords: 要过滤的关键字 或关系
        :param output_dir: 保存的目录
        """
        _nodes = self._get_nodes(nodes)
        for node in _nodes:
            output_basename = '%s_system.log' % node.name
            output = os.path.join(output_dir, output_basename)
            node.download_system_log(*keywords, output=output)

    def _get_node(self, node: Union[ChainMakerNode, str, int]) -> ChainMakerNode:
        """
        根据节点名称获取节点对象
        :param node: 节点名称 eg. node1
        :return: 节点名称对应的节点对象
        """
        if isinstance(node, ChainMakerNode):
            return node
        if isinstance(node, int):
            index = node
        elif isinstance(node, str):
            index = int(node.lstrip('node')) - 1
        else:
            index = 0
        return self.nodes[index]

    def _get_nodes(self, nodes: List[str] = None):
        if nodes is None:
            nodes = DEFAULT_NODES
        return [self._get_node(node) for node in nodes] if nodes else self.nodes

    @classmethod
    def from_chainmaker_go(cls, host: Host, chainmaker_go_path: str = None,
                           crypto_config_path: Union[Path, str] = None,
                           rpc_port: int = 12301, hash_type: str = 'sha256'):
        """
        从标准chainmaker-go build的项目得到集群对象
        :param hash_type: 哈希类型
        :param host: 主机对象
        :param chainmaker_go_path: chainmaker-go路径
        :param rpc_port: 起始RPC端口
        :param crypto_config_path: 本地crypto_config路径
        :return:
        """
        chainmaker_go_path = chainmaker_go_path or f'{host.workspace.rstrip("/")}/chainmaker-go'
        if not os.path.exists(crypto_config_path):
            download_crypto_config(host, chainmaker_go_path, crypto_config_path)
        nodes = []
        release_paths = get_release_paths_by_chainmaker_go_path(host, chainmaker_go_path)
        crypto_config = load_crypto_config(crypto_config_path, host.host, rpc_port, hash_type)

        cc = crypto_config.new_chain_client(endorsers_cnt=crypto_config.org_or_node_cnt)
        for index, release_path in enumerate(release_paths):
            node_rpc_port = rpc_port + index
            node = ChainMakerNode(index=index, host=host, release_path=release_path, rpc_port=node_rpc_port,
                                  crypto_config=crypto_config, cc=cc)
            nodes.append(node)
        return cls(nodes=nodes, crypto_config=crypto_config, cc=cc)

    @classmethod
    def from_conf(cls, server_config: dict, cc: ChainClientWithEndorsers = None):
        """
        根据配置生成长安链集群对象
        :param cc: 指定链客户端
        :param server_config:
            eg1. 单主机标准chainmaker-go节点配置(节点统一位于chainmaker-go/build/release下){
                {'host': {'host': '127.0.0.1', 'port': 36000, 'user': 'root', 'password': '...'},
                'chainmaker_go_path': '/home/hzc/chainmaker-go',
                'crypto_config_path': 'resources/crypto-config'  # 本地crypto-config路径
                'rpc_start_port': 12301
                }
            eg2. 单主机分布式节点配置
                {'host': {'host': '127.0.0.1', 'port': 36000, 'user': 'root', 'password': '...'},
                'rpc_start_port': 12301,
                'crypto_config_path': 'resources/crypto-config',  # 本地crypto-config路径
                'nodes': [
                    {'release_path': '/home/hzc/chainmaker-go/build/release/chainmaker-v3.0.0_alpha-wx-org1.chainmaker.org'},
                    {'release_path': '/home/hzc/chainmaker-go/build/release/chainmaker-v3.0.0_alpha-wx-org2.chainmaker.org'},
                    {'release_path': '/home/hzc/chainmaker-go/build/release/chainmaker-v3.0.0_alpha-wx-org3.chainmaker.org'},
                    {'release_path': '/home/hzc/chainmaker-go/build/release/chainmaker-v3.0.0_alpha-wx-org4.chainmaker.org',
                     'rpc_port': 12304},
                    ]
                }
            eg3. 多主机节点配置
                {'crypto_config_path': 'resources/crypto-config'  # 本地crypto-config路径
                 'nodes': [
                    {'host': {'host': '127.0.0.1', 'port': 36000, 'user': 'root', 'password': '...')},
                     'release_path': '/home/hzc/chainmaker-go/build/release/chainmaker-v3.0.0_alpha-wx-org1.chainmaker.org'},
                    {'host': {'host': '127.0.0.2', 'port': 36000, 'user': 'root', 'password': '...')},
                     'release_path': '/home/hzc/chainmaker-go/build/release/chainmaker-v3.0.0_alpha-wx-org2.chainmaker.org'},
                    {'host': {'host': '127.0.0.3', 'port': 36000, 'user': 'root', 'password': '...')},
                     'release_path': '/home/hzc/chainmaker-go/build/release/chainmaker-v3.0.0_alpha-wx-org3.chainmaker.org'},
                    {'host': {'host': '127.0.0.4', 'port': 36000, 'user': 'root', 'password': '...')},
                     'release_path': '/home/hzc/chainmaker-go/build/release/chainmaker-v3.0.0_alpha-wx-org4.chainmaker.org',
                     'rpc_port': 12304}
                    ]
                }
        :return: 长安链集群对象
        """
        crypto_config_path = server_config.get('crypto_config_path')
        assert crypto_config_path, 'server_config需包含本地crypto_config_path配置'

        host_config = server_config.get('host') or {}

        if not host_config:
            host = None
        elif host_config.get('host') in ['127.0.0.1', 'localhost']:
            host = Local(**host_config)
        else:
            host = Host(**host_config)

        rpc_start_port = server_config.get('rpc_port') or server_config.get('rpc_start_port') or 12301
        #
        # crypto_config = CryptoConfig(crypto_config_path, host=host_config.get('host', '127.0.0.1'),
        #                              rpc_start_port=rpc_start_port)

        crypto_config = load_crypto_config(crypto_config_path, host=host_config.get('host', '127.0.0.1'),
                                           rpc_start_port=rpc_start_port)
        cc = cc or crypto_config.new_chain_client(endorsers_cnt=crypto_config.org_or_node_cnt, conn_node=0)

        if 'nodes' in server_config:
            nodes_config = server_config.get('nodes')
        else:
            assert host_config, 'server_config需包含host配置'
            chainmaker_go_path = server_config.get('chainmaker_go_path') or f"{host.workspace}/chainmaker-go"
            release_paths = get_release_paths_by_chainmaker_go_path(host, chainmaker_go_path)
            nodes_config = [{'release_path': item} for item in release_paths]

        nodes = []
        for index, item in enumerate(nodes_config):
            node_host = host if host_config else Host(**item.get('host'))
            release_path = item.get('release_path')
            rpc_port = item.get('rpc_port') or rpc_start_port + index
            node = ChainMakerNode(index=index, host=node_host, release_path=release_path, rpc_port=rpc_port,
                                  crypto_config=crypto_config, cc=cc)
            nodes.append(node)
        return cls(nodes=nodes, crypto_config=crypto_config, cc=cc)
