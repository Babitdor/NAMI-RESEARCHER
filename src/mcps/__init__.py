"""
MCP (Model Context Protocol) integration for the multi-agent system.
"""

from mcps.client import (
    get_mcp_client,
    get_mcp_client_with_memory,
    get_default_mcp_client,
)
from mcps.mcp_tools import get_mcp_tools, get_mcp_tools_by_server

__all__ = ["get_mcp_client", "get_mcp_tools", "get_mcp_tools_by_server"]
