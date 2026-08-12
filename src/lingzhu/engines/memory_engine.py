"""
记忆引擎 — 负责存储、检索和管理 Agent 的记忆。
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from lingzhu.engines.base import BaseEngine


class MemoryEngine(BaseEngine):
    """记忆引擎 — 短期记忆与长期记忆管理。"""

    def __init__(self):
        super().__init__(
            engine_id="memory_engine",
            name="MemoryEngine",
            version="2.0.0"
        )
        self._short_term: List[Dict[str, Any]] = []
        self._long_term: Dict[str, Dict[str, Any]] = {}
        self._max_short_term = 100

    def initialize(self) -> bool:
        """初始化记忆引擎。"""
        self._short_term = []
        self._long_term = {}
        self.initialized_at = datetime.now(timezone.utc).isoformat()
        return True

    def process(self, **kwargs) -> Any:
        """处理记忆操作。"""
        action = kwargs.get("action", "store")
        if action == "store":
            return self.store_memory(
                kwargs.get("content", ""),
                kwargs.get("memory_type", "short"),
                kwargs.get("tags", [])
            )
        elif action == "retrieve":
            return self.retrieve_memory(kwargs.get("query", ""))
        elif action == "forget":
            return self.forget_memory(kwargs.get("memory_id", ""))
        return None

    def store_memory(self, content: str, memory_type: str = "short", 
                     tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """存储记忆。"""
        memory_id = f"mem-{len(self._long_term) + 1:04d}"
        memory = {
            "memory_id": memory_id,
            "content": content,
            "memory_type": memory_type,
            "tags": tags or [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "access_count": 0,
        }

        if memory_type == "short":
            self._short_term.append(memory)
            if len(self._short_term) > self._max_short_term:
                self._short_term.pop(0)
        else:
            self._long_term[memory_id] = memory

        return memory

    def retrieve_memory(self, query: str = "") -> List[Dict[str, Any]]:
        """检索记忆。"""
        results = []
        all_memories = list(self._long_term.values()) + self._short_term
        
        if not query:
            return all_memories[:10]

        for memory in all_memories:
            if query.lower() in memory["content"].lower():
                memory["access_count"] += 1
                results.append(memory)
        
        return sorted(results, key=lambda x: x["access_count"], reverse=True)[:10]

    def forget_memory(self, memory_id: str) -> bool:
        """删除记忆。"""
        if memory_id in self._long_term:
            del self._long_term[memory_id]
            return True
        for i, mem in enumerate(self._short_term):
            if mem["memory_id"] == memory_id:
                self._short_term.pop(i)
                return True
        return False

    def consolidate(self) -> int:
        """将短期记忆巩固为长期记忆。"""
        consolidated = 0
        for memory in self._short_term[-20:]:
            if memory.get("access_count", 0) >= 3:
                memory_id = memory["memory_id"]
                self._long_term[memory_id] = memory
                consolidated += 1
        return consolidated

    def shutdown(self) -> bool:
        """关闭引擎。"""
        self._short_term = []
        self._long_term = {}
        return True
