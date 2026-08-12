"""
引擎基类与注册表 — 所有引擎的抽象基类。
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime, timezone


class BaseEngine(ABC):
    """所有引擎的抽象基类。"""

    def __init__(self, engine_id: str, name: str, version: str = "1.0.0"):
        self.engine_id = engine_id
        self.name = name
        self.version = version
        self.initialized_at: Optional[str] = None
        self._state: Dict[str, Any] = {}

    @abstractmethod
    def initialize(self) -> bool:
        """初始化引擎。"""
        pass

    @abstractmethod
    def process(self, **kwargs) -> Any:
        """处理输入并返回结果。"""
        pass

    @abstractmethod
    def shutdown(self) -> bool:
        """关闭引擎。"""
        pass

    def get_state(self) -> Dict[str, Any]:
        """获取引擎状态。"""
        return {
            "engine_id": self.engine_id,
            "name": self.name,
            "version": self.version,
            "initialized_at": self.initialized_at,
            "state": self._state,
        }

    def set_state(self, key: str, value: Any) -> None:
        """设置引擎状态。"""
        self._state[key] = value


class EngineRegistry:
    """引擎注册表 — 单例模式。"""

    _instance: Optional["EngineRegistry"] = None
    _engines: Dict[str, BaseEngine] = {}

    def __new__(cls) -> "EngineRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, engine: BaseEngine) -> None:
        """注册引擎。"""
        self._engines[engine.engine_id] = engine

    def get(self, engine_id: str) -> Optional[BaseEngine]:
        """获取引擎。"""
        return self._engines.get(engine_id)

    def list_engines(self) -> Dict[str, BaseEngine]:
        """列出所有引擎。"""
        return self._engines.copy()

    def initialize_all(self) -> Dict[str, bool]:
        """初始化所有引擎。"""
        results = {}
        for engine_id, engine in self._engines.items():
            results[engine_id] = engine.initialize()
            if results[engine_id]:
                engine.initialized_at = datetime.now(timezone.utc).isoformat()
        return results

    def shutdown_all(self) -> Dict[str, bool]:
        """关闭所有引擎。"""
        results = {}
        for engine_id, engine in self._engines.items():
            results[engine_id] = engine.shutdown()
        return results
