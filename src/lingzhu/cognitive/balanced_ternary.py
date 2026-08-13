"""
平衡三进制编码器

三元九维认知架构的数学基础
3^9 = 19,683 全息认知状态空间
"""

import math
from typing import List, Tuple, Dict, Any
from functools import lru_cache


class BalancedTernaryEncoder:
    """
    平衡三进制编码器
    
    核心功能:
    - 三进制 ↔ 十进制转换
    - 九维向量编码
    - 19,683 状态空间映射
    """
    
    # 数学常数
    PI = math.pi          # 空间常数 3.14159...
    E = math.e            # 时间常数 2.71828...
    GAMMA = 0.5772156649  # 因果常数 (欧拉 - 马斯刻若尼常数)
    
    # 状态空间大小
    STATE_SPACE_SIZE = 3 ** 9  # 19,683
    
    # 特殊状态码
    SPECIAL_STATES = {
        0: {'name': '坤', 'description': '纯阴态，收敛沉淀', 'element': '地'},
        9841: {'name': '太极', 'description': '完全平衡，空性', 'element': '道'},
        19682: {'name': '乾', 'description': '纯阳态，创造扩张', 'element': '天'},
    }
    
    # 维度名称 (可配置)
    DIMENSION_NAMES = {
        'default': ['过去', '现在', '未来', '内', '中', '外', '因', '缘', '果'],
        'taoist': ['天', '地', '人', '时', '势', '空', '因', '缘', '果'],
        'buddhist': ['过去', '现在', '未来', '内', '中', '外', '因', '缘', '果'],
        'confucian': ['知', '行', '意', '内', '中', '外', '因', '缘', '果'],
    }
    
    def __init__(self, mapping: str = 'default'):
        """
        初始化编码器
        
        Args:
            mapping: 维度映射模式 ('default', 'taoist', 'buddhist', 'confucian')
        """
        self.mapping = mapping
        self.dimension_names = self.DIMENSION_NAMES.get(mapping, self.DIMENSION_NAMES['default'])
    
    # ========== 基础编码转换 ==========
    
    def ternary_to_decimal(self, ternary: List[int]) -> int:
        """
        平衡三进制转十进制
        
        Args:
            ternary: 平衡三进制列表 [-1, 0, 1]
        
        Returns:
            十进制数 (0-19682)
        
        Example:
            >>> encoder = BalancedTernaryEncoder()
            >>> encoder.ternary_to_decimal([0,0,0,0,0,0,0,0,0])
            9841  # 太极状态
        """
        decimal = 0
        for i, digit in enumerate(ternary):
            # 平衡三进制转标准三进制 (-1,0,1 → 0,1,2)
            standard = digit + 1
            decimal += standard * (3 ** i)
        return decimal
    
    def decimal_to_ternary(self, decimal: int) -> List[int]:
        """
        十进制转平衡三进制
        
        Args:
            decimal: 十进制数 (0-19682)
        
        Returns:
            平衡三进制列表 [-1, 0, 1]
        
        Example:
            >>> encoder = BalancedTernaryEncoder()
            >>> encoder.decimal_to_ternary(9841)
            [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 太极状态
        """
        if decimal < 0 or decimal >= self.STATE_SPACE_SIZE:
            raise ValueError(f"十进制数必须在 0-{self.STATE_SPACE_SIZE-1} 范围内")
        
        ternary = []
        for i in range(9):
            # 标准三进制
            digit = (decimal // (3 ** i)) % 3
            # 转平衡三进制 (0,1,2 → -1,0,1)
            balanced = digit - 1
            ternary.append(balanced)
        
        return ternary
    
    @lru_cache(maxsize=19683)
    def cached_decimal_to_ternary(self, decimal: int) -> Tuple[int, ...]:
        """
        缓存版十进制转三进制 (性能优化)
        
        Returns:
            元组 (可哈希，适合缓存)
        """
        return tuple(self.decimal_to_ternary(decimal))
    
    # ========== 九维向量操作 ==========
    
    def create_vector(self, **kwargs) -> List[float]:
        """
        创建九维向量
        
        Args:
            任意维度参数
        
        Returns:
            九维向量列表
        
        Example:
            >>> vector = encoder.create_vector(
            ...     time_past=-0.5, time_present=0.5, time_future=0.7,
            ...     space_inner=0.3, space_middle=0.5, space_outer=-0.3,
            ...     cause_seed=0.6, cause_condition=0.4, cause_effect=0.7
            ... )
        """
        vector = [0.0] * 9
        
        dimension_map = {
            'time_past': 0, 'time_present': 1, 'time_future': 2,
            'space_inner': 3, 'space_middle': 4, 'space_outer': 5,
            'cause_seed': 6, 'cause_condition': 7, 'cause_effect': 8,
        }
        
        for key, value in kwargs.items():
            if key in dimension_map:
                vector[dimension_map[key]] = self.clamp(value)
        
        return vector
    
    def clamp(self, value: float) -> float:
        """
        钳制到 [-1, 1] 范围
        
        三进制的核心：-1 (阴), 0 (和), 1 (阳)
        """
        if value < -1.0:
            return -1.0
        elif value > 1.0:
            return 1.0
        return value
    
    def ternary_clamp(self, value: float) -> int:
        """
        钳制到平衡三进制 [-1, 0, 1]
        
        这是认知状态的核心操作
        """
        if value < -0.5:
            return -1  # 阴
        elif value > 0.5:
            return 1   # 阳
        else:
            return 0   # 和 ← 涌现态
    
    # ========== 状态空间导航 ==========
    
    def hamming_distance(self, v1: List[int], v2: List[int]) -> int:
        """
        汉明距离：不同维度的数量
        
        用于：状态分类、快速检索、状态空间导航
        """
        return sum(1 for a, b in zip(v1, v2) if a != b)
    
    def euclidean_distance(self, v1: List[float], v2: List[float]) -> float:
        """
        欧式距离：几何距离
        
        用于：相似度计算、聚类分析
        """
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))
    
    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """
        余弦相似度：方向相似度
        
        用于：语义相似性、推荐系统
        """
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude1 = math.sqrt(sum(a ** 2 for a in v1))
        magnitude2 = math.sqrt(sum(b ** 2 for b in v2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def ternary_semantic_distance(self, v1: List[int], v2: List[int]) -> float:
        """
        三进制语义距离
        
        考虑阴阳和的哲学语义:
        - 相同：0
        - 和与阴/阳：0.5
        - 阴与阳：1
        """
        distance = 0.0
        for a, b in zip(v1, v2):
            if a == b:
                distance += 0
            elif a == 0 or b == 0:
                distance += 0.5  # 和与阴/阳的距离
            else:
                distance += 1.0  # 阴与阳的距离
        return distance
    
    def navigate_states(self, from_code: int, to_code: int) -> Dict[str, Any]:
        """
        状态空间导航
        
        生成从一个认知状态到另一个状态的转化路径
        
        Args:
            from_code: 起始状态码
            to_code: 目标状态码
        
        Returns:
            导航路径信息
        
        Example:
            >>> result = encoder.navigate_states(9841, 19682)
            >>> print(f"从太极到乾卦需要{result['distance']}步")
        """
        from_ternary = self.decimal_to_ternary(from_code)
        to_ternary = self.decimal_to_ternary(to_code)
        
        # 计算汉明距离
        distance = self.hamming_distance(from_ternary, to_ternary)
        
        # 生成路径 (每一步改变一个维度)
        path = []
        current = from_ternary.copy()
        
        for step in range(distance):
            for i in range(9):
                if current[i] != to_ternary[i]:
                    old_val = current[i]
                    current[i] = to_ternary[i]
                    path.append({
                        'step': step + 1,
                        'state': self.ternary_to_decimal(current),
                        'dimension': self.dimension_names[i],
                        'dimension_index': i,
                        'change': f"{old_val} → {to_ternary[i]}",
                        'change_meaning': self._get_change_meaning(old_val, to_ternary[i])
                    })
                    break
        
        return {
            'from': from_code,
            'to': to_code,
            'from_name': self.SPECIAL_STATES.get(from_code, {}).get('name', '普通态'),
            'to_name': self.SPECIAL_STATES.get(to_code, {}).get('name', '普通态'),
            'distance': distance,
            'path': path,
            'from_ternary': from_ternary,
            'to_ternary': to_ternary
        }
    
    def _get_change_meaning(self, old_val: int, new_val: int) -> str:
        """获取维度变化的哲学含义"""
        meanings = {
            (-1, 0): "阴→和：收敛转平衡",
            (-1, 1): "阴→阳：收敛转扩张",
            (0, -1): "和→阴：平衡转收敛",
            (0, 1): "和→阳：平衡转扩张",
            (1, -1): "阳→阴：扩张转收敛",
            (1, 0): "阳→和：扩张转平衡",
        }
        return meanings.get((old_val, new_val), "状态转化")
    
    # ========== 数学常数加速 ==========
    
    def spatial_encode(self, vector: List[float]) -> List[float]:
        """
        空间编码 (π加速)
        
        利用π的周期性和超越性进行空间相位编码
        """
        encoded = []
        for i, val in enumerate(vector):
            # π用于空间相位编码
            phase = val * self.PI * (i + 1) / 9
            encoded.append(math.sin(phase))
        return encoded
    
    def temporal_evolve(self, vector: List[float], age: float) -> List[float]:
        """
        时间演化 (e 加速)
        
        利用 e 的自然增长/衰减特性
        """
        decay_factor = self.E ** (-age / 100)  # 100 为时间常数
        return [val * decay_factor for val in vector]
    
    def causal_strength(self, cause_chain_length: int) -> float:
        """
        因果强度计算 (γ加速)
        
        利用γ的调和级数特性
        """
        harmonic_sum = sum(1/i for i in range(1, cause_chain_length + 1))
        return (harmonic_sum - self.GAMMA) * self.GAMMA
    
    def combined_accelerate(self, vector: List[float], operation: str, 
                           age: float = 0, cause_count: int = 1) -> float:
        """
        三常数协同加速
        
        π(空间) × e(时间) × γ(因果)
        
        Args:
            vector: 认知向量
            operation: 操作类型 ('store', 'retrieve', 'reason')
            age: 时间年龄
            cause_count: 因果链长度
        
        Returns:
            加速后的相关性分数
        """
        if operation == 'store':
            # 存储：空间编码 (π) + 时间标记 (e)
            spatial = self.spatial_encode(vector)
            return sum(spatial) / len(spatial)
        
        elif operation == 'retrieve':
            # 检索：空间匹配 (π) + 时间衰减 (e) + 因果强度 (γ)
            spatial_factor = sum(self.spatial_encode(vector)) / len(vector)
            temporal_factor = self.E ** (-age / 100)
            causal_factor = self.causal_strength(cause_count)
            
            return spatial_factor * temporal_factor * causal_factor
        
        elif operation == 'reason':
            # 推理：三常数协同
            spatial = self.spatial_encode(vector)
            temporal = self.temporal_evolve(spatial, age)
            causal = self.causal_strength(cause_count)
            
            return sum(temporal) * causal
        
        return 0.0
    
    # ========== 特殊状态查询 ==========
    
    def get_state_info(self, code: int) -> Dict[str, Any]:
        """
        获取状态信息
        
        Returns:
            状态的详细信息 (名称、描述、元素等)
        """
        if code in self.SPECIAL_STATES:
            return self.SPECIAL_STATES[code]
        
        # 计算状态的阴阳平衡
        ternary = self.decimal_to_ternary(code)
        yin_count = sum(1 for v in ternary if v == -1)
        yang_count = sum(1 for v in ternary if v == 1)
        he_count = sum(1 for v in ternary if v == 0)
        
        return {
            'name': f'状态{code}',
            'yin': yin_count,
            'yang': yang_count,
            'he': he_count,
            'balance': '平衡' if he_count >= 5 else ('偏阴' if yin_count > yang_count else '偏阳'),
            'ternary': ternary
        }
    
    def get_all_special_states(self) -> List[Dict[str, Any]]:
        """获取所有特殊状态"""
        return [
            {'code': code, **info}
            for code, info in self.SPECIAL_STATES.items()
        ]
    
    # ========== 性能优化方法 ==========
    
    def batch_encode(self, vectors: List[List[float]]) -> List[int]:
        """
        批量编码 (性能优化)
        
        将多个向量批量编码为状态码
        """
        codes = []
        for vector in vectors:
            ternary = [self.ternary_clamp(v) for v in vector]
            code = self.ternary_to_decimal(ternary)
            codes.append(code)
        return codes
    
    def batch_decode(self, codes: List[int]) -> List[List[int]]:
        """
        批量解码 (性能优化)
        
        将多个状态码批量解码为三进制向量
        """
        return [self.decimal_to_ternary(code) for code in codes]
    
    @lru_cache(maxsize=1000)
    def cached_state_info(self, code: int) -> Dict[str, Any]:
        """缓存版状态信息查询"""
        return self.get_state_info(code)


# ========== 便捷函数 ==========

def encode_state(vector: List[float], mapping: str = 'default') -> int:
    """便捷函数：编码状态"""
    encoder = BalancedTernaryEncoder(mapping)
    ternary = [encoder.ternary_clamp(v) for v in vector]
    return encoder.ternary_to_decimal(ternary)


def decode_state(code: int, mapping: str = 'default') -> List[int]:
    """便捷函数：解码状态"""
    encoder = BalancedTernaryEncoder(mapping)
    return encoder.decimal_to_ternary(code)


def navigate(from_code: int, to_code: int, mapping: str = 'default') -> Dict[str, Any]:
    """便捷函数：状态导航"""
    encoder = BalancedTernaryEncoder(mapping)
    return encoder.navigate_states(from_code, to_code)


# ========== 使用示例 ==========

if __name__ == "__main__":
    print("=" * 60)
    print("  平衡三进制编码器演示")
    print("=" * 60)
    print()
    
    encoder = BalancedTernaryEncoder(mapping='default')
    
    # 1. 基础编码演示
    print("1️⃣  基础编码演示")
    print("-" * 60)
    
    # 太极状态 (全 0)
    taiji_ternary = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    taiji_code = encoder.ternary_to_decimal(taiji_ternary)
    print(f"太极状态：{taiji_ternary} → 状态码：{taiji_code}")
    
    # 乾卦 (全阳)
    qian_ternary = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    qian_code = encoder.ternary_to_decimal(qian_ternary)
    print(f"乾卦状态：{qian_ternary} → 状态码：{qian_code}")
    
    # 坤卦 (全阴)
    kun_ternary = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    kun_code = encoder.ternary_to_decimal(kun_ternary)
    print(f"坤卦状态：{kun_ternary} → 状态码：{kun_code}")
    print()
    
    # 2. 状态空间导航
    print("2️⃣  状态空间导航")
    print("-" * 60)
    
    result = encoder.navigate_states(9841, 19682)
    print(f"从 {result['from_name']} (太极) 到 {result['to_name']} (乾卦)")
    print(f"汉明距离：{result['distance']} 步")
    print("转化路径:")
    for step in result['path'][:3]:  # 显示前 3 步
        print(f"  第{step['step']}步：{step['dimension']} {step['change_meaning']}")
    print()
    
    # 3. 三常数加速
    print("3️⃣  三常数加速演示")
    print("-" * 60)
    
    test_vector = [0.3, 0.5, 0.7, 0.4, 0.5, -0.3, 0.6, 0.4, 0.7]
    
    store_score = encoder.combined_accelerate(test_vector, 'store')
    retrieve_score = encoder.combined_accelerate(test_vector, 'retrieve', age=10, cause_count=5)
    reason_score = encoder.combined_accelerate(test_vector, 'reason', age=5, cause_count=3)
    
    print(f"存储加速分数：{store_score:.4f}")
    print(f"检索加速分数：{retrieve_score:.4f}")
    print(f"推理加速分数：{reason_score:.4f}")
    print()
    
    # 4. 特殊状态
    print("4️⃣  特殊状态查询")
    print("-" * 60)
    
    for state in encoder.get_all_special_states():
        print(f"状态码 {state['code']}: {state['name']} - {state['description']}")
    print()
    
    print("=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)
