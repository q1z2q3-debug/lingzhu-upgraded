"""
全局异常处理器

统一处理所有异常，返回标准化的错误响应。
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
import logging
import traceback

from lingzhu.config.settings import settings

logger = logging.getLogger("lingzhu.exceptions")


class APIException(HTTPException):
    """自定义 API 异常基类。"""
    def __init__(
        self,
        status_code: int = 500,
        message: str = "Internal Server Error",
        error_code: str = "INTERNAL_ERROR",
        details: dict = None
    ):
        super().__init__(status_code=status_code, detail=message)
        self.error_code = error_code
        self.details = details or {}


class NotFoundException(APIException):
    """资源未找到异常。"""
    def __init__(self, resource: str = "Resource", identifier: str = ""):
        msg = f"{resource} {identifier} 不存在" if identifier else f"{resource} 不存在"
        super().__init__(
            status_code=404,
            message=msg,
            error_code="NOT_FOUND"
        )


class ConflictException(APIException):
    """资源冲突异常。"""
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            status_code=409,
            message=message,
            error_code="CONFLICT"
        )


class UnauthorizedException(APIException):
    """未授权异常。"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            status_code=401,
            message=message,
            error_code="UNAUTHORIZED"
        )


class BadRequestException(APIException):
    """请求错误异常。"""
    def __init__(self, message: str = "Bad Request"):
        super().__init__(
            status_code=400,
            message=message,
            error_code="BAD_REQUEST"
        )


def register_exception_handlers(app: FastAPI) -> None:
    """注册异常处理器。"""

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """处理 HTTP 异常。"""
        logger.warning(
            f"HTTP {exc.status_code}: {exc.detail} | Path: {request.url.path}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": getattr(exc, "error_code", "HTTP_ERROR"),
                    "message": exc.detail,
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "path": request.url.path,
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """处理请求验证异常。"""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"],
                "type": error["type"],
            })

        logger.warning(f"验证错误：{errors} | Path: {request.url.path}")
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "请求参数验证失败",
                    "details": errors,
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "path": request.url.path,
            }
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        """处理数据库异常。"""
        logger.error(f"数据库错误：{str(exc)} | Path: {request.url.path}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "DATABASE_ERROR",
                    "message": "数据库操作失败",
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "path": request.url.path,
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """处理所有未捕获的异常。"""
        logger.error(
            f"未捕获异常：{str(exc)}\n{traceback.format_exc()} | Path: {request.url.path}"
        )
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "内部服务器错误" if settings.ENVIRONMENT == "production" else str(exc),
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "path": request.url.path,
            }
        )

    logger.info("异常处理器已注册")
