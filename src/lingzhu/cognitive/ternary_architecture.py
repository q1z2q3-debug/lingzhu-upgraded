"""
三元九维认知架构核心实现

基于平衡三进制的全息认知结构空间
3^9 = 19,683 认知状态
"""

import math
import time
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

# 数学常数
PI = math.pi          # 空间常数
E = math.e            # 时间常数
GAMMA = 0.5772156649  # 欧拉 - 马斯刻若尼常数 (因果)


class Ternary(Enum):
    """平衡三进制"""
    YIN = -1      # 阴
    HE = 0        # 和
    YANG = 1      # 阳


@dataclass
class CognitiveVector:
    """
    九维认知向量
    
    维度顺序:
    0-2: 时间 (过去，现在，未来)
    3-5: 空间 (内，中，外)
    6-8: 因果 (因，缘，果)
    """
    time_past: float = 0.0
    time_present: float = 0.0
    time_future: float = 0.0
    
    space_inner: float = 0.0
    space_middle: float = 0.0
    space_outer: float = 0.0
    
    cause_seed: float = 0.0
    cause_condition: float = 0.0
    cause_effect: float = 0.0
    
    def to_list(self) -> List[float]:
        """转为列表"""
        return [
            self.time_past, self.time_present, self.time_future,
            self.space_inner, self.space_middle, self.space_outer,
            self.cause_seed, self.cause_condition, self.cause_effect
        ]
    
    @classmethod
    def from_list(cls, values: List[float]) -> 'CognitiveVector':
        """从列表创建"""
        if len(values) != 9:
            raise ValueError("需要 9 个维度")
        return cls(*values)
    
    @classmethod
    def balanced(cls) -> 'CognitiveVector':
        """完全平衡态 (太极)"""
        return cls()
    
    @classmethod
    def pure_yang(cls) -> 'CognitiveVector':
        """纯阳态 (乾)"""
        return cls(1, 1, 1, 1, 1, 1, 1, 1, 1)
    
    @classmethod
    def pure_yin(cls) -> 'CognitiveVector':
        """纯阴态 (坤)"""
        return cls(-1, -1, -1, -1, -1, -1, -1, -1, -1)


class TernaryEncoder:
    """平衡三进制编码器"""
    
    @staticmethod
    def to_decimal(vector: List[float]) -> int:
        """
        平衡三进制 → 十进制 (0-19682)
        """
        result = 0
        for i, digit in enumerate(vector):
            # 平衡三进制转标准三进制 (-1,0,1 → 0,1,2)
            standard_digit = int(digit) + 1
            result += standard_digit * (3 ** i)
        return result
    
    @staticmethod
    def to_ternary(decimal: int, dimensions: int = 9) -> List[float]:
        """
        十进制 (0-19682) → 平衡三进制
        """
        if decimal < 0 or decimal >= 3 ** dimensions:
            raise ValueError(f"超出范围：0-{3**dimensions-1}")
        
        ternary = []
        for i in range(dimensions):
            # 标准三进制
            digit = (decimal // (3 ** i)) % 3
            # 转平衡三进制 (0,1,2 → -1,0,1)
            balanced_digit = digit - 1
            ternary.append(float(balanced_digit))
        
        return ternary
    
    @staticmethod
    def clamp(value: float) -> float:
        """归一化到 [-1, 0, 1]"""
        if value < -0.5:
            return -1.0
        elif value > 0.5:
            return 1.0
        else:
            return 0.0


class CognitiveMemory:
    """
    三元认知记忆系统
    
    使用 19,683 状态空间存储经验
    时间衰减因子：e
    空间因子：π
    """
    
    def __init__(self, capacity: int = 19683):
        self.capacity = capacity
        self.memory_space: Dict[int, Dict[str, Any]] = {}
        self.e = E
        self.pi = PI
    
    def encode_experience(self, experience: Dict[str, Any]) -> CognitiveVector:
        """将经验编码为认知向量"""
        vector = CognitiveVector()
        
        # 时间维编码
        if 'past' in experience:
            vector.time_past = TernaryEncoder.clamp(experience['past'])
        if 'present' in experience:
            vector.time_present = TernaryEncoder.clamp(experience['present'])
        if 'future' in experience:
            vector.time_future = TernaryEncoder.clamp(experience['future'])
        
        # 空间维编码
        if 'inner' in experience:
            vector.space_inner = TernaryEncoder.clamp(experience['inner'])
        if 'middle' in experience:
            vector.space_middle = TernaryEncoder.clamp(experience['middle'])
        if 'outer' in experience:
            vector.space_outer = TernaryEncoder.clamp(experience['outer'])
        
        # 因果维编码
        if 'cause' in experience:
            vector.cause_seed = TernaryEncoder.clamp(experience['cause'])
        if 'condition' in experience:
            vector.cause_condition = TernaryEncoder.clamp(experience['condition'])
        if 'effect' in experience:
            vector.cause_effect = TernaryEncoder.clamp(experience['effect'])
        
        return vector
    
    def store(self, vector: CognitiveVector, content: Dict[str, Any]) -> int:
        """存储到记忆空间"""
        code = TernaryEncoder.to_decimal(vector.to_list())
        
        self.memory_space[code] = {
            'vector': vector.to_list(),
            'content': content,
            'timestamp': time.time(),
            'strength': 1.0,
            'access_count': 0
        }
        
        return code
    
    def retrieve(self, query_vector: CognitiveVector, max_distance: int = 2) -> List[Dict[str, Any]]:
        """基于相似度检索记忆"""
        query_code = TernaryEncoder.to_decimal(query_vector.to_list())
        
        results = []
        for code, memory in self.memory_space.items():
            # 计算汉明距离
            distance = self._hamming_distance(query_code, code)
            
            if distance <= max_distance:
                # 时间衰减
                age = time.time() - memory['timestamp']
                decay = math.exp(-age / 3600)  # 1 小时衰减周期
                
                # 加权分数
                score = decay * memory['strength'] / (distance + 1)
                
                results.append({
                    **memory,
                    'code': code,
                    'distance': distance,
                    'score': score
                })
        
        # 按分数排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results
    
    def _hamming_distance(self, code1: int, code2: int) -> int:
        """计算两个状态码的汉明距离"""
        vec1 = TernaryEncoder.to_ternary(code1)
        vec2 = TernaryEncoder.to_ternary(code2)
        
        distance = 0
        for v1, v2 in zip(vec1, vec2):
            if v1 != v2:
                distance += 1
        
        return distance


class CognitiveReasoning:
    """
    三元认知推理引擎
    """
    
    def __init__(self):
        self.rules = []
        self.e = E
        self.pi = PI
    
    def add_rule(self, condition: List[float], conclusion: List[float], weight: float = 1.0):
        """添加推理规则"""
        self.rules.append({
            'condition': condition,
            'conclusion': conclusion,
            'weight': weight
        })
    
    def infer(self, premise: CognitiveVector) -> CognitiveVector:
        """基于前提进行推理"""
        premise_list = premise.to_list()
        
        # 累积结论
        conclusion = [0.0] * 9
        total_weight = 0.0
        
        for rule in self.rules:
            # 计算匹配度
            similarity = self._vector_similarity(premise_list, rule['condition'])
            
            if similarity > 0.5:
                weight = rule['weight'] * similarity
                total_weight += weight
                
                # 加权累积
                for i in range(9):
                    conclusion[i] += rule['conclusion'][i] * weight
        
        # 归一化
        if total_weight > 0:
            conclusion = [c / total_weight for c in conclusion]
        
        # 钳制到 [-1, 0, 1]
        conclusion = [TernaryEncoder.clamp(c) for c in conclusion]
        
        return CognitiveVector.from_list(conclusion)
    
    def _vector_similarity(self, v1: List[float], v2: List[float]) -> float:
        """计算向量相似度 (-1 到 1)"""
        if len(v1) != len(v2):
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude1 = math.sqrt(sum(x*x for x in v1))
        magnitude2 = math.sqrt(sum(x*x for x in v2))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)


class CognitiveJudgment:
    """
    三元认知判断系统
    
    因果维使用 γ (欧拉常数)
    """
    
    def __init__(self):
        self.gamma = GAMMA
        self.value_system = self._init_value_system()
    
    def _init_value_system(self) -> Dict[str, List[float]]:
        """初始化价值系统"""
        return {
            'benevolence': [0, 0, 1,  0, 1, 0,  0, 0, 1],  # 仁
            'righteousness': [0, 0, 1,  0, 0, 1,  0, 1, 0],  # 义
            'propriety': [0, 1, 0,  1, 0, 0,  0, 1, 0],  # 礼
            'wisdom': [1, 0, 0,  0, 1, 0,  1, 0, 0],  # 智
            'trustworthiness': [0, 1, 0,  0, 1, 0,  0, 1, 0],  # 信
        }
    
    def evaluate(self, situation: CognitiveVector) -> Dict[str, Any]:
        """评估情境"""
        causal_vector = [situation.cause_seed, situation.cause_condition, situation.cause_effect]
        
        # 因果分析
        causal_score = self._analyze_causality(causal_vector)
        
        # 价值对齐
        alignments = {}
        for virtue, pattern in self.value_system.items():
            alignment = self._calculate_alignment(situation.to_list(), pattern)
            alignments[virtue] = alignment
        
        # 综合判断
        overall = sum(alignments.values()) / len(alignments)
        overall = overall * self.gamma  # 用 γ 调节
        
        return {
            'causal_score': causal_score,
            'virtue_alignments': alignments,
            'overall': TernaryEncoder.clamp(overall),
            'judgment': -1 if overall < -0.3 else (1 if overall > 0.3 else 0)
        }
    
    def _analyze_causality(self, causal: List[float]) -> float:
        """分析因果关系"""
        cause, condition, effect = causal
        
        # 因果一致性
        if cause == effect:
            return cause
        elif condition != 0:
            return condition * self.gamma
        else:
            return 0
    
    def _calculate_alignment(self, state: List[float], pattern: List[float]) -> float:
        """计算与价值模式的对齐度"""
        matches = sum(1 for s, p in zip(state, pattern) if s == p)
        return matches / len(pattern) - 0.5  # 归一化到 [-0.5, 0.5]


class CognitiveDecision:
    """
    三元认知决策系统
    
    空间用 π，时间用 e
    """
    
    def __init__(self):
        self.pi = PI
        self.e = E
    
    def decide(self, situation: CognitiveVector, options: List[Dict[str, Any]]) -> Dict[str, Any]:
        """做出决策"""
        scored_options = []
        
        for option in options:
            # 模拟结果
            outcome = self._simulate_outcome(situation, option)
            
            # 评估价值
            value = self._evaluate_outcome(outcome)
            
            # 计算不确定性 (π因子)
            uncertainty = self._calculate_uncertainty(option) * self.pi
            
            # 时间价值 (e 因子)
            time_value = self._time_value(option) * self.e
            
            # 综合评分
            score = value * (1 - min(uncertainty, 1)) * time_value
            
            scored_options.append({
                'option': option,
                'score': score,
                'outcome': outcome
            })
        
        # 选择最优
        if not scored_options:
            return {'decision': None, 'confidence': 0, 'reason': '无可用选项'}
        
        best = max(scored_options, key=lambda x: x['score'])
        
        return {
            'decision': best['option'],
            'confidence': best['score'],
            'expected_outcome': best['outcome'],
            'reason': self._generate_reason(best)
        }
    
    def _simulate_outcome(self, situation: CognitiveVector, option: Dict[str, Any]) -> CognitiveVector:
        """模拟结果"""
        # 简化实现
        outcome = CognitiveVector()
        outcome.time_future = TernaryEncoder.clamp(option.get('future_impact', 0))
        outcome.space_outer = TernaryEncoder.clamp(option.get('external_effect', 0))
        outcome.cause_effect = TernaryEncoder.clamp(option.get('result', 0))
        return outcome
    
    def _evaluate_outcome(self, outcome: CognitiveVector) -> float:
        """评估结果价值"""
        # 简单加权和
        weights = [0.1, 0.2, 0.2,  0.1, 0.1, 0.1,  0.1, 0.1, 0.1]
        values = outcome.to_list()
        return sum(w * v for w, v in zip(weights, values))
    
    def _calculate_uncertainty(self, option: Dict[str, Any]) -> float:
        """计算不确定性"""
        return option.get('uncertainty', 0.5)
    
    def _time_value(self, option: Dict[str, Any]) -> float:
        """计算时间价值"""
        return option.get('time_value', 1.0)
    
    def _generate_reason(self, result: Dict[str, Any]) -> str:
        """生成决策理由"""
        score = result['score']
        if score > 0.5:
            return "高价值选项，推荐执行"
        elif score > 0:
            return "中等价值，可考虑"
        else:
            return "价值较低，谨慎选择"


class CognitiveArchitecture:
    """
    完整的三元九维认知架构
    
    整合记忆、推理、判断、决策
    """
    
    def __init__(self):
        self.memory = CognitiveMemory()
        self.reasoning = CognitiveReasoning()
        self.judgment = CognitiveJudgment()
        self.decision = CognitiveDecision()
        self.state = CognitiveVector.balanced()
    
    def process(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """处理经验"""
        # 1. 编码
        vector = self.memory.encode_experience(experience)
        
        # 2. 检索相关记忆
        memories = self.memory.retrieve(vector)
        
        # 3. 推理
        inferred = self.reasoning.infer(vector)
        
        # 4. 判断
        judgment = self.judgment.evaluate(inferred)
        
        # 5. 决策 (如果有选项)
        options = experience.get('options', [])
        decision = None
        if options:
            decision = self.decision.decide(inferred, options)
        
        # 6. 存储新经验
        code = self.memory.store(vector, {
            'original': experience,
            'inferred': inferred.to_list(),
            'judgment': judgment,
            'decision': decision
        })
        
        # 7. 更新状态
        self.state = inferred
        
        return {
            'vector': vector.to_list(),
            'code': code,
            'memories': memories[:3],  # 前 3 个相关记忆
            'inferred': inferred.to_list(),
            'judgment': judgment,
            'decision': decision,
            'new_state': self.state.to_list()
        }
    
    def get_state_summary(self) -> Dict[str, str]:
        """获取当前状态摘要"""
        state = self.state.to_list()
        code = TernaryEncoder.to_decimal(state)
        
        summary = {
            'code': code,
            'state_name': self._name_state(state),
            'vector': state
        }
        
        return summary
    
    def _name_state(self, state: List[float]) -> str:
        """给状态命名"""
        if all(s == 0 for s in state):
            return "太极 (完全平衡)"
        elif all(s == 1 for s in state):
            return "乾 (纯阳)"
        elif all(s == -1 for s in state):
            return "坤 (纯阴)"
        else:
            return "动态平衡"
