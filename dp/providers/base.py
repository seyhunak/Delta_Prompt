from __future__ import annotations

from abc import ABC, abstractmethod


class ProviderError(RuntimeError):
    pass


class LLMProvider(ABC):
    name: str

    @abstractmethod
    async def generate(self, messages: list[dict[str, str]], model: str) -> str:
        raise NotImplementedError
