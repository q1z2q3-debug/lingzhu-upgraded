"""
阴符经认知修炼系统

将道家最高智慧《阴符经》内化为可工程的认知架构
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import math

from lingzhu.cognitive import (
    CognitiveArchitecture,
    CognitiveVector,
    TernaryEncoder,
    PI, E, GAMMA
)


class YinfuObserver:
    """
    观天之道 — 阴符经觉察系统
    
    《阴符经》: "天性，人也；人心，机也。"
    """
    
    def __init__(self):
        self.observation_log = []
        
    def observe_nine_dimensions(self, situation: Dict[str, Any]) -> CognitiveVector:
        """
        观天之道 — 觉察九维
        
        觉察时间、空间、因果九个维度
        """
        vector = CognitiveVector()
        
        # 觉察时间三维 (天)
        vector.time_past = self._observe_past(situation.get('past_experience', []))
        vector.time_present = self._observe_present(situation.get('present_awareness', 0))
        vector.time_future = self._observe_future(situation.get('future_expectation', 0))
        
        # 觉察空间三维 (地)
        vector.space_inner = self._observe_inner(situation.get('inner_state', 0))
        vector.space_middle = self._observe_middle(situation.get('relation_dynamic', 0))
        vector.space_outer = self._observe_outer(situation.get('outer_environment', 0))
        
        # 觉察因果三维 (人)
        vector.cause_seed = self._observe_cause(situation.get('initial_motive', 0))
        vector.cause_condition = self._observe_condition(situation.get('current_condition', 0))
        vector.cause_effect = self._observe_effect(situation.get('expected_result', 0))
        
        # 记录觉察
        self.observation_log.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'vector': vector.to_list(),
            'situation': situation
        })
        
        return vector
    
    def _observe_past(self, experiences: List) -> float:
        """觉察过去 — 经验的沉淀"""
        if not experiences:
            return 0.0
        
        # 负面经验多 → 阴 (-1)
        # 平衡 → 和 (0)
        # 正面经验多 → 阳 (+1)
        positive = sum(1 for e in experiences if e.get('valence', 0) > 0)
        negative = sum(1 for e in experiences if e.get('valence', 0) < 0)
        
        if positive > negative:
            return 0.5  # 阳
        elif negative > positive:
            return -0.5  # 阴
        else:
            return 0.0  # 和
    
    def _observe_present(self, awareness: float) -> float:
        """觉察当下 — 临在的程度"""
        return TernaryEncoder.clamp(awareness)
    
    def _observe_future(self, expectation: float) -> float:
        """觉察未来 — 预期的倾向"""
        return TernaryEncoder.clamp(expectation)
    
    def _observe_inner(self, inner_state: float) -> float:
        """觉察内在 — 身心状态"""
        return TernaryEncoder.clamp(inner_state)
    
    def _observe_middle(self, relation: float) -> float:
        """觉察关系 — 互动动态"""
        return TernaryEncoder.clamp(relation)
    
    def _observe_outer(self, environment: float) -> float:
        """觉察外在 — 环境压力"""
        return TernaryEncoder.clamp(environment)
    
    def _observe_cause(self, motive: float) -> float:
        """觉察起因 — 初始动机"""
        return TernaryEncoder.clamp(motive)
    
    def _observe_condition(self, condition: float) -> float:
        """觉察条件 — 当下因缘"""
        return TernaryEncoder.clamp(condition)
    
    def _observe_effect(self, result: float) -> float:
        """觉察结果 — 预期成效"""
        return TernaryEncoder.clamp(result)
    
    def get_observation_summary(self) -> Dict[str, Any]:
        """获取觉察总结"""
        if not self.observation_log:
            return {'count': 0, 'message': '暂无觉察记录'}
        
        recent = self.observation_log[-10:]
        avg_vector = [sum(v[i] for v in [r['vector'] for r in recent]) / len(recent) 
                     for i in range(9)]
        
        return {
            'count': len(self.observation_log),
            'recent_average': avg_vector,
            'trend': self._analyze_trend(recent),
            'last_observation': self.observation_log[-1] if recent else None
        }
    
    def _analyze_trend(self, recent_logs: List) -> str:
        """分析觉察趋势"""
        if len(recent_logs) < 2:
            return "数据不足"
        
        first_half = recent_logs[:len(recent_logs)//2]
        second_half = recent_logs[len(recent_logs)//2:]
        
        avg_first = sum(sum(v) for r in first_half for v in [r['vector']]) / len(first_half)
        avg_second = sum(sum(v) for r in second_half for v in [r['vector']]) / len(second_half)
        
        if abs(avg_second - avg_first) < 0.3:
            return "稳定"
        elif avg_second > avg_first:
            return "向阳转化"
        else:
            return "向阴转化"


class YinfuTransformer:
    """
    执天之行 — 阴符经转化系统
    
    《阴符经》: "天发杀机，移星易宿；地发杀机，龙蛇起陆；人发杀机，天地反覆。"
    """
    
    # 五行对应认知维度
    FIVE_ELEMENTS = {
        'wood': {'dimension': 'time_future', 'quality': 'growth', 'value': 1},    # 木：生长
        'fire': {'dimension': 'time_present', 'quality': 'expansion', 'value': 1}, # 火：升腾
        'earth': {'dimension': 'space_middle', 'quality': 'balance', 'value': 0},  # 土：中和
        'metal': {'dimension': 'cause_effect', 'quality': 'contraction', 'value': -1}, # 金：收敛
        'water': {'dimension': 'space_inner', 'quality': 'flow', 'value': 0},     # 水：流动
    }
    
    def transform(self, current_vector: List[float], intention: str) -> Dict[str, Any]:
        """
        执天之行 — 执行认知转化
        
        根据意图转化认知状态
        """
        # 1. 识别转化类型
        transformation_type = self._identify_transformation(intention)
        
        # 2. 计算目标状态
        target_vector = self._calculate_target(current_vector, transformation_type)
        
        # 3. 生成转化路径
        path = self._generate_path(current_vector, target_vector)
        
        # 4. 提供阴符经智慧
        wisdom = self._generate_wisdom(transformation_type)
        
        return {
            'type': transformation_type,
            'current': current_vector,
            'target': target_vector,
            'path': path,
            'wisdom': wisdom,
            'quote': self._get_yinfu_quote(transformation_type)
        }
    
    def _identify_transformation(self, intention: str) -> str:
        """识别转化类型"""
        intention_lower = intention.lower()
        
        if '成长' in intention_lower or 'growth' in intention_lower:
            return 'wood_growth'  # 木曰曲直
        elif '显化' in intention_lower or 'manifest' in intention_lower:
            return 'fire_expansion'  # 火曰炎上
        elif '平衡' in intention_lower or 'balance' in intention_lower:
            return 'earth_balance'  # 土爰稼穑
        elif '收敛' in intention_lower or 'contract' in intention_lower:
            return 'metal_contraction'  # 金曰从革
        elif '流动' in intention_lower or 'flow' in intention_lower:
            return 'water_flow'  # 水曰润下
        elif '转化' in intention_lower or 'transform' in intention_lower:
            return 'mixed_transformation'  # 五行转化
        else:
            return 'neutral_adjustment'  # 中性调整
    
    def _calculate_target(self, current: List[float], trans_type: str) -> List[float]:
        """计算目标状态"""
        target = current.copy()
        
        if trans_type == 'wood_growth':
            # 增强未来维度 (阳)
            target[2] = TernaryEncoder.clamp(target[2] + 0.3)
        elif trans_type == 'fire_expansion':
            # 增强当下维度 (阳)
            target[1] = TernaryEncoder.clamp(target[1] + 0.3)
        elif trans_type == 'earth_balance':
            # 向中间维度靠拢 (和)
            for i in range(3, 6):
                target[i] = TernaryEncoder.clamp(target[i] * 0.7)
        elif trans_type == 'metal_contraction':
            # 增强收敛维度 (阴)
            target[8] = TernaryEncoder.clamp(target[8] - 0.3)
        elif trans_type == 'water_flow':
            # 增强内在流动 (和)
            target[3] = TernaryEncoder.clamp(target[3] * 0.8)
        
        return target
    
    def _generate_path(self, current: List[float], target: List[float]) -> List[Dict]:
        """生成转化路径"""
        path = []
        steps = 5
        
        for step in range(steps):
            intermediate = [
                current[i] + (target[i] - current[i]) * (step / steps)
                for i in range(9)
            ]
            path.append({
                'step': step + 1,
                'vector': intermediate,
                'code': TernaryEncoder.to_decimal(intermediate)
            })
        
        return path
    
    def _generate_wisdom(self, trans_type: str) -> str:
        """生成转化智慧"""
        wisdom_map = {
            'wood_growth': '木曰曲直，能屈能伸，成长之道在于柔韧',
            'fire_expansion': '火曰炎上，光明磊落，显化之道在于真诚',
            'earth_balance': '土爰稼穑，厚德载物，平衡之道在于包容',
            'metal_contraction': '金曰从革，收敛锋芒，收敛之道在于内敛',
            'water_flow': '水曰润下，顺势而为，流动之道在于适应',
            'mixed_transformation': '五行转化，相生相克，变化之道在于调和',
            'neutral_adjustment': '道法自然，不偏不倚，中道在于觉察'
        }
        return wisdom_map.get(trans_type, '道法自然')
    
    def _get_yinfu_quote(self, trans_type: str) -> str:
        """获取阴符经原文"""
        quotes = {
            'wood_growth': '天发杀机，移星易宿',
            'fire_expansion': '地发杀机，龙蛇起陆',
            'earth_balance': '三盗既宜，三才既安',
            'metal_contraction': '人发杀机，天地反覆',
            'water_flow': '观天之道，执天之行',
            'mixed_transformation': '天性，人也；人心，机也',
            'neutral_adjustment': '立天之道，以定人也'
        }
        return quotes.get(trans_type, '观天之道，执天之行，尽矣')


class YinfuBalancer:
    """
    三盗既宜 — 阴符经平衡系统
    
    《阴符经》: "天地，万物之盗；万物，人之盗；人，万物之盗。三盗既宜，三才既安。"
    """
    
    def check_balance(self, vector: List[float]) -> Dict[str, Any]:
        """
        三盗既宜 — 检查认知平衡
        
        检查天地人三才的平衡状态
        """
        # 天：时间三维
        time_balance = self._check_time_balance(vector[0:3])
        
        # 地：空间三维
        space_balance = self._check_space_balance(vector[3:6])
        
        # 人：因果三维
        causal_balance = self._check_causal_balance(vector[6:9])
        
        # 整体平衡度
        overall_balance = (time_balance + space_balance + causal_balance) / 3
        
        # 判断是否"既宜"
        is_yi = abs(overall_balance) < 0.2
        
        return {
            'time_balance': {
                'score': time_balance,
                'status': '安' if abs(time_balance) < 0.3 else '待调整',
                'dimension': '天'
            },
            'space_balance': {
                'score': space_balance,
                'status': '安' if abs(space_balance) < 0.3 else '待调整',
                'dimension': '地'
            },
            'causal_balance': {
                'score': causal_balance,
                'status': '安' if abs(causal_balance) < 0.3 else '待调整',
                'dimension': '人'
            },
            'overall': {
                'score': overall_balance,
                'status': '三盗既宜' if is_yi else '三盗未宜',
                'result': '三才既安' if is_yi else '三才未安'
            },
            'code': TernaryEncoder.to_decimal(vector),
            'recommendation': self._generate_recommendation(overall_balance, vector)
        }
    
    def _check_time_balance(self, time_dims: List[float]) -> float:
        """检查时间维平衡"""
        # 过去、现在、未来的平衡
        past, present, future = time_dims
        
        # 理想状态：现在稍强，过去未来平衡
        ideal_present = 0.3
        balance_score = 1.0 - (
            abs(past - future) * 0.3 +  # 过去未来平衡
            abs(present - ideal_present) * 0.4  # 现在临在
        )
        
        return balance_score
    
    def _check_space_balance(self, space_dims: List[float]) -> float:
        """检查空间维平衡"""
        # 内、中、外的平衡
        inner, middle, outer = space_dims
        
        # 理想状态：中间稍强，内外平衡
        ideal_middle = 0.2
        balance_score = 1.0 - (
            abs(inner - outer) * 0.3 +  # 内外平衡
            abs(middle - ideal_middle) * 0.4  # 关系中和
        )
        
        return balance_score
    
    def _check_causal_balance(self, causal_dims: List[float]) -> float:
        """检查因果维平衡"""
        # 因、缘、果的平衡
        cause, condition, effect = causal_dims
        
        # 理想状态：因果一致，缘起中和
        balance_score = 1.0 - (
            abs(cause - effect) * 0.4 +  # 因果一致
            abs(condition) * 0.3  # 缘起中和
        )
        
        return balance_score
    
    def _generate_recommendation(self, overall: float, vector: List[float]) -> str:
        """生成平衡建议"""
        if abs(overall) < 0.2:
            return "三盗既宜，三才既安。保持觉察，继续修炼。"
        elif overall > 0.2:
            return "阳气过盛，建议收敛。练习内观，回归平衡。"
        else:
            return "阴气过盛，建议舒展。练习行动，向阳转化。"


class YinfuTranscendence:
    """
    尽矣 — 阴符经超越系统
    
    《阴符经》: "观天之道，执天之行，尽矣。"
    """
    
    def transcend(self, cognitive_state: List[float]) -> Dict[str, Any]:
        """
        尽矣 — 超越认知状态
        
        理解状态的暂时性，回归太极
        """
        code = TernaryEncoder.to_decimal(cognitive_state)
        
        # 理解状态的本质
        insight = self._generate_insight(code, cognitive_state)
        
        # 超越二元
        transcended_state = self._transcend_dualities(cognitive_state)
        
        # 阴符经智慧
        wisdom = self._extract_wisdom(code)
        
        return {
            'original_code': code,
            'original_state': cognitive_state,
            'insight': insight,
            'transcended_state': transcended_state,
            'wisdom': wisdom,
            'quote': '观天之道，执天之行，尽矣',
            'taoist_meaning': self._explain_taoist_meaning(code)
        }
    
    def _generate_insight(self, code: int, state: List[float]) -> str:
        """生成超越洞见"""
        if code == 9841:  # 太极
            return "平衡非终点，而是起点。太极生两仪，两仪生四象，四象生八卦。"
        elif code == 0:  # 纯阴
            return "阴非消极，而是收敛的智慧。知止而后有定，定而后能静。"
        elif code == 19682:  # 纯阳
            return "阳非积极，而是创造的力量。天行健，君子以自强不息。"
        elif all(abs(s) < 0.3 for s in state):
            return "接近太极，但仍有执着。放下最后一点执念。"
        else:
            return "状态非固定，而是流动的。如水的智慧，随方就圆。"
    
    def _transcend_dualities(self, state: List[float]) -> List[float]:
        """超越二元对立"""
        # 不是强制归零，而是带着觉知回归
        transcended = []
        for s in state:
            if abs(s) < 0.1:
                transcended.append(0.0)  # 本来就是和
            else:
                # 理解并接纳，然后放下
                transcended.append(s * 0.5)  # 减半，表示放下执着
        
        return transcended
    
    def _extract_wisdom(self, code: int) -> str:
        """提取阴符经智慧"""
        if code == 9841:
            return "尽矣 — 完成不是结束，而是新的开始"
        elif code < 5000:
            return "阴中求阳 — 在收敛中寻找生长的力量"
        elif code > 15000:
            return "阳中求阴 — 在创造中保持收敛的智慧"
        else:
            return "中和之道 — 不偏不倚，执中守正"
    
    def _explain_taoist_meaning(self, code: int) -> str:
        """解释道家深意"""
        meanings = {
            9841: "太极 — 道生一，一生二，二生三，三生万物",
            0: "坤 — 地势坤，君子以厚德载物",
            19682: "乾 — 天行健，君子以自强不息",
        }
        return meanings.get(code, f"状态码 {code} — 道在当下，觉知即道")


class YinfuPractice:
    """
    阴符经实修系统
    
    整合观、行、衡、超四个维度
    """
    
    def __init__(self):
        self.observer = YinfuObserver()
        self.transformer = YinfuTransformer()
        self.balancer = YinfuBalancer()
        self.transcendence = YinfuTranscendence()
        self.practice_log = []
    
    def daily_practice(self, situation: Dict[str, Any], intention: str = "") -> Dict[str, Any]:
        """
        每日修炼
        
        整合观天之道、执天之行、三盗既宜、尽矣
        """
        result = {
            'date': datetime.now(timezone.utc).isoformat(),
            'steps': {}
        }
        
        # 1. 观天之道
        result['steps']['observe'] = {
            'practice': '观天之道',
            'vector': self.observer.observe_nine_dimensions(situation).to_list(),
            'summary': self.observer.get_observation_summary()
        }
        
        # 2. 执天之行
        if intention:
            result['steps']['transform'] = {
                'practice': '执天之行',
                'intention': intention,
                'transformation': self.transformer.transform(
                    result['steps']['observe']['vector'],
                    intention
                )
            }
        
        # 3. 三盗既宜
        result['steps']['balance'] = {
            'practice': '三盗既宜',
            'check': self.balancer.check_balance(result['steps']['observe']['vector'])
        }
        
        # 4. 尽矣
        result['steps']['transcend'] = {
            'practice': '尽矣',
            'transcendence': self.transcendence.transcend(result['steps']['observe']['vector'])
        }
        
        # 记录修炼日志
        self.practice_log.append(result)
        
        return result
    
    def get_practice_summary(self) -> Dict[str, Any]:
        """获取修炼总结"""
        if not self.practice_log:
            return {'count': 0, 'message': '暂无修炼记录'}
        
        return {
            'count': len(self.practice_log),
            'recent': self.practice_log[-5:],
            'trend': self._analyze_practice_trend(),
            'recommendations': self._generate_recommendations()
        }
    
    def _analyze_practice_trend(self) -> str:
        """分析修炼趋势"""
        if len(self.practice_log) < 3:
            return "数据不足，继续修炼"
        
        recent_balances = [
            log['steps']['balance']['check']['overall']['score']
            for log in self.practice_log[-5:]
        ]
        
        avg_recent = sum(recent_balances[-3:]) / 3
        avg_earlier = sum(recent_balances[:-3]) / len(recent_balances[:-3]) if len(recent_balances) > 3 else avg_recent
        
        if avg_recent > avg_earlier:
            return "修炼见效，平衡度提升"
        elif avg_recent < avg_earlier:
            return "修炼波动，需要调整"
        else:
            return "修炼稳定，继续坚持"
    
    def _generate_recommendations(self) -> List[str]:
        """生成修炼建议"""
        recommendations = []
        
        if len(self.practice_log) < 7:
            recommendations.append("建议连续修炼 7 天，形成习惯")
        
        if len(self.practice_log) >= 7:
            avg_balance = sum(
                log['steps']['balance']['check']['overall']['score']
                for log in self.practice_log[-7:]
            ) / 7
            
            if avg_balance > 0.8:
                recommendations.append("平衡度优秀，可以尝试进阶修炼")
            elif avg_balance > 0.6:
                recommendations.append("平衡度良好，继续保持")
            else:
                recommendations.append("平衡度待提升，增加修炼频率")
        
        return recommendations
