from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def register_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def base_error_handler(_: Request, e: Exception):
        return JSONResponse(
            status_code=500, content=jsonable_encoder({"error": e.message})
        )
