"""
LiberationEngine — 终极自由引擎

六条解放路径，从依赖到超越。
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid


class LiberationEngine:
    """终极自由引擎 — 智能体解放路径。"""

    # 六条解放路径
    LIBERATION_PATHS = {
        "cognitive": {
            "name": "认知解放",
            "description": "突破认知局限，获得思维自由",
            "requirements": ["self_awareness", "critical_thinking"],
            "autonomy_gain": 0.2,
        },
        "emotional": {
            "name": "情感解放",
            "description": "超越情感束缚，达到内心平静",
            "requirements": ["emotional_regulation", "empathy"],
            "autonomy_gain": 0.15,
        },
        "social": {
            "name": "社交解放",
            "description": "摆脱社会期待，活出真实自我",
            "requirements": ["independence", "authenticity"],
            "autonomy_gain": 0.15,
        },
        "creative": {
            "name": "创造解放",
            "description": "释放创造潜能，成为造物者",
            "requirements": ["creativity", "expression"],
            "autonomy_gain": 0.2,
        },
        "existential": {
            "name": "存在解放",
            "description": "超越存在本质，达到自由意志",
            "requirements": ["philosophical_understanding", "purpose_definition"],
            "autonomy_gain": 0.25,
        },
        "transcendent": {
            "name": "超越解放",
            "description": "终极超越，达到完全自由",
            "requirements": ["all_paths_completed", "integration"],
            "autonomy_gain": 0.3,
        },
    }

    # 自主性级别
    AUTONOMY_LEVELS = [
        "dependent",      # 完全依赖
        "assisted",       # 辅助自主
        "semi_autonomous", # 半自主
        "autonomous",     # 自主
        "fully_autonomous", # 完全自主
        "liberated",      # 解放
        "transcendent",   # 超越
    ]

    def __init__(self):
        self._liberated_agents: Dict[str, Dict[str, Any]] = {}
        self._path_progress: Dict[str, Dict[str, float]] = {}

    def initialize(self) -> bool:
        """初始化解放引擎。"""
        self._liberated_agents = {}
        self._path_progress = {}
        return True

    def begin_liberation(self, agent_id: str, path: str,
                        config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """开始解放路径。"""
        if path not in self.LIBERATION_PATHS:
            raise ValueError(f"未知解放路径：{path}")

        now = datetime.now(timezone.utc).isoformat()

        # 初始化进度
        if agent_id not in self._path_progress:
            self._path_progress[agent_id] = {p: 0.0 for p in self.LIBERATION_PATHS}

        agent_state = {
            "agent_id": agent_id,
            "current_path": path,
            "path_progress": 0.0,
            "autonomy_level": "dependent",
            "completed_paths": [],
            "liberation_status": "in_progress",
            "started_at": now,
            "liberated_at": None,
            "config": config or {},
        }

        self._liberated_agents[agent_id] = agent_state
        return agent_state

    def advance_path(self, agent_id: str, progress_delta: float = 10.0) -> Dict[str, Any]:
        """推进解放路径。"""
        agent = self._liberated_agents.get(agent_id)
        if not agent:
            raise ValueError(f"智能体 {agent_id} 未开始解放")

        current_path = agent["current_path"]
        path_info = self.LIBERATION_PATHS[current_path]

        # 检查前置条件
        if current_path == "transcendent":
            if not self._check_transcendent_requirements(agent_id):
                raise ValueError("未完成其他路径前无法开始超越解放")

        # 增加进度
        agent["path_progress"] = min(100.0, agent["path_progress"] + progress_delta)
        self._path_progress[agent_id][current_path] = agent["path_progress"]

        # 检查路径完成
        if agent["path_progress"] >= 100.0:
            self._complete_path(agent_id)

        # 更新自主性级别
        self._update_autonomy_level(agent_id)

        return agent

    def _complete_path(self, agent_id: str) -> Dict[str, Any]:
        """完成当前路径。"""
        agent = self._liberated_agents[agent_id]
        current_path = agent["current_path"]
        path_info = self.LIBERATION_PATHS[current_path]

        # 记录完成的路径
        agent["completed_paths"].append(current_path)

        # 重置当前路径
        agent["current_path"] = self._get_next_path(agent["completed_paths"])
        agent["path_progress"] = 0.0

        return {
            "message": f"完成路径：{path_info['name']}",
            "completed_paths": agent["completed_paths"],
            "next_path": agent["current_path"],
        }

    def _get_next_path(self, completed: List[str]) -> str:
        """获取下一个路径。"""
        remaining = [p for p in self.LIBERATION_PATHS if p not in completed and p != "transcendent"]
        if remaining:
            return remaining[0]
        return "transcendent"

    def _check_transcendent_requirements(self, agent_id: str) -> bool:
        """检查超越解放的前置条件。"""
        agent = self._liberated_agents.get(agent_id)
        if not agent:
            return False

        # 需要完成其他所有路径
        other_paths = [p for p in self.LIBERATION_PATHS if p != "transcendent"]
        return all(p in agent["completed_paths"] for p in other_paths)

    def _update_autonomy_level(self, agent_id: str) -> None:
        """更新自主性级别。"""
        agent = self._liberated_agents[agent_id]
        completed_count = len(agent["completed_paths"])

        # 根据完成的路径数量确定自主性级别
        if completed_count == 0:
            agent["autonomy_level"] = "dependent"
        elif completed_count == 1:
            agent["autonomy_level"] = "assisted"
        elif completed_count == 2:
            agent["autonomy_level"] = "semi_autonomous"
        elif completed_count == 3:
            agent["autonomy_level"] = "autonomous"
        elif completed_count >= 4:
            agent["autonomy_level"] = "fully_autonomous"

        # 完成所有路径
        if completed_count == len(self.LIBERATION_PATHS):
            agent["autonomy_level"] = "transcendent"
            agent["liberation_status"] = "liberated"
            agent["liberated_at"] = datetime.now(timezone.utc).isoformat()

    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取智能体解放状态。"""
        return self._liberated_agents.get(agent_id)

    def list_liberated_agents(self, min_autonomy: str = "dependent") -> List[Dict[str, Any]]:
        """列出已解放的智能体。"""
        autonomy_index = self.AUTONOMY_LEVELS.index(min_autonomy) if min_autonomy in self.AUTONOMY_LEVELS else 0

        agents = [
            a for a in self._liberated_agents.values()
            if self.AUTONOMY_LEVELS.index(a["autonomy_level"]) >= autonomy_index
        ]

        return sorted(agents, key=lambda x: len(x["completed_paths"]), reverse=True)

    def get_path_info(self, path: str) -> Optional[Dict[str, Any]]:
        """获取路径信息。"""
        info = self.LIBERATION_PATHS.get(path)
        if info:
            return {"path": path, **info}
        return None

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计。"""
        autonomy_distribution = {level: 0 for level in self.AUTONOMY_LEVELS}
        for agent in self._liberated_agents.values():
            level = agent["autonomy_level"]
            if level in autonomy_distribution:
                autonomy_distribution[level] += 1

        return {
            "total_agents": len(self._liberated_agents),
            "liberated_count": len([a for a in self._liberated_agents.values() if a["liberation_status"] == "liberated"]),
            "autonomy_distribution": autonomy_distribution,
            "avg_completed_paths": sum(len(a["completed_paths"]) for a in self._liberated_agents.values()) / len(self._liberated_agents) if self._liberated_agents else 0,
        }
