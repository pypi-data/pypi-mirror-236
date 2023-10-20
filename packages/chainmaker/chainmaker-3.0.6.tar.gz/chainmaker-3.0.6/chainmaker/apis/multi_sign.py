#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   multi_sign.py
# @Function     :   ChainMaker多签接口
from typing import Callable, Union

from chainmaker.apis.base_client import BaseClient
from chainmaker.protos.common.request_pb2 import EndorsementEntry, Payload
from chainmaker.protos.common.result_pb2 import TxResponse
from chainmaker.protos.syscontract.multi_sign_pb2 import MultiSignInfo, MultiSignVoteInfo
from chainmaker.user import ClientUser
from chainmaker.keys import SystemContractName, MultiSignMethod, ParamKey, VoteStatus

from chainmaker.utils.result_utils import check_response


class MultiSignMixin(BaseClient):
    """多签操作"""
    get_tx_by_tx_id: Callable

    def create_multi_sign_req_payload(self, params: Union[list, dict], tx_id: str = None) -> Payload:
        """
        创建多签请求待签名Payload
        :param params: 发起多签请求所需的参数
        :param tx_id: 指定交易Id
        :return: 待签名Payload
        """
        return self._payload_builder.create_invoke_payload(SystemContractName.MULTI_SIGN.name, MultiSignMethod.REQ.name,
                                                           params, tx_id=tx_id)

    # 04-00 发起多签请求
    def multi_sign_req(self, payload: Payload, timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        发起多签请求
        <04-00-MULTI_SIGN-REQ>
        :param payload: 待签名payload
        :param timeout: 请求超时时间
        :param with_sync_result: 是否同步获取交易结果
        :return: 交易响应或交易信息
        """
        self._debug('begin to send multi sign request')
        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 04-01 对多签请求Payload进行投票
    def multi_sign_vote(self, multi_sign_req_payload, endorser: ClientUser = None, is_agree: bool = True,
                        timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        对多签请求Payload进行投票
        <04-01-MULTI_SIGN-VOTE>
        :param multi_sign_req_payload: 待签名payload
        :param endorser: 投票用户对象
        :param is_agree: 是否同意，true为同意，false则反对
        :param timeout: 请求超时时间
        :param with_sync_result: 是否同步获取交易结果
        :return: 交易响应或交易信息
        """
        if endorser is None:
            endorser = self.user
        self._debug('begin to vote multi sign request payload [is_agree:%s]' % is_agree)
        vote_status = VoteStatus.AGREE.name if is_agree is True else VoteStatus.REJECT.name
        payload_bytes = multi_sign_req_payload.SerializeToString()
        vote_info = self._create_vote_info(vote_status=vote_status, endorsement=endorser.sign(payload_bytes))

        params = {
            ParamKey.VOTE_INFO.name: vote_info.SerializeToString(),
            ParamKey.TX_ID.name: multi_sign_req_payload.tx_id
        }
        payload = self._payload_builder.create_invoke_payload(SystemContractName.MULTI_SIGN.name,
                                                              MultiSignMethod.VOTE.name,
                                                              params)
        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)

    def multi_sign_vote_by_tx_id(self, tx_id: str, endorser: ClientUser = None, is_agree: bool = True,
                                 timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        根据交易Id对多签请求进行投票
        :param tx_id: 交易Id
        :param endorser: 投票用户对象
        :param is_agree: 是否同意，true为同意，false则反对
        :param timeout: 请求超时时间
        :param with_sync_result: 是否同步获取交易结果
        :return: 交易响应或交易信息
        """
        if endorser is None:
            endorser = self.user
        tx = self.get_tx_by_tx_id(tx_id)
        payload = tx.transaction.payload
        payload_bytes = payload.SerializeToString()
        vote_status = VoteStatus.AGREE.name if is_agree is True else VoteStatus.REJECT.name
        vote_info = self._create_vote_info(vote_status=vote_status, endorsement=endorser.sign(payload_bytes))
        params = {
            ParamKey.VOTE_INFO.name: vote_info.SerializeToString(),
            ParamKey.TX_ID.name: tx_id
        }

        payload = self._payload_builder.create_invoke_payload(SystemContractName.MULTI_SIGN.name,
                                                              MultiSignMethod.VOTE.name,
                                                              params)
        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)

    # 04-02 查询多签状态
    def multi_sign_query(self, tx_id: str, timeout: int = None) -> MultiSignInfo:
        """
        查询多签状态
        <04-02-MULTI_SIGN-QUERY>
        :param tx_id: 交易ID
        :param timeout: RPC请求超时时间
        :return: 多签信息
        """
        self._debug('begin to query multi sign request [tx_id:%s]' % tx_id)
        params = {ParamKey.TX_ID.name: tx_id}
        payload = self._payload_builder.create_query_payload(SystemContractName.MULTI_SIGN.name,
                                                             MultiSignMethod.QUERY.name,
                                                             params)
        response = self.send_request(payload, timeout=timeout)
        check_response(response)
        multi_sign_info = MultiSignInfo()
        multi_sign_info.ParseFromString(response.contract_result.result)
        return multi_sign_info

    def multi_sign_trig(self, multi_sign_req_payload: Payload = None, tx_id: str = None, gas_limit: int=None,
                        timeout: int = None, with_sync_result: bool = None) -> TxResponse:
        """
        发送线上多签触发请求到节点 v2.3.1新增
        :param gas_limit:
        :param tx_id:
        :param multi_sign_req_payload: 多签请求
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        if multi_sign_req_payload is not None:
            tx_id = multi_sign_req_payload.tx_id
        params = {ParamKey.TX_ID.name: tx_id}
        payload = self._payload_builder.create_invoke_payload(SystemContractName.MULTI_SIGN.name,
                                                              MultiSignMethod.TRIG.name,
                                                              params)
        if gas_limit:
            self.attach_gas_limit(payload, gas_limit)

        return self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)

    @staticmethod
    def _create_vote_info(vote_status: str, endorsement: EndorsementEntry) -> MultiSignVoteInfo:
        """
        创建多签投票信息结构体
        :param vote_status: AGREE或REJECT
        :param endorsement: 背书项
        :return: 多签投票信息结构体
        """
        return MultiSignVoteInfo(vote=vote_status, endorsement=endorsement)
