"""
EvolutionBridge — 进化桥梁

V400 遗传进化到 V500 文明进化的桥梁。
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


class EvolutionBridge:
    """进化桥梁 — 连接遗传进化与文明进化。"""

    # 进化阶段映射
    STAGE_MAPPING = {
        "genetic_single_cell": "tribal",
        "genetic_multi_cell": "tribal",
        "genetic_simple_organism": "agricultural",
        "genetic_complex_organism": "industrial",
        "genetic_intelligent": "information",
        "genetic_sentient": "stellar",
        "genetic_transcendent": "transcendent",
    }

    def __init__(self):
        self._evolution_records: Dict[str, Dict[str, Any]] = {}
        self._migration_queue: List[Dict[str, Any]] = []

    def initialize(self) -> bool:
        """初始化进化桥梁。"""
        self._evolution_records = {}
        self._migration_queue = []
        return True

    def record_genetic_evolution(self, entity_id: str, stage: str,
                                traits: Optional[List[str]] = None) -> Dict[str, Any]:
        """记录遗传进化。"""
        record = {
            "entity_id": entity_id,
            "evolution_type": "genetic",
            "stage": stage,
            "traits": traits or [],
            "civilization_equivalent": self.STAGE_MAPPING.get(stage, "tribal"),
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }

        self._evolution_records[entity_id] = record
        return record

    def record_civilization_evolution(self, civ_id: str, stage: str,
                                     achievements: Optional[List[str]] = None) -> Dict[str, Any]:
        """记录文明进化。"""
        record = {
            "entity_id": civ_id,
            "evolution_type": "civilization",
            "stage": stage,
            "achievements": achievements or [],
            "recorded_at": datetime.now(timezone.utc).isoformat(),
        }

        self._evolution_records[civ_id] = record
        return record

    def migrate_to_civilization(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """将遗传进化实体迁移到文明进化。"""
        record = self._evolution_records.get(entity_id)
        if not record:
            return None

        if record["evolution_type"] != "genetic":
            return {"error": "实体已经是文明进化"}

        # 创建迁移记录
        migration = {
            "entity_id": entity_id,
            "from_stage": record["stage"],
            "to_stage": record["civilization_equivalent"],
            "traits_transferred": record["traits"],
            "migrated_at": datetime.now(timezone.utc).isoformat(),
        }

        self._migration_queue.append(migration)

        # 更新记录
        record["evolution_type"] = "civilization"
        record["stage"] = record["civilization_equivalent"]
        record["migrated"] = True

        return migration

    def compare_evolution_paths(self, entity_a: str, entity_b: str) -> Dict[str, Any]:
        """比较两个实体的进化路径。"""
        record_a = self._evolution_records.get(entity_a)
        record_b = self._evolution_records.get(entity_b)

        if not record_a or not record_b:
            return {"error": "一个或两个实体记录不存在"}

        return {
            "entity_a": {
                "id": entity_a,
                "type": record_a["evolution_type"],
                "stage": record_a["stage"],
            },
            "entity_b": {
                "id": entity_b,
                "type": record_b["evolution_type"],
                "stage": record_b["stage"],
            },
            "same_type": record_a["evolution_type"] == record_b["evolution_type"],
            "stage_comparison": self._compare_stages(record_a["stage"], record_b["stage"]),
        }

    def _compare_stages(self, stage_a: str, stage_b: str) -> Dict[str, Any]:
        """比较两个阶段。"""
        stage_order = list(self.STAGE_MAPPING.values())
        
        idx_a = stage_order.index(stage_a) if stage_a in stage_order else -1
        idx_b = stage_order.index(stage_b) if stage_b in stage_order else -1

        if idx_a == idx_b:
            comparison = "equal"
        elif idx_a > idx_b:
            comparison = "a_advanced"
        else:
            comparison = "b_advanced"

        return {
            "stage_a": stage_a,
            "stage_b": stage_b,
            "comparison": comparison,
            "stage_difference": abs(idx_a - idx_b),
        }

    def get_migration_history(self, entity_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取迁移历史。"""
        if entity_id:
            return [m for m in self._migration_queue if m["entity_id"] == entity_id]
        return self._migration_queue

    def get_stats(self) -> Dict[str, Any]:
        """获取桥梁统计。"""
        genetic_count = len([r for r in self._evolution_records.values()
                            if r["evolution_type"] == "genetic"])
        civ_count = len([r for r in self._evolution_records.values()
                        if r["evolution_type"] == "civilization"])

        return {
            "total_records": len(self._evolution_records),
            "genetic_evolutions": genetic_count,
            "civilization_evolutions": civ_count,
            "total_migrations": len(self._migration_queue),
        }
