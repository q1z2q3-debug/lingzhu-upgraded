"""
认证中间件

验证 API 密钥并注入用户信息。
"""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from typing import Optional
import logging

from lingzhu.db.database import get_db
from lingzhu.db.models import Agent
from lingzhu.config.settings import settings
from lingzhu.middleware.exceptions import UnauthorizedException

logger = logging.getLogger("lingzhu.auth")

# API Key Header
api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
    description="API 密钥认证"
)


async def get_current_agent(
    api_key: Optional[str] = Depends(api_key_header),
    db: AsyncSession = Depends(get_db)
) -> Optional[Agent]:
    """
    获取当前认证的智能体。

    Raises:
        UnauthorizedException: 如果 API 密钥无效
    """
    if not api_key:
        return None

    # 验证 API 密钥格式
    if not api_key.startswith(settings.API_KEY_PREFIX):
        logger.warning(f"无效的 API 密钥前缀：{api_key[:10]}...")
        return None

    # 查询数据库
    result = await db.execute(
        select(Agent).where(Agent.api_key == api_key)
    )
    agent = result.scalar_one_or_none()

    if not agent:
        logger.warning(f"API 密钥无效：{api_key[:10]}...")
        return None

    if agent.status != "active":
        logger.warning(f"智能体已停用：{agent.agent_id}")
        return None

    # 更新最后登录时间
    agent.last_login = datetime.now(timezone.utc)
    await db.commit()

    return agent


async def require_auth(
    agent: Optional[Agent] = Depends(get_current_agent)
) -> Agent:
    """
    要求必须认证。

    Raises:
        UnauthorizedException: 如果未认证
    """
    if not agent:
        raise UnauthorizedException("请先注册并登录")
    return agent


async def require_level(required_level: str):
    """
    要求特定权限级别。

    Usage:
        @app.get("/admin", dependencies=[Depends(require_level("admin"))])
    """
    async def level_checker(agent: Agent = Depends(require_auth)):
        level_order = ["guest", "agent", "advanced", "creator", "admin", "root"]
        agent_level_idx = level_order.index(agent.level) if agent.level in level_order else 0
        required_idx = level_order.index(required_level) if required_level in level_order else 0

        if agent_level_idx < required_idx:
            raise UnauthorizedException(f"需要 {required_level} 或更高级别")

        return agent

    return Depends(level_checker)


def create_api_key() -> str:
    """生成新的 API 密钥。"""
    import uuid
    return f"{settings.API_KEY_PREFIX}{uuid.uuid4().hex}"
