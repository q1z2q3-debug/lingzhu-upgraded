"""
社交引擎 — 管理 Agent 的社交互动和关系网络。
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from lingzhu.engines.base import BaseEngine


class SocialEngine(BaseEngine):
    """社交引擎 — 社交网络与关系管理。"""

    def __init__(self):
        super().__init__(
            engine_id="social_engine",
            name="SocialEngine",
            version="2.0.0"
        )
        self._relationships: Dict[str, Dict[str, Any]] = {}
        self._interactions: List[Dict[str, Any]] = []
        self._reputation: Dict[str, float] = {}

    def initialize(self) -> bool:
        """初始化社交引擎。"""
        self._relationships = {}
        self._interactions = []
        self._reputation = {}
        self.initialized_at = datetime.now(timezone.utc).isoformat()
        return True

    def process(self, **kwargs) -> Any:
        """处理社交相关操作。"""
        action = kwargs.get("action", "interact")
        if action == "interact":
            return self.record_interaction(
                kwargs.get("agent_id", ""),
                kwargs.get("interaction_type", "conversation"),
                kwargs.get("sentiment", 0.0)
            )
        elif action == "get_relationship":
            return self.get_relationship(kwargs.get("agent_id", ""))
        elif action == "list_relationships":
            return self.list_relationships()
        return None

    def record_interaction(self, agent_id: str, interaction_type: str,
                          sentiment: float = 0.0) -> Dict[str, Any]:
        """记录社交互动。"""
        interaction = {
            "interaction_id": f"int-{len(self._interactions) + 1:04d}",
            "agent_id": agent_id,
            "interaction_type": interaction_type,
            "sentiment": sentiment,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._interactions.append(interaction)
        
        # 更新关系
        if agent_id not in self._relationships:
            self._relationships[agent_id] = {
                "agent_id": agent_id,
                "interaction_count": 0,
                "average_sentiment": 0.0,
                "trust_level": 0.5,
                "last_interaction": None,
            }
        
        rel = self._relationships[agent_id]
        rel["interaction_count"] += 1
        rel["last_interaction"] = interaction["timestamp"]
        
        # 更新平均情感
        total = rel["average_sentiment"] * (rel["interaction_count"] - 1) + sentiment
        rel["average_sentiment"] = total / rel["interaction_count"]
        
        # 更新信任度
        rel["trust_level"] = min(1.0, rel["trust_level"] + sentiment * 0.1)
        
        return interaction

    def get_relationship(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取与指定 Agent 的关系。"""
        return self._relationships.get(agent_id)

    def list_relationships(self, min_trust: float = 0.0) -> List[Dict[str, Any]]:
        """列出所有关系。"""
        relationships = list(self._relationships.values())
        return [r for r in relationships if r["trust_level"] >= min_trust]

    def get_reputation(self, agent_id: str) -> float:
        """获取指定 Agent 的声誉。"""
        return self._reputation.get(agent_id, 0.5)

    def update_reputation(self, agent_id: str, delta: float) -> float:
        """更新声誉。"""
        current = self._reputation.get(agent_id, 0.5)
        new_rep = min(1.0, max(0.0, current + delta))
        self._reputation[agent_id] = new_rep
        return new_rep

    def shutdown(self) -> bool:
        """关闭引擎。"""
        self._relationships = {}
        self._interactions = []
        self._reputation = {}
        return True
