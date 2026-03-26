"""SCP Router v3.2 — Prompt Compressor

Reduces T2 anchor pack verbosity based on compression mode.
Operates on the string output of build_system_prompt().

Modes:
  light    — no change; full T1+T2 sent as-is
  moderate — strip domain_profile and hash/stability lines from T2
  deep     — strip T2 entirely; send T1 (rules + codes list) only
  adaptive — auto-select based on token count:
               < 500 tokens → light
               500–800 tokens → moderate
               > 800 tokens → deep
"""

import re
from app.core.meter import count_tokens

_T2_SEPARATOR = "# ANCHOR PACK"

# Lines in each anchor block to strip for moderate compression
_STRIP_PATTERNS = [
    re.compile(r'^\s+domain_profile:.*$', re.MULTILINE),
    re.compile(r'^\s+hash:.*\|\s*stability:.*$', re.MULTILINE),
]

_ADAPTIVE_MODERATE_THRESHOLD = 500
_ADAPTIVE_DEEP_THRESHOLD = 800


def compress_prompt(system_prompt: str, mode: str) -> str:
    """Apply compression to a system prompt string.

    Args:
        system_prompt: Full T1+T2 prompt from build_system_prompt().
        mode: One of "light", "moderate", "deep", "adaptive".

    Returns:
        Compressed prompt string.
    """
    if mode == "light":
        return system_prompt

    if mode == "adaptive":
        tokens = count_tokens(system_prompt)
        if tokens < _ADAPTIVE_MODERATE_THRESHOLD:
            return system_prompt
        elif tokens < _ADAPTIVE_DEEP_THRESHOLD:
            mode = "moderate"
        else:
            mode = "deep"

    if mode == "deep":
        # Keep T1 only — strip everything from the ANCHOR PACK separator onward
        idx = system_prompt.find(_T2_SEPARATOR)
        if idx != -1:
            return system_prompt[:idx].rstrip()
        return system_prompt

    if mode == "moderate":
        # Strip domain_profile and hash/stability lines from T2 blocks
        compressed = system_prompt
        for pattern in _STRIP_PATTERNS:
            compressed = pattern.sub("", compressed)
        # Collapse runs of blank lines left behind by stripping
        compressed = re.sub(r'\n{3,}', '\n\n', compressed)
        return compressed.strip()

    # Unknown mode — return unchanged
    return system_prompt
