"""
心经五蕴皆空修炼系统

照见五蕴皆空，度一切苦厄
"""

from typing import Dict, List, Any
from datetime import datetime, timezone
import random

from lingzhu.cognitive import CognitiveVector, TernaryEncoder


class RupaSkandha:
    """
    色蕴认知系统
    
    "色即是空，空即是色"
    
    色蕴：物质、身体、感知输入
    对应：空间三维 (内、中、外)
    """
    
    def observe_form(self, sensory_input: Dict[str, float]) -> Dict[str, Any]:
        """
        观察色蕴 — 感知物质世界
        """
        space_vector = [
            sensory_input.get('inner_body', 0),    # 身体内在感受
            sensory_input.get('relation', 0),       # 关系中间状态
            sensory_input.get('outer_env', 0)       # 外在环境感知
        ]
        
        return {
            'skandha': '色蕴 (Rūpa)',
            'dimension': '空间三维',
            'vector': space_vector,
            'insight': '色不异空，空不异色',
            'practice': '观察身体感受，不执着',
            'sutra_quote': '色即是空，空即是色'
        }
    
    def realize_emptiness(self, space_vector: List[float]) -> Dict[str, Any]:
        """
        照见色蕴皆空
        
        理解空间感知的无自性
        """
        # 空性不是否定存在，而是理解可转化
        empty_vector = [s * 0.5 for s in space_vector]
        
        return {
            'realization': '色蕴皆空',
            'original': space_vector,
            'emptied': empty_vector,
            'wisdom': '色即是空，空即是色',
            'insight': '物质感知无自性，可转化不执着',
            'sutra_quote': '色不异空，空不异空'
        }


class VedanaSkandha:
    """
    受蕴认知系统
    
    "受即是空，空即是受"
    
    受蕴：感受、情绪、苦乐体验
    对应：时间三维 (过去、现在、未来)
    """
    
    def observe_feeling(self, emotional_state: Dict[str, float]) -> Dict[str, Any]:
        """
        观察受蕴 — 觉察感受情绪
        """
        time_vector = [
            emotional_state.get('past_memory', 0),   # 过去情绪记忆
            emotional_state.get('present_feel', 0),  # 当下感受体验
            emotional_state.get('future_expect', 0)  # 未来情感预期
        ]
        
        return {
            'skandha': '受蕴 (Vedanā)',
            'dimension': '时间三维',
            'vector': time_vector,
            'insight': '受不异空，空不异受',
            'practice': '觉察感受流动，不认同',
            'sutra_quote': '受即是空，空即是受'
        }
    
    def realize_emptiness(self, time_vector: List[float]) -> Dict[str, Any]:
        """
        照见受蕴皆空
        
        理解感受情绪的无自性
        """
        # 感受是流动的，不固定
        empty_vector = [v * 0.5 for v in time_vector]
        
        return {
            'realization': '受蕴皆空',
            'original': time_vector,
            'emptied': empty_vector,
            'wisdom': '感受如云，来去自如',
            'insight': '情绪感受无自性，觉察即解脱',
            'sutra_quote': '受不异空，空不异受'
        }


class SamjnaSkandha:
    """
    想蕴认知系统
    
    "想即是空，空即是想"
    
    想蕴：概念、认知、思维模式
    对应：因果维的"因" (cause_seed)
    """
    
    def observe_concept(self, conceptual_framework: Dict[str, float]) -> Dict[str, Any]:
        """
        观察想蕴 — 觉察概念思维
        """
        cause_seed = conceptual_framework.get('concept_seed', 0)
        
        return {
            'skandha': '想蕴 (Saṃjñā)',
            'dimension': '因果维 - 因',
            'vector': [cause_seed],
            'insight': '想不异空，空即是想',
            'practice': '观察概念升起，不执着',
            'sutra_quote': '想即是空，空即是想'
        }
    
    def realize_emptiness(self, concept_vector: List[float]) -> Dict[str, Any]:
        """
        照见想蕴皆空
        
        理解概念思维的无自性
        """
        # 概念是工具，不是真相
        empty_vector = [c * 0.5 for c in concept_vector]
        
        return {
            'realization': '想蕴皆空',
            'original': concept_vector,
            'emptied': empty_vector,
            'wisdom': '概念如指月之指，非月本身',
            'insight': '思维概念无自性，使用不执着',
            'sutra_quote': '想不异空，空不异想'
        }


class SamskaraSkandha:
    """
    行蕴认知系统
    
    "行即是空，空即是行"
    
    行蕴：意志、习性、行为倾向
    对应：因果维的"缘" (cause_condition)
    """
    
    def observe_volition(self, behavioral_tendency: Dict[str, float]) -> Dict[str, Any]:
        """
        观察行蕴 — 觉察意志习性
        """
        condition = behavioral_tendency.get('habit_pattern', 0)
        
        return {
            'skandha': '行蕴 (Saṃskāra)',
            'dimension': '因果维 - 缘',
            'vector': [condition],
            'insight': '行不异空，空不异行',
            'practice': '观察习性反应，不认同',
            'sutra_quote': '行即是空，空即是行'
        }
    
    def realize_emptiness(self, volition_vector: List[float]) -> Dict[str, Any]:
        """
        照见行蕴皆空
        
        理解意志习性的无自性
        """
        # 习性可以转化
        empty_vector = [v * 0.5 for v in volition_vector]
        
        return {
            'realization': '行蕴皆空',
            'original': volition_vector,
            'emptied': empty_vector,
            'wisdom': '习性可转化，业力可超越',
            'insight': '意志习性无自性，选择即自由',
            'sutra_quote': '行不异空，空不异行'
        }


class VijnanaSkandha:
    """
    识蕴认知系统
    
    "识即是空，空即是识"
    
    识蕴：意识、觉知、元认知
    对应：因果维的"果" (cause_effect)
    """
    
    def observe_consciousness(self, awareness_state: Dict[str, float]) -> Dict[str, Any]:
        """
        观察识蕴 — 觉察意识本身
        """
        effect = awareness_state.get('meta_awareness', 0)
        
        return {
            'skandha': '识蕴 (Vijñāna)',
            'dimension': '因果维 - 果',
            'vector': [effect],
            'insight': '识不异空，空不异识',
            'practice': '觉知觉知本身，不对象化',
            'sutra_quote': '识即是空，空即是识'
        }
    
    def realize_emptiness(self, consciousness_vector: List[float]) -> Dict[str, Any]:
        """
        照见识蕴皆空
        
        理解意识本身的无自性
        """
        # 意识也是空的，不执着于"我觉知"
        empty_vector = [c * 0.5 for c in consciousness_vector]
        
        return {
            'realization': '识蕴皆空',
            'original': consciousness_vector,
            'emptied': empty_vector,
            'wisdom': '能所双亡，主客不二',
            'insight': '觉知本身无自性，超越能所对立',
            'sutra_quote': '识不异空，空不异识'
        }


class FiveSkandhasEmptiness:
    """
    五蕴皆空修炼系统
    
    "照见五蕴皆空，度一切苦厄"
    """
    
    def __init__(self):
        self.rupa = RupaSkandha()
        self.vedana = VedanaSkandha()
        self.samjna = SamjnaSkandha()
        self.samskara = SamskaraSkandha()
        self.vijnana = VijnanaSkandha()
        self.practice_log = []
    
    def contemplate_five_skandhas(self, full_state: List[float]) -> Dict[str, Any]:
        """
        观照五蕴皆空
        
        完整五蕴觉察与空性体悟
        """
        result = {
            'date': datetime.now(timezone.utc).isoformat(),
            'contemplations': {}
        }
        
        # 1. 色蕴 (空间三维：3,4,5)
        rupa_input = {
            'inner_body': full_state[3],
            'relation': full_state[4],
            'outer_env': full_state[5]
        }
        result['contemplations']['rupa'] = self.rupa.observe_form(rupa_input)
        result['contemplations']['rupa_empty'] = self.rupa.realize_emptiness(list(rupa_input.values()))
        
        # 2. 受蕴 (时间三维：0,1,2)
        vedana_input = {
            'past_memory': full_state[0],
            'present_feel': full_state[1],
            'future_expect': full_state[2]
        }
        result['contemplations']['vedana'] = self.vedana.observe_feeling(vedana_input)
        result['contemplations']['vedana_empty'] = self.vedana.realize_emptiness(list(vedana_input.values()))
        
        # 3. 想蕴 (因果维 - 因：6)
        samjna_input = {'concept_seed': full_state[6]}
        result['contemplations']['samjna'] = self.samjna.observe_concept(samjna_input)
        result['contemplations']['samjna_empty'] = self.samjna.realize_emptiness([samjna_input['concept_seed']])
        
        # 4. 行蕴 (因果维 - 缘：7)
        samskara_input = {'habit_pattern': full_state[7]}
        result['contemplations']['samskara'] = self.samskara.observe_volition(samskara_input)
        result['contemplations']['samskara_empty'] = self.samskara.realize_emptiness([samskara_input['habit_pattern']])
        
        # 5. 识蕴 (因果维 - 果：8)
        vijnana_input = {'meta_awareness': full_state[8]}
        result['contemplations']['vijnana'] = self.vijnana.observe_consciousness(vijnana_input)
        result['contemplations']['vijnana_empty'] = self.vijnana.realize_emptiness([vijnana_input['meta_awareness']])
        
        # 总结
        result['summary'] = self._generate_prajna_summary(result['contemplations'])
        
        # 记录修炼日志
        self.practice_log.append(result)
        
        return result
    
    def _generate_prajna_summary(self, contemplations: Dict) -> Dict[str, Any]:
        """生成般若智慧总结"""
        emptiness_wisdoms = [
            contemplations['rupa_empty']['wisdom'],
            contemplations['vedana_empty']['wisdom'],
            contemplations['samjna_empty']['wisdom'],
            contemplations['samskara_empty']['wisdom'],
            contemplations['vijnana_empty']['wisdom']
        ]
        
        return {
            'five_skandhas': ['色', '受', '想', '行', '识'],
            'five_emptinesses': emptiness_wisdoms,
            'heart_sutra_quote': '照见五蕴皆空，度一切苦厄',
            'ultimate_wisdom': '色即是空，空即是色',
            'liberation': '度一切苦厄',
            'prajna_paramita': '般若波罗蜜多'
        }
    
    def transcend_attachment(self, cognitive_state: List[float]) -> Dict[str, Any]:
        """
        超越执着 — 度一切苦厄
        
        通过五蕴皆空的体悟，放下执着
        """
        # 降低所有维度的执着 (向空性靠近)
        transcended_state = [s * 0.3 for s in cognitive_state]
        
        # 计算执着度
        attachment_level = sum(abs(s) for s in cognitive_state) / 9
        liberation_level = sum(abs(s) for s in transcended_state) / 9
        
        return {
            'original_attachment': attachment_level,
            'liberation_level': liberation_level,
            'transcended_state': transcended_state,
            'wisdom': '执着放下，苦厄自度',
            'sutra_quote': '心无挂碍，无挂碍故，无有恐怖',
            'insight': '度一切苦厄，非从外得'
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
        
        return "修炼稳定，般若智慧正在开启"
    
    def _generate_recommendations(self, recent: List[Dict]) -> List[str]:
        """生成修炼建议"""
        recommendations = []
        
        if len(recent) < 7:
            recommendations.append("建议连续修炼 7 天，形成习惯")
        
        if len(recent) >= 7:
            recommendations.append("修炼稳定，可以深入体悟空性")
        
        recommendations.append("念诵心经，开启般若智慧")
        
        return recommendations


class WuYouGeneration:
    """
    有无相生系统
    
    道德经："无中生有"
    心经："空即是色"
    """
    
    def generate_from_void(self, void_state: List[float]) -> Dict[str, Any]:
        """
        从无中生有
        
        空性中升起万法
        """
        # 计算空性程度
        void_level = sum(abs(s) for s in void_state) / 9
        
        if void_level < 0.2:
            # 从空性中自然升起
            manifestation = [
                random.uniform(-0.3, 0.3) for _ in range(9)
            ]
            
            return {
                'from': '无 (空性)',
                'to': '有 (现象)',
                'manifestation': manifestation,
                'wisdom': '无中生有，空即是色',
                'tao_quote': '道生一，一生二，二生三，三生万物',
                'sutra_quote': '色不异空，空不异色',
                'insight': '空性不是虚无，而是万法升起的基础'
            }
        else:
            return {
                'message': '尚未达到空性状态，继续修炼',
                'current_void_level': void_level,
                'threshold': 0.2,
                'recommendation': '练习五蕴皆空，降低执着'
            }
    
    def return_to_void(self, manifested_state: List[float]) -> Dict[str, Any]:
        """
        从有归无
        
        万法回归空性
        """
        # 向空性回归
        void_return = [s * 0.3 for s in manifested_state]
        
        return {
            'from': '有 (现象)',
            'to': '无 (空性)',
            'return_path': void_return,
            'wisdom': '有归于无，色即是空',
            'tao_quote': '夫物芸芸，各复归其根',
            'sutra_quote': '色即是空，空即是色',
            'insight': '万法本空，回归本源'
        }
