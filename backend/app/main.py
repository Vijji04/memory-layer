import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.capture import router as capture_router
from app.api.retrieve import router as retrieve_router
from app.config import settings
from app.services.storage import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Agentic Memory Layer",
    description="Memory capture, classification, and retrieval for AI agents",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print(f"ERROR: {exc}\n{tb}")
    error_type = type(exc).__name__
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "type": error_type},
    )


app.include_router(capture_router, prefix="/api")
app.include_router(retrieve_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
