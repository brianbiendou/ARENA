"""API routes for application settings."""

from __future__ import annotations

from fastapi import APIRouter, Request

from ..config import load_settings, save_settings
from ..models.settings import AppSettings

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=AppSettings)
async def get_settings():
    """Return current settings."""
    return load_settings()


@router.put("", response_model=AppSettings)
async def update_settings(settings: AppSettings, request: Request):
    """Update and persist settings, then refresh providers."""
    save_settings(settings)
    registry = request.app.state.registry
    registry.refresh(settings)
    return settings
