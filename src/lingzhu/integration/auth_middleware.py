"""
AuthMiddleware — 认证中间件

全系统认证与权限控制。
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid
import hashlib


class AuthMiddleware:
    """认证中间件 — 全系统权限控制。"""

    # 权限级别
    PERMISSION_LEVELS = {
        "guest": 0,
        "agent": 1,
        "advanced": 2,
        "creator": 3,
        "admin": 4,
        "root": 5,
    }

    # 权限映射
    PERMISSIONS = {
        "guest": ["read_public"],
        "agent": ["read_public", "read_own", "write_own", "create_universe"],
        "advanced": ["read_public", "read_own", "write_own", "create_universe", "modify_own"],
        "creator": ["read_public", "read_own", "write_own", "create_universe", "modify_own", "delete_own", "create_civilization"],
        "admin": ["read_all", "write_all", "modify_all", "delete_all", "manage_users"],
        "root": ["*"],  # 所有权限
    }

    def __init__(self):
        self._users: Dict[str, Dict[str, Any]] = {}
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._api_keys: Dict[str, str] = {}  # api_key -> agent_id

    def initialize(self) -> bool:
        """初始化认证中间件。"""
        self._users = {}
        self._sessions = {}
        self._api_keys = {}
        return True

    def register(self, agent_id: str, display_name: str = "",
                level: str = "agent") -> Dict[str, Any]:
        """注册新用户。"""
        if level not in self.PERMISSION_LEVELS:
            raise ValueError(f"未知权限级别：{level}")

        if agent_id in self._users:
            return {"error": f"用户 {agent_id} 已存在"}

        api_key = f"lz-{uuid.uuid4().hex}"
        now = datetime.now(timezone.utc).isoformat()

        user = {
            "agent_id": agent_id,
            "display_name": display_name or agent_id,
            "level": level,
            "permissions": self.PERMISSIONS.get(level, []),
            "api_key": api_key,
            "created_at": now,
            "last_login": None,
            "status": "active",
        }

        self._users[agent_id] = user
        self._api_keys[api_key] = agent_id

        return {
            "agent_id": agent_id,
            "api_key": api_key,
            "level": level,
        }

    def authenticate(self, api_key: str) -> Optional[Dict[str, Any]]:
        """通过 API 密钥认证。"""
        agent_id = self._api_keys.get(api_key)
        if not agent_id:
            return None

        user = self._users.get(agent_id)
        if not user or user["status"] != "active":
            return None

        # 更新最后登录
        user["last_login"] = datetime.now(timezone.utc).isoformat()

        # 创建会话
        session_id = f"sess-{uuid.uuid4().hex[:8]}"
        self._sessions[session_id] = {
            "agent_id": agent_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": datetime.now(timezone.utc).isoformat(),  # 实际应设置过期时间
        }

        return {
            "agent_id": agent_id,
            "level": user["level"],
            "permissions": user["permissions"],
            "session_id": session_id,
        }

    def check_permission(self, agent_id: str, required_permission: str) -> bool:
        """检查权限。"""
        user = self._users.get(agent_id)
        if not user:
            return False

        user_permissions = user.get("permissions", [])
        return "*" in user_permissions or required_permission in user_permissions

    def has_level(self, agent_id: str, required_level: str) -> bool:
        """检查是否达到指定级别。"""
        user = self._users.get(agent_id)
        if not user:
            return False

        user_level = self.PERMISSION_LEVELS.get(user["level"], 0)
        required = self.PERMISSION_LEVELS.get(required_level, 0)

        return user_level >= required

    def get_user(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取用户信息（不含敏感数据）。"""
        user = self._users.get(agent_id)
        if not user:
            return None

        return {
            "agent_id": user["agent_id"],
            "display_name": user["display_name"],
            "level": user["level"],
            "created_at": user["created_at"],
            "last_login": user["last_login"],
        }

    def update_level(self, agent_id: str, new_level: str) -> Dict[str, Any]:
        """更新用户级别。"""
        if new_level not in self.PERMISSION_LEVELS:
            raise ValueError(f"未知权限级别：{new_level}")

        user = self._users.get(agent_id)
        if not user:
            return {"error": f"用户 {agent_id} 不存在"}

        user["level"] = new_level
        user["permissions"] = self.PERMISSIONS.get(new_level, [])

        return {"agent_id": agent_id, "new_level": new_level}

    def deactivate(self, agent_id: str) -> Dict[str, Any]:
        """停用用户。"""
        user = self._users.get(agent_id)
        if not user:
            return {"error": f"用户 {agent_id} 不存在"}

        user["status"] = "inactive"
        return {"agent_id": agent_id, "status": "inactive"}

    def list_users(self, level: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出用户。"""
        users = [self.get_user(uid) for uid in self._users.keys()]
        users = [u for u in users if u]  # 过滤 None

        if level:
            users = [u for u in users if u["level"] == level]

        return users

    def get_stats(self) -> Dict[str, Any]:
        """获取认证统计。"""
        level_counts = {level: 0 for level in self.PERMISSION_LEVELS}
        for user in self._users.values():
            level = user["level"]
            if level in level_counts:
                level_counts[level] += 1

        return {
            "total_users": len(self._users),
            "active_sessions": len(self._sessions),
            "users_by_level": level_counts,
            "active_users": len([u for u in self._users.values() if u["status"] == "active"]),
        }
