#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   chain_config.py
# @Function     :   sdk_config链配置及默认配置
import logging
# from dataclasses import dataclass
from pathlib import Path
from typing import List, Union, Dict

from chainmaker.exceptions import SdkConfigError
from chainmaker.keys import AuthType, HashType, AddrType
# SDK_MESSAGE_TYPE = os.getenv('SDK_MESSAGE_TYPE') or ResultMessageType.DICT
# SDK_RESULT_TYPE = os.getenv('SDK_MESSAGE_TYPE') or ResultType.ORIGIN
from chainmaker.utils.file_utils import load_yaml


class ClientUserConfig:
    """sdk_config.yml用户配置"""
    def __init__(self, user_sign_key_file_path: str, user_sign_crt_file_path: str = None, user_sign_key_pwd: str = None,
                 user_key_file_path: str = None, user_crt_file_path: str = None, user_key_pwd: str = None,
                 user_enc_key_file_path: str = None, user_enc_crt_file_path: str = None, user_enc_key_pwd: str = None,
                 org_id: str = None, crypto: Dict[str, str] = None, auth_type: str = None, alias: str = None):
        """

        :param user_sign_key_file_path:
        :param user_sign_crt_file_path: 客户端用户交易签名证书路径(若未设置，将使用user_crt_file_path)
        :param user_sign_key_pwd:
        :param user_key_file_path: 客户端用户(TLS)私钥路径
        :param user_crt_file_path: 客户端用户(TLS)证书路径
        :param user_key_pwd: 客户端用户私钥密码(无密码则不需要设置)
        :param user_enc_key_file_path: 客户端用户加密证书路径(tls加密证书，应用于国密GMTLS双证书体系；若未设置仅使用单证书）
        :param user_enc_crt_file_path: 客户端用户交易签名私钥路径(若未设置，将使用user_key_file_path)
        :param user_enc_key_pwd:
        :param org_id:
        :param crypto: 签名使用的哈希算法，和节点保持一致, eg. {'hash': 'SHA256'}
        :param auth_type:
        :param alias: 当前签名证书的别名。当设置此配置项时，chain client 对象将自动检查链上是否已添加此别名，
                      如果没有则自动上链此证书别名， 并且后续所有交易都会使用别名，别名可降低交易体大小。若为空则不启用。
        """
        self.user_sign_key_file_path = user_sign_key_file_path
        self.user_sign_crt_file_path = user_sign_crt_file_path
        self.user_sign_key_pwd = user_sign_key_pwd
        self.user_key_file_path = user_key_file_path
        self.user_crt_file_path = user_crt_file_path
        self.user_key_pwd = user_key_pwd
        self.user_enc_key_file_path = user_enc_key_file_path
        self.user_enc_crt_file_path = user_enc_crt_file_path
        self.user_enc_key_pwd = user_enc_key_pwd
        self.org_id = org_id
        self.crypto = crypto
        self.auth_type = auth_type
        self.alias = alias


class ClientNodeConfig:
    def __init__(self, node_addr: str, conn_cnt: int = None, enable_tls: bool = None,
                 trust_root_paths: List[str] = None, tls_host_name: str = None, **kwargs):
        """

        :param node_addr: 节点地址，格式为：IP:端口
        :param conn_cnt: 节点连接数
        :param enable_tls: RPC连接是否启用双向TLS认证
        :param trust_root_paths: 信任证书池路径
        :param ls_host_name: TLS hostname
        """
        self.node_addr = node_addr
        self.conn_cnt = conn_cnt
        self.enable_tls = enable_tls
        self.trust_root_paths = trust_root_paths
        self.tls_host_name = tls_host_name


class ArchiveConfig:
    """数据归档链外存储相关配置"""
    def __init__(self, type: str, dest: str, secret_key: str, **kwargs):
        """
        :param type: eg. 'mysql'
        :param dest: eg. 'root:passw0rd:localhost:3306'
        :param secret_key:
        """
        self.type = type
        self.dest = dest
        self.secret_key = secret_key


class RpcClientConfig:
    """sdk_config.yml RPC客户端配置
    参考 https://grpc.github.io/grpc/core/group__grpc__arg__keys.html
    """
    def __init__(self, max_receive_message_size: int = None, max_send_message_size: int = None,
                 send_tx_timeout: int = None, get_tx_timeout: int = None, **kwargs):
        self.max_receive_message_size = max_receive_message_size
        self.max_send_message_size = max_send_message_size
        self.send_tx_timeout = send_tx_timeout
        self.get_tx_timeout = get_tx_timeout


class Pkcs11Config:
    """sdk_config.yml PKCS11配置"""
    def __init__(self, enabled: bool, library: str, label: str, password: str, session_cache_size: int, hash: str, **kwargs):
        """
        :param enabled: 默认不启用
        :param library: pkcs11动态链接库.son文件路径
        :param label: label for the slot to be used
        :param password: password to logon the HSM(Hardware security module)
        :param session_cache_size: size of HSM session cache, default to 10
        :param hash: hash algorithm used to compute SKI
        """
        self.enabled = enabled
        self.library = library
        self.label = label
        self.password = password
        self.session_cache_size = self
        self.hash = hash

class ArchiveCenterConfigTLSConfig:

    def __init__(self, server_name: str, priv_key_file: str, cert_file: str, trust_ca_list: List[str], **kwargs):
        self.server_name = server_name
        self.priv_key_file = priv_key_file
        self.cert_file = cert_file
        self.trust_ca_list = trust_ca_list


class ArchiveCenterConfig:
    def __init__(self, chain_genesis_hash: str,
                 archive_center_http_url: str = None,
                 request_second_limit: int = None,
                 rpc_address: str = None,
                 tls_enable: bool = None,
                 tls: dict = None, **kwargs):
        self.chain_genesis_hash = chain_genesis_hash
        self.archive_center_http_url = archive_center_http_url
        self.request_second_limit = request_second_limit
        self.rpc_address = rpc_address
        self.tls_enable = tls_enable
        self.tls = ArchiveCenterConfigTLSConfig(**tls) if isinstance(tls, dict) else None

class ChainClientConfig(ClientUserConfig):
    def __init__(self, chain_id: str, nodes: List[ClientNodeConfig],
                 user_sign_key_file_path: str, user_sign_crt_file_path: str = None, user_sign_key_pwd: str = None,
                 user_key_file_path: str = None, user_crt_file_path: str = None, user_key_pwd: str = None,
                 user_enc_key_file_path: str = None, user_enc_crt_file_path: str = None, user_enc_key_pwd: str = None,
                 org_id: str = None, crypto: Dict[str, str] = None, auth_type: str = None, alias: str = None,
                 retry_limit: int = None, retry_interval: int = None, retry_timeout: int = None,
                 archive: ArchiveConfig = None,
                 rpc_client: RpcClientConfig = None,
                 pkcs11: Pkcs11Config = None,
                 enable_normal_key: bool=None,
                 endorsers: List[ClientUserConfig] = None,
                 **kwargs
                 ):
        """

        :param chain_id: 链Id
        :param nodes: 节点配置列表
        :param user_sign_key_file_path:
        :param user_sign_crt_file_path: 客户端用户交易签名证书路径(若未设置，将使用user_crt_file_path)
        :param user_sign_key_pwd:
        :param user_key_file_path: 客户端用户(TLS)私钥路径
        :param user_crt_file_path: 客户端用户(TLS)证书路径
        :param user_key_pwd: 客户端用户私钥密码(无密码则不需要设置)
        :param user_enc_key_file_path: 客户端用户加密证书路径(tls加密证书，应用于国密GMTLS双证书体系；若未设置仅使用单证书）
        :param user_enc_crt_file_path: 客户端用户交易签名私钥路径(若未设置，将使用user_key_file_path)
        :param user_enc_key_pwd:
        :param org_id:
        :param crypto: 签名使用的哈希算法，和节点保持一致, eg. {'hash': 'SHA256'}
        :param auth_type:
        :param alias: 当前签名证书的别名。当设置此配置项时，chain client 对象将自动检查链上是否已添加此别名，
                      如果没有则自动上链此证书别名， 并且后续所有交易都会使用别名，别名可降低交易体大小。若为空则不启用。
        :param retry_limit: 同步交易结果模式下，轮询获取交易结果时的最大轮询次数，删除此项或设为<=0则使用默认值 60
        :param retry_interval: 同步交易结果模式下，每次轮询交易结果时的等待时间，单位：ms 删除此项或设为<=0则使用默认值 500
        :param retry_timeout: 同步交易结果模式下，轮询获取交易结果时的最大轮询超时时间，单位秒, 和retry_limit二选一，默认30s
        :param archive:
        :param rpc_client:
        :param pkcs11:
        :param endorsers:
        """
        self.chain_id = chain_id
        self.nodes = nodes
        super().__init__(user_sign_key_file_path, user_sign_crt_file_path, user_sign_key_pwd, user_key_file_path,
                         user_crt_file_path, user_key_pwd, user_enc_key_file_path, user_enc_crt_file_path,
                         user_enc_key_pwd, org_id, crypto, auth_type, alias)

        self.retry_limit = retry_limit
        self.retry_interval = retry_interval
        self.retry_timeout = retry_timeout
        self.archive = archive
        self.rpc_client = rpc_client
        self.pkcs11 = pkcs11
        self.enable_normal_key = enable_normal_key
        self.endorsers = endorsers

    @classmethod
    def _check_config(cls, chain_client_config: dict):
        # 签名key未配置时使用用户key(同TLS)

        retry_limit = chain_client_config.get('retry_limit', DefaultConfig.retry_limit)
        if retry_limit is not None:
            if not isinstance(retry_limit, int) or retry_limit <= 0:
                raise SdkConfigError('"retry_limit" must be int and > 0')

        retry_timeout = chain_client_config.get('retry_timeout', DefaultConfig.retry_timeout)
        if retry_timeout is not None:
            if not isinstance(retry_timeout, int) or retry_timeout <= 0:
                raise SdkConfigError('"retry_timeout" must be int and > 0')

        retry_interval = chain_client_config.get('retry_interval', DefaultConfig.retry_interval)
        if retry_interval is not None:
            if not isinstance(retry_interval, int) or retry_interval <= 0:
                raise SdkConfigError('"retry_interval" must be int and > 0')

        archive = chain_client_config.get('archive')
        if archive is not None:
            if not isinstance(archive, dict):
                raise SdkConfigError('"archive" must be dict')

        rpc_client = chain_client_config.get('rpc_client')
        if rpc_client is not None:
            if not isinstance(rpc_client, dict):
                raise SdkConfigError('"rpc_client" must be dict')

        pkcs11 = chain_client_config.get('pkcs11')
        if pkcs11 is not None:
            if not isinstance(pkcs11, dict):
                raise SdkConfigError('"pkcs11" must be dict')

        auth_type = chain_client_config.get('auth_type')
        if auth_type is not None:
            if not isinstance(auth_type, str) or auth_type.lower() not in ('public',
                                                                           'permissionedwithkey',
                                                                           'permissionedwithcert'):
                raise SdkConfigError('"auth_type" must be str and one of '
                                     '"public, permissionedWithKey, permissionedWithCert"')

    @classmethod
    def from_conf(cls, chain_client_config: dict) -> "ChainClientConfig":
        cls._check_config(chain_client_config)
        nodes = chain_client_config.pop('nodes') if 'nodes' in chain_client_config else []
        archive = chain_client_config.pop('archive') if 'archive' in chain_client_config else {}
        rpc_client = chain_client_config.pop('rpc_client') if 'rpc_client' in chain_client_config else {}
        pkcs11 = chain_client_config.pop('pkcs11') if 'pkcs11' in chain_client_config else {}
        archive_center_config = chain_client_config.get('archive_center_config')  or {}

        endorsers = []
        if 'endorsers' in chain_client_config:
            endorsers = chain_client_config.pop('endorsers') or []

        chain_client = ChainClientConfig(**chain_client_config,
                                         nodes=[ClientNodeConfig(**item) for item in nodes])
        chain_client.archive = ArchiveConfig(**archive) if archive else None
        chain_client.rpc_client = RpcClientConfig(**rpc_client) if rpc_client else None
        chain_client.pkcs11 = Pkcs11Config(**pkcs11) if pkcs11 else None
        chain_client.archive_center_config=ArchiveCenterConfig(**archive_center_config) if archive_center_config else None
        # extra
        chain_client.endorsers = [ClientUserConfig(**item) for item in endorsers]
        return chain_client


# @dataclass
class SdkConfig:
    # chain_client: ChainClientConfig
    def __init__(self, chain_client: ChainClientConfig):
        """
        :param chain_client: 链客户端配置
        """
        self.chain_client = chain_client

    @staticmethod
    def _load_sdk_config(sdk_config: Union[dict, str, Path]) -> dict:
        if isinstance(sdk_config, dict):  # 增加支持字典格式的sdk_config
            return sdk_config
        return load_yaml(sdk_config)

    @classmethod
    def from_conf(cls, sdk_config: Union[Path, str, dict]) -> "SdkConfig":
        sdk_config = cls._load_sdk_config(sdk_config)
        chain_client = ChainClientConfig.from_conf(sdk_config.get('chain_client'))
        return cls(chain_client)


class DefaultConfig:
    """链客户端默认配置"""
    chain_id = 'chain1'
    seq = 0  # 默认交易序列号
    endorsers = None  # 默认背书列表 # todo remove
    gas_limit = None

    auth_type = AuthType.PermissionedWithCert
    hash_type = HashType.SHA256
    addr_type = AddrType.ETHEREUM

    # 节点配置
    conn_node = None
    conn_cnt = 10
    node_index = conn_node  # 即将废弃

    tls_home_name = 'chainmaker.org'

    init_version = '1.0'
    upgrade_version = '2.0'

    enable_cert_hash = False

    subscribe_timeout = 60 * 10  # 订阅等待区块超时时间, 单位, 秒
    check_cert_timeout = 30

    with_sync_result = True  #
    with_rwset = False

    # rpc链接
    rpc_retry_interval = 500  # 获取可用客户端连接对象重试时间间隔，单位：ms
    rpc_retry_limit = 3  # 获取可用客户端连接对象最大重试次数

    retry_limit = 90  # 同步交易结果模式下，轮询获取交易结果时的最大轮询次数，删除此项或设为<=0则使用默认值 60 (sdk-go默认为30)
    retry_interval = 500  # 同步交易结果模式下，每次轮询交易结果时的等待时间，单位：ms 删除此项或设为<=0则使用默认值 500
    # 额外
    retry_timeout = 90  # 同步交易结果模式下，轮询获取交易结果时的最大轮询超时时间，单位秒, 和retry_limit二选一，默认30s

    wait_chainmaker_ok_timeout = 60
    wait_chainmaker_ok_interval = 1000

    txpool_full_retry_timeout = 60
    txpool_full_retry_interval = 1000

    # archive_config
    archive_type = 'mysql'
    archive_dest = 'root:123456:localhost:3306'
    archive_secret_key = 'passw0rd'

    # rpc_client_config
    rpc_max_send_message_length = 100  # grpc客户端接收消息时，允许单条message大小的最大值(MB)
    rpc_max_receive_message_length = 100  # grpc客户端发送消息时，允许单条message大小的最大值(MB)
    rpc_send_tx_timeout = 60  # grpc客户端发送交易超时时间 (invoke请求超时时间)
    rpc_get_tx_timeout = 60  # grpc客户端查询交易超时时间 (query请求超时时间)

    # pkcs11_config
    pkcs11_enabled = False  # pkcs11 is not used by default
    pkcs11_library = '/usr/local/lib64 /pkcs11/libupkcs11.so '  # path to the .so file of pkcs11 interface
    pkcs11_label = 'HSM'  # label for the slot to be used
    pkcs11_password = '11111111'  # password to logon the HSM(Hardware security module)
    pkcs11_session_cache_size = 10  # size of HSM session cache, default to 10
    pkcs11_hash = 'SHA256'  # hash algorithm used to compute SKI

    # log_config
    enable_log: bool = True
    logger_name: str = 'sdk'
    log_level: int = logging.DEBUG
    log_format: str = '%(asctime)s.%(msecs)03d\t[%(levelname)s]\t%(message)s'
    log_datefmt: str = '%Y-%m-%d %H:%M:%S'
    log_file: str = None  # 日志文件路径


DEFAULT_ARCHIVE_CONFIG = ArchiveConfig(DefaultConfig.archive_type,
                                       DefaultConfig.archive_dest,
                                       DefaultConfig.archive_secret_key)

DEFAULT_PKCS11_CONFIG = Pkcs11Config(DefaultConfig.pkcs11_enabled, DefaultConfig.pkcs11_library,
                                     DefaultConfig.pkcs11_label, DefaultConfig.pkcs11_password,
                                     DefaultConfig.pkcs11_session_cache_size, DefaultConfig.pkcs11_hash)

DEFAULT_RPC_CLIENT_CONFIG = RpcClientConfig(DefaultConfig.rpc_max_send_message_length,
                                            DefaultConfig.rpc_max_receive_message_length,
                                            DefaultConfig.rpc_send_tx_timeout,
                                            DefaultConfig.rpc_get_tx_timeout)
