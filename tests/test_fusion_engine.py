"""
融合认知引擎测试套件

测试覆盖率目标：>90%
"""

import pytest
from lingzhu.cognitive.trit_compiler import TritCompiler
from lingzhu.cognitive.strategy_deriver import StrategyDeriver
from lingzhu.cognitive.adaptive_pi import AdaptivePiScheduler
from lingzhu.cognitive.adaptive_e import AdaptiveEHalflife
from lingzhu.cognitive.decision_tracer import DecisionTracer
from lingzhu.cognitive.fusion_engine import FusionCognitionEngine


class TestTritCompiler:
    """Trit 编译器测试"""
    
    @pytest.fixture
    def compiler(self):
        return TritCompiler()
    
    def test_json_parse(self, compiler):
        """测试 JSON 解析"""
        json_str = '{"trit_vector": [1, 0, 1, -1, 0, 0, 1, 1, 0]}'
        trits, confident, info = compiler.compile(json_str)
        assert confident is True
        assert len(trits) == 9
    
    def test_regex_parse(self, compiler):
        """测试正则解析"""
        text = '[+1, 0, +1, -1, 0, 0, +1, +1, 0]'
        trits, confident, info = compiler.compile(text)
        assert confident is True
        assert trits[0] == 1
    
    def test_semantic_parse(self, compiler):
        """测试语义解析"""
        text = '过去需要回顾，现在需要把握，未来需要规划'
        trits, confident, info = compiler.compile(text)
        assert len(trits) == 9
    
    def test_fallback(self, compiler):
        """测试降级为全 0"""
        trits, confident, info = compiler.compile('asdfghjkl')
        assert confident is False
        assert trits == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    def test_coordinate_mapping(self, compiler):
        """测试坐标映射"""
        trits = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        coord = compiler.trit_to_coordinate(trits)
        assert coord == 9841  # 太极状态


class TestStrategyDeriver:
    """策略派生引擎测试"""
    
    @pytest.fixture
    def deriver(self):
        return StrategyDeriver()
    
    def test_steady_state(self, deriver):
        """测试平稳状态"""
        trits = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        result = deriver.derive(trits)
        assert result['action'] == 'steady_cruise'
        assert result['derivation_path'] == 'Layer1_base_vector'
    
    def test_critical_override(self, deriver):
        """测试关键组合覆盖"""
        trits = [0, -1, 0, 0, 0, -1, 0, 0, -1]  # 三危局
        result = deriver.derive(trits)
        assert result['derivation_path'] == 'Layer2_critical_override'
        assert result['level'] == 'critical'


class TestAdaptivePi:
    """π自适应调度器测试"""
    
    @pytest.fixture
    def scheduler(self):
        return AdaptivePiScheduler()
    
    def test_high_urgency_low_familiar(self, scheduler):
        """测试高紧急 + 低熟悉"""
        trits = [1, 0, 1, -1, 0, -1, 0, 1, -1]
        result = scheduler.calculate_depth(trits, {})
        assert result['depth'] >= 7
    
    def test_low_urgency_high_familiar(self, scheduler):
        """测试低紧急 + 高熟悉"""
        trits = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        memory = {"visit_counts": {9841: 100}}
        result = scheduler.calculate_depth(trits, memory)
        assert result['depth'] <= 4


class TestAdaptiveE:
    """e 自适应半衰期调度器测试"""
    
    @pytest.fixture
    def scheduler(self):
        return AdaptiveEHalflife()
    
    def test_high_volatility(self, scheduler):
        """测试高波动"""
        trits = [-1, -1, 1, -1, -1, 1, -1, -1, -1]
        result = scheduler.calculate(trits)
        assert result['halflife_days'] <= 1.0
    
    def test_low_volatility(self, scheduler):
        """测试低波动"""
        trits = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        result = scheduler.calculate(trits)
        assert result['halflife_days'] >= 7.0


class TestDecisionTracer:
    """决策追溯器测试"""
    
    @pytest.fixture
    def tracer(self):
        return DecisionTracer()
    
    def test_trace_generation(self, tracer):
        """测试追溯生成"""
        trace = tracer.trace(
            raw_input={"qps": 15000},
            llm_output='[1,0,1]',
            trit_vector=[1, 0, 1, 0, 0, 0, 0, 0, 0],
            is_confident=True,
            compile_info="test",
            coord=12345,
            pi_result={"depth": 5},
            e_result={"halflife_days": 7.0},
            strategy_result={"action": "test", "level": "low"},
        )
        assert "decision_id" in trace
        assert "summary" in trace
    
    def test_stats(self, tracer):
        """测试统计"""
        tracer.trace(
            raw_input={},
            llm_output='test',
            trit_vector=[0]*9,
            is_confident=True,
            compile_info="test",
            coord=9841,
            pi_result={"depth": 3},
            e_result={"halflife_days": 7.0},
            strategy_result={"action": "test", "level": "none"},
        )
        stats = tracer.stats()
        assert stats["total"] == 1


class TestFusionEngine:
    """融合引擎集成测试"""
    
    @pytest.fixture
    def engine(self):
        return FusionCognitionEngine(mapping='taoist')
    
    def test_full_pipeline(self, engine):
        """测试完整决策流程"""
        llm_output = '{"trit_vector": [1, 0, 1, 0, 0, 0, 1, 1, 0]}'
        metrics = {"volatility": 0.5}
        
        decision = engine.decide(llm_output, metrics)
        
        assert "trit_vector" in decision
        assert "coordinate" in decision
        assert "pi" in decision
        assert "e" in decision
        assert "strategy" in decision
        assert "trace" in decision
        assert decision["safe"] is True
    
    def test_memory_update(self, engine):
        """测试记忆更新"""
        llm_output = '[0, 0, 0, 0, 0, 0, 0, 0, 0]'
        engine.decide(llm_output)
        engine.decide(llm_output)
        
        stats = engine.stats()
        assert stats["total_decisions"] == 2
        assert stats["total_visits"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
