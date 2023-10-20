#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   common.py
# @Function     :   实用工具方法
import uuid
from enum import Enum
from pathlib import Path
from typing import List, Union

from google.protobuf.message import Message

from chainmaker.keys import AuthType, HashType
from chainmaker.protos.common import request_pb2
from chainmaker.sdk_config import DefaultConfig
from chainmaker.utils import file_utils


def gen_rand_tx_id() -> str:
    """生成随机交易Id"""
    return uuid.uuid4().hex + uuid.uuid4().hex


def gen_timestamp_tx_id() -> str:  # todo
    """根据时间戳生成交易Id"""
    pass


def gen_rand_contract_name(prefix: str = 'contract_') -> str:
    """
    生成随机合约名称
    :param prefix: 合约名前缀
    :return: 随机合约名称
    """
    return '%s%s' % (prefix, str(uuid.uuid4()).replace("-", ""))


def gen_rand_alias(prefix: str = 'alias_') -> str:
    """
    生成随机合约名称
    :param prefix: 合约名前缀
    :return: 随机合约名称
    """
    return '%s%s' % (prefix, str(uuid.uuid4()).replace("-", ""))


def ensure_bytes(value: Union[bytes, str, bool, int, Enum]):
    """确保转为bytes类型"""
    if isinstance(value, Enum):
        value = value.value
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode()
    elif isinstance(value, bool):
        return b'true' if value is True else b'false'
    else:
        return str(value).encode()


def ensure_str(item: Union[Enum, str]):
    if isinstance(item, str):
        return item
    if isinstance(item, Enum):
        return item.name
    return str(item)


def ensure_list_str(items: List[Union[Enum, str]]):
    if not items or isinstance(items, list):
        return items
    _items = []
    for item in items:
        if isinstance(item, str):
            _items.append(item)
        if isinstance(item, Enum):
            _items.append(item.name)
        else:
            _items.append(str(item))
    return _items


def ensure_path(path: Union[Path, str]):
    if isinstance(path, Path):
        return path
    return Path(path)


def ensure_enum(item: Union[Enum, str, int], enum_type):
    if isinstance(item, enum_type):
        return item
    if isinstance(item, int):
        return enum_type(item)
    if isinstance(item, str):
        return enum_type[item]


def ensure_cert_bytes(cert_bytes_or_cert_file_path: Union[Path, str, bytes]) -> bytes:
    """
    确保为证书二进制内容
    :param cert_bytes_or_cert_file_path: 证书二进制内容或证书文件路径
    :return:
    """
    if isinstance(cert_bytes_or_cert_file_path, bytes):
        return cert_bytes_or_cert_file_path
    return file_utils.read_file_bytes(cert_bytes_or_cert_file_path)


def params_map_kv_pairs(params: Union[None, dict, list]) -> list:
    if not params:
        return []

    assert isinstance(params, (dict, list)), "params仅支持None, dict或list类型"

    if isinstance(params, list) and len(params) > 0 and isinstance(params[0], request_pb2.KeyValuePair):
        return params

    if isinstance(params, list):
        pairs = []
        for item in params:
            assert isinstance(item, dict), f'list中每一项应为dict类型: {item}'
            kv = request_pb2.KeyValuePair(key=ensure_str(item.get('key')), value=ensure_bytes(item.get('value')))
            pairs.append(kv)
    else:
        return [request_pb2.KeyValuePair(key=ensure_str(key), value=ensure_bytes(value)) for key, value in
                params.items()]


def uint64_to_bytes(i: int):
    """无符号uint64转bytes"""
    # return struct.pack('<Q', i)
    return i.to_bytes(8, byteorder='little', signed=False)


def int64_to_bytes(i: int):
    """有符号int64转bytes"""
    return i.to_bytes(8, byteorder='little', signed=True)


def msg_to_bytes(msg: Message) -> bytes:
    """proto消息对象转bytes"""
    return msg.SerializeToString()


def msg_from_bytes(msg: Message, data: bytes) -> Message:
    """proto消息对象从bytes中加载数据"""
    return msg.ParseFromString(data)


def format_hash_type(hash_type: str) -> HashType:
    """格式化hash_type"""
    if not hash_type:
        return DefaultConfig.hash_type
    hash_type = hash_type.upper()
    if hash_type == 'SHA256':
        return HashType.SHA256
    if hash_type == 'SHA3_256' or hash_type == 'SHA3_256':
        return HashType.SHA3_256
    if hash_type == 'SM3':
        return HashType.SM3
    return DefaultConfig.hash_type


def format_auth_type(auth_type: str) -> AuthType:
    """格式化auth_type"""
    if not auth_type:
        return DefaultConfig.auth_type
    if auth_type.lower() == 'public':
        return AuthType.Public
    if auth_type.lower() == 'permissionedwithkey':
        return AuthType.PermissionedWithKey
    return DefaultConfig.auth_type
