#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   sm2_asn1.py
# @Function     :   

from pyasn1.type import namedtype, namedval, univ

SM2_OID = '1.2.840.10045.2.1'
EC_PUBLIC_KEY_OID = '1.2.156.10197.1.301'


class AlgorithmIdentifier(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('algorithm', univ.ObjectIdentifier()),
        namedtype.NamedType('namedCurve', univ.ObjectIdentifier())
    )


class SM2PublicKeyInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('algorithm', AlgorithmIdentifier()),
        namedtype.NamedType('publicKey', univ.BitString())
    )


# pkcs8
class SM2PrivateKeyInfo(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('v1', 0), ))),
        namedtype.NamedType('privateKeyAlgorithm', AlgorithmIdentifier()),
        # in ECDSA format 30740201010420 + private_key + a00706052b8104000aa144034200 + 04 + public_key.x + public_key.y
        namedtype.NamedType('privateKey', univ.OctetString()),

    )


class SM2Signature(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('r', univ.Integer()),
        namedtype.NamedType('s', univ.Integer()),
    )


sm2_algorithm = AlgorithmIdentifier()
sm2_algorithm["algorithm"] = SM2_OID
sm2_algorithm["namedCurve"] = EC_PUBLIC_KEY_OID
