#!/usr/bin/env python3
# -*- coding(Enum): utf-8 -*-
# Copyright (C) THL A29 Limited, a Tencent company. All rights reserved.
#
# SPDX-License-Identifier(Enum): Apache-2.0
#
# @FileName     (Enum):   keys.py
# @Function     (Enum):   默认参数及常量
from collections import namedtuple
from enum import Enum
from typing import Union

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ec, rsa

from chainmaker.utils.gm import SM2PrivateKey, SM2PublicKey

RechargeGasItem = namedtuple('RechargeGasItem', 'address amount')

CONSENSUS_TYPE_MAP = {'SOLO': 0, 'TBFT': 1, 'MAXBFT': 3, 'RAFT': 4, 'DPOS': 5, 'ABFT': 6}  # todo remove


class ConsensusType(Enum):
    """共识类型"""
    SOLO = 0
    TBFT = 1
    MAXBFT = 3
    RAFT = 4
    DPOS = 5
    ABFT = 6


class AuthType(Enum):
    """授权类型"""
    PermissionedWithCert = 'PermissionedWithCert'
    PermissionedWithKey = 'PermissionedWithKey'
    Public = 'Public'


class AlgoType(Enum):
    """公钥加密算法类型"""
    EC = 'ecc_p256'
    RSA = 'rsa2048'
    SM2 = 'sm2'
    Dilithium2 = 'dilithium2'


class HashType(Enum):
    """证书哈希算法"""
    SHA256 = 'sha256'  # default
    SHA3_256 = 'sha3_256'
    SM3 = 'sm3'


class MemberType(Enum):
    """用户证书模式"""
    CERT = 'CERT'
    CERT_HASH = 'CERT_HASH'
    ALIAS = 'ALIAS'
    PUBLIC_KEY = 'PUBLIC_KEY'


class PolicyRole(Enum):  # todo Remove
    """策略可用角色"""
    ADMIN = 'ADMIN'


class UserRole(Enum):  # todo Remove
    """用户可用角色类型"""
    LIGHT = 'LIGHT'
    ADMIN = 'ADMIN'
    CLIENT = 'CLIENT'


class Role(Enum):
    """角色类型"""
    CONSENSUS = 'CONSENSUS'
    COMMON = 'COMMON'
    LIGHT = 'LIGHT'

    ADMIN = 'ADMIN'
    CLIENT = 'CLIENT'


class PolicyRule(Enum):  # todo remove
    """访问规则"""
    ALL = 'ALL'
    ANY = 'ANY'
    MAJORITY = 'MAJORITY'
    SELF = 'SELF'
    FORBIDDEN = 'FORBIDDEN'


class Rule(Enum):
    """访问规则"""
    ALL = 'ALL'
    ANY = 'ANY'
    MAJORITY = 'MAJORITY'
    SELF = 'SELF'
    FORBIDDEN = 'FORBIDDEN'


class ContractStatus(Enum):
    """合约状态"""
    NORMAL = 0  # normal, can be invoked
    FROZEN = 1  # frozen, cannot be invoked temporarily
    REVOKED = 2  # revoked, cannot be invoked permanently


class RuntimeType(Enum):
    """虚拟机类型"""
    INVALID = 0
    NATIVE = 1  # native implement in chainmaker - go
    WASMER = 2  # vm - wasmer, language - c + +
    WXVM = 3  # vm - wxvm, language - cpp
    GASM = 4  # wasm interpreter in go
    EVM = 5  # vm - evm
    DOCKER_GO = 6  # vm - docker, language - golang
    DOCKER_JAVA = 7  # vm - java, language - java
    GO = 8  # vm - go, language - go


class AddrType(Enum):
    """地址类型"""
    CHAINMAKER = 0
    ZXL = 1
    ETHEREUM = 2  # default


class SystemContractName(Enum):
    """系统合约方法名"""
    CHAIN_CONFIG = 0  # system chain configuration contract used to add, delete and change the chain configuration
    CHAIN_QUERY = 1  # system chain query contract used to query the configuration on the chain
    CERT_MANAGE = 2  # system certificate storage contract used to manage certificates
    GOVERNANCE = 3  # governance contract  # todo
    MULTI_SIGN = 4  # multi signature contract on chain
    CONTRACT_MANAGE = 5  # manage user contract
    PRIVATE_COMPUTE = 6  # private compute contract  # todo
    DPOS_ERC20 = 7  # erc20 contract for DPoS
    DPOS_STAKE = 8  # stake contract for dpos
    SUBSCRIBE_MANAGE = 9  # subscribe block info,tx info and contract info.
    ARCHIVE_MANAGE = 10  # archive/restore block  # todo
    CROSS_TRANSACTION = 11  # cross chain transaction system contract  # todo
    PUBKEY_MANAGE = 12  # pubkey manage system contract
    ACCOUNT_MANAGER = 13  # account manager system contract
    DPOS_DISTRIBUTION = 14  # distribution for dpos  # todo
    DPOS_SLASHING = 15  # slashing for dpos  # todo
    COINBASE = 16  # coinbase manager system contract  # todo
    RELAY_CROSS = 17  # 中继跨链系统合约  # todo

    TRANSACTION_MANAGER = 18
    SNAPSHOT_MANAGE = 19
    HOT_COLD_DATA_SEPARATE_MANAGE = 20
    ETHEREUM = 21

    T = 99  # for test or debug contract code  # todo



class ChainConfigMethod(Enum):
    """0-链配置方法"""
    GET_CHAIN_CONFIG = 0  # get chain configuration
    GET_CHAIN_CONFIG_AT = 1  # get the latest configuration block the incoming block height must exist in the database
    CORE_UPDATE = 2  # switch_branch core
    BLOCK_UPDATE = 3  # switch_branch block
    TRUST_ROOT_ADD = 4  # add trusted certificate (org_id and root)
    #  [self] modify an individual's own trusted root certificate [org_id must
    #  exist in the original trust_roots,
    #  and the new root certificate must be different from other certificates]
    TRUST_ROOT_UPDATE = 5
    #  delete trusted root certificate [org_ ID should be in trust_ The nodes in
    #  nodes need to be deleted]
    TRUST_ROOT_DELETE = 6
    #  organization add node address
    #  org_id must already exist in nodes，you can add addresses in batches
    #  the parameter is addresses. Single addresses are separated by ","
    #  ip+port and peerid cannot be repeated
    #  Deprecated , replace by NODE_ID_ADD
    NODE_ADDR_ADD = 7
    #  [self]the organization updates an address
    # [org_id and address must already exist in nodes, new_address is the new
    #  address. ip+port and peerId cannot be duplicated]
    #  Deprecated , replace by NODE_ID_UPDATE
    NODE_ADDR_UPDATE = 8
    #  organization delete node address [org_id and address must already exist in
    #  nodes]
    #  Deprecated , replace by NODE_ID_DELETE
    NODE_ADDR_DELETE = 9
    #  organization add node address in batches
    #  [org_id在nodes不存在，批量添加地址，参数为node_ids，单地址用逗号","隔开。nodeId不能重复]
    NODE_ORG_ADD = 10
    #  organization switch_branch
    #  org_id must already exist in nodes，the parameter is addresses，Single
    #  addresses are separated by ","
    #  ip+port and peerid cannot be repeated
    NODE_ORG_UPDATE = 11
    NODE_ORG_DELETE = 12  # organization delete, org_id must already exist in nodes
    CONSENSUS_EXT_ADD = 13  # add consensus parameters, key is not exit in ext_config
    CONSENSUS_EXT_UPDATE = 14  # switch_branch consensus parameters, key exit in ext_config
    CONSENSUS_EXT_DELETE = 15  # delete consensus parameters, key exit in ext_config
    PERMISSION_ADD = 16  # add permission
    PERMISSION_UPDATE = 17  # switch_branch permission
    PERMISSION_DELETE = 18  # delete permission
    #  organization add node_id
    #  org_id must already exist in nodes，you can add node_id in batches
    #  the parameter is node_ids. Single node_ids are separated by ","
    #  node_id cannot be repeated
    NODE_ID_ADD = 19
    #  [self]the organization updates a node_ids
    #  [org_id and node_ids must already exist in nodes, new_node_id is the new
    #  node_id. node_id cannot be duplicated]
    NODE_ID_UPDATE = 20
    NODE_ID_DELETE = 21  # organization delete node_id [org_id and node_id must already exist in nodes]
    TRUST_MEMBER_ADD = 22  # add trusted member (org_id sign cert role  node_id)
    #  [self] modify an individual's own trusted member [node_id must exist in the original trust_members,
    #  and the new trust member must be different from other trust members]
    TRUST_MEMBER_UPDATE = 23
    #  delete trusted member certificate [node_ ID should be in trust_ The nodes in nodes need to be deleted]
    TRUST_MEMBER_DELETE = 24
    ALTER_ADDR_TYPE = 25  # alter address type
    ENABLE_OR_DISABLE_GAS = 26  # able or enable gas calc
    SET_INVOKE_BASE_GAS = 27  # set invoke base gas
    SET_ACCOUNT_MANAGER_ADMIN = 28  # set account manager admin
    PERMISSION_LIST = 29  # list permissions
    UPDATE_VERSION = 30  # switch_branch version
    MULTI_SIGN_ENABLE_MANUAL_RUN = 31  # update `enable_manual_run` flag of multi sign
    CONSENSUS_SWITCH = 32  # switch consensus algorithm
    DPOS_NODE_ID_UPDATE = 33  # switch_branch node ids in dpos
    SET_ETH_CONFIG = 34

    SET_INVOKE_GAS_PRICE = 1
    ENABLE_ONLY_CREATOR_UPGRADE = 1
    DISABLE_ONLY_CREATOR_UPGRADE = 1
    SET_INSTALL_BASE_GAS = 1
    SET_INSTALL_GAS_PRICE = 1


class ChainQueryMethod(Enum):
    """1-链查询方法"""
    GET_BLOCK_BY_TX_ID = 0  # get block by transactionId
    GET_TX_BY_TX_ID = 1  # get transaction by transactionId
    GET_BLOCK_BY_HEIGHT = 2  # get block by block height
    GET_CHAIN_INFO = 3  # get chain information, include current height and consensus node list
    GET_LAST_CONFIG_BLOCK = 4  # get the last configuration block
    GET_BLOCK_BY_HASH = 5  # get block by block hash
    GET_NODE_CHAIN_LIST = 6  # get the list of chains the node knows
    GET_GOVERNANCE_CONTRACT = 7  # get governance information
    GET_BLOCK_WITH_TXRWSETS_BY_HEIGHT = 8  # get read/write set information by height
    GET_BLOCK_WITH_TXRWSETS_BY_HASH = 9  # get read/write set information by hash
    GET_LAST_BLOCK = 10  # get the last block
    GET_FULL_BLOCK_BY_HEIGHT = 11  # get full block by height
    GET_BLOCK_HEIGHT_BY_TX_ID = 12  # get block height by tx id
    GET_BLOCK_HEIGHT_BY_HASH = 13  # get block height by hash
    GET_BLOCK_HEADER_BY_HEIGHT = 14  # get block header by height
    GET_ARCHIVED_BLOCK_HEIGHT = 15  # get archived block height
    GET_ALL_CONTRACTS = 16  # get all contract info list
    GET_MERKLE_PATH_BY_TX_ID = 17  # get merkle path by tx id

    GET_ARCHIVE_STATUS = None


class CertManageMethod(Enum):
    """2-证书管理方法"""
    CERT_ADD = 0  # add one certificate
    CERTS_DELETE = 1  # delete certificates
    CERTS_QUERY = 2  # query certificates
    CERTS_FREEZE = 3  # freeze certificates
    CERTS_UNFREEZE = 4  # unfreeze certificates
    CERTS_REVOKE = 5  # revoke certificates
    CERT_ALIAS_ADD = 6  # add one certificate alias, any
    CERT_ALIAS_UPDATE = 7  # switch_branch one certificate alias, self
    CERTS_ALIAS_DELETE = 8  # delete certificate alias, admin
    CERTS_ALIAS_QUERY = 9  # query certificate alias, admin


class CoinBaseMethod(Enum):
    """CoinBase方法"""
    RUN_COINBASE = 0


class GovernanceMethod(Enum):
    """3-统治方法"""


class MultiSignMethod(Enum):
    """4-多签方法"""
    REQ = 0  # multi signature request
    VOTE = 1  # multi signature voting
    QUERY = 2  # multi signature query
    TRIG = 3  # multi signature execute


class ContractManageMethod(Enum):
    """05-合约管理方法"""
    INIT_CONTRACT = 0  # init contract
    UPGRADE_CONTRACT = 1  # upgrade contract version
    FREEZE_CONTRACT = 2  # freeze contract, cannot be invoked temporarily
    UNFREEZE_CONTRACT = 3  # unfreeze contract to normal status
    REVOKE_CONTRACT = 4  # revoke contract, cannot be invoked permanently
    GRANT_CONTRACT_ACCESS = 5  # grant access to a native contract
    REVOKE_CONTRACT_ACCESS = 6  # revoke access to a native contract
    VERIFY_CONTRACT_ACCESS = 7  # verify if has access to a certain native contract
    INIT_NEW_NATIVE_CONTRACT = 8  # initial new chain maker version native contract list


class ContractQueryMethod(Enum):
    """合约查询方法"""
    GET_CONTRACT_INFO = 0  # get contract information
    GET_CONTRACT_BYTECODE = 1  # get contract bytecode
    GET_CONTRACT_LIST = 2  # get all installed contract
    GET_DISABLED_CONTRACT_LIST = 3  # get native contract list has access to


class PrivateComputeMethod(Enum):  # todo
    """06-隐私计算方法"""
    GET_CONTRACT = 0  # get contract code
    GET_DATA = 1  # get private data
    SAVE_CA_CERT = 2  # save cert of tee
    SAVE_DIR = 3  # save private data dir
    SAVE_DATA = 4  # save data of private computation result
    SAVE_ENCLAVE_REPORT = 5  # save enclave report
    GET_ENCLAVE_PROOF = 6  # get enclave proof
    GET_CA_CERT = 7  # get cert of tee
    GET_DIR = 8  # get private data dir
    CHECK_CALLER_CERT_AUTH = 9  # check caller cert auth
    GET_ENCLAVE_ENCRYPT_PUB_KEY = 10
    GET_ENCLAVE_VERIFICATION_PUB_KEY = 11
    GET_ENCLAVE_REPORT = 12
    GET_ENCLAVE_CHALLENGE = 13
    GET_ENCLAVE_SIGNATURE = 14
    SAVE_REMOTE_ATTESTATION = 15


class DposErc20Method(Enum):
    """07-Dpos Erc20操作方法"""
    GET_OWNER = 0  # get owner of DPoS
    GET_DECIMALS = 1  # get decimals of DPoS
    TRANSFER = 2  # transfer token at DPoS
    TRANSFER_FROM = 3  # transfer token from user at DPoS
    GET_BALANCEOF = 4  # get balance of user at DPoS
    APPROVE = 5  # approve token for user to other user at DPoS
    GET_ALLOWANCE = 6  # get allowance at DPoS
    BURN = 7  # burn token at DPoS
    MINT = 8  # mint token at DPoS
    TRANSFER_OWNERSHIP = 9  # transfer owner ship at DPoS
    GET_TOTAL_SUPPLY = 10  # get total supply of tokens


class DposStakeMethod(Enum):
    """08-Dpos Stake操作方法"""
    GET_ALL_CANDIDATES = 0  # get all validator candidates
    GET_VALIDATOR_BY_ADDRESS = 1  # get validator by address
    DELEGATE = 2  # delegate
    GET_DELEGATIONS_BY_ADDRESS = 3  # get delegate by address
    GET_USER_DELEGATION_BY_VALIDATOR = 4  # get user delegation by validator
    UNDELEGATE = 5  # undelegate
    READ_EPOCH_BY_ID = 6  # read epoch by id
    READ_LATEST_EPOCH = 7  # read latest epoch
    SET_NODE_ID = 8  # set node id before join network
    GET_NODE_ID = 9  # get node id after join network
    UPDATE_MIN_SELF_DELEGATION = 10  # switch_branch min self delegation
    READ_MIN_SELF_DELEGATION = 11  # read min self delegation
    UPDATE_EPOCH_VALIDATOR_NUMBER = 12  # switch_branch epoch validator number
    READ_EPOCH_VALIDATOR_NUMBER = 13  # read epoch validator number
    UPDATE_EPOCH_BLOCK_NUMBER = 14  # switch_branch epoch block number
    READ_EPOCH_BLOCK_NUMBER = 15  # read epoch block number
    READ_COMPLETE_UNBOUNDING_EPOCH_NUMBER = 16  # read complete unbounding epoch number
    READ_SYSTEM_CONTRACT_ADDR = 18  # read system contract address
    UNBOUNDING = 19  # unbounding
    CREATE_EPOCH = 20  # create epoch
    UPDATE_EPOCH_VALIDATOR_NUMBER_AND_EPOCH_BLOCK_NUMBER = 21  # switch_branch epoch validator num and block num


class SubscribeManageMethod(Enum):
    """09-订阅管理方法"""
    SUBSCRIBE_BLOCK = 0
    SUBSCRIBE_TX = 1
    SUBSCRIBE_CONTRACT_EVENT = 2


class ArchiveManageMethod(Enum):
    """10-系统合约归档方法"""
    ARCHIVE_BLOCK = 0
    RESTORE_BLOCK = 1


class CrossTransactionMethod(Enum):  # todo
    """11-跨链交易方法"""
    EXECUTE = 0  # transaction execute
    COMMIT = 1  # transaction commit
    ROLLBACK = 2  # transaction rollback
    READ_STATE = 3  # read cross id state
    SAVE_PROOF = 4  # save cross other transaction proof
    READ_PROOF = 5  # read cross other transaction proof
    ARBITRATE = 6  # arbitrate the cross transaction


class PubkeyManageMethod(Enum):
    """12-公钥管理方法"""
    PUBKEY_ADD = 0  # add one pubkey
    PUBKEY_DELETE = 1  # delete pubkeys
    PUBKEY_QUERY = 2  # query pubkeys


class RelayCrossMethod(Enum):  # todo
    """17-中继跨链方法"""
    SAVE_GATEWAY = 0  # save gateway
    UPDATE_GATEWAY = 1  # switch_branch gateway
    SAVE_CROSS_CHAIN_INFO = 2  # save cross chain info
    GET_ERROR_CROSS_CHAIN_TX_LIST = 3  # get error cross chain transaction list
    DELETE_ERROR_CROSS_CHAIN_TX_LIST = 4  # delete error cross chain transaction list
    UPDATE_CROSS_CHAIN_TRY = 5  # switch_branch cross chain try
    UPDATE_CROSS_CHAIN_RESULT = 6  # switch_branch cross chain result
    UPDATE_CROSS_CHAIN_CONFIRM = 7  # switch_branch cross chain confirm
    UPDATE_SRC_GATEWAY_CONFIRM = 8  # switch_branch source gateway confirm
    GET_GATEWAY_NUM = 9  # get gateway number
    GET_GATEWAY = 10  # get gateway
    GET_GATEWAY_BY_RANGE = 11  # get gateway by range
    GET_CROSS_CHAIN_NUM = 12  # get cross chain number
    GET_CROSS_CHAIN_INFO = 13  # get cross chain information
    GET_CROSS_CHAIN_INFO_BY_RANGE = 14  # get cross chain information by range
    GET_NOT_END_CROSS_CHIAN_ID_LIST = 15  # get not end cross chain id list


class AccountManagerMethod(Enum):
    """13-Gas账户管理方法"""
    SET_ADMIN = 0  # set admin   todo
    GET_ADMIN = 1  # get admin
    RECHARGE_GAS = 2  # recharge gas
    GET_BALANCE = 3  # get balance
    CHARGE_GAS = 4  # charge gas
    FROZEN_ACCOUNT = 5  # frozen account
    UNFROZEN_ACCOUNT = 6  # unfrozen account
    ACCOUNT_STATUS = 7  # account status
    REFUND_GAS = 8  # refund gas
    REFUND_GAS_VM = 9  # refund gas for vm
    CHARGE_GAS_FOR_MULTI_ACCOUNT = 10  # charge gas for multi accounts


class DposConfigMethod(Enum):  # todo
    """Dpos配置方法"""
    GET_DPOS_CONFIG = 0  # get dpos config
    UPDATE_DPOS_CONFIG = 1  # switch_branch dpos config


class DposDistributionMethod(Enum):  # todo
    """14-Dpos分发方法"""
    REWARD = 0  # Reward for Distribution
    GET_DISTRIBUTION_DETAIL = 1  # Get Distribution Detail for Every Delegator
    SET_DISTRIBUTION_PER_BLOCK = 2  # Set Distribution per block
    GET_DISTRIBUTION_PER_BLOCK = 3  # Get Distribution per Block
    SET_DISTRIBUTION_FROM_SLASHING = 4  # Set Distribution from Slashing
    GET_DISTRIBUTION_FROM_SLASHING = 5  # Get Distribution from Slashing
    SET_GAS_EXCHANGE_RATE = 6  # Set Gas Exchange Rate
    GET_GAS_EXCHANGE_RATE = 7  # Get Gas Exchange Rate


class DposSlashingMethod(Enum):  # todo
    """15-Dpos开叉方法"""
    PUNISH = 0  # Punish for Slashing
    SET_SLASHING_PER_BLOCK = 2  # Set Slashing per block
    GET_SLASHING_PER_BLOCK = 3  # Get Slashing per Block
    GET_SLASHING_ADDRESS_BALANCE = 4  # Get Slashing address balance
    GET_SLASHING_DETAIL = 5  # Get Slashing Detail
    GET_SLASHING_ADDRESS = 6

class TransactionManagerMethod:
    ADD_BLACKLIST_TX_IDS = 0
    DELETE_BLACKLIST_TX_IDS = 1
    GET_BLACKLIST_TX_IDS = 2

class TMethod(Enum):  # todo
    """99-测试调试合约代码方法"""
    P = 0  # put data, parameters: k,v
    G = 1  # get data parameter: k
    N = 2  # nothing to do.
    D = 3  # delete data by key, parameter: k


# 所有系统合约方法
SystemMethod = Union[
    ChainConfigMethod, ChainQueryMethod, CertManageMethod, GovernanceMethod, MultiSignMethod,
    ContractManageMethod,
    ContractQueryMethod,
    PrivateComputeMethod, SubscribeManageMethod,
    ArchiveManageMethod, CrossTransactionMethod, PubkeyManageMethod, AccountManagerMethod,
    DposErc20Method, DposStakeMethod, DposConfigMethod, DposSlashingMethod,
    CoinBaseMethod, TMethod]


class ParamKey(Enum):
    """参数键名"""
    block_height = 'block_height'
    org_id = 'org_id'
    root = 'root'
    node_id = 'node_id'
    node_addr = 'node_addr'
    new_node_id = 'new_node_id'
    new_node_addr = 'new_node_addr'
    node_ids = 'node_ids'
    node_addrs = 'node_addrs'
    member_info = 'member_info'
    role = 'role'
    pubkey = 'pubkey'
    tx_scheduler_timeout = 'tx_scheduler_timeout'
    tx_scheduler_validate_timeout = 'tx_scheduler_validate_timeout'
    tx_timestamp_verify = 'tx_timestamp_verify'
    tx_timeout = 'tx_timeout'
    block_tx_capacity = 'block_tx_capacity'
    block_size = 'block_size'
    block_interval = 'block_interval'
    tx_parameter_size = 'tx_parameter_size'
    addr_type = 'addr_type'

    NATIVE_CONTRACT_NAME = 'NATIVE_CONTRACT_NAME'
    CONTRACT_NAME = 'CONTRACT_NAME'
    txId = 'txId'
    blockHeight = 'blockHeight'
    blockHash = 'blockHash'
    withRWSet = 'withRWSet'
    START_BLOCK = 'START_BLOCK'
    END_BLOCK = 'END_BLOCK'
    WITH_RWSET = 'WITH_RWSET'
    ONLY_HEADER = 'ONLY_HEADER'
    TX_IDS = 'TX_IDS'
    TOPIC = 'TOPIC'
    VOTE_INFO = 'VOTE_INFO'
    TX_ID = 'TX_ID'
    SYS_CONTRACT_NAME = 'SYS_CONTRACT_NAME'
    SYS_METHOD = 'SYS_METHOD'
    CONTRACT_VERSION = 'CONTRACT_VERSION'
    CONTRACT_BYTECODE = 'CONTRACT_BYTECODE'
    CONTRACT_RUNTIME_TYPE = 'CONTRACT_RUNTIME_TYPE'
    BLOCK_HEIGHT = 'BLOCK_HEIGHT'
    FULL_BLOCK = 'FULL_BLOCK'

    batch_recharge = 'batch_recharge'
    address_key = 'address_key'
    charge_gas_amount = 'charge_gas_amount'
    alias = 'alias'
    aliases = 'aliases'
    cert = 'cert_or_cert_bytes'

    set_invoke_base_gas = 'set_invoke_base_gas'
    to = 'to'
    value = 'value'
    address = 'address'
    amount = 'amount'
    delegator_address = 'delegator_address'
    validator_address = 'validator_address'
    _from = 'from'
    epoch_id = 'epoch_id'
    cert_hashes = 'cert_hashes'
    certs = 'certs'
    cert_crl = 'cert_crl'
    enable_optimize_charge_gas = 'enable_optimize_charge_gas'
    owner = 'owner'
    block_version = 'block_version'
    ext_config = 'ext_config'
    # 隐私计算 keys
    order_id = 'order_id'
    private_dir = 'private_dir'
    contract_name = 'contract_name'
    code_hash = 'code_hash'
    result = 'result'
    code_header = 'code_header'
    version = 'version'
    is_deploy = 'is_deploy'
    rw_set = 'rw_set'
    report_hash = 'report_hash'
    sign = 'sign'
    key = 'key'
    payload = 'payload'
    org_ids = 'org_ids'
    sign_pairs = 'sign_pairs'
    ca_cert = 'ca_cert'
    enclave_id = 'enclave_id'
    report = 'report'
    proof = 'proof'
    deploy_req = 'deploy_req'
    private_req = 'private_req'

    multi_sign_enable_manual_run = 'multi_sign_enable_manual_run'

    epoch_block_number = 'epoch_block_number'
    epoch_validator_number = 'epoch_validator_number'
    distribution_per_block = 'distribution_per_block'
    gas_exchange_rate = 'gas_exchange_rate'
    slashing_per_block = 'slashing_per_block'
    min_self_delegation = 'min_self_delegation'

    set_install_base_gas = 'set_install_base_gas'
    set_invoke_gas_price = 'set_invoke_gas_price'
    set_install_gas_price = 'set_install_gas_price'


class VoteStatus(Enum):
    """投票状态"""
    AGREE = 0  # 同意
    REJECT = 1  # 拒绝


class MultiSignStatus(Enum):
    """多签状态"""
    PROCESSING = 0
    ADOPTED = 1
    REFUSED = 2
    FAILED = 3
    PASSED = 4




class ArchiveDB:
    MysqlDBNamePrefix = "cm_archived_chain"
    MysqlTableNamePrefix = "t_block_info"
    RowsPerBlockInfoTable = 10000  # v2.3.2 修改
    QUERY_FULL_BLOCK_BY_HEIGHT_SQL = 'SELECT Fblock_with_rwset, Fhmac from %s WHERE Fblock_height=%s'
    MysqlSysInfoTable = 'sysinfo'  # v2.3.2 新增
    MysqlTableCharset = 'utf8mb4'  # v2.3.2 新增
    MySqlTableCollate = 'utf8mb4_unicode_ci'  # v2.3.2 新增



class ChainConfigCoreKey(Enum):
    txSchedulerTimeout = "txSchedulerTimeout"
    txSchedulerValidateTimeout = "txSchedulerValidateTimeout"
    consensusTurboConfig = "consensusTurboConfig"
    enableConflictsBitWindow = "enableConflictsBitWindow"


class ChainConfigBlockKey(Enum):
    txTimestampVerify = 'txTimestampVerify'
    txTimeout = 'txTimeout'
    blockTxCapacity = 'blockTxCapacity'
    blockSize = 'blockSize'
    blockInterval = 'blockInterval'


class ResourceName(Enum):
    """权限资源名称"""
    CHAIN_CONFIG_CORE_UPDATE = 'CHAIN_CONFIG-CORE_UPDATE'
    CHAIN_CONFIG_BLOCK_UPDATE = 'CHAIN_CONFIG-BLOCK_UPDATE'
    CHAIN_CONFIG_TRUST_ROOT_ADD = 'CHAIN_CONFIG-TRUST_ROOT_ADD'
    CHAIN_CONFIG_TRUST_ROOT_UPDATE = 'CHAIN_CONFIG-TRUST_ROOT_UPDATE'
    CHAIN_CONFIG_TRUST_ROOT_DELETE = 'CHAIN_CONFIG-TRUST_ROOT_DELETE'
    CHAIN_CONFIG_TRUST_MEMBER_ADD = 'CHAIN_CONFIG-TRUST_MEMBER_ADD'
    CHAIN_CONFIG_TRUST_MEMBER_UPDATE = 'CHAIN_CONFIG-TRUST_MEMBER_UPDATE'
    CHAIN_CONFIG_TRUST_MEMBER_DELETE = 'CHAIN_CONFIG-TRUST_MEMBER_DELETE'
    CHAIN_CONFIG_NODE_ADDR_ADD = 'CHAIN_CONFIG-NODE_ADDR_ADD'
    CHAIN_CONFIG_NODE_ADDR_UPDATE = 'CHAIN_CONFIG-NODE_ADDR_UPDATE'
    CHAIN_CONFIG_NODE_ADDR_DELETE = 'CHAIN_CONFIG-NODE_ADDR_DELETE'
    CHAIN_CONFIG_NODE_ORG_ADD = 'CHAIN_CONFIG-NODE_ORG_ADD'
    CHAIN_CONFIG_NODE_ORG_UPDATE = 'CHAIN_CONFIG-NODE_ORG_UPDATE'
    CHAIN_CONFIG_NODE_ORG_DELETE = 'CHAIN_CONFIG-NODE_ORG_DELETE'
    CHAIN_CONFIG_CONSENSUS_EXT_ADD = 'CHAIN_CONFIG-CONSENSUS_EXT_ADD'
    CHAIN_CONFIG_CONSENSUS_EXT_UPDATE = 'CHAIN_CONFIG-CONSENSUS_EXT_UPDATE'
    CHAIN_CONFIG_CONSENSUS_EXT_DELETE = 'CHAIN_CONFIG-CONSENSUS_EXT_DELETE'
    CHAIN_CONFIG_PERMISSION_ADD = 'CHAIN_CONFIG-PERMISSION_ADD'
    CHAIN_CONFIG_PERMISSION_UPDATE = 'CHAIN_CONFIG-PERMISSION_UPDATE'
    CHAIN_CONFIG_PERMISSION_DELETE = 'CHAIN_CONFIG-PERMISSION_DELETE'
    CHAIN_CONFIG_NODE_ID_ADD = 'CHAIN_CONFIG-NODE_ID_ADD'
    CHAIN_CONFIG_NODE_ID_UPDATE = 'CHAIN_CONFIG-NODE_ID_UPDATE'
    CHAIN_CONFIG_NODE_ID_DELETE = 'CHAIN_CONFIG-NODE_ID_DELETE'

    CERT_MANAGE_CERTS_DELETE = 'CERT_MANAGE-CERTS_DELETE'
    CERT_MANAGE_CERTS_FREEZE = 'CERT_MANAGE-CERTS_FREEZE'
    CERT_MANAGE_CERTS_UNFREEZE = 'CERT_MANAGE-CERTS_UNFREEZE'
    CERT_MANAGE_CERTS_REVOKE = 'CERT_MANAGE-CERTS_REVOKE'
    CERT_MANAGE_CERT_ALIAS_UPDATE = 'CERT_MANAGE-CERT_ALIAS_UPDATE'
    CERT_MANAGE_CERTS_ALIAS_DELETE = 'CERT_MANAGE-CERTS_ALIAS_DELETE'

    CONTRACT_MANAGE_INIT_CONTRACT = 'CONTRACT_MANAGE-INIT_CONTRACT'
    CONTRACT_MANAGE_UPGRADE_CONTRACT = 'CONTRACT_MANAGE-UPGRADE_CONTRACT'
    CONTRACT_MANAGE_FREEZE_CONTRACT = 'CONTRACT_MANAGE-FREEZE_CONTRACT'
    CONTRACT_MANAGE_UNFREEZE_CONTRACT = 'CONTRACT_MANAGE-UNFREEZE_CONTRACT'
    CONTRACT_MANAGE_REVOKE_CONTRACT = 'CONTRACT_MANAGE-REVOKE_CONTRACT'

    PRIVATE_COMPUTE_SAVE_CA_CERT = 'PRIVATE_COMPUTE-SAVE_CA_CERT'
    PRIVATE_COMPUTE_SAVE_ENCLAVE_REPORT = 'PRIVATE_COMPUTE-SAVE_ENCLAVE_REPORT'


class ChainMakerVersion(Enum):
    """长安链版本"""
    v1_0_0 = 'v1.0.0'
    v1_1_0 = 'v1.1.0'
    v1_1_1 = 'v1.1.1'
    v1_2_0 = 'v1.2.0'
    v1_2_3 = 'v1.2.3'
    v1_2_4 = 'v1.2.4'
    v1_2_5 = 'v1.2.5'
    v1_2_6 = 'v1.2.6'

    v2_0_0 = 'v2.0.0'
    v2_1_0 = 'v2.1.0'
    v2_2_0 = 'v2.2.0'
    v2_2_1 = 'v2.2.1'
    v2_2_2 = 'v2.2.2'
    v2_2_3 = 'v2.2.3'
    v2_2_4 = 'v2.2.4'

    v2_3_0 = 'v2.3.0'
    v2_3_1 = 'v2.3.1'
    v2_4_0 = 'v2.4.0'
    v3_0_0 = 'v3.0.0'


class CryptoEngine(Enum):
    """国密引擎"""
    tjfoc = 'tjfoc'  # default
    gmssl = 'gmssl'
    tencentsm = 'tencentsm'


class NetProvider(Enum):
    """网络模式"""
    LibP2P = 'LibP2P'  # default
    Liquid = 'Liquid'


class RpcTlsMode(Enum):
    """chainmaker.yml RPC TLS模式"""
    twoway = 'twoway'  # default
    oneway = 'oneway'
    disable = 'disable'


class DbType(Enum):
    """chainmaker数据库类型"""
    blockdb = 'blockdb'  # 允许 # 1. leveldb; 2. mysql; 3. badgerdb; 4. tikvdb; 5. 文件存储；6. sqlkv(优先级低)
    statedb = 'statedb'  # 允许  # 1.leveldb; 2. mysql; 3. badgerdb; 4. tikvdb; 5. sqlkv
    historydb = 'historydb'  # 允许 # 1. leveldb; 2. mysql; 3. badgerdb; 4. tikvdb; 5. disable; 6. sqlkv(优先级低)
    resultdb = 'resultdb'  # 允许  # 1. leveldb; 2. mysql; 3. badgerdb; 4. tikvdb; 5. disable; 6. sqlkv(优先级低)
    contract_eventdb = 'contract_eventdb'  # 允许  # 1. mysql; 2. disable


class DbProvider(Enum):
    """chainmaker.yml 数据引擎类型"""
    leveldb = 'leveldb'  # default
    mysql = 'mysql'  # sql类型
    badgerdb = 'badgerdb'
    tikvdb = 'tikvdb'
    sqlkv = 'sqlkv'
    disable = 'disable'


class TxFilterType(Enum):
    """"""
    store = 0  # default  disabled
    birds_nest = 1
    map = 2
    sharding_birds_nest = 3  # enabled


class ResultMessageType(Enum):
    """返回消息类型"""
    MESSAGE = 'MESSAGE'  # default
    DICT = 'DICT'
    JSON = 'JSON'


class ResultType(Enum):
    """返回结果类型"""
    ORIGIN = 'ORIGIN'  # default
    RESULT_OR_ERR_MSG = 'RESULT_OR_ERR_MSG'
    RESULT_AND_ERR_MSG = 'RESULT_AND_ERR_MSG'


class ContractResultType(Enum):
    """合约结果类型"""
    STRING = 0
    INT = 1
    JSON = 2
    HEX = 3


# # 私钥类型
# PrivateKey = Union[rsa.RSAPrivateKey, ec.EllipticCurvePrivateKey]
# # 公钥类型
# PublicKey = Union[rsa.RSAPublicKey, ec.EllipticCurvePublicKey]

PublicKey = Union[ec.EllipticCurvePublicKey, rsa.RSAPublicKey, SM2PublicKey]
PrivateKey = Union[ec.EllipticCurvePrivateKey, rsa.RSAPrivateKey, SM2PrivateKey]

# 证书类型
Certificate = x509.Certificate


class TxType(Enum):
    """交易池交易类型"""
    UNKNOWN_TYPE = 0
    CONFIG_TX = 1
    COMMON_TX = 2
    ALL_TYPE = 3


class TxStage(Enum):
    """交易池交易状态"""
    UNKNOWN_STAGE = 0
    IN_QUEUE = 1
    IN_PENDING = 2
    ALL_STAGE = 3


class TxPoolType(Enum):
    """交易池类型"""
    normal = 0
    single = 1
    batch = 2


class ArchiveType(Enum):
    mysql = "mysql"
    archivecenter = "archivecenter"
