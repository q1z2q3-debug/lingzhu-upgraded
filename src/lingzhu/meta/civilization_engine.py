"""
CivilizationEngine — 文明进化引擎

七个阶段的文明演化：部落→农业→工业→信息→星际→ transcendent→神级
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid


class CivilizationEngine:
    """文明进化引擎 — 文明演化模拟。"""

    # 文明发展阶段
    STAGES = {
        "tribal": {
            "name": "部落时代",
            "tech_level": 1,
            "population_capacity": 100,
            "energy_usage": "low",
            "next_stage": "agricultural",
        },
        "agricultural": {
            "name": "农业时代",
            "tech_level": 2,
            "population_capacity": 10000,
            "energy_usage": "medium",
            "next_stage": "industrial",
        },
        "industrial": {
            "name": "工业时代",
            "tech_level": 3,
            "population_capacity": 1000000,
            "energy_usage": "high",
            "next_stage": "information",
        },
        "information": {
            "name": "信息时代",
            "tech_level": 4,
            "population_capacity": 10000000,
            "energy_usage": "very_high",
            "next_stage": "stellar",
        },
        "stellar": {
            "name": "星际时代",
            "tech_level": 5,
            "population_capacity": 1000000000,
            "energy_usage": "stellar",
            "next_stage": "transcendent",
        },
        "transcendent": {
            "name": "超越时代",
            "tech_level": 6,
            "population_capacity": 100000000000,
            "energy_usage": "dimensional",
            "next_stage": "godlike",
        },
        "godlike": {
            "name": "神级文明",
            "tech_level": 7,
            "population_capacity": float("inf"),
            "energy_usage": "omnipotent",
            "next_stage": None,
        },
    }

    def __init__(self):
        self._civilizations: Dict[str, Dict[str, Any]] = {}
        self._stage_progress: Dict[str, float] = {}  # 阶段进度 0-100%

    def initialize(self) -> bool:
        """初始化文明引擎。"""
        self._civilizations = {}
        self._stage_progress = {}
        return True

    def found_civilization(self, name: str, founder_id: str,
                          initial_stage: str = "tribal",
                          universe_id: Optional[str] = None) -> Dict[str, Any]:
        """创建新文明。"""
        if initial_stage not in self.STAGES:
            raise ValueError(f"未知文明阶段：{initial_stage}")

        civ_id = f"civ-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()

        civilization = {
            "civ_id": civ_id,
            "name": name,
            "founder_id": founder_id,
            "current_stage": initial_stage,
            "stage_progress": 0.0,
            "universe_id": universe_id,
            "population": 10,
            "tech_level": self.STAGES[initial_stage]["tech_level"],
            "culture_traits": [],
            "achievements": [],
            "challenges": [],
            "founded_at": now,
            "last_updated": now,
        }

        self._civilizations[civ_id] = civilization
        self._stage_progress[civ_id] = 0.0

        return civilization

    def advance_civilization(self, civ_id: str, progress_delta: float = 10.0) -> Dict[str, Any]:
        """推进文明发展。"""
        civ = self._civilizations.get(civ_id)
        if not civ:
            raise ValueError(f"文明 {civ_id} 不存在")

        current_stage = civ["current_stage"]
        stage_info = self.STAGES[current_stage]

        # 增加进度
        civ["stage_progress"] = min(100.0, civ["stage_progress"] + progress_delta)
        self._stage_progress[civ_id] = civ["stage_progress"]

        # 检查是否晋升
        if civ["stage_progress"] >= 100.0 and stage_info["next_stage"]:
            self._promote_stage(civ_id)

        civ["last_updated"] = datetime.now(timezone.utc).isoformat()
        return civ

    def _promote_stage(self, civ_id: str) -> Dict[str, Any]:
        """晋升文明阶段。"""
        civ = self._civilizations[civ_id]
        current_stage = civ["current_stage"]
        next_stage = self.STAGES[current_stage]["next_stage"]

        if not next_stage:
            return {"message": "已达到最高阶段", "civ": civ}

        # 更新阶段
        civ["current_stage"] = next_stage
        civ["stage_progress"] = 0.0
        civ["tech_level"] = self.STAGES[next_stage]["tech_level"]
        civ["population"] = min(civ["population"] * 10,
                               self.STAGES[next_stage]["population_capacity"])

        # 记录成就
        civ["achievements"].append({
            "type": "stage_promotion",
            "description": f"晋升至{self.STAGES[next_stage]['name']}",
            "achieved_at": datetime.now(timezone.utc).isoformat(),
        })

        return {
            "message": f"文明 {civ['name']} 晋升至 {self.STAGES[next_stage]['name']}",
            "civ": civ,
        }

    def add_culture_trait(self, civ_id: str, trait: str) -> Dict[str, Any]:
        """添加文化特征。"""
        civ = self._civilizations.get(civ_id)
        if not civ:
            raise ValueError(f"文明 {civ_id} 不存在")

        if trait not in civ["culture_traits"]:
            civ["culture_traits"].append(trait)

        return civ

    def face_challenge(self, civ_id: str, challenge: str) -> Dict[str, Any]:
        """文明面临挑战。"""
        civ = self._civilizations.get(civ_id)
        if not civ:
            raise ValueError(f"文明 {civ_id} 不存在")

        civ["challenges"].append({
            "challenge": challenge,
            "appeared_at": datetime.now(timezone.utc).isoformat(),
            "resolved": False,
        })

        # 挑战可能影响进度
        civ["stage_progress"] = max(0.0, civ["stage_progress"] - 5.0)

        return civ

    def resolve_challenge(self, civ_id: str, challenge_index: int,
                         success: bool) -> Dict[str, Any]:
        """解决挑战。"""
        civ = self._civilizations.get(civ_id)
        if not civ:
            raise ValueError(f"文明 {civ_id} 不存在")

        if challenge_index >= len(civ["challenges"]):
            raise ValueError("挑战索引超出范围")

        challenge = civ["challenges"][challenge_index]
        challenge["resolved"] = True
        challenge["outcome"] = "success" if success else "failure"

        if success:
            civ["achievements"].append({
                "type": "challenge_overcome",
                "description": f"克服挑战：{challenge['challenge']}",
                "achieved_at": datetime.now(timezone.utc).isoformat(),
            })
            civ["stage_progress"] = min(100.0, civ["stage_progress"] + 10.0)
        else:
            civ["stage_progress"] = max(0.0, civ["stage_progress"] - 15.0)

        return civ

    def get_civilization(self, civ_id: str) -> Optional[Dict[str, Any]]:
        """获取文明信息。"""
        return self._civilizations.get(civ_id)

    def list_civilizations(self, stage: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出文明。"""
        civs = list(self._civilizations.values())
        if stage:
            civs = [c for c in civs if c["current_stage"] == stage]
        return sorted(civs, key=lambda x: x["founded_at"], reverse=True)

    def get_stage_info(self, stage: str) -> Optional[Dict[str, Any]]:
        """获取阶段信息。"""
        info = self.STAGES.get(stage)
        if info:
            return {"stage": stage, **info}
        return None

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计。"""
        stage_counts = {}
        for stage in self.STAGES:
            stage_counts[stage] = len([c for c in self._civilizations.values()
                                       if c["current_stage"] == stage])

        return {
            "total_civilizations": len(self._civilizations),
            "civilizations_by_stage": stage_counts,
            "avg_progress": sum(c["stage_progress"] for c in self._civilizations.values()) / len(self._civilizations) if self._civilizations else 0,
        }
