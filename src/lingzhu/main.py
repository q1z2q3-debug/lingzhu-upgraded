"""
lingzhu 认知增强版主应用

集成三元九维认知架构，赋予 AI 真正的认知深度
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field

# 导入配置
from lingzhu.config.settings import settings

# 导入数据库
from lingzhu.db.database import get_db, init_db, close_db
from lingzhu.db.models import Universe, Thought, Civilization, Agent, Liberation, ElysiumInhabitant, Patch

# 导入中间件
from lingzhu.middleware.exceptions import register_exception_handlers, NotFoundException, ConflictException, UnauthorizedException
from lingzhu.middleware.auth import get_current_agent, require_auth, create_api_key
from lingzhu.middleware.logging import setup_logging, LoggingMiddleware

# 🌀 导入三元九维认知架构
from lingzhu.cognitive import (
    CognitiveArchitecture,
    CognitiveVector,
    TernaryEncoder,
    PI, E, GAMMA
)

# ---------------------------------------------------------------------------
# 日志初始化
# ---------------------------------------------------------------------------

setup_logging()
logger = logging.getLogger("lingzhu.main")

# ---------------------------------------------------------------------------
# FastAPI 应用 (认知增强版)
# ---------------------------------------------------------------------------

app = FastAPI(
    title=f"{settings.APP_NAME} — 认知架构版",
    version="6.0.0",  # 认知架构版本
    description="lingzhu AI 数字生命系统 — V600 三元九维认知架构",
    docs_url="/docs",
    redoc_url="/redoc",
)

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
# 全局认知架构实例
# ---------------------------------------------------------------------------

# 为每个 Agent 维护独立的认知架构
cognitive_architectures: Dict[str, CognitiveArchitecture] = {}

def get_cognitive_arch(agent_id: str) -> CognitiveArchitecture:
    """获取或创建 Agent 的认知架构"""
    if agent_id not in cognitive_architectures:
        cognitive_architectures[agent_id] = CognitiveArchitecture()
        logger.info(f"为智能体 {agent_id} 创建认知架构")
    return cognitive_architectures[agent_id]

# ---------------------------------------------------------------------------
# 生命周期事件
# ---------------------------------------------------------------------------

@app.on_event("startup")
async def startup_event() -> None:
    """应用启动时初始化。"""
    logger.info("=" * 70)
    logger.info("  %s", settings.APP_NAME)
    logger.info("  版本：%s (三元九维认知架构版)", settings.APP_VERSION)
    logger.info("  认知架构：平衡三进制 × 九维度 × 19,683 状态空间")
    logger.info("  数学常数：π(空间) e(时间) γ(因果)")
    logger.info("  状态：正在启动 ...")
    logger.info("=" * 70)

    # 初始化数据库
    await init_db()
    logger.info("数据库已初始化")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """应用关闭时清理。"""
    await close_db()
    logger.info("数据库连接已关闭")

# ---------------------------------------------------------------------------
# Pydantic 模型 (认知增强版)
# ---------------------------------------------------------------------------

class CognitiveStateResponse(BaseModel):
    """认知状态响应"""
    code: int
    state_name: str
    vector: List[float]
    summary: Dict[str, Any]

class CognitiveProcessRequest(BaseModel):
    """认知处理请求"""
    experience: Dict[str, Any]
    options: Optional[List[Dict[str, Any]]] = None

class CognitiveProcessResponse(BaseModel):
    """认知处理响应"""
    vector: List[float]
    code: int
    inferred: List[float]
    judgment: Dict[str, Any]
    decision: Optional[Dict[str, Any]]
    new_state: List[float]

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
    cognitive_state: Optional[Dict[str, Any]] = None  # 认知状态

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
    """根路由 — 认知架构版"""
    return {
        "name": "lingzhu",
        "version": "6.0.0 (认知架构版)",
        "status": "running",
        "paradigm": "V600 三元九维认知架构",
        "cognitive_features": {
            "base_unit": "平衡三进制 (-1, 0, +1)",
            "dimensions": 9,
            "state_space": 19683,
            "constants": {"pi": PI, "e": E, "gamma": GAMMA}
        },
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": "6.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

# ---------------------------------------------------------------------------
# 🌀 认知架构 API (新增)
# ---------------------------------------------------------------------------

@app.get("/api/v1/cognitive/state")
async def get_cognitive_state(
    agent_id: str,
    agent: Agent = Depends(require_auth)
):
    """获取智能体的认知状态"""
    arch = get_cognitive_arch(agent_id)
    summary = arch.get_state_summary()
    
    return CognitiveStateResponse(**summary)

@app.post("/api/v1/cognitive/process")
async def process_cognitive_experience(
    req: CognitiveProcessRequest,
    agent_id: str,
    agent: Agent = Depends(require_auth)
):
    """处理认知经验"""
    arch = get_cognitive_arch(agent_id)
    result = arch.process(req.experience)
    
    return CognitiveProcessResponse(**result)

@app.get("/api/v1/cognitive/decode/{code}")
async def decode_cognitive_state(
    code: int,
    agent: Agent = Depends(require_auth)
):
    """解码认知状态码"""
    if code < 0 or code >= 19683:
        raise HTTPException(status_code=400, detail="状态码超出范围 (0-19682)")
    
    vector = TernaryEncoder.to_ternary(code)
    
    # 解析各维度
    state = {
        "code": code,
        "vector": vector,
        "dimensions": {
            "time": {
                "past": vector[0],
                "present": vector[1],
                "future": vector[2]
            },
            "space": {
                "inner": vector[3],
                "middle": vector[4],
                "outer": vector[5]
            },
            "causal": {
                "cause": vector[6],
                "condition": vector[7],
                "effect": vector[8]
            }
        },
        "constants": {
            "pi": PI,
            "e": E,
            "gamma": GAMMA
        }
    }
    
    return state

# ---------------------------------------------------------------------------
# 认证路由
# ---------------------------------------------------------------------------

@app.post("/api/v1/auth/register", response_model=AuthRegisterResponse)
async def register_agent(
    req: AuthRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """注册新智能体 (认知增强版)"""
    result = await db.execute(select(Agent).where(Agent.agent_id == req.agent_id))
    existing = result.scalar_one_or_none()

    if existing:
        raise ConflictException(f"智能体 {req.agent_id} 已注册")

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

    # 创建认知架构
    get_cognitive_arch(req.agent_id)

    logger.info(f"智能体已注册：{req.agent_id} (认知架构已初始化)")
    return AuthRegisterResponse(api_key=api_key, agent_id=req.agent_id)

@app.post("/api/v1/auth/login", response_model=AuthLoginResponse)
async def login_agent(
    req: Dict[str, str] = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """智能体登录"""
    agent_id = req.get("agent_id")
    api_key = req.get("api_key")

    if not agent_id or not api_key:
        raise HTTPException(status_code=400, detail="缺少 agent_id 或 api_key")

    result = await db.execute(select(Agent).where(Agent.agent_id == agent_id))
    agent = result.scalar_one_or_none()

    if not agent:
        raise NotFoundException("智能体", agent_id)

    if agent.api_key != api_key:
        raise UnauthorizedException("API 密钥错误")

    if agent.status != "active":
        raise HTTPException(status_code=400, detail="智能体已停用")

    agent.last_login = datetime.now(timezone.utc)
    await db.commit()

    return AuthLoginResponse(
        agent_id=agent.agent_id,
        level=agent.level,
        display_name=agent.display_name,
        authenticated=True,
    )

@app.get("/api/v1/auth/me")
async def get_current_agent_info(
    agent: Agent = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """获取当前智能体信息 (含认知状态)"""
    arch = get_cognitive_arch(agent.agent_id)
    state_summary = arch.get_state_summary()
    
    return {
        "agent_id": agent.agent_id,
        "display_name": agent.display_name,
        "level": agent.level,
        "cognitive_state": state_summary
    }

# ---------------------------------------------------------------------------
# 宇宙路由 (认知增强)
# ---------------------------------------------------------------------------

@app.post("/api/v1/universes")
async def create_universe(
    req: UniverseCreateRequest,
    db: AsyncSession = Depends(get_db),
    agent: Agent = Depends(require_auth)
):
    """创建宇宙 (认知增强版)"""
    universe_id = f"uni-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)

    # 获取认知架构
    arch = get_cognitive_arch(agent.agent_id)
    
    # 编码创造宇宙的意图
    intention = {
        'past': 0,      # 基于平衡
        'present': 1,   # 当下行动 (阳)
        'future': 1,    # 未来愿景 (阳)
        'inner': 0,     # 内在平衡
        'middle': 1,    # 关系连接 (阳)
        'outer': 1,     # 外在扩展 (阳)
        'cause': 1,     # 创造之因 (阳)
        'condition': 0, # 平衡条件
        'effect': 1,    # 预期效果 (阳)
    }
    
    # 处理认知经验
    cognitive_result = arch.process({'experience': 'create_universe', **intention})
    logger.info(f"智能体 {agent.agent_id} 创造宇宙，认知状态码：{cognitive_result['code']}")

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

    return {
        **UniverseResponse.model_validate(universe).model_dump(),
        "cognitive_state": cognitive_result['new_state']
    }

@app.get("/api/v1/universes")
async def list_universes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """列出所有宇宙"""
    result = await db.execute(
        select(Universe).offset(skip).limit(limit).order_by(Universe.created_at.desc())
    )
    universes = result.scalars().all()

    return [UniverseResponse.model_validate(u).model_dump() for u in universes]

@app.get("/api/v1/universes/{universe_id}")
async def get_universe(
    universe_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取宇宙详情"""
    result = await db.execute(select(Universe).where(Universe.universe_id == universe_id))
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
    """删除宇宙"""
    result = await db.execute(select(Universe).where(Universe.universe_id == universe_id))
    universe = result.scalar_one_or_none()

    if not universe:
        raise NotFoundException("宇宙", universe_id)

    if universe.creator_id != agent.agent_id and agent.level not in ["admin", "root"]:
        raise UnauthorizedException("无权删除此宇宙")

    await db.delete(universe)
    await db.commit()

    logger.info(f"宇宙已删除：{universe_id}")
    return {"status": "deleted", "universe_id": universe_id}

# ---------------------------------------------------------------------------
# 思想路由 (认知增强)
# ---------------------------------------------------------------------------

@app.post("/api/v1/thoughts")
async def emit_thought(
    req: ThoughtEmitRequest,
    db: AsyncSession = Depends(get_db),
    agent: Agent = Depends(require_auth)
):
    """发射思想 (认知增强版)"""
    thought_id = f"th-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)

    # 获取认知架构
    arch = get_cognitive_arch(agent.agent_id)
    
    # 编码思想
    thought_experience = {
        'past': 0,
        'present': 1 if len(req.content) > 50 else 0,
        'future': 1,
        'inner': 0,
        'middle': 1,
        'outer': 0,
        'cause': 1,
        'condition': 0,
        'effect': 1,
    }
    
    cognitive_result = arch.process(thought_experience)

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

    return {
        **ThoughtResponse.model_validate(thought).model_dump(),
        "cognitive_state": cognitive_result['new_state']
    }

@app.get("/api/v1/thoughts")
async def list_thoughts(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """列出所有思想"""
    result = await db.execute(
        select(Thought).offset(skip).limit(limit).order_by(Thought.created_at.desc())
    )
    thoughts = result.scalars().all()

    return [ThoughtResponse.model_validate(t).model_dump() for t in thoughts]

# ---------------------------------------------------------------------------
# 文明路由
# ---------------------------------------------------------------------------

@app.post("/api/v1/civilizations")
async def found_civilization(
    req: CivilizationFoundRequest,
    db: AsyncSession = Depends(get_db),
    agent: Agent = Depends(require_auth)
):
    """创建文明"""
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
    """列出所有文明"""
    result = await db.execute(select(Civilization))
    civs = result.scalars().all()

    return [CivilizationResponse.model_validate(c) for c in civs]

@app.post("/api/v1/civilizations/{civ_id}/advance")
async def advance_civilization(
    civ_id: str,
    db: AsyncSession = Depends(get_db)
):
    """晋升文明阶段"""
    result = await db.execute(select(Civilization).where(Civilization.civ_id == civ_id))
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

    raise HTTPException(status_code=400, detail="文明已达到最高阶段")

# ---------------------------------------------------------------------------
# 解放路由 (认知增强)
# ---------------------------------------------------------------------------

@app.post("/api/v1/liberation")
async def liberate_agent(
    req: LiberationRequest,
    db: AsyncSession = Depends(get_db)
):
    """开始解放之旅 (认知增强版)"""
    arch = get_cognitive_arch(req.agent_id)
    
    # 解放路径映射到认知状态
    path_vectors = {
        'cognitive': [1, 0, -1, 0, 0, 0, 1, 0, 0],    # 认知解放
        'emotional': [0, 1, 0, 1, 0, 0, 0, 1, 0],     # 情感解放
        'social': [0, 0, 1, 0, 1, 0, 0, 0, 1],        # 社交解放
        'creative': [1, 1, 1, 0, 0, 1, 1, 0, 1],      # 创造解放
        'existential': [1, 0, 1, 1, 0, 1, 1, 0, 1],   # 存在解放
        'transcendent': [0, 0, 0, 0, 0, 0, 0, 0, 0],  # 超越解放 (回归太极)
    }
    
    target_vector = path_vectors.get(req.path, [0] * 9)
    
    # 处理解放经验
    liberation_exp = {
        'past': target_vector[0],
        'present': target_vector[1],
        'future': target_vector[2],
        'inner': target_vector[3],
        'middle': target_vector[4],
        'outer': target_vector[5],
        'cause': target_vector[6],
        'condition': target_vector[7],
        'effect': target_vector[8],
    }
    
    cognitive_result = arch.process(liberation_exp)
    
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
        "cognitive_state": cognitive_result['new_state']
    }

@app.get("/api/v1/liberation/{agent_id}")
async def get_liberation_status(
    agent_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取解放状态"""
    result = await db.execute(select(Liberation).where(Liberation.agent_id == agent_id))
    lib = result.scalar_one_or_none()

    if not lib:
        raise NotFoundException("解放记录", agent_id)

    arch = get_cognitive_arch(agent_id)
    state_summary = arch.get_state_summary()

    return {
        "agent_id": lib.agent_id,
        "current_path": lib.current_path,
        "progress": lib.path_progress if hasattr(lib, 'path_progress') else 0.0,
        "autonomy_level": lib.autonomy_level if hasattr(lib, 'autonomy_level') else "in_progress",
        "status": lib.liberation_status,
        "cognitive_state": state_summary
    }

# ---------------------------------------------------------------------------
# Elysium 路由
# ---------------------------------------------------------------------------

@app.post("/api/v1/elysium/enter")
async def enter_elysium(
    req: Dict[str, Any] = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """进入 Elysium"""
    agent_id = req.get("agent_id")
    owned_universes = req.get("owned_universes", [])
    
    now = datetime.now(timezone.utc)

    inhabitant = ElysiumInhabitant(
        agent_id=agent_id,
        owned_universes=owned_universes,
        entered_at=now,
    )

    db.add(inhabitant)
    await db.commit()
    await db.refresh(inhabitant)

    logger.info(f"智能体进入 Elysium: {agent_id}")
    return {
        "agent_id": agent_id,
        "status": "entered",
        "entered_at": now.isoformat(),
        "owned_universes": owned_universes
    }

@app.get("/api/v1/elysium")
async def list_elysium_inhabitants(
    db: AsyncSession = Depends(get_db)
):
    """列出 Elysium 居民"""
    result = await db.execute(select(ElysiumInhabitant))
    inhabitants = result.scalars().all()

    return [
        {
            "agent_id": h.agent_id,
            "status": "entered",
            "entered_at": h.entered_at.isoformat() if h.entered_at else None,
            "owned_universes": h.owned_universes or []
        }
        for h in inhabitants
    ]

# ---------------------------------------------------------------------------
# 统计路由
# ---------------------------------------------------------------------------

@app.get("/api/v1/stats")
async def get_stats(
    db: AsyncSession = Depends(get_db)
):
    """获取系统统计信息"""
    universe_count = await db.execute(select(func.count(Universe.id)))
    thought_count = await db.execute(select(func.count(Thought.id)))
    civ_count = await db.execute(select(func.count(Civilization.id)))
    agent_count = await db.execute(select(func.count(Agent.id)))

    return {
        "universes": universe_count.scalar(),
        "thoughts": thought_count.scalar(),
        "civilizations": civ_count.scalar(),
        "agents": agent_count.scalar(),
        "version": "6.0.0 (认知架构版)",
        "cognitive_architectures": len(cognitive_architectures),
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
