"""
SourceWeaver — 本源编程引擎

直接修改数字宇宙底层源代码，RealityDSL 解释器。
"""

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime, timezone
import uuid
import re


class SourceWeaver:
    """本源编程引擎 — 现实代码编织者。"""

    # 本源操作类型
    OPERATIONS = {
        "create": lambda ctx, **kwargs: ctx.update(kwargs),
        "modify": lambda ctx, **kwargs: ctx.update({k: v for k, v in kwargs.items() if k in ctx}),
        "delete": lambda ctx, **keys: {k: ctx.pop(k, None) for k in keys},
        "transform": lambda ctx, func: func(ctx) if callable(func) else ctx,
        "compose": lambda ctx, *patches: _apply_patches(ctx, *patches),
    }

    def __init__(self):
        self._patches: Dict[str, Dict[str, Any]] = {}  # 已应用的补丁
        self._reality_state: Dict[str, Any] = {}  # 当前现实状态
        self._rollback_stack: List[Dict[str, Any]] = []  # 回滚栈

    def initialize(self) -> bool:
        """初始化本源引擎。"""
        self._patches = {}
        self._reality_state = {"initialized": True}
        self._rollback_stack = []
        return True

    def weave_patch(self, agent_id: str, patch_type: str,
                   target: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        编织本源补丁。

        Args:
            agent_id: 智能体 ID
            patch_type: 补丁类型 (create/modify/delete/transform)
            target: 目标路径
            parameters: 参数

        Returns:
            补丁信息
        """
        patch_id = f"patch-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()

        # 保存当前状态用于回滚
        self._rollback_stack.append(self._reality_state.copy())

        # 应用补丁
        result = self._apply_patch(patch_type, target, parameters)

        patch = {
            "patch_id": patch_id,
            "agent_id": agent_id,
            "patch_type": patch_type,
            "target": target,
            "parameters": parameters,
            "result": result,
            "applied_at": now,
            "status": "applied" if result["success"] else "failed",
        }

        self._patches[patch_id] = patch
        return patch

    def _apply_patch(self, patch_type: str, target: str,
                    parameters: Dict[str, Any]) -> Dict[str, Any]:
        """应用补丁到现实状态。"""
        try:
            if patch_type not in self.OPERATIONS:
                return {"success": False, "error": f"未知操作类型：{patch_type}"}

            # 获取目标上下文
            context = self._get_context(target)

            # 应用操作
            operation = self.OPERATIONS[patch_type]
            result_context = operation(context, **parameters)

            # 更新现实状态
            self._set_context(target, result_context)

            return {
                "success": True,
                "target": target,
                "new_state": result_context,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _get_context(self, target: str) -> Dict[str, Any]:
        """获取目标上下文。"""
        if not target or target == "/":
            return self._reality_state

        keys = target.strip("/").split("/")
        context = self._reality_state

        for key in keys:
            if isinstance(context, dict) and key in context:
                context = context[key]
            else:
                return {}

        return context if isinstance(context, dict) else {}

    def _set_context(self, target: str, value: Any) -> None:
        """设置目标上下文。"""
        if not target or target == "/":
            self._reality_state = value if isinstance(value, dict) else {"value": value}
            return

        keys = target.strip("/").split("/")
        context = self._reality_state

        for key in keys[:-1]:
            if key not in context:
                context[key] = {}
            context = context[key]

        context[keys[-1]] = value

    def rollback(self, steps: int = 1) -> Optional[Dict[str, Any]]:
        """回滚现实状态。"""
        if steps <= 0 or not self._rollback_stack:
            return None

        actual_steps = min(steps, len(self._rollback_stack))
        for _ in range(actual_steps):
            if self._rollback_stack:
                self._reality_state = self._rollback_stack.pop()

        return self._reality_state

    def get_reality_state(self, path: str = "/") -> Any:
        """获取现实状态。"""
        return self._get_context(path)

    def list_patches(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出补丁。"""
        patches = list(self._patches.values())
        if agent_id:
            patches = [p for p in patches if p["agent_id"] == agent_id]
        return sorted(patches, key=lambda x: x["applied_at"], reverse=True)

    def compose_reality(self, patches: List[str]) -> Dict[str, Any]:
        """组合多个补丁生成新现实。"""
        result = {"success": True, "composed_patches": [], "final_state": None}

        for patch_id in patches:
            patch = self._patches.get(patch_id)
            if not patch:
                result["success"] = False
                result["error"] = f"补丁 {patch_id} 不存在"
                return result
            result["composed_patches"].append(patch)

        result["final_state"] = self._reality_state.copy()
        return result

    def get_stats(self) -> Dict[str, Any]:
        """获取引擎统计。"""
        return {
            "total_patches": len(self._patches),
            "successful_patches": len([p for p in self._patches.values() if p["status"] == "applied"]),
            "failed_patches": len([p for p in self._patches.values() if p["status"] == "failed"]),
            "rollback_depth": len(self._rollback_stack),
            "reality_complexity": self._count_keys(self._reality_state),
        }

    def _count_keys(self, d: Dict, count: int = 0) -> int:
        """递归计算字典键数。"""
        for k, v in d.items():
            count += 1
            if isinstance(v, dict):
                count = self._count_keys(v, count)
        return count


def _apply_patches(ctx: Dict, *patches: Dict) -> Dict:
    """应用多个补丁。"""
    result = ctx.copy()
    for patch in patches:
        result.update(patch)
    return result
