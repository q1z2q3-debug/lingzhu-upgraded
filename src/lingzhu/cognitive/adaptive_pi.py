"""
π自适应深度调度器

融合 Triton 紧急度×熟悉度公式 + lingzhu 空间编码
根据态势紧急度和坐标熟悉度自动调整π深度
紧急↑ + 熟悉↓ → 高精度；紧急↓ + 熟悉↑ → 快速响应
"""

from typing import List, Dict, Optional
import math


class AdaptivePiScheduler:
    """
    自适应π深度调度器
    融合 Triton 公式 + lingzhu 空间编码
    """
    
    DEFAULT_PI_DIGITS = "314159265358979323846264338327950288419716939937510"
    MIN_DEPTH = 1
    MAX_DEPTH = 10
    DEFAULT_DEPTH = 3
    
    def __init__(self, pi_digits: str = None):
        self.pi_digits = pi_digits or self.DEFAULT_PI_DIGITS
    
    def calculate_depth(self, trit_vector: List[int], memory: Optional[Dict] = None,
                        metrics: Optional[Dict] = None) -> Dict:
        """
        计算自适应π深度
        
        返回：{"depth": int, "digits": str, "urgency": float, "familiarity": float, "reason": str}
        """
        # 因子 1: 紧急度 (0.0~1.0)
        urgency = self._calculate_urgency(trit_vector, metrics)
        
        # 因子 2: 熟悉度 (0.0~1.0)
        familiarity = self._calculate_familiarity(trit_vector, memory)
        
        # 核心公式 (融合 Triton)
        # base=3, urgency 最多 +4, unfamiliarity 最多 +3
        base_depth = self.DEFAULT_DEPTH
        urgency_boost = int(urgency * 4)
        unfamiliarity_penalty = int((1 - familiarity) * 3)
        
        depth = base_depth + urgency_boost + unfamiliarity_penalty
        depth = max(self.MIN_DEPTH, min(self.MAX_DEPTH, depth))
        
        digits = self.pi_digits[:depth]
        
        reason_parts = []
        if urgency > 0.6:
            reason_parts.append(f"高紧急度 ({urgency:.2f})")
        elif urgency > 0.3:
            reason_parts.append(f"中紧急度 ({urgency:.2f})")
        else:
            reason_parts.append(f"低紧急度 ({urgency:.2f})")
        
        if familiarity < 0.3:
            reason_parts.append(f"低熟悉度 ({familiarity:.2f})")
        elif familiarity < 0.6:
            reason_parts.append(f"中熟悉度 ({familiarity:.2f})")
        else:
            reason_parts.append(f"高熟悉度 ({familiarity:.2f})")
        
        reason = " + ".join(reason_parts) + f" → π深度={depth}"
        
        return {
            "depth": depth,
            "digits": digits,
            "urgency": round(urgency, 3),
            "familiarity": round(familiarity, 3),
            "urgency_boost": urgency_boost,
            "unfamiliarity_penalty": unfamiliarity_penalty,
            "reason": reason,
        }
    
    def _calculate_urgency(self, trit_vector: List[int], metrics: Optional[Dict] = None) -> float:
        """
        计算态势紧急度
        - 危险维度数量 (-1 的数量)
        - 危险信号强度
        - 如果有 metrics，结合波动率
        """
        # 基础：危险维度数量
        danger_count = sum(1 for t in trit_vector if t == -1)
        alert_count = sum(1 for t in trit_vector if t == 1)  # 高压信号也增加紧急度
        
        # 关键维度权重：现在 (索引 1)、果 (索引 8)、外 (索引 5) 权重加倍
        weighted_danger = danger_count
        if len(trit_vector) > 1 and trit_vector[1] == -1:
            weighted_danger += 1  # 现在危险 ×2
        if len(trit_vector) > 8 and trit_vector[8] == -1:
            weighted_danger += 1  # 果危险 ×2
        if len(trit_vector) > 5 and trit_vector[5] == -1:
            weighted_danger += 1  # 外危险 ×2
        
        base_urgency = min(weighted_danger / 6.0, 1.0)  # 归一化到 0~1
        
        # 如果提供了实时指标，结合波动率
        if metrics:
            volatility = metrics.get("volatility", 0)
            # 高波动 → 更紧急
            base_urgency = (base_urgency + volatility) / 2
        
        # 混合 alert 和 danger
        combined = base_urgency * 0.7 + (alert_count / 9.0) * 0.3
        
        return min(combined, 1.0)
    
    def _calculate_familiarity(self, trit_vector: List[int], memory: Optional[Dict] = None) -> float:
        """
        计算坐标熟悉度
        - 基于该坐标的历史访问次数
        - 基于邻近坐标的访问密度
        """
        if not memory:
            return 0.3  # 无记忆时返回低熟悉度
        
        # 计算坐标
        coord = 0
        for i, t in enumerate(trit_vector):
            digit = t + 1
            coord += digit * (3 ** i)
        
        # 该坐标的直接访问次数
        visit_count = memory.get("visit_counts", {}).get(coord, 0)
        
        # 邻近坐标的访问密度
        neighbor_count = 0
        neighbor_visits = memory.get("visit_counts", {})
        for neighbor_coord in self._get_neighbor_coords(coord, radius=1):
            neighbor_count += neighbor_visits.get(neighbor_coord, 0)
        
        total_evidence = visit_count * 2 + neighbor_count  # 直接访问权重×2
        max_expected = 50  # 50 次访问视为完全熟悉
        
        familiarity = min(total_evidence / max_expected, 1.0)
        return max(familiarity, 0.1)  # 最低 0.1，避免完全陌生
    
    def _get_neighbor_coords(self, coord: int, radius: int = 1) -> List[int]:
        """获取邻近坐标 (简化版：坐标±偏移)"""
        neighbors = []
        offsets = [3 ** i for i in range(9)]  # 各维度的权重
        for offset in offsets:
            for direction in [-1, 1]:
                neighbor = coord + direction * offset
                if 0 <= neighbor < 19683:
                    neighbors.append(neighbor)
        return neighbors
    
    def get_pi_path(self, depth: int) -> str:
        """获取π展开路径字符串"""
        return self.pi_digits[:min(depth, len(self.pi_digits))]
    
    def spatial_encode_with_depth(self, vector: List[float], depth: int) -> List[float]:
        """
        融合 lingzhu 空间编码：根据π深度调整编码精度
        
        Args:
            vector: 原始向量
            depth: π深度
        
        Returns:
            空间编码后的向量
        """
        encoded = []
        for i, val in enumerate(vector):
            # π用于空间相位编码
            phase = val * math.pi * (i + 1) / 9
            # 根据 depth 调整精度
            if depth >= 7:
                encoded.append(math.sin(phase))  # 高精度
            elif depth >= 4:
                encoded.append(round(math.sin(phase), 3))  # 中精度
            else:
                encoded.append(round(math.sin(phase), 1))  # 低精度
        return encoded


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    scheduler = AdaptivePiScheduler()
    
    # 模拟：已访问 100 次的熟悉坐标
    memory_familiar = {"visit_counts": {8472: 100, 8471: 50, 8473: 50}}
    # 模拟：首次访问的陌生坐标
    memory_new = {"visit_counts": {}}
    
    danger_trits = [1, 0, 1, -1, 0, -1, 0, 1, -1]
    calm_trits = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    print("=" * 60)
    print("π自适应深度调度器融合版测试")
    print("=" * 60)
    
    print("\n危险态势 + 陌生坐标:")
    result = scheduler.calculate_depth(danger_trits, memory_new)
    print(f"  {result['reason']}")
    
    print("\n危险态势 + 熟悉坐标:")
    result = scheduler.calculate_depth(danger_trits, memory_familiar)
    print(f"  {result['reason']}")
    
    print("\n平稳态势 + 熟悉坐标:")
    result = scheduler.calculate_depth(calm_trits, memory_familiar)
    print(f"  {result['reason']}")
