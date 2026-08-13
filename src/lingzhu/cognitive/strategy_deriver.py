"""
三层策略派生引擎

融合 Triton 三层规则 + lingzhu 阴符经修炼
Layer1: 基向量映射 (27 条规则)
Layer2: 关键组合覆盖 (危险坐标强制策略)
Layer3: 邻近 Hamming 距离继承 (稀疏坐标回退)
"""

from typing import List, Dict, Optional, Tuple
import math


class StrategyDeriver:
    """融合策略派生引擎"""
    
    # 九维名称 (可自定义)
    DEFAULT_DIM_NAMES = [
        '过去', '现在', '未来', '内', '中', '外', '因', '缘', '果'
    ]
    
    # Layer1: 基向量映射表 (融合阴符经语义)
    BASE_VECTOR = {
        '过去': {-1: '回顾整理', 0: '保持现状', 1: '吸取教训'},
        '现在': {-1: '谨慎观察', 0: '平衡处理', 1: '积极行动'},
        '未来': {-1: '保守规划', 0: '灵活应对', 1: '进取布局'},
        '内': {-1: '内省收敛', 0: '内在平衡', 1: '内在扩展'},
        '中': {-1: '关系收缩', 0: '关系和谐', 1: '关系扩展'},
        '外': {-1: '环境压力', 0: '环境适应', 1: '环境改造'},
        '因': {-1: '恶因', 0: '无因', 1: '善因'},
        '缘': {-1: '恶缘', 0: '无缘', 1: '善缘'},
        '果': {-1: '恶果', 0: '无果', 1: '善果'},
    }
    
    # Layer2: 关键危险组合 (融合道家危局)
    CRITICAL_RULES = [
        {
            'condition': {'现在': -1, '果': -1, '外': -1},
            'override': {'action': 'emergency_retreat', 'level': 'critical', 'reason': '三危局：当下 + 结果 + 环境全面恶化'},
        },
        {
            'condition': {'未来': 1, '因': 1, '缘': 1},
            'override': {'action': 'aggressive_expand', 'level': 'high', 'reason': '三善局：未来 + 因缘全面向好'},
        },
        {
            'condition': {'内': -1, '中': -1, '外': -1},
            'override': {'action': 'full_contraction', 'level': 'critical', 'reason': '空间三维全面收缩'},
        },
        {
            'condition': {'过去': -1, '现在': -1, '未来': -1},
            'override': {'action': 'temporal_crisis', 'level': 'critical', 'reason': '时间三维全面恶化'},
        },
        {
            'condition': {'因': 1, '果': -1},
            'override': {'action': 'cause_effect_mismatch', 'level': 'high', 'reason': '善因恶果：行动与结果不匹配'},
        },
    ]
    
    def __init__(self, dim_names: List[str] = None, base_vector: Dict = None, critical_rules: List = None):
        self.dim_names = dim_names or self.DEFAULT_DIM_NAMES
        self.base_vector = base_vector or self.BASE_VECTOR
        self.critical_rules = critical_rules or self.CRITICAL_RULES
    
    def derive(self, trit_vector: List[int], memory: Optional[Dict] = None) -> Dict:
        """
        从 Trit 向量派生策略
        
        返回：{"action": str, "level": str, "dim_actions": [...], "derivation_path": str, ...}
        """
        dim_name_map = {i: name for i, name in enumerate(self.dim_names)}
        
        # Layer2 优先：检查关键危险组合
        override_result = self._check_critical_override(trit_vector, dim_name_map)
        if override_result:
            override_result["derivation_path"] = "Layer2_critical_override"
            override_result["trit_vector"] = trit_vector
            return override_result
        
        # Layer1: 基向量映射
        dim_actions = []
        action_tags = []
        for i, trit in enumerate(trit_vector):
            dim_name = dim_name_map.get(i, f"dim_{i}")
            strategy_map = self.base_vector.get(dim_name, {})
            action = strategy_map.get(trit, "unknown")
            dim_actions.append({
                "dimension": dim_name,
                "trit": trit,
                "action": action,
            })
            action_tags.append(action)
        
        # 综合策略
        overall_action = self._synthesize_action(action_tags, trit_vector)
        
        result = {
            "action": overall_action["action"],
            "level": overall_action["level"],
            "dim_actions": dim_actions,
            "derivation_path": "Layer1_base_vector",
            "trit_vector": trit_vector,
            "coord": self._trit_to_coord(trit_vector),
        }
        
        # Layer3: 如果整体 action 是 unknown，尝试邻近继承
        if overall_action["action"] == "unknown" and memory:
            neighbor = self._inherit_from_neighbors(trit_vector, memory)
            if neighbor:
                result["action"] = neighbor["action"]
                result["derivation_path"] = "Layer3_neighbor_inherit"
                result["neighbor_source"] = neighbor.get("coord")
        
        return result
    
    def _check_critical_override(self, trits: List[int], dim_map: Dict) -> Optional[Dict]:
        """检查是否触发关键组合规则"""
        for rule in self.critical_rules:
            match = True
            for dim_name, expected_trit in rule["condition"].items():
                # 找到该维度在 trit_vector 中的位置
                found = False
                for i, name in dim_map.items():
                    if name == dim_name:
                        found = True
                        if trits[i] != expected_trit:
                            match = False
                        break
                if not found:
                    match = False
                if not match:
                    break
            if match:
                return dict(rule["override"])
        return None
    
    def _synthesize_action(self, action_tags: List[str], trits: List[int]) -> Dict:
        """综合各维度 action，生成整体策略"""
        critical_count = sum(1 for a in action_tags if a in (
            'emergency_retreat', 'full_contraction', 'temporal_crisis', 'cause_effect_mismatch'
        ))
        expand_count = sum(1 for a in action_tags if a in (
            'aggressive_expand', '进取布局', '内在扩展', '关系扩展', '环境改造'
        ))
        contract_count = sum(1 for a in action_tags if a in (
            '回顾整理', '谨慎观察', '保守规划', '内省收敛', '关系收缩'
        ))
        maintain_count = sum(1 for a in action_tags if a in (
            '保持现状', '平衡处理', '灵活应对', '内在平衡', '关系和谐'
        ))
        
        if critical_count >= 2:
            return {"action": "emergency_protocol", "level": "critical"}
        elif critical_count == 1 and expand_count >= 1:
            return {"action": "defensive_expand", "level": "high"}
        elif expand_count >= 4:
            return {"action": "aggressive_expand", "level": "low"}
        elif maintain_count >= 7:
            return {"action": "steady_cruise", "level": "none"}
        else:
            # 混合态：根据 9 维 majority 决定倾向
            pos_count = sum(1 for t in trits if t == 1)
            neg_count = sum(1 for t in trits if t == -1)
            if pos_count > neg_count + 2:
                return {"action": "cautious_expand", "level": "low"}
            elif neg_count > pos_count + 2:
                return {"action": "cautious_contract", "level": "medium"}
            else:
                return {"action": "observe_and_wait", "level": "none"}
    
    def _inherit_from_neighbors(self, trits: List[int], memory: Dict, radius: int = 2) -> Optional[Dict]:
        """从 Hamming 距离≤radius 的邻近坐标继承最优策略"""
        coord = self._trit_to_coord(trits)
        candidates = []
        
        for r in range(1, radius + 1):
            neighbors = self._get_hamming_neighbors(trits, r)
            for neighbor_trits in neighbors:
                neighbor_coord = self._trit_to_coord(neighbor_trits)
                hist = memory.get(neighbor_coord, {})
                if hist and hist.get("success_rate", 0) > 0.5:
                    candidates.append({
                        "coord": neighbor_coord,
                        "trits": neighbor_trits,
                        "action": hist.get("best_action"),
                        "success_rate": hist.get("success_rate", 0),
                        "hamming_distance": r,
                    })
        
        if candidates:
            candidates.sort(key=lambda c: (c["success_rate"], -c["hamming_distance"]), reverse=True)
            return candidates[0]
        return None
    
    def _get_hamming_neighbors(self, trits: List[int], distance: int) -> List[List[int]]:
        """生成 Hamming 距离=distance 的所有邻近向量"""
        neighbors = []
        indices = list(range(9))
        from itertools import combinations, product
        
        for changed_indices in combinations(indices, distance):
            for deltas in product([-1, 1], repeat=distance):
                new_trits = list(trits)
                for idx, delta in zip(changed_indices, deltas):
                    new_val = trits[idx] + delta
                    if new_val in (-1, 0, 1):
                        new_trits[idx] = new_val
                    else:
                        break
                else:
                    neighbors.append(new_trits)
        return neighbors
    
    @staticmethod
    def _trit_to_coord(trits: List[int]) -> int:
        """Trit 向量→19683 坐标"""
        coord = 0
        for i, t in enumerate(trits):
            digit = t + 1
            coord += digit * (3 ** i)
        return coord


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    deriver = StrategyDeriver()
    
    scenarios = [
        ("日常平稳", [0, 0, 0, 0, 0, 0, 0, 0, 0]),
        ("未来进取", [0, 0, 1, 0, 0, 0, 1, 1, 1]),
        ("三危局", [0, -1, 0, 0, 0, -1, 0, 0, -1]),
        ("三善局", [0, 0, 1, 0, 0, 0, 1, 1, 0]),
        ("混合态", [1, 0, -1, 0, 1, -1, 0, 1, 0]),
    ]
    
    print("=" * 60)
    print("三层策略派生引擎融合版测试")
    print("=" * 60)
    
    for name, trits in scenarios:
        result = deriver.derive(trits)
        print(f"\n{name}: {trits}")
        print(f"  策略：{result['action']}")
        print(f"  级别：{result['level']}")
        print(f"  路径：{result['derivation_path']}")
        if result.get('neighbor_source'):
            print(f"  邻近源：{result['neighbor_source']}")
