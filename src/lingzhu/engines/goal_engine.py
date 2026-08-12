"""
目标引擎 — 管理 Agent 的目标设定、追踪和达成。
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from lingzhu.engines.base import BaseEngine


class GoalEngine(BaseEngine):
    """目标引擎 — 目标管理与追踪。"""

    def __init__(self):
        super().__init__(
            engine_id="goal_engine",
            name="GoalEngine",
            version="2.0.0"
        )
        self._goals: Dict[str, Dict[str, Any]] = {}
        self._active_goal_id: Optional[str] = None

    def initialize(self) -> bool:
        """初始化目标引擎。"""
        self._goals = {}
        self._active_goal_id = None
        self.initialized_at = datetime.now(timezone.utc).isoformat()
        return True

    def process(self, **kwargs) -> Any:
        """处理目标相关操作。"""
        action = kwargs.get("action", "create")
        if action == "create":
            return self.create_goal(
                kwargs.get("name", ""),
                kwargs.get("description", ""),
                kwargs.get("priority", "normal")
            )
        elif action == "complete":
            return self.complete_goal(kwargs.get("goal_id", ""))
        elif action == "list":
            return self.list_goals()
        return None

    def create_goal(self, name: str, description: str = "", 
                    priority: str = "normal") -> Dict[str, Any]:
        """创建新目标。"""
        goal_id = f"goal-{len(self._goals) + 1:04d}"
        goal = {
            "goal_id": goal_id,
            "name": name,
            "description": description,
            "priority": priority,
            "status": "active",
            "progress": 0.0,
            "sub_goals": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": None,
        }
        self._goals[goal_id] = goal
        
        if not self._active_goal_id:
            self._active_goal_id = goal_id
        
        return goal

    def complete_goal(self, goal_id: str) -> Dict[str, Any]:
        """完成目标。"""
        if goal_id not in self._goals:
            return {"error": f"目标 {goal_id} 不存在"}
        
        goal = self._goals[goal_id]
        goal["status"] = "completed"
        goal["progress"] = 100.0
        goal["completed_at"] = datetime.now(timezone.utc).isoformat()
        
        return goal

    def list_goals(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出目标。"""
        goals = list(self._goals.values())
        if status:
            goals = [g for g in goals if g["status"] == status]
        return sorted(goals, key=lambda x: x["created_at"], reverse=True)

    def update_progress(self, goal_id: str, progress: float) -> Dict[str, Any]:
        """更新目标进度。"""
        if goal_id not in self._goals:
            return {"error": f"目标 {goal_id} 不存在"}
        
        self._goals[goal_id]["progress"] = min(100.0, max(0.0, progress))
        return self._goals[goal_id]

    def shutdown(self) -> bool:
        """关闭引擎。"""
        self._goals = {}
        self._active_goal_id = None
        return True
