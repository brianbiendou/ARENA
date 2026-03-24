"""LM Studio LLM provider (local, OpenAI-compatible API)."""

from __future__ import annotations

import time
from typing import AsyncIterator

import httpx

from .base import BaseLLMProvider, LLMResponse, ModelInfo


class LMStudioProvider(BaseLLMProvider):

    def __init__(self, endpoint: str = "http://localhost:1234"):
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
                f"{self.endpoint}/v1/chat/completions",
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_tokens": max_tokens,
                    "stream": False,
                },
            )
            resp.raise_for_status()
            data = resp.json()

        elapsed_ms = (time.perf_counter_ns() - start) // 1_000_000
        choice = data.get("choices", [{}])[0]
        content = choice.get("message", {}).get("content", "")
        usage = data.get("usage", {})
        tokens = usage.get("total_tokens", 0)

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
        import json as _json

        async with httpx.AsyncClient(timeout=timeout_s) as client:
            async with client.stream(
                "POST",
                f"{self.endpoint}/v1/chat/completions",
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_tokens": max_tokens,
                    "stream": True,
                },
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    line = line.strip()
                    if not line or not line.startswith("data: "):
                        continue
                    payload = line[6:]
                    if payload == "[DONE]":
                        break
                    chunk = _json.loads(payload)
                    delta = chunk.get("choices", [{}])[0].get("delta", {})
                    token = delta.get("content", "")
                    if token:
                        yield token

    async def list_models(self) -> list[ModelInfo]:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{self.endpoint}/v1/models")
            resp.raise_for_status()
            data = resp.json()

        models = []
        for m in data.get("data", []):
            models.append(ModelInfo(
                id=m["id"],
                name=m.get("id", "unknown"),
                provider="lm_studio",
            ))
        return models

    async def test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.endpoint}/v1/models")
                return resp.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException):
            return False
