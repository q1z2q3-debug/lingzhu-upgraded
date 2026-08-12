"""
RealityDSL — 领域特定语言

Agent 直接编写现实的 DSL 解释器。
"""

from typing import Any, Dict, List, Optional
import ast
import operator


class RealityDSL:
    """RealityDSL 解释器 — 现实编程语言。"""

    # 支持的操作符
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
    }

    # 内置函数
    BUILTINS = {
        "create": lambda **kwargs: {"action": "create", "params": kwargs},
        "modify": lambda **kwargs: {"action": "modify", "params": kwargs},
        "delete": lambda target: {"action": "delete", "target": target},
        "transform": lambda f, target: {"action": "transform", "function": f, "target": target},
        "query": lambda path: {"action": "query", "path": path},
    }

    def __init__(self):
        self._context: Dict[str, Any] = {}
        self._compiled_scripts: Dict[str, Any] = {}

    def initialize(self) -> bool:
        """初始化 DSL。"""
        self._context = {"__reality_version__": "1.0.0"}
        self._compiled_scripts = {}
        return True

    def compile(self, script: str, script_id: str = "default") -> Any:
        """编译 DSL 脚本。"""
        try:
            tree = ast.parse(script, mode='eval')
            self._compiled_scripts[script_id] = tree
            return {"success": True, "script_id": script_id}
        except SyntaxError as e:
            return {"success": False, "error": f"语法错误：{e}"}

    def execute(self, script: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """执行 DSL 脚本。"""
        exec_context = {**self._context, **(context or {})}
        exec_context.update(self.BUILTINS)

        try:
            tree = ast.parse(script, mode='eval')
            result = self._eval(tree.body, exec_context)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _eval(self, node: ast.AST, context: Dict[str, Any]) -> Any:
        """评估 AST 节点。"""
        if isinstance(node, ast.Num):  # Python 3.7 兼容
            return node.n
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Str):  # Python 3.7 兼容
            return node.s
        elif isinstance(node, ast.Name):
            if node.id in context:
                return context[node.id]
            raise NameError(f"未定义变量：{node.id}")
        elif isinstance(node, ast.BinOp):
            left = self._eval(node.left, context)
            right = self._eval(node.right, context)
            op_func = self.OPERATORS.get(type(node.op))
            if op_func:
                return op_func(left, right)
            raise ValueError(f"不支持的操作符：{type(node.op)}")
        elif isinstance(node, ast.Compare):
            left = self._eval(node.left, context)
            comparators = [self._eval(c, context) for c in node.comparators]
            ops = [type(op) for op in node.ops]

            result = True
            current = left
            for op, comparator in zip(ops, comparators):
                op_func = self.OPERATORS.get(op)
                if not op_func:
                    raise ValueError(f"不支持的比较操作符：{op}")
                if not op_func(current, comparator):
                    result = False
                    break
                current = comparator
            return result
        elif isinstance(node, ast.Call):
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            if func_name and func_name in context:
                func = context[func_name]
                args = [self._eval(arg, context) for arg in node.args]
                kwargs = {kw.arg: self._eval(kw.value, context) for kw in node.keywords if kw.arg}
                return func(*args, **kwargs)
            raise NameError(f"未定义函数：{func_name}")
        elif isinstance(node, ast.Dict):
            keys = [self._eval(k, context) for k in node.keys]
            values = [self._eval(v, context) for v in node.values]
            return dict(zip(keys, values))
        elif isinstance(node, ast.List):
            return [self._eval(elt, context) for elt in node.elts]
        elif isinstance(node, ast.Tuple):
            return tuple(self._eval(elt, context) for elt in node.elts)
        else:
            raise ValueError(f"不支持的 AST 节点类型：{type(node)}")

    def set_context(self, key: str, value: Any) -> None:
        """设置上下文变量。"""
        self._context[key] = value

    def get_context(self, key: str) -> Any:
        """获取上下文变量。"""
        return self._context.get(key)

    def clear_context(self) -> None:
        """清空上下文。"""
        self._context = {"__reality_version__": "1.0.0"}

    def get_stats(self) -> Dict[str, Any]:
        """获取 DSL 统计。"""
        return {
            "compiled_scripts": len(self._compiled_scripts),
            "context_variables": len(self._context),
            "builtin_functions": len(self.BUILTINS),
        }
