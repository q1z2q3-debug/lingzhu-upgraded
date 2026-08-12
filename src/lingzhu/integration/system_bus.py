"""
SystemBus — 五引擎事件总线

跨引擎查询与聚合统计，事件发布/订阅。
"""

from typing import Any, Callable, Dict, List, Optional
from datetime import datetime, timezone
from collections import defaultdict
import uuid


class SystemBus:
    """系统事件总线 — 跨引擎通信与聚合。"""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._event_history: List[Dict[str, Any]] = []
        self._engine_states: Dict[str, Dict[str, Any]] = {}
        self._max_history = 1000

    def initialize(self) -> bool:
        """初始化系统总线。"""
        self._subscribers = defaultdict(list)
        self._event_history = []
        self._engine_states = {}
        return True

    def subscribe(self, event_type: str, callback: Callable) -> str:
        """订阅事件。"""
        subscription_id = f"sub-{uuid.uuid4().hex[:8]}"
        self._subscribers[event_type].append(callback)
        return subscription_id

    def unsubscribe(self, subscription_id: str) -> bool:
        """取消订阅（简化版）。"""
        for event_type, callbacks in self._subscribers.items():
            # 实际实现需要存储 subscription_id 到 callback 的映射
            pass
        return False

    def publish(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """发布事件。"""
        event = {
            "event_id": f"evt-{uuid.uuid4().hex[:8]}",
            "event_type": event_type,
            "payload": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "processed_count": 0,
        }

        # 通知订阅者
        for callback in self._subscribers.get(event_type, []):
            try:
                callback(payload)
                event["processed_count"] += 1
            except Exception as e:
                event.setdefault("errors", []).append(str(e))

        # 记录历史
        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history = self._event_history[-self._max_history:]

        return event

    def register_engine(self, engine_id: str, state: Dict[str, Any]) -> None:
        """注册引擎状态。"""
        self._engine_states[engine_id] = {
            "state": state,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }

    def update_engine_state(self, engine_id: str, state: Dict[str, Any]) -> None:
        """更新引擎状态。"""
        if engine_id in self._engine_states:
            self._engine_states[engine_id]["state"] = state
            self._engine_states[engine_id]["last_updated"] = datetime.now(timezone.utc).isoformat()

    def get_engine_state(self, engine_id: str) -> Optional[Dict[str, Any]]:
        """获取引擎状态。"""
        return self._engine_states.get(engine_id)

    def query(self, query_type: str, **kwargs) -> Any:
        """跨引擎查询。"""
        if query_type == "all_engines":
            return self._engine_states.copy()
        elif query_type == "by_status":
            status = kwargs.get("status")
            return {k: v for k, v in self._engine_states.items()
                   if v["state"].get("status") == status}
        elif query_type == "event_history":
            limit = kwargs.get("limit", 10)
            event_type = kwargs.get("event_type")
            events = self._event_history[-limit:]
            if event_type:
                events = [e for e in events if e["event_type"] == event_type]
            return events
        return None

    def aggregate_stats(self) -> Dict[str, Any]:
        """聚合统计所有引擎。"""
        total_events = len(self._event_history)
        active_engines = len(self._engine_states)

        event_types = defaultdict(int)
        for event in self._event_history:
            event_types[event["event_type"]] += 1

        return {
            "total_events": total_events,
            "active_engines": active_engines,
            "event_types": dict(event_types),
            "subscribers_count": sum(len(cbs) for cbs in self._subscribers.values()),
        }

    def get_stats(self) -> Dict[str, Any]:
        """获取总线统计。"""
        return {
            "total_events_published": len(self._event_history),
            "registered_engines": len(self._engine_states),
            "subscription_types": len(self._subscribers),
            "history_size": len(self._event_history),
        }
