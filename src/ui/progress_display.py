"""
Enhanced Progress Display System for NAMI CLI

Inspired by Claude Code's approach to showing real-time progress:
- Status line with current operation
- Elapsed time tracking
- Phase indicators with spinners
- Agent activity with tool calls
- Token usage (when available)
"""

import sys
import time
import threading
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


# ANSI Escape Codes
class ANSI:
    """ANSI escape codes for terminal control"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"

    # Cursor
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    CURSOR_UP = "\033[{}A"
    CLEAR_LINE = "\033[2K"
    CLEAR_TO_END = "\033[K"

    # Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def _safe_print(text: str) -> None:
    """Print text safely, handling Unicode encoding issues on Windows."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fall back to ASCII-safe version
        ascii_text = text.encode("ascii", errors="replace").decode("ascii")
        print(ascii_text)


class PhaseStatus(Enum):
    """Status of a research phase"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class ToolCall:
    """Represents a tool call made by an agent"""
    tool_name: str
    status: str  # "running", "complete", "error"
    start_time: float
    end_time: Optional[float] = None
    result_preview: Optional[str] = None


@dataclass
class AgentActivity:
    """Tracks an agent's current activity"""
    name: str
    role: str
    status: str  # "idle", "thinking", "tool_call", "complete", "error"
    current_action: str = ""
    tool_calls: List[ToolCall] = field(default_factory=list)
    start_time: Optional[float] = None
    tokens_used: int = 0


@dataclass
class ResearchPhase:
    """Represents a phase in the research process"""
    name: str
    description: str
    status: PhaseStatus = PhaseStatus.PENDING
    agents: List[str] = field(default_factory=list)
    start_time: Optional[float] = None
    end_time: Optional[float] = None


class ProgressDisplay:
    """
    Real-time progress display for research operations.

    Features:
    - Status line with spinner
    - Phase tracking
    - Agent activity with tool calls
    - Elapsed time display
    - Token usage tracking
    """

    # Spinner frames (Claude Code style)
    SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    # Alternative braille spinner
    BRAILLE_SPINNER = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]

    # Dots spinner
    DOTS_SPINNER = ["⠋", "⠙", "⠚", "⠞", "⠖", "⠦", "⠴", "⠲", "⠳", "⠓"]

    def __init__(self):
        self._lock = threading.Lock()
        self._active = False
        self._spinner_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        # State
        self._phases: List[ResearchPhase] = []
        self._current_phase: Optional[ResearchPhase] = None
        self._agents: Dict[str, AgentActivity] = {}
        self._start_time: Optional[float] = None
        self._spinner_idx = 0
        self._status_message = ""
        self._sub_message = ""

        # Display options
        self._show_tool_calls = True
        self._show_tokens = True
        self._compact_mode = False
        self._lines_rendered = 0

    def start(self, topic: str, strategy: str) -> None:
        """Start the progress display for a research session"""
        with self._lock:
            if self._active:
                return

            self._active = True
            self._start_time = time.time()
            self._status_message = f"Researching: {topic[:50]}..."
            self._sub_message = f"Strategy: {strategy}"

            # Start spinner thread
            self._stop_event.clear()
            self._spinner_thread = threading.Thread(target=self._spinner_loop, daemon=True)
            self._spinner_thread.start()

    def stop(self, success: bool = True) -> None:
        """Stop the progress display"""
        with self._lock:
            if not self._active:
                return

            self._active = False
            self._stop_event.set()

        if self._spinner_thread:
            self._spinner_thread.join(timeout=0.5)

        # Print final status
        self._print_completion(success)

    def set_phase(self, name: str, description: str, agents: List[str] = None) -> None:
        """Set the current research phase"""
        with self._lock:
            # Complete previous phase
            if self._current_phase and self._current_phase.status == PhaseStatus.RUNNING:
                self._current_phase.status = PhaseStatus.COMPLETE
                self._current_phase.end_time = time.time()

            # Create new phase
            phase = ResearchPhase(
                name=name,
                description=description,
                status=PhaseStatus.RUNNING,
                agents=agents or [],
                start_time=time.time()
            )
            self._phases.append(phase)
            self._current_phase = phase
            self._status_message = f"{name}: {description}"

    def complete_phase(self, success: bool = True) -> None:
        """Mark the current phase as complete"""
        with self._lock:
            if self._current_phase:
                self._current_phase.status = PhaseStatus.COMPLETE if success else PhaseStatus.ERROR
                self._current_phase.end_time = time.time()

    def register_agent(self, name: str, role: str) -> None:
        """Register an agent for tracking"""
        with self._lock:
            self._agents[name] = AgentActivity(
                name=name,
                role=role,
                status="idle"
            )

    def agent_start(self, agent_name: str, action: str = "Processing") -> None:
        """Mark an agent as active"""
        with self._lock:
            if agent_name in self._agents:
                agent = self._agents[agent_name]
                agent.status = "thinking"
                agent.current_action = action
                agent.start_time = time.time()
            else:
                # Auto-register
                self._agents[agent_name] = AgentActivity(
                    name=agent_name,
                    role="Agent",
                    status="thinking",
                    current_action=action,
                    start_time=time.time()
                )

    def agent_tool_call(self, agent_name: str, tool_name: str) -> None:
        """Record a tool call by an agent"""
        with self._lock:
            if agent_name in self._agents:
                agent = self._agents[agent_name]
                agent.status = "tool_call"
                agent.current_action = f"Calling {tool_name}"
                agent.tool_calls.append(ToolCall(
                    tool_name=tool_name,
                    status="running",
                    start_time=time.time()
                ))
                self._sub_message = f"-> {tool_name}"

    def agent_tool_complete(self, agent_name: str, tool_name: str, preview: str = None) -> None:
        """Mark a tool call as complete"""
        with self._lock:
            if agent_name in self._agents:
                agent = self._agents[agent_name]
                for tool in reversed(agent.tool_calls):
                    if tool.tool_name == tool_name and tool.status == "running":
                        tool.status = "complete"
                        tool.end_time = time.time()
                        tool.result_preview = preview
                        break
                agent.status = "thinking"
                agent.current_action = "Processing results"

    def agent_complete(self, agent_name: str, result: str = "") -> None:
        """Mark an agent as complete"""
        with self._lock:
            if agent_name in self._agents:
                agent = self._agents[agent_name]
                agent.status = "complete"
                agent.current_action = result or "Complete"

    def agent_error(self, agent_name: str, error: str) -> None:
        """Mark an agent as errored"""
        with self._lock:
            if agent_name in self._agents:
                agent = self._agents[agent_name]
                agent.status = "error"
                agent.current_action = error

    def update_status(self, message: str, sub_message: str = "") -> None:
        """Update the status message"""
        with self._lock:
            self._status_message = message
            if sub_message:
                self._sub_message = sub_message

    def update_tokens(self, agent_name: str, tokens: int) -> None:
        """Update token count for an agent"""
        with self._lock:
            if agent_name in self._agents:
                self._agents[agent_name].tokens_used += tokens

    def _spinner_loop(self) -> None:
        """Background thread for spinner animation"""
        while not self._stop_event.is_set():
            with self._lock:
                if self._active:
                    self._render_status_line()
            self._stop_event.wait(0.1)

    def _render_status_line(self) -> None:
        """Render the current status line"""
        try:
            # Calculate elapsed time
            elapsed = time.time() - self._start_time if self._start_time else 0
            elapsed_str = self._format_elapsed(elapsed)

            # Get spinner frame
            frame = self.SPINNER_FRAMES[self._spinner_idx % len(self.SPINNER_FRAMES)]
            self._spinner_idx += 1

            # Build status line
            status_color = ANSI.BRIGHT_CYAN

            # Main status line
            line = (
                f"\r{ANSI.CLEAR_LINE}"
                f"{status_color}{frame}{ANSI.RESET} "
                f"{ANSI.BOLD}{self._status_message}{ANSI.RESET}"
            )

            # Add elapsed time
            line += f" {ANSI.DIM}({elapsed_str}){ANSI.RESET}"

            # Add sub-message if present
            if self._sub_message:
                line += f" {ANSI.DIM}{self._sub_message}{ANSI.RESET}"

            sys.stdout.write(line)
            sys.stdout.flush()

        except Exception:
            pass  # Ignore errors in display

    def _format_elapsed(self, seconds: float) -> str:
        """Format elapsed time"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            mins = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{mins}m {secs}s"
        else:
            hours = int(seconds // 3600)
            mins = int((seconds % 3600) // 60)
            return f"{hours}h {mins}m"

    def _print_completion(self, success: bool) -> None:
        """Print final completion status"""
        elapsed = time.time() - self._start_time if self._start_time else 0
        elapsed_str = self._format_elapsed(elapsed)

        # Clear current line
        sys.stdout.write(f"\r{ANSI.CLEAR_LINE}")

        if success:
            icon = f"{ANSI.BRIGHT_GREEN}[OK]{ANSI.RESET}"
            status = f"{ANSI.BRIGHT_GREEN}Complete{ANSI.RESET}"
        else:
            icon = f"{ANSI.BRIGHT_RED}[X]{ANSI.RESET}"
            status = f"{ANSI.BRIGHT_RED}Failed{ANSI.RESET}"

        # Print summary
        _safe_print(f"{icon} Research {status} {ANSI.DIM}({elapsed_str}){ANSI.RESET}")

        # Print phase summary if phases were tracked
        if self._phases:
            _safe_print(f"\n{ANSI.BRIGHT_WHITE}Phases:{ANSI.RESET}")
            for phase in self._phases:
                phase_icon = self._get_phase_icon(phase.status)
                phase_time = ""
                if phase.start_time and phase.end_time:
                    phase_duration = phase.end_time - phase.start_time
                    phase_time = f" {ANSI.DIM}({self._format_elapsed(phase_duration)}){ANSI.RESET}"
                _safe_print(f"  {phase_icon} {phase.name}{phase_time}")

        # Print agent summary
        if self._agents:
            total_tools = sum(len(a.tool_calls) for a in self._agents.values())
            total_tokens = sum(a.tokens_used for a in self._agents.values())

            _safe_print(f"\n{ANSI.BRIGHT_WHITE}Summary:{ANSI.RESET}")
            _safe_print(f"  {ANSI.DIM}Agents used:{ANSI.RESET} {len(self._agents)}")
            _safe_print(f"  {ANSI.DIM}Tool calls:{ANSI.RESET} {total_tools}")
            if total_tokens > 0:
                _safe_print(f"  {ANSI.DIM}Tokens used:{ANSI.RESET} {total_tokens:,}")

        print()

    def _get_phase_icon(self, status: PhaseStatus) -> str:
        """Get icon for phase status (using ASCII-safe characters)"""
        icons = {
            PhaseStatus.PENDING: f"{ANSI.DIM}o{ANSI.RESET}",
            PhaseStatus.RUNNING: f"{ANSI.BRIGHT_CYAN}*{ANSI.RESET}",
            PhaseStatus.COMPLETE: f"{ANSI.BRIGHT_GREEN}+{ANSI.RESET}",
            PhaseStatus.ERROR: f"{ANSI.BRIGHT_RED}x{ANSI.RESET}",
            PhaseStatus.SKIPPED: f"{ANSI.DIM}-{ANSI.RESET}",
        }
        return icons.get(status, "o")

    def print_activity_log(self, message: str, level: str = "info") -> None:
        """Print an activity log message below the status line"""
        with self._lock:
            # Move to new line and print message
            icons = {
                "info": f"{ANSI.BRIGHT_CYAN}*{ANSI.RESET}",
                "success": f"{ANSI.BRIGHT_GREEN}[OK]{ANSI.RESET}",
                "warning": f"{ANSI.BRIGHT_YELLOW}[!]{ANSI.RESET}",
                "error": f"{ANSI.BRIGHT_RED}[X]{ANSI.RESET}",
                "tool": f"{ANSI.BRIGHT_MAGENTA}->{ANSI.RESET}",
            }
            icon = icons.get(level, "*")

            # Clear line and print
            sys.stdout.write(f"\r{ANSI.CLEAR_LINE}")
            _safe_print(f"  {icon} {message}")

            # Re-render status line
            if self._active:
                self._render_status_line()


# Global instance
_progress: Optional[ProgressDisplay] = None
_progress_lock = threading.Lock()


def get_progress() -> ProgressDisplay:
    """Get or create the global progress display"""
    global _progress
    with _progress_lock:
        if _progress is None:
            _progress = ProgressDisplay()
        return _progress


def reset_progress() -> None:
    """Reset the global progress display"""
    global _progress
    with _progress_lock:
        if _progress:
            _progress.stop()
        _progress = ProgressDisplay()


# Convenience functions for common operations
def start_progress(topic: str, strategy: str) -> None:
    """Start progress tracking"""
    get_progress().start(topic, strategy)


def stop_progress(success: bool = True) -> None:
    """Stop progress tracking"""
    get_progress().stop(success)


def set_phase(name: str, description: str, agents: List[str] = None) -> None:
    """Set current phase"""
    get_progress().set_phase(name, description, agents)


def complete_phase(success: bool = True) -> None:
    """Complete current phase"""
    get_progress().complete_phase(success)


def agent_start(name: str, action: str = "Processing") -> None:
    """Mark agent as started"""
    get_progress().agent_start(name, action)


def agent_tool(name: str, tool: str) -> None:
    """Record tool call"""
    get_progress().agent_tool_call(name, tool)


def agent_complete(name: str, result: str = "") -> None:
    """Mark agent as complete"""
    get_progress().agent_complete(name, result)


def update_status(message: str, sub_message: str = "") -> None:
    """Update status message"""
    get_progress().update_status(message, sub_message)


def log_activity(message: str, level: str = "info") -> None:
    """Log an activity message"""
    get_progress().print_activity_log(message, level)
