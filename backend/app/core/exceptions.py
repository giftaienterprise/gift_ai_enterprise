from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class BusinessException(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code


async def business_exception_handler(
    request: Request,
    exc: BusinessException,
):
    return JSONResponse(
        status_code=exc.code,
        content={
            "code": exc.code,
            "message": exc.message,
            "data": None,
        },
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": "参数校验失败",
            "data": exc.errors(),
        },
    )