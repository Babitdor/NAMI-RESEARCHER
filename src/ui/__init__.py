"""
NAMI UI Package

CLI branding, output management, and progress display components.
"""

from src.ui.output_manager import console, OutputManager
from src.ui.cli_branding import Colors, print_banner, print_footer
from src.ui.spinner import Spinner, run_with_spinner
from src.ui.agent_activity import AgentActivityTracker, get_tracker
from src.ui.progress_display import (
    ProgressDisplay,
    get_progress,
    reset_progress,
    start_progress,
    stop_progress,
    set_phase,
    complete_phase,
    agent_start,
    agent_tool,
    agent_complete,
    update_status,
    log_activity,
)

__all__ = [
    # Output manager
    "console",
    "OutputManager",
    # Branding
    "Colors",
    "print_banner",
    "print_footer",
    # Spinner
    "Spinner",
    "run_with_spinner",
    # Agent activity
    "AgentActivityTracker",
    "get_tracker",
    # Progress display
    "ProgressDisplay",
    "get_progress",
    "reset_progress",
    "start_progress",
    "stop_progress",
    "set_phase",
    "complete_phase",
    "agent_start",
    "agent_tool",
    "agent_complete",
    "update_status",
    "log_activity",
]
