from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import yaml
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, SseConnectionParams
from loguru import logger
from mcp import StdioServerParameters

_mcp_toolsets: list[McpToolset] | None = None


def load_mcp_servers(path: str | Path) -> Dict[str, Dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return data.get("mcpServers", {})


# factory
def create_toolset(cfg: Dict[str, Any]) -> McpToolset:
    t = cfg.get("type")

    raw_cwd = cfg.get("cwd")
    cwd = os.path.expandvars(raw_cwd) if isinstance(raw_cwd, str) else None

    if t == "stdio":
        return McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=cfg["command"],
                    args=cfg.get("args", []),
                    cwd=cwd,
                ),
                timeout=cfg.get("timeout", 30),
            )
        )
    elif t == "sse":
        return McpToolset(
            connection_params=SseConnectionParams(
                url=cfg["url"]
            )
        )
    else:
        raise ValueError(f"Unknown MCP server type: {t}")


def get_mcp_toolsets(config_path: str | Path) -> list[McpToolset]:
    global _mcp_toolsets
    if _mcp_toolsets is None:
        cfg = load_mcp_servers(config_path)
        logger.debug("Loaded MCP toolsets {}:", cfg)
        _mcp_toolsets = [
            create_toolset(name, server_cfg)
            for name, server_cfg in cfg.items()
        ]
    return _mcp_toolsets


def get_mcp_tools() -> list[McpToolset]:
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "config" / "mcp.yml"
    return get_mcp_toolsets(config_path)
