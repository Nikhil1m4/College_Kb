"""FastAPI application entry point.

Vercel detects this file automatically because it defines an ``app`` variable
and lives at ``api/index.py``, one of the supported entrypoints.
"""
import asyncio
import os
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from api.core.settings import get_settings
from api.routers.auth import router as auth_router

app = FastAPI(title="College KB API", version="0.1.0")

app.include_router(auth_router)



@app.get("/api/health")
def health() -> dict[str, str]:
    """Return service health and current environment."""
    settings = get_settings()
    region = os.environ.get("VERCEL_REGION", "local")
    return {"status": "ok", "env": settings.app_env, "region": region}


@app.get("/api/stream-test")
async def stream_test() -> StreamingResponse:
    """Throwaway SSE endpoint to verify streaming works on Vercel.

    Yields 5 chunks, one per second.
    """

    async def _generate() -> AsyncGenerator[str, None]:
        for i in range(1, 6):
            yield f"data: chunk {i}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(_generate(), media_type="text/event-stream")
