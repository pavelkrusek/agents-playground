from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams

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


def get_mcp_toolsets() -> list[McpToolset]:
    """Process-wide singleton list of MCPToolset instances (one per server)."""
    global _mcp_toolset
    if _mcp_toolset is None:
        base_dir = Path(__file__).resolve().parent.parent
        cfg_path = base_dir / "config" / "mcp.yml"
        servers = load_mcp_servers(cfg_path)

        toolsets: list[McpToolset] = []
        for name, cfg in servers.items():
            url = cfg["url"]
            toolsets.append(
                McpToolset(
                    connection_params=SseServerParams(url=url)
                )
            )
        _mcp_toolset = toolsets
    return _mcp_toolset


def get_mcp_tools():
    """Convenience: return all MCP tools for use in Agent(..., tools=...)."""
    return list(get_mcp_toolsets())
