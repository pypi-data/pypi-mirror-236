#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   chain_client_config.py
# @Function     :   ChainMaker链客户端
import time
import warnings
from pathlib import Path
from typing import List, Optional, Union

import grpc
from cryptography.hazmat.primitives.asymmetric import ec, rsa

from chainmaker import exceptions
from chainmaker.apis import (AccountManagerMixIn, AccountManagerWithEndorsers, ArchiveMixIn, ArchiveWithEndorsers,
                             CanonicalTxResultMixIn, CertManageMixIn, CertManageWithEndorsers, ChainConfigMixIn,
                             ChainConfigWithEndorsers, ChainMakerServerMixIn, ChainQueryMixIn, ConsensusMixIn,
                             ContractManageWithEndorsers, ContractQueryMixIn, DPosDistributionMixIn,
                             DPosDistributionWithEndorsers, DPosErc20MixIn, DPosErc20WithEndorsers, DPosSlashingMixIn,
                             DPosSlashingWithEndorsers, DPosStakeMixIn, DPosStakeWithEndorsers, MultiSignMixin,
                             PubkeyManageMixIn, PubkeyManageWithEndorsers, SubscribeManageMixIn, SystemContractMixIn,
                             TxPoolMixIn, UserContractMixIn)
from chainmaker.apis.chain_query import ChainQueryExtras
from chainmaker.apis.private_compute import PrivateComputeMixIn
from chainmaker.archive_service import ArchiveService
from chainmaker.conn_pool import ConnectionPool
from chainmaker.exceptions import GetTxTimeoutError
from chainmaker.keys import (AddrType, AuthType, Certificate, ConsensusType, HashType, MemberType, PrivateKey,
                             PublicKey)
from chainmaker.node import Node
from chainmaker.payload import PayloadBuilder
from chainmaker.protos.api.rpc_node_pb2_grpc import RpcNodeStub
from chainmaker.protos.common.request_pb2 import EndorsementEntry, Payload, TxRequest, TxType
from chainmaker.protos.common.result_pb2 import Result, TxResponse, TxStatusCode
from chainmaker.protos.config.chain_config_pb2 import ChainConfig
from chainmaker.sdk_config import (ChainClientConfig, DEFAULT_ARCHIVE_CONFIG, DEFAULT_PKCS11_CONFIG,
                                   DEFAULT_RPC_CLIENT_CONFIG, DefaultConfig, Pkcs11Config, SdkConfig)
from chainmaker.user import User
from chainmaker.utils.common import ensure_enum
from chainmaker.utils.log_utils import get_logger

SDK_CONFIG_USER_CONFIG_FILTER = {"user_sign_key_file_path", "user_sign_crt_file_path", "user_sign_key_pwd",
                                 "user_key_file_path", "user_crt_file_path", "user_key_pwd",
                                 "user_enc_key_file_path", "user_enc_crt_file_path", "user_enc_key_pwd",
                                 "org_id", "crypto", "auth_type", "alias"}

SDK_LOGGER = get_logger(DefaultConfig.logger_name, DefaultConfig.log_level, format=DefaultConfig.log_format,
                        datefmt=DefaultConfig.log_datefmt, log_file=DefaultConfig.log_file)


class ChainClient(SystemContractMixIn, ChainQueryMixIn, UserContractMixIn, ContractQueryMixIn, ChainConfigMixIn,
                  CertManageMixIn,
                  SubscribeManageMixIn, ArchiveMixIn, PubkeyManageMixIn, AccountManagerMixIn,
                  MultiSignMixin, ChainMakerServerMixIn, TxPoolMixIn, CanonicalTxResultMixIn,
                  ConsensusMixIn, DPosErc20MixIn, DPosStakeMixIn, DPosSlashingMixIn, DPosDistributionMixIn,
                  PrivateComputeMixIn):

    def __init__(self, chain_id, user: User, nodes: List[Node], conn_node: int = None,
                 node_index: int = None):
        self._chain_id = chain_id
        self.user = user  # todo change to _user
        self.nodes = nodes  # todo change to _nodes
        self.node_cnt = len(nodes)

        if conn_node is None and node_index is not None:
            conn_node = node_index
        self._conn_node = DefaultConfig.conn_node if conn_node is None else conn_node

        self._logger = SDK_LOGGER
        self._pool = ConnectionPool(user, nodes, conn_node=self._conn_node, logger=self._logger)
        self._payload_builder = PayloadBuilder(self._chain_id)

        self._archive_config = DEFAULT_ARCHIVE_CONFIG
        self._pkcs11_config = DEFAULT_PKCS11_CONFIG
        self._rpc_client_config = DEFAULT_RPC_CLIENT_CONFIG

        self._timeout: int = DefaultConfig.rpc_send_tx_timeout

        self._with_sync_result: bool = DefaultConfig.with_sync_result

        self._retry_limit = DefaultConfig.retry_limit
        self._retry_timeout = DefaultConfig.retry_timeout
        self._retry_interval: int = DefaultConfig.retry_interval

        self._default_gas_limit = DefaultConfig.gas_limit

        self.endorsers = DefaultConfig.endorsers
        # 交易记录功能
        self._enabled_tx_records: bool = True
        self._tx_records = []  # 记录请求过的invoke交易信息,在请求失败通过交易Id追踪错误

        if DefaultConfig.enable_log is not True:
            self.disable_log()

        # 自动启用别名
        if self.user.alias and isinstance(user.alias, str) and len(user.alias) > 0:
            self.enable_alias()

        if self.user.enabled_cert_hash:
            self.enable_cert_hash()

        # v2.3.0 增加
        self.signer = user

        # v2.32 增加
        self.payer = None  # Default payer
        self.archive_center_query_first = None
        self.archive_center_config = None
        self._archive_service: Optional[ArchiveService] = None

    def __repr__(self):
        return '<ChainClient %s>' % self.node.node_addr

    @property
    def chain_id(self) -> str:
        return self._chain_id

    @chain_id.setter
    def chain_id(self, chain_id: str):
        self._chain_id = chain_id
        self._payload_builder.chain_id = self._chain_id

    @property
    def node(self) -> Node:
        """[只读]当前连接节点"""
        return self._pool.node

    @property
    def org_id(self) -> str:
        """[只读]当前用户组织ID"""
        return self.user.org_id

    @property
    def alias(self) -> str:
        """用户证书别名"""
        return self.user.alias

    @alias.setter
    def alias(self, alias: str):
        """设置当前用户证书别名"""
        if isinstance(alias, str) and len(alias) > 0:
            self.user.alias = alias

    @property
    def hash_type(self) -> HashType:
        """[只读]当前用户证书/密钥哈希类型"""
        return self.user.hash_type

    @property
    def auth_type(self) -> AuthType:
        """[只读]当前权限模式"""
        return self.user.auth_type

    # @property
    # def addr_type(self) -> AddrType:
    #     """[只读]获取链配置并更新user.addr_type"""
    #     self.user.addr_type = self.chain_config.vm.addr_type
    #     return self.user.addr_type

    @property
    def enabled_alias(self) -> bool:
        """[只读]是否已启用别名"""
        return self.user.enabled_alias

    @property
    def enabled_cert_hash(self) -> bool:
        """[只读]是否已启用证书哈希"""
        # warnings.warn('请使用cc.is_cert_hash_enabled', DeprecationWarning)
        return self.user.enabled_cert_hash

    # @property
    # def enabled_gas(self) -> bool:
    #     """[只读]是否已启用Gas"""
    #     return self.get_chain_config().account_config.enable_gas
    @property
    def addr_type(self) -> AddrType:
        """[只读]地址类型"""
        self.user.addr_type = ensure_enum(self.chain_config.vm.addr_type, AddrType)
        return self.user.addr_type

    @property
    def member_type(self) -> MemberType:
        """[只读]当前签名类型-可通过cc.change_member_type()修改"""
        return self.user.member_type

    @property
    def cert(self) -> Certificate:
        """[只读]用户签名证书"""
        return self.user.cert

    @property
    def cert_hash(self) -> str:  # 注意由原来的返回bytes修改为了返回hex字符串
        """[只读]用户证书哈希"""
        return self.user.cert_hash

    @property
    def cert_hash_bytes(self) -> bytes:
        """[只读]用户证书哈希"""
        return self.user.cert_hash_bytes

    @property
    def private_key(self) -> PrivateKey:
        """[只读]用户私钥对象"""
        return self.user.private_key

    @property
    def public_key(self) -> PublicKey:
        """[只读]用户公钥对象"""
        return self.user.public_key

    @property
    def public_bytes(self) -> bytes:
        """[只读]用户公钥二进制内容"""
        return self.user.public_bytes

    @property
    def sender_address(self) -> str:  # todo remove
        """用户账户地址"""
        warnings.warn("use cc.address instead", DeprecationWarning)
        self.user.addr_type = self.get_chain_config().vm.addr_type
        return self.user.sender_address

    @property
    def address(self) -> str:
        """用户账户地址"""
        if self.user.addr_type is None:
            self.user.addr_type = ensure_enum(self.chain_config.vm.addr_type, AddrType)
        return self.user.address

    @property
    def is_archive_center_query_first(self) -> bool:
        """
        sdk_config.yml是否设置了archive_center_query_first=true
        v2.3.2 新增
        :return: sdk_config.yml开启archive_center_query_first返回True,否则返回False
        """
        return self.archive_center_query_first is True

    def _get_client(self, conn_node: int = None) -> RpcNodeStub:
        """
        根据策略或去连接
        :param conn_node: 节点索引
        :return:
        """
        client = self._pool.get_client(conn_node)
        # self._debug(f'get rpc client for node {self.node.node_addr}')
        return client

    def _create_endorsers(self, payload: Payload, endorse_users: List[User] = None) -> List[EndorsementEntry]:
        """
        根据背书用户创建背书
        :param payload: 待签名请求负荷
        :param endorse_users: 背书用户列表
        :return: 背书列表
        """
        if endorse_users is None:
            endorse_users = self.endorsers
        payload_bytes = payload.SerializeToString()
        endorsers = [user.sign(payload_bytes) for user in endorse_users or []]
        return endorsers

    def create_endorsers(self, payload: Payload, endorsers_config: List[dict]) -> List[EndorsementEntry]:
        """
        根据背书用户创建背书
        :param payload: 待签名请求负荷
        :param endorsers_config: 用户组织、签名证书等配置列表
        :return: 背书列表
        """
        endorse_users = [User.from_conf(**item) for item in endorsers_config]
        return self._create_endorsers(payload, endorse_users)

    def _get_sync_result_with_timeout(self, tx_id: str, retry_timeout: int, retry_interval: int) -> Result:
        """
        通过交易id轮询交易结果直到可以查询到交易结果或者超时-限制轮询超时时间
        :param tx_id: 交易ID
        :param retry_timeout: 轮询超时时间
        :param retry_interval: 轮询间隔, 单位毫秒
        :return: 交易结果Result对象
        :raise: 超时未查询到交易信息则抛出 GetTxTimeoutError
        """
        self._debug('begin to get sync result [tx_id:%s]/[timeout:%s]' % (tx_id, retry_timeout))
        start = time.time()
        err_msg = ''
        while time.time() - start < retry_timeout:
            try:
                transaction_info = self._get_tx_by_tx_id(tx_id)
                return transaction_info.transaction.result
            except exceptions.RequestError as ex:
                err_msg = str(ex)
                time.sleep(retry_interval // 1000)
        raise GetTxTimeoutError(f'[Sdk] get tx_id="%s" transaction info %ss timeout: %s'
                                % (tx_id, retry_timeout, err_msg))

    def _get_sync_result_with_limit(self, tx_id: str, retry_limit: int, retry_interval: int) -> Result:
        """
        通过交易id轮询交易结果直到可以查询到交易结果或者超时-限制轮询次数
        :param tx_id: 交易ID
        :param retry_limit: 轮询次数
        :param retry_interval: 轮询间隔, 单位毫秒
        :return: 交易结果Result对象
        :raise: 超时未查询到交易信息则抛出 GetTxTimeoutError
        """
        self._debug('begin to get sync result [tx_id:%s]/[retry_times:%d]' % (tx_id, retry_limit))
        err_msg = ''
        for i in range(retry_limit):
            try:
                transaction_info = self._get_tx_by_tx_id(tx_id)
                return transaction_info.transaction.result
            except exceptions.RequestError as ex:
                err_msg = str(ex)
                time.sleep(retry_interval // 1000)
        raise GetTxTimeoutError(f'[Sdk] get tx_id="%s" transaction info timeout when retry %s times: %s'
                                % (tx_id, retry_limit, err_msg))

    def get_sync_result(self, tx_id: str, retry_limit: int = None, retry_timeout: int = None,
                        retry_interval: int = None):
        """通过交易id轮询交易结果直到可以查询到交易结果或者超时"""
        if retry_limit is None:
            retry_limit = self._retry_limit
        if retry_timeout is None:
            retry_timeout = self._retry_timeout
        if retry_interval is None:
            retry_interval = self._retry_interval
        assert retry_interval and any([retry_timeout, retry_limit]), '[Sdk] retry_timeout or retry_limit must be set'

        if self._retry_timeout is not None:
            return self._get_sync_result_with_timeout(tx_id, retry_timeout, retry_interval)

        return self._get_sync_result_with_limit(tx_id, retry_limit, retry_interval)

    def sign(self, payload_bytes: bytes) -> EndorsementEntry:
        """
        签名Payload二进制内容
        :param payload_bytes: Payload二进制内容
        :return: 背书条目
        """
        return self.user.sign(payload_bytes)

    def _generate_tx_request(self, payload, endorsers: List[EndorsementEntry] = None,
                             signer: User = None, payer: User = None) -> TxRequest:
        """
        生成交易请求
        :param payload: 待签名Payload
        :param endorsers: 背书列表
        :param signer: 签名用户 v2.3.0 增加
        :param payer: 代扣Gas用户 v2.3.2 增加
        :return: 交易请求
        """
        payload_bytes = payload.SerializeToString()
        # v2.3.0 修改
        signer = signer or self.signer
        sender = signer.sign(payload_bytes)

        tx_request = TxRequest(
            payload=payload,
            sender=sender,
            endorsers=endorsers,
        )
        # v2.3.2 增加
        payer = payer or self.payer
        if payer is not None:
            tx_request.payer = payer.sign(payload_bytes)

        return tx_request

    def _get_timeout(self, tx_type: TxType) -> int:
        """
        根据交易类型获取sdk_config.py中rpc_client配置的超时时间
        :param tx_type: 交易类型
        :return: 超时时间(秒)
        """
        if tx_type == TxType.QUERY_CONTRACT:
            timeout = self._rpc_client_config.get_tx_timeout if self._rpc_client_config is not None \
                else DefaultConfig.rpc_get_tx_timeout
        else:
            timeout = self._rpc_client_config.send_tx_timeout if self._rpc_client_config is not None \
                else DefaultConfig.rpc_send_tx_timeout
        return timeout

    def _send_request(self, payload: Payload, endorsers: List[EndorsementEntry] = None,
                      timeout: int = None, gas_limit: int = None, signer: User = None,
                      payer: User = None) -> TxResponse:
        """
        发送带超时时间的交易请求
        :param payload: 待签名请求Payload
        :param endorsers: 背书列表
        :param timeout: 超时时间
        :return: 交易响应TxResponse对象
        :raise 连接异常时抛出 InactiveRpcError
        """
        if timeout is None or timeout <= 0:
            timeout = self._get_timeout(payload.tx_type)

        if gas_limit is not None:
            self.attach_gas_limit(payload, gas_limit)

        # 处理默认背书
        if self.endorsers:
            endorsers = endorsers or self._create_endorsers(payload, endorsers)

        # 构造请求结构
        tx_request = self._generate_tx_request(payload, endorsers, signer=signer, payer=payer)

        # 仅记录Invoke交易
        if self._enabled_tx_records and tx_request.payload.tx_type == TxType.INVOKE_CONTRACT:
            self._tx_records.append(tx_request)

        return self._pool.send_rpc_request(tx_request, timeout=timeout, conn_node=self._conn_node)

    def _send_request_with_timeout(self, payload: Payload, endorsers: List[EndorsementEntry] = None,
                                   timeout: int = None, gas_limit: int = None, signer: User = None,
                                   payer: User = None) -> TxResponse:
        warnings.warn('[Sdk] please use cc._send_request instead', DeprecationWarning)
        return self._send_request(payload, endorsers, timeout, gas_limit=gas_limit, signer=signer, payer=payer)

    @staticmethod
    def _handle_errors(tx_response):
        if tx_response.code != TxStatusCode.SUCCESS:
            if tx_response.code == 5:  # InternalError
                exceptions.handle_internal_error(tx_response)
            elif tx_response.code == 4:  # ContractFail
                exceptions.handle_contract_fail(tx_response)
            err_class = exceptions.TX_RESPONSE_ERROR_MAP.get(tx_response.code)
            raise err_class(TxStatusCode.Name(tx_response.code), tx_response.message)
        return tx_response

    def send_request(self, payload: Payload, endorsers: List[EndorsementEntry] = None,
                     timeout: int = None,
                     gas_limit: int = None, signer: User = None, payer: User = None) -> TxResponse:
        """
        发送交易请求并检查是否成功
        带重连机制，基于 self._send_request_with_retry_connect
        :param payload: 待签名请求Payload
        :param endorsers: 背书列表
        :param timeout: 超时时间
        :param gas_limit: Gas交易限制
        :param signer: 指定签名用户
        :param payer: 指定Gas代扣用户
        :return: 交易响应TxResponse对象
        :raise 重连超过retry_limit限制仍无法成功时抛出 RpcConnectError
        :raise: RequestError错误子类，如InvalidParameter等
        """
        tx_response = self._send_request(payload, endorsers, timeout)
        if self.retry_on_txpool_full is True:
            # handle txpool is full error
            retry_timeout = DefaultConfig.txpool_full_retry_timeout
            retry_interval = DefaultConfig.txpool_full_retry_interval
            start = time.time()
            while (tx_response.code == 5 and 'TxPool is full' in tx_response.message) and (
                    time.time() - start < retry_timeout):
                time.sleep(retry_interval / 1000)
                tx_response = self._send_request(payload, endorsers, timeout, gas_limit=gas_limit, signer=signer,
                                                 payer=payer)
        return self._handle_errors(tx_response)

    @staticmethod
    def _update_tx_response_with_result(tx_response: TxResponse, result: Result) -> TxResponse:
        """
        更新交易响应，将轮询得到的交易结果中的信息添加到交易响应中
        :param tx_response: 原交易响应
        :param result: self.get_sync_result轮询得到到交易结果
        :return: 包含交易结果的交易响应
        """
        tx_response.code = result.code
        tx_response.message = result.message
        tx_response.contract_result.code = result.contract_result.code
        tx_response.contract_result.result = result.contract_result.result
        tx_response.contract_result.result = result.contract_result.result
        tx_response.contract_result.message = result.contract_result.message
        tx_response.contract_result.gas_used = result.contract_result.gas_used
        for contract_event in result.contract_result.contract_event:
            tx_response.contract_result.contract_event.append(contract_event)

        return tx_response

    def send_request_with_sync_result(self, payload: Payload, endorsers: List[EndorsementEntry] = None,
                                      timeout: int = None, with_sync_result: bool = None,
                                      gas_limit: int = None, signer: User = None, payer: User = None) -> TxResponse:
        """
        发送请求并支持轮询交易结果
        :param payload: 待签名请求Payload
        :param timeout: 超时时间
        :param with_sync_result: 是否同步获取交易结果，默认为False
        :param endorsers: 背书配置
        :param gas_limit: Gas交易限制
        :param signer: 指定签名用户
        :param payer: 指定Gas代扣用户
        :return: 交易响应TxResponse对象
        :raise: RequestError错误子类，如InvalidParameter等
        :raise: 在指定时间（self.check_tx_timeout）内未获取到结果抛出，GetTxTimeoutError
        """
        if with_sync_result is None:
            with_sync_result = self._with_sync_result

        tx_response = self.send_request(payload, endorsers, timeout, gas_limit=gas_limit, signer=signer, payer=payer)

        if with_sync_result is True:
            tx_response.tx_id = payload.tx_id
            result = self.get_sync_result(payload.tx_id)
            tx_response = self._update_tx_response_with_result(tx_response, result)

        return tx_response

    def stop(self):
        """停止客户端-关闭所有channel连接"""
        self._pool.close()

    def disable_log(self):
        """禁用SDK日志"""
        self._logger.disabled = True

    @staticmethod
    def _set_config(cc: "ChainClient", chain_client_config: ChainClientConfig):
        cc._retry_limit = chain_client_config.retry_limit or DefaultConfig.retry_limit
        cc._retry_timeout = chain_client_config.retry_timeout or DefaultConfig.retry_timeout
        cc._retry_interval = chain_client_config.retry_interval or DefaultConfig.retry_interval
        cc._archive_config = chain_client_config.archive or DEFAULT_ARCHIVE_CONFIG
        cc._pkcs11_config = chain_client_config.pkcs11 or DEFAULT_PKCS11_CONFIG
        cc._rpc_client_config = chain_client_config.rpc_client or DEFAULT_RPC_CLIENT_CONFIG

        # 处理背书配置
        endorsers_config = chain_client_config.endorsers
        if endorsers_config:
            cc.endorsers = [User.from_conf(**item.__dict__) for item in endorsers_config]

    @classmethod
    def from_conf(cls, sdk_config: Union[dict, str, Path], conn_node: int = None,
                  node_index: int = None) -> "ChainClient":
        """
        加载sdk_config配置文件并生成链客户端对象
        :param node_index:
        :param sdk_config: 加载后的sdk_config内容或, sdk_config.yml配置文件路径
        :param conn_node: 要连接到节点索引
        :return: ChainClient链客户端对象
        """
        chain_client = SdkConfig.from_conf(sdk_config).chain_client
        user_conf = {key: chain_client.__dict__.get(key) for key in SDK_CONFIG_USER_CONFIG_FILTER}
        user = User.from_conf(**user_conf)

        nodes = [Node.from_conf(**item.__dict__) for conn_node, item
                 in enumerate(chain_client.nodes)]

        cc = cls(chain_client.chain_id, user, nodes, conn_node=conn_node, node_index=node_index)
        cls._set_config(cc, chain_client)
        return cc

    # 即将废弃方法 -------------------------------------------------------------------------------------------------------
    @org_id.setter
    def org_id(self, org_id: str) -> None:
        warnings.warn('[Sdk] not allowed to change user.org_id directly now', DeprecationWarning)
        self.user.org_id = org_id

    @hash_type.setter
    def hash_type(self, hash_type: HashType) -> None:
        """设置用户证书/私钥哈希类型"""
        warnings.warn('[Sdk] not allowed to change user.hash_type directly now', DeprecationWarning)
        self.user.hash_type = hash_type

    @auth_type.setter
    def auth_type(self, auth_type: AuthType) -> None:
        """设置权限模式"""
        warnings.warn('[Sdk] not allowed to change user.auth_type directly now', DeprecationWarning)
        self.user.auth_type = auth_type

    @property
    def enabled_crt_hash(self) -> bool:
        warnings.warn('[Sdk] please use cc.enabled_cert_hash "crt" has changed to "cert"', DeprecationWarning)
        return self.user.enabled_cert_hash

    @enabled_crt_hash.setter
    def enabled_crt_hash(self, is_enable: bool) -> None:
        warnings.warn('[Sdk] please use cc.enable_cert_hash() or cc.disable_cert_hash() instead', DeprecationWarning)
        self.user.enabled_crt_hash = is_enable

    @property
    def user_cert_hash(self) -> bytes:
        """用户证书哈希二进制内容"""
        warnings.warn('[Sdk] please use cc.cert_hash_bytes instead', DeprecationWarning)
        return self.cert_hash_bytes

    @user_cert_hash.setter
    def user_cert_hash(self, cert_hash: bytes) -> None:
        """设置用户证书哈希二进制内容"""
        warnings.warn('[Sdk] not allowed to change user.sign_cert_hash directly', DeprecationWarning)
        self.user.cert_hash = cert_hash

    @member_type.setter
    def member_type(self, member_type: MemberType):
        """切换PermissionedWithCert模式下签名类型member_type"""
        warnings.warn('[Sdk] please use ChainManager instead to change member_type', DeprecationWarning)
        if self.auth_type != AuthType.PermissionedWithCert:
            raise ValueError('[Sdk] set member_type only allowed when auth_type=permissionedWithCert')

        if member_type not in [MemberType.CERT, MemberType.CERT_HASH, MemberType.ALIAS]:
            raise ValueError('[Sdk] member_type should be one of CERT、CERT_HASH、ALIAS')

        if member_type == MemberType.CERT:
            self.user.is_cert_hash_enabled = False
            self.user.is_alias_enabled = False
        elif member_type == MemberType.CERT_HASH:
            self.enable_cert_hash()
            self.user.is_alias_enabled = False
        else:
            self.user.is_cert_hash_enabled = False
            self.enable_alias()  # raise Errors

    def get_enabled_crt_hash(self) -> bool:  # TODO Test
        """
        是否启用了证书哈希
        :return:
        """
        warnings.warn('[Sdk] please use cc.enabled_cert_hash instead, "crt" has changed to "cert"', DeprecationWarning)
        return self.enabled_cert_hash

    def get_user_cert_hash(self) -> bytes:
        """获取用户证书哈希"""
        warnings.warn('[Sdk] please use cc.cert_hash_bytes instead', DeprecationWarning)
        return self.cert_hash_bytes

    def get_hash_type(self) -> HashType:
        """获取用户证书加密哈希类型"""
        warnings.warn('[Sdk] please use cc.hash_type instead', DeprecationWarning)
        return self.user.hash_type

    def get_auth_type(self) -> AuthType:
        """获取链授权类型"""
        warnings.warn('[Sdk] please use cc.auth_type instead', DeprecationWarning)
        return self.user.auth_type

    def get_public_key(self) -> Union[ec.EllipticCurvePublicKey, rsa.RSAPublicKey]:
        """获取当前用户公钥"""
        warnings.warn('[Sdk] please use cc.public_key instead', DeprecationWarning)
        return self.user.public_key

    def get_private_key(self) -> Union[ec.EllipticCurvePrivateKey, rsa.RSAPrivateKey]:
        """获取当前用户私钥"""
        warnings.warn('[Sdk] please use cc.private_key instead', DeprecationWarning)
        return self.user.private_key

    def get_pkcs11_config(self) -> Pkcs11Config:
        warnings.warn('[Sdk] please use cc.pkcs11_config instead', DeprecationWarning)
        return self._pkcs11_config

    def get_cert_pem(self):
        """获取证书PEM格式二进制内容-同self.user_crt_bytes"""
        warnings.warn('[Sdk] please use cc.user.sign_cert_bytes instead', DeprecationWarning)
        return self.user.sign_cert_bytes

    def get_local_cert_alias(self):
        """获取用户证书别名 同 self.alias"""
        warnings.warn('[Sdk] please use cc.alias instead', DeprecationWarning)
        return self.user.alias

    def send_manage_request(self, payload: Payload, endorse_users: List[User] = None,
                            timeout: int = None, with_sync_result: bool = True,
                            gas_limit: int = None, signer: User = None, payer: User = None) -> TxResponse:
        """
        发送带默认背书的管理请求
        :param payload: 待签名请求Payload
        :param endorse_users: 背书用户列表，默认为None并使用self.endorse_users
        :param timeout: 超时时间
        :param with_sync_result: 是否同步交易结果，默认为True
        :param gas_limit: Gas交易限制
        :param signer: 指定签名用户
        :param payer: 指定Gas代扣用户
        :return: 交易响应TxResponse
        """
        # warnings.warn('[Sdk] please use ChainManager instead for client with default endorsers', DeprecationWarning)
        self._debug('begin to send manage request with default endorsers [tx_id:%s]' % payload.tx_id)
        if endorse_users is None:
            endorse_users = self.endorsers  # 背书用户

        endorsers = self._create_endorsers(payload, endorse_users)

        response = self.send_request_with_sync_result(payload, endorsers, timeout, with_sync_result,
                                                      gas_limit=gas_limit, signer=signer, payer=payer)
        return response

    def _send_request_with_retry_connect(self, payload: Payload, endorsers: List[EndorsementEntry] = None,
                                         timeout: int = None, gas_limit: int = None, signer: User = None,
                                         payer: User = None) -> TxResponse:
        """
        发送带重连的交易请求
        基于self._send_request_with_timeout
        :param payload: 待签名请求Payload
        :param endorsers: 背书列表
        :param timeout: 超时时间
        :return: 交易响应TxResponse对象
        :raise 重连超过retry_limit限制仍无法成功时抛出 RpcConnectError
        """
        warnings.warn('[Sdk] has moved to conn_poll, use cc._send_request() instead', DeprecationWarning)
        err_msg = ''
        for i in range(DefaultConfig.rpc_retry_limit):
            try:
                return self._send_request(payload, endorsers, timeout, gas_limit=gas_limit, signer=signer, payer=payer)
            except grpc._channel._InactiveRpcError as ex:
                err_msg = exceptions.ERR_MSG_MAP.get(ex.details(), ex.details())
                time.sleep(DefaultConfig.rpc_retry_interval // 1000)  # 毫秒
        else:
            self._logger.error("[Sdk] statusErr.Code() : %s")

            raise exceptions.RpcConnectError(
                '[Sdk] Rpc service<%s enable_tls=%s> not available: %s' % (
                    self.node.node_addr, self.node.enable_tls, err_msg))

    @property
    def node_index(self) -> int:
        warnings.warn('[Sdk] please use cc._conn_node', DeprecationWarning)
        return self._conn_node

    @node_index.setter
    def node_index(self, node_index: int) -> None:
        warnings.warn('[Sdk] please use cc._conn_node', DeprecationWarning)
        self._conn_node = node_index


class ChainClientWithEndorsers(ChainClient, AccountManagerWithEndorsers, CertManageWithEndorsers,
                               ChainConfigWithEndorsers, ContractManageWithEndorsers, PubkeyManageWithEndorsers,
                               ArchiveWithEndorsers, DPosErc20WithEndorsers, DPosStakeWithEndorsers,
                               DPosSlashingWithEndorsers, DPosDistributionWithEndorsers, ChainQueryExtras):
    @property
    def chain_config(self) -> ChainConfig:
        """链配置(缓存)"""
        if not hasattr(self, '_cached_chain_config') or getattr(self, '_cached_chain_config') is None:
            setattr(self, '_cached_chain_config', self.get_chain_config())
        return getattr(self, '_cached_chain_config')

    @property
    def consensus_type(self) -> ConsensusType:
        """[只读]共识类型"""
        return ensure_enum(self.chain_config.consensus.type, ConsensusType)

    @property
    def consensus_node_cnt(self):
        """[只读]共识节点数量"""
        return len(self.chain_config.consensus.nodes)

    @property
    def version(self) -> str:
        """[只读]chainmaker版本"""
        return self.chain_config.version

    @property
    def enabled_gas(self) -> bool:
        """[只读]是否已启用Gas"""
        return self.chain_config.account_config.enable_gas

    @property
    def default_gas(self) -> int:
        """[只读]是否已启用Gas"""
        return self.chain_config.account_config.default_gas

    @property
    def gas_count(self) -> int:
        """[只读]是否已启用Gas"""
        return self.chain_config.account_config.gas_count

    @property
    def enable_sql_support(self) -> bool:
        return self.chain_config.contract.enable_sql_support
