#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   exceptions.py
# @Function     :   已知异常

# InactiveRpcError = grpc._channel._InactiveRpcError
from chainmaker.protos.common.result_pb2 import TxStatusCode

ERR_MSG_MAP = {
    'Empty switch_branch': 'Empty trust_root_paths',
    'failed to connect to all addresses': 'Failed to connect address, please check server, port and trust_root_paths'
}


class RpcRequestTimeout(Exception):
    """
    DeadLine Exceeded
    eg. grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
        status = StatusCode.DEADLINE_EXCEEDED
        details = "Deadline Exceeded"
        debug_error_string = "{"created":"@1652179414.038091000","description":
        "Error received from peer ipv4:192.168.1.241:12301","file":"src/core/lib/surface/call.cc","file_line":904,
        "grpc_message":"Deadline Exceeded","grpc_status":4}"
    """


class RpcConnectError(Exception):
    """
    Failed to connect to the rpc server
    """


class SdkConfigError(Exception):
    """sdk_config配置错误"""


class OnChainFailedError(Exception):
    """
    failed to put data or tx on chain
    """


class InvalidParametersError(Exception):
    """
    failed to put data or tx on chain
    """


class GetTxTimeoutError(TimeoutError):
    """通过交易Id获取交易信息超时"""


# ChainMaker返回Fail
class RequestError(Exception):
    """
    We failed to decode ABI output.

    Most likely ABI mismatch.
    """

    def __init__(self, err_code, err_msg, *args):
        self.err_code = err_code
        self.err_msg = err_msg
        super().__init__(f'TxStatusCode: {self.err_code} message: {self.err_msg}', *args)


class Timeout(RequestError):
    """"""


class InvalidParameter(RequestError):
    """"""


class NoPermission(RequestError):
    """"""


class ContractFail(RequestError):
    """"""


class InternalError(RequestError):
    """"""


class InvalidContractTransactionType(RequestError):
    pass


class InvalidContractParameterContractName(RequestError):
    pass


class InvalidContractParameterMethod(RequestError):
    pass


class InvalidContractParameterInitMethod(RequestError):
    pass


class InvalidContractParameterUpgradeMethod(RequestError): ...


class InvalidContractParameterByteCode(RequestError): ...


class InvalidContractParameterRuntimeType(RequestError): ...


class InvalidContractParameterVersion(RequestError): ...


class GetFromTxContextFailed(RequestError): ...


class PutIntoTxContextFailed(RequestError): ...


class ContractVersionExistFailed(RequestError): ...


class ContractVersionNotExistFailed(RequestError): ...


class ContractByteCodeNotExistFailed(RequestError): ...


class MarshalSenderFailed(RequestError): ...


class InvokeInitMethodFailed(RequestError): ...


class InvokeUpgradeMethodFailed(RequestError): ...


class CreateRuntimeInstanceFailed(RequestError): ...


class UnmarshalCreatorFailed(RequestError): ...


class UnmarshalSenderFailed(RequestError): ...


class GetSenderPkFailed(RequestError): ...


class GetCreatorPkFailed(RequestError): ...


class GetCreatorFailed(RequestError): ...


class GetCreateCertFailed(RequestError): ...


class GetSenderCertFailed(RequestError): ...


class ContractFreezeFailed(RequestError): ...


class ContractTooDeepFailed(RequestError): ...


class ContractRevokeFailed(RequestError): ...


class ContractInvokeMethodFailed(RequestError): ...


class GasBalanceNotEnoughFailed(RequestError): ...


TX_RESPONSE_ERROR_MAP = {
    1: Timeout,
    2: InvalidParameter,
    3: NoPermission,
    4: ContractFail,
    5: InternalError,

    10: InvalidContractTransactionType,
    11: InvalidContractParameterContractName,
    12: InvalidContractParameterMethod,
    13: InvalidContractParameterInitMethod,
    14: InvalidContractParameterUpgradeMethod,
    15: InvalidContractParameterByteCode,
    16: InvalidContractParameterRuntimeType,
    17: InvalidContractParameterVersion,

    20: GetFromTxContextFailed,
    21: PutIntoTxContextFailed,
    22: ContractVersionExistFailed,
    23: ContractVersionNotExistFailed,
    24: ContractByteCodeNotExistFailed,
    25: MarshalSenderFailed,
    26: InvokeInitMethodFailed,
    27: InvokeUpgradeMethodFailed,
    28: CreateRuntimeInstanceFailed,
    29: UnmarshalCreatorFailed,
    30: UnmarshalSenderFailed,
    31: GetSenderPkFailed,
    32: GetCreatorPkFailed,
    33: GetCreatorFailed,
    34: GetCreateCertFailed,
    35: GetSenderCertFailed,
    36: ContractFreezeFailed,
    37: ContractTooDeepFailed,
    38: ContractRevokeFailed,
    39: ContractInvokeMethodFailed,
    42: GasBalanceNotEnoughFailed,

}


# 补充-非ChainMaker标准Error
class AuthenticationError(InternalError):
    """
    交易校验失败-验证交易权限失败-权限出错
    eg. tx _verify failed, _verify tx authentation failed, authentication error
    """


class EndorsementNotEnoughError(AuthenticationError):
    """
    背书不足错误
    eg. authentication fail: not enough participants support this action:
    3 valid endorsements required, 0 valid endorsements received
    """


class EndorsementEmptyError(AuthenticationError):
    """
    背书为空错误
    eg. tx _verify failed, _verify tx authentation failed,
    endorsement is nil in verifyTxAuth for resourceId[CONTRACT_MANAGE-INIT_CONTRACT]
    """


class EndorsementInvalidError(AuthenticationError):
    """
    背书无效错误
    eg.  tx _verify failed, _verify tx authentation failed, authentication error: authentication failed,
    [refine endorsements failed, all endorsers have failed verification]
    """


class ForbiddenAccessError(AuthenticationError):
    """
    禁止访问错误
    eg.  tx _verify failed, _verify tx authentation failed, authentication error: authentication failed,
    is forbidden to access
    """


class TxPoolFullError(InternalError):
    """Add tx failed, TxPool is full"""


# contract_fail


class GasLimitNotEnoughError(ContractFail):
    """eg. gas limit is not enough, [limit:0]/[gasUsed:1376]"""


class ContractInitialError(ContractFail):
    """
    eg. contract initial fail, out of memory
    eg. contract initial fail, contract message:amount is null
    """


# todo target [wx-org4.chainmaker.org] does not belong to the signer,
# verify admin failed
#  'the method does not found'
# account address is illegal
# signers do not meet the requirements (ARCHIVE)


def handle_internal_error(tx_response):
    if 'tx verify failed' in tx_response.message:
        if 'is forbidden to access' in tx_response.message:
            raise ForbiddenAccessError(TxStatusCode.Name(tx_response.code), tx_response.message)
        if 'not enough participants' in tx_response.message:
            raise EndorsementNotEnoughError(TxStatusCode.Name(tx_response.code), tx_response.message)
        if 'endorsement is nil' in tx_response.message:
            raise EndorsementEmptyError(TxStatusCode.Name(tx_response.code), tx_response.message)
        if 'refine endorsements failed' in tx_response.message:
            raise EndorsementInvalidError(TxStatusCode.Name(tx_response.code), tx_response.message)
        raise AuthenticationError(TxStatusCode.Name(tx_response.code), tx_response.message)
    if 'TxPool is full' in tx_response.message:
        raise TxPoolFullError(TxStatusCode.Name(tx_response.code), tx_response.message)


def handle_contract_fail(tx_response):
    if 'gas limit is not enough' in tx_response.message:
        raise GasLimitNotEnoughError(TxStatusCode.Name(tx_response.code), tx_response.message)
    if 'contract initial fail' in tx_response.message:
        raise ContractInitialError(TxStatusCode.Name(tx_response.code), tx_response.message)


class ChainClientException(Exception):
    pass
