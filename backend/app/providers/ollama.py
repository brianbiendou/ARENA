"""Ollama LLM provider (local)."""

from __future__ import annotations

import time
from typing import AsyncIterator

import httpx

from .base import BaseLLMProvider, LLMResponse, ModelInfo


class OllamaProvider(BaseLLMProvider):

    def __init__(self, endpoint: str = "http://localhost:11434"):
        self.endpoint = endpoint.rstrip("/")

    async def generate(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 800,
        timeout_s: int = 60,
    ) -> LLMResponse:
        start = time.perf_counter_ns()
        async with httpx.AsyncClient(timeout=timeout_s) as client:
            resp = await client.post(
                f"{self.endpoint}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "top_p": top_p,
                        "num_predict": max_tokens,
                    },
                },
            )
            resp.raise_for_status()
            data = resp.json()

        elapsed_ms = (time.perf_counter_ns() - start) // 1_000_000
        content = data.get("message", {}).get("content", "")
        tokens = data.get("eval_count", 0) + data.get("prompt_eval_count", 0)

        return LLMResponse(
            content=content,
            tokens_used=tokens,
            response_time_ms=elapsed_ms,
            model=model,
            raw=data,
        )

    async def stream(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 800,
        timeout_s: int = 60,
    ) -> AsyncIterator[str]:
        async with httpx.AsyncClient(timeout=timeout_s) as client:
            async with client.stream(
                "POST",
                f"{self.endpoint}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": True,
                    "options": {
                        "temperature": temperature,
                        "top_p": top_p,
                        "num_predict": max_tokens,
                    },
                },
            ) as resp:
                resp.raise_for_status()
                import json as _json
                async for line in resp.aiter_lines():
                    if line.strip():
                        chunk = _json.loads(line)
                        token = chunk.get("message", {}).get("content", "")
                        if token:
                            yield token
                        if chunk.get("done"):
                            break

    async def list_models(self) -> list[ModelInfo]:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{self.endpoint}/api/tags")
            resp.raise_for_status()
            data = resp.json()

        models = []
        for m in data.get("models", []):
            models.append(ModelInfo(
                id=m["name"],
                name=m["name"],
                provider="ollama",
                context_length=None,
            ))
        return models

    async def test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.endpoint}/api/tags")
                return resp.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False
