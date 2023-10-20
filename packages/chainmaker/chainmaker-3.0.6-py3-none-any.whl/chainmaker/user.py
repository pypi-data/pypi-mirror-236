#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   user_full_name.py
# @Function     :   ChainMaker客户端User对象
import warnings
from pathlib import Path
from typing import Union, List, Dict

from cryptography.hazmat._oid import NameOID
from cryptography.hazmat.primitives import serialization

from chainmaker.keys import AuthType, HashType, MemberType, AddrType, PrivateKey, Certificate, PublicKey
from chainmaker.protos.accesscontrol.member_pb2 import Member
from chainmaker.protos.common.request_pb2 import EndorsementEntry
from chainmaker.sdk_config import DefaultConfig
from chainmaker.utils import crypto_utils, file_utils, address_utils
from chainmaker.utils.common import format_auth_type, format_hash_type, ensure_enum


class User(object):
    """客户端用户"""

    def __init__(self, org_id: str = '',
                 sign_key_bytes: bytes = None, sign_cert_bytes: bytes = None,
                 tls_key_bytes: bytes = None, tls_cert_bytes: bytes = None,
                 enc_key_bytes: bytes = None, enc_cert_bytes: bytes = None,
                 auth_type: AuthType = None, hash_type: HashType = None,
                 alias: str = None,
                 sign_key_pwd: str = None, tls_key_pwd: str = None, enc_key_pwd: str = None,
                 addr_type: AddrType = None):
        """
        客户端用户对象初始化方法
        :param sign_key_bytes: 必须, PEM格式用户签名私钥文件二进制内容
        :param sign_cert_bytes: PEM格式用户签名证书文件二进制内容
        :param sign_key_pwd: 用户签名私钥密码
        :param tls_key_bytes: PEM格式用户tls私钥文件二进制内容
        :param tls_cert_bytes: PEM格式用户tls证书文件二进制内容
        :param tls_key_pwd: 用户tls私钥密码
        :param enc_key_bytes: 国密双证书PEM格式用户tls加密私钥文件二进制内容
        :param enc_cert_bytes: 国密双证书PEM格式用户tls加密证书文件二进制内容
        :param enc_key_pwd: 国密双证书PEM格式用户tls加密私钥密码
        :param org_id: 组织ID
        :param auth_type: 授权类型，默认为AuthType.PermissionedWithCert
        :param hash_type: 哈希类型，默认为HashType.SHA256
        :param alias: 证书别名，默认为None
        """

        self.org_id = org_id
        self.sign_key_bytes = sign_key_bytes
        self.sign_cert_bytes = sign_cert_bytes
        self.tls_key_bytes = tls_key_bytes
        self.tls_cert_bytes = tls_cert_bytes
        self.enc_key_bytes = enc_key_bytes
        self.enc_cert_bytes = enc_cert_bytes
        self.alias = alias
        self.sign_key_pwd = sign_key_pwd
        self.tls_key_pwd = tls_key_pwd
        self.enc_key_pwd = enc_key_pwd

        self.auth_type = auth_type or DefaultConfig.auth_type
        self.hash_type = hash_type or DefaultConfig.hash_type
        self.addr_type = addr_type or DefaultConfig.addr_type

        self._handle_missing_sign_key()
        self.enabled_alias = None
        self.enabled_cert_hash = DefaultConfig.enable_cert_hash

    def _handle_missing_sign_key(self):
        """签名key未配置时使用用户key(同TLS)"""
        if self.sign_key_bytes is None and self.tls_key_bytes is not None:
            self.sign_key_bytes = self.tls_key_bytes
            if self.sign_cert_bytes is None and self.tls_cert_bytes is not None:
                self.sign_cert_bytes = self.tls_cert_bytes
            if self.sign_key_pwd is None and self.tls_key_pwd is not None:
                self.sign_key_pwd = self.tls_key_pwd

    def __repr__(self):
        return f'<User {self.member_id}>'

    def __eq__(self, other):
        if hasattr(other, 'sign_key_bytes'):
            return self.sign_key_bytes == other.sign_key_bytes
        return False

    @property
    def cert(self) -> Certificate:  # sign_cert
        """用户签名证书"""
        return crypto_utils.load_pem_cert(self.sign_cert_bytes) if self.sign_cert_bytes else None

    @property
    def cert_hash_bytes(self) -> bytes:
        """签名证书哈希-即sign_cert_hash"""
        return crypto_utils.get_cert_hash_bytes(self.cert)

    @property
    def cert_hash(self) -> str:  # 注意 由原来的返回bytes更改为返回hex字符串
        """签名证书哈希-即sign_cert_hash"""
        return self.cert_hash_bytes.hex()

    @property
    def private_key(self) -> PrivateKey:  # sign_key
        """用户签名私钥对象, 即sign_key"""
        return crypto_utils.load_pem_private_key(self.sign_key_bytes, password=self.sign_key_pwd)

    @property
    def public_key(self) -> PublicKey:
        """用户签名公钥对象"""
        return self.private_key.public_key()

    @property
    def public_bytes(self):
        """用户公钥二进制内容"""
        return self.public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo)

    @property
    def tls_key(self) -> PrivateKey:
        """用户tls私钥"""
        return crypto_utils.load_pem_private_key(self.tls_key_bytes, password=self.tls_key_pwd)

    @property
    def tls_cert(self) -> Certificate:
        """用户tls证书"""
        return crypto_utils.load_pem_cert(self.tls_cert_bytes) if self.tls_cert_bytes else None

    @property
    def enc_key(self) -> PrivateKey:
        """用户enc私钥对象"""
        return crypto_utils.load_pem_private_key(self.enc_key_bytes, password=self.enc_key_pwd)

    @property
    def enc_cert(self) -> Certificate:
        """用户enc证书对象"""
        return crypto_utils.load_pem_cert(self.enc_cert_bytes) if self.enc_cert_bytes else None

    @property
    def uid(self) -> str:
        """
        用户Id, 即ski(subject key identifier)
        :return: hex字符串
        """
        if self.cert:
            return address_utils._get_ski_from_cert(self.cert)
        return address_utils.get_ski_from_public_key(self.public_key)

    @property
    def address(self):
        """用户账户地址"""
        assert self.addr_type is not None, '[SDK] missing set user.addr_type'
        return self.get_address()

    @property
    def sender_address(self):
        """用户账户地址"""
        assert self.addr_type is not None, '[SDK] missing set user.addr_type'
        return self.get_address()

    @property
    def member_id(self) -> str:
        """从用户(签名)证书中获取用户通用名称"""
        if self.cert:
            subject = self.cert.subject
            return subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
        return self.public_bytes.decode()

    @property
    def role(self) -> str:
        """从用户(签名)证书中获取用户角色"""
        if self.cert:
            subject = self.cert.subject
            return subject.get_attributes_for_oid(NameOID.ORGANIZATIONAL_UNIT_NAME)[0].value.upper()

    @property
    def member_info(self) -> bytes:  # todo 实现
        if self.member_type == MemberType.ALIAS:  # 证书别名模式
            return self.alias.encode()
        if self.member_type == MemberType.CERT_HASH:  # 证书哈希(短证书)模式
            return self.cert_hash_bytes
        if self.member_type == MemberType.CERT:  # 证书模式
            return self.sign_cert_bytes
        else:  # 公钥模式
            return self.public_bytes

    @property
    def member_type(self) -> MemberType:
        if self.auth_type == AuthType.PermissionedWithCert:
            if self.enabled_alias is True and isinstance(self.alias, str) and len(self.alias) > 0:
                return MemberType.ALIAS
            if self.enabled_cert_hash is True and len(self.cert_hash_bytes) > 0:
                return MemberType.CERT_HASH
            return MemberType.CERT
        else:
            return MemberType.PUBLIC_KEY

    @property
    def signer(self) -> Member:
        """签名者"""
        signer = Member(org_id=self.org_id, member_info=self.member_info, member_type=self.member_type.value)
        return signer

    def sign(self, payload_bytes: bytes, enabled_crt_hash: bool = False) -> EndorsementEntry:
        """
        签名并生成背书条目
        :param payload_bytes: payload.SerializeToString() 序列化后的payload bytes数据
        :param enabled_crt_hash: 是否只用证书的hash值  # todo
        :return: 背书条目
        """
        sign_bytes = crypto_utils.sign(self.private_key, self.cert, payload_bytes, hash_type=self.hash_type)
        sender = EndorsementEntry(signer=self.signer, signature=sign_bytes)
        return sender

    def update_sign_key_and_cert(self, sign_key_bytes_or_file_path: Union[Path, str, bytes],
                                 sign_cert_bytes_or_file_path: Union[Path, str, bytes] = None,
                                 sign_key_pwd: str = None):
        """更新用户签名密钥及证书
        :param sign_key_bytes_or_file_path: 签名私钥二进制内容或证书文件路径
        :param sign_cert_bytes_or_file_path: 签名证书二进制内容或证书文件路径
        :param sign_key_pwd: 签名私钥密码
        :return:
        """
        if isinstance(sign_key_bytes_or_file_path, (Path, str)):
            self.sign_key_bytes = file_utils.read_file_bytes(sign_key_bytes_or_file_path)
        else:
            self.sign_key_bytes = sign_key_bytes_or_file_path

        if isinstance(sign_cert_bytes_or_file_path, (Path, str)):
            self.sign_cert_bytes = file_utils.read_file_bytes(sign_cert_bytes_or_file_path)
        else:
            self.sign_cert_bytes = sign_cert_bytes_or_file_path
        self.sign_key_pwd = sign_key_pwd

    def update_tls_key_and_cert(self, tls_key_bytes_or_file_path: Union[Path, str, bytes],
                                tls_cert_bytes_or_file_path: Union[Path, str, bytes] = None,
                                tls_key_pwd: str = None):
        """更新用户tls密钥及证书
        :param tls_key_bytes_or_file_path: tls私钥二进制内容或证书文件路径
        :param tls_cert_bytes_or_file_path: tls证书二进制内容或证书文件路径
        :param tls_key_pwd: tls私钥密码
        :return:
        """
        if isinstance(tls_key_bytes_or_file_path, (Path, str)):
            self.tls_key_bytes = file_utils.read_file_bytes(tls_key_bytes_or_file_path)
        else:
            self.tls_key_bytes = tls_key_bytes_or_file_path

        if isinstance(tls_cert_bytes_or_file_path, (Path, str)):
            self.tls_cert_bytes = file_utils.read_file_bytes(tls_cert_bytes_or_file_path)
        else:
            self.tls_cert_bytes = tls_cert_bytes_or_file_path
        self.tls_key_pwd = tls_key_pwd

    def update_enc_key_and_cert(self, enc_key_bytes_or_file_path: Union[Path, str, bytes],
                                enc_cert_bytes_or_file_path: Union[Path, str, bytes] = None,
                                enc_key_pwd: str = None):
        """更新用户enc密钥及证书
        :param enc_key_bytes_or_file_path: enc私钥二进制内容或证书文件路径
        :param enc_cert_bytes_or_file_path: enc证书二进制内容或证书文件路径
        :param enc_key_pwd: enc私钥密码
        :return:
        """
        if isinstance(enc_key_bytes_or_file_path, (Path, str)):
            self.enc_key_bytes = file_utils.read_file_bytes(enc_key_bytes_or_file_path)
        else:
            self.enc_key_bytes = enc_key_bytes_or_file_path

        if isinstance(enc_cert_bytes_or_file_path, (Path, str)):
            self.enc_cert_bytes = file_utils.read_file_bytes(enc_cert_bytes_or_file_path)
        else:
            self.enc_cert_bytes = enc_cert_bytes_or_file_path
        self.enc_key_pwd = enc_key_pwd

    def get_address(self, addr_type: Union[AddrType, str, int] = None) -> str:
        """
        返回账户地址
        :param addr_type: 地址类型 0-长安链 1-至信链 2-以太坊
        :return: 40位长安链地址 或 42位至信链地址(ZX开头) 或 42位以太坊地址(0x开头)
        """
        addr_type = self.addr_type if addr_type is None else ensure_enum(addr_type, AddrType)
        return address_utils.public_key_to_addr(self.public_key, self.hash_type, addr_type)

        # if addr_type == AddrType.ETHEREUM.value:
        #     return address_utils.get_evm_address_from_public_key(self.public_key, self.hash_type)
        # if addr_type == AddrType.ZXL.value:
        #     return address_utils.get_zxl_address_from_public_key(self.public_key, hash_type=HashType.SM3)
        # return address_utils.get_chainmaker_address_from_public_key(self.public_key, self.hash_type)

    @classmethod
    def from_conf(cls, org_id: str = None, user_sign_key_file_path: str = None, user_sign_crt_file_path: str = None,
                  user_key_file_path: str = None, user_crt_file_path: str = None,
                  user_enc_key_file_path: str = None, user_enc_crt_file_path: str = None,
                  crypto: dict = None, auth_type: str = None, alias: str = None,
                  user_sign_key_pwd: str = None, user_key_pwd: str = None,
                  user_enc_key_pwd: str = None) -> "ClientUser":

        auth_type = format_auth_type(auth_type)

        # 处理hash_type
        hash_type = DefaultConfig.hash_type
        if isinstance(crypto, dict):
            hash_type = format_hash_type(crypto.get('hash'))

        if isinstance(alias, str):  # 证书别名
            alias = alias

        sign_key_bytes = file_utils.read_file_bytes(user_sign_key_file_path)
        sign_cert_bytes = file_utils.read_file_bytes(user_sign_crt_file_path)
        tls_key_bytes = file_utils.read_file_bytes(user_key_file_path)
        tls_crt_bytes = file_utils.read_file_bytes(user_crt_file_path)
        enc_key_bytes = file_utils.read_file_bytes(user_enc_key_file_path)
        enc_cert_bytes = file_utils.read_file_bytes(user_enc_crt_file_path)

        user = cls(sign_key_bytes=sign_key_bytes, sign_cert_bytes=sign_cert_bytes,
                   tls_key_bytes=tls_key_bytes, tls_cert_bytes=tls_crt_bytes,
                   enc_key_bytes=enc_key_bytes, enc_cert_bytes=enc_cert_bytes,
                   org_id=org_id, auth_type=auth_type, hash_type=hash_type, alias=alias,
                   sign_key_pwd=user_sign_key_pwd, tls_key_pwd=user_key_pwd, enc_key_pwd=user_enc_key_pwd)

        return user

    @classmethod
    def load_users(cls, users_conf_file: str) -> Union[List["User"], Dict[str, "User"]]:
        """
        从用户配置文件中加载用户对象列表
        :param users_conf_file: 用户配置文件
        eg: user_full_name.yml内容
        admin1:
          org_id: "wx-org1.chainmaker.org"
          user_key_file_path: "crypto-config/wx-org1.chainmaker.org/user_full_name/admin1/admin1.tls.key"
          user_crt_file_path: "crypto-config/wx-org1.chainmaker.org/user_full_name/admin1/admin1.tls.crt"
          user_sign_key_file_path: "crypto-config/wx-org1.chainmaker.org/user_full_name/admin1/admin1._sign.key"
          user_sign_crt_file_path: "crypto-config/wx-org1.chainmaker.org/user_full_name/admin1/admin1._sign.crt"
        ...
        或
        - org_id: "wx-org1.chainmaker.org"
          user_key_file_path: "crypto-config/wx-org1.chainmaker.org/user_full_name/admin1/admin1.tls.key"
          user_crt_file_path: "crypto-config/wx-org1.chainmaker.org/user_full_name/admin1/admin1.tls.crt"
          user_sign_key_file_path: "crypto-config/wx-org1.chainmaker.org/user_full_name/admin1/admin1._sign.key"
          user_sign_crt_file_path: "crypto-config/wx-org1.chainmaker.org/user_full_name/admin1/admin1._sign.crt"
        ...
        :return: 用户对象字典或用户对象列表
        """
        data = file_utils.load_yaml(users_conf_file)
        if isinstance(data, dict):
            return {key: User.from_conf(**data[key]) for key in data}
        return [User.from_conf(**item) for item in data]

    # 即将废弃方法 --------------------------------------------------------
    @property
    def certificate(self) -> Certificate:
        """用户签名证书"""
        warnings.warn('[SDK] please use user.cert or user.sign_cert instead', DeprecationWarning)
        return self.cert

    def get_cert_hash(self, hash_type: HashType = None) -> bytes:
        """
        根据哈希类型，设置当前证书哈希
        :param hash_type:
        :return:
        """
        warnings.warn('[SDK] please use crypto_utils.get_cert_hash_bytes() instead', DeprecationWarning)
        # cert_hash_bytes = crypto_utils.get_cert_hash_bytes(self.sign_cert)
        # self.sign_cert_hash = cert_hash_bytes.hex()
        return self.cert_hash_bytes

    @cert_hash.setter
    def cert_hash(self, cert_hash: bytes) -> None:
        """获取证书哈希"""
        warnings.warn('[SDK] not allow to set user.cert_hash directly now', DeprecationWarning)
        # self.sign_cert_hash = cert_hash

    def endorse(self, payload_bytes: bytes, enabled_crt_hash: bool = False) -> EndorsementEntry:
        """
        签名并生成背书条目
        :param payload_bytes: payload.SerializeToString() 序列化后的payload bytes数据
        :param enabled_crt_hash: 是否只用证书的hash值
        :return: 背书条目
        """
        warnings.warn('[SDK] please use user._sign() instead', DeprecationWarning)
        return self.sign(payload_bytes)


ClientUser = Signer = User
