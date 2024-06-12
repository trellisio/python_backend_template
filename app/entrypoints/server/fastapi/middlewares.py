import json
import time
from typing import Any, Awaitable, Callable, Literal

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.logger import logger

CallNext = Callable[[Request], Awaitable[Response]]


def register_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(AddProcessTimeHeader)
    app.add_middleware(AddRequestLogger)


class AddProcessTimeHeader(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: CallNext):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(round(process_time, 5))
        return response


class AddRequestLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: CallNext):
        try:
            response = await call_next(request)
        except Exception as e:
            body = await request.body()
            payload = {
                "body": body.decode("utf-8"),
                "headers": dict(request.headers),
                "params": dict(request.query_params),
                "method": request.method,
                "url": str(request.url),
                "error": str(e),
            }
            logger.opt(ansi=True).error(f"<red>{json.dumps(payload, indent=4)}</red>")
            raise e

        logger.opt(ansi=True).info(
            f"[{request.method}] {request.url} {response.status_code} - {response.headers["X-Process-Time"]}"
        )
        return response
