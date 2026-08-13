"""
Decision Tracer - 五维决策全链路可解释性

融合 Triton 全链路追溯 + lingzhu 五蕴观照
每次决策生成完整 JSON 轨迹
记录：原始输入→Trit 向量→坐标→π/e 推导→策略选择→历史依据
"""

import json
import time
from typing import List, Dict, Optional


class DecisionTracer:
    """全链路决策轨迹记录器 (融合版)"""
    
    def __init__(self, trace_dir: Optional[str] = None):
        self.trace_dir = trace_dir
        self.traces: List[Dict] = []
        self.counter = 0
    
    def trace(self,
              raw_input: Dict,
              llm_output: str,
              trit_vector: List[int],
              is_confident: bool,
              compile_info: str,
              coord: int,
              pi_result: Dict,
              e_result: Dict,
              strategy_result: Dict,
              historical_basis: Optional[Dict] = None,
              yinfu_result: Optional[Dict] = None,
              skandhas_result: Optional[Dict] = None) -> Dict:
        """
        生成一条完整的 Decision Trace (融合 lingzhu 五蕴观照)
        """
        self.counter += 1
        timestamp = time.time()
        decision_id = f"d_{coord}_{pi_result['depth']}_{e_result['halflife_days']:.1f}d_{int(timestamp)}"
        
        trace_record = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(timestamp)),
            "decision_id": decision_id,
            "sequence": self.counter,
            "trace": {
                "raw_input": raw_input,
                "llm_compile": {
                    "raw_output": llm_output[:500],  # 截断长输出
                    "is_confident": is_confident,
                    "compile_info": compile_info,
                },
                "trit_vector": trit_vector,
                "coordinate": coord,
                "pi_scheduling": pi_result,
                "e_scheduling": {
                    "halflife_days": e_result["halflife_days"],
                    "volatility": e_result["volatility"],
                    "reason": e_result["reason"],
                },
                "strategy_derivation": {
                    "action": strategy_result.get("action"),
                    "level": strategy_result.get("level"),
                    "derivation_path": strategy_result.get("derivation_path"),
                    "dim_actions": strategy_result.get("dim_actions", []),
                    "neighbor_source": strategy_result.get("neighbor_source"),
                },
                "historical_basis": historical_basis or {},
                "yinfu_practice": yinfu_result or {},
                "skandhas_contemplation": skandhas_result or {},
            },
            "summary": self._generate_summary(
                trit_vector, coord, strategy_result, pi_result, e_result
            ),
        }
        
        self.traces.append(trace_record)
        return trace_record
    
    def _generate_summary(self, trits: List[int], coord: int,
                          strategy: Dict, pi: Dict, e: Dict) -> str:
        """生成可读决策摘要 (融合阴符经语义)"""
        action = strategy.get("action", "unknown")
        path = strategy.get("derivation_path", "unknown")
        pi_depth = pi.get("depth", 3)
        e_days = e.get("halflife_days", 7)
        
        danger_count = sum(1 for t in trits if t == -1)
        alert_count = sum(1 for t in trits if t == 1)
        zero_count = 9 - danger_count - alert_count
        
        # 阴符经语义映射
        if danger_count > 4:
            crisis_level = "阴盛"
        elif alert_count > 4:
            crisis_level = "阳盛"
        elif zero_count > 6:
            crisis_level = "平衡"
        else:
            crisis_level = "混合"
        
        return (
            f"坐标{coord}({crisis_level}) | "
            f"阴{danger_count}/阳{alert_count}/和{zero_count} | "
            f"π深度{pi_depth} | e 半衰{e_days:.1f}天 | "
            f"策略:{action}({path})"
        )
    
    def get_recent_traces(self, n: int = 10) -> List[Dict]:
        """获取最近 n 条轨迹"""
        return self.traces[-n:]
    
    def get_trace_by_coord(self, coord: int, n: int = 5) -> List[Dict]:
        """获取指定坐标的最近 n 条轨迹"""
        matching = [t for t in self.traces if t["trace"]["coordinate"] == coord]
        return matching[-n:]
    
    def export_json(self, filepath: Optional[str] = None) -> str:
        """导出全部轨迹为 JSON"""
        output_path = filepath or f"decision_traces_{int(time.time())}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "version": "2.0.0-fusion",
                "total_decisions": self.counter,
                "traces": self.traces,
            }, f, ensure_ascii=False, indent=2)
        return output_path
    
    def stats(self) -> Dict:
        """轨迹统计"""
        if not self.traces:
            return {"total": 0}
        
        actions = {}
        paths = {}
        coords = {}
        
        for t in self.traces:
            action = t["trace"]["strategy_derivation"]["action"]
            path = t["trace"]["strategy_derivation"]["derivation_path"]
            coord = t["trace"]["coordinate"]
            
            actions[action] = actions.get(action, 0) + 1
            paths[path] = paths.get(path, 0) + 1
            coords[coord] = coords.get(coord, 0) + 1
        
        top_coords = sorted(coords.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total": len(self.traces),
            "top_actions": sorted(actions.items(), key=lambda x: x[1], reverse=True),
            "derivation_paths": paths,
            "unique_coords_visited": len(coords),
            "top_coords": [(c, n) for c, n in top_coords],
            "non_confident_ratio": sum(
                1 for t in self.traces if not t["trace"]["llm_compile"]["is_confident"]
            ) / len(self.traces) if self.traces else 0,
        }


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    tracer = DecisionTracer()
    
    # 模拟一次决策
    trace = tracer.trace(
        raw_input={"qps": 15000, "error_rate": 0.02},
        llm_output='[+1, 0, +1, -1, 0, 0, +1, +1, 0]',
        trit_vector=[1, 0, 1, -1, 0, 0, 1, 1, 0],
        is_confident=True,
        compile_info="json_parse: 9 dims extracted",
        coord=15234,
        pi_result={"depth": 5, "digits": "31415", "urgency": 0.6, "reason": "高紧急度"},
        e_result={"halflife_days": 3.0, "volatility": 0.6, "reason": "高波动"},
        strategy_result={"action": "cautious_expand", "level": "low", "derivation_path": "Layer1_base_vector"},
        historical_basis={"available": True, "success_rate": 0.8},
    )
    
    print("=" * 60)
    print("Decision Tracer 融合版测试")
    print("=" * 60)
    print(f"\n决策摘要：{trace['summary']}")
    print(f"\n完整轨迹：{json.dumps(trace, ensure_ascii=False, indent=2)}")
