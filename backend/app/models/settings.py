"""Pydantic models for settings and provider configuration."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ProviderType(str, Enum):
    OLLAMA = "ollama"
    LM_STUDIO = "lm_studio"
    OPENROUTER = "openrouter"


class FallbackStrategy(str, Enum):
    IGNORE = "ignore"
    REPLACE = "replace"
    STOP = "stop"


class ProviderConfig(BaseModel):
    type: ProviderType
    enabled: bool = True
    endpoint: str = ""
    api_key: Optional[str] = None
    connected: bool = False


class OllamaConfig(ProviderConfig):
    type: ProviderType = ProviderType.OLLAMA
    endpoint: str = "http://localhost:11434"


class LMStudioConfig(ProviderConfig):
    type: ProviderType = ProviderType.LM_STUDIO
    endpoint: str = "http://localhost:1234"


class OpenRouterConfig(ProviderConfig):
    type: ProviderType = ProviderType.OPENROUTER
    endpoint: str = "https://openrouter.ai/api/v1"
    api_key: Optional[str] = None


class LLMDefaults(BaseModel):
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    top_p: float = Field(0.9, ge=0.0, le=1.0)
    max_tokens: int = Field(800, ge=100, le=4096)
    response_timeout_s: int = Field(60, ge=10, le=300)


class BatchConfig(BaseModel):
    pause_between_runs_ms: int = Field(2000, ge=0, le=30000)
    max_concurrent_runs: int = Field(1, ge=1, le=5)


class AppSettings(BaseModel):
    providers: dict[ProviderType, ProviderConfig] = Field(default_factory=lambda: {
        ProviderType.OLLAMA: OllamaConfig(),
        ProviderType.LM_STUDIO: LMStudioConfig(),
        ProviderType.OPENROUTER: OpenRouterConfig(),
    })
    llm_defaults: LLMDefaults = Field(default_factory=LLMDefaults)
    batch: BatchConfig = Field(default_factory=BatchConfig)
    fallback_strategy: FallbackStrategy = FallbackStrategy.STOP
    debug_logging: bool = False
    data_dir: str = "data"
