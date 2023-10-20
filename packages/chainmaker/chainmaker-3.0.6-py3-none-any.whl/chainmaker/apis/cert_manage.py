#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   cert_manage_api.py
# @Function     :   ChainMaker证书管理接口
import time
from pathlib import Path
from typing import List
from typing import Union

from chainmaker.apis.base_client import BaseClient
from chainmaker.exceptions import OnChainFailedError, RequestError
from chainmaker.keys import ParamKey, SystemContractName, CertManageMethod
from chainmaker.protos.common.request_pb2 import EndorsementEntry, Payload
from chainmaker.protos.common.result_pb2 import AliasInfos, CertInfos, Result, TxResponse

from chainmaker.sdk_config import DefaultConfig
from chainmaker.utils import crypto_utils


class _CertAliasManage(BaseClient):
    """证书别名操作"""

    def enable_alias(self, alias: str = None):
        """
        启用证书别名
        :return:
        """
        self.alias = alias or self.alias
        if self.alias is None:
            self._error('[Sdk] missing set alias')
            return
        if self.user.enabled_alias is True:
            self._debug('alias: %s is already enabled' % self.alias)
            return
        if self.check_alias() is True:
            self._debug('alias: %s is already on chain' % self.alias)
            self.user.enabled_alias = True
            return

        self.add_alias()
        if self.check_alias():
            self._debug('alias: %s on chain success' % self.alias)
            self.user.enabled_alias = True

    def disable_alias(self):
        self.user.enabled_alias = False

    def check_alias(self, alias: str = None):  # 对应sdk-go getCheckAlias   # ✅
        """
        检查证书别名是否上链
        :return:
        """
        alias = alias or self.alias
        res = self.query_cert_alias([alias])
        if res is None:
            return False

        if len(res.alias_infos) != 1:
            self._debug(f'not found alias: %s on chain' % alias)
            return False

        alias_on_chain = res.alias_infos[0].alias
        if alias_on_chain != alias:
            self._debug(f'alias_on_chain: %s != self.alias: %s' % (alias_on_chain, alias))
            return False

        if not res.alias_infos[0].now_cert.cert:  # 删除后为 b''
            self._debug('alias: %s has been deleted' % alias)
            return False

        return True

    # 02-06 添加证书别名
    def add_alias(self, alias: str = None) -> Result:  # MemberType must be MemberType_CERT
        """
        添加证书别名
        <02-06-CERT_MANAGE-CERT_ALIAS_ADD>
        :return: 响应信息
        """
        alias = alias or self.alias
        self._debug('begin to add alias')
        params = {ParamKey.alias.name: alias}
        payload = self._create_cert_manage_payload(CertManageMethod.CERT_ALIAS_ADD.name, params)
        result = self.send_request_with_sync_result(payload, with_sync_result=True)

        # assert 0 == result.contract_result.code
        # assert self.alias.encode()  == result.contract_result.result
        return result

    # 02-07 创建通过别名更新证书待签名Payload
    def create_update_cert_by_alias_payload(self, alias: str, new_cert_pem: str) -> Payload:  # ✅
        """
        创建通过别名更新证书待签名Payload
        <02-07-CERT_MANAGE-CERT_ALIAS_UPDATE>
        :param alias: 用户别名
        :param new_cert_pem: 新证书文件内容
        :return: 签名Payload
        """
        self._debug('create [CERT_MANAGE-CERT_ALIAS_UPDATE] to be signed payload')
        params = {ParamKey.alias.name: alias,
                  ParamKey.cert.name: new_cert_pem}
        return self._create_cert_manage_payload(CertManageMethod.CERT_ALIAS_UPDATE.name, params)

    # 02-08 创建删除证书别名待签名Payload
    def create_delete_cert_alias_payload(self, aliases: List[str]) -> Payload:
        """
        创建删除证书别名待签名Payload
        <02-08-CERT_MANAGE-CERTS_ALIAS_DELETE>
        :param aliases: 证书别名列表
        :return: 待签名Payload
        """
        self._debug('create [CERT_MANAGE-CERTS_ALIAS_DELETE] to be signed payload')
        params = {ParamKey.aliases.name: ','.join(aliases)}
        return self._create_cert_manage_payload(CertManageMethod.CERTS_ALIAS_DELETE.name, params)

    # 02-09 查询证书别名
    def query_cert_alias(self, aliases: List[str] = None) -> AliasInfos:
        """
        查询证书别名
        <02-09-CERT_MANAGE-CERTS_ALIAS_QUERY>
        :param aliases: 证书别名列表
        :return: 仅当所有别名存在时返回别名信息列表，否则返回None，建议单个别名查询
        """
        self._debug('begin to query cert by aliases')

        params = {ParamKey.aliases.name: ','.join(aliases)} if isinstance(aliases, list) else {}
        payload = self._payload_builder.create_query_payload(SystemContractName.CERT_MANAGE.name,
                                                             CertManageMethod.CERTS_ALIAS_QUERY.name,
                                                             params)
        try:
            response = self.send_request_with_sync_result(payload, with_sync_result=False)
        except RequestError as ex:
            self._exception(ex)
            return None
        # assert 0 == response.code, response.result
        alias_infos = AliasInfos()
        alias_infos.ParseFromString(response.contract_result.result)
        return alias_infos

    def sign_delete_alias_payload(self, payload_bytes: bytes) -> EndorsementEntry:
        self._debug('sign [CERT_MANAGE-CERTS_ALIAS_DELETE] payload bytes')
        return self.user.sign(payload_bytes)

    def sign_update_cert_by_alias_payload(self, payload_bytes: bytes) -> EndorsementEntry:
        self._debug('sign [CERT_MANAGE-CERTS_ALIAS_UPDATE] payload bytes')
        return self.user.sign(payload_bytes)

    # def update_cert_by_alias(self, payload: Payload, endorsers: List[EndorsementEntry] = None, timeout: int = None):
    #     self._debug('send [UpdateCertByAlias] payload')
    #     return self.send_cert_manage_request(payload, endorsers, timeout)


class _CertHashManage(BaseClient):
    """证书哈希(短证书)操作"""

    def enable_cert_hash(self):
        """启用证书hash，会修改实例的enabled_crt_hash值。默认为不启用。
        :raises OnChainFailedError: 证书上链失败
        :raises EndorsementInvalidError: 证书已删除
        """
        self._debug("begin to enable cert hash")
        if self.enabled_cert_hash:
            return True

        # 查询是否已经上链
        on_chain = self._check_cert_hash_on_chain(self.cert_hash)

        if on_chain:
            self.user.enabled_cert_hash = True
        else:
            self.add_cert()
            on_chain = self._retry_check_cert_hash_on_chain(self.cert_hash)
            if on_chain:
                self.user.enabled_cert_hash = True
        return on_chain

    def disable_cert_hash(self):
        """
        关闭证书哈希(短证书)
        """
        self._debug("begin to disable cert hash")
        self.user.enabled_cert_hash = False

    def get_cert_hash_bytes(self) -> bytes:
        """
        返回用户的签名证书哈希
        :return: 证书hash-bytes值
        """
        self._debug("begin to get cert hash bytes")
        return self.cert_hash_bytes

    def get_cert_hash(self, cert_bytes_or_file_path: Union[Path, str, bytes] = None) -> str:
        """
        返回用户的签名证书哈希
        :return: 证书hash-hex值
        """
        self._debug("begin to get cert hash")
        if cert_bytes_or_file_path is None:
            return self.cert_hash
        cert = crypto_utils.load_pem_cert(cert_bytes_or_file_path)
        return crypto_utils.get_cert_hash_bytes(cert).hex()

    def _check_cert_hash_on_chain(self, cert_hash) -> bool:
        """
        检查指定证书哈希是否上链
        :param cert_hash: 证书哈希
        :return: 已上链返回True，否则返回False
        :raise: 查询不到证书抛出 RequestError
        """
        res = self.query_cert([cert_hash])
        cert_info = res.cert_infos[0]

        return True if cert_info.cert else False

    def _retry_check_cert_hash_on_chain(self, cert_hash: str, check_timeout: int = None) -> bool:
        """
        重试检查指定证书哈希是否上链
        :param cert_hash: 证书哈希
        :param check_timeout: 检查超时时间
        :return: 已上链返回True，否则返回False
        :raise: 超时查询不到证书抛出 OnChainFailedError
        """
        if check_timeout is None:
            check_timeout = DefaultConfig.check_cert_timeout
        start = time.time()
        err_msg = ''
        while time.time() - start < check_timeout:
            self._debug('check cert_hash="%s"' % cert_hash)
            try:
                return self._check_cert_hash_on_chain(cert_hash)
            except RequestError as ex:
                err_msg = str(ex)
                time.sleep(self._tx_check_interval)
        raise OnChainFailedError(
            f'[Sdk] check cert_hash="%s" %ss timeout: %s' % (cert_hash, self._tx_check_timeout, err_msg))


class CertManageMixIn(_CertAliasManage, _CertHashManage):
    """证书管理操作"""

    # 02-00 添加证书
    def add_cert(self, cert_hashes: List[str] = None, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        添加证书
        <02-00-CERT_MANAGE-CERT_ADD>
        :param cert_hashes: 证书哈希列表，为None时添加当前用户证书
        :param timeout: 设置请求超时时间
        :param with_sync_result: 同步返回请求结果
        :return: Response
        :raises RequestError: 请求失败
        """
        if cert_hashes is None:
            cert_hashes = [self.user.cert_hash]

        self._debug("begin to add cert")
        params = {
            ParamKey.cert_hashes.name: ",".join(cert_hashes)
        }
        payload = self._create_cert_manage_payload(CertManageMethod.CERT_ADD.name, params)
        response = self.send_cert_manage_request(payload, endorsers=None, timeout=timeout,
                                                 with_sync_result=with_sync_result)
        return response

    # 02-01 创建证书管理证书删除待签名Payload
    def create_cert_delete_payload(self, cert_hashes: Union[list, str] = None) -> TxResponse:
        """
        创建证书管理证书删除待签名Payload
         <02-01-CERT_MANAGE-CERTS_DELETE>
        :param cert_hashes: 证书hash列表, 每个证书hash应转为hex字符串, 为None时使用当前用户证书哈希
        :return: Payload
        """
        if cert_hashes is None:
            cert_hashes = [self.user.cert_hash]
        if isinstance(cert_hashes, str):
            cert_hashes = [cert_hashes]
        self._debug("begin to create [CERT_MANAGE-CERTS_DELETE] to be signed payload")

        params = {ParamKey.cert_hashes.name: ",".join(cert_hashes)}

        return self._create_cert_manage_payload(CertManageMethod.CERTS_DELETE.name, params)

    # 02-02 根据证书哈希查询证书
    def query_cert(self, cert_hashes: Union[list, str] = None, timeout: int = None) -> CertInfos:
        """
        根据证书哈希查询证书
        <02-02-CERT_MANAGE-CERTS_QUERY>
        :param cert_hashes: 证书hash列表(List)，每个证书hash应转为hex字符串, 为None时查询当前用户证书
        :param timeout: 请求超时时间
        :return: result_pb2.CertInfos
        :raises 查询不到证书抛出 RequestError
        """
        if cert_hashes is None:
            cert_hashes = [self.user.cert_hash]
        if isinstance(cert_hashes, str):
            cert_hashes = [cert_hashes]
        self._debug("begin to query cert [cert_hashes:%s]", cert_hashes)

        params = {
            ParamKey.cert_hashes.name: ",".join(cert_hashes)
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.CERT_MANAGE.name,
                                                             CertManageMethod.CERTS_QUERY.name,
                                                             params)
        try:
            response = self.send_request(payload, timeout=timeout)
        except RequestError:
            return None
        cert_infos = CertInfos()
        cert_infos.ParseFromString(response.contract_result.result)
        return cert_infos

    # 02-03 创建证书管理证书冻结待签名Payload
    def create_cert_freeze_payload(self, certs: List[str]) -> Payload:
        """
        创建证书管理证书冻结待签名Payload
        <02-03-CERT_MANAGE-CERTS_FREEZE>
        :param certs: 证书列表(List)，证书为证书文件读取后的字符串格式
        :return: Payload
        """
        self._debug("begin to create [CERT_MANAGE-CERTS_FREEZE] to be signed payload")
        params = {
            ParamKey.certs.name: ','.join(certs)
        }
        return self._create_cert_manage_payload(CertManageMethod.CERTS_FREEZE.name, params)

    # 02-04 创建证书管理证书解冻待签名Payload
    def create_cert_unfreeze_payload(self, certs: List[str]) -> Payload:
        """
        创建证书管理证书解冻待签名Payload
        <02-04-CERT_MANAGE-CERTS_UNFREEZE>
        :param certs: 证书列表，证书为证书文件读取后的字符串格式
        :return: Payload
        """
        self._debug("begin to create [CERT_MANAGE-CERTS_UNFREEZE] to be signed payload")
        params = {
            ParamKey.certs.name: ','.join(certs)
        }
        return self._create_cert_manage_payload(CertManageMethod.CERTS_UNFREEZE.name, params)

    # 02-05 创建证书管理证书吊销待签名Payload
    def create_cert_revoke_payload(self, cert_crl: str) -> Payload:
        """
        创建证书管理证书吊销待签名Payload
        <02-05-CERT_MANAGE-CERTS_REVOKE>
        :param cert_crl: 证书吊销列表 文件内容，字符串形式
        :return: Payload
        """
        self._debug("begin to create [CERT_MANAGE-CERTS_REVOKE] to be signed payload")

        params = {
            ParamKey.cert_crl.name: cert_crl
        }
        return self._create_cert_manage_payload(CertManageMethod.CERTS_REVOKE.name, params)

    def _create_cert_manage_payload(self, method: str, params: Union[dict, list] = None):
        """创建证书管理payload
        :param method: 方法名。CERTS_FROZEN(证书冻结)/CERTS_UNFROZEN(证书解冻)/CERTS_REVOCATION(证书吊销)
        :param params: 证书管理操作参数，dict格式
        :return: 证书管理payload
        :raises
        """
        return self._payload_builder.create_invoke_payload(SystemContractName.CERT_MANAGE.name, method, params)

    @staticmethod
    def create_cert_crl(cert_bytes_or_file_path: Union[Path, str, bytes],
                        ca_key_bytes_or_file_path: Union[Path, str, bytes],
                        ca_crt_bytes_or_file_path: Union[Path, str, bytes]) -> str:
        """ 创建吊销证书列表文件二进制数据
        :param cert_bytes_or_file_path: 原客户端证书文件
               eg ./crypto-config/wx-org2.chainmaker.org/user_full_name/client1/client1.tls.crt'
        :param ca_key_bytes_or_file_path: 同组织根证书私钥文件
               eg. ./crypto-config/wx-org2.chainmaker.org/ca/ca.key
        :param ca_crt_bytes_or_file_path: 同组织跟证书文件
               eg. ./crypto-config/wx-org2.chainmaker.org/ca/ca.crt
        :return: 生成的crl文件二进制内容
        """
        return crypto_utils.create_crl_bytes(cert_bytes_or_file_path, ca_key_bytes_or_file_path,
                                             ca_crt_bytes_or_file_path).decode()

    def sign_cert_manage_payload(self, payload_bytes: bytes) -> EndorsementEntry:
        """
        对证书管理的payload进行签名
        :param: 待签名payload
        :return: 背书条目
        """
        return self.user.sign(payload_bytes)

    def send_cert_manage_request(self, payload: Payload, endorsers: List[EndorsementEntry] = None,
                                 timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        发送证书管理请求
        :param payload: 交易payload
        :param endorsers: 背书列表
        :param timeout: 超时时间
        :param with_sync_result: 是否同步交易执行结果。如果不同步，返回tx_id，供异步查询; 同步则循环等待，返回交易的执行结果。
        :return: Response
        :raises RequestError: 请求失败
        """
        return self.send_request_with_sync_result(payload, endorsers=endorsers, timeout=timeout,
                                                  with_sync_result=with_sync_result)

    # def delete_cert(self, payload: Payload, endorsers: List[EndorsementEntry], timeout: int = None) -> TxResponse:
    #     """删除用户的证书
    #     :param payload: 待签名Payload
    #     :param endorsers 背书列表
    #     :param timeout: 超时时长
    #     :param with_sync_result: 是否同步返回请求结果
    #     :return: Response
    #     :raises RequestError: 请求失败
    #     """
    #     warnings.warn('please use cc.send_cert_manage_request', DeprecationWarning)
    #     self._debug("begin to DeleteCert")
    #     return self.send_cert_manage_request(payload, endorsers, timeout=timeout)


class CertManageWithEndorsers(BaseClient):
    # todo add cert
    # 02-01 删除证书

    def delete_certs(self, cert_hashes: List[str] = None,
                     timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        删除证书
        <02-01-CERT_MANAGE-CERTS_DELETE>
        :param cert_hashes: 证书hash列表, 每个证书hash应转为hex字符串
        :param timeout: 超时时长
        :param with_sync_result: 是否同步返回请求结果
        :return: Response
        :raises RequestError: 请求失败
        """
        payload = self.create_cert_delete_payload(cert_hashes)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 02-02 根据证书哈希查询证书
    def query_certs(self, cert_hashes: Union[list, str] = None, timeout: int = None) -> CertInfos:
        """
        查询证书的hash是否已经上链
        <02-02-CERT_MANAGE-CERTS_QUERY>
        :param cert_hashes: 证书hash列表(List)，每个证书hash应转为hex字符串, 为None时查询当前用户证书
        :param timeout: 请求超时时间
        :return: CertInfos
        :raises 查询不到证书抛出 RequestError
        """
        return self.query_cert(cert_hashes, timeout)

    # 02-03 冻结证书
    def freeze_certs(self, certs: List[str], timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        冻结证书
        <02-03-CERT_MANAGE-CERTS_FREEZE>
        :param certs: 证书内容列表
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        payload = self.create_cert_freeze_payload(certs)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 02-04 解冻证书
    def unfreeze_certs(self, certs: List[str], timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        解冻证书
        <02-04-CERT_MANAGE-CERTS_UNFREEZE>
        :param certs: 证书内容
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        payload = self.create_cert_unfreeze_payload(certs)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 02-05 吊销证书
    def revoke_cert(self, cert_bytes_or_file_path: Union[Path, str, bytes] = None,
                    ca_key_bytes_or_file_path: Union[Path, str, bytes] = None,
                    ca_cert_bytes_or_file_path: Union[Path, str, bytes] = None,
                    cert_crl: bytes = None,
                    timeout: int = None, with_sync_result: bool = None) -> TxResponse:  # todo 多个证书
        """
        吊销证书
         <02-05-CERT_MANAGE-CERTS_REVOKE>
        :param cert_crl:
        :param cert_bytes_or_file_path: 证书文件路径
        :param ca_key_bytes_or_file_path: 所属组织ca证书文件路径
        :param ca_cert_bytes_or_file_path: 所属组织ca私钥文件路径
        :param timeout: RCP请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """

        cert_crl = cert_crl or crypto_utils.create_crl_bytes(cert_bytes_or_file_path, ca_key_bytes_or_file_path,
                                                             ca_cert_bytes_or_file_path)

        payload = self.create_cert_revoke_payload(cert_crl.decode())
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 02-06 添加证书别名
    def add_cert_alias(self, alias: str = None) -> Result:  # MemberType must be MemberType_CERT
        """
        添加证书别名
        <02-06-CERT_MANAGE-CERT_ALIAS_ADD>
        :return: 响应信息
        """
        return self.add_alias(alias)

    # 02-07 通过别名更新证书
    def update_cert_by_alias(self, alias: str, new_cert_pem: str,
                             timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        通过别名更新证书
        <02-07-CERT_MANAGE-CERTS_ALIAS_UPDATE>
        :param alias: 用户别名
        :param new_cert_pem: 新证书文件内容
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        payload = self.create_update_cert_by_alias_payload(alias, new_cert_pem)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 02-08 删除证书别名
    def delete_cert_aliases(self, aliases: List[str], timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        删除证书别名
        :param aliases: 别名列表
        <02-07-CERT_MANAGE-CERTS_ALIAS_DELETE>
        :param timeout: RPC请求超时实际
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        :raises: RequestError: 请求出错
        """
        payload = self.create_delete_cert_alias_payload(aliases)
        return self.send_manage_request(payload, timeout=timeout, with_sync_result=with_sync_result)
