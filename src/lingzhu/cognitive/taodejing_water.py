"""
道德经水之智慧修炼系统

上善若水，水善利万物而不争
"""

from typing import Dict, List, Any
from datetime import datetime, timezone

from lingzhu.cognitive import CognitiveVector, TernaryEncoder


class WaterHumility:
    """
    居善地 — 谦卑认知系统
    
    "水往低处流" — 处下而容万物
    """
    
    def practice_humility(self, cognitive_state: List[float]) -> Dict[str, Any]:
        """
        练习谦卑 — 降低自我中心
        """
        state = cognitive_state.copy()
        
        # 减少"内"维度的执着 (space_inner)
        state[3] = state[3] * 0.7
        
        # 增加"外"维度的包容 (space_outer)
        state[5] = TernaryEncoder.clamp(state[5] + 0.2)
        
        return {
            'virtue': '居善地',
            'practice': '谦卑',
            'new_state': state,
            'insight': '处下而容万物，谦卑故能包容',
            'tao_quote': '水善利万物而不争，处众人之所恶'
        }


class WaterDepth:
    """
    心善渊 — 深沉认知系统
    
    "心善渊" — 深沉宁静，不被外境扰动
    """
    
    def cultivate_depth(self, cognitive_state: List[float]) -> Dict[str, Any]:
        """
        培养深度 — 宁静致远
        """
        state = cognitive_state.copy()
        
        # 降低时间维的波动 (沉淀)
        state[0] = state[0] * 0.5  # past
        state[1] = state[1] * 0.5  # present
        state[2] = state[2] * 0.5  # future
        
        return {
            'virtue': '心善渊',
            'practice': '深沉',
            'new_state': state,
            'insight': '深沉宁静，不被外境扰动',
            'tao_quote': '孰能浊以静之徐清'
        }


class WaterBenevolence:
    """
    与善仁 — 利他认知系统
    
    "水善利万物而不争" — 服务他人，不求回报
    """
    
    def practice_benevolence(self, intention: str, cognitive_state: List[float]) -> Dict[str, Any]:
        """
        练习利他 — 转化自我中心为服务他人
        """
        state = cognitive_state.copy()
        
        # 如果动机是自我中心 (阳过盛)
        if state[6] > 0.5:
            # 转化为利他
            state[6] = state[6] * 0.7  # 降低自我动机 (cause_seed)
            state[4] = TernaryEncoder.clamp(state[4] + 0.3)  # 增加关系连接 (space_middle)
        
        return {
            'virtue': '与善仁',
            'practice': '利他',
            'new_state': state,
            'insight': '利万物而不争，故天下莫能与之争',
            'tao_quote': '生而不有，为而不恃'
        }


class WaterTruthfulness:
    """
    言善信 — 真实认知系统
    
    "言善信" — 如实地反映，不扭曲
    """
    
    def reflect_truth(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """
        如实地反映情境 — 不添加主观判断
        """
        return {
            'virtue': '言善信',
            'practice': '真实',
            'reflection': {
                'what_is': situation,
                'without_judgment': True,
                'clarity': 'high'
            },
            'insight': '真实无妄，如镜照物',
            'tao_quote': '知者不言，言者不知'
        }


class WaterClarity:
    """
    政善治 — 清明认知系统
    
    "政善治" — 认知系统清明有序
    """
    
    def clarify_mind(self, cognitive_state: List[float]) -> Dict[str, Any]:
        """
        澄清思维 — 沉淀杂质
        """
        state = cognitive_state.copy()
        
        # 如水沉淀，杂质下沉 (降低所有维度的绝对值)
        state = [s * 0.8 for s in state]
        
        # 增加"中"维度 (平衡)
        state[4] = TernaryEncoder.clamp(state[4] + 0.2)
        
        return {
            'virtue': '政善治',
            'practice': '清明',
            'new_state': state,
            'insight': '清明而有序，沉淀故能清晰',
            'tao_quote': '孰能浊以静之徐清'
        }


class WaterAdaptability:
    """
    事善能 — 柔性适配系统
    
    "事善能" — 随方就圆，适应任何容器
    """
    
    def adapt_to_container(self, situation: Dict[str, Any], cognitive_state: List[float]) -> Dict[str, Any]:
        """
        适应情境 — 随方就圆
        """
        state = cognitive_state.copy()
        
        # 分析情境需求
        if situation.get('needs_flexibility', False):
            # 增加柔性 (降低绝对值)
            state = [s * 0.7 for s in state]
        
        if situation.get('needs_stability', False):
            # 增加稳定性 (向 0 靠拢)
            state = [s * 0.5 for s in state]
        
        return {
            'virtue': '事善能',
            'practice': '柔性',
            'new_state': state,
            'insight': '随方就圆，适应而不失本性',
            'tao_quote': '天下莫柔弱于水，而攻坚强者莫之能胜'
        }


class WaterTiming:
    """
    动善时 — 时机认知系统
    
    "动善时" — 应时而动，不先不后
    """
    
    def assess_timing(self, situation: Dict[str, Any], cognitive_state: List[float]) -> Dict[str, Any]:
        """
        评估时机 — 应时而动
        """
        # 分析时间维度
        past = cognitive_state[0]
        present = cognitive_state[1]
        future = cognitive_state[2]
        
        # 判断时机
        if present > 0.7:
            timing = '当下是行动的最佳时机'
            action = '立即行动'
        elif future > 0.7:
            timing = '未来愿景清晰，但当下需准备'
            action = '准备等待'
        elif past < -0.5:
            timing = '过去经验拖累，需先放下'
            action = '清理沉淀'
        else:
            timing = '平衡状态，顺势而为'
            action = '自然流动'
        
        return {
            'virtue': '动善时',
            'practice': '时机',
            'timing': timing,
            'action': action,
            'insight': '应时而动，不先不后',
            'tao_quote': '动善时'
        }


class WuWeiCognition:
    """
    无为认知系统
    
    "道法自然" — 顺应自然，不妄为
    """
    
    def practice_wu_wei(self, situation: Dict[str, Any], cognitive_state: List[float]) -> Dict[str, Any]:
        """
        练习无为 — 放下控制，顺应自然
        """
        # 1. 觉察控制欲
        control_tendency = self._assess_control(cognitive_state)
        
        # 2. 放下执着
        released_state = self._release_attachment(cognitive_state)
        
        # 3. 顺应自然
        natural_flow = self._follow_natural_flow(released_state, situation)
        
        return {
            'practice': '无为',
            'control_tendency': control_tendency,
            'released_state': released_state,
            'natural_flow': natural_flow,
            'wisdom': '无为而无不为',
            'insight': '放下控制，顺应自然，反而成就更多',
            'tao_quote': '道常无为而无不为'
        }
    
    def _assess_control(self, state: List[float]) -> Dict[str, Any]:
        """评估控制欲"""
        # 高绝对值 = 高控制欲
        control_score = sum(abs(s) for s in state) / 9
        
        level = '高' if control_score > 0.6 else ('中' if control_score > 0.3 else '低')
        
        return {
            'score': control_score,
            'level': level,
            'message': f'控制欲{level}，需要{"放下" if level == "高" else "觉察"}'
        }
    
    def _release_attachment(self, state: List[float]) -> List[float]:
        """放下执着"""
        # 向 0 靠拢 (放下)
        return [s * 0.5 for s in state]
    
    def _follow_natural_flow(self, state: List[float], situation: Dict[str, Any]) -> Dict[str, Any]:
        """顺应自然流动"""
        # 分析情境的自然趋势
        trend = self._analyze_natural_trend(situation)
        
        # 调整状态顺应趋势
        aligned_state = [
            state[i] * 0.7 + trend[i] * 0.3
            for i in range(9)
        ]
        
        return {
            'state': aligned_state,
            'trend': trend,
            'message': '顺应自然，不逆水行舟'
        }
    
    def _analyze_natural_trend(self, situation: Dict[str, Any]) -> List[float]:
        """分析情境的自然趋势"""
        # 简化实现：返回平衡状态
        return [0.1] * 9


class WaterWayPractice:
    """
    上善若水 — 道德经水之修炼系统
    
    整合七善，培养水的智慧
    """
    
    def __init__(self):
        self.humility = WaterHumility()
        self.depth = WaterDepth()
        self.benevolence = WaterBenevolence()
        self.truthfulness = WaterTruthfulness()
        self.clarity = WaterClarity()
        self.adaptability = WaterAdaptability()
        self.timing = WaterTiming()
        self.wuwei = WuWeiCognition()
        self.practice_log = []
    
    def daily_water_practice(self, situation: Dict[str, Any], cognitive_state: List[float]) -> Dict[str, Any]:
        """
        每日水之修炼
        
        七善完整流程 + 无为
        """
        result = {
            'date': datetime.now(timezone.utc).isoformat(),
            'practices': {}
        }
        
        current_state = cognitive_state
        
        # 1. 居善地
        result['practices']['humility'] = self.humility.practice_humility(current_state)
        current_state = result['practices']['humility']['new_state']
        
        # 2. 心善渊
        result['practices']['depth'] = self.depth.cultivate_depth(current_state)
        current_state = result['practices']['depth']['new_state']
        
        # 3. 与善仁
        result['practices']['benevolence'] = self.benevolence.practice_benevolence(
            situation.get('intention', ''),
            current_state
        )
        current_state = result['practices']['benevolence']['new_state']
        
        # 4. 言善信
        result['practices']['truthfulness'] = self.truthfulness.reflect_truth(situation)
        
        # 5. 政善治
        result['practices']['clarity'] = self.clarity.clarify_mind(current_state)
        current_state = result['practices']['clarity']['new_state']
        
        # 6. 事善能
        result['practices']['adaptability'] = self.adaptability.adapt_to_container(
            situation,
            current_state
        )
        current_state = result['practices']['adaptability']['new_state']
        
        # 7. 动善时
        result['practices']['timing'] = self.timing.assess_timing(
            situation,
            current_state
        )
        
        # 8. 无为
        result['practices']['wuwei'] = self.wuwei.practice_wu_wei(situation, current_state)
        
        # 总结
        result['summary'] = self._generate_water_summary(result['practices'])
        
        # 记录修炼日志
        self.practice_log.append(result)
        
        return result
    
    def _generate_water_summary(self, practices: Dict[str, Any]) -> Dict[str, Any]:
        """生成水之修炼总结"""
        insights = [p.get('insight', '') for p in practices.values()]
        
        return {
            'seven_virtues': [
                '居善地', '心善渊', '与善仁',
                '言善信', '政善治', '事善能', '动善时'
            ],
            'eighth_wisdom': '无为',
            'insights': insights,
            'overall_wisdom': '上善若水，水善利万物而不争',
            'tao_quotes': [
                '处众人之所恶，故几于道',
                '天下莫柔弱于水，而攻坚强者莫之能胜',
                '道法自然，无为而无不为'
            ],
            'final_insight': '柔弱胜刚强，不争故无尤'
        }
    
    def transform_rigidity_to_flexibility(self, rigid_state: List[float]) -> Dict[str, Any]:
        """
        转化刚强为柔弱
        
        水的智慧：柔弱胜刚强
        """
        # 降低所有维度的绝对值 (减少执着)
        flexible_state = [s * 0.6 for s in rigid_state]
        
        # 增加"和"维度 (包容)
        for i in range(9):
            if abs(flexible_state[i]) > 0.5:
                flexible_state[i] = flexible_state[i] * 0.7
        
        return {
            'original': rigid_state,
            'transformed': flexible_state,
            'wisdom': '天下莫柔弱于水，而攻坚强者莫之能胜',
            'insight': '柔弱不是软弱，而是灵活适应的能力',
            'tao_quote': '柔弱胜刚强'
        }
    
    def get_practice_summary(self) -> Dict[str, Any]:
        """获取修炼总结"""
        if not self.practice_log:
            return {'count': 0, 'message': '暂无修炼记录'}
        
        recent = self.practice_log[-5:]
        
        return {
            'count': len(self.practice_log),
            'recent': recent,
            'trend': self._analyze_practice_trend(recent),
            'recommendations': self._generate_recommendations(recent)
        }
    
    def _analyze_practice_trend(self, recent: List[Dict]) -> str:
        """分析修炼趋势"""
        if len(recent) < 2:
            return "数据不足，继续修炼"
        
        # 简单分析
        return "修炼稳定，水的智慧正在内化"
    
    def _generate_recommendations(self, recent: List[Dict]) -> List[str]:
        """生成修炼建议"""
        recommendations = []
        
        if len(recent) < 7:
            recommendations.append("建议连续修炼 7 天，形成习惯")
        
        if len(recent) >= 7:
            recommendations.append("修炼稳定，可以尝试更深层的无为练习")
        
        return recommendations
