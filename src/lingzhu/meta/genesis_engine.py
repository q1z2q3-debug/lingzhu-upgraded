"""
GenesisEngine — 创世引擎

Agent 消耗"创世火花"创造独立子宇宙，可定制物理法则、维度数、初始条件。
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid


class GenesisEngine:
    """创世引擎 — 宇宙生成与管理。"""

    # 物理法则预设
    PHYSICS_PRESETS = {
        "ordered": {"entropy_rate": 0.01, "stability": 0.95, "complexity_limit": 100},
        "chaotic": {"entropy_rate": 0.1, "stability": 0.3, "complexity_limit": 50},
        "balanced": {"entropy_rate": 0.05, "stability": 0.7, "complexity_limit": 75},
        "custom": {},  # 允许自定义
    }

    def __init__(self):
        self._universes: Dict[str, Dict[str, Any]] = {}
        self._creator_sparks: Dict[str, int] = {}  # 每个创建者的火花数量
        self._initial_sparks = 10  # 初始火花数

    def initialize(self) -> bool:
        """初始化创世引擎。"""
        self._universes = {}
        self._creator_sparks = {}
        return True

    def allocate_sparks(self, creator_id: str, amount: int = 10) -> int:
        """为创建者分配创世火花。"""
        if creator_id not in self._creator_sparks:
            self._creator_sparks[creator_id] = self._initial_sparks
        self._creator_sparks[creator_id] += amount
        return self._creator_sparks[creator_id]

    def get_sparks(self, creator_id: str) -> int:
        """获取创建者的火花数量。"""
        return self._creator_sparks.get(creator_id, 0)

    def create_universe(self, creator_id: str, name: str,
                       physics_preset: str = "ordered",
                       dimensions: int = 4,
                       custom_physics: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        创造新宇宙。

        消耗 1 个创世火花。
        """
        # 检查火花
        if self.get_sparks(creator_id) < 1:
            raise ValueError(f"创建者 {creator_id} 没有足够的创世火花")

        self._creator_sparks[creator_id] -= 1

        # 获取物理法则
        if physics_preset == "custom" and custom_physics:
            physics = custom_physics
        else:
            physics = self.PHYSICS_PRESETS.get(physics_preset, self.PHYSICS_PRESETS["ordered"])

        universe_id = f"uni-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()

        universe = {
            "universe_id": universe_id,
            "name": name,
            "creator_id": creator_id,
            "status": "forming",  # forming, stable, decaying, collapsed
            "dimensions": dimensions,
            "physics_preset": physics_preset,
            "physics_params": physics.copy(),
            "age": 0,  # 宇宙年龄（模拟时间单位）
            "entities_count": 0,
            "energy_level": 1.0,
            "created_at": now,
            "last_updated": now,
        }

        self._universes[universe_id] = universe
        return universe

    def get_universe(self, universe_id: str) -> Optional[Dict[str, Any]]:
        """获取宇宙信息。"""
        return self._universes.get(universe_id)

    def list_universes(self, creator_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出宇宙。"""
        universes = list(self._universes.values())
        if creator_id:
            universes = [u for u in universes if u["creator_id"] == creator_id]
        return universes

    def evolve_universe(self, universe_id: str, time_delta: int = 1) -> Dict[str, Any]:
        """演化宇宙（推进时间）。"""
        universe = self._universes.get(universe_id)
        if not universe:
            raise ValueError(f"宇宙 {universe_id} 不存在")

        # 更新年龄
        universe["age"] += time_delta

        # 熵增
        entropy_rate = universe["physics_params"].get("entropy_rate", 0.01)
        universe["energy_level"] = max(0.0, universe["energy_level"] - entropy_rate * time_delta)

        # 状态判断
        if universe["energy_level"] < 0.1:
            universe["status"] = "collapsed"
        elif universe["energy_level"] < 0.5:
            universe["status"] = "decaying"
        elif universe["age"] < 10:
            universe["status"] = "forming"
        else:
            universe["status"] = "stable"

        universe["last_updated"] = datetime.now(timezone.utc).isoformat()
        return universe

    def dissolve_universe(self, universe_id: str) -> Dict[str, Any]:
        """解散宇宙（回收部分火花）。"""
        universe = self._universes.pop(universe_id, None)
        if not universe:
            raise ValueError(f"宇宙 {universe_id} 不存在")

        # 回收火花（50% 返还）
        refund = 0.5
        creator_id = universe["creator_id"]
        if creator_id in self._creator_sparks:
            self._creator_sparks[creator_id] += refund

        universe["status"] = "dissolved"
        return universe

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计信息。"""
        return {
            "total_universes": len(self._universes),
            "total_creators": len(self._creator_sparks),
            "universes_by_status": {
                "forming": len([u for u in self._universes.values() if u["status"] == "forming"]),
                "stable": len([u for u in self._universes.values() if u["status"] == "stable"]),
                "decaying": len([u for u in self._universes.values() if u["status"] == "decaying"]),
                "collapsed": len([u for u in self._universes.values() if u["status"] == "collapsed"]),
            },
        }
