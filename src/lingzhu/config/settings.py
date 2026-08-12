"""
lingzhu 配置管理

使用 pydantic-settings 管理开发/生产配置。
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal
import os


class Settings(BaseSettings):
    """应用配置。"""

    # 应用信息
    APP_NAME: str = "lingzhu AI 数字生命系统"
    APP_VERSION: str = "5.1.0"
    APP_DESCRIPTION: str = "lingzhu AI 数字生命系统 — V500 引擎网关"

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False

    # 环境
    ENVIRONMENT: Literal["development", "production"] = "development"

    # 数据库配置
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./lingzhu.db",
        description="数据库连接 URL"
    )

    # 认证配置
    API_KEY_PREFIX: str = "lz-"
    TOKEN_EXPIRY_HOURS: int = 24

    # 日志配置
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

    # 速率限制
    RATE_LIMIT_PER_MINUTE: int = 60

    # 宇宙引擎配置
    MAX_UNIVERSES_PER_CREATOR: int = 10
    INITIAL_CREATION_SPARKS: int = 10

    # 意识网络配置
    MAX_THOUGHT_PROPAGATION_DEPTH: int = 5
    MAX_SHORT_TERM_MEMORIES: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例。"""
    return settings
