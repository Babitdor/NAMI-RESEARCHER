from langchain_mcp_adapters.client import MultiServerMCPClient
import os
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def get_mcp_client(
    include_memory: bool = False, include_markdown_pdf: bool = False
) -> Any:
    """Returns configured MCP client instance with optional lazy loading.

    Args:
        include_memory: If True, includes memory MCP server (slower, use selectively)
        include_markdown_pdf: If True, includes markdown PDF MCP server

    Returns:
        MultiServerMCPClient with selected servers enabled
    """
    servers: Dict[str, Any] = {
        "sequentialthinking": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
        },
        "arxiv-latex-mcp": {
            "transport": "stdio",
            "command": "uv",
            "args": [
                "--directory",
                "B:/Winter 2025 Projects/Proj-2 - Multi-Agent/mcps/arxiv-latex-mcp",
                "run",
                "server/main.py",
            ],
        },
    }

    # Add optional servers only when specifically requested
    if include_memory:
        servers["memory"] = {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-memory"],
            "env": {"MEMORY_FILE_PATH": os.path.join(os.getcwd(), "memory.jsonl")},
        }
        logger.info("Memory MCP server enabled")

    if include_markdown_pdf:
        servers["markdown-pdf"] = {
            "transport": "stdio",
            "command": "npx",
            "args": ["md-mermaid-to-pdf-mcp"],
        }
        logger.info("Markdown PDF MCP server enabled")

    return MultiServerMCPClient(servers)  # type: ignore


# Default client without memory (fast loading)
def get_default_mcp_client() -> Any:
    """Get default MCP client without memory server (fast)."""
    return get_mcp_client(include_memory=False)


# Client with memory (slower but with persistent memory)
def get_mcp_client_with_memory() -> Any:
    """Get MCP client with memory server enabled (slower but with memory persistence)."""
    return get_mcp_client(include_memory=True)
