"""
Trit 编译器 - LLM 输出到确定性九维 Trit 向量的转换层

融合 lingzhu 平衡三进制编码器 + Triton 鲁棒编译策略
支持：JSON/纯文本/混合/乱码 → [-1, 0, +1] × 9
编译失败 → 全 0 悬置态 → 触发 L7 裂变层
"""

import re
import json
from typing import List, Tuple, Optional, Dict
from lingzhu.cognitive.balanced_ternary import BalancedTernaryEncoder


class TritCompiler:
    """
    融合编译器：将 LLM 任意格式输出编译为确定性九维 Trit 向量
    """
    
    VALID_DIM = 9
    FALLBACK_VECTOR = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # 全 0 悬置态
    
    # 九维语义映射 (可配置)
    DIM_NAMES = {
        'default': ['过去', '现在', '未来', '内', '中', '外', '因', '缘', '果'],
        'ops': ['流量压力', '错误率', '延迟', '活跃度', '资源利用', '威胁', '数据质量', '高峰', '稳定'],
        'finance': ['趋势', '波动', '成交量', '情绪', '估值', '动量', '基本面', '技术面', '风险'],
        'taoist': ['天', '地', '人', '正', '反', '合', '归', '守', '进'],
    }
    
    def __init__(self, mapping: str = 'default'):
        self.mapping = mapping
        self.dim_names = self.DIM_NAMES.get(mapping, self.DIM_NAMES['default'])
        self.encoder = BalancedTernaryEncoder(mapping=mapping)
    
    def compile(self, llm_raw_output: str) -> Tuple[List[int], bool, str]:
        """
        编译 LLM 输出为九维 Trit 向量
        
        返回：(trit_vector, is_confident, trace_info)
        - trit_vector: 九维 Trit 列表 [-1, 0, +1]
        - is_confident: 是否确定 (False 表示降级为全 0 悬置态)
        - trace_info: 编译过程说明
        """
        # 策略 1: JSON 解析
        parsed = self._try_json(llm_raw_output)
        if parsed:
            trits, conf = self._validate_and_pad(parsed)
            return trits, conf, f"json_parse: {len(parsed)} dims extracted"
        
        # 策略 2: 正则提取 -1/0/+1 token
        parsed = self._try_regex(llm_raw_output)
        if parsed:
            trits, conf = self._validate_and_pad(parsed)
            return trits, conf, f"regex_parse: {len(parsed)} tokens extracted"
        
        # 策略 3: 语义编码 (lingzhu 关键词匹配)
        parsed = self._try_semantic(llm_raw_output)
        if parsed:
            trits, conf = self._validate_and_pad(parsed)
            return trits, conf, f"semantic_parse: {len(parsed)} dims matched"
        
        # 策略 4: 降级为全 0 悬置态 (触发 L7 裂变)
        return self.FALLBACK_VECTOR, False, "fallback: unable to parse, triggering L7 fission"
    
    def _try_json(self, text: str) -> Optional[List[int]]:
        """尝试从 JSON 中解析 Trit 向量"""
        try:
            data = json.loads(text)
            # 尝试多种可能的 key
            for key in ["trit_vector", "vector", "trits", "cognition_vector", "nine_dims", "state"]:
                if key in data and isinstance(data[key], list):
                    return self._normalize_trits(data[key])
            # 如果本身就是数组
            if isinstance(data, list):
                return self._normalize_trits(data)
        except (json.JSONDecodeError, TypeError):
            pass
        return None
    
    def _try_regex(self, text: str) -> Optional[List[int]]:
        """正则提取所有 -1/0/+1 形式的 token"""
        # 匹配 +1, -1, 0 三种形式
        pattern = r'[+-]?[01]'
        matches = re.findall(pattern, text)
        if not matches:
            return None
        return self._normalize_trits(matches)
    
    def _try_semantic(self, text: str) -> Optional[List[int]]:
        """语义编码 (lingzhu 关键词匹配)"""
        scores = [0] * 9
        text_lower = text.lower()
        
        # 简化的关键词匹配 (可扩展)
        keywords = {
            0: ['过去', 'past', 'history', '之前'],
            1: ['现在', 'present', 'current', '当下'],
            2: ['未来', 'future', '将要', '预期'],
            3: ['内', 'inner', '内部', '内在'],
            4: ['中', 'middle', '中间', '平衡'],
            5: ['外', 'outer', '外部', '外在'],
            6: ['因', 'cause', '原因', '种子'],
            7: ['缘', 'condition', '条件', '机会'],
            8: ['果', 'effect', '结果', '成效'],
        }
        
        for dim, words in keywords.items():
            for word in words:
                if word in text_lower:
                    scores[dim] += 1
        
        # 归一化为 -1/0/+1
        normalized = []
        for score in scores:
            if score >= 2:
                normalized.append(1)
            elif score == 0:
                normalized.append(0)
            else:
                normalized.append(-1)
        
        return normalized if any(s != 0 for s in normalized) else None
    
    def _normalize_trits(self, raw: List) -> Optional[List[int]]:
        """将各种输入格式归一化为 -1/0/+1"""
        result = []
        for item in raw:
            if isinstance(item, (int, float)):
                val = int(item)
            elif isinstance(item, str):
                item = item.strip()
                if item in ('+1', '1'):
                    val = 1
                elif item == '-1':
                    val = -1
                elif item == '0':
                    val = 0
                else:
                    continue
            else:
                continue
            result.append(max(-1, min(1, val)))
        return result if result else None
    
    def _validate_and_pad(self, trits: List[int]) -> Tuple[List[int], bool]:
        """校验并补齐到 9 维"""
        if not trits or len(trits) == 0:
            return self.FALLBACK_VECTOR, False
        
        # 截断或补齐
        if len(trits) > self.VALID_DIM:
            trits = trits[:self.VALID_DIM]
        elif len(trits) < self.VALID_DIM:
            trits = trits + [0] * (self.VALID_DIM - len(trits))
        
        # 校验每个值在 [-1,0,1] 范围内
        valid = all(t in (-1, 0, 1) for t in trits)
        if not valid:
            return self.FALLBACK_VECTOR, False
        
        # 信息量检查：全 0 且非原始全 0 → 标记为不确定
        is_all_zero = all(t == 0 for t in trits)
        is_confident = not is_all_zero
        
        return trits, is_confident
    
    def trit_to_coordinate(self, trits: List[int]) -> int:
        """将九维 Trit 向量转换为 19683 空间坐标 (0~19682)"""
        return self.encoder.ternary_to_decimal(trits)
    
    def coordinate_to_trits(self, coord: int) -> List[int]:
        """将 19683 坐标反解为九维 Trit 向量"""
        return self.encoder.decimal_to_ternary(coord)
    
    def get_state_info(self, code: int) -> Dict[str, any]:
        """获取状态信息 (融合 lingzhu 特殊状态)"""
        return self.encoder.get_state_info(code)


# ============================================================
# 使用示例
# ============================================================

if __name__ == "__main__":
    compiler = TritCompiler(mapping='default')
    
    test_cases = [
        # 格式 1: 标准 JSON
        '{"trit_vector": [1, 0, 1, -1, 0, 0, 1, 1, 0]}',
        # 格式 2: 纯文本列表
        '[+1, 0, +1, -1, 0, 0, +1, +1, 0]',
        # 格式 3: 带解释文字
        '当前态势：过去 +1，现在 0，未来 +1，内 -1，中 0，外 0，因 +1，缘 +1，果 0',
        # 格式 4: 只有部分维度
        '[+1, 0, -1]',
        # 格式 5: 乱码 (应降级为全 0)
        'asdfghjkl',
        # 格式 6: 语义描述
        '我需要回顾过去的经验，把握当下的机会，规划未来的方向',
    ]
    
    print("=" * 60)
    print("Trit 编译器融合版测试")
    print("=" * 60)
    
    for i, case in enumerate(test_cases):
        trits, confident, info = compiler.compile(case)
        coord = compiler.trit_to_coordinate(trits)
        state_info = compiler.get_state_info(coord)
        
        print(f"\n测试{i+1}: {case[:60]}...")
        print(f"  向量：{trits}")
        print(f"  坐标：{coord}")
        print(f"  状态：{state_info.get('name', '普通态')}")
        print(f"  确定：{confident}")
        print(f"  信息：{info}")
