#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# @FileName     :   dpos.py
# @Function     :   ChainMaker DPOS ERC20 / DPOS Stake 等操作接口

from chainmaker.apis.base_client import BaseClient
from chainmaker.keys import (SystemContractName, DposStakeMethod, ParamKey)
from chainmaker.protos.common.request_pb2 import Payload
from chainmaker.protos.common.result_pb2 import TxResponse
from chainmaker.protos.syscontract.dpos_stake_pb2 import Delegation, DelegationInfo, Epoch, Validator, ValidatorVector


class DPosStakeMixIn(BaseClient):
    """DPos权益操作"""

    # 08-00 查询所有的候选人
    def get_all_candidates(self) -> ValidatorVector:  # ✅
        """
        查询所有的候选人
        <08-00-DPOS_STAKE-GET_ALL_CANDIDATES>
        :return: 候选人列表
        """
        self._debug('begin to get all candidates')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_STAKE.name,
                                                             DposStakeMethod.GET_ALL_CANDIDATES.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        vectors = ValidatorVector()
        vectors.ParseFromString(data)
        return vectors

    # 08-01 通过地址获取验证人的信息
    def get_validator_by_address(self, address: str):  # ✅
        """
        通过地址获取验证人的信息
        <08-01-DPOS_STAKE-GET_VALIDATOR_BY_ADDRESS>
        :param address:
        :return:
        """
        self._debug('begin to get validator by address %s' % address)
        params = {
            ParamKey.address.name: address
        }
        payload = self._payload_builder.create_query_payload(
            SystemContractName.DPOS_STAKE.name,
            DposStakeMethod.GET_VALIDATOR_BY_ADDRESS.name,
            params)

        response = self.send_request(payload)
        data = response.contract_result.result
        validator = Validator()
        validator.ParseFromString(data)
        return validator

    # 08-02 抵押权益到验证人
    def delegate(self, address: str, amount: int) -> Delegation:  # fixme 无结果
        """
        抵押权益到验证人
        <08-02-DPOS_STAKE-DELEGATE>
        :param address:
        :param amount:
        :return:
        """
        self._debug('begin to delegate %s %s' % (address, amount))
        params = {
            ParamKey.to.name: address,
            ParamKey.amount.name: str(amount)
        }
        payload = self._payload_builder.create_invoke_payload(
            SystemContractName.DPOS_STAKE.name,
            DposStakeMethod.DELEGATE.name,
            params)

        response = self.send_request(payload)
        data = response.contract_result.result
        delegation = Delegation()
        delegation.ParseFromString(data)
        return delegation

    # 08-03 查询指定地址的抵押信息
    def get_delegations_by_address(self, address: str) -> DelegationInfo:  # ✅
        """
        查询指定地址的抵押信息
        <08-03-DPOS_STAKE-GET_DELEGATIONS_BY_ADDRESS>
        :param address:
        :return:
        """
        self._debug('begin to get delegation by address %s' % address)
        params = {
            ParamKey.address.name: address
        }
        payload = self._payload_builder.create_query_payload(
            SystemContractName.DPOS_STAKE.name,
            DposStakeMethod.GET_DELEGATIONS_BY_ADDRESS.name,
            params)
        response = self.send_request(payload)
        data = response.contract_result.result
        delegate_info = DelegationInfo()
        delegate_info.ParseFromString(data)
        return delegate_info

    # 08-04 查询指定地址的抵押信息
    def get_user_delegation_by_validator(self, delegator: str, validator: str) -> Delegation:  # ✅
        """
        查询指定地址的抵押信息
        <08-04-DPOS_STAKE-GET_USER_DELEGATION_BY_VALIDATOR>
        :param delegator:
        :param validator:
        :return:
        """
        self._debug('begin to get delegation by address %s %s' % (delegator, validator))
        params = {
            ParamKey.delegator_address.name: delegator,
            ParamKey.validator_address.name: validator,
        }
        payload = self._payload_builder.create_query_payload(
            SystemContractName.DPOS_STAKE.name,
            DposStakeMethod.GET_USER_DELEGATION_BY_VALIDATOR.name,
            params)
        response = self.send_request(payload)
        data = response.contract_result.result
        delegation = Delegation()
        delegation.ParseFromString(data)
        return delegation

    # 08-04 从验证人解除抵押的权益
    def undelegate(self, address: str, amount: int) -> Delegation:  # fixme 无结果
        """
        从验证人解除抵押的权益
        <08-05-DPOS_STAKE-UNDELEGATE>
        :param address:
        :param amount:
        :return:
        """
        self._debug('begin to undelegate %s %s' % (address, amount))
        params = {
            ParamKey._from.name: address,
            ParamKey.amount.name: str(amount)
        }
        payload = self._payload_builder.create_invoke_payload(
            SystemContractName.DPOS_STAKE.name,
            DposStakeMethod.UNDELEGATE.name,
            params)

        response = self.send_request(payload)
        data = response.contract_result.result
        delegation = Delegation()
        delegation.ParseFromString(data)
        return delegation

    # 08-06 查询指定世代信息
    def get_epoch_by_id(self, epoch_id: str) -> Epoch:  # ✅
        """
        查询指定世代信息
        <08-06-DPOS_STAKE-READ_EPOCH_BY_ID>
        :param epoch_id: 世代Id eg. 0
        :return:
        """
        self._debug('begin to get epoch by id %s' % epoch_id)
        params = {
            ParamKey.epoch_id.name: epoch_id
        }
        payload = self._payload_builder.create_query_payload(
            SystemContractName.DPOS_STAKE.name,
            DposStakeMethod.READ_EPOCH_BY_ID.name,
            params)
        response = self.send_request(payload)
        data = response.contract_result.result
        epoch = Epoch()
        epoch.ParseFromString(data)
        return epoch

    # 08-07 查询当前世代信息
    def get_last_epoch(self) -> Epoch:  # ✅
        """
        查询当前世代信息
        <08-07-DPOS_STAKE-READ_LATEST_EPOCH>
        :return:
        """
        self._debug('begin to get last epoch')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_STAKE.name,
                                                             DposStakeMethod.READ_LATEST_EPOCH.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        epoch = Epoch()
        epoch.ParseFromString(data)
        return epoch

    # 08-08 Stake合约中设置验证人的NodeID
    def set_node_id(self, node_id: str, timeout: int = None, with_sync_result: bool = None) -> TxResponse:  # ✅
        """
        Stake合约中设置验证人的NodeId
        <08-08-DPOS_STAKE-SET_NODE_ID>
        :param node_id: 节点Id
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        self._debug('begin to set node id')
        params = {
            ParamKey.node_id.name: node_id
        }
        payload = self._payload_builder.create_invoke_payload(
            SystemContractName.DPOS_STAKE.name,
            DposStakeMethod.SET_NODE_ID.name,
            params)
        response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return response

    # 08-09 Stake合约中查询验证人的NodeId
    def get_node_id(self, address: str) -> str:  # ✅
        """
        Stake合约中查询验证人的NodeID
        <08-09-DPOS_STAKE-GET_NODE_ID>
        :param address:
        :return:
        """
        self._debug('begin to get node id')
        params = {
            ParamKey.address.name: address
        }
        payload = self._payload_builder.create_query_payload(
            SystemContractName.DPOS_STAKE.name,
            DposStakeMethod.GET_NODE_ID.name,
            params)

        response = self.send_request(payload)
        data = response.contract_result.result
        return data.decode()

    # 08-10 更新验证人节点的最少自我抵押数量
    def create_update_min_self_delegation_payload(self, min_self_delegation: int) -> Payload:  # todo
        """
        更新验证人节点的最少自我抵押数量
        <08-10-DPOS_STAKE-UPDATE_MIN_SELF_DELEGATION>
        :return:
        """
        self._debug('begin to create [DPOS_STAKE-UPDATE_MIN_SELF_DELEGATION] to be signed payload')
        params = {
            ParamKey.min_self_delegation.name: min_self_delegation
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_STAKE.name,
                                                             DposStakeMethod.UPDATE_MIN_SELF_DELEGATION.name,
                                                             params)
        return payload

    # 08-11 查询验证人节点的最少自我抵押数量
    def get_min_self_delegation(self) -> int:  # ✅
        """
        查询验证人节点的最少自我抵押数量
        <08-11-DPOS_STAKE-READ_MIN_SELF_DELEGATION>
        :return:
        """
        self._debug('begin to get min self delegation')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_STAKE.name,
                                                             DposStakeMethod.READ_EPOCH_VALIDATOR_NUMBER.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data) if data else 0

    # 08-12 更新世代中的验证人数
    def create_update_epoch_validator_number_payload(self, epoch_validator_number: int) -> Payload:
        """
        更新世代中的验证人数
        <08-12-DPOS_STAKE-UPDATE_EPOCH_VALIDATOR_NUMBER>
        :return:
        """
        self._debug('begin to create [DPOS_STAKE-UPDATE_MIN_SELF_DELEGATION] to be signed payload')
        params = {
            ParamKey.epoch_validator_number.name: epoch_validator_number
        }
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_STAKE.name,
                                                             DposStakeMethod.UPDATE_EPOCH_BLOCK_NUMBER.name,
                                                             params)
        return payload

    # 08-13 查询世代中的验证人数
    def get_epoch_validator_number(self) -> int:  # ✅
        """
        查询世代中的验证人数
        <08-13-DPOS_STAKE-READ_EPOCH_VALIDATOR_NUMBER>
        :return:
        """
        self._debug('begin to get epoch validator number')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_STAKE.name,
                                                             DposStakeMethod.READ_EPOCH_VALIDATOR_NUMBER.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data) if data else 0

    # 08-14 更新世代中的区块数量
    def create_update_epoch_block_number_payload(self, epoch_block_number: int) -> Payload:
        """
        更新世代中的区块数量
        <08-14-DPOS_STAKE-UPDATE_EPOCH_BLOCK_NUMBER>
        :return:
        """
        self._debug('begin to create [DPOS_STAKE-UPDATE_EPOCH_BLOCK_NUMBER] to be signed payload')
        params = {
            ParamKey.epoch_block_number.name: epoch_block_number
        }
        payload = self._payload_builder.create_invoke_payload(SystemContractName.DPOS_STAKE.name,
                                                              DposStakeMethod.UPDATE_EPOCH_BLOCK_NUMBER.name, params)
        return payload

    # 08-15 查询世代中的区块数量
    def get_epoch_block_number(self) -> int:  # ✅
        """
        查询世代中的区块数量
        <08-15-DPOS_STAKE-READ_EPOCH_BLOCK_NUMBER>
        :return:
        """
        self._debug('begin to get epoch block number')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_STAKE.name,
                                                             DposStakeMethod.READ_EPOCH_BLOCK_NUMBER.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data) if data else 0

    # 08-16 查询收到解质押退款间隔的世代数
    def get_unbounding_interval_epoch_number(self) -> int:  # ✅
        """
        查询收到解质押退款间隔的世代数
        <08-16-DPOS_STAKE-READ_COMPLETE_UNBOUNDING_EPOCH_NUMBER>
        :return:
        """
        self._debug('begin to get unbounding interval epoch number')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_STAKE.name,
                                                             DposStakeMethod.READ_COMPLETE_UNBOUNDING_EPOCH_NUMBER.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return int(data) if data else 0

    # 08-17 查询Stake合约的系统地址
    def get_stake_contract_address(self) -> str:  # ✅
        """
        查询Stake合约的系统地址
        <08-18-DPOS_STAKE-READ_SYSTEM_CONTRACT_ADDR>
        :return:
        """
        self._debug('begin to get state contract address')
        payload = self._payload_builder.create_query_payload(SystemContractName.DPOS_STAKE.name,
                                                             DposStakeMethod.READ_SYSTEM_CONTRACT_ADDR.name)
        response = self.send_request(payload)
        data = response.contract_result.result
        return data.decode()

    # 08-19
    # def create_unbounding_payload(self) -> Payload:  # todo
    #     """
    #     <08-19-DPOS_STAKE-UNBOUNDING>
    #     :return:
    #     """
    #     raise NotImplementedError("待实现")
    #     self._debug('begin to create [DPOS_STAKE-UNBOUNDING] to be signed payload')
    #     params = {
    #         # todo
    #     }
    #     payload = self._payload_builder.create_invoke_payload(
    #         SystemContractName.DPOS_STAKE.name,
    #         DposStakeMethod.UNBOUNDING.name,
    #         params)
    #     return payload

    # 08-20
    def create_create_epoch_payload(self) -> Payload:
        """
        <08-20-DPOS_STAKE-CREATE_EPOCH>
        :return:
        """
        self._debug('begin to create [DPOS_STAKE-CREATE_EPOCH] to be signed payload')
        params = {
            # todo
        }
        payload = self._payload_builder.create_invoke_payload(
            SystemContractName.DPOS_STAKE.name,
            DposStakeMethod.CREATE_EPOCH.name,
            params)
        return payload

    # 08-21
    def create_update_epoch_validator_number_and_epoch_block_number_payload(self, epoch_block_number: int,
                                                                            epoch_validator_number: int) -> Payload:
        """
        <08-21-DPOS_STAKE-UPDATE_EPOCH_VALIDATOR_NUMBER_AND_EPOCH_BLOCK_NUMBER>
        :return:
        """
        self._debug('begin to create [DPOS_STAKE-UPDATE_EPOCH_VALIDATOR_NUMBER_AND_EPOCH_BLOCK_NUMBER] '
                    'to be signed payload')
        params = {
            ParamKey.epoch_block_number: epoch_block_number,
            ParamKey.epoch_validator_number.name: epoch_validator_number
        }
        payload = self._payload_builder.create_invoke_payload(
            SystemContractName.DPOS_STAKE.name,
            DposStakeMethod.UPDATE_EPOCH_VALIDATOR_NUMBER_AND_EPOCH_BLOCK_NUMBER.name,
            params)
        return payload


class DPosStakeWithEndorsers(BaseClient):
    # 08-10 更新验证人节点的最少自我抵押数量
    def set_min_self_delegation(self, min_self_delegation: int, timeout: int = None,
                                with_sync_result: bool = None) -> TxResponse:  # todo
        """
        更新验证人节点的最少自我抵押数量
        <08-10-DPOS_STAKE-UPDATE_MIN_SELF_DELEGATION>
        :param min_self_delegation: 最少自我抵押数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        payload = self.create_update_min_self_delegation_payload(min_self_delegation)
        tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return tx_response

    # 08-12 更新世代中的验证人数量
    def set_epoch_validator_number(self, epoch_validator_number: int, timeout: int = None,
                                   with_sync_result: bool = None) -> TxResponse:
        """
        更新世代中的验证人数量
        <08-12-DPOS_STAKE-UPDATE_EPOCH_VALIDATOR_NUMBER>
        :param epoch_validator_number:  世代验证者数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        payload = self.create_update_epoch_validator_number_payload(epoch_validator_number)
        tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return tx_response

    # 08-14 更新世代中的区块数量
    def set_epoch_block_number(self, epoch_block_number: int, timeout: int = None,
                               with_sync_result: bool = None) -> TxResponse:
        """
        更新世代中的区块数量
        <08-14-DPOS_STAKE-UPDATE_EPOCH_BLOCK_NUMBER>
        :param epoch_block_number: 世代区块数量
        :param timeout: RPC请求超时时间
        :param with_sync_result: 是否同步轮询交易结果
        :return: 交易响应
        """
        payload = self.create_update_epoch_block_number_payload(epoch_block_number)
        tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return tx_response

    # 08-19
    # def unbounding(self, timeout: int = None, with_sync_result: bool = None) -> TxResponse:  # todo
    #     """
    #     <08-19-DPOS_STAKE-UNBOUNDING>
    #     :param timeout: RPC请求超时时间
    #     :param with_sync_result: 是否同步轮询交易结果
    #     :return: 交易响应
    #     """
    #     raise NotImplementedError("待实现")
    #     payload = self.create_unbounding_payload()
    #     tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
    #     return tx_response

    # 08-20
    # def create_epoch(self) -> Payload:
    #     """
    #     <08-20-DPOS_STAKE-CREATE_EPOCH>
    #     :return:
    #     """
    #     raise NotImplementedError("待实现")

    # 08-21
    def set_epoch_validator_number_and_epoch_block_number(self, epoch_block_number: int,
                                                          epoch_validator_number: int, timeout: int = None,
                                                          with_sync_result: bool = None) -> Payload:
        """
        <08-21-DPOS_STAKE-UPDATE_EPOCH_VALIDATOR_NUMBER_AND_EPOCH_BLOCK_NUMBER>
        :return:
        """
        payload = self.create_update_epoch_validator_number_and_epoch_block_number_payload(epoch_block_number,
                                                                                           epoch_validator_number)
        tx_response = self.send_request_with_sync_result(payload, timeout=timeout, with_sync_result=with_sync_result)
        return tx_response
