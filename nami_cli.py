#!/usr/bin/env python
"""
NAMI CLI - Interactive Command Line Interface for Multi-Agent Research System

An interactive REPL-style interface inspired by Claude Code with:
- Enhanced slash commands with detailed help
- Research history persistence
- Real-time progress display
- Tab completion
"""

import sys
import os
import re
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import click

# Regex to strip ANSI escape codes from user input
ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def sanitize_input(text: str) -> str:
    """Remove ANSI escape codes and control characters from user input."""
    # Strip ANSI escape sequences
    text = ANSI_ESCAPE_PATTERN.sub('', text)
    # Remove other control characters (except newline/tab)
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
    return text.strip()


from src.ui.cli_branding import (
    print_banner,
    print_footer,
    Colors,
)
from src.ui.output_manager import console
from src.agents.research_system import (
    run_multi_agent_research,
    RESEARCH_STRATEGIES,
)
from src.config import update_llm_model
from src.cli.commands import execute_command, registry, command_history, history
from dotenv import load_dotenv

# Try to import readline for tab completion
try:
    import readline

    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

load_dotenv()

# Version info
__version__ = "1.1.0"
__author__ = "NAMI Team"


class NAMISession:
    """Manages NAMI interactive session state"""

    def __init__(self):
        # Validate strategy number from environment
        try:
            strategy = int(os.getenv("RESEARCH_STRATEGY", "4"))
            if strategy not in RESEARCH_STRATEGIES:
                console.warning(f"Invalid RESEARCH_STRATEGY={strategy} in .env, using default (4)")
                strategy = 4
        except ValueError:
            console.warning(f"Invalid RESEARCH_STRATEGY in .env, using default (4)")
            strategy = 4

        self.strategy = strategy
        self.model = os.getenv("MODEL_NAME", "glm-4.6:cloud")
        self.verbose = True
        self.running = True
        self._research_count = 0

    def get_prompt(self):
        """Generate prompt with current settings"""
        return f"{Colors.BRIGHT_CYAN}nami{Colors.RESET}[{Colors.BRIGHT_YELLOW}S{self.strategy}{Colors.RESET}]> "

    def show_status(self):
        """Show current session configuration"""
        console.print(f"\n{Colors.BRIGHT_WHITE}Session Status{Colors.RESET}")
        console.print(
            f"  Strategy: {Colors.BRIGHT_CYAN}#{self.strategy} - {RESEARCH_STRATEGIES[self.strategy]['name']}{Colors.RESET}"
        )
        console.print(f"  Model:    {Colors.BRIGHT_CYAN}{self.model}{Colors.RESET}")
        console.print(f"  Verbose:  {Colors.BRIGHT_CYAN}{self.verbose}{Colors.RESET}")
        console.print(
            f"  Research: {Colors.BRIGHT_CYAN}{self._research_count} sessions{Colors.RESET}"
        )
        console.print()

    def increment_research(self):
        """Increment research counter"""
        self._research_count += 1


class NAMICompleter:
    """Enhanced tab completion for NAMI commands"""

    def __init__(self):
        self.matches = []
        # Build command list from registry
        self.commands = ["/" + cmd for cmd in registry.list_commands()]
        # Add aliases
        for name, info in registry._info.items():
            if info.aliases:
                for alias in info.aliases:
                    self.commands.append("/" + alias)
        self.commands = sorted(set(self.commands))

    def complete(self, text, state):
        """Readline completion function"""
        if state == 0:
            # First call - generate matches
            if text.startswith("/"):
                # Complete commands
                self.matches = [cmd for cmd in self.commands if cmd.startswith(text)]
            else:
                # No completion for regular text
                self.matches = []

        # Return match at state position
        try:
            return self.matches[state]
        except IndexError:
            return None


def setup_readline():
    """Setup readline for tab completion and history"""
    if not READLINE_AVAILABLE:
        return

    try:
        # Set up tab completion
        completer = NAMICompleter()
        readline.set_completer(completer.complete)
        readline.parse_and_bind("tab: complete")
        readline.set_completer_delims(" \t\n")

        # Load command history
        history_file = Path.home() / ".nami" / "readline_history"
        if history_file.exists():
            try:
                readline.read_history_file(str(history_file))
            except Exception:
                pass

        # Set max history size
        readline.set_history_length(1000)

    except Exception:
        pass


def save_readline_history():
    """Save readline history on exit"""
    if not READLINE_AVAILABLE:
        return

    try:
        history_file = Path.home() / ".nami" / "readline_history"
        history_file.parent.mkdir(parents=True, exist_ok=True)
        readline.write_history_file(str(history_file))
    except Exception:
        pass


def print_welcome():
    """Print welcome message with tips"""
    console.print(f"\n{Colors.BRIGHT_WHITE}Welcome to NAMI Interactive Mode!{Colors.RESET}")
    console.print(f"{Colors.DIM}Type your research query or use slash commands.{Colors.RESET}")
    console.print(f"{Colors.DIM}Type / for commands, /help for detailed help.{Colors.RESET}\n")


def run_interactive():
    """Run NAMI in interactive mode"""
    # Show welcome
    print_banner(style="fancy")
    console.separator("═", 79, Colors.BRIGHT_CYAN)

    # Initialize session
    session = NAMISession()

    # Setup tab completion
    setup_readline()

    # Welcome message and status
    print_welcome()
    session.show_status()

    # Main REPL loop
    try:
        while session.running:
            try:
                # Get user input and sanitize it
                raw_input = input(session.get_prompt())
                user_input = sanitize_input(raw_input)

                if not user_input:
                    continue

                # Handle slash commands
                if user_input.startswith("/"):
                    result = execute_command(user_input, session)
                    # Some commands (like /run) might return a topic to research
                    if result and isinstance(result, str):
                        user_input = sanitize_input(result)
                    else:
                        continue

                # Handle research query (non-slash input)
                console.print()
                console.separator("─", 79, Colors.BRIGHT_YELLOW)
                console.print(
                    f"{Colors.BRIGHT_WHITE}Research Topic:{Colors.RESET} {Colors.BRIGHT_CYAN}{user_input}{Colors.RESET}"
                )
                console.print(
                    f"{Colors.BRIGHT_WHITE}Strategy:{Colors.RESET} #{session.strategy} - {RESEARCH_STRATEGIES[session.strategy]['name']}"
                )
                console.separator("─", 79, Colors.BRIGHT_YELLOW)
                console.print()

                # Track start time
                import time

                start_time = time.time()

                # Run research
                try:
                    run_multi_agent_research(
                        topic=user_input, strategy=session.strategy, verbose=session.verbose
                    )
                    success = True
                except Exception as e:
                    console.error(f"Research failed: {e}")
                    success = False

                # Calculate duration
                duration = time.time() - start_time

                # Add to history
                history.add(
                    topic=user_input, strategy=session.strategy, duration=duration, success=success
                )

                # Increment counter
                session.increment_research()

                console.print()
                console.separator("═", 79, Colors.BRIGHT_GREEN)
                console.success("Research completed!")
                console.separator("═", 79, Colors.BRIGHT_GREEN)
                console.print()

            except KeyboardInterrupt:
                console.print(
                    f"\n{Colors.BRIGHT_YELLOW}Interrupted. Type /exit to quit or continue researching.{Colors.RESET}\n"
                )
                continue
            except EOFError:
                break
            except Exception as e:
                console.error(f"Error: {e}")
                console.print()

    except KeyboardInterrupt:
        console.print(f"\n\n{Colors.BRIGHT_GREEN}Goodbye!{Colors.RESET}\n")
    finally:
        # Save histories
        save_readline_history()
        command_history.save()


@click.command()
@click.option("--strategy", "-s", type=int, help="Initial strategy (1-10)")
@click.option("--model", "-m", help="LLM model name")
@click.argument("query", required=False, nargs=-1)
def cli(strategy, model, query):
    """
    NAMI - Multi-Agent Research Intelligence System

    Interactive REPL-style interface inspired by Claude Code.

    \b
    Usage:
      nami_cli                         # Start interactive mode
      nami_cli "your query"            # Run one-off research
      nami_cli -s 4 "your query"       # Research with specific strategy

    \b
    In interactive mode, use slash commands:
      /help          Show all commands
      /strat <N>     Change strategy
      /llm [model]   Change LLM model
      /history       Show research history
      /agents        List available agents
      /tools         List available tools
      /exit          Exit NAMI
    """
    # Handle initial configuration
    if strategy:
        os.environ["RESEARCH_STRATEGY"] = str(strategy)
    if model:
        os.environ["MODEL_NAME"] = model
        try:
            update_llm_model(model)
        except Exception:
            pass

    # If query provided, run one-off research
    if query:
        query_text = " ".join(query)
        print_banner(style="fancy")
        console.separator("═", 79, Colors.BRIGHT_CYAN)
        console.print()

        run_multi_agent_research(
            topic=query_text, strategy=strategy if strategy else None, verbose=True
        )

        print_footer()
        return

    # Otherwise, start interactive mode
    run_interactive()


if __name__ == "__main__":
    cli()
