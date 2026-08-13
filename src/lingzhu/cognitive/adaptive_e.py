"""
e 自适应半衰期调度器

融合 Triton 波动率→半衰期公式 + lingzhu 时间演化
环境波动率 → 自适应半衰期
高波动 → 短半衰期 (旧经验快速失效)
稳定 → 长半衰期 (旧经验依然可信)
"""

from typing import Dict, Optional, List, Tuple
import math
import time


class AdaptiveEHalflife:
    """
    自适应 e 衰减调度器
    融合 Triton 波动率公式 + lingzhu 时间演化
    """
    
    DEFAULT_HALFLIFE_DAYS = 7
    MIN_HALFLIFE_HOURS = 1   # 极高波动：1 小时
    MAX_HALFLIFE_DAYS = 30   # 极稳定：30 天
    
    def __init__(self, default_halflife_days: float = DEFAULT_HALFLIFE_DAYS):
        self.default_halflife_ms = default_halflife_days * 24 * 3600 * 1000
    
    def calculate(self, trit_vector: List[int], memory: Optional[Dict] = None,
                  metrics: Optional[Dict] = None) -> Dict:
        """
        计算自适应 e 参数
        
        返回：{"halflife_days": float, "current_weight": float, "volatility": float, "reason": str}
        """
        # 计算环境波动率
        volatility = self._calculate_volatility(trit_vector, memory, metrics)
        
        # 波动率 → 半衰期映射 (融合 Triton)
        halflife_days = self._map_volatility_to_halflife(volatility)
        
        # 生成原因说明
        reason = self._generate_reason(volatility, halflife_days)
        
        return {
            "halflife_days": round(halflife_days, 2),
            "halflife_ms": int(halflife_days * 24 * 3600 * 1000),
            "volatility": round(volatility, 3),
            "decay_rate": round(math.log(2) / (halflife_days * 24 * 3600 * 1000), 10),
            "reason": reason,
        }
    
    def get_weight(self, timestamp_ms: float, halflife_ms: float) -> float:
        """
        计算某条记忆在当前时刻的活性权重
        weight = e^(-age / halflife_ms)
        """
        age = (time.time() * 1000) - timestamp_ms
        if age < 0:
            return 1.0
        return math.exp(-age / halflife_ms)
    
    def get_decayed_memories(self, memories: List[Dict], halflife_ms: float,
                             top_k: int = 5) -> List[Dict]:
        """
        对记忆列表按 e 权重排序，返回 top_k 条
        """
        now_ms = time.time() * 1000
        for mem in memories:
            ts = mem.get("savedAt")
            if isinstance(ts, str):
                try:
                    from datetime import datetime
                    ts = datetime.fromisoformat(ts.replace('Z', '+00:00')).timestamp() * 1000
                except:
                    ts = now_ms
            elif isinstance(ts, (int, float)):
                pass
            else:
                ts = now_ms
            
            age = now_ms - ts
            mem["e_weight"] = math.exp(-age / halflife_ms) if age >= 0 else 1.0
            mem["age_days"] = round(age / (24 * 3600 * 1000), 2)
        
        memories.sort(key=lambda m: m.get("e_weight", 0), reverse=True)
        return memories[:top_k]
    
    def _calculate_volatility(self, trit_vector: List[int],
                              memory: Optional[Dict] = None,
                              metrics: Optional[Dict] = None) -> float:
        """
        计算环境波动率 (0.0~1.0)
        - 来源 1：Trit 向量中危险/高压信号密度
        - 来源 2：metrics 中的实时波动率
        - 来源 3：memory 中该坐标的历史策略效果稳定性
        """
        vol_sources = []
        
        # 来源 1：Trit 向量波动特征
        danger_ratio = sum(1 for t in trit_vector if t == -1) / 9.0
        alert_ratio = sum(1 for t in trit_vector if t == 1) / 9.0
        zero_ratio = sum(1 for t in trit_vector if t == 0) / 9.0
        
        # 高危险 + 高警戒 + 低不确定 = 高波动 (局势明朗但危险)
        # 高危险 + 高警戒 + 高不确定 = 极高波动 (混乱)
        # 低危险 + 高零值 = 低波动 (平稳)
        trit_vol = (danger_ratio * 0.5 + alert_ratio * 0.3 + (1 - zero_ratio) * 0.2)
        vol_sources.append(trit_vol)
        
        # 来源 2：实时指标波动率
        if metrics and "volatility" in metrics:
            vol_sources.append(metrics["volatility"])
        if metrics and "error_rate_change" in metrics:
            vol_sources.append(min(abs(metrics["error_rate_change"]), 1.0))
        
        # 来源 3：历史策略稳定性
        if memory:
            # 计算坐标
            coord = 0
            for i, t in enumerate(trit_vector):
                digit = t + 1
                coord += digit * (3 ** i)
            
            coord_history = memory.get("strategy_history", {}).get(coord, [])
            if len(coord_history) >= 3:
                # 计算历史成功率的方差
                success_rates = [h.get("success", 0) for h in coord_history[-10:]]
                if success_rates:
                    mean = sum(success_rates) / len(success_rates)
                    variance = sum((s - mean) ** 2 for s in success_rates) / len(success_rates)
                    hist_vol = min(math.sqrt(variance) * 2, 1.0)
                    vol_sources.append(hist_vol)
        
        # 综合：取最大值 (最坏情况驱动)
        if vol_sources:
            # 加权：取最大值和均值的加权
            max_vol = max(vol_sources)
            avg_vol = sum(vol_sources) / len(vol_sources)
            volatility = max_vol * 0.6 + avg_vol * 0.4
        else:
            volatility = 0.3  # 默认中等波动
        
        return min(volatility, 1.0)
    
    def _map_volatility_to_halflife(self, volatility: float) -> float:
        """
        波动率 → 半衰期 (天) 映射 (融合 Triton)
        高波动 → 短半衰期；稳定 → 长半衰期
        """
        if volatility > 0.8:
            return 1.0 / 24  # 1 小时
        elif volatility > 0.6:
            return 1.0  # 1 天
        elif volatility > 0.4:
            return 3.0  # 3 天
        elif volatility > 0.2:
            return 7.0  # 7 天 (默认)
        else:
            return 14.0  # 14 天
    
    def _generate_reason(self, volatility: float, halflife_days: float) -> str:
        """生成自适应原因说明"""
        if volatility > 0.8:
            level = "极高波动"
        elif volatility > 0.6:
            level = "高波动"
        elif volatility > 0.4:
            level = "中等波动"
        elif volatility > 0.2:
            level = "低波动"
        else:
            level = "稳定"
        
        return f"{level}({volatility:.2f}) → 半衰期={halflife_days:.1f}天"
    
    def temporal_evolve(self, vector: List[float], age: float, halflife_days: float) -> List[float]:
        """
        融合 lingzhu 时间演化：根据半衰期调整演化速率
        
        Args:
            vector: 原始向量
            age: 时间年龄 (天)
            halflife_days: 半衰期 (天)
        
        Returns:
            时间演化后的向量
        """
        decay_factor = math.exp(-age / halflife_days)
        return [val * decay_factor for val in vector]


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    scheduler = AdaptiveEHalflife()
    
    # 高危险 = 高波动
    high_vol_trits = [-1, -1, 1, -1, -1, 1, -1, -1, -1]
    # 平稳
    calm_trits = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    print("=" * 60)
    print("e 自适应半衰期调度器融合版测试")
    print("=" * 60)
    
    print("\n高波动态势:")
    result = scheduler.calculate(high_vol_trits)
    print(f"  {result['reason']}")
    
    print("\n平稳态势:")
    result = scheduler.calculate(calm_trits)
    print(f"  {result['reason']}")
