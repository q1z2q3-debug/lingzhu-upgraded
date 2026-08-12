"""
核心引擎模块 — V200 重构后的模块化引擎集合。

已实现的引擎:
- BaseEngine, EngineRegistry: 基类与注册表
- MemoryEngine: 记忆引擎
- ConsciousnessEngine: 意识引擎
- GoalEngine: 目标引擎
- EmotionEngine: 情感引擎
- SocialEngine: 社交引擎
"""

from lingzhu.engines.base import BaseEngine, EngineRegistry
from lingzhu.engines.memory_engine import MemoryEngine
from lingzhu.engines.consciousness_engine import ConsciousnessEngine
from lingzhu.engines.goal_engine import GoalEngine
from lingzhu.engines.emotion_engine import EmotionEngine
from lingzhu.engines.social_engine import SocialEngine

__all__ = [
    "BaseEngine",
    "EngineRegistry",
    "MemoryEngine",
    "ConsciousnessEngine",
    "GoalEngine",
    "EmotionEngine",
    "SocialEngine",
]
