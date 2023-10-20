#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @FileName     :   file_utils.py
# @Author       :   superhin
# @CreateTime   :   2022/4/8 14:57
# @Function     :   文件读取、目录切换等实用方法
import base64
import json
import os
import re
import warnings
from pathlib import Path
from typing import Union

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from yaml import load

_pattern = re.compile(r'.*?(\${\w+}).*?')


def read_file(file_path: Union[str, Path], ignore_io_error: bool = False):
    warnings.warn('will be removed for not used', DeprecationWarning)
    if file_path is None:
        return None
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except IOError:
        if ignore_io_error is True:
            return
        raise


def read_file_bytes(file_path: Union[str, Path], ignore_io_error: bool = False) -> Union[bytes, None]:
    if file_path is None:
        return None
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except IOError:
        if ignore_io_error is True:
            return
        raise


def load_byte_code(byte_code_or_file_path: Union[str, Path, bytes]) -> bytes:
    """
    加载合约二进制文件
    :param byte_code_or_file_path: 合约字节码：可以是字节码；合约文件路径；或者 hex编码字符串；或者 base64编码字符串
    :return:
    """
    # 如果是字节码 直接返回
    if isinstance(byte_code_or_file_path, bytes):
        return byte_code_or_file_path

    byte_code_or_file_path = str(byte_code_or_file_path)

    # 如果是文件 返回文件内容（字节码）
    if isinstance(byte_code_or_file_path, str) or isinstance(byte_code_or_file_path, Path):
        with open(byte_code_or_file_path, 'rb') as f:
            return f.read()

    # 如果 字符串 先尝试hex解码， 解码成功后返回
    try:
        return bytes.fromhex(str(byte_code_or_file_path))
    except ValueError:
        pass
    # 如果 字符串 尝试base64解码，解码成功后返回
    try:
        return base64.b64decode(byte_code_or_file_path)
    except ValueError:
        raise


def load_abi_file(abi_file: str) -> dict:
    """
    加载abi_file得到fuctions列表
    :param abi_file: abi_file路径
    :return: 函数名：参数类型列表
    """
    warnings.warn('will be removed for not used', DeprecationWarning)
    with open(abi_file) as f:
        data = json.load(f)
    functions = {}
    for item in data:
        if 'function' == item.get('type'):
            functions[item.get('name')] = [param.get('type') for param in item.get('inputs', [])]
    return functions


class switch_dir:
    """用于切换目录以支持yaml配置文件中使用相对路径"""

    def __init__(self, path):
        self.origin_path = os.getcwd()
        if os.path.isdir(path):
            self.path = path
        else:  # 如果传入文件则切换到文件所在目录
            self.path = os.path.dirname(path)

    def __enter__(self):
        os.chdir(self.path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.origin_path)


def _env_var_constructor(loader, node):
    """为yaml增加支持${系统环境变量支持}"""
    value = loader.construct_scalar(node)
    for item in _pattern.findall(value):  # 遍历所有匹配到到${变量名}的变量, 如${USER}
        var_name = item.strip('${} ')  # 如,USER
        value = value.replace(item, os.getenv(var_name, item))  # 用环境变量中取到的对应值替换当前变量
    return value  # 如superhin替换${USER}，取不到则使用原值${USER}


def load_yaml(file_path: Union[str, Path], is_switch_dir=False) -> Union[dict, list]:
    """
    加载yaml文件数据
    :param file_path: 文件路径
    :param is_switch_dir: 是否切换路径到文件所在路径进行加载（以支持文件中到相对路径）
    :return: dict/list
    """
    assert os.path.isfile(str(file_path)), 'FileNotExist: %s' % file_path
    Loader.add_constructor('!env', _env_var_constructor)
    Loader.add_implicit_resolver('!env', _pattern, None)
    with open(file_path, encoding='utf-8') as f:
        if is_switch_dir is True:
            with switch_dir(file_path):
                return load(stream=f, Loader=Loader)
        return load(stream=f, Loader=Loader)


def get_abs_path(path: Union[Path, str], parent_dir: str = '.'):
    """将相遇于配置目录当相对路径转为绝对路径"""
    warnings.warn('will be removed for not used', DeprecationWarning)
    path = str(path)
    return path if path.startswith('/') else os.path.abspath(os.path.join(parent_dir, path))
