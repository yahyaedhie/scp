"""SCP Router v3.2 — Token Meter

Counts tokens and estimates savings from SCP compression.
Uses tiktoken (cl100k_base) as an approximation for Claude token counts.
Note: Claude's tokenizer differs from OpenAI's; for exact counts use
the Anthropic SDK client.messages.count_tokens() instead.
"""

import tiktoken
from functools import lru_cache
from app.config import settings


@lru_cache(maxsize=1)
def _encoder():
    return tiktoken.get_encoding(settings.token_model)


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken encoding."""
    if not text:
        return 0
    return len(_encoder().encode(text))


def estimate_savings(original_text: str, compressed_text: str) -> dict:
    original_tokens = count_tokens(original_text)
    compressed_tokens = count_tokens(compressed_text)
    saved = original_tokens - compressed_tokens
    pct = (saved / original_tokens * 100) if original_tokens > 0 else 0
    return {
        "original_tokens": original_tokens,
        "compressed_tokens": compressed_tokens,
        "tokens_saved": saved,
        "savings_percent": round(pct, 1),
    }


def estimate_expansion_cost(code: str, expansion: str) -> dict:
    code_tokens = count_tokens(code)
    expansion_tokens = count_tokens(expansion)
    return {
        "code": code,
        "code_tokens": code_tokens,
        "expansion_tokens": expansion_tokens,
        "saved_per_mention": expansion_tokens - code_tokens,
    }


def estimate_session_savings(
    turns: int,
    codes_per_turn: int = 3,
    avg_expansion_tokens: int = 12,
    avg_code_tokens: int = 3,
) -> dict:
    total_saved = 0
    for turn in range(1, turns + 1):
        total_mentions = codes_per_turn + codes_per_turn * (turn - 1)
        total_saved += total_mentions * (avg_expansion_tokens - avg_code_tokens)

    total_without = sum(
        (codes_per_turn * t) * avg_expansion_tokens for t in range(1, turns + 1)
    )
    total_with = total_without - total_saved
    pct = (total_saved / total_without * 100) if total_without > 0 else 0

    return {
        "turns": turns,
        "total_tokens_without_scp": total_without,
        "total_tokens_with_scp": total_with,
        "total_tokens_saved": total_saved,
        "savings_percent": round(pct, 1),
    }
