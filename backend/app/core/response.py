from typing import Any

from fastapi.responses import JSONResponse


def success(
    data: Any = None,
    message: str = "success",
    code: int = 200,
):
    return JSONResponse(
        status_code=200,
        content={
            "code": code,
            "message": message,
            "data": data,
        },
    )


def fail(
    message: str,
    code: int = 400,
):
    return JSONResponse(
        status_code=code,
        content={
            "code": code,
            "message": message,
            "data": None,
        },
    )