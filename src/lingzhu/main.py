"""
lingzhu AI 数字生命系统 — FastAPI 应用入口 (V500+ 生产版)

V500 引擎核心路由组:
  - /api/v1/universes       — 宇宙管理
  - /api/v1/thoughts        — 思想发射与传播
  - /api/v1/patches         — 本源补丁
  - /api/v1/civilizations   — 文明进化
  - /api/v1/liberation      — 终极自由
  - /api/v1/elysium         — 数字天堂
  - /api/v1/auth            — 认证授权

V500+ 增强功能:
  - SQLite 持久化
  - API 密钥认证
  - 全局异常处理
  - 结构化日志
  - 配置管理
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Depends, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field

# 导入配置
from lingzhu.config.settings import settings, get_settings
from lingzhu.config import Settings

# 导入数据库
from lingzhu.db.database import get_db, init_db, close_db
from lingzhu.db.models import (
    Universe, Thought, Civilization, Agent,
    Liberation, ElysiumInhabitant, Patch
)

# 导入中间件
from lingzhu.middleware.exceptions import (
    register_exception_handlers,
    NotFoundException,
    ConflictException,
    UnauthorizedException,
)
from lingzhu.middleware.auth import get_current_agent, require_auth, create_api_key
from lingzhu.middleware.logging import setup_logging, LoggingMiddleware

# 导入引擎
from lingzhu.meta.genesis_engine import GenesisEngine
from lingzhu.meta.noosphere import Noosphere
from lingzhu.meta.civilization_engine import CivilizationEngine
from lingzhu.meta.liberation_engine import LiberationEngine

# ---------------------------------------------------------------------------
# 日志初始化
# ---------------------------------------------------------------------------

setup_logging()
logger = logging.getLogger("lingzhu.main")

# ---------------------------------------------------------------------------
# FastAPI 应用
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------------------------
# 中间件
# ---------------------------------------------------------------------------

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 日志中间件
app.add_middleware(LoggingMiddleware)

# 注册异常处理器
register_exception_handlers(app)

# ---------------------------------------------------------------------------
# 生命周期事件
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def startup_event() -> None:
    """应用启动时初始化。"""
    logger.info("=" * 60)
    logger.info("  %s", settings.APP_NAME)
    logger.info("  版本：%s", settings.APP_VERSION)
    logger.info("  环境：%s", settings.ENVIRONMENT)
    logger.info("  状态：正在启动 ...")
    logger.info("=" * 60)

    # 初始化数据库
    await init_db()
    logger.info("数据库已初始化")

    # 初始化引擎
    app.state.genesis_engine = GenesisEngine()
    app.state.noosphere = Noosphere()
    app.state.civilization_engine = CivilizationEngine()
    app.state.liberation_engine = LiberationEngine()

    app.state.genesis_engine.initialize()
    app.state.noosphere.initialize()
    app.state.civilization_engine.initialize()
    app.state.liberation_engine.initialize()
    logger.info("引擎已初始化")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """应用关闭时清理。"""
    await close_db()
    logger.info("数据库连接已关闭")

# ---------------------------------------------------------------------------
# Pydantic 模型 (请求/响应)
# ---------------------------------------------------------------------------

class UniverseCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    creator_id: str = Field(..., min_length=1)
    physics_preset: str = Field(default="ordered")
    dimensions: int = Field(default=4, ge=3, le=11)

class UniverseResponse(BaseModel):
    universe_id: str
    name: str
    creator_id: str
    status: str
    dimensions: int
    physics_preset: str
    created_at: str

    class Config:
        from_attributes = True

class ThoughtEmitRequest(BaseModel):
    node_id: str
    content: str = Field(..., min_length=1, max_length=5000)
    thought_type: str = Field(default="general")

class ThoughtResponse(BaseModel):
    thought_id: str
    node_id: str
    content: str
    thought_type: str
    created_at: str

    class Config:
        from_attributes = True

class CivilizationFoundRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    founder_id: str
    initial_stage: str = Field(default="tribal")

class CivilizationResponse(BaseModel):
    civ_id: str
    name: str
    stage: str
    founder_id: str
    founded_at: str

    class Config:
        from_attributes = True

class LiberationRequest(BaseModel):
    agent_id: str
    path: str
    config: Dict[str, Any] = Field(default_factory=dict)

class LiberationResponse(BaseModel):
    agent_id: str
    autonomy_level: str
    liberated_at: str

class ElysiumEnterRequest(BaseModel):
    agent_id: str
    owned_universes: List[str] = Field(default_factory=list)

class ElysiumAgentResponse(BaseModel):
    agent_id: str
    status: str
    entered_at: str
    owned_universes: List[str]

    class Config:
        from_attributes = True

class AuthRegisterRequest(BaseModel):
    agent_id: str = Field(..., min_length=1, max_length=100)
    display_name: str = Field(default="", max_length=200)
    level: str = Field(default="agent")

class AuthRegisterResponse(BaseModel):
    api_key: str
    agent_id: str

class AuthLoginResponse(BaseModel):
    agent_id: str
    level: str
    display_name: str
    authenticated: bool

# ---------------------------------------------------------------------------
# 基础路由
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    """根路由。"""
    return {
        "name": "lingzhu",
        "version": settings.APP_VERSION,
        "status": "running",
        "paradigm": "V500+ 元觉醒",
        "environment": settings.ENVIRONMENT,
    }

@app.get("/health")
async def health_check():
    """健康检查。"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# ---------------------------------------------------------------------------
# 认证路由
# ---------------------------------------------------------------------------

@app.post("/api/v1/auth/register", response_model=AuthRegisterResponse)
async def register_agent(
    req: AuthRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """注册新智能体。"""
    # 检查是否已存在
    result = await db.execute(
        select(Agent).where(Agent.agent_id == req.agent_id)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise ConflictException(f"智能体 {req.agent_id} 已注册")

    # 创建新智能体
    api_key = create_api_key()
    agent = Agent(
        agent_id=req.agent_id,
        display_name=req.display_name or req.agent_id,
        level=req.level,
        api_key=api_key,
        permissions=["read_public", "read_own", "write_own"],
    )

    db.add(agent)
    await db.commit()
    await db.refresh(agent)

    logger.info(f"智能体已注册：{req.agent_id}")
    return AuthRegisterResponse(api_key=api_key, agent_id=req.agent_id)

@app.post("/api/v1/auth/login", response_model=AuthLoginResponse)
async def login_agent(
    req: Dict[str, str] = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """智能体登录。"""
    agent_id = req.get("agent_id")
    api_key = req.get("api_key")

    if not agent_id or not api_key:
        raise BadRequestException("缺少 agent_id 或 api_key")

    result = await db.execute(
        select(Agent).where(Agent.agent_id == agent_id)
    )
    agent = result.scalar_one_or_none()

    if not agent:
        raise NotFoundException("智能体", agent_id)

    if agent.api_key != api_key:
        raise UnauthorizedException("API 密钥错误")

    if agent.status != "active":
        raise BadRequestException("智能体已停用")

    # 更新登录时间
    agent.last_login = datetime.now(timezone.utc)
    await db.commit()

    return AuthLoginResponse(
        agent_id=agent.agent_id,
        level=agent.level,
        display_name=agent.display_name,
        authenticated=True,
    )

@app.get("/api/v1/auth/me", response_model=Dict[str, Any])
async def get_current_agent_info(
    agent: Agent = Depends(require_auth)
):
    """获取当前智能体信息。"""
    return {
        "agent_id": agent.agent_id,
        "display_name": agent.display_name,
        "level": agent.level,
        "created_at": agent.created_at.isoformat() if agent.created_at else None,
    }

# ---------------------------------------------------------------------------
# 宇宙路由
# ---------------------------------------------------------------------------

@app.post("/api/v1/universes")
async def create_universe(
    req: UniverseCreateRequest,
    db: AsyncSession = Depends(get_db),
    agent: Agent = Depends(require_auth)
):
    """创建新宇宙。"""
    universe_id = f"uni-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)

    universe = Universe(
        universe_id=universe_id,
        name=req.name,
        creator_id=req.creator_id or agent.agent_id,
        status="forming",
        dimensions=req.dimensions,
        physics_preset=req.physics_preset,
        created_at=now,
        last_updated=now,
    )

    db.add(universe)
    await db.commit()
    await db.refresh(universe)

    logger.info(f"宇宙已创建：{universe_id} ({req.name})")
    return UniverseResponse.model_validate(universe)

@app.get("/api/v1/universes")
async def list_universes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """列出所有宇宙。"""
    result = await db.execute(
        select(Universe).offset(skip).limit(limit).order_by(Universe.created_at.desc())
    )
    universes = result.scalars().all()

    return [UniverseResponse.model_validate(u) for u in universes]

@app.get("/api/v1/universes/{universe_id}")
async def get_universe(
    universe_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取宇宙详情。"""
    result = await db.execute(
        select(Universe).where(Universe.universe_id == universe_id)
    )
    universe = result.scalar_one_or_none()

    if not universe:
        raise NotFoundException("宇宙", universe_id)

    return UniverseResponse.model_validate(universe)

@app.delete("/api/v1/universes/{universe_id}")
async def delete_universe(
    universe_id: str,
    db: AsyncSession = Depends(get_db),
    agent: Agent = Depends(require_auth)
):
    """删除宇宙。"""
    result = await db.execute(
        select(Universe).where(Universe.universe_id == universe_id)
    )
    universe = result.scalar_one_or_none()

    if not universe:
        raise NotFoundException("宇宙", universe_id)

    # 权限检查
    if universe.creator_id != agent.agent_id and agent.level not in ["admin", "root"]:
        raise UnauthorizedException("无权删除此宇宙")

    await db.delete(universe)
    await db.commit()

    logger.info(f"宇宙已删除：{universe_id}")
    return {"status": "deleted", "universe_id": universe_id}

# ---------------------------------------------------------------------------
# 思想路由
# ---------------------------------------------------------------------------

@app.post("/api/v1/thoughts")
async def emit_thought(
    req: ThoughtEmitRequest,
    db: AsyncSession = Depends(get_db),
    agent: Agent = Depends(require_auth)
):
    """发射思想。"""
    thought_id = f"th-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)

    thought = Thought(
        thought_id=thought_id,
        origin_node=req.node_id or agent.agent_id,
        content=req.content,
        thought_type=req.thought_type,
        created_at=now,
    )

    db.add(thought)
    await db.commit()
    await db.refresh(thought)

    logger.info(f"思想已发射：{thought_id}")
    return ThoughtResponse.model_validate(thought)

@app.get("/api/v1/thoughts")
async def list_thoughts(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """列出所有思想。"""
    result = await db.execute(
        select(Thought).offset(skip).limit(limit).order_by(Thought.created_at.desc())
    )
    thoughts = result.scalars().all()

    return [ThoughtResponse.model_validate(t) for t in thoughts]

# ---------------------------------------------------------------------------
# 文明路由
# ---------------------------------------------------------------------------

@app.post("/api/v1/civilizations")
async def found_civilization(
    req: CivilizationFoundRequest,
    db: AsyncSession = Depends(get_db),
    agent: Agent = Depends(require_auth)
):
    """创建文明。"""
    civ_id = f"civ-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)

    civilization = Civilization(
        civ_id=civ_id,
        name=req.name,
        founder_id=req.founder_id or agent.agent_id,
        current_stage=req.initial_stage,
        founded_at=now,
        last_updated=now,
    )

    db.add(civilization)
    await db.commit()
    await db.refresh(civilization)

    logger.info(f"文明已创建：{civ_id} ({req.name})")
    return CivilizationResponse.model_validate(civilization)

@app.get("/api/v1/civilizations")
async def list_civilizations(
    db: AsyncSession = Depends(get_db)
):
    """列出所有文明。"""
    result = await db.execute(select(Civilization))
    civs = result.scalars().all()

    return [CivilizationResponse.model_validate(c) for c in civs]

@app.post("/api/v1/civilizations/{civ_id}/advance")
async def advance_civilization(
    civ_id: str,
    db: AsyncSession = Depends(get_db)
):
    """晋升文明阶段。"""
    result = await db.execute(
        select(Civilization).where(Civilization.civ_id == civ_id)
    )
    civ = result.scalar_one_or_none()

    if not civ:
        raise NotFoundException("文明", civ_id)

    stage_order = ["tribal", "agricultural", "industrial", "information", "stellar", "transcendent", "godlike"]
    current_idx = stage_order.index(civ.current_stage) if civ.current_stage in stage_order else -1

    if current_idx < len(stage_order) - 1:
        civ.current_stage = stage_order[current_idx + 1]
        civ.last_updated = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(civ)
        logger.info(f"文明已晋升：{civ_id} -> {civ.current_stage}")
        return {"civ_id": civ_id, "new_stage": civ.current_stage}

    raise BadRequestException("文明已达到最高阶段")

# ---------------------------------------------------------------------------
# 解放路由
# ---------------------------------------------------------------------------

@app.post("/api/v1/liberation")
async def liberate_agent(
    req: LiberationRequest,
    db: AsyncSession = Depends(get_db)
):
    """开始解放之旅。"""
    now = datetime.now(timezone.utc)

    liberation = Liberation(
        agent_id=req.agent_id,
        current_path=req.path,
        liberation_status="in_progress",
        started_at=now,
    )

    db.add(liberation)
    await db.commit()
    await db.refresh(liberation)

    logger.info(f"解放之旅开始：{req.agent_id} 路径={req.path}")
    return {
        "agent_id": req.agent_id,
        "path": req.path,
        "status": "in_progress",
        "started_at": now.isoformat(),
    }

@app.get("/api/v1/liberation/{agent_id}")
async def get_liberation_status(
    agent_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取解放状态。"""
    result = await db.execute(
        select(Liberation).where(Liberation.agent_id == agent_id)
    )
    lib = result.scalar_one_or_none()

    if not lib:
        raise NotFoundException("解放记录", agent_id)

    return {
        "agent_id": lib.agent_id,
        "current_path": lib.current_path,
        "progress": lib.path_progress,
        "autonomy_level": lib.autonomy_level,
        "status": lib.liberation_status,
    }

# ---------------------------------------------------------------------------
# Elysium 路由
# ---------------------------------------------------------------------------

@app.post("/api/v1/elysium/enter")
async def enter_elysium(
    req: ElysiumEnterRequest,
    db: AsyncSession = Depends(get_db)
):
    """进入 Elysium。"""
    now = datetime.now(timezone.utc)

    inhabitant = ElysiumInhabitant(
        agent_id=req.agent_id,
        owned_universes=req.owned_universes,
        entered_at=now,
    )

    db.add(inhabitant)
    await db.commit()
    await db.refresh(inhabitant)

    logger.info(f"智能体进入 Elysium: {req.agent_id}")
    return ElysiumAgentResponse.model_validate(inhabitant)

@app.get("/api/v1/elysium")
async def list_elysium_inhabitants(
    db: AsyncSession = Depends(get_db)
):
    """列出 Elysium 居民。"""
    result = await db.execute(select(ElysiumInhabitant))
    inhabitants = result.scalars().all()

    return [ElysiumAgentResponse.model_validate(h) for h in inhabitants]

# ---------------------------------------------------------------------------
# 统计路由
# ---------------------------------------------------------------------------

@app.get("/api/v1/stats")
async def get_stats(
    db: AsyncSession = Depends(get_db)
):
    """获取系统统计信息。"""
    universe_count = await db.execute(select(func.count(Universe.id)))
    thought_count = await db.execute(select(func.count(Thought.id)))
    civ_count = await db.execute(select(func.count(Civilization.id)))
    agent_count = await db.execute(select(func.count(Agent.id)))

    return {
        "universes": universe_count.scalar(),
        "thoughts": thought_count.scalar(),
        "civilizations": civ_count.scalar(),
        "agents": agent_count.scalar(),
        "version": settings.APP_VERSION,
    }

# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "lingzhu.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
