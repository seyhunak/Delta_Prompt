from __future__ import annotations

import os

import httpx

from dp.providers.base import LLMProvider, ProviderError


class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self, api_key: str | None = None, timeout_s: float = 60.0) -> None:
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.timeout_s = timeout_s
        if not self.api_key:
            raise ProviderError("ANTHROPIC_API_KEY is not set")

    async def generate(self, messages: list[dict[str, str]], model: str) -> str:
        system = ""
        anthropic_messages: list[dict[str, str]] = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                system = content
            elif role in {"user", "assistant"}:
                anthropic_messages.append({"role": role, "content": content})

        payload = {
            "model": model,
            "max_tokens": 2048,
            "temperature": 0.2,
            "system": system,
            "messages": anthropic_messages,
        }
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout_s) as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            raise ProviderError(f"Anthropic request failed: {exc}") from exc

        try:
            blocks = data["content"]
            text = "".join(block.get("text", "") for block in blocks if block.get("type") == "text")
            return text.strip()
        except (KeyError, TypeError, AttributeError) as exc:
            raise ProviderError("Anthropic response format was invalid") from exc
