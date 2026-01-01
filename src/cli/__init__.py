"""
NAMI CLI Package

Provides enhanced command-line interface functionality.
"""

from src.cli.commands import (
    registry,
    execute_command,
    history,
    cmd_history,
    CommandInfo,
    CommandRegistry,
    ResearchHistory,
    CommandHistory,
)

__all__ = [
    "registry",
    "execute_command",
    "history",
    "cmd_history",
    "CommandInfo",
    "CommandRegistry",
    "ResearchHistory",
    "CommandHistory",
]
