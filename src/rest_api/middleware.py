import time
from typing import Any

from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import Message

from src.configuration import logger
from .app import app

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)


async def set_body(request: Request, body: bytes) -> None:
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


@app.middleware("http")
async def log_request_body(request: Request, call_next: Any) -> Response:
    start_time = time.time()
    logger.debug(f"Request headers: `{dict(request.headers)}`")

    request_body = await request.body()
    logger.debug(f"Request body: `{request_body.decode()}`")

    await set_body(request, request_body)
    response = await call_next(request)

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    logger.debug(f"Response text: `{response_body.decode()}`")

    end_time = time.time()
    processing_time = end_time - start_time
    logger.info(f"Processing time: {processing_time:.4f} seconds")

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type,
    )
