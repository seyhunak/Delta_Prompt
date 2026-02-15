from __future__ import annotations

import os

import httpx

from dp.providers.base import LLMProvider, ProviderError


class OpenAIProvider(LLMProvider):
    name = "openai"

    def __init__(self, api_key: str | None = None, timeout_s: float = 60.0) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.timeout_s = timeout_s
        if not self.api_key:
            raise ProviderError("OPENAI_API_KEY is not set")

    async def generate(self, messages: list[dict[str, str]], model: str) -> str:
        payload = {"model": model, "messages": messages, "temperature": 0.2}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout_s) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            raise ProviderError(f"OpenAI request failed: {exc}") from exc

        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, AttributeError, TypeError) as exc:
            raise ProviderError("OpenAI response format was invalid") from exc
