from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

_mcp_toolset: McpToolset = None


def load_mcp_servers(path: str | Path) -> Dict[str, Dict[str, Any]]:
    """
    Load MCP server definitions from YAML config file.
    Expected format:

    mcpServers:
      name:
        type: sse | ws
        url: https://...
    """
    path = Path(path)
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return data.get("mcpServers", {})


def get_mcp_toolset() -> McpToolset:
    """Process-wide singleton for local mcp-wikidata server (stdio)."""
    global _mcp_toolset
    if _mcp_toolset is None:
        _mcp_toolset = McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uv",
                    args=["run", "mcp-wikidata"],
                    cwd="/home/pavelk/dev/mcp-wikidata",
                ),
                timeout=30,
            )
        )
    return _mcp_toolset


def get_mcp_tools() -> list[McpToolset]:
    """Convenience: return all MCP tools for use in Agent(..., tools=...)."""
    return [get_mcp_toolset()]
