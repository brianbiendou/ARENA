"""Abstract base class for LLM providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator


@dataclass
class LLMResponse:
    content: str
    tokens_used: int
    response_time_ms: int
    model: str
    raw: dict | None = None


@dataclass
class ModelInfo:
    id: str
    name: str
    provider: str
    context_length: int | None = None
    cost_input: float | None = None
    cost_output: float | None = None


class BaseLLMProvider(ABC):
    """Interface that all LLM providers must implement."""

    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 800,
        timeout_s: int = 60,
    ) -> LLMResponse:
        """Generate a completion from the model."""
        ...

    @abstractmethod
    async def stream(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 800,
        timeout_s: int = 60,
    ) -> AsyncIterator[str]:
        """Stream a completion token by token."""
        ...

    @abstractmethod
    async def list_models(self) -> list[ModelInfo]:
        """Return available models from this provider."""
        ...

    @abstractmethod
    async def test_connection(self) -> bool:
        """Test if the provider is reachable."""
        ...
