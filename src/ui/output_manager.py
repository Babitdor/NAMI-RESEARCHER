"""
Centralized Output Manager for Multi-Agent Research System

This module provides a unified interface for all terminal output in the system,
ensuring consistent formatting, proper Unicode handling, and preventing spinner conflicts.

Usage:
    from utils.output_manager import console

    console.print("Normal message")
    console.success("Success message")
    console.error("Error message")
    console.warning("Warning message")

    with console.spinner("Processing..."):
        # Work happens here
        pass
"""

import sys
import threading
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from src.ui.spinner import Spinner
from src.ui.live_display import (
    start_live_display,
    stop_live_display,
    update_agent_status,
    print_permanent_message,
)


# ANSI Color Codes
class Colors:
    """ANSI color codes for terminal styling"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


class OutputManager:
    """
    Centralized output manager for consistent terminal printing.

    Features:
    - Unicode-safe printing with automatic fallback
    - Consistent formatting across the application
    - Spinner integration with automatic cleanup
    - Thread-safe output operations
    - Prevents spinner overlap issues
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._active_spinner: Optional[Spinner] = None
        self._live_mode = False  # Track if live display is active

    def _safe_output(self, text: str) -> None:
        """
        Print text with fallback for Unicode encoding errors.
        Thread-safe and spinner-aware.
        """
        with self._lock:
            # Pause active spinner temporarily if needed
            spinner_to_resume: Optional[Spinner] = None
            spinner_text: Optional[str] = None
            if self._active_spinner:
                spinner_to_resume = self._active_spinner
                spinner_text = getattr(self._active_spinner, 'text', None)
                self._active_spinner.stop(success=True)

            try:
                print(text)
            except UnicodeEncodeError:
                # Remove emojis and special characters
                ascii_text = text.encode("ascii", errors="ignore").decode("ascii")
                print(ascii_text)

            # Resume spinner if it was active
            if spinner_to_resume is not None:
                spinner_to_resume.start()
                self._active_spinner = spinner_to_resume

    def print(self, text: str = "", prefix: str = "") -> None:
        """Print a normal message."""
        message = f"{prefix}{text}" if prefix else text
        self._safe_output(message)

    def success(self, text: str) -> None:
        """Print a success message with icon."""
        self._safe_output(f"[OK] {text}")

    def error(self, text: str) -> None:
        """Print an error message with icon."""
        self._safe_output(f"[ERROR] {text}")

    def warning(self, text: str) -> None:
        """Print a warning message with icon."""
        self._safe_output(f"[WARN] {text}")

    def info(self, text: str) -> None:
        """Print an info message with icon."""
        self._safe_output(f"[INFO] {text}")

    def debug(self, text: str) -> None:
        """Print a debug message with icon."""
        self._safe_output(f"[DEBUG] {text}")

    def separator(self, char: str = "─", length: int = 75, color: str = "") -> None:
        """Print a separator line."""
        try:
            line = f"{color}{char * length}{Colors.RESET}" if color else char * length
            self._safe_output(line)
        except UnicodeEncodeError:
            # Fallback to simple dash
            line = "-" * length
            self._safe_output(line)

    def header(self, text: str, style: str = "box") -> None:
        """
        Print a header with decorative formatting.

        Args:
            text: Header text
            style: Style type - "box", "simple", or "minimal"
        """
        try:
            if style == "box":
                width = max(len(text) + 4, 75)
                self._safe_output(f"\n{Colors.BRIGHT_CYAN}╭{'─' * (width - 2)}╮{Colors.RESET}")
                padding = (width - len(text) - 2) // 2
                self._safe_output(
                    f"{Colors.BRIGHT_CYAN}│{Colors.RESET}{' ' * padding}{Colors.BOLD}{Colors.BRIGHT_WHITE}{text}{Colors.RESET}{' ' * (width - len(text) - padding - 2)}{Colors.BRIGHT_CYAN}│{Colors.RESET}"
                )
                self._safe_output(f"{Colors.BRIGHT_CYAN}╰{'─' * (width - 2)}╯{Colors.RESET}\n")
            elif style == "simple":
                self.separator(color=Colors.BRIGHT_CYAN)
                self._safe_output(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}{text}{Colors.RESET}")
                self.separator(color=Colors.BRIGHT_CYAN)
            else:
                self._safe_output(f"\n{Colors.BOLD}{text}{Colors.RESET}\n")
        except UnicodeEncodeError:
            # Fallback to simple formatting
            self._safe_output("\n" + "=" * 75)
            self._safe_output(text)
            self._safe_output("=" * 75 + "\n")

    def phase(self, phase_name: str) -> None:
        """Print a phase indicator."""
        icons = {
            "research": "[RESEARCH]",
            "analyze": "[ANALYZE]",
            "analysis": "[ANALYZE]",
            "write": "[WRITE]",
            "writing": "[WRITE]",
            "code": "[CODE]",
            "coding": "[CODE]",
            "critique": "[CRITIQUE]",
            "validate": "[OK]",
            "supervisor": "[SUPER]",
            "system-init": "[INIT]",
        }
        icon = icons.get(phase_name.lower(), "[PHASE]")

        # Special case for system init
        if phase_name.lower() == "system-init":
            self._safe_output(f"\n{icon} System Initialization...")
        else:
            self._safe_output(f"\n{icon} Executing {phase_name.title()} Phase...")

    def agent_action(self, agent_name: str, action: str) -> None:
        """Print an agent action message."""
        icons = {
            "pookie": "🐶",
            "pooch": "🦊",
            "buddy": "🐯",
            "pochi": "🐺",
            "planko": "🔬",
            "judge": "⚖️",
        }
        icon = icons.get(agent_name.lower(), "🤖")
        self._safe_output(f"{icon} {agent_name} | {action}")

    def decision(self, decision: str, reasoning: str = "") -> None:
        """Print a supervisor decision."""
        self._safe_output(f"\n🎯 Supervisor Decision: {decision}")
        if reasoning:
            truncated = reasoning[:200] + ("..." if len(reasoning) > 200 else "")
            self._safe_output(f"   Reasoning: {truncated}")

    def metric(self, name: str, value: any, unit: str = "") -> None:
        """Print a metric with consistent formatting."""
        unit_str = f" {unit}" if unit else ""
        self._safe_output(f"   {name}: {value}{unit_str}")

    def validation(self, phase: str, status: str, details: str = "") -> None:
        """Print validation results."""
        self._safe_output(f"\n📋 {phase.title()} Validation: {status}")
        if details:
            self._safe_output(f"   {details}")

    @contextmanager
    def spinner(self, text: str, icon: str = "🦊 Agent | ", color: str = "orange"):
        """
        Context manager for spinner operations.

        Usage:
            with console.spinner("Processing..."):
                # work here
                pass
        """
        with self._lock:
            # Ensure no other spinner is active
            if self._active_spinner:
                self._active_spinner.stop(success=True)
                self._active_spinner = None

            # Start new spinner
            spinner = Spinner(text, icon=icon, color=color)
            self._active_spinner = spinner

        spinner.start()
        try:
            yield spinner
            spinner.stop(success=True)
        except Exception as e:
            spinner.stop(success=False)
            raise
        finally:
            with self._lock:
                if self._active_spinner == spinner:
                    self._active_spinner = None

    def table(self, headers: list[str], rows: list[list[str]]) -> None:
        """Print a simple ASCII table."""
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Print header
        header_line = " | ".join(
            h.ljust(w) for h, w in zip(headers, col_widths)
        )
        self._safe_output(header_line)
        self._safe_output("-" * len(header_line))

        # Print rows
        for row in rows:
            row_line = " | ".join(
                str(cell).ljust(w) for cell, w in zip(row, col_widths)
            )
            self._safe_output(row_line)

    def quality_summary(self, phase: str, confidence: float, metrics: dict) -> None:
        """Print a formatted quality summary."""
        self._safe_output(f"\n📊 {phase.title()} Quality Summary:")
        self._safe_output(f"   Confidence: {confidence:.2%}")
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                self._safe_output(f"   {key.replace('_', ' ').title()}: {value}")
            else:
                self._safe_output(f"   {key.replace('_', ' ').title()}: {value}")

    def progress_bar(
        self, current: int, total: int, prefix: str = "", suffix: str = "", length: int = 50
    ) -> None:
        """
        Print a progress bar.

        Args:
            current: Current progress value
            total: Total value
            prefix: Text before progress bar
            suffix: Text after progress bar
            length: Length of progress bar in characters
        """
        percent = current / total if total > 0 else 0
        filled = int(length * percent)
        bar = "█" * filled + "░" * (length - filled)

        try:
            output = f"\r{prefix} {Colors.BRIGHT_CYAN}[{bar}]{Colors.RESET} {percent:.1%} {suffix}"
            self._safe_output(output)
        except UnicodeEncodeError:
            # ASCII fallback
            bar_ascii = "#" * filled + "-" * (length - filled)
            output = f"\r{prefix} [{bar_ascii}] {percent:.1%} {suffix}"
            self._safe_output(output)

    def status_box(self, title: str, items: Dict[str, Any]) -> None:
        """
        Print a status box with key-value pairs.

        Args:
            title: Box title
            items: Dictionary of status items
        """
        try:
            max_key_len = max(len(str(k)) for k in items.keys()) if items else 0
            width = max(max_key_len + 30, len(title) + 4, 50)

            self._safe_output(f"\n{Colors.BRIGHT_CYAN}╭{'─' * (width - 2)}╮{Colors.RESET}")
            padding = (width - len(title) - 2) // 2
            self._safe_output(
                f"{Colors.BRIGHT_CYAN}│{Colors.RESET}{' ' * padding}{Colors.BOLD}{title}{Colors.RESET}{' ' * (width - len(title) - padding - 2)}{Colors.BRIGHT_CYAN}│{Colors.RESET}"
            )
            self._safe_output(f"{Colors.BRIGHT_CYAN}├{'─' * (width - 2)}┤{Colors.RESET}")

            for key, value in items.items():
                key_str = f"{Colors.BRIGHT_WHITE}{key}{Colors.RESET}"
                value_str = self._format_value(value)
                spacing = width - len(key) - len(str(value)) - 5
                self._safe_output(
                    f"{Colors.BRIGHT_CYAN}│{Colors.RESET} {key_str}: {value_str}{' ' * max(0, spacing)}{Colors.BRIGHT_CYAN}│{Colors.RESET}"
                )

            self._safe_output(f"{Colors.BRIGHT_CYAN}╰{'─' * (width - 2)}╯{Colors.RESET}\n")
        except (UnicodeEncodeError, Exception):
            # ASCII fallback
            self._safe_output("\n" + "=" * 50)
            self._safe_output(f"  {title}")
            self._safe_output("=" * 50)
            for key, value in items.items():
                self._safe_output(f"  {key}: {value}")
            self._safe_output("=" * 50 + "\n")

    def _format_value(self, value: Any) -> str:
        """Format a value with appropriate color."""
        if isinstance(value, bool):
            if value:
                return f"{Colors.BRIGHT_GREEN}[Yes]{Colors.RESET}"
            else:
                return f"{Colors.BRIGHT_RED}[No]{Colors.RESET}"
        elif isinstance(value, (int, float)):
            return f"{Colors.BRIGHT_YELLOW}{value}{Colors.RESET}"
        else:
            return f"{Colors.BRIGHT_WHITE}{value}{Colors.RESET}"

    def step(self, step_num: int, total_steps: int, description: str) -> None:
        """
        Print a step indicator.

        Args:
            step_num: Current step number
            total_steps: Total number of steps
            description: Step description
        """
        try:
            self._safe_output(
                f"\n{Colors.BRIGHT_CYAN}[{Colors.BRIGHT_WHITE}{step_num}{Colors.BRIGHT_CYAN}/{Colors.BRIGHT_WHITE}{total_steps}{Colors.BRIGHT_CYAN}]{Colors.RESET} {Colors.BOLD}{description}{Colors.RESET}"
            )
        except UnicodeEncodeError:
            self._safe_output(f"\n[{step_num}/{total_steps}] {description}")

    def list_items(self, items: List[str], numbered: bool = False, indent: int = 2) -> None:
        """
        Print a list of items.

        Args:
            items: List of items to print
            numbered: Whether to use numbers instead of bullets
            indent: Indentation level
        """
        indent_str = " " * indent
        for i, item in enumerate(items, 1):
            if numbered:
                self._safe_output(f"{indent_str}{Colors.BRIGHT_CYAN}{i}.{Colors.RESET} {item}")
            else:
                self._safe_output(f"{indent_str}{Colors.BRIGHT_CYAN}-{Colors.RESET} {item}")

    def start_live_display(self):
        """Start the live-updating agent status display"""
        with self._lock:
            if not self._live_mode:
                self._live_mode = True
                start_live_display()

    def stop_live_display(self):
        """Stop the live-updating agent status display"""
        with self._lock:
            if self._live_mode:
                self._live_mode = False
                stop_live_display()

    def update_agent_status(self, agent_name: str, status: str, message: str):
        """
        Update an agent's status in the live display.

        Args:
            agent_name: Agent name (Pookie, Pooch, Buddy, Pochi, Judge)
            status: "working", "complete", "error", "idle"
            message: Status message
        """
        if self._live_mode:
            update_agent_status(agent_name, status, message)
        else:
            # Fallback to regular output if live mode not active
            icons = {
                "working": "[WORK]",
                "complete": "[OK]",
                "error": "[X]",
                "idle": "[IDLE]",
            }
            icon = icons.get(status, "-")
            self.agent_action(agent_name, f"{icon} {message}")

    def print_permanent(self, text: str):
        """
        Print a permanent message.

        If live mode is active, this prints below the status panel.
        Otherwise, prints normally.
        """
        if self._live_mode:
            print_permanent_message(text)
        else:
            self._safe_output(text)


# Global singleton instance
console = OutputManager()


# Backward compatibility wrapper
def safe_print(text: str):
    """
    Legacy function for backward compatibility.
    New code should use console.print() instead.
    """
    console.print(text)
