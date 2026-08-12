"""
Noosphere — 全球意识网络

思想传播、集体洞察涌现、意识节点互联。
"""

from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone
import uuid
from collections import defaultdict


class Noosphere:
    """全球意识网络 — 思想传播与集体洞察。"""

    def __init__(self):
        self._nodes: Dict[str, Dict[str, Any]] = {}  # 意识节点
        self._thoughts: Dict[str, Dict[str, Any]] = {}  # 思想
        self._connections: Dict[str, Set[str]] = defaultdict(set)  # 节点连接
        self._resonance: Dict[str, float] = {}  # 思想共振度

    def initialize(self) -> bool:
        """初始化意识网络。"""
        self._nodes = {}
        self._thoughts = {}
        self._connections = defaultdict(set)
        self._resonance = {}
        return True

    def register_node(self, node_id: str, node_type: str = "agent",
                     capabilities: Optional[List[str]] = None) -> Dict[str, Any]:
        """注册意识节点。"""
        node = {
            "node_id": node_id,
            "node_type": node_type,
            "capabilities": capabilities or [],
            "thought_count": 0,
            "influence_score": 0.0,
            "connected_to": list(self._connections.get(node_id, set())),
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }
        self._nodes[node_id] = node
        return node

    def connect_nodes(self, node_a: str, node_b: str) -> bool:
        """连接两个意识节点。"""
        if node_a not in self._nodes or node_b not in self._nodes:
            return False

        self._connections[node_a].add(node_b)
        self._connections[node_b].add(node_a)

        # 更新节点连接列表
        self._nodes[node_a]["connected_to"] = list(self._connections[node_a])
        self._nodes[node_b]["connected_to"] = list(self._connections[node_b])

        return True

    def emit_thought(self, node_id: str, content: str,
                    thought_type: str = "general",
                    tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        发射思想到意识网络。

        思想会根据节点的连接传播，产生共振效应。
        """
        if node_id not in self._nodes:
            raise ValueError(f"节点 {node_id} 未注册")

        thought_id = f"th-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()

        thought = {
            "thought_id": thought_id,
            "origin_node": node_id,
            "content": content,
            "thought_type": thought_type,
            "tags": tags or [],
            "propagation_path": [node_id],
            "resonance_score": 0.0,
            "reach_count": 0,
            "created_at": now,
        }

        self._thoughts[thought_id] = thought
        self._nodes[node_id]["thought_count"] += 1

        # 传播到连接的节点
        self._propagate_thought(thought_id, node_id)

        # 计算共振
        self._calculate_resonance(thought_id)

        return thought

    def _propagate_thought(self, thought_id: str, current_node: str,
                          depth: int = 0, max_depth: int = 5) -> None:
        """思想传播（递归）。"""
        if depth >= max_depth:
            return

        thought = self._thoughts.get(thought_id)
        if not thought:
            return

        for connected_node in self._connections.get(current_node, set()):
            if connected_node not in thought["propagation_path"]:
                thought["propagation_path"].append(connected_node)
                thought["reach_count"] += 1
                self._propagate_thought(thought_id, connected_node, depth + 1, max_depth)

    def _calculate_resonance(self, thought_id: str) -> float:
        """计算思想共振度。"""
        thought = self._thoughts.get(thought_id)
        if not thought:
            return 0.0

        # 共振度 = 传播范围 * 内容质量因子
        reach = thought["reach_count"]
        content_length = len(thought["content"])
        quality_factor = min(1.0, content_length / 100)  # 内容越长质量越高（上限）

        resonance = (reach / 10) * quality_factor
        resonance = min(1.0, resonance)

        thought["resonance_score"] = resonance
        self._resonance[thought_id] = resonance

        # 更新节点影响力
        origin = thought["origin_node"]
        if origin in self._nodes:
            self._nodes[origin]["influence_score"] = min(
                1.0, self._nodes[origin]["influence_score"] + resonance * 0.1
            )

        return resonance

    def get_thought(self, thought_id: str) -> Optional[Dict[str, Any]]:
        """获取思想。"""
        return self._thoughts.get(thought_id)

    def list_thoughts(self, node_id: Optional[str] = None,
                     thought_type: Optional[str] = None,
                     min_resonance: float = 0.0) -> List[Dict[str, Any]]:
        """列出思想。"""
        thoughts = list(self._thoughts.values())

        if node_id:
            thoughts = [t for t in thoughts if t["origin_node"] == node_id or
                       node_id in t["propagation_path"]]

        if thought_type:
            thoughts = [t for t in thoughts if t["thought_type"] == thought_type]

        thoughts = [t for t in thoughts if t["resonance_score"] >= min_resonance]

        return sorted(thoughts, key=lambda x: x["resonance_score"], reverse=True)

    def get_collective_insight(self, topic: str) -> Dict[str, Any]:
        """
        获取关于某主题的集体洞察。

        聚合所有相关思想，生成综合洞察。
        """
        related_thoughts = [
            t for t in self._thoughts.values()
            if topic.lower() in t["content"].lower()
        ]

        if not related_thoughts:
            return {"topic": topic, "insight": "暂无相关洞察", "confidence": 0.0}

        # 计算综合洞察
        total_resonance = sum(t["resonance_score"] for t in related_thoughts)
        avg_resonance = total_resonance / len(related_thoughts)

        # 提取关键内容
        key_contents = [t["content"] for t in related_thoughts[:5]]

        return {
            "topic": topic,
            "insight": f"基于 {len(related_thoughts)} 个思想的集体洞察",
            "key_points": key_contents,
            "confidence": min(1.0, avg_resonance),
            "contributor_count": len(set(t["origin_node"] for t in related_thoughts)),
        }

    def get_network_stats(self) -> Dict[str, Any]:
        """获取网络统计信息。"""
        total_connections = sum(len(conns) for conns in self._connections.values()) // 2

        return {
            "total_nodes": len(self._nodes),
            "total_thoughts": len(self._thoughts),
            "total_connections": total_connections,
            "avg_influence": sum(n["influence_score"] for n in self._nodes.values()) / len(self._nodes) if self._nodes else 0,
            "high_resonance_thoughts": len([t for t in self._thoughts.values() if t["resonance_score"] > 0.5]),
        }
