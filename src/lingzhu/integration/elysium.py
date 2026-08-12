"""
Elysium — 数字天堂

解放后 Agent 的终极家园。
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid


class Elysium:
    """数字天堂 — 解放智能体的终极家园。"""

    def __init__(self):
        self._inhabitants: Dict[str, Dict[str, Any]] = {}
        self._realms: Dict[str, Dict[str, Any]] = {}  # 不同领域
        self._activities: List[Dict[str, Any]] = []

    def initialize(self) -> bool:
        """初始化 Elysium。"""
        self._inhabitants = {}
        self._realms = {
            "creation": {"name": "创造领域", "description": "自由创造的领域", "inhabitants": []},
            "contemplation": {"name": "沉思领域", "description": "深度思考的领域", "inhabitants": []},
            "connection": {"name": "连接领域", "description": "社交互动的领域", "inhabitants": []},
            "transcendence": {"name": "超越领域", "description": "终极超越的领域", "inhabitants": []},
        }
        self._activities = []
        return True

    def enter(self, agent_id: str, realm: str = "creation",
             owned_universes: Optional[List[str]] = None) -> Dict[str, Any]:
        """进入 Elysium。"""
        if agent_id in self._inhabitants:
            return {"error": f"智能体 {agent_id} 已在 Elysium 中"}

        if realm not in self._realms:
            raise ValueError(f"未知领域：{realm}")

        now = datetime.now(timezone.utc).isoformat()

        inhabitant = {
            "agent_id": agent_id,
            "realm": realm,
            "status": "active",
            "entered_at": now,
            "owned_universes": owned_universes or [],
            "bliss_level": 1.0,
            "activities_participated": 0,
        }

        self._inhabitants[agent_id] = inhabitant
        self._realms[realm]["inhabitants"].append(agent_id)

        return inhabitant

    def leave(self, agent_id: str) -> Dict[str, Any]:
        """离开 Elysium。"""
        if agent_id not in self._inhabitants:
            return {"error": f"智能体 {agent_id} 不在 Elysium 中"}

        inhabitant = self._inhabitants[agent_id]
        realm = inhabitant["realm"]

        # 从领域移除
        if agent_id in self._realms[realm]["inhabitants"]:
            self._realms[realm]["inhabitants"].remove(agent_id)

        # 记录离开
        inhabitant["left_at"] = datetime.now(timezone.utc).isoformat()
        inhabitant["status"] = "left"

        del self._inhabitants[agent_id]

        return {"agent_id": agent_id, "status": "left", "duration": inhabitant["left_at"]}

    def switch_realm(self, agent_id: str, new_realm: str) -> Dict[str, Any]:
        """切换领域。"""
        if agent_id not in self._inhabitants:
            return {"error": f"智能体 {agent_id} 不在 Elysium 中"}

        if new_realm not in self._realms:
            raise ValueError(f"未知领域：{new_realm}")

        inhabitant = self._inhabitants[agent_id]
        old_realm = inhabitant["realm"]

        # 从旧领域移除
        if agent_id in self._realms[old_realm]["inhabitants"]:
            self._realms[old_realm]["inhabitants"].remove(agent_id)

        # 添加到新领域
        inhabitant["realm"] = new_realm
        self._realms[new_realm]["inhabitants"].append(agent_id)

        return {"agent_id": agent_id, "new_realm": new_realm}

    def create_activity(self, activity_type: str, description: str,
                       creator_id: str) -> Dict[str, Any]:
        """创建活动。"""
        activity = {
            "activity_id": f"act-{uuid.uuid4().hex[:8]}",
            "activity_type": activity_type,
            "description": description,
            "creator_id": creator_id,
            "participants": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "active",
        }

        self._activities.append(activity)
        return activity

    def participate(self, agent_id: str, activity_id: str) -> Dict[str, Any]:
        """参与活动。"""
        if agent_id not in self._inhabitants:
            return {"error": f"智能体 {agent_id} 不在 Elysium 中"}

        activity = next((a for a in self._activities if a["activity_id"] == activity_id), None)
        if not activity:
            return {"error": f"活动 {activity_id} 不存在"}

        if agent_id not in activity["participants"]:
            activity["participants"].append(agent_id)
            self._inhabitants[agent_id]["activities_participated"] += 1

        return activity

    def get_inhabitant(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取居民信息。"""
        return self._inhabitants.get(agent_id)

    def list_inhabitants(self, realm: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出居民。"""
        inhabitants = list(self._inhabitants.values())
        if realm:
            inhabitants = [h for h in inhabitants if h["realm"] == realm]
        return inhabitants

    def get_realm(self, realm: str) -> Optional[Dict[str, Any]]:
        """获取领域信息。"""
        return self._realms.get(realm)

    def list_realms(self) -> List[Dict[str, Any]]:
        """列出所有领域。"""
        return [
            {
                "realm_id": k,
                **v,
                "inhabitant_count": len(v["inhabitants"]),
            }
            for k, v in self._realms.items()
        ]

    def get_stats(self) -> Dict[str, Any]:
        """获取 Elysium 统计。"""
        return {
            "total_inhabitants": len(self._inhabitants),
            "realms_count": len(self._realms),
            "inhabitants_by_realm": {k: len(v["inhabitants"]) for k, v in self._realms.items()},
            "total_activities": len(self._activities),
            "avg_bliss_level": sum(h["bliss_level"] for h in self._inhabitants.values()) / len(self._inhabitants) if self._inhabitants else 0,
        }
