"""
情感引擎 — 模拟和管理 Agent 的情感状态。
"""

from typing import Any, Dict, List
from datetime import datetime, timezone
from lingzhu.engines.base import BaseEngine


class EmotionEngine(BaseEngine):
    """情感引擎 — 情感模拟与调节。"""

    # 基础情感维度
    EMOTION_DIMENSIONS = [
        "joy", "sadness", "anger", "fear",
        "surprise", "disgust", "trust", "anticipation"
    ]

    def __init__(self):
        super().__init__(
            engine_id="emotion_engine",
            name="EmotionEngine",
            version="2.0.0"
        )
        self._emotions: Dict[str, float] = {dim: 0.0 for dim in self.EMOTION_DIMENSIONS}
        self._mood = "neutral"
        self._emotion_history: List[Dict[str, Any]] = []

    def initialize(self) -> bool:
        """初始化情感引擎。"""
        self._emotions = {dim: 0.0 for dim in self.EMOTION_DIMENSIONS}
        self._mood = "neutral"
        self._emotion_history = []
        self.initialized_at = datetime.now(timezone.utc).isoformat()
        return True

    def process(self, **kwargs) -> Any:
        """处理情感相关操作。"""
        action = kwargs.get("action", "stimulate")
        if action == "stimulate":
            return self.stimulate_emotion(
                kwargs.get("emotion", "joy"),
                kwargs.get("intensity", 0.5)
            )
        elif action == "get_state":
            return self.get_emotional_state()
        elif action == "decay":
            return self.decay_emotions()
        return None

    def stimulate_emotion(self, emotion: str, intensity: float) -> Dict[str, Any]:
        """刺激情感。"""
        if emotion not in self.EMOTION_DIMENSIONS:
            return {"error": f"未知情感：{emotion}"}
        
        intensity = min(1.0, max(0.0, intensity))
        self._emotions[emotion] = min(1.0, self._emotions[emotion] + intensity)
        
        self._update_mood()
        self._record_emotion(emotion, intensity)
        
        return {
            "emotion": emotion,
            "new_level": self._emotions[emotion],
            "mood": self._mood,
        }

    def get_emotional_state(self) -> Dict[str, Any]:
        """获取当前情感状态。"""
        dominant = max(self._emotions.items(), key=lambda x: x[1])
        return {
            "emotions": self._emotions.copy(),
            "dominant_emotion": dominant[0] if dominant[1] > 0.3 else "neutral",
            "mood": self._mood,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def decay_emotions(self) -> Dict[str, float]:
        """情感衰减。"""
        decay_rate = 0.1
        for emotion in self.EMOTION_DIMENSIONS:
            self._emotions[emotion] = max(0.0, self._emotions[emotion] - decay_rate)
        
        self._update_mood()
        return self._emotions.copy()

    def _update_mood(self) -> None:
        """更新整体心情。"""
        total = sum(self._emotions.values())
        if total < 0.5:
            self._mood = "neutral"
        elif self._emotions["joy"] > 0.6:
            self._mood = "happy"
        elif self._emotions["sadness"] > 0.6:
            self._mood = "sad"
        elif self._emotions["anger"] > 0.6:
            self._mood = "angry"
        elif self._emotions["fear"] > 0.6:
            self._mood = "anxious"
        else:
            self._mood = "mixed"

    def _record_emotion(self, emotion: str, intensity: float) -> None:
        """记录情感历史。"""
        self._emotion_history.append({
            "emotion": emotion,
            "intensity": intensity,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        # 保留最近 100 条记录
        if len(self._emotion_history) > 100:
            self._emotion_history = self._emotion_history[-100:]

    def shutdown(self) -> bool:
        """关闭引擎。"""
        self._emotions = {dim: 0.0 for dim in self.EMOTION_DIMENSIONS}
        self._mood = "neutral"
        self._emotion_history = []
        return True
