#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   address_utils.py
# @Function     :   从证书文件、私钥对象、公钥对象获取长安链、至信链、以太坊地址
import hashlib
import warnings
from typing import Union

import asn1
import sha3
from cryptography import x509  # pip install cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.x509 import Certificate
from pyasn1.codec.der import decoder
from pyasn1_modules import rfc3280

from chainmaker.keys import HashType, AddrType, PublicKey
from chainmaker.utils.common import ensure_enum
from chainmaker.utils.gm import sm3


def keccak_256(data: bytes) -> str:
    k = sha3.keccak_256()
    k.update(data)
    return k.hexdigest()


def ans1_dump(*args: int) -> bytes:
    warnings.warn('todo remove by using pyasn1', DeprecationWarning)
    enc = asn1.Encoder()
    enc.start()
    enc.enter(asn1.Numbers.Sequence)
    for number in args:
        enc.write(number)
    enc.leave()
    res = enc.output()
    return res


def _calc_address_from_ski(ski: str) -> str:
    """
    通过ski计算地址
    :param ski: 16进制SubjectKeyIdentifier值
    :return: 40位地址
    """
    return keccak_256(bytes.fromhex(ski))[24:]


def _get_pk_der_bytes_from_public_key(public_key: PublicKey) -> bytes:
    return public_key.public_bytes(serialization.Encoding.DER,
                                   serialization.PublicFormat.SubjectPublicKeyInfo)  # encodedPub


def _get_ski_from_pk_der_bytes(pk_der_bytes: bytes, hash_type: HashType) -> str:
    sub_pki, _ = decoder.decode(pk_der_bytes, asn1Spec=rfc3280.SubjectPublicKeyInfo())
    sub_pki_bytes = sub_pki.components[1].asOctets()

    if hash_type == HashType.SHA256:
        return hashlib.sha256(sub_pki_bytes).hexdigest()
    if hash_type == HashType.SHA3_256:
        return sha3.sha3_256(sub_pki_bytes).hexdigest()
    if hash_type == HashType.SM3:
        return sm3.sm3_hash(sub_pki_bytes)
    raise NotImplementedError('哈希类型暂时仅支持SHA256, SHA3_256, SM3')


def get_ski_from_public_key(pk_or_pk_bytes: Union[PublicKey, bytes], hash_type: HashType = HashType.SHA256) -> str:
    """
    通过公钥对象或公钥二进制内容，获取证书使用者密钥标识subject key identifier
    :param pk_or_pk_bytes: 公钥对象或公钥二进制内容
    :param hash_type: 哈希类型
    :return:
    """
    if isinstance(pk_or_pk_bytes, bytes):
        pk_der_bytes = pk_or_pk_bytes
    else:
        pk_der_bytes = _get_pk_der_bytes_from_public_key(pk_or_pk_bytes)
    return _get_ski_from_pk_der_bytes(pk_der_bytes, hash_type)


def _get_ski_from_cert(cert_or_cert_bytes: Union[Certificate, bytes]) -> str:
    """
    获取证书对象或证书二进制内容，获取证书使用者密钥标识subject key identifier
    :param cert_or_cert_bytes: 证书对象或证书二进制内容
    :return: hex字符串
    """
    cert = cert_or_cert_bytes
    if isinstance(cert_or_cert_bytes, bytes):
        cert = x509.load_pem_x509_certificate(cert_or_cert_bytes)
    ski = cert.extensions.get_extension_for_oid(
        x509.oid.ExtensionOID.SUBJECT_KEY_IDENTIFIER).value.key_identifier.hex()
    return ski


def get_evm_address_from_public_key(pk: Union[ec.EllipticCurvePublicKey, rsa.RSAPublicKey],
                                    hash_type: HashType = HashType.SHA256) -> str:
    """
    根据公钥生成以太坊地址
    :param hash_type:
    :param pk: 公钥对象
    :return: 42位地址
    """
    # pk_der_bytes = pk.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    # sub_pki, _ = decoder.decode(pk_der_bytes, asn1Spec=rfc3280.SubjectPublicKeyInfo())
    # sub_pki_bytes = sub_pki.components[1].asOctets()

    # if hash_type.upper() == HashType.SHA256:
    # ski = sha256(sub_pki_bytes).hexdigest()
    # ski = sub_pki_bytes.hex()
    # addr = _calc_address_from_ski(ski)
    # return str(int(addr, 16))
    # raise NotImplementedError('哈希类型暂时仅支持SHA256')  # todo SHA3_256 SHA3_256 SM3

    # ski = sub_pki_bytes.hex()
    # addr = _calc_address_from_ski(ski)
    # return addr

    # pk = cert.public_key()
    pk_der_bytes = _get_public_der_bytes(pk)
    return _calc_address_from_ski(pk_der_bytes.hex()[2:])


def get_evm_address_from_cert_bytes(cert_bytes: bytes) -> str:
    cert = x509.load_pem_x509_certificate(cert_bytes)
    # ski = _get_ski_from_cert(cert)
    # addr = _calc_address_from_ski(ski)
    # return str(int(addr, 16))
    pk = cert.public_key()
    # pk_der_bytes = _get_public_der_bytes(pk)
    # return _calc_address_from_ski(pk_der_bytes.hex()[2:])
    return get_evm_address_from_public_key(pk)


def get_chainmaker_address_from_public_key(pk: PublicKey, hash_type: HashType = HashType.SHA256) -> str:
    """
    根据公钥生成Chainmaker地址
    :param hash_type:
    :param pk: 公钥对象
    :return: 40位地址
    """
    ski = get_ski_from_public_key(pk, hash_type)
    return _calc_address_from_ski(ski)


def get_chainmaker_address_from_cert_bytes(cert_bytes: bytes) -> str:
    """
    通过PEM格式证二进制内容书获取地址
    :param cert_bytes: 证书二进制内容
    :return: 40位地址
    """
    cert = x509.load_pem_x509_certificate(cert_bytes)
    ski = _get_ski_from_cert(cert)
    return _calc_address_from_ski(ski)


def get_zxl_address_from_public_key(pk: PublicKey, hash_type: HashType = HashType.SM3) -> str:
    """
    根据公钥生成至信链地址
    :param pk: 公钥对象
    :param hash_type: 哈希类型, 目前至信链地址哈希类型仅支持SM3
    :return: 42位地址
    """
    pk_der_bytes = _get_public_der_bytes(pk)
    if hash_type == HashType.SM3:
        addr = sm3.sm3_hash(pk_der_bytes)[:40]
        return 'ZX%s' % addr
    raise NotImplementedError('至信链地址哈希类型目前仅执行SM3')


def get_zxl_address_from_cert_pem(cert_bytes: bytes) -> str:  # todo remove for not used
    """
    通过PEM格式证书二进制内容获取至信链地址
    :param cert_bytes: PEM格式证书二进制内容
    :return: 42位地址
    """
    warnings.warn('will be removed for not used', DeprecationWarning)
    cert = x509.load_pem_x509_certificate(cert_bytes)
    pk = cert.public_key()
    return get_zxl_address_from_public_key(pk)


def get_address_from_private_key_pem(private_key_pem: bytes, addr_type: AddrType = AddrType.CHAINMAKER,
                                     hash_type: HashType = HashType.SHA256):
    """
    根据PEM私钥文件二进制内容获取用户地址
    :param private_key_pem: PEM格式私钥文件二进制内容
    :param addr_type: 地址类型 0-长安链 1-至信链 2-以太坊
    :param hash_type: 哈希类型，至信链仅支持HashType.SM3
    :return: 40位长安链地址 或 42位至信链地址(ZX开头) 或 42位以太坊地址(0x开头)
    """

    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    pk = private_key.public_key()
    return public_key_to_addr(pk, hash_type, addr_type)


def get_address_from_cert_bytes(cert_bytes: bytes, addr_type: AddrType = AddrType.CHAINMAKER) -> str:
    """
    根据PEM证书文件二进制内容获取用户地址
    :param cert_bytes: PEM格式证书二进制内容
    :param addr_type: 地址类型 0-长安链 1-至信链 2-以太坊
    :return: 40位长安链地址 或 42位至信链地址(ZX开头) 或 42位以太坊地址(0x开头)
    """
    cert = x509.load_pem_x509_certificate(cert_bytes)
    pk = cert.public_key()

    if addr_type == AddrType.ZXL:
        return get_zxl_address_from_public_key(pk, HashType.SM3)

    elif addr_type == AddrType.CHAINMAKER:
        return get_chainmaker_address_from_cert_bytes(cert_bytes)

    elif addr_type == AddrType.ETHEREUM:
        return get_evm_address_from_cert_bytes(cert_bytes)


def public_key_to_addr(public_key: PublicKey, hash_type: HashType, addr_type: AddrType):
    """公钥对象转地址"""
    if addr_type == AddrType.ETHEREUM:
        return get_evm_address_from_public_key(public_key, hash_type)
    if addr_type == AddrType.ZXL:
        return get_zxl_address_from_public_key(public_key, hash_type=HashType.SM3)
    return get_chainmaker_address_from_public_key(public_key, hash_type)


def cert2addr(cert_pem: str, addr_type: Union[AddrType, str, int]):
    """证书转地址"""
    addr_type = ensure_enum(addr_type, AddrType)
    return get_address_from_cert_bytes(cert_pem.encode(), addr_type)


def sk2addr(private_key_pem: str, hash_type: [HashType, str, int] = HashType.SHA256,
            addr_type: Union[AddrType, str, int] = AddrType.ETHEREUM):
    """私钥转地址"""
    hash_type = ensure_enum(hash_type, HashType)
    addr_type = ensure_enum(addr_type, AddrType)
    return get_address_from_private_key_pem(private_key_pem.encode(), addr_type, hash_type)


def pk2addr(public_key_pem, hash_type: Union[HashType, str, int] = HashType.SHA256,
            addr_type: Union[AddrType, str, int] = AddrType.ETHEREUM):
    """公钥转地址"""
    public_key = serialization.load_pem_public_key(public_key_pem)
    return public_key_to_addr(public_key, hash_type, addr_type)


def name2addr(name: str, block_version: int = 2300, addr_type: Union[AddrType, str, int] = AddrType.ETHEREUM):  # ✅
    """名称转地址"""
    addr_type = ensure_enum(addr_type, AddrType)
    data = name.encode()
    if block_version >= 2300:
        if addr_type == AddrType.ZXL:
            data = bytes.fromhex(sm3.sm3_hash(data))
        else:
            data = bytes.fromhex(keccak_256(data))
    if addr_type == AddrType.ZXL:
        addr = 'ZX%s' % sm3.sm3_hash(data)[:40]
    else:
        addr = keccak_256(data)[24:]
    return addr


def hex2addr(pk_hex: str, hash_type: Union[HashType, str, int] = HashType.SHA256,
             addr_type: Union[AddrType, str, int] = AddrType.ETHEREUM):
    """公钥哈希转地址"""
    hash_type = ensure_enum(hash_type, HashType)
    addr_type = ensure_enum(addr_type, AddrType)
    pk_der_bytes = bytes.fromhex(pk_hex)
    public_key = serialization.load_der_public_key(pk_der_bytes)
    return public_key_to_addr(public_key, hash_type, addr_type)


def _get_public_der_bytes(pk: PublicKey):
    pk_numbers = pk.public_numbers()
    if isinstance(pk, rsa.RSAPublicKey):
        n, e = pk_numbers.n, pk_numbers.e
        pk_der_bytes = ans1_dump(n, e)
    else:
        x, y = pk_numbers.x, pk_numbers.y
        ret = '04%064x%064x' % (x, y)
        pk_der_bytes = bytes.fromhex(ret)  # todo pk.key_size
    return pk_der_bytes
