"""Provider registry — instantiate and cache LLM providers."""

from __future__ import annotations

from ..models.settings import AppSettings, ProviderType
from .base import BaseLLMProvider
from .lm_studio import LMStudioProvider
from .ollama import OllamaProvider
from .openrouter import OpenRouterProvider


class ProviderRegistry:
    """Manages provider instances based on app settings."""

    def __init__(self):
        self._providers: dict[ProviderType, BaseLLMProvider] = {}

    def refresh(self, settings: AppSettings) -> None:
        """Rebuild provider instances from current settings."""
        self._providers.clear()
        for ptype, cfg in settings.providers.items():
            if not cfg.enabled:
                continue
            if ptype == ProviderType.OLLAMA:
                self._providers[ptype] = OllamaProvider(endpoint=cfg.endpoint)
            elif ptype == ProviderType.LM_STUDIO:
                self._providers[ptype] = LMStudioProvider(endpoint=cfg.endpoint)
            elif ptype == ProviderType.OPENROUTER:
                if cfg.api_key:
                    self._providers[ptype] = OpenRouterProvider(
                        api_key=cfg.api_key, endpoint=cfg.endpoint,
                    )

    def get(self, provider_type: ProviderType) -> BaseLLMProvider | None:
        return self._providers.get(provider_type)

    def get_for_model(self, model: str, provider_type: ProviderType) -> BaseLLMProvider:
        provider = self.get(provider_type)
        if provider is None:
            raise ValueError(f"Provider {provider_type.value} is not configured or disabled")
        return provider

    @property
    def available(self) -> list[ProviderType]:
        return list(self._providers.keys())
