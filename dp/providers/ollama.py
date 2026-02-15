from __future__ import annotations

import httpx

from dp.providers.base import LLMProvider, ProviderError


class OllamaProvider(LLMProvider):
    name = "ollama"

    def __init__(self, base_url: str = "http://localhost:11434", timeout_s: float = 120.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s

    @staticmethod
    def _build_prompt(messages: list[dict[str, str]]) -> str:
        prompt_parts: list[str] = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt_parts.append(f"{role.upper()}: {content}")
        return "\n\n".join(prompt_parts)

    async def _list_models(self, client: httpx.AsyncClient) -> list[str]:
        response = await client.get(f"{self.base_url}/api/tags")
        response.raise_for_status()
        data = response.json()
        models = data.get("models", [])
        names = [m.get("name", "") for m in models if isinstance(m, dict)]
        return [name for name in names if isinstance(name, str) and name.strip()]

    async def generate(self, messages: list[dict[str, str]], model: str) -> str:
        prompt = self._build_prompt(messages)
        try:
            async with httpx.AsyncClient(timeout=self.timeout_s) as client:
                try:
                    response = await client.post(
                        f"{self.base_url}/api/generate",
                        json={"model": model, "prompt": prompt, "stream": False},
                    )
                    response.raise_for_status()
                    data = response.json()
                except httpx.HTTPStatusError as exc:
                    detail = ""
                    try:
                        detail = exc.response.json().get("error", "")
                    except ValueError:
                        detail = exc.response.text

                    is_missing_model = exc.response.status_code == 404 and "not found" in detail.lower()
                    if not is_missing_model:
                        raise ProviderError(
                            f"Ollama request failed ({exc.response.status_code}): {detail or str(exc)}"
                        ) from exc

                    available_models = await self._list_models(client)
                    if not available_models:
                        raise ProviderError(
                            "Ollama is running but no local models are installed. "
                            "Run: ollama pull llama3.1:8b (or any model), then retry."
                        ) from exc

                    fallback_model = available_models[0]
                    fallback_response = await client.post(
                        f"{self.base_url}/api/generate",
                        json={"model": fallback_model, "prompt": prompt, "stream": False},
                    )
                    fallback_response.raise_for_status()
                    data = fallback_response.json()
        except httpx.HTTPError as exc:
            raise ProviderError(f"Ollama request failed: {exc}") from exc

        text = data.get("response")
        if not isinstance(text, str):
            raise ProviderError("Ollama response format was invalid")
        return text.strip()


async def is_ollama_available(base_url: str = "http://localhost:11434") -> bool:
    try:
        async with httpx.AsyncClient(timeout=1.0) as client:
            response = await client.get(f"{base_url.rstrip('/')}/api/tags")
            return response.status_code == 200
    except httpx.HTTPError:
        return False
