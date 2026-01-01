"""
Utility functions for working with MCP tools in LangChain agents.
"""

from mcps.client import get_mcp_client, get_default_mcp_client, get_mcp_client_with_memory
from typing import List
import logging
import asyncio
import os
import sys
import concurrent.futures
from contextlib import contextmanager

logger = logging.getLogger(__name__)


@contextmanager
def suppress_output():
    """Context manager to suppress stdout and stderr temporarily."""
    # Save original stdout/stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr

    try:
        # Redirect to devnull
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        yield
    finally:
        # Restore original stdout/stderr
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = old_stdout
        sys.stderr = old_stderr


def _make_tool_sync_compatible(tool):
    """
    Wrap an async-only MCP tool to support both sync and async invocation.

    LangChain's StructuredTool requires a _run method for sync calls,
    but MCP tools only have _arun (async). This wrapper adds sync support
    by running the async function in a new thread with its own event loop.

    This addresses the NotImplementedError('StructuredTool does not support sync invocation.')
    """
    from langchain_core.tools import StructuredTool, Tool
    import concurrent.futures
    import inspect

    # Check if it's a StructuredTool without sync support
    if isinstance(tool, StructuredTool):
        # Store original async method and metadata
        original_arun = tool._arun
        tool_name = tool.name
        tool_description = tool.description
        tool_args_schema = tool.args_schema

        # Create a sync wrapper that runs the async function
        def sync_wrapper(*args, config=None, **kwargs):
            """Synchronous wrapper for async tool - runs in thread with new event loop."""

            def run_async():
                """Helper to run async function in new event loop."""
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    # Pass config as keyword-only argument if provided
                    if config is not None:
                        return new_loop.run_until_complete(
                            original_arun(*args, config=config, **kwargs)
                        )
                    else:
                        return new_loop.run_until_complete(
                            original_arun(*args, **kwargs)
                        )
                finally:
                    new_loop.close()

            # Run in thread to avoid event loop conflicts
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(run_async)
                return future.result(timeout=120)  # 2 minute timeout

        # Create async wrapper to preserve async functionality
        async def async_wrapper(*args, config=None, **kwargs):
            """Async wrapper that calls original async function."""
            # Pass config as keyword-only argument if provided
            if config is not None:
                return await original_arun(*args, config=config, **kwargs)
            else:
                return await original_arun(*args, **kwargs)

        # Method 1: Try to patch the existing tool
        try:
            # Set both sync and async methods
            tool.func = sync_wrapper
            tool._run = sync_wrapper
            tool._arun = async_wrapper

            # Force the tool to recognize sync support
            if hasattr(tool, "coroutine"):
                tool.coroutine = None

            logger.debug(f"Patched tool '{tool_name}' with sync wrapper")
            return tool

        except Exception as e:
            # Method 2: If patching fails, create a new StructuredTool
            logger.warning(
                f"Failed to patch tool '{tool_name}': {e}. Creating new tool."
            )

            try:
                # Create a new StructuredTool with both sync and async support
                new_tool = StructuredTool(
                    name=tool_name,
                    description=tool_description,
                    func=sync_wrapper,
                    coroutine=async_wrapper,
                    args_schema=tool_args_schema,
                )
                logger.debug(f"Created new sync-compatible tool '{tool_name}'")
                return new_tool
            except Exception as e2:
                # Method 3: Fallback to basic Tool class
                logger.warning(
                    f"Failed to create StructuredTool for '{tool_name}': {e2}. Using basic Tool."
                )

                new_tool = Tool(
                    name=tool_name,
                    description=tool_description or "MCP tool",
                    func=sync_wrapper,
                )
                return new_tool

    return tool


async def _get_mcp_tools_async(include_memory: bool = False) -> List:
    """
    Async helper to get MCP tools from the configured MCP client.

    Args:
        include_memory: If True, loads memory MCP server (slower)

    Returns:
        List: A list of LangChain tools from the MCP client
    """
    with suppress_output():
        if include_memory:
            mcp_client = get_mcp_client_with_memory()
        else:
            mcp_client = get_default_mcp_client()
        tools = await mcp_client.get_tools()
    return tools


async def _get_mcp_tools_with_timeout(timeout: int, include_memory: bool = False) -> List:
    """Helper to load MCP tools with a timeout."""
    return await asyncio.wait_for(
        _get_mcp_tools_async(include_memory=include_memory), timeout=timeout
    )


def get_mcp_tools(timeout: int = 30, silent: bool = False, include_memory: bool = False) -> List:
    """
    Get MCP tools from the configured MCP client.

    Args:
        timeout: Timeout in seconds for loading MCP tools (default: 30)
        silent: If True, suppress all output (default: False)
        include_memory: If True, includes memory MCP server for persistent memory (slower)

    Returns:
        List: A list of LangChain tools from the MCP client
    """
    try:
        if not silent:
            memory_note = " (with memory)" if include_memory else ""
            print(f"Loading MCP tools{memory_note} (timeout: {timeout}s)...")
        tools = asyncio.run(_get_mcp_tools_with_timeout(timeout, include_memory=include_memory))

        if not silent:
            print(f"[OK] Loaded {len(tools)} MCP tools, making them sync-compatible...")

        # Make all tools sync-compatible
        sync_tools = []
        for i, tool in enumerate(tools):
            try:
                sync_tool = _make_tool_sync_compatible(tool)
                sync_tools.append(sync_tool)
                logger.debug(
                    f"Tool {i+1}/{len(tools)}: '{sync_tool.name}' - sync-compatible"
                )
            except Exception as e:
                logger.error(f"Failed to make tool {i+1} sync-compatible: {e}")
                if not silent:
                    print(f"[WARNING] Skipping tool {i+1} due to error: {e}")
                # Skip this tool rather than failing completely
                continue

        logger.info(
            f"Successfully loaded {len(sync_tools)} MCP tools (sync-compatible)"
        )
        if not silent:
            print(f"[OK] {len(sync_tools)} MCP tools ready (sync-compatible)")
            if len(sync_tools) < len(tools):
                print(
                    f"[WARNING] {len(tools) - len(sync_tools)} tools skipped due to errors"
                )

        return sync_tools
    except asyncio.TimeoutError:
        logger.warning(f"MCP tool loading timed out after {timeout}s")
        if not silent:
            print(
                f"[WARNING] MCP tool loading timed out after {timeout}s - continuing without MCP tools"
            )
        return []
    except Exception as e:
        logger.error(f"Failed to load MCP tools: {e}", exc_info=True)
        if not silent:
            print(
                f"[WARNING] Failed to load MCP tools: {str(e)[:100]} - continuing without MCP tools"
            )
        return []


async def _get_mcp_tools_by_server_async(server_name: str) -> List:
    """
    Async helper to get MCP tools from a specific server.

    Args:
        server_name: Name of the MCP server

    Returns:
        List: A list of LangChain tools from the specified MCP server
    """
    mcp_client = get_mcp_client()
    tools = await mcp_client.get_tools()

    # Filter tools by server name if the tool has server metadata
    server_tools = [
        tool
        for tool in tools
        if hasattr(tool, "metadata") and tool.metadata.get("server") == server_name  # type: ignore
    ]

    if not server_tools:
        # If no server metadata, return all tools (user can filter manually)
        logger.warning(f"No server metadata found, returning all {len(tools)} tools")
        return tools

    return server_tools


def get_mcp_tools_by_server(server_name: str, silent: bool = False) -> List:
    """
    Get MCP tools from a specific server.

    Args:
        server_name: Name of the MCP server (e.g., 'sequentialthinking', 'arxiv-latex-mcp')
        silent: If True, suppress all output (default: False)

    Returns:
        List: A list of LangChain tools from the specified MCP server
    """
    try:
        if not silent:
            print(f"Loading tools from MCP server '{server_name}'...")

        server_tools = asyncio.run(_get_mcp_tools_by_server_async(server_name))

        # Make all tools sync-compatible
        sync_tools = []
        for i, tool in enumerate(server_tools):
            try:
                sync_tool = _make_tool_sync_compatible(tool)
                sync_tools.append(sync_tool)
                logger.debug(
                    f"Tool {i+1}/{len(server_tools)}: '{sync_tool.name}' - sync-compatible"
                )
            except Exception as e:
                logger.error(
                    f"Failed to make tool {i+1} from {server_name} sync-compatible: {e}"
                )
                if not silent:
                    print(f"[WARNING] Skipping tool {i+1} due to error: {e}")
                continue

        logger.info(
            f"Successfully loaded {len(sync_tools)} tools from {server_name} (sync-compatible)"
        )
        if not silent:
            print(f"[OK] {len(sync_tools)} tools from '{server_name}' ready")
            if len(sync_tools) < len(server_tools):
                print(
                    f"[WARNING] {len(server_tools) - len(sync_tools)} tools skipped due to errors"
                )

        return sync_tools
    except Exception as e:
        logger.error(f"Failed to load MCP tools from {server_name}: {e}", exc_info=True)
        if not silent:
            print(f"[WARNING] Failed to load tools from '{server_name}': {e}")
        return []
