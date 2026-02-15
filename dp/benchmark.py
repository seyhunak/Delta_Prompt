from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol

from dp.providers.base import LLMProvider


@dataclass
class BenchmarkResult:
    provider: str
    model: str
    latency_ms: float
    prompt_token_estimate: int
    output_token_estimate: int
    total_token_estimate: int
    output: str


class OutputScorer(Protocol):
    def score(self, reference: str, candidate: str) -> float:
        ...


class LexicalOverlapScorer:
    def score(self, reference: str, candidate: str) -> float:
        ref_tokens = {t.lower() for t in reference.split() if t.strip()}
        cand_tokens = {t.lower() for t in candidate.split() if t.strip()}
        if not ref_tokens and not cand_tokens:
            return 1.0
        if not ref_tokens:
            return 0.0
        return len(ref_tokens & cand_tokens) / max(len(ref_tokens), 1)


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


async def run_single_benchmark(
    provider_name: str,
    provider: LLMProvider,
    model: str,
    messages: list[dict[str, str]],
) -> BenchmarkResult:
    start = time.perf_counter()
    prompt_text = "\n".join(msg.get("content", "") for msg in messages)
    prompt_tokens = estimate_tokens(prompt_text)
    output = await provider.generate(messages=messages, model=model)
    output_tokens = estimate_tokens(output)
    latency_ms = (time.perf_counter() - start) * 1000

    return BenchmarkResult(
        provider=provider_name,
        model=model,
        latency_ms=latency_ms,
        prompt_token_estimate=prompt_tokens,
        output_token_estimate=output_tokens,
        total_token_estimate=prompt_tokens + output_tokens,
        output=output,
    )
