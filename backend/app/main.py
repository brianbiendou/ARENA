"""ARENA — FastAPI application entry point."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import experiments, providers, runs, settings
from .api.ws import router as ws_router, ws_manager
from .config import load_settings
from .providers.registry import ProviderRegistry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(name)-20s  %(levelname)-7s  %(message)s",
)
logger = logging.getLogger("arena")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown logic."""
    logger.info("ARENA starting up …")
    app_settings = load_settings()
    registry = ProviderRegistry()
    registry.refresh(app_settings)
    app.state.registry = registry
    app.state.ws_manager = ws_manager
    logger.info("Providers ready: %s", [p.value for p in registry.available])
    yield
    logger.info("ARENA shutting down.")


app = FastAPI(
    title="ARENA",
    description="Multi-agent AI experimental platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow the React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(experiments.router, prefix="/api")
app.include_router(providers.router, prefix="/api")
app.include_router(runs.router, prefix="/api")
app.include_router(settings.router, prefix="/api")
app.include_router(ws_router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "arena"}
