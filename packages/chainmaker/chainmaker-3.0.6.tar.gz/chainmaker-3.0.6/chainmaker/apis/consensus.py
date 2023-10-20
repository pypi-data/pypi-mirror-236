import json
from typing import List

from chainmaker.apis.base_client import BaseClient
from chainmaker.protos.consensus.consensus_pb2 import GetConsensusStatusRequest


class ConsensusMixIn(BaseClient):
    """共识状态操作"""

    def get_consensus_validators(self) -> List[str]:
        """
        获取所有共识节点的身份标识
        :return: 共识节点身份标识
        :exception: 当查询的节点非共识节点时或共识节点内部查询中出现错误，返回error
        """
        self._debug("begin to GetConsensusValidators")
        req = GetConsensusStatusRequest(chain_id=self.chain_id)
        response = self._get_client().GetConsensusValidators(req)
        return response.nodes

    def get_consensus_height(self) -> int:
        """
        获取节点正在共识的区块高度
        :return:
        """
        self._debug("begin to GetConsensusHeight")
        req = GetConsensusStatusRequest(chain_id=self.chain_id)
        response = self._get_client().GetConsensusHeight(req)
        return response.value

    def get_consensus_state_json(self) -> dict:
        """
        获取共识节点的状态
        :return: 查询的共识节点状态
        """
        self._debug("begin to GetConsensusStateJSON")
        req = GetConsensusStatusRequest(chain_id=self.chain_id)
        response = self._get_client().GetConsensusStateJSON(req)
        return json.loads(response.value)
