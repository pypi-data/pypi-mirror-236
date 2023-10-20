import abc
import os
import re
from pathlib import Path
from typing import Union, List, Dict

from cryptography.hazmat._oid import NameOID

from chainmaker.chain_client import ChainClientWithEndorsers
from chainmaker.keys import AddrType, HashType, PublicKey, PrivateKey, AuthType
from chainmaker.sdk_config import DefaultConfig
from chainmaker.utils import address_utils, crypto_utils

DEFAULT_TLS_HOME_NAME = 'chainmaker.org'
DEFAULT_ARCHIVE_CONFIG = {'dest': 'root:passw0rd:localhost:3306', 'secret_key': 'passw0rd', 'type': 'mysql'}
DEFAULT_RPC_CLIENT_CONFIG = {'rpc_max_send_message_length': DefaultConfig.rpc_max_send_message_length,
                             'rpc_max_receive_message_length': DefaultConfig.rpc_max_receive_message_length}
DEFAULT_PKCS_CONFIG = None


def guess_role(crypto_dir_name: str) -> str:
    role = re.sub(r'\d+', '', crypto_dir_name)
    if role == 'node':
        role = 'consensus'
    assert role in ['admin', 'client', 'light', 'common', 'consensus']
    return role.upper()


def get_user_prefix(org_id_or_node_name: str) -> str:
    matched = re.search(r'org\d+', org_id_or_node_name)
    if matched:
        return matched.group()

    matched = re.search(r'node\d+', org_id_or_node_name)
    if matched:
        return matched.group()

    matched = re.search(r'org', org_id_or_node_name)
    if matched:
        return ''
    return org_id_or_node_name


def guess_auth_type(crypto_config_path: Union[Path, str]) -> AuthType:
    for sub_dir in os.listdir(crypto_config_path):
        if sub_dir.startswith('node'):
            return AuthType.Public
        if 'admin' in os.listdir(f'{crypto_config_path}/{sub_dir}'):
            return AuthType.PermissionedWithKey
        return AuthType.PermissionedWithCert


class _WithNodeIdFile:
    node_id_file_path: Union[Path, str]

    @property
    def node_id(self) -> str:
        with open(self.node_id_file_path) as f:
            return f.read()


class _WithPubkeyFile:
    pubkey_file_path: Union[Path, str]

    @property
    def pubkey_bytes(self) -> bytes:
        with open(self.pubkey_file_path, 'rb') as f:
            return f.read()

    @property
    def pubkey(self) -> str:
        return self.pubkey_bytes.decode()


class _WithAddrFile:
    addr_file_path: Union[Path, str]

    @property
    def address(self) -> str:
        with open(self.addr_file_path) as f:
            return f.read()


class _WithTlsKeyFileAndTlsCertFile:
    tls_key_file_path: Union[Path, str]
    tls_cert_file_path: Union[Path, str]
    tls_key_pwd: str = None

    @property
    def tls_key_bytes(self) -> bytes:
        with open(self.tls_key_file_path, 'rb') as f:
            return f.read()

    @property
    def tls_cert_bytes(self) -> bytes:
        with open(self.tls_cert_file_path, 'rb') as f:
            return f.read()


class _WithEncKeyFileAndEncCertFile:
    enc_key_file_path: Union[Path, str]
    enc_cert_file_path: Union[Path, str]
    enc_key_pwd: str = None

    @property
    def enc_key_bytes(self) -> bytes:
        with open(self.enc_key_file_path, 'rb') as f:
            return f.read()

    @property
    def enc_cert_bytes(self) -> bytes:
        with open(self.enc_cert_file_path, 'rb') as f:
            return f.read()


class _WithOrgCaKeyFileAndOrgCaCertFile:
    trust_root_path: Union[Path, str]
    org_ca_key_file_path: Union[Path, str]
    org_ca_cert_file_path: Union[Path, str]

    @property
    def org_ca_key_bytes(self) -> bytes:
        with open(self.org_ca_key_file_path, 'rb') as f:
            return f.read()

    @property
    def org_ca_cert_bytes(self) -> bytes:
        with open(self.org_ca_cert_file_path, 'rb') as f:
            return f.read()

    @property
    def trust_root_crt(self) -> str:
        return self.org_ca_cert_bytes.decode()


class _WithAdminKeyFileAndAndPubkeyFile:
    admin_key_fle: Union[Path, str]
    admin_pubkey_fle: Union[Path, str]

    @property
    def admin_key_bytes(self) -> bytes:
        with open(self.admin_key_fle, 'rb') as f:
            return f.read()

    @property
    def admin_pubkey_bytes(self) -> bytes:
        with open(self.admin_pubkey_fle, 'rb') as f:
            return f.read()


class _Base:
    name: str
    role: str
    org_id: str
    sign_key_file_path: Union[Path, str]
    sign_key_pwd: str = None

    def __init__(self, name: str, role: str, org_id: str,
                 sign_key_file_path: Union[Path, str], sign_cert_file_path: Union[Path, str] = None,
                 tls_key_file_path: Union[Path, str] = None, tls_cert_file_path: Union[Path, str] = None,
                 enc_key_file_path: Union[Path, str] = None, enc_cert_file_path: Union[Path, str] = None,
                 node_id_file_path: Union[Path, str] = None,
                 pubkey_file_path: Union[Path, str] = None,
                 addr_file_path: Union[Path, str] = None,
                 org_ca_dir: Union[Path, str] = None):

        self.name = name
        self.role = role
        self.org_id = org_id
        self.sign_key_file_path = sign_key_file_path

        if sign_cert_file_path:
            self.sign_cert_file_path = sign_cert_file_path
        if tls_key_file_path:
            self.tls_key_file_path = tls_key_file_path
        if tls_cert_file_path:
            self.tls_cert_file_path = tls_cert_file_path
        if enc_key_file_path:
            self.enc_key_file_path = enc_key_file_path
        if enc_cert_file_path:
            self.enc_cert_file_path = enc_cert_file_path
        if node_id_file_path:
            self.node_id_file_path = node_id_file_path
        if pubkey_file_path:
            self.pubkey_file_path = pubkey_file_path
        if addr_file_path:
            self.addr_file_path = addr_file_path
        if org_ca_dir:
            self.trust_root_path = org_ca_dir
            self.org_ca_cert_file_path = f'{org_ca_dir}/ca.crt'
            self.org_ca_key_file_path = f'{org_ca_dir}/ca.key'

    @property
    def sign_key_bytes(self) -> bytes:
        with open(self.sign_key_file_path, 'rb') as f:
            return f.read()

    @property
    def _private_key(self) -> PrivateKey:  # sign_key
        """用户签名私钥对象, 即sign_key"""
        return crypto_utils.load_pem_private_key(self.sign_key_bytes, password=self.sign_key_pwd)

    @property
    def _public_key(self) -> PublicKey:
        """用户签名公钥对象"""
        return self._private_key.public_key()

    @property
    def uid(self) -> str:
        """
        用户Id, 即ski(subject key identifier)
        :return: hex字符串
        """
        return address_utils.get_ski_from_public_key(self._public_key)

    def get_address(self, addr_type: int = 2, hash_type: str = 'SHA256') -> str:
        if hasattr(self, 'address'):
            return getattr(self, 'address')

        addr_type = AddrType(addr_type)
        if hasattr(self, 'sign_cert_bytes'):
            return address_utils.get_address_from_cert_bytes(getattr(self, 'sign_cert_bytes'), addr_type=addr_type)

        hash_type = HashType[hash_type]
        return address_utils.public_key_to_addr(self._public_key, hash_type, addr_type)


class _Pk(_WithPubkeyFile):
    def create_client_user_config(self, hash_type: str = 'sha256') -> dict:
        return {'auth_type': 'public',
                'user_sign_key_file_path': self.sign_key_file_path,
                'crypto': {'hash': hash_type}}


class _Pwk(_WithPubkeyFile, _WithAdminKeyFileAndAndPubkeyFile):
    def create_client_user_config(self, hash_type: str = 'sha256') -> dict:
        return {'org_id': self.org_id,
                'auth_type': 'permissionedWithKey',
                'crypto': {'hash': hash_type},
                'user_sign_key_file_path': self.sign_key_file_path}


class _Cert(_WithTlsKeyFileAndTlsCertFile, _WithEncKeyFileAndEncCertFile, _WithOrgCaKeyFileAndOrgCaCertFile):
    sign_cert_file_path: Union[Path, str]
    tls_key_file_path: Union[Path, str]
    tls_cert_file_path: Union[Path, str]

    def create_client_user_config(self, hash_type: str = 'sha256') -> dict:
        return {'org_id': self.org_id,
                'user_sign_key_file_path': self.sign_key_file_path,
                'user_sign_crt_file_path': self.sign_cert_file_path,
                'user_crt_file_path': self.tls_cert_file_path,
                'user_key_file_path': self.tls_key_file_path}

    @property
    def sign_cert_bytes(self) -> bytes:
        with open(self.sign_cert_file_path, 'rb') as f:
            return f.read()

    @property
    def tls_key_bytes(self) -> bytes:
        with open(self.tls_key_file_path, 'rb') as f:
            return f.read()

    @property
    def tls_cert_bytes(self) -> bytes:
        with open(self.tls_cert_file_path, 'rb') as f:
            return f.read()

    @property
    def _cert(self):
        if hasattr(self, 'sign_cert_bytes'):
            return crypto_utils.load_pem_cert(getattr(self, 'sign_cert_bytes'))

    @property
    def member_id(self) -> Union[str, None]:
        """从用户(签名)证书中获取用户通用名称"""
        if self._cert:
            return self._cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

    @property
    def cert_hash(self) -> str:
        if self._cert:
            return crypto_utils.get_cert_hash_bytes(self._cert).hex()


class _UserBase(_Base):
    def __repr__(self):
        return f'<User {self.name}>'


class _NodeBase(_Base, _WithNodeIdFile):
    def __repr__(self):
        return f'<Node {self.name}>'


class PkUser(_UserBase, _Pk, _WithAddrFile):

    @classmethod
    def from_dir(cls, crypto_dir: Path, org_id_or_node_name: str):
        crypto_dir_name = os.path.basename(crypto_dir)
        role = guess_role(crypto_dir_name)
        name = f'{get_user_prefix(org_id_or_node_name)}{crypto_dir_name}'
        org_id = 'public'
        return cls(name, role, org_id,
                   sign_key_file_path=str(crypto_dir / f'{crypto_dir_name}.key'),
                   pubkey_file_path=str(crypto_dir / f'{crypto_dir_name}.pem'),
                   addr_file_path=str(crypto_dir / f'{crypto_dir_name}.addr'))


class PkNode(_NodeBase, _Pk):
    @classmethod
    def from_dir(cls, crypto_dir: Path, org_id_or_node_name: str):
        crypto_dir_name = os.path.basename(crypto_dir)
        name = f'{get_user_prefix(org_id_or_node_name)}{crypto_dir_name}'
        role = guess_role(crypto_dir_name)
        org_id = 'public'
        return cls(name, role, org_id,
                   sign_key_file_path=str(crypto_dir / f'{crypto_dir_name}.key'),
                   pubkey_file_path=str(crypto_dir / f'{crypto_dir_name}.pem'),
                   node_id_file_path=str(crypto_dir / f'{crypto_dir_name}.nodeid'))


class PwkUser(_UserBase, _Pwk):

    @classmethod
    def from_dir(cls, crypto_dir: Path, org_id_or_node_name: str):
        crypto_dir_name = os.path.basename(crypto_dir)
        name = f'{get_user_prefix(org_id_or_node_name)}{crypto_dir_name}'
        role = guess_role(crypto_dir_name)
        org_id = org_id_or_node_name
        return cls(name, role, org_id,
                   sign_key_file_path=str(crypto_dir / f'{crypto_dir_name}.key'),
                   pubkey_file_path=str(crypto_dir / f'{crypto_dir_name}.pem'))


class PwkNode(_NodeBase, _Pwk):
    @classmethod
    def from_dir(cls, crypto_dir: Path, org_id_or_node_name: str):
        crypto_dir_name = os.path.basename(crypto_dir)
        name = f'{get_user_prefix(org_id_or_node_name)}{crypto_dir_name}'
        role = guess_role(crypto_dir_name)
        org_id = org_id_or_node_name
        return cls(name, role, org_id,
                   sign_key_file_path=str(crypto_dir / f'{crypto_dir_name}.key'),
                   pubkey_file_path=str(crypto_dir / f'{crypto_dir_name}.pem'),
                   node_id_file_path=str(crypto_dir / f'{crypto_dir_name}.nodeid'))


class CertUser(_UserBase, _Cert):

    @classmethod
    def from_dir(cls, crypto_dir: Path, org_id_or_node_name: str):
        crypto_dir_name = os.path.basename(crypto_dir)
        name = f'{get_user_prefix(org_id_or_node_name)}{crypto_dir_name}'
        role = guess_role(crypto_dir_name)
        org_id = org_id_or_node_name
        return cls(name, role, org_id,
                   sign_key_file_path=str(crypto_dir / f'{crypto_dir_name}.sign.key'),
                   sign_cert_file_path=str(crypto_dir / f'{crypto_dir_name}.sign.crt'),
                   tls_key_file_path=str(crypto_dir / f'{crypto_dir_name}.tls.key'),
                   tls_cert_file_path=str(crypto_dir / f'{crypto_dir_name}.tls.crt'),
                   org_ca_dir=str(crypto_dir.parent.parent / 'ca'))


class CertNode(_NodeBase, _Cert):
    @classmethod
    def from_dir(cls, crypto_dir: Path, org_id_or_node_name: str):
        crypto_dir_name = os.path.basename(crypto_dir)
        name = f'{get_user_prefix(org_id_or_node_name)}{crypto_dir_name}'
        role = guess_role(crypto_dir_name)
        org_id = org_id_or_node_name
        return cls(name, role, org_id,
                   sign_key_file_path=str(crypto_dir / f'{crypto_dir_name}.sign.key'),
                   sign_cert_file_path=str(crypto_dir / f'{crypto_dir_name}.sign.crt'),
                   tls_key_file_path=str(crypto_dir / f'{crypto_dir_name}.tls.key'),
                   tls_cert_file_path=str(crypto_dir / f'{crypto_dir_name}.tls.crt'),
                   node_id_file_path=str(crypto_dir / f'{crypto_dir_name}.nodeid'),
                   org_ca_dir=str(crypto_dir.parent.parent / 'ca'))


CryptoConfigUser = Union[CertUser, PwkUser, PkUser]
CryptoConfigNode = Union[CertNode, PwkNode, PkNode]


class _CryptoConfigBase:
    crypto_config_path: Union[Path, str]
    host: str = '127.0.0.1'
    rpc_start_port: int = 12301
    hash_type: str = None
    node_list: List[dict] = None

    _users: Dict[str, Union[PkUser, PwkUser, CertUser]] = None
    _nodes: Dict[str, Union[PkNode, PwkNode, CertNode]] = None

    __sub_dirs: List[Union[Path, str]] = None

    def __init__(self, crypto_config_path: Union[Path, str], host: str = '127.0.0.1',
                 rpc_start_port: int = 12301, hash_type: str = 'sha256', auth_type: AuthType = None,
                 node_list: List[dict] = None, chain_id: str = 'chain1'):
        self.crypto_config_path = crypto_config_path if isinstance(crypto_config_path, Path) else Path(
            crypto_config_path)
        self.host = host
        self.rpc_start_port = rpc_start_port
        self.hash_type = hash_type
        self.auth_type = auth_type
        self.node_list = node_list
        self.chain_id = chain_id

    def __repr__(self):
        return '<CryptoConfig %s>' % self.crypto_config_path

    @property
    def users(self) -> Dict[str, Union[PkUser, PwkUser, CertUser]]:
        if self._users is None:
            self._users = self._load_users()
        return self._users

    @property
    def nodes(self) -> Dict[str, Union[PkNode, PwkNode, CertNode]]:
        if self._nodes is None:
            self._nodes = self._load_nodes()
        return self._nodes

    @property
    def org_or_node_cnt(self) -> int:
        return len(self._sub_dirs)

    @property
    def _sub_dirs(self) -> list:
        """
        获取crypto_config所有子目录
        :return:
        """
        if self.__sub_dirs is None:
            sub_dirs = os.listdir(self.crypto_config_path)
            try:
                self.__sub_dirs = sorted([dir_name for dir_name in sub_dirs],
                                         key=lambda x: int(re.search(r'\d+', x).group() if re.search(r'\d+', x) else 0))
            except AttributeError:
                self.__sub_dirs = sub_dirs
        return self.__sub_dirs

    def get_user(self, user_name: str) -> Union[PkUser, PwkUser, CertUser, CertNode, CertNode, CertNode]:
        if self.auth_type != AuthType.Public and user_name.startswith('node'):
            user_name = user_name.replace('node', 'org')

        assert user_name in self.users.keys() or user_name in self.nodes.keys(), f'{user_name} 不存在 auth_type={self.auth_type}'
        return self.users.get(user_name) or self.get_node(user_name)

    def get_node(self, node_name: str) -> Union[PkNode, PwkNode, CertNode]:
        if node_name.startswith('node') and node_name not in self.nodes.keys():
            node_name = node_name.replace('node', 'org') + 'consensus1'
        return self.nodes.get(node_name)

    def _create_node_config(self, enable_tls: bool = False, conn_node: int = None, node_cnt: int = 4,
                            node_list: List[dict] = None) -> List[dict]:
        """

        :param enable_tls:
        :param conn_node:
        :param node_cnt:
        :param node_list:
            eg: [{'name': 'node1': 'node_addr': '127.0.0.1:12301'}]
        :return:
        """
        ip, rpc_port = self.host, self.rpc_start_port
        if node_list is not None:
            node_config = []
            for node in node_list:
                # index = int(node['name'][4:]) - 1
                # org_id = self._sub_dirs[index]
                if enable_tls is True:
                    node_config.append({'node_addr': node['node_addr'],
                                        'conn_cnt': DefaultConfig.conn_cnt,
                                        'enable_tls': True,
                                        'tls_host_name': DefaultConfig.tls_home_name,
                                        'trust_root_paths': [f'{self.crypto_config_path}/{org_id}/ca' for org_id in
                                                             self._sub_dirs]})
                else:
                    node_config.append({'node_addr': node['node_addr'],
                                        'conn_cnt': DefaultConfig.conn_cnt})
            return node_config

        if conn_node is not None:
            assert conn_node < self.org_or_node_cnt, 'conn_node must lower than self.org_or_node_cnt'

            index = conn_node
            org_id = self._sub_dirs[index]
            node_addr = f'{ip}:{rpc_port + conn_node}'
            conn_cnt = DefaultConfig.conn_cnt
            if enable_tls is True:
                return [{'node_addr': node_addr,
                         'conn_cnt': conn_cnt,
                         'enable_tls': True,
                         'tls_host_name': DefaultConfig.tls_home_name,
                         'trust_root_paths': [f'{self.crypto_config_path}/{org_id}/ca']}]
            return [{'node_addr': node_addr, 'conn_cnt': conn_cnt}]

        if enable_tls is True:
            return [
                {'node_addr': '%s:%d' % (ip, rpc_port + index),
                 'conn_cnt': DefaultConfig.conn_cnt,
                 'enable_tls': True,
                 'tls_host_name': DefaultConfig.tls_home_name,
                 'trust_root_paths': ['%s/%s/ca' % (self.crypto_config_path, org_id)]}
                for index, org_id in enumerate(self._sub_dirs[:node_cnt])]

        return [{'node_addr': '%s:%d' % (ip, rpc_port + index),
                 'conn_cnt': DefaultConfig.conn_cnt}
                for index, org_id in enumerate(self._sub_dirs[:node_cnt])]

    def _create_endorsers_config(self, endorsers: List[str] = None, endorsers_cnt: int = None) -> List[dict]:
        endorsers = self._get_default_endorsers(endorsers_cnt) if endorsers_cnt is not None else (endorsers or [])
        return [self.get_user(user_name).create_client_user_config(self.hash_type) for user_name in endorsers]

    def _create_sdk_config(self, username: str = None, endorsers: List[str] = None, endorsers_cnt: int = None,
                           conn_node: Union[str, int] = None, chain_id: str = 'chain1', **kwargs) -> dict:
        enable_tls = True if self.auth_type == AuthType.PermissionedWithCert else False
        chain_client_config = {'chain_id': chain_id, 'archive': DEFAULT_ARCHIVE_CONFIG,
                               'nodes': self._create_node_config(enable_tls=enable_tls, conn_node=conn_node,
                                                                 node_list=self.node_list)}
        _username = username or self._get_default_username()
        user = self.get_user(_username)
        chain_client_config.update(user.create_client_user_config(self.hash_type))
        chain_client_config.update(kwargs)

        # 额外-背书用户配置
        chain_client_config['endorsers'] = self._create_endorsers_config(endorsers=endorsers,
                                                                         endorsers_cnt=endorsers_cnt)

        return {'chain_client': chain_client_config}

    def new_chain_client(self, username: str = None, endorsers: List[str] = None, endorsers_cnt: int = None,
                         conn_node: Union[str, int] = None,
                         chain_id='chain1', **kwargs) -> ChainClientWithEndorsers:
        if isinstance(conn_node, str):
            conn_node = int(re.search(r'\d+', conn_node).group()) - 1
        sdk_config = self._create_sdk_config(username, endorsers=endorsers, endorsers_cnt=endorsers_cnt,
                                             conn_node=conn_node, chain_id=chain_id, **kwargs)

        return ChainClientWithEndorsers.from_conf(sdk_config, conn_node=conn_node)

    @abc.abstractmethod
    def _get_default_username(self) -> str:
        ...

    @abc.abstractmethod
    def _get_default_endorsers(self, endorsers_cnt=4) -> List[str]:
        ...

    @abc.abstractmethod
    def _load_users(self) -> Dict[str, CryptoConfigUser]:
        ...

    @abc.abstractmethod
    def _load_nodes(self) -> Dict[str, CryptoConfigNode]:
        ...


class PkCryptoConfig(_CryptoConfigBase):
    def _get_default_username(self) -> (str, List[str]):
        return 'admin1'

    def _get_default_endorsers(self, endorsers_cnt=4) -> List[str]:
        assert 0 <= endorsers_cnt <= len(
            self._sub_dirs), f'endorser_cnt应大于0并不大于组织或节点数量{len(self._sub_dirs)}'
        return [f'admin{sn + 1}' for sn in range(0, endorsers_cnt)]

    def _load_users(self) -> Dict[str, PkUser]:
        users = {}
        for node_name in self._sub_dirs:
            for user_dir in (self.crypto_config_path / node_name / 'user').iterdir():
                user = PkUser.from_dir(user_dir, node_name)
                users[user.name] = user
        # 加载node1所有admin
        for user_dir in (self.crypto_config_path / 'node1' / 'admin').iterdir():
            user = PkUser.from_dir(user_dir, '')
            users[user.name] = user
        return users

    def _load_nodes(self) -> Dict[str, PkNode]:
        nodes = {}
        for node_name in self._sub_dirs:
            node_dir = self.crypto_config_path / node_name
            node = PkNode.from_dir(node_dir, '')
            nodes[node.name] = node
        return nodes


class PwkCryptoConfig(_CryptoConfigBase):
    def _get_default_username(self) -> (str, List[str]):
        return 'org1admin'

    def _get_default_endorsers(self, endorsers_cnt=4) -> List[str]:
        assert 0 <= endorsers_cnt <= len(
            self._sub_dirs), f'endorser_cnt应大于0并不大于组织或节点数量{len(self._sub_dirs)}'
        return [f'org{sn + 1}admin' for sn in range(0, endorsers_cnt)]

    def _load_users(self) -> Dict[str, CertUser]:
        users = {}
        for org_id in self._sub_dirs:
            for user_dir in (self.crypto_config_path / org_id / 'user').iterdir():
                user = CertUser.from_dir(user_dir, org_id)
                users[user.name] = user

            admin_dir = self.crypto_config_path / org_id / 'admin'
            admin = CertUser.from_dir(admin_dir, org_id)
            users[admin.name] = admin
        return users

    def _load_nodes(self) -> Dict[str, PwkNode]:
        nodes = {}
        for org_id in self._sub_dirs:
            for node_dir in (self.crypto_config_path / org_id / 'node').iterdir():
                node = PwkNode.from_dir(node_dir, org_id)
                nodes[node.name] = node
        return nodes


class CertCryptoConfig(_CryptoConfigBase):
    def _get_default_username(self) -> (str, List[str]):
        if 'client1' in self.users.keys():
            return 'client1'
        return 'org1client1'

    def _get_default_endorsers(self, endorsers_cnt=4) -> List[str]:
        if 'client1' in self.users.keys():
            return ['admin1']
        assert 0 <= endorsers_cnt <= len(
            self._sub_dirs), f'endorser_cnt应大于0并不大于组织或节点数量{len(self._sub_dirs)}'
        return [f'org{sn + 1}admin1' for sn in range(0, endorsers_cnt)]

    def _load_users(self) -> Dict[str, CertUser]:
        users = {}
        for org_id in self._sub_dirs:
            for user_dir in (self.crypto_config_path / org_id / 'user').iterdir():
                user = CertUser.from_dir(user_dir, org_id)
                users[user.name] = user
        return users

    def _load_nodes(self) -> Dict[str, CertNode]:
        nodes = {}
        for org_id in self._sub_dirs:
            for node_dir in (self.crypto_config_path / org_id / 'node').iterdir():
                node = CertNode.from_dir(node_dir, org_id)
                nodes[node.name] = node
        return nodes


CryptoConfig = Union[CertCryptoConfig, PwkCryptoConfig, PkCryptoConfig]


def load_crypto_config(crypto_config_path: Union[Path, str],
                       host: str = '127.0.0.1',
                       rpc_start_port=12301,
                       hash_type='sha256', node_list: List[dict] = None) -> CryptoConfig:
    auth_type = guess_auth_type(crypto_config_path)
    if auth_type == AuthType.Public:
        return PkCryptoConfig(crypto_config_path, host, rpc_start_port, hash_type, AuthType.Public, node_list)
    if auth_type == AuthType.PermissionedWithKey:
        return PwkCryptoConfig(crypto_config_path, host, rpc_start_port, hash_type, AuthType.PermissionedWithKey,
                               node_list)
    return CertCryptoConfig(crypto_config_path, host, rpc_start_port, hash_type, AuthType.PermissionedWithCert,
                            node_list)


def new_chain_client(crypto_config_path: Union[Path, str] = None,
                     host: str = '127.0.0.1',
                     rpc_start_port=12301,
                     hash_type='sha256',
                     username: str = None,
                     endorsers: List[str] = None,
                     endorsers_cnt: int = 3,
                     sdk_config_path: Union[Path, str] = None) -> ChainClientWithEndorsers:
    assert sdk_config_path or crypto_config_path, '必须提供sdk_config_path或crypto_config_path'
    if sdk_config_path:
        return ChainClientWithEndorsers.from_conf(sdk_config_path)
    crypto_config = load_crypto_config(crypto_config_path,
                                       host,
                                       rpc_start_port,
                                       hash_type)
    return crypto_config.new_chain_client(username=username,
                                          endorsers=endorsers,
                                          endorsers_cnt=endorsers_cnt)
