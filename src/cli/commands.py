"""
Enhanced CLI Commands for NAMI Research System

Provides new slash commands with improved help and functionality.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass
from datetime import datetime

from src.ui.cli_branding import Colors
from src.ui.output_manager import console


@dataclass
class CommandInfo:
    """Metadata for a CLI command"""

    name: str
    description: str
    usage: str
    examples: List[str]
    aliases: List[str] = None
    category: str = "general"

    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []


class CommandRegistry:
    """
    Registry for CLI commands with improved help and organization.
    """

    def __init__(self):
        self._commands: Dict[str, Callable] = {}
        self._info: Dict[str, CommandInfo] = {}
        self._categories = {
            "research": "Research Commands",
            "config": "Configuration",
            "info": "Information",
            "utility": "Utilities",
        }

    def register(self, info: CommandInfo):
        """Decorator to register a command"""

        def decorator(func: Callable):
            self._commands[info.name] = func
            self._info[info.name] = info

            # Register aliases
            for alias in info.aliases or []:
                self._commands[alias] = func
                # Store info for alias too (for help lookup)
                alias_info = CommandInfo(
                    name=alias,
                    description=f"Alias for /{info.name}",
                    usage=info.usage.replace(info.name, alias),
                    examples=info.examples,
                    aliases=[],
                    category=info.category,
                )
                self._info[alias] = alias_info

            return func

        return decorator

    def get_command(self, name: str) -> Optional[Callable]:
        """Get a command by name"""
        return self._commands.get(name.lower())

    def get_info(self, name: str) -> Optional[CommandInfo]:
        """Get command info by name"""
        return self._info.get(name.lower())

    def list_commands(self) -> List[str]:
        """List all command names (without aliases)"""
        return sorted([name for name, info in self._info.items() if name == info.name])

    def list_by_category(self) -> Dict[str, List[CommandInfo]]:
        """Group commands by category"""
        by_category: Dict[str, List[CommandInfo]] = {}
        for name, info in self._info.items():
            if name != info.name:  # Skip aliases
                continue
            cat = info.category
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(info)

        # Sort each category
        for cat in by_category:
            by_category[cat].sort(key=lambda x: x.name)

        return by_category

    def find_similar(self, query: str, max_results: int = 3) -> List[str]:
        """Find commands similar to query"""
        query = query.lower()
        matches = []

        # Exact prefix matches first
        for name in self._commands:
            if name.startswith(query):
                matches.append(name)

        # Substring matches
        if len(matches) < max_results:
            for name in self._commands:
                if query in name and name not in matches:
                    matches.append(name)

        return matches[:max_results]


# Global registry instance
registry = CommandRegistry()


class ResearchHistory:
    """
    Manages research session history with persistence.
    """

    HISTORY_FILE = Path.home() / ".nami" / "research_history.json"
    MAX_HISTORY = 100

    def __init__(self):
        self._history: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        """Load history from file"""
        try:
            if self.HISTORY_FILE.exists():
                with open(self.HISTORY_FILE, "r", encoding="utf-8") as f:
                    self._history = json.load(f)
        except json.JSONDecodeError as e:
            # Corrupted JSON file - reset history
            console.warning(f"Research history corrupted, resetting: {e}")
            self._history = []
        except PermissionError:
            console.warning(f"Cannot read research history: permission denied")
            self._history = []
        except Exception as e:
            console.warning(f"Failed to load research history: {e}")
            self._history = []

    def _save(self) -> None:
        """Save history to file"""
        try:
            self.HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(self.HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self._history[-self.MAX_HISTORY :], f, indent=2)
        except PermissionError:
            console.warning("Cannot save research history: permission denied")
        except Exception as e:
            console.warning(f"Failed to save research history: {e}")

    def add(self, topic: str, strategy: int, duration: float = 0, success: bool = True) -> None:
        """Add a research session to history"""
        entry = {
            "topic": topic,
            "strategy": strategy,
            "timestamp": datetime.now().isoformat(),
            "duration": duration,
            "success": success,
        }
        self._history.append(entry)
        self._save()

    def get_recent(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get most recent history entries"""
        return list(reversed(self._history[-count:]))

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search history by topic"""
        query = query.lower()
        return [h for h in self._history if query in h["topic"].lower()]

    def clear(self) -> None:
        """Clear all history"""
        self._history = []
        self._save()


# Global history instance
history = ResearchHistory()


class CommandHistory:
    """
    Manages command history for the CLI.
    """

    HISTORY_FILE = Path.home() / ".nami" / "command_history.txt"
    MAX_COMMANDS = 500

    def __init__(self):
        self._commands: List[str] = []
        self._load()

    def _load(self) -> None:
        """Load command history"""
        try:
            if self.HISTORY_FILE.exists():
                with open(self.HISTORY_FILE, "r", encoding="utf-8") as f:
                    self._commands = [line.strip() for line in f.readlines()]
        except PermissionError:
            # Silently ignore permission errors on load (common on first run)
            self._commands = []
        except Exception as e:
            console.warning(f"Failed to load command history: {e}")
            self._commands = []

    def save(self) -> None:
        """Save command history"""
        try:
            self.HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(self.HISTORY_FILE, "w", encoding="utf-8") as f:
                for cmd in self._commands[-self.MAX_COMMANDS :]:
                    f.write(cmd + "\n")
        except PermissionError:
            console.warning("Cannot save command history: permission denied")
        except Exception as e:
            console.warning(f"Failed to save command history: {e}")

    def add(self, command: str) -> None:
        """Add a command to history"""
        if command and (not self._commands or self._commands[-1] != command):
            self._commands.append(command)

    def get_all(self) -> List[str]:
        """Get all commands"""
        return self._commands

    def get_recent(self, count: int = 20) -> List[str]:
        """Get recent commands"""
        return list(reversed(self._commands[-count:]))


# Global command history
command_history = CommandHistory()


def format_help_for_command(info: CommandInfo) -> str:
    """Format detailed help for a command"""
    lines = []

    # Header
    lines.append(f"\n{Colors.BRIGHT_WHITE}/{info.name}{Colors.RESET}")
    lines.append(f"{Colors.DIM}{info.description}{Colors.RESET}")

    # Aliases
    if info.aliases:
        aliases_str = ", ".join(f"/{a}" for a in info.aliases)
        lines.append(f"\n{Colors.BRIGHT_CYAN}Aliases:{Colors.RESET} {aliases_str}")

    # Usage
    lines.append(f"\n{Colors.BRIGHT_CYAN}Usage:{Colors.RESET}")
    lines.append(f"  {Colors.BRIGHT_WHITE}{info.usage}{Colors.RESET}")

    # Examples
    if info.examples:
        lines.append(f"\n{Colors.BRIGHT_CYAN}Examples:{Colors.RESET}")
        for example in info.examples:
            lines.append(f"  {Colors.BRIGHT_GREEN}{example}{Colors.RESET}")

    lines.append("")
    return "\n".join(lines)


def format_command_list() -> str:
    """Format the full command list"""
    lines = []

    lines.append(f"\n{Colors.BRIGHT_WHITE}NAMI Commands{Colors.RESET}\n")

    by_category = registry.list_by_category()

    for cat_key, cat_name in [
        ("research", "Research Commands"),
        ("config", "Configuration"),
        ("info", "Information"),
        ("utility", "Utilities"),
    ]:
        if cat_key not in by_category:
            continue

        commands = by_category[cat_key]
        lines.append(f"{Colors.BRIGHT_YELLOW}{cat_name}{Colors.RESET}")

        for cmd in commands:
            aliases_str = ""
            if cmd.aliases:
                aliases_str = f" {Colors.DIM}(/{', /'.join(cmd.aliases)}){Colors.RESET}"

            lines.append(
                f"  {Colors.BRIGHT_CYAN}/{cmd.name:<14}{Colors.RESET} "
                f"{cmd.description}{aliases_str}"
            )

        lines.append("")

    lines.append(f"{Colors.DIM}Type /<command> --help for detailed usage{Colors.RESET}")
    lines.append(f"{Colors.DIM}Type any text (no slash) to start research{Colors.RESET}\n")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════
# COMMAND DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════


@registry.register(
    CommandInfo(
        name="help",
        description="Show available commands and usage",
        usage="/help [command]",
        examples=["/help", "/help strat", "/help llm"],
        category="info",
    )
)
def cmd_help(args: str, session) -> None:
    """Show help information"""
    if args:
        # Show help for specific command
        cmd_name = args.split()[0].lstrip("/")
        info = registry.get_info(cmd_name)
        if info:
            console.print(format_help_for_command(info))
        else:
            console.error(f"Unknown command: {cmd_name}")
            similar = registry.find_similar(cmd_name)
            if similar:
                console.print(f"\n{Colors.BRIGHT_WHITE}Did you mean:{Colors.RESET}")
                for s in similar:
                    console.print(f"  {Colors.BRIGHT_CYAN}/{s}{Colors.RESET}")
    else:
        console.print(format_command_list())


@registry.register(
    CommandInfo(
        name="run",
        description="Run research with specific options",
        usage="/run [strategy] <topic>",
        examples=[
            "/run quantum computing applications",
            "/run 4 AI safety research",
            "/run --strategy 7 pros and cons of remote work",
        ],
        aliases=["r"],
        category="research",
    )
)
def cmd_run(args: str, session) -> Optional[str]:
    """Run research directly with options.

    Returns:
        Optional[str]: The research topic if valid, None if command handled or error.
    """
    if not args:
        console.error("Usage: /run [strategy] <topic>")
        console.info("Example: /run 4 quantum computing")
        return None

    parts = args.split(None, 1)

    # Check if first arg is a strategy number
    try:
        strategy = int(parts[0])
        if 1 <= strategy <= 10:
            if len(parts) > 1:
                topic = parts[1]
                session.strategy = strategy
                # Return topic to trigger research
                return topic
            else:
                console.error("Please provide a research topic")
                return None
        else:
            # Strategy number out of range
            console.error(f"Invalid strategy: {strategy}. Must be 1-10.")
            console.info("Use /strategies to see all available strategies")
            return None
    except ValueError:
        pass

    # First arg is part of the topic
    return args


@registry.register(
    CommandInfo(
        name="history",
        description="Show research history",
        usage="/history [count|search <query>|clear]",
        examples=["/history", "/history 20", "/history search quantum", "/history clear"],
        aliases=["hist", "h"],
        category="research",
    )
)
def cmd_history(args: str, session) -> None:
    """Show research history"""
    if not args:
        # Show recent history
        entries = history.get_recent(10)
        if not entries:
            console.info("No research history yet")
            return

        console.print(f"\n{Colors.BRIGHT_WHITE}Recent Research{Colors.RESET}\n")
        for i, entry in enumerate(entries, 1):
            status = (
                f"{Colors.BRIGHT_GREEN}✓{Colors.RESET}"
                if entry.get("success", True)
                else f"{Colors.BRIGHT_RED}✗{Colors.RESET}"
            )
            timestamp = entry.get("timestamp", "")[:10]
            topic = entry.get("topic", "")[:50]
            strategy = entry.get("strategy", "?")

            console.print(
                f"  {status} {Colors.DIM}{timestamp}{Colors.RESET} "
                f"{Colors.BRIGHT_CYAN}[S{strategy}]{Colors.RESET} {topic}"
            )

        console.print()
        return

    parts = args.split(None, 1)
    cmd = parts[0].lower()

    if cmd == "clear":
        history.clear()
        console.success("Research history cleared")
    elif cmd == "search" and len(parts) > 1:
        query = parts[1]
        results = history.search(query)
        if results:
            console.print(f"\n{Colors.BRIGHT_WHITE}Search Results: {query}{Colors.RESET}\n")
            for entry in results[-10:]:
                timestamp = entry.get("timestamp", "")[:10]
                topic = entry.get("topic", "")
                console.print(f"  {Colors.DIM}{timestamp}{Colors.RESET} {topic}")
            console.print()
        else:
            console.info(f"No results found for: {query}")
    else:
        try:
            count = int(cmd)
            entries = history.get_recent(count)
            console.print(
                f"\n{Colors.BRIGHT_WHITE}Last {len(entries)} Research Sessions{Colors.RESET}\n"
            )
            for entry in entries:
                timestamp = entry.get("timestamp", "")[:16]
                topic = entry.get("topic", "")
                console.print(f"  {Colors.DIM}{timestamp}{Colors.RESET} {topic}")
            console.print()
        except ValueError:
            console.error("Usage: /history [count|search <query>|clear]")


@registry.register(
    CommandInfo(
        name="agents",
        description="List available agents and their roles",
        usage="/agents [name]",
        examples=["/agents", "/agents researcher"],
        category="info",
    )
)
def cmd_agents(args: str, session) -> None:
    """Show agent information"""
    try:
        from src.agents.subagent_registry import SubagentRegistry

        if args:
            # Show specific agent
            name = args.strip().lower()
            try:
                agent = SubagentRegistry.get(name)
                console.print(f"\n{Colors.BRIGHT_WHITE}{agent.name}{Colors.RESET}")
                console.print(f"{Colors.DIM}{agent.description}{Colors.RESET}")
                console.print(f"\n{Colors.BRIGHT_CYAN}Tools:{Colors.RESET}")
                for tool in agent.tools[:5]:
                    tool_name = getattr(tool, "__name__", str(tool))
                    console.print(f"  • {tool_name}")
                if len(agent.tools) > 5:
                    console.print(f"  {Colors.DIM}...and {len(agent.tools) - 5} more{Colors.RESET}")
                console.print()
            except KeyError:
                console.error(f"Agent not found: {name}")
                console.info("Use /agents to list all available agents")
        else:
            # List all agents
            agents = SubagentRegistry.list_all()
            console.print(f"\n{Colors.BRIGHT_WHITE}Available Agents{Colors.RESET}\n")

            # Group by role type
            for agent_name in sorted(agents)[:15]:
                try:
                    agent = SubagentRegistry.get(agent_name)
                    desc = (
                        agent.description[:50] + "..."
                        if len(agent.description) > 50
                        else agent.description
                    )
                    console.print(
                        f"  {Colors.BRIGHT_CYAN}{agent_name:<20}{Colors.RESET} "
                        f"{Colors.DIM}{desc}{Colors.RESET}"
                    )
                except Exception:
                    pass

            if len(agents) > 15:
                console.print(f"\n  {Colors.DIM}...and {len(agents) - 15} more{Colors.RESET}")

            console.print(f"\n{Colors.DIM}Use /agents <name> for details{Colors.RESET}\n")

    except ImportError:
        console.error("Agent registry not available")


@registry.register(
    CommandInfo(
        name="tools",
        description="List available research tools",
        usage="/tools [name]",
        examples=["/tools", "/tools search_tavily"],
        category="info",
    )
)
def cmd_tools(args: str, session) -> None:
    """Show available tools"""
    try:
        from src.tools.tool_sets import ToolSets

        if args:
            # Show specific tool or tool set
            name = args.strip().upper()
            if hasattr(ToolSets, name):
                tools = getattr(ToolSets, name)
                console.print(f"\n{Colors.BRIGHT_WHITE}Tool Set: {name}{Colors.RESET}\n")
                for tool in tools:
                    tool_name = getattr(tool, "__name__", str(tool))
                    doc = getattr(tool, "__doc__", "") or ""
                    doc_preview = doc.split("\n")[0][:60] if doc else ""
                    console.print(
                        f"  {Colors.BRIGHT_CYAN}•{Colors.RESET} {tool_name}"
                        f"{' - ' + doc_preview if doc_preview else ''}"
                    )
                console.print()
            else:
                console.error(f"Tool set not found: {name}")
        else:
            # List tool sets
            console.print(f"\n{Colors.BRIGHT_WHITE}Available Tool Sets{Colors.RESET}\n")

            tool_sets = [
                ("BASIC_SEARCH", "Web search tools"),
                ("ACADEMIC_SEARCH", "Academic/scholarly search"),
                ("DEEP_READING", "Content extraction"),
                ("WRITING", "Text processing & output"),
                ("THINKING", "Reflection tools"),
                ("KNOWLEDGE_BASE", "RAG tools"),
            ]

            for name, desc in tool_sets:
                if hasattr(ToolSets, name):
                    tools = getattr(ToolSets, name)
                    console.print(
                        f"  {Colors.BRIGHT_CYAN}{name:<18}{Colors.RESET} "
                        f"{Colors.DIM}{desc} ({len(tools)} tools){Colors.RESET}"
                    )

            console.print(f"\n{Colors.DIM}Use /tools <SET_NAME> for details{Colors.RESET}\n")

    except ImportError:
        console.error("Tool sets not available")


@registry.register(
    CommandInfo(
        name="strat",
        description="Change research strategy",
        usage="/strat <number>",
        examples=["/strat 4", "/strat 7"],
        aliases=["strategy", "s"],
        category="config",
    )
)
def cmd_strat(args: str, session) -> None:
    """Change research strategy"""
    from src.agents.research_system import RESEARCH_STRATEGIES

    if not args:
        console.error("Usage: /strat <number>")
        console.info("Example: /strat 4")
        console.info("Use /strategies to see all available strategies")
        return

    try:
        strategy = int(args.split()[0])
        if strategy not in RESEARCH_STRATEGIES:
            console.error(f"Invalid strategy: {strategy}. Must be 1-10.")
            return

        old = session.strategy
        session.strategy = strategy

        console.success(f"Strategy changed: #{old} → #{strategy}")
        console.info(f"Now using: {RESEARCH_STRATEGIES[strategy]['name']}")

    except ValueError:
        console.error("Invalid strategy number")


@registry.register(
    CommandInfo(
        name="strategies",
        description="List all research strategies",
        usage="/strategies",
        examples=["/strategies"],
        aliases=["strats"],
        category="info",
    )
)
def cmd_strategies(args: str, session) -> None:
    """List all strategies"""
    from src.agents.research_system import RESEARCH_STRATEGIES

    console.print(f"\n{Colors.BRIGHT_WHITE}Research Strategies{Colors.RESET}\n")

    for sid, info in sorted(RESEARCH_STRATEGIES.items()):
        active = " ←" if sid == session.strategy else ""
        marker = (
            f"{Colors.BRIGHT_GREEN}●{Colors.RESET}"
            if sid == session.strategy
            else f"{Colors.DIM}○{Colors.RESET}"
        )

        console.print(
            f"  {marker} {Colors.BRIGHT_CYAN}{sid:2}.{Colors.RESET} "
            f"{info['name']:<28} "
            f"{Colors.DIM}{info['best_for'][:35]}...{Colors.RESET}"
            f"{Colors.BRIGHT_GREEN}{active}{Colors.RESET}"
        )

    console.print(f"\n{Colors.DIM}Use /strat <N> to change strategy{Colors.RESET}")
    console.print(f"{Colors.DIM}Use /info <N> for details{Colors.RESET}\n")


@registry.register(
    CommandInfo(
        name="llm",
        description="List or change LLM model",
        usage="/llm [model_name|number]",
        examples=["/llm", "/llm 2", "/llm llama3"],
        aliases=["model"],
        category="config",
    )
)
def cmd_llm(args: str, session) -> None:
    """Change LLM model"""
    from src.config import update_llm_model

    def get_ollama_models():
        import subprocess

        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return []
            lines = result.stdout.strip().split("\n")
            if len(lines) < 2:
                return []
            models = []
            for line in lines[1:]:
                parts = line.split()
                if parts:
                    models.append({"name": parts[0], "size": parts[1] if len(parts) > 1 else ""})
            return models
        except Exception:
            return None

    if not args:
        # List available models
        console.print(f"\n{Colors.BRIGHT_WHITE}Available LLM Models{Colors.RESET}\n")

        models = get_ollama_models()
        if models is None:
            console.warning("Ollama not found")
            console.print(f"\n{Colors.BRIGHT_WHITE}Current:{Colors.RESET} {session.model}\n")
            return
        elif not models:
            console.warning("No Ollama models found")
            return

        for idx, model in enumerate(models, 1):
            active = " ←" if model["name"] == session.model else ""
            marker = (
                f"{Colors.BRIGHT_GREEN}●{Colors.RESET}"
                if model["name"] == session.model
                else f"{Colors.DIM}○{Colors.RESET}"
            )

            console.print(
                f"  {marker} {Colors.BRIGHT_YELLOW}{idx:2}.{Colors.RESET} "
                f"{Colors.BRIGHT_CYAN}{model['name']:<30}{Colors.RESET} "
                f"{Colors.DIM}{model['size']}{Colors.RESET}"
                f"{Colors.BRIGHT_GREEN}{active}{Colors.RESET}"
            )

        console.print(f"\n{Colors.DIM}Usage: /llm <number> or /llm <model_name>{Colors.RESET}\n")
        return

    # Parse selection
    selection = args.strip()
    models = get_ollama_models()

    try:
        idx = int(selection)
        # Check if models is available and index is valid
        if models is None:
            console.error("Cannot select by number: Ollama not available")
            console.info("Try: /llm <model_name> to set model directly")
            return
        if not models:
            console.error("No Ollama models found")
            return
        if 1 <= idx <= len(models):
            model_name = models[idx - 1]["name"]
        else:
            console.error(f"Invalid model number: {idx}. Must be 1-{len(models)}")
            return
    except ValueError:
        model_name = selection

    # Update model
    old = session.model
    session.model = model_name

    try:
        update_llm_model(model_name)
        console.success(f"Model changed: {old} → {model_name}")
    except Exception as e:
        console.error(f"Failed to update model: {e}")


@registry.register(
    CommandInfo(
        name="config",
        description="Show current configuration",
        usage="/config",
        examples=["/config"],
        category="info",
    )
)
def cmd_config(args: str, session) -> None:
    """Show current configuration"""
    from src.agents.research_system import RESEARCH_STRATEGIES

    console.print(f"\n{Colors.BRIGHT_WHITE}Current Configuration{Colors.RESET}\n")

    config_items = [
        ("Strategy", f"#{session.strategy} - {RESEARCH_STRATEGIES[session.strategy]['name']}"),
        ("Model", session.model),
        ("Verbose", str(session.verbose)),
        ("Max Iterations", os.getenv("MAX_RESEARCHER_ITERATIONS", "3")),
    ]

    for key, value in config_items:
        console.print(
            f"  {Colors.BRIGHT_WHITE}{key:<16}{Colors.RESET} {Colors.BRIGHT_CYAN}{value}{Colors.RESET}"
        )

    console.print(f"\n{Colors.DIM}Edit .env to change defaults{Colors.RESET}\n")


@registry.register(
    CommandInfo(
        name="info",
        description="Show strategy details",
        usage="/info <strategy_number>",
        examples=["/info 4", "/info 7"],
        category="info",
    )
)
def cmd_info(args: str, session) -> None:
    """Show strategy information"""
    from src.agents.research_system import get_strategy_info

    if not args:
        console.error("Usage: /info <strategy_number>")
        return

    try:
        sid = int(args.split()[0])
        info = get_strategy_info(sid)

        console.print(f"\n{Colors.BRIGHT_YELLOW}Strategy {sid}: {info['name']}{Colors.RESET}\n")
        console.print(f"{Colors.BRIGHT_WHITE}Description:{Colors.RESET}")
        console.print(f"  {info['description']}\n")
        console.print(f"{Colors.BRIGHT_WHITE}Best For:{Colors.RESET}")
        console.print(f"  {info['best_for']}\n")
        console.print(f"{Colors.DIM}Use /strat {sid} to switch{Colors.RESET}\n")

    except ValueError as e:
        console.error(str(e))


@registry.register(
    CommandInfo(
        name="status",
        description="Show session status",
        usage="/status",
        examples=["/status"],
        category="info",
    )
)
def cmd_status(args: str, session) -> None:
    """Show session status"""
    session.show_status()


@registry.register(
    CommandInfo(
        name="set",
        description="Set configuration value",
        usage="/set <key> <value>",
        examples=["/set MAX_ITERATIONS 5"],
        category="config",
    )
)
def cmd_set(args: str, session) -> None:
    """Set configuration value"""
    if not args:
        console.error("Usage: /set <key> <value>")
        return

    parts = args.split(None, 1)
    if len(parts) < 2:
        console.error("Usage: /set <key> <value>")
        return

    key, value = parts
    os.environ[key] = value
    console.success(f"Set {key} = {value}")
    console.warning("Note: This only affects the current session")


@registry.register(
    CommandInfo(
        name="verbose",
        description="Toggle verbose output",
        usage="/verbose [on|off]",
        examples=["/verbose", "/verbose on", "/verbose off"],
        category="config",
    )
)
def cmd_verbose(args: str, session) -> None:
    """Toggle verbose output"""
    if not args:
        session.verbose = not session.verbose
    else:
        arg = args.lower().strip()
        if arg in ["on", "true", "1", "yes"]:
            session.verbose = True
        elif arg in ["off", "false", "0", "no"]:
            session.verbose = False
        else:
            console.error("Usage: /verbose [on|off]")
            return

    status = "enabled" if session.verbose else "disabled"
    console.success(f"Verbose output {status}")


@registry.register(
    CommandInfo(
        name="clear",
        description="Clear screen",
        usage="/clear",
        examples=["/clear"],
        aliases=["cls"],
        category="utility",
    )
)
def cmd_clear(args: str, session) -> None:
    """Clear screen"""
    from src.ui.cli_branding import print_banner

    os.system("cls" if os.name == "nt" else "clear")
    print_banner(style="simple")
    console.print()


@registry.register(
    CommandInfo(
        name="version",
        description="Show version information",
        usage="/version",
        examples=["/version"],
        category="info",
    )
)
def cmd_version(args: str, session) -> None:
    """Show version information"""
    console.print(f"\n{Colors.BRIGHT_WHITE}NAMI Version Information{Colors.RESET}\n")
    console.print(f"  Version:    {Colors.BRIGHT_CYAN}1.1.0{Colors.RESET}")
    console.print(f"  Author:     {Colors.BRIGHT_CYAN}NAMI Team{Colors.RESET}")
    console.print(f"  Strategies: {Colors.BRIGHT_CYAN}10{Colors.RESET}")
    console.print(
        f"  Python:     {Colors.BRIGHT_CYAN}{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}{Colors.RESET}"
    )
    console.print()


@registry.register(
    CommandInfo(
        name="exit",
        description="Exit NAMI",
        usage="/exit",
        examples=["/exit"],
        aliases=["quit", "q"],
        category="utility",
    )
)
def cmd_exit(args: str, session) -> None:
    """Exit NAMI"""
    session.running = False
    console.print(f"\n{Colors.BRIGHT_GREEN}Thanks for using NAMI!{Colors.RESET}\n")


def execute_command(command_line: str, session) -> Optional[str]:
    """
    Execute a slash command.

    Returns:
        None if command was handled
        str if command returned a topic to research
    """
    if not command_line.startswith("/"):
        return None

    # Parse command
    parts = command_line[1:].strip().split(None, 1)

    if not parts:
        console.print(format_command_list())
        return None

    cmd_name = parts[0].lower()

    # Check for --help flag
    args = parts[1] if len(parts) > 1 else ""
    if args == "--help" or args == "-h":
        info = registry.get_info(cmd_name)
        if info:
            console.print(format_help_for_command(info))
        else:
            console.error(f"Unknown command: {cmd_name}")
        return None

    # Execute command
    handler = registry.get_command(cmd_name)
    if handler:
        try:
            result = handler(args, session)
            # Record command in history
            command_history.add(command_line)
            return result
        except Exception as e:
            console.error(f"Command failed: {e}")
            return None
    else:
        console.error(f"Unknown command: /{cmd_name}")
        similar = registry.find_similar(cmd_name)
        if similar:
            console.print(f"\n{Colors.BRIGHT_WHITE}Did you mean:{Colors.RESET}")
            for s in similar:
                console.print(f"  {Colors.BRIGHT_CYAN}/{s}{Colors.RESET}")
        else:
            console.info("Type / to see all available commands")

    return None
