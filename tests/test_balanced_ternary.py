"""
平衡三进制编码器测试套件

测试覆盖率目标：>90%
"""

import pytest
import math
from lingzhu.cognitive.balanced_ternary import (
    BalancedTernaryEncoder,
    encode_state,
    decode_state,
    navigate,
)


class TestBalancedTernaryEncoder:
    """平衡三进制编码器测试"""
    
    @pytest.fixture
    def encoder(self):
        """创建编码器实例"""
        return BalancedTernaryEncoder()
    
    # ========== 基础编码测试 ==========
    
    def test_ternary_to_decimal_taiji(self, encoder):
        """测试太极状态编码"""
        taiji = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        code = encoder.ternary_to_decimal(taiji)
        assert code == 9841, "太极状态码应为 9841"
    
    def test_ternary_to_decimal_qian(self, encoder):
        """测试乾卦状态编码"""
        qian = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        code = encoder.ternary_to_decimal(qian)
        assert code == 19682, "乾卦状态码应为 19682"
    
    def test_ternary_to_decimal_kun(self, encoder):
        """测试坤卦状态编码"""
        kun = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
        code = encoder.ternary_to_decimal(kun)
        assert code == 0, "坤卦状态码应为 0"
    
    def test_decimal_to_ternary_roundtrip(self, encoder):
        """测试往返编解码"""
        original = [0, 1, -1, 0, 1, -1, 0, 1, -1]
        code = encoder.ternary_to_decimal(original)
        decoded = encoder.decimal_to_ternary(code)
        assert decoded == original, "往返编解码应保持一致"
    
    def test_decimal_range(self, encoder):
        """测试十进制范围"""
        assert encoder.ternary_to_decimal([0]*9) == 9841
        assert encoder.ternary_to_decimal([1]*9) == 19682
        assert encoder.ternary_to_decimal([-1]*9) == 0
    
    def test_invalid_decimal(self, encoder):
        """测试无效十进制数"""
        with pytest.raises(ValueError):
            encoder.decimal_to_ternary(-1)
        
        with pytest.raises(ValueError):
            encoder.decimal_to_ternary(19683)
    
    # ========== 向量操作测试 ==========
    
    def test_create_vector(self, encoder):
        """测试创建九维向量"""
        vector = encoder.create_vector(
            time_past=-0.5,
            time_present=0.5,
            time_future=0.7,
            space_inner=0.3,
            space_middle=0.5,
            space_outer=-0.3,
            cause_seed=0.6,
            cause_condition=0.4,
            cause_effect=0.7
        )
        assert len(vector) == 9
        assert all(-1 <= v <= 1 for v in vector)
    
    def test_clamp(self, encoder):
        """测试钳制函数"""
        assert encoder.clamp(-2.0) == -1.0
        assert encoder.clamp(2.0) == 1.0
        assert encoder.clamp(0.5) == 0.5
    
    def test_ternary_clamp(self, encoder):
        """测试三进制钳制"""
        assert encoder.ternary_clamp(-0.6) == -1
        assert encoder.ternary_clamp(0.6) == 1
        assert encoder.ternary_clamp(0.3) == 0
        assert encoder.ternary_clamp(-0.3) == 0
    
    # ========== 距离度量测试 ==========
    
    def test_hamming_distance(self, encoder):
        """测试汉明距离"""
        v1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        v2 = [1, 1, 1, 0, 0, 0, 0, 0, 0]
        distance = encoder.hamming_distance(v1, v2)
        assert distance == 3
    
    def test_euclidean_distance(self, encoder):
        """测试欧式距离"""
        v1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        v2 = [1, 0, 0, 0, 0, 0, 0, 0, 0]
        distance = encoder.euclidean_distance(v1, v2)
        assert abs(distance - 1.0) < 0.001
    
    def test_cosine_similarity(self, encoder):
        """测试余弦相似度"""
        v1 = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        v2 = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        similarity = encoder.cosine_similarity(v1, v2)
        assert abs(similarity - 1.0) < 0.001
    
    def test_ternary_semantic_distance(self, encoder):
        """测试三进制语义距离"""
        v1 = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        v2 = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
        distance = encoder.ternary_semantic_distance(v1, v2)
        assert distance == 4.5  # 9 个维度 × 0.5
    
    # ========== 状态导航测试 ==========
    
    def test_navigate_states(self, encoder):
        """测试状态导航"""
        result = encoder.navigate_states(9841, 19682)
        
        assert 'from' in result
        assert 'to' in result
        assert 'distance' in result
        assert 'path' in result
        assert result['from'] == 9841
        assert result['to'] == 19682
        assert result['distance'] == 9  # 太极到乾卦需要 9 步
    
    def test_navigate_path_steps(self, encoder):
        """测试导航路径步数"""
        result = encoder.navigate_states(9841, 19682)
        
        # 每一步只改变一个维度
        for step in result['path']:
            assert 'step' in step
            assert 'dimension' in step
            assert 'change' in step
    
    # ========== 数学常数测试 ==========
    
    def test_mathematical_constants(self, encoder):
        """测试数学常数定义"""
        assert abs(encoder.PI - math.pi) < 0.0001
        assert abs(encoder.E - math.e) < 0.0001
        assert abs(encoder.GAMMA - 0.5772156649) < 0.0001
    
    def test_spatial_encode(self, encoder):
        """测试空间编码"""
        vector = [0.5] * 9
        encoded = encoder.spatial_encode(vector)
        assert len(encoded) == 9
        assert all(-1 <= v <= 1 for v in encoded)
    
    def test_temporal_evolve(self, encoder):
        """测试时间演化"""
        vector = [1.0] * 9
        evolved = encoder.temporal_evolve(vector, age=100)
        assert len(evolved) == 9
        # 时间衰减后应小于初始值
        assert all(v < 1.0 for v in evolved)
    
    def test_causal_strength(self, encoder):
        """测试因果强度"""
        strength = encoder.causal_strength(5)
        assert strength > 0
        assert strength < 1
    
    def test_combined_accelerate(self, encoder):
        """测试三常数协同加速"""
        vector = [0.5] * 9
        
        store_score = encoder.combined_accelerate(vector, 'store')
        retrieve_score = encoder.combined_accelerate(vector, 'retrieve', age=10, cause_count=5)
        reason_score = encoder.combined_accelerate(vector, 'reason', age=5, cause_count=3)
        
        assert isinstance(store_score, float)
        assert isinstance(retrieve_score, float)
        assert isinstance(reason_score, float)
    
    # ========== 特殊状态测试 ==========
    
    def test_get_state_info_taiji(self, encoder):
        """测试太极状态信息"""
        info = encoder.get_state_info(9841)
        assert info['name'] == '太极'
        assert '平衡' in info.get('balance', '')
    
    def test_get_state_info_qian(self, encoder):
        """测试乾卦状态信息"""
        info = encoder.get_state_info(19682)
        assert info['name'] == '乾'
        assert '纯阳' in info.get('description', '')
    
    def test_get_state_info_kun(self, encoder):
        """测试坤卦状态信息"""
        info = encoder.get_state_info(0)
        assert info['name'] == '坤'
        assert '纯阴' in info.get('description', '')
    
    def test_get_all_special_states(self, encoder):
        """测试获取所有特殊状态"""
        states = encoder.get_all_special_states()
        assert len(states) >= 3  # 至少包含太极、乾、坤
        
        for state in states:
            assert 'code' in state
            assert 'name' in state
    
    # ========== 批量操作测试 ==========
    
    def test_batch_encode(self, encoder):
        """测试批量编码"""
        vectors = [[0.5] * 9, [0.3] * 9, [-0.5] * 9]
        codes = encoder.batch_encode(vectors)
        assert len(codes) == 3
        assert all(isinstance(code, int) for code in codes)
    
    def test_batch_decode(self, encoder):
        """测试批量解码"""
        codes = [9841, 19682, 0]
        vectors = encoder.batch_decode(codes)
        assert len(vectors) == 3
        assert all(len(v) == 9 for v in vectors)
    
    # ========== 缓存测试 ==========
    
    def test_cached_operations(self, encoder):
        """测试缓存操作"""
        # 第一次调用
        code1 = encoder.ternary_to_decimal([0]*9)
        # 第二次调用 (应使用缓存)
        code2 = encoder.ternary_to_decimal([0]*9)
        assert code1 == code2


class TestConvenienceFunctions:
    """便捷函数测试"""
    
    def test_encode_state(self):
        """测试便捷编码函数"""
        vector = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        code = encode_state(vector)
        assert code == 9841
    
    def test_decode_state(self):
        """测试便捷解码函数"""
        code = 9841
        vector = decode_state(code)
        assert vector == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    def test_navigate(self):
        """测试便捷导航函数"""
        result = navigate(9841, 19682)
        assert result['from'] == 9841
        assert result['to'] == 19682


class TestDimensionMappings:
    """维度映射测试"""
    
    def test_default_mapping(self):
        """测试默认映射"""
        encoder = BalancedTernaryEncoder('default')
        assert encoder.dimension_names[0] == '过去'
    
    def test_taoist_mapping(self):
        """测试道家映射"""
        encoder = BalancedTernaryEncoder('taoist')
        assert encoder.dimension_names[0] == '天'
    
    def test_buddhist_mapping(self):
        """测试佛家映射"""
        encoder = BalancedTernaryEncoder('buddhist')
        assert encoder.dimension_names[0] == '过去'
    
    def test_confucian_mapping(self):
        """测试儒家映射"""
        encoder = BalancedTernaryEncoder('confucian')
        assert encoder.dimension_names[0] == '知'


# ========== 性能测试 ==========

class TestPerformance:
    """性能测试"""
    
    @pytest.fixture
    def encoder(self):
        return BalancedTernaryEncoder()
    
    def test_encoding_speed(self, encoder, benchmark):
        """测试编码速度"""
        vector = [0.5] * 9
        benchmark(encoder.ternary_to_decimal, [encoder.ternary_clamp(v) for v in vector])
    
    def test_decoding_speed(self, encoder, benchmark):
        """测试解码速度"""
        code = 9841
        benchmark(encoder.decimal_to_ternary, code)
    
    def test_cached_speed(self, encoder, benchmark):
        """测试缓存速度"""
        code = 9841
        benchmark(encoder.cached_decimal_to_ternary, code)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
