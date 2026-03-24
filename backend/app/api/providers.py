"""API routes for LLM providers."""

from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Request

from ..models.settings import ProviderType

router = APIRouter(prefix="/providers", tags=["providers"])


def _get_registry(request: Request):
    return request.app.state.registry


@router.get("")
async def list_providers(request: Request):
    """List all providers and their status."""
    registry = _get_registry(request)
    result = []
    for ptype in ProviderType:
        provider = registry.get(ptype)
        result.append({
            "type": ptype.value,
            "available": provider is not None,
        })
    return result


@router.get("/{provider_type}/models")
async def list_models(provider_type: ProviderType, request: Request):
    """List available models for a provider."""
    registry = _get_registry(request)
    provider = registry.get(provider_type)
    if provider is None:
        raise HTTPException(404, f"Provider {provider_type.value} not available")
    models = await provider.list_models()
    return [asdict(m) for m in models]


@router.post("/{provider_type}/test")
async def test_provider(provider_type: ProviderType, request: Request):
    """Test connection to a provider."""
    registry = _get_registry(request)
    provider = registry.get(provider_type)
    if provider is None:
        raise HTTPException(404, f"Provider {provider_type.value} not configured")
    ok = await provider.test_connection()
    return {"type": provider_type.value, "connected": ok}
