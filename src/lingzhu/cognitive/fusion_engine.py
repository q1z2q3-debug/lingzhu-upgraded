"""
融合认知引擎 - Triton×lingzhu 完整集成

Pipeline: LLM 输出 → Trit 编译 → 坐标映射 → π/e 自适应 → 策略派生 → 阴符经修炼 → 全链路追溯
"""

from typing import List, Dict, Optional
from .trit_compiler import TritCompiler
from .strategy_deriver import StrategyDeriver
from .adaptive_pi import AdaptivePiScheduler
from .adaptive_e import AdaptiveEHalflife
from .decision_tracer import DecisionTracer


class FusionCognitionEngine:
    """
    融合认知引擎核心编排器
    接收 LLM 原始输出和业务指标，输出确定性策略 + 全链路追溯 + 阴符经修炼
    """
    
    def __init__(self,
                 dim_names: List[str] = None,
                 base_vector: Dict = None,
                 critical_rules: List = None,
                 trace_dir: Optional[str] = None,
                 mapping: str = 'default'):
        """
        初始化融合引擎
        
        Args:
            dim_names: 九维名称列表
            base_vector: 基向量映射表
            critical_rules: 关键规则列表
            trace_dir: 追溯文件目录
            mapping: 维度映射模式 ('default'/'ops'/'finance'/'taoist')
        """
        self.compiler = TritCompiler(mapping=mapping)
        self.strategy_deriver = StrategyDeriver(
            dim_names=dim_names,
            base_vector=base_vector,
            critical_rules=critical_rules
        )
        self.pi_scheduler = AdaptivePiScheduler()
        self.e_scheduler = AdaptiveEHalflife()
        self.tracer = DecisionTracer(trace_dir=trace_dir)
        self.memory: Dict = {}
        
        # 延迟导入 lingzhu 模块 (避免循环依赖)
        self._yinfu = None
        self._skandhas = None
    
    def _load_lingzhu_modules(self):
        """延迟加载 lingzhu 模块"""
        if self._yinfu is None:
            try:
                from .yinfu_practice import YinfuPractice
                self._yinfu = YinfuPractice()
            except ImportError:
                self._yinfu = None
        
        if self._skandhas is None:
            try:
                from .xinjing_five_skandhas import FiveSkandhasEmptiness
                self._skandhas = FiveSkandhasEmptiness()
            except ImportError:
                self._skandhas = None
    
    def decide(self,
               llm_raw_output: str,
               metrics: Optional[Dict] = None) -> Dict:
        """
        执行一次完整的融合认知决策
        
        Args:
            llm_raw_output: LLM 的原始输出 (任意格式)
            metrics: 业务指标，如 {"qps": 15000, "error_rate": 0.02, ...}
        
        Returns:
            {
                "trit_vector": [...],
                "coordinate": int,
                "is_confident": bool,
                "pi": {...},
                "e": {...},
                "strategy": {...},
                "yinfu": {...},  # 阴符经修炼结果
                "skandhas": {...},  # 五蕴观照结果
                "trace": {...},
                "safe": bool
            }
        """
        # Step 1: Trit 编译 (LLM 输出 → 确定性向量)
        trit_vector, is_confident, compile_info = self.compiler.compile(llm_raw_output)
        
        # Step 2: 坐标映射
        coord = self.compiler.trit_to_coordinate(trit_vector)
        
        # Step 3: π自适应调度
        pi_result = self.pi_scheduler.calculate_depth(trit_vector, self.memory, metrics)
        
        # Step 4: e 自适应调度
        e_result = self.e_scheduler.calculate(trit_vector, self.memory, metrics)
        
        # Step 5: 策略派生
        strategy = self.strategy_deriver.derive(trit_vector, self.memory)
        
        # Step 6: 历史依据查询
        hist_basis = self._query_history(coord, strategy)
        
        # Step 7: 阴符经修炼 (lingzhu 融合)
        yinfu_result = None
        if self._yinfu:
            self._load_lingzhu_modules()
            yinfu_result = self._yinfu.daily_practice(
                situation={"coord": coord, "vector": trit_vector},
                intention=strategy.get("action", "observe")
            )
        
        # Step 8: 五蕴观照 (lingzhu 融合)
        skandhas_result = None
        if self._skandhas:
            self._load_lingzhu_modules()
            skandhas_result = self._skandhas.contemplate_five_skandhas(trit_vector)
        
        # Step 9: Decision Trace
        trace = self.tracer.trace(
            raw_input=metrics or {},
            llm_output=llm_raw_output,
            trit_vector=trit_vector,
            is_confident=is_confident,
            compile_info=compile_info,
            coord=coord,
            pi_result=pi_result,
            e_result=e_result,
            strategy_result=strategy,
            historical_basis=hist_basis,
            yinfu_result=yinfu_result,
            skandhas_result=skandhas_result,
        )
        
        # Step 10: 更新记忆
        self._update_memory(coord, strategy, is_confident)
        
        return {
            "trit_vector": trit_vector,
            "coordinate": coord,
            "is_confident": is_confident,
            "compile_info": compile_info,
            "pi": pi_result,
            "e": e_result,
            "strategy": strategy,
            "yinfu": yinfu_result,
            "skandhas": skandhas_result,
            "trace": trace,
            "safe": True,  # 编译失败时向量全 0，策略为 observe_and_wait，始终安全
        }
    
    def _query_history(self, coord: int, strategy: Dict) -> Dict:
        """查询该坐标下的历史决策效果"""
        history = self.memory.get("strategy_history", {}).get(coord, [])
        if not history:
            return {"available": False}
        
        actions = [h for h in history if h.get("action") == strategy.get("action")]
        success_count = sum(1 for a in actions if a.get("success"))
        
        return {
            "available": True,
            "total_visits": len(history),
            "same_action_count": len(actions),
            "same_action_success_rate": round(
                success_count / len(actions), 2
            ) if actions else 0,
        }
    
    def _update_memory(self, coord: int, strategy: Dict, is_confident: bool):
        """更新内存中的坐标访问记录"""
        if "strategy_history" not in self.memory:
            self.memory["strategy_history"] = {}
        if "visit_counts" not in self.memory:
            self.memory["visit_counts"] = {}
        
        # 访问计数
        self.memory["visit_counts"][coord] = self.memory["visit_counts"].get(coord, 0) + 1
        
        # 策略记录 (实际应用中需要后续反馈来更新 success 字段)
        record = {
            "action": strategy.get("action"),
            "level": strategy.get("level"),
            "is_confident": is_confident,
            "success": None,  # 待后续反馈
        }
        if coord not in self.memory["strategy_history"]:
            self.memory["strategy_history"][coord] = []
        self.memory["strategy_history"][coord].append(record)
    
    def feedback(self, coord: int, success: bool):
        """对最近一次该坐标的策略提供成功/失败反馈"""
        history = self.memory.get("strategy_history", {}).get(coord, [])
        if history:
            history[-1]["success"] = success
    
    def stats(self) -> Dict:
        """引擎运行统计"""
        return {
            "total_decisions": self.tracer.counter,
            "trace_stats": self.tracer.stats(),
            "memory_coords": len(self.memory.get("visit_counts", {})),
            "total_visits": sum(self.memory.get("visit_counts", {}).values()),
        }
    
    def export_traces(self, filepath: Optional[str] = None) -> str:
        """导出全部决策轨迹"""
        return self.tracer.export_json(filepath)


# ============================================================
# 融合引擎快速使用
# ============================================================

if __name__ == "__main__":
    engine = FusionCognitionEngine(mapping='taoist')
    
    # 模拟 LLM 输出
    llm_output = """
    当前态势分析：
    过去经验需要回顾 (+1)，
    当下需要谨慎观察 (-1)，
    未来应该进取布局 (+1)，
    内在保持平衡 (0)，
    关系需要扩展 (+1)，
    环境有压力 (-1)，
    善因已种 (+1)，
    善缘成熟 (+1)，
    善果待收 (0)。
    
    向量：[+1, -1, +1, 0, +1, -1, +1, +1, 0]
    """
    
    metrics = {
        "volatility": 0.6,
        "qps": 15000,
        "error_rate": 0.02,
    }
    
    decision = engine.decide(llm_output, metrics)
    
    print("=" * 60)
    print("融合认知引擎决策结果")
    print("=" * 60)
    print(f"\nTrit 向量：{decision['trit_vector']}")
    print(f"19683 坐标：{decision['coordinate']}")
    print(f"LLM 确定：{decision['is_confident']}")
    print(f"\nπ调度：深度={decision['pi']['depth']}, 紧急度={decision['pi']['urgency']}")
    print(f"e 调度：半衰期={decision['e']['halflife_days']}天，波动率={decision['e']['volatility']}")
    print(f"\n策略：{decision['strategy']['action']}")
    print(f"级别：{decision['strategy']['level']}")
    print(f"派生路径：{decision['strategy']['derivation_path']}")
    print(f"安全：{decision['safe']}")
    print(f"\n决策摘要：{decision['trace']['summary']}")
    
    if decision['yinfu']:
        print(f"\n阴符经修炼：{decision['yinfu'].get('summary', 'N/A')}")
    
    if decision['skandhas']:
        print(f"\n五蕴观照：{decision['skandhas'].get('summary', 'N/A')}")
    
    print(f"\n引擎统计：{engine.stats()}")
