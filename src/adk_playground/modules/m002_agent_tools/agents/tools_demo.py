from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from adk_playground.core.settings import MODEL, SAFE_BASE

# tools_demo.py — design notes for tools
# 1) Clean signatures: enforce keyword-only args with `*`; use simple types (str, int, bool, small dict/list).
#    Example: def safe_read(*, path: str, max_bytes: int = 2000) -> dict: ...
#    (Avoid *args/**kwargs and overly nested structures.)
#
# 2) Good docstring → better tool selection by the LLM: first line = what it does; then Args/Returns.
#    Example:
#    def wordcount(*, text: str) -> dict:
#        """Count words in plain text.
#        Args: text (str) – UTF-8 text.
#        Returns: {'words': int} – total word count.
#        """
#
# 3) Guardrails: whitelist (e.g., .txt/.md + SAFE_BASE), size limits, idempotence.
#    Example (schematic):
#    ALLOWED_EXTS = {".txt", ".md"}
#    def safe_read(*, path: str, max_bytes: int = 2000) -> dict:
#        if Path(path).suffix.lower() not in ALLOWED_EXTS:
#            return {"error": "disallowed_extension"}
#        data = Path(path).read_text(encoding="utf-8", errors="ignore")[:max_bytes]
#        return {"text": data}
#
# 4) Small structured returns: prefer concise dicts with clear keys → easier chaining between steps.
#    Example:
#    def extract_bullets(*, text: str, n: int = 5) -> dict:
#        return {"bullets": [f"- {line}" for line in text.splitlines()[:n]]}
#
# Prompt: "Summarize file m002_notes.md"

ALLOWED_EXTS = {".txt", ".md"}


def _resolve_safe(*, path: str) -> Path | None:
    """Resolve to absolute path inside SAFE_BASE; return None if outside."""
    p = (SAFE_BASE / path).resolve() if not os.path.isabs(path) else Path(path).resolve()
    try:
        p.relative_to(SAFE_BASE)
    except Exception:
        return None
    return p


def safe_read(tool_context: ToolContext, *, path: str, max_bytes: int = 2000) -> dict[str, Any]:
    """Read a small local text file safely.

    Args:
        path: Relative or absolute path inside SAFE_BASE. Allowed extensions: .txt, .md.
        max_bytes: Maximum number of bytes to read (content is truncated to this size).

    Returns:
        {'text': str} on success, or {'error': str} with one of:
        'path_outside_safe_base' | 'disallowed_extension' | 'not_found'.

    Notes:
        `tool_context` is injected by ADK and not provided by the LLM/tool call.
    """
    p = _resolve_safe(path=path)
    if p is None:
        return {"error": "path_outside_safe_base"}

    if p.suffix.lower() not in ALLOWED_EXTS:
        return {"error": "disallowed_extension"}

    if not p.exists() or not p.is_file():
        return {"error": "not_found"}

    data = p.read_text(encoding="utf-8", errors="ignore")[: max(0, int(max_bytes))]
    return {"text": data}


def wordcount(tool_context: ToolContext, *, text: str) -> dict[str, Any]:
    """Count words in plain text.

    Args:
        text: UTF-8 text to analyze; words are counted via whitespace splitting.

    Returns:
        {'words': int} – total word count.

    Notes:
        `tool_context` is injected by ADK.
    """
    return {"words": len(text.split())}


def extract_bullets(tool_context: ToolContext, *, text: str, n: int = 5) -> dict[str, Any]:
    """Extract up to n short bullets from text.

    Args:
        text: Source text; blank lines are ignored, lines are trimmed and clipped.
        n: Maximum number of bullets to return (>=1).

    Returns:
        {'bullets': List[str]} – list of short bullet strings.

    Notes:
        `tool_context` is injected by ADK.
    """
    n = max(1, int(n))
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    bullets: list[str] = [f"- {ln[:120]}" for ln in lines[:n]]
    return {"bullets_md": "\n".join(bullets)}


def build_agent() -> Agent:
    return Agent(
        name="tools_demo",
        model=MODEL,
        instruction=(
            "You have tools: 'safe_read', 'wordcount', 'extract_bullets'. "
            "If the user asks about a local file, first call 'safe_read(path)'. "
            "If 'text' is returned, call 'wordcount(text)' and then 'extract_bullets(text)'. "
            "Finally, return a concise answer that includes the word count and the bullets. "
            "If an 'error' is returned from a tool, explain it briefly and stop."
        ),
        tools=[safe_read, wordcount, extract_bullets],
        output_key="final_output",
    )
