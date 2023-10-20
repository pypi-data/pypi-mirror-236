#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   deploy_utils.py
# @Function     :   chainmaker-go部署实用方法
import os
import time
import warnings
from typing import List, Union

from chainmaker.utils.server_utils import ChainMakerCluster

try:
    from hostz import Host, Local
except ImportError:
    print('please install hostz: pip install hostz')

try:
    from logz import log
except ImportError:
    print('please install logz: pip install logz')

from chainmaker.keys import AuthType, ConsensusType, HashType, AlgoType, TxPoolType, DbProvider

CHAINMAKER_GO_REPO = 'git@git.code.tencent.com:ChainMaker/chainmaker-go.git'
CHAINMAKER_CRYPTOGEN_REPO = 'git@git.code.tencent.com:ChainMaker/chainmaker-cryptogen.git'
VM_ENGINE_REPO = 'git@git.code.tencent.com:ChainMaker/vm-engine.git'
VM_DOCKER_GO_REPO = 'git@git.code.tencent.com:ChainMaker/vm-docker-go.git'


class BaseChainBuilder:
    @staticmethod
    def _get_version_from_branch(branch: str):
        return branch.split('_')[0]

    @staticmethod
    def wait(self, secs: int = 1):
        time.sleep(secs)
        return self


class SingleHostChainBuilder(BaseChainBuilder):
    def __init__(self, host: Union[Host, Local], workspace: str = None, crypto_config_path: str = 'crypto-config'):
        """
        :param host: 远程主机对象
        :param workspace: chainmaker-go / chainmaker-cryptogen / vm-engine / vm-docker-go 上级目录
        :param crypto_config_path: 本地的crypto-config路径(部署后自动下载)

        """
        self._logger = log
        self.host = host
        self.workspace = workspace or self.host.workspace.rstrip("/")
        self.crypto_config_path = crypto_config_path

        self.chainmaker_go_path = f'{self.workspace}/chainmaker-go'
        self.chainmaker_cryptogen_path = f'{self.workspace}/chainmaker-cryptogen'
        self.vm_engine_path = f'{self.workspace}/vm-engine'

        self.scripts_path = f'{self.chainmaker_go_path}/scripts'

    @staticmethod
    def _get_prepare_script_by_auth_type(auth_type: AuthType):
        if auth_type == AuthType.PermissionedWithCert:
            prepare_script = 'prepare.sh'
        elif auth_type == AuthType.PermissionedWithKey:
            prepare_script = 'prepare_pwk.sh'
        else:
            prepare_script = 'prepare_pk.sh'
        return prepare_script

    def switch_branch(self, branch, enable_vm_go: bool = False, enable_vm_docker_go: bool = False) -> str:
        """切换分支"""
        result = ''
        result += self._prepare_chainmaker_cryptogen()
        result += self._prepare_chainmaker_go(branch)
        if enable_vm_go:
            result += self._prepare_vm_engine(branch)
        if enable_vm_docker_go:
            result += self._prepare_vm_docker_go(branch)

        self._logger.debug(f'重置并切换chainmaker-go分支为{branch}')
        result += self.host.run(f'git reset --hard && git remote prune origin && git checkout {branch} && git pull;',
                                workspace=self.chainmaker_go_path)
        return result

    def prepare(self, auth_type=AuthType.PermissionedWithCert,
                chain_cnt: int = 1, node_cnt: int = 4,
                consensus_type: ConsensusType = ConsensusType.TBFT,
                p2p_port: int = 11301, rpc_port: int = 12301,
                vm_go_runtime_port: int = 32351, vm_go_engine_port: int = 22351,
                vm_go_transport_protocol='tcp', log_level: str = 'INFO',
                enable_vm_go: bool = False, hash_type: HashType = HashType.SHA256,
                docker_java_engine_port: int = 22351, enable_docker_java: bool = False) -> str:
        # version = branch.split('_')[0]
        # vm_engine_branch = f'{version}_qc'
        enable_vm_go = 'true' if enable_vm_go else 'false'
        enable_docker_java = 'true' if enable_docker_java else 'false'
        prepare_script = self._get_prepare_script_by_auth_type(auth_type)

        # if enable_vm_go is True:
        # self._prepare_vm_engine(vm_engine_branch)

        self._logger.debug(f'执行 {prepare_script}')
        if auth_type == AuthType.PermissionedWithCert:
            cmd = (f'sh prepare.sh {node_cnt} {chain_cnt} {p2p_port} {rpc_port} '
                   f'{vm_go_runtime_port} {vm_go_engine_port} {docker_java_engine_port} '
                   f'-c {consensus_type.value} -l {log_level} '
                   f'-v {enable_vm_go} --vlog={log_level} '
                   f'-j {enable_docker_java} --jlog={log_level};')

        elif auth_type == AuthType.Public:
            cmd = f'''echo '{hash_type.name}
' | ''' + (f'sh prepare_pk.sh {node_cnt} {chain_cnt} {p2p_port} {rpc_port} '
           f'{vm_go_runtime_port} {vm_go_engine_port} {docker_java_engine_port} '
           f'-c {consensus_type.value} -l {log_level} '
           f'--hash {hash_type.name} '
           f'-v {enable_vm_go} --vlog={log_level} '
           f'-j {enable_docker_java} --jlog={log_level};')
        else:
            cmd = f'''echo '{hash_type.name}
' | ''' + (f'sh prepare_pwk.sh {node_cnt} {chain_cnt} {p2p_port} {rpc_port} '
           f'{vm_go_runtime_port} {vm_go_engine_port} {docker_java_engine_port} '
           f'-c {consensus_type.value} -l {log_level} --hash {hash_type.name} '
           f'-v {enable_vm_go} --vlog={log_level} '
           f'-j {enable_docker_java} --jlog={log_level};')
        result = self.host.run(cmd, workspace=self.scripts_path)
        return result

    def build_release(self) -> str:
        self._logger.debug('执行 build_release.sh')
        result = self.host.run(f'sh build_release.sh;', workspace=self.scripts_path)
        return result

    def start_cluster(self) -> str:
        self._logger.debug('启动集群')
        result = self.host.run(f'sh cluster_quick_start.sh normal >/dev/null 2>&1;', workspace=self.scripts_path)
        self.wait(1)
        return result

    def stop_cluster(self, clean: bool = True) -> str:
        self._logger.debug('停止集群')
        cmd = 'sh cluster_quick_stop.sh clean;' if clean else 'sh cluster_quick_stop.sh;'
        result = self.host.run(cmd, workspace=self.scripts_path)
        self.wait(1)
        return result

    def deploy(self, branch: str,
               auth_type=AuthType.PermissionedWithCert,
               chain_cnt: int = 1,
               node_cnt: int = 4,
               total_node_cnt: int = None,
               consensus_type: ConsensusType = ConsensusType.TBFT,
               algo_type: AlgoType = AlgoType.EC,
               hash_type: HashType = HashType.SHA256,
               log_level: str = 'INFO',
               p2p_port: int = 11301,
               rpc_port: int = 12301,
               vm_go_runtime_port: int = 32351,
               vm_go_engine_port: int = 22351,
               vm_go_transport_protocol='tcp',
               enable_vm_go: bool = False,
               enable_vm_docker_go: bool = False,
               docker_go_log_level: str = 'INFO',
               enable_docker_java: bool = False,
               docker_java_engine_port: int = 22351,
               docker_java_log_level: str = 'INFO',
               start_cluster: bool = True,
               container_name_prefix: str = None,
               chain_id: str = 'chain1',
               txpool_type: TxPoolType = TxPoolType.normal,
               vm_support_list: List[str] = ('wasmer', 'gasm', 'evm', 'dockergo', 'wxvm', 'docker_java'),
               db_provider: DbProvider = DbProvider.leveldb,
               db_dns: str = None,
               enable_file_db: bool = True,
               enable_fast_sync: bool = True,
               spv_cnt: int = None,
               ):
        """
        部署chainmaker-go
        :param db_dns:
        :param spv_cnt:
        :param enable_fast_sync:
        :param enable_file_db:
        :param chain_id:
        :param db_provider:
        :param enable_docker_java:
        :param docker_java_engine_port:
        :param container_name_prefix:
        :param docker_go_log_level:
        :param docker_java_log_level:
        :param txpool_type:
        :param vm_support_list:
        :param branch: chainmaker-go / chainmaker-cryptogen / vm-engine  / vm-docker-go 分支
        :param auth_type: 权限类型
        :param chain_cnt: 链数量
        :param node_cnt: 共识节点数量
        :param total_node_cnt: 总节点数量
        :param consensus_type: 共识类型
        :param algo_type: 公钥算法类型
        :param hash_type: 哈希类型
        :param log_level: 日志登记
        :param p2p_port: 起始P2P端口
        :param rpc_port: 起始RPC端口
        :param vm_go_runtime_port: 起始VmGo运行时端口
        :param vm_go_engine_port: 起始VmEngine运行时端口
        :param vm_go_transport_protocol: VmGo传输类型 'tcp'/ 'utp'
        :param enable_vm_go: 是否启用 VmEngine
        :param enable_vm_docker_go:  是否启用 VmDockerGo
        :param start_cluster: 部署后是否启动集群
        :return: 当前链对象
        """
        result = ''
        self._logger.info(f'部署chainmaker-go {auth_type} {consensus_type} {node_cnt}节点')

        # 查看Golang版本
        result += self.host.run('go version')

        # 准备项目并切换分支
        result += self.switch_branch(branch, enable_vm_go, enable_vm_docker_go)

        # 修改chainmaker-cryptogen 加密类型及哈希类型配置
        result += self._modify_chainmaker_cryptogen_config(auth_type, algo_type.value, hash_type.value)

        # 停止原有链
        result += self.stop_cluster()

        # 清理原build
        result += self.host.run('rm -rf build', workspace=self.chainmaker_go_path)

        if total_node_cnt is None:
            total_node_cnt = node_cnt
        # 执行prepare
        result += self.prepare(auth_type, chain_cnt, total_node_cnt, consensus_type, p2p_port, rpc_port,
                               vm_go_runtime_port,
                               vm_go_engine_port, vm_go_transport_protocol, log_level, enable_vm_go, hash_type,
                               docker_java_engine_port=docker_java_engine_port,
                               enable_docker_java=enable_docker_java)

        # 修改build/config配置节点数量
        if total_node_cnt > node_cnt:
            result += self._modify_config_node_cnt(node_cnt, total_node_cnt, p2p_port, auth_type, chain_cnt=chain_cnt)

        if container_name_prefix:
            self._modify_start_stop_sh(container_name_prefix)

        if chain_id != 'chain1':
            self._modify_chain_id(chain_id)

        if txpool_type != TxPoolType.normal:
            self._modify_txpool_type(txpool_type)

        # 执行build_release
        result += self.build_release()

        # 启动集群
        if start_cluster is True:
            result += self.start_cluster()
            process_num = self.check_chainmaker_process_number()
            assert process_num == str(total_node_cnt), '部署失败'

            # 停止多余节点
            if total_node_cnt > node_cnt:
                result += (self.stop_nodes(list(range(node_cnt + 1, total_node_cnt + 1))) or '')

            process_num = self.check_chainmaker_process_number()
            assert process_num == str(node_cnt), '部署失败'

            # 下载crypto-config到本地
            # download_crypto_config(self.host, self.chainmaker_go_path, self.crypto_config_path)  # fixme
            # return self.get_cluster(rpc_port)
        return result

    def _modify_chain_id(self, chain_id: str, chain_cnt=1):
        result = ''
        for i in range(1, chain_cnt + 1):
            result += self.host.run(f"sed -i 's/chain1/{chain_id}/g' ../build/config/node*/chainconfig/bc{i}.yml",
                                    workspace=self.scripts_path)
        return result

    def _modify_txpool_type(self, txpool_type: TxPoolType):
        result = self.host.run(
            f"sed -i 's/pool_type: .*/pool_type: {txpool_type.name}/g' ../build/config/node*/chainmaker.yml",
            workspace=self.scripts_path)
        return result

    def get_cluster(self, rpc_port) -> ChainMakerCluster:
        """部署并下载crypto-config到本地后获取集群对象"""
        return ChainMakerCluster.from_chainmaker_go(self.host, self.chainmaker_go_path, self.crypto_config_path,
                                                    rpc_port)

    def deploy_cert_4_nodes_tbft_enable_vm_go(self, branch=None) -> bool:
        warnings.warn('即将废弃', DeprecationWarning)
        if branch:
            self.host.run(f'git reset --hard && git remote prune origin && git checkout {branch} && git pull',
                          workspace=self.chainmaker_go_path)
        # cmd = '''sh cluster_quick_stop.sh clean
        # sh prepare.sh 4 1 11301 12301 32351 22351 -c 1 -l INFO -v true --vtp=tcp --vlog=INFO
        # sh build_release.sh
        # sh cluster_quick_start.sh normal
        #         '''
        self.host.run('sh cluster_quick_stop.sh clean >/dev/null 2>&1', workspace=self.scripts_path)
        self.host.run(
            'sh prepare.sh 4 1 11301 12301 32351 22351 23351 -c 1 -l INFO -v true --vlog=INFO -j false -jlog=INFO',
            workspace=self.scripts_path)
        self.host.run('sh build_release.sh', workspace=self.scripts_path)
        self.host.run('sh cluster_quick_start.sh normal >/dev/null 2>&1', workspace=self.scripts_path)

        if self.host.run('ps -ef | grep chainmaker | grep -v "grep" | wc -l') == '4':
            return True
        return False

    def deploy_pwk_4_nodes_raft_not_enable_vm_go(self, branch=None) -> bool:
        warnings.warn('即将废弃', DeprecationWarning)
        if branch:
            self.host.run(f'git reset --hard && git remote prune origin && git checkout {branch} && git pull',
                          workspace=self.chainmaker_go_path)

        self.host.run('sh cluster_quick_stop.sh clean', workspace=self.scripts_path)
        self.host.run(
            'sh prepare_pwk.sh 4 1 11301 12301 32351 22351 23351 -c 4 -l INFO -v false --hash=SHA256 --vtp=tcp --vlog=INFO -j false -jlog=INFO',
            workspace=self.scripts_path)
        self.host.run('sh build_release.sh', workspace=self.scripts_path)
        self.host.run('sh cluster_quick_start.sh normal >/dev/null 2>&1', workspace=self.scripts_path)

        if self.host.run('ps -ef | grep chainmaker | grep -v "grep" | wc -l') == '4':
            return True
        return False

    def deploy_pk_4_nodes_dpos_not_enable_vm_go(self, branch=None) -> bool:
        warnings.warn('即将废弃', DeprecationWarning)
        if branch:
            self.host.run(f'git reset --hard && git remote prune origin && git checkout {branch} && git pull',
                          workspace=self.chainmaker_go_path)

        version = branch.split('_')[0]
        result = self.host.run(f'docker images | grep "chainmaker-vm-engine" | grep "{version}"')
        if not result:
            self.host.run(f'git reset --hard && git checkout {branch} && make build-image',
                          workspace=self.vm_engine_path)

        self.host.run('sh cluster_quick_stop.sh clean', workspace=self.scripts_path)
        self.host.run(
            'sh prepare_pk.sh 4 1 11301 12301 32351 22351 23351 -c 5 -l INFO -v false --hash=SHA256 --vtp=tcp --vlog=INFO -j false -jlog=INFO',
            workspace=self.scripts_path)
        self.host.run('sh build_release.sh', workspace=self.scripts_path)
        self.host.run('sh cluster_quick_start.sh normal >/dev/null 2>&1', workspace=self.scripts_path)

        if self.host.run('ps -ef | grep chainmaker | grep -v "grep" | wc -l') == '4':
            return True
        return False

    def deploy_cert_10_nodes_tbft_enable_vm_go(self, branch=None, rpc_port=32301,
                                               container_name_prefix: str = None) -> bool:
        warnings.warn('即将废弃', DeprecationWarning)
        if branch:
            self.host.run(f'git reset --hard && git remote prune origin && git checkout {branch} && git pull',
                          workspace=self.chainmaker_go_path)

        version = self._get_version_from_branch(branch)
        result = self.host.run(f'docker images | grep "chainmaker-vm-engine" | grep "{version}"')
        if not result:
            self.host.run(f'git reset --hard && git checkout {branch} && make build-image',
                          workspace=self.vm_engine_path)

        self.host.run('sh cluster_quick_stop.sh clean', workspace=self.scripts_path)
        self.host.run('rm -rf ../build')

        if container_name_prefix:
            self._modify_start_stop_sh(container_name_prefix)

        self.host.run(
            f'sh prepare.sh 10 1 31301 {rpc_port} 62351 62451 62551 -c 1 -l INFO -v true --vlog=INFO -j false -jlog=INFO',
            workspace=self.scripts_path)

        # 修改为4个共识节点
        self.host.run("sed -i '/- org_id: \"wx-org5.chainmaker.org\"/,/- org_id: \"{org11_id}\"/d' "
                      "../build/config/node*/chainconfig/bc1.yml", workspace=self.scripts_path)
        self.host.run("sed -i '/31305\/p2p/,/31310\/p2p/d' ../build/config/node*/chainmaker.yml",
                      workspace=self.scripts_path)

        self.host.run('sh build_release.sh', workspace=self.scripts_path)
        self.host.run('sh cluster_quick_start.sh normal >/dev/null 2>&1', workspace=self.scripts_path)

        if self.host.run('ps -ef | grep chainmaker | grep -v "grep" | wc -l') != '10':
            self._logger.debug('部署失败')

        # 停止node5-node10
        for sn in range(5, 11):
            self.host.run('sh stop.sh full && cd -',
                          workspace=f'{self.chainmaker_go_path}/build/release/chainmaker-*{sn}*/bin')

        if self.host.run('ps -ef | grep chainmaker | grep -v "grep" | wc -l') == '4':
            return True
        return False

    def check_chainmaker_process_number(self) -> int:  # todo 仅限当前主机仅一条链
        self._logger.debug('检查chainmaker节点数')
        result = self.host.run('ps -ef | grep "./chainmaker start -c" | grep -v "grep" | wc -l')
        return result

    def stop_nodes(self, node_sn_list: List[int]):
        self._logger.debug(f'停止节点 {node_sn_list}')
        for sn in node_sn_list:
            self.host.run('sh stop.sh full',
                          workspace=f'{self.chainmaker_go_path}/build/release/chainmaker-*{sn}*/bin')

    def start_nodes(self, node_sn_list: List[int]):
        self._logger.debug(f'启动节点 {node_sn_list}')
        for sn in node_sn_list:
            self.host.run('sh stop.sh full && sh start full -y',
                          workspace=f'{self.chainmaker_go_path}/build/release/chainmaker-*{sn}*/bin')

    def restart_nodes(self, node_sn_list: List[int]):
        self._logger.debug(f'重启节点 {node_sn_list}')
        for sn in node_sn_list:
            self.host.run('sh restart.sh full',
                          workspace=f'{self.chainmaker_go_path}/build/release/chainmaker-*{sn}*/bin')

    def distribute(self, nodes_config: List[dict]):
        # 拷贝release包到各节点
        result = self.host.run('ls -rt| grep "chainmaker" | grep ".gz";',
                               workspace=f'{self.chainmaker_go_path}/build/release/').split()

        if 'node1' in result[0]:
            result = sorted(result, key=lambda x: int(x.split('-')[2].lstrip('node').rstrip('/')))
        else:
            result = sorted(result, key=lambda x: int(x.split('-')[3].lstrip('org').rstrip('.chainmaker.org/')))

        for _from, node_config in zip(result, nodes_config):
            file_name = os.path.basename(_from)
            host, port, user, password = (node_config['host'], node_config.get('port'), node_config.get('user'),
                                          node_config['password'])
            _to = f"{node_config.get('workspace')}/{file_name}"
            # self.host.scp(_from, _to, host, user, password, port, workspace=f'{self.chainmaker_go_path}/build/release/')
            node_host = Host(host, port, user, password, workspace=os.path.dirname(_to))
            node_host.untar(_to)
            node_host.run(f'rm -rf {_to}')

    def _prepare_chainmaker_go(self, branch: str) -> str:
        result = ''
        if not self.host.exists(self.chainmaker_go_path):
            result += self.host.run(f'git clone -b {branch} {CHAINMAKER_GO_REPO}')
        if not self.host.exists(f'{self.chainmaker_go_path}/tools/chainmaker-cryptogen'):
            result += self.host.run(f'ln -s {self.chainmaker_cryptogen_path} {self.chainmaker_go_path}/tools/')
        return result

    def _prepare_chainmaker_cryptogen(self, branch: str = 'develop') -> str:
        result = ''
        chainmaker_cryptogen_path = f'{self.workspace}/chainmaker-cryptogen'
        if not self.host.exists(chainmaker_cryptogen_path):
            result += self.host.run(f'git clone -b {branch} {CHAINMAKER_CRYPTOGEN_REPO}', workspace=self.workspace)
            result += self.host.run('make', workspace=chainmaker_cryptogen_path)
        return result

    def _prepare_vm_engine(self, branch: str) -> str:
        result = ''
        version = branch.split('_')[0]
        vm_engine_path = f'{self.workspace}/vm-engine'
        if not self.host.exists(vm_engine_path):
            result += self.host.run(f'git clone -b {branch} {VM_ENGINE_REPO}', workspace=self.workspace)
        self._logger.debug('检查docker镜像')
        result += self.host.run(f'docker images | grep "chainmaker-vm-engine" | grep "{version}"')
        if not result:
            result += self.host.run(f'git reset --hard && git checkout {branch} && make build-image',
                                    workspace=vm_engine_path)
        return result

    def _prepare_vm_docker_go(self, branch: str) -> str:
        result = ''
        version = branch.split('_')[0]
        vm_docker_go_path = f'{self.workspace}/vm-docker-go'
        if not self.host.exists(vm_docker_go_path):
            result += self.host.run(f'git clone -b {branch} {VM_DOCKER_GO_REPO}', workspace=self.workspace)
        self._logger.debug('检查docker镜像')
        result += self.host.run(f'docker images | grep "chainmaker-vm-docker-go" | grep "{version}"')
        if not result:
            result += self.host.run(f'git reset --hard && git checkout {branch} && make build-image',
                                    workspace=vm_docker_go_path)
        return result

    def _modify_config_node_cnt(self, node_cnt, total_node_cnt, p2p_port,
                                auth_type: AuthType = AuthType.PermissionedWithCert, chain_cnt=1) -> str:
        """修改build/config中节点数量"""
        result = ''
        assert total_node_cnt <= 10, '目前仅支持最大10节点'
        self._logger.debug(f'修改 build/config中节点数量为 {node_cnt}')
        if auth_type == AuthType.PermissionedWithCert:
            sn = node_cnt + 1
            for i in range(1, chain_cnt + 1):
                result += self.host.run("sed -i '/- org_id: \"wx-org%d.chainmaker.org\"/,/- org_id: \"{org11_id}\"/d' "
                                        f"../build/config/node*/chainconfig/bc%d.yml" % (sn, i),
                                        workspace=self.scripts_path)

        elif auth_type == AuthType.Public:
            _pattern = 'n;' * (node_cnt + 1) + 'N;' * (total_node_cnt - node_cnt + 1) + ';d'
            for i in range(1, chain_cnt + 1):
                result += self.host.run(
                    "sed -i '/node_id/{%s}' ../build/config/node*/chainconfig/bc%d.yml" % (_pattern, i),
                    workspace=self.scripts_path)

        result += self.host.run("sed -i '/%d\/p2p/,/%d\/p2p/d' "
                                "../build/config/node*/chainmaker.yml" % (
                                    p2p_port + node_cnt, p2p_port + total_node_cnt - 1),
                                workspace=self.scripts_path)
        return result

    def _modify_chainmaker_cryptogen_config(self, auth_type, pk_algo: str, hash_algo: str) -> str:
        """
        修改chainmaker-cryptogen算法类型及哈希类型配置
        :param auth_type:
        :param pk_algo:
        :param hash_algo:
        :return:
        """
        result = ''
        self._logger.debug(f'修改chainmaker-cryptogen配置为: {pk_algo}-{hash_algo}')
        if auth_type == AuthType.PermissionedWithCert:
            config_file = f'{self.chainmaker_cryptogen_path}/config/crypto_config_template.yml'
        elif auth_type == AuthType.PermissionedWithKey:
            config_file = f'{self.chainmaker_cryptogen_path}/config/pwk_config_template.yml'
        else:
            config_file = f'{self.chainmaker_cryptogen_path}/config/pk_config_template.yml'

        result += self.host.execute(f"sed -i 's/pk_algo: .*/pk_algo: {pk_algo}/g' {config_file}")

        if auth_type == AuthType.PermissionedWithCert:
            result += self.host.execute(f"sed -i 's/ski_hash: .*/ski_hash: {hash_algo}/g' {config_file}")
        else:
            result += self.host.execute(f"sed -i 's/hash_algo: .*/hash_algo: {hash_algo}/g' {config_file}")
        return result

    def _enable_vm_docker_go_in_chainmaker_yml(self):
        chainmaker_yml_vm_docker_go_config = '''# Docker go virtual machine configuration
      docker_go:
        # Enable docker go virtual machine
        enable_dockervm: true
        # Mount point in chainmaker
        dockervm_mount_path: ../data/wx-org1.chainmaker.org/docker-go
        # Specify log file path
        dockervm_log_path: ../log/wx-org1.chainmaker.org/docker-go
        # Whether to self._logger.debug log at terminal
        log_in_console: true
        # Log level
        log_level: DEBUG
        # Unix domain socket open, used for chainmaker and docker manager communication
        uds_open: true
        # docker vm contract service host, default 127.0.0.1
        docker_vm_host: 127.0.0.1
        # docker vm contract service port, default 22351
        docker_vm_port: 22451
        # Grpc max send message size, Default size is 4, Unit: MB
        max_send_msg_size: 20
        # Grpc max receive message size, Default size is 4, Unit: MB
        max_recv_msg_size: 20
        # max number of connection created to connect docker vm service
        max_connection: 5'''
        chainmaker_go_path = f'{self.workspace}/chainmaker-go'
        any_chainmaker_yml_path = f'{chainmaker_go_path}/build/release/${{release_path}}/config/*/chainmaker.yml'
        result = self.host.run(f"for release_path in `ls -d */` ; do echo '{chainmaker_yml_vm_docker_go_config}' "
                               f">> {any_chainmaker_yml_path}; done",
                               workspace=f'{self.workspace}/chainmaker-go/build/release')
        return result

    def _modify_start_stop_sh(self, container_name_prefix: str):
        self.host.run(f"sed -i 's/container_name=/container_name={container_name_prefix}-/g' bin/start.sh",
                      workspace=self.scripts_path)
        self.host.run(f"sed -i 's/--name /--name {container_name_prefix}-/g' bin/start.sh",
                      workspace=self.scripts_path)
        self.host.run(f"sed -i 's/_container_name=/_container_name={container_name_prefix}-/g' bin/stop.sh",
                      workspace=self.scripts_path)


class MultiSignChainBuilder(BaseChainBuilder):
    def __init__(self, workspace):
        self.host = Local(workspace=workspace)

    def build_release(self):
        pass

    def deploy(self, nodes_config: List[dict], slave_config: dict):
        """分发"""
        # 拷贝release包到各节点
        result = self.host.run('ls -rt| grep "chainmaker" | grep ".gz";',
                               workspace=f'{self.chainmaker_go_path}/build/release/').split()

        if 'node1' in result[0]:
            result = sorted(result, key=lambda x: int(x.split('-')[2].lstrip('node').rstrip('/')))
        else:
            result = sorted(result, key=lambda x: int(x.split('-')[3].lstrip('org').rstrip('.chainmaker.org/')))

        for _from, node_config in zip(result, nodes_config):
            user = node_config.get('user')
            password = node_config.get('password')
            port = node_config.get('port')
            _to = node_config.get('workspace')
            self.host.scp(_from, _to, user, password, port)

        # 拷贝crypto-config到压测机
        _from = self.host.run('ls -rt| grep "crypto-config" | grep ".gz";',
                              workspace=f'{self.chainmaker_go_path}/build/release/').split()
        user = slave_config.get('user')
        password = slave_config.get('password')
        port = slave_config.get('port')
        _to = slave_config.get('workspace')
        self.host.scp(_from, _to, user, password, port)


class DockerChainBuild(BaseChainBuilder):
    pass


class K8sChainBuild(BaseChainBuilder):
    pass
