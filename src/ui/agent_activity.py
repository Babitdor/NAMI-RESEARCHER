"""
Professional Agent Activity Tracker for NAMI Research System

Provides live visual feedback during agent execution with:
- Agent status indicators
- Activity tracking
- Progress visualization
- Clean, professional formatting
"""

import sys
import time
from typing import Optional, List, Dict
from src.ui.cli_branding import Colors


class AgentActivityTracker:
    """Tracks and displays agent activities in real-time"""

    def __init__(self):
        self.current_phase = None
        self.current_agent = None
        self.activities = []
        self.start_time = None

    def start_research(self, topic: str, strategy: str):
        """Initialize research tracking"""
        self.start_time = time.time()
        self.activities = []
        print(f"\n{Colors.BRIGHT_CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}║{Colors.RESET} {Colors.BRIGHT_WHITE}Research Session Started{Colors.RESET}                                                    {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")

    def set_phase(self, phase_name: str, description: str = ""):
        """Update current research phase"""
        self.current_phase = phase_name

        print(f"\n{Colors.BRIGHT_YELLOW}┌─ Phase: {phase_name}{Colors.RESET}")
        if description:
            print(f"{Colors.DIM}│  {description}{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}└{'─' * (len(phase_name) + 9)}{Colors.RESET}\n")

    def agent_start(self, agent_name: str, task: str = ""):
        """Mark agent as started"""
        self.current_agent = agent_name

        # Format agent name
        agent_display = agent_name.replace("_", " ").title()

        self._safe_print(f"{Colors.BRIGHT_CYAN}  > {agent_display}{Colors.RESET}", end="")
        if task:
            self._safe_print(f" {Colors.DIM}- {task}{Colors.RESET}")
        else:
            print()

        sys.stdout.flush()

    def _safe_print(self, text: str, end: str = "\n"):
        """Print text safely, handling Unicode encoding issues."""
        try:
            print(text, end=end)
        except UnicodeEncodeError:
            ascii_text = text.encode("ascii", errors="replace").decode("ascii")
            print(ascii_text, end=end)

    def agent_activity(self, activity: str, level: str = "info"):
        """Log agent activity"""
        # Choose symbol and color based on level (ASCII-safe)
        if level == "success":
            symbol = "[OK]"
            color = Colors.BRIGHT_GREEN
        elif level == "warning":
            symbol = "[!]"
            color = Colors.BRIGHT_YELLOW
        elif level == "error":
            symbol = "[X]"
            color = Colors.BRIGHT_RED
        elif level == "info":
            symbol = "*"
            color = Colors.BRIGHT_CYAN
        else:
            symbol = "-"
            color = Colors.DIM

        self._safe_print(f"{Colors.DIM}    {color}{symbol}{Colors.RESET} {Colors.DIM}{activity}{Colors.RESET}")
        sys.stdout.flush()

    def agent_complete(self, agent_name: str, result: str = ""):
        """Mark agent as completed"""
        agent_display = agent_name.replace("_", " ").title()

        self._safe_print(f"{Colors.BRIGHT_GREEN}  [OK] {agent_display}{Colors.RESET}", end="")
        if result:
            self._safe_print(f" {Colors.DIM}- {result}{Colors.RESET}")
        else:
            self._safe_print(f" {Colors.DIM}- Complete{Colors.RESET}")

        print()  # Add spacing
        sys.stdout.flush()

    def agent_error(self, agent_name: str, error: str):
        """Mark agent as errored"""
        agent_display = agent_name.replace("_", " ").title()

        self._safe_print(f"{Colors.BRIGHT_RED}  [X] {agent_display}{Colors.RESET}")
        self._safe_print(f"{Colors.DIM}    Error: {error}{Colors.RESET}\n")
        sys.stdout.flush()

    def show_progress(self, current: int, total: int, label: str = ""):
        """Show progress bar"""
        if total == 0:
            return

        percentage = int((current / total) * 100)
        filled = int((current / total) * 40)
        empty = 40 - filled

        bar = f"{Colors.BRIGHT_CYAN}{'█' * filled}{Colors.DIM}{'░' * empty}{Colors.RESET}"

        if label:
            print(f"\r  {label}: [{bar}] {percentage}%", end="")
        else:
            print(f"\r  Progress: [{bar}] {percentage}%", end="")

        if current == total:
            print()  # New line when complete

        sys.stdout.flush()

    def complete_research(self):
        """Mark research as complete"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)

            time_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"

            self._safe_print(f"\n{Colors.BRIGHT_GREEN}+{'=' * 75}+{Colors.RESET}")
            self._safe_print(f"{Colors.BRIGHT_GREEN}|{Colors.RESET} {Colors.BRIGHT_WHITE}Research Complete{Colors.RESET} {Colors.DIM}- Time: {time_str}{Colors.RESET}                                        {Colors.BRIGHT_GREEN}|{Colors.RESET}")
            self._safe_print(f"{Colors.BRIGHT_GREEN}+{'=' * 75}+{Colors.RESET}\n")

    def show_summary(self, agents_used: List[str], iterations: int = 0):
        """Show research summary"""
        print(f"{Colors.BRIGHT_WHITE}Research Summary:{Colors.RESET}")
        print(f"  {Colors.BRIGHT_CYAN}Agents Deployed:{Colors.RESET} {len(agents_used)}")

        if agents_used:
            print(f"  {Colors.DIM}├─ {', '.join([a.replace('_', ' ').title() for a in agents_used[:3]])}{Colors.RESET}")
            if len(agents_used) > 3:
                print(f"  {Colors.DIM}└─ +{len(agents_used) - 3} more...{Colors.RESET}")

        if iterations > 0:
            print(f"  {Colors.BRIGHT_CYAN}Iterations:{Colors.RESET} {iterations}")

        print()


# Global tracker instance
_tracker = None


def get_tracker() -> AgentActivityTracker:
    """Get global agent activity tracker"""
    global _tracker
    if _tracker is None:
        _tracker = AgentActivityTracker()
    return _tracker


def reset_tracker():
    """Reset the global tracker"""
    global _tracker
    _tracker = AgentActivityTracker()


# Convenience functions
def start_research(topic: str, strategy: str):
    """Start tracking research"""
    get_tracker().start_research(topic, strategy)


def set_phase(phase_name: str, description: str = ""):
    """Set current phase"""
    get_tracker().set_phase(phase_name, description)


def agent_start(agent_name: str, task: str = ""):
    """Agent started"""
    get_tracker().agent_start(agent_name, task)


def agent_activity(activity: str, level: str = "info"):
    """Log agent activity"""
    get_tracker().agent_activity(activity, level)


def agent_complete(agent_name: str, result: str = ""):
    """Agent completed"""
    get_tracker().agent_complete(agent_name, result)


def agent_error(agent_name: str, error: str):
    """Agent errored"""
    get_tracker().agent_error(agent_name, error)


def show_progress(current: int, total: int, label: str = ""):
    """Show progress"""
    get_tracker().show_progress(current, total, label)


def complete_research():
    """Research complete"""
    get_tracker().complete_research()


def show_summary(agents_used: List[str], iterations: int = 0):
    """Show summary"""
    get_tracker().show_summary(agents_used, iterations)
