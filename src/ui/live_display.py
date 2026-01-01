"""
Live Status Display System for NAMI

This module provides a live-updating terminal display where agent statuses
update in place rather than printing new lines. Creates a cleaner, more
professional output similar to modern CLI tools.
"""

import sys
import threading
import time
from typing import Dict, Optional
from dataclasses import dataclass


# ANSI escape codes
class ANSI:
    """ANSI escape codes for terminal control"""
    # Cursor movement
    CURSOR_UP = "\033[{}A"  # Move cursor up N lines
    CURSOR_DOWN = "\033[{}B"  # Move cursor down N lines
    CURSOR_SAVE = "\033[s"  # Save cursor position
    CURSOR_RESTORE = "\033[u"  # Restore cursor position
    CURSOR_HOME = "\033[H"  # Move cursor to home

    # Line manipulation
    CLEAR_LINE = "\033[2K"  # Clear entire line
    CLEAR_TO_END = "\033[K"  # Clear from cursor to end of line
    CLEAR_SCREEN = "\033[2J"  # Clear entire screen

    # Colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


@dataclass
class AgentStatus:
    """Status information for an agent"""
    name: str
    icon: str
    status: str  # "idle", "working", "complete", "error"
    message: str
    color: str


class LiveStatusDisplay:
    """
    Live-updating status display for multiple agents.

    Shows a status panel that updates in place without creating new lines.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._agents: Dict[str, AgentStatus] = {}
        self._active = False
        self._lines_written = 0
        self._last_update = 0
        self._update_interval = 0.1  # Minimum time between updates (100ms)

        # Define agent order for consistent display
        self._agent_order = ["Pookie", "Pooch", "Buddy", "Pochi", "Judge"]

    def initialize_agents(self):
        """Initialize all agents in the display"""
        agents_info = [
            ("Pookie", "🐶", "Researcher"),
            ("Pooch", "🦊", "Analyst"),
            ("Buddy", "🐯", "Writer"),
            ("Pochi", "🐺", "Supervisor"),
            ("Judge", "⚖️ ", "Critic"),
        ]

        for name, icon, role in agents_info:
            self._agents[name] = AgentStatus(
                name=name,
                icon=icon,
                status="idle",
                message=f"{role} ready",
                color=ANSI.DIM
            )

    def start_display(self):
        """Start the live display"""
        with self._lock:
            if self._active:
                return

            self._active = True
            self.initialize_agents()
            self._render_full()

    def stop_display(self):
        """Stop the live display and move cursor below it"""
        with self._lock:
            if not self._active:
                return

            self._active = False
            # Move cursor below the status panel
            sys.stdout.write("\n")
            sys.stdout.flush()

    def update_agent(self, agent_name: str, status: str, message: str):
        """
        Update an agent's status.

        Args:
            agent_name: Name of the agent (e.g., "Pookie", "Pooch")
            status: Status - "working", "complete", "error", "idle"
            message: Status message to display
        """
        with self._lock:
            if not self._active or agent_name not in self._agents:
                return

            # Throttle updates to prevent flickering
            current_time = time.time()
            if current_time - self._last_update < self._update_interval:
                # Still update the data, just don't render yet
                agent = self._agents[agent_name]
                agent.status = status
                agent.message = message
                agent.color = self._get_color_for_status(status)
                return

            # Update agent data
            agent = self._agents[agent_name]
            agent.status = status
            agent.message = message
            agent.color = self._get_color_for_status(status)

            self._last_update = current_time
            self._render_update()

    def _get_color_for_status(self, status: str) -> str:
        """Get ANSI color code for a status"""
        colors = {
            "idle": ANSI.DIM,
            "working": ANSI.BRIGHT_CYAN,
            "complete": ANSI.BRIGHT_GREEN,
            "error": ANSI.GREEN,  # Changed to green to match existing style
        }
        return colors.get(status, ANSI.WHITE)

    def _get_icon_for_status(self, status: str) -> str:
        """Get status icon (ASCII-safe)"""
        icons = {
            "idle": "[IDLE]",
            "working": "[WORK]",
            "complete": "[OK]",
            "error": "[X]",
        }
        return icons.get(status, "-")

    def _render_full(self):
        """Render the complete status panel"""
        if not self._active:
            return

        try:
            # Print header
            header = f"\n{ANSI.BRIGHT_CYAN}{'─' * 75}{ANSI.RESET}\n"
            header += f"{ANSI.BOLD}{ANSI.BRIGHT_WHITE}  AGENT STATUS{ANSI.RESET}\n"
            header += f"{ANSI.BRIGHT_CYAN}{'─' * 75}{ANSI.RESET}\n"
            sys.stdout.write(header)

            # Print each agent status
            lines = 3  # Header lines
            for agent_name in self._agent_order:
                if agent_name not in self._agents:
                    continue

                agent = self._agents[agent_name]
                status_icon = self._get_icon_for_status(agent.status)

                line = (
                    f"  {agent.icon} {ANSI.BOLD}{agent.name:<8}{ANSI.RESET} "
                    f"{agent.color}{status_icon} {agent.message[:50]}{ANSI.RESET}"
                )
                sys.stdout.write(line + "\n")
                lines += 1

            # Print footer
            footer = f"{ANSI.BRIGHT_CYAN}{'─' * 75}{ANSI.RESET}\n"
            sys.stdout.write(footer)
            lines += 1

            sys.stdout.flush()
            self._lines_written = lines

        except Exception:
            # Fallback to simple output on error
            pass

    def _render_update(self):
        """Update the status panel in place"""
        if not self._active or self._lines_written == 0:
            return

        try:
            # Move cursor up to the start of the status panel
            sys.stdout.write(ANSI.CURSOR_UP.format(self._lines_written - 4))

            # Update each agent line
            for agent_name in self._agent_order:
                if agent_name not in self._agents:
                    continue

                agent = self._agents[agent_name]
                status_icon = self._get_icon_for_status(agent.status)

                # Clear line and write updated status
                line = (
                    f"\r{ANSI.CLEAR_LINE}"
                    f"  {agent.icon} {ANSI.BOLD}{agent.name:<8}{ANSI.RESET} "
                    f"{agent.color}{status_icon} {agent.message[:50]:<50}{ANSI.RESET}\n"
                )
                sys.stdout.write(line)

            # Move cursor back down to footer
            sys.stdout.write(ANSI.CURSOR_DOWN.format(1))
            sys.stdout.flush()

        except Exception:
            # Fallback to simple output on error
            pass

    def print_permanent(self, message: str):
        """
        Print a permanent message below the status panel.

        This moves the cursor below the panel, prints the message,
        and then re-renders the panel.
        """
        with self._lock:
            if not self._active:
                print(message)
                return

            try:
                # Move to bottom of panel
                sys.stdout.write("\n")
                # Print message
                sys.stdout.write(message + "\n")
                sys.stdout.flush()

                # Re-render the panel below the message
                self._render_full()

            except Exception:
                print(message)


# Global singleton instance
_live_display: Optional[LiveStatusDisplay] = None
_display_lock = threading.Lock()


def get_live_display() -> LiveStatusDisplay:
    """Get or create the global LiveStatusDisplay instance"""
    global _live_display
    with _display_lock:
        if _live_display is None:
            _live_display = LiveStatusDisplay()
        return _live_display


def start_live_display():
    """Start the live status display"""
    display = get_live_display()
    display.start_display()


def stop_live_display():
    """Stop the live status display"""
    display = get_live_display()
    display.stop_display()


def update_agent_status(agent_name: str, status: str, message: str):
    """
    Update an agent's status in the live display.

    Args:
        agent_name: Agent name (Pookie, Pooch, Buddy, Pochi, Judge)
        status: "working", "complete", "error", "idle"
        message: Status message
    """
    display = get_live_display()
    display.update_agent(agent_name, status, message)


def print_permanent_message(message: str):
    """Print a message that stays below the live status panel"""
    display = get_live_display()
    display.print_permanent(message)
