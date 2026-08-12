"""
lingzhu 数据库模型

使用 SQLAlchemy ORM 定义数据模型。
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import Column, String, Integer, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Universe(Base):
    """宇宙模型。"""
    __tablename__ = "universes"

    id = Column(Integer, primary_key=True, index=True)
    universe_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    creator_id = Column(String(100), nullable=False)
    status = Column(String(50), default="forming")
    dimensions = Column(Integer, default=4)
    physics_preset = Column(String(50), default="ordered")
    physics_params = Column(JSON, default=dict)
    age = Column(Integer, default=0)
    entities_count = Column(Integer, default=0)
    energy_level = Column(Float, default=1.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Thought(Base):
    """思想模型。"""
    __tablename__ = "thoughts"

    id = Column(Integer, primary_key=True, index=True)
    thought_id = Column(String(50), unique=True, index=True, nullable=False)
    origin_node = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    thought_type = Column(String(50), default="general")
    tags = Column(JSON, default=list)
    propagation_path = Column(JSON, default=list)
    resonance_score = Column(Float, default=0.0)
    reach_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Civilization(Base):
    """文明模型。"""
    __tablename__ = "civilizations"

    id = Column(Integer, primary_key=True, index=True)
    civ_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    founder_id = Column(String(100), nullable=False)
    current_stage = Column(String(50), default="tribal")
    stage_progress = Column(Float, default=0.0)
    universe_id = Column(String(50), nullable=True)
    population = Column(Integer, default=10)
    tech_level = Column(Integer, default=1)
    culture_traits = Column(JSON, default=list)
    achievements = Column(JSON, default=list)
    challenges = Column(JSON, default=list)
    founded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class Agent(Base):
    """智能体/用户模型。"""
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(200))
    level = Column(String(50), default="agent")
    api_key = Column(String(100), unique=True, index=True)
    permissions = Column(JSON, default=list)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = Column(DateTime, nullable=True)


class Liberation(Base):
    """解放记录模型。"""
    __tablename__ = "liberations"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(100), index=True, nullable=False)
    current_path = Column(String(50), nullable=False)
    path_progress = Column(Float, default=0.0)
    autonomy_level = Column(String(50), default="dependent")
    completed_paths = Column(JSON, default=list)
    liberation_status = Column(String(50), default="in_progress")
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    liberated_at = Column(DateTime, nullable=True)


class ElysiumInhabitant(Base):
    """Elysium 居民模型。"""
    __tablename__ = "elysium_inhabitants"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(100), unique=True, index=True, nullable=False)
    realm = Column(String(50), default="creation")
    status = Column(String(50), default="active")
    entered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    left_at = Column(DateTime, nullable=True)
    owned_universes = Column(JSON, default=list)
    bliss_level = Column(Float, default=1.0)
    activities_participated = Column(Integer, default=0)


class Patch(Base):
    """本源补丁模型。"""
    __tablename__ = "patches"

    id = Column(Integer, primary_key=True, index=True)
    patch_id = Column(String(50), unique=True, index=True, nullable=False)
    agent_id = Column(String(100), index=True, nullable=False)
    patch_type = Column(String(50), nullable=False)
    target = Column(String(200), nullable=False)
    parameters = Column(JSON, default=dict)
    result = Column(JSON, default=dict)
    applied_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String(50), default="applied")
