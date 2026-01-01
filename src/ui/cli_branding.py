"""
CLI Branding and Visual Identity for NAMI

This module provides ASCII art, banners, and visual branding elements
for the NAMI Multi-Agent Research System.
"""

from typing import Optional
import sys


# Color codes for terminal output
class Colors:
    """ANSI color codes for terminal styling"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

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

    # Background colors
    BG_BLACK = "\033[40m"
    BG_YELLOW = "\033[43m"
    BG_CYAN = "\033[46m"


# NAMI ASCII Art with Bee
NAMI_BANNER = f"""{Colors.BRIGHT_YELLOW}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║    ███╗   ██╗ █████╗ ███╗   ███╗██╗          )))                          ║
║    ████╗  ██║██╔══██╗████╗ ████║██║         (o o)                         ║
║    ██╔██╗ ██║███████║██╔████╔██║██║     ooO--(_)--Ooo                     ║
║    ██║╚██╗██║██╔══██║██║╚██╔╝██║██║         Bee                           ║
║    ██║ ╚████║██║  ██║██║ ╚═╝ ██║██║                                       ║
║    ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝                                       ║
║                                                                           ║
║           {Colors.BRIGHT_CYAN}Multi-Agent Research Intelligence System{Colors.BRIGHT_YELLOW}                        ║
║                   {Colors.BRIGHT_WHITE}Powered by LangGraph & Ollama{Colors.BRIGHT_YELLOW}                           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""

NAMI_BANNER_SIMPLE = f"""{Colors.BRIGHT_YELLOW}
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│    ███╗   ██╗ █████╗ ███╗   ███╗██╗          )))                          │
│    ████╗  ██║██╔══██╗████╗ ████║██║         (o o)                         │
│    ██╔██╗ ██║███████║██╔████╔██║██║     ooO--(_)--Ooo                     │
│    ██║╚██╗██║██╔══██║██║╚██╔╝██║██║         Bee                           │
│    ██║ ╚████║██║  ██║██║ ╚═╝ ██║██║                                       │
│    ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝                                       │
│                                                                           │
│           {Colors.BRIGHT_CYAN}Multi-Agent Research Intelligence System{Colors.BRIGHT_YELLOW}                        │
│                   {Colors.BRIGHT_WHITE}Powered by LangGraph & Ollama{Colors.BRIGHT_YELLOW}                           │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
{Colors.RESET}"""

# Minimal ASCII fallback (for terminals with limited Unicode support)
NAMI_BANNER_ASCII = """
===============================================================================

    N   N   AAA   M   M  III          )))
    NN  N  A   A  MM MM   I          (o o)
    N N N  AAAAA  M M M   I      ooO--(_)--Ooo
    N  NN  A   A  M   M   I          Bee
    N   N  A   A  M   M  III

           Multi-Agent Research Intelligence System
                   Powered by LangGraph & Ollama

===============================================================================
"""

# Agent team info
AGENT_TEAM = f"""{Colors.BRIGHT_CYAN}
╭───────────────────────── Agent Team ──────────────────────────╮
│                                                                │
│  {Colors.BRIGHT_YELLOW}🐺 Pochi{Colors.BRIGHT_CYAN}      - Supervisor (Orchestrator)                 │
│  {Colors.BRIGHT_YELLOW}🐶 Pookie{Colors.BRIGHT_CYAN}     - Researcher (Information Gatherer)         │
│  {Colors.BRIGHT_YELLOW}🦊 Pooch{Colors.BRIGHT_CYAN}      - Analyst (Critical Thinker)               │
│  {Colors.BRIGHT_YELLOW}🐯 Buddy{Colors.BRIGHT_CYAN}      - Writer (Report Composer)                 │
│  {Colors.BRIGHT_YELLOW}⚖️  Judge{Colors.BRIGHT_CYAN}      - Critic (Quality Assessor)                │
│                                                                │
╰────────────────────────────────────────────────────────────────╯
{Colors.RESET}"""

AGENT_TEAM_SIMPLE = """
┌───────────────────────── Agent Team ──────────────────────────┐
│                                                                │
│  🐺 Pochi      - Supervisor (Orchestrator)                    │
│  🐶 Pookie     - Researcher (Information Gatherer)            │
│  🦊 Pooch      - Analyst (Critical Thinker)                   │
│  🐯 Buddy      - Writer (Report Composer)                     │
│  ⚖️  Judge      - Critic (Quality Assessor)                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
"""


def print_banner(style: str = "fancy") -> None:
    """
    Print the NAMI banner.

    Args:
        style: Banner style - "fancy", "simple", or "ascii"
    """
    try:
        if style == "fancy":
            print(NAMI_BANNER)
        elif style == "simple":
            print(NAMI_BANNER_SIMPLE)
        else:
            print(NAMI_BANNER_ASCII)
    except UnicodeEncodeError:
        # Fallback to ASCII for terminals that don't support Unicode
        print(NAMI_BANNER_ASCII)


def print_agent_team(style: str = "fancy", num_agents: int = 3) -> None:
    """
    Print the agent team information with configurable research agents.

    Args:
        style: Display style - "fancy", "simple", or "minimal"
        num_agents: Number of parallel research agents to display (default 3)
    """
    # Strategy names mapping (from graph.py logic)
    strategies = ["comprehensive", "technical", "practical", "critical", "future"]

    try:
        if style == "fancy" or style == "simple":
            # Build dynamic agent list
            print("\n┌───────────────────────── Agent Team ──────────────────────────┐")
            print("│                                                                │")

            # Show N research agents with strategies
            for i in range(1, num_agents + 1):
                strategy = strategies[(i - 1) % len(strategies)]
                strategy_display = strategy.replace("_", " ").title()
                agent_line = f"│  🐶 Researcher-{i}  - Research Agent (Strategy: {strategy_display})"
                padding = 64 - len(agent_line)
                print(f"{agent_line}{' ' * padding}│")

            # Show Writer and Critic (no Analyst, no Supervisor)
            print("│  🐯 Buddy       - Writer (Report Composer)                     │")
            print("│  ⚖️  Judge       - Critic (Quality Assessor)                    │")
            print("│                                                                │")
            print("└────────────────────────────────────────────────────────────────┘\n")
        else:
            # Minimal style
            print("\n=== Agent Team ===")
            for i in range(1, num_agents + 1):
                strategy = strategies[(i - 1) % len(strategies)]
                print(f"Researcher-{i} ({strategy})")
            print("Buddy (Writer) | Judge (Critic)\n")
    except UnicodeEncodeError:
        # Fallback for Unicode errors
        print("\n=== Agent Team ===")
        for i in range(1, num_agents + 1):
            strategy = strategies[(i - 1) % len(strategies)]
            print(f"Researcher-{i} ({strategy})")
        print("Buddy (Writer) | Judge (Critic)\n")


def print_welcome(persona_mode: bool = False) -> None:
    """
    Print welcome message with system information.

    Args:
        persona_mode: Whether persona mode is enabled
    """
    mode_text = "PERSONA MODE" if persona_mode else "STANDARD MODE"
    mode_color = Colors.BRIGHT_MAGENTA if persona_mode else Colors.BRIGHT_GREEN

    try:
        print(f"\n{mode_color}╭{'─' * 60}╮{Colors.RESET}")
        print(f"{mode_color}│{Colors.RESET}  System Mode: {mode_color}{mode_text:<46}{Colors.RESET}{mode_color}│{Colors.RESET}")
        print(f"{mode_color}│{Colors.RESET}  Status: {Colors.BRIGHT_GREEN}Ready{Colors.RESET}{' ' * 49}{mode_color}│{Colors.RESET}")
        print(f"{mode_color}╰{'─' * 60}╯{Colors.RESET}\n")
    except UnicodeEncodeError:
        print(f"\n{'=' * 62}")
        print(f"  System Mode: {mode_text}")
        print(f"  Status: Ready")
        print(f"{'=' * 62}\n")


def print_startup_info() -> None:
    """Print startup information and tips."""
    try:
        print(f"\n{Colors.BRIGHT_WHITE}{'-' * 75}{Colors.RESET}")
        print(f"{Colors.BRIGHT_CYAN}Tips:{Colors.RESET}")
        print(f"  {Colors.BRIGHT_WHITE}-{Colors.RESET} Ask research questions for comprehensive reports")
        print(f"  {Colors.BRIGHT_WHITE}-{Colors.RESET} Request code generation for technical implementations")
        print(f"  {Colors.BRIGHT_WHITE}-{Colors.RESET} Enable PERSONA_MODE in .env for enhanced workflows")
        print(f"  {Colors.BRIGHT_WHITE}-{Colors.RESET} Reports are auto-saved to knowledge base for future use")
        print(f"{Colors.BRIGHT_WHITE}{'-' * 75}{Colors.RESET}\n")
    except UnicodeEncodeError:
        print("\n" + "=" * 75)
        print("Tips:")
        print("  - Ask research questions for comprehensive reports")
        print("  - Request code generation for technical implementations")
        print("  - Enable PERSONA_MODE in .env for enhanced workflows")
        print("  - Reports are auto-saved to knowledge base for future use")
        print("=" * 75 + "\n")


def print_footer() -> None:
    """Print footer/goodbye message."""
    try:
        print(f"\n{Colors.BRIGHT_YELLOW}")
        print("╭───────────────────────────────────────────────────────────────────────────╮")
        print("│                                                                           │")
        print(f"│        {Colors.BRIGHT_WHITE}Thank you for using NAMI!{Colors.BRIGHT_YELLOW}                                      │")
        print(f"│        {Colors.BRIGHT_CYAN}Your research has been completed successfully.{Colors.BRIGHT_YELLOW}                │")
        print("│                                                                           │")
        print("╰───────────────────────────────────────────────────────────────────────────╯")
        print(Colors.RESET)
    except UnicodeEncodeError:
        print("\n" + "=" * 75)
        print("     Thank you for using NAMI!")
        print("     Your research has been completed successfully.")
        print("=" * 75 + "\n")


def get_input_prompt(persona_mode: bool = False) -> str:
    """
    Get formatted input prompt.

    Args:
        persona_mode: Whether persona mode is enabled

    Returns:
        Formatted prompt string
    """
    try:
        if persona_mode:
            return f"\n{Colors.BRIGHT_MAGENTA}🐺 NAMI >{Colors.RESET} "
        else:
            return f"\n{Colors.BRIGHT_YELLOW}🐺 NAMI >{Colors.RESET} "
    except UnicodeEncodeError:
        return "\nNAMI > "
