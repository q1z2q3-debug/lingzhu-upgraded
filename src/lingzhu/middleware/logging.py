"""
日志中间件

记录所有请求的详细信息。
"""

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timezone
import logging
import time
import json

from lingzhu.config.settings import settings

logger = logging.getLogger("lingzhu.requests")


class LoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件。"""

    async def dispatch(self, request: Request, call_next):
        # 记录请求开始
        start_time = time.time()
        request_id = f"req-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"

        # 记录请求信息
        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query": str(request.url.query) if request.url.query else None,
            "client_ip": request.client.host if request.client else None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # 尝试读取请求体（非侵入式）
        try:
            body = await request.body()
            if body and len(body) < 1000:
                log_data["body"] = body.decode("utf-8", errors="ignore")
        except Exception:
            pass

        logger.info(f"请求开始：{json.dumps(log_data)}")

        try:
            # 执行请求
            response = await call_next(request)

            # 记录响应信息
            duration = time.time() - start_time
            log_data["duration_ms"] = round(duration * 1000, 2)
            log_data["status_code"] = response.status_code

            logger.info(f"请求完成：{json.dumps(log_data)}")

            return response

        except Exception as e:
            duration = time.time() - start_time
            log_data["duration_ms"] = round(duration * 1000, 2)
            log_data["error"] = str(e)

            logger.error(f"请求失败：{json.dumps(log_data)}")
            raise


def setup_logging() -> None:
    """配置日志系统。"""
    log_format = settings.LOG_FORMAT
    log_level = getattr(logging, settings.LOG_LEVEL)

    # 配置根日志记录器
    logging.basicConfig(
        level=log_level,
        format=log_format,
    )

    # 配置应用日志
    lingzhu_logger = logging.getLogger("lingzhu")
    lingzhu_logger.setLevel(log_level)

    # 配置第三方库日志级别
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

    logger.info(f"日志系统已初始化，级别：{settings.LOG_LEVEL}")
