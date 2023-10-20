#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   setup.py
# @Function     :   安装配置

from setuptools import find_packages, setup

__version__ = '3.0.6'

INSTALL_REQUIRES = [
    "protobuf",
    "grpcio",
    "pyyaml",
    "cryptography",
    "pysha3",
    "pymysql",
    "eth-abi>2.6",
    "asn1",  # todo remove
    "pyasn1",
    "pyasn1-modules",
    "requests",
]

TEST_REQUIRES = [
    'pytest>=3.3.1',
    'pytest-timeout'
]

PACKAGES = [
    'chainmaker',
    'chainmaker.apis',
    'chainmaker.archive_service',
    'chainmaker.utils',
    'chainmaker.utils.gm',
    'chainmaker.protos',
    'chainmaker.protos.accesscontrol',
    'chainmaker.protos.api',
    'chainmaker.protos.archivecenter',
    'chainmaker.protos.common',
    'chainmaker.protos.config',
    'chainmaker.protos.consensus',
    'chainmaker.protos.discovery',
    'chainmaker.protos.eth',
    'chainmaker.protos.net',
    'chainmaker.protos.google',
    'chainmaker.protos.google.api',
    'chainmaker.protos.google.protobuf',
    'chainmaker.protos.store',
    'chainmaker.protos.sync',
    'chainmaker.protos.syscontract',
    'chainmaker.protos.tee',
    'chainmaker.protos.txfilter',
    'chainmaker.protos.txpool',
    'chainmaker.protos.vm',
]

setup(
    name='chainmaker',
    version=__version__,
    description='ChainMaker Python SDK',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='THL chainmaker developers',
    author_email='operation@chainmaker.org',
    license='Apache License',
    url='https://git.chainmaker.org.cn/chainmaker/chainmaker-sdk-python.git',
    include_package_data=True,
    # packages=find_packages(),
    packages=PACKAGES,
    zip_safe=True,
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
    keywords=["chainmaker", "blockchain", "chainmaker-sdk-python", "chainmaker-sdk"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: User Interfaces',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
