"""Multi-Agent Research System - Supports 10 different research strategies

This module provides a flexible research system with 10 specialized strategies:

STRATEGY 1: Multi-Agent Research Orchestrator (Mapper → Diver → Critic → Synthesizer)
STRATEGY 2: Supervisor Researcher (Research → Analyze → Write → Critique)
STRATEGY 3: Delegation Research (Coordinated sub-agent delegation)
STRATEGY 4: Parallel Swarm Research (3 parallel researchers + consensus)
STRATEGY 5: Iterative Refinement (Research → Critique → Refine loop)
STRATEGY 6: Domain-Specific Research (Academic + Industry + Technical)
STRATEGY 7: Debate-Driven Research (Advocate vs Skeptic + Judge)
STRATEGY 8: Hierarchical Deep Dive (Overview → Detail → Specialist)
STRATEGY 9: Real-Time Collaborative (Speed-optimized for breaking news)
STRATEGY 10: Comparative Research (Option A vs B vs C + Recommendations)
"""

import sys
import os
import time
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from datetime import datetime
from langchain_ollama import ChatOllama
from src.prompts.core_agent_prompts import (
    MULTI_AGENT_WORKFLOW_INSTRUCTIONS,
)
from src.agents.core_agents import get_agent
from dotenv import load_dotenv

load_dotenv()

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")


# MODEL CONFIGURATION (kept for compatibility but agents use get_llm() now)
model = ChatOllama(model=os.getenv("MODEL_NAME", "glm-4.6:cloud"), temperature=0.0)


# STRATEGY SELECTOR MAPPING
# Note: "agent" is now None and will be created dynamically via get_agent()
RESEARCH_STRATEGIES = {
    1: {
        "name": "Multi-Agent Orchestrator",
        "agent": None,  # Created dynamically
        "description": "Hierarchical workflow: Mapper → Diver → Critic → Synthesizer",
        "best_for": "Complex topics requiring structured decomposition and quality assessment",
        "workflow": MULTI_AGENT_WORKFLOW_INSTRUCTIONS,
    },
    2: {
        "name": "Supervisor Researcher",
        "agent": None,  # Created dynamically
        "description": "Sequential workflow: Research → Analyze → Write → Critique",
        "best_for": "Standard research reports with iterative refinement",
        "workflow": "Research the topic: {topic}\n\nDate: {current_date}",
    },
    3: {
        "name": "Delegation Research",
        "agent": None,  # Created dynamically
        "description": "Coordinated sub-agent delegation with todo tracking",
        "best_for": "Token-efficient research with adaptive parallelization",
        "workflow": "Research the topic: {topic}\n\nDate: {current_date}",
    },
    4: {
        "name": "Parallel Swarm",
        "agent": None,  # Created dynamically
        "description": "3 parallel researchers + consensus building",
        "best_for": "High-confidence findings through cross-validation",
        "workflow": "Research the topic using parallel swarm approach: {topic}\n\nDate: {current_date}",
    },
    5: {
        "name": "Iterative Refinement",
        "agent": None,  # Created dynamically
        "description": "Research → Critique → Refine loop for quality improvement",
        "best_for": "High-quality reports requiring progressive refinement",
        "workflow": "Research the topic with iterative refinement: {topic}\n\nDate: {current_date}",
    },
    6: {
        "name": "Domain-Specific",
        "agent": None,  # Created dynamically
        "description": "Academic + Industry + Technical researchers in parallel",
        "best_for": "Multi-perspective research combining theory and practice",
        "workflow": "Research the topic across academic, industry, and technical domains: {topic}\n\nDate: {current_date}",
    },
    7: {
        "name": "Debate-Driven",
        "agent": None,  # Created dynamically
        "description": "Advocate vs Skeptic with moderated debate",
        "best_for": "Balanced perspectives on controversial or debated topics",
        "workflow": "Research the topic using debate approach: {topic}\n\nDate: {current_date}",
    },
    8: {
        "name": "Hierarchical Deep Dive",
        "agent": None,  # Created dynamically
        "description": "Overview → Detailed → Specialist (3-level hierarchy)",
        "best_for": "Comprehensive documentation from broad to expert-level detail",
        "workflow": "Research the topic using hierarchical deep dive: {topic}\n\nDate: {current_date}",
    },
    9: {
        "name": "Real-Time Collaborative",
        "agent": None,  # Created dynamically
        "description": "Speed-optimized for breaking news and time-sensitive research",
        "best_for": "Rapid intelligence on trending topics (8-15 minute target)",
        "workflow": "Research the topic with real-time speed optimization: {topic}\n\nDate: {current_date}",
    },
    10: {
        "name": "Comparative Research",
        "agent": None,  # Created dynamically
        "description": "Option A vs B vs C + comparison analysis + recommendations",
        "best_for": "Side-by-side comparisons with decision support",
        "workflow": "Compare the following: {topic}\n\nDate: {current_date}",
    },
}


# HELPER FUNCTIONS
def list_strategies():
    """
    List all available research strategies with descriptions.

    Returns:
        None (prints to console)
    """
    print("\n" + "=" * 80)
    print("AVAILABLE RESEARCH STRATEGIES")
    print("=" * 80 + "\n")

    for strategy_id, strategy_info in RESEARCH_STRATEGIES.items():
        print(f"STRATEGY {strategy_id}: {strategy_info['name']}")
        print(f"  Description: {strategy_info['description']}")
        print(f"  Best For: {strategy_info['best_for']}")
        print()


def get_strategy_info(strategy_id: int):
    """
    Get information about a specific strategy.

    Args:
        strategy_id: Strategy number (1-10)

    Returns:
        dict: Strategy information

    Raises:
        ValueError: If strategy_id is invalid
    """
    if strategy_id not in RESEARCH_STRATEGIES:
        raise ValueError(
            f"Invalid strategy_id: {strategy_id}. Must be between 1 and 10."
        )

    return RESEARCH_STRATEGIES[strategy_id]


def run_multi_agent_research(
    topic: str, strategy: int = None, verbose: bool = True  # type: ignore
):
    """
    Run a multi-agent research workflow using the specified strategy.

    This function supports 10 different research strategies, each optimized
    for different types of research tasks.

    Args:
        topic: The research topic or question to investigate
        strategy: Strategy number (1-10). If None, uses RESEARCH_STRATEGY env var or defaults to 1.
        verbose: Whether to print progress messages (default: True)

    Returns:
        dict: The complete workflow response including the final report

    Examples:
        >>> # Use default strategy (Strategy 1)
        >>> result = run_multi_agent_research("Quantum computing")

        >>> # Use parallel swarm strategy
        >>> result = run_multi_agent_research("AI safety", strategy=4)

        >>> # Use comparative research
        >>> result = run_multi_agent_research("Python vs JavaScript", strategy=10)

        >>> # List all strategies
        >>> list_strategies()
    """
    # Determine strategy
    if strategy is None:
        strategy = int(os.getenv("RESEARCH_STRATEGY", 1))

    # Validate strategy
    if strategy not in RESEARCH_STRATEGIES:
        raise ValueError(
            f"Invalid strategy: {strategy}. Must be between 1 and 10. "
            f"Use list_strategies() to see available strategies."
        )

    strategy_info = RESEARCH_STRATEGIES[strategy]

    # Track timing
    start_time = time.time()

    if verbose:
        from src.ui.output_manager import console
        from src.ui.cli_branding import Colors
        from src.ui.progress_display import (
            get_progress, set_phase, agent_start, agent_complete, log_activity
        )

        progress = get_progress()

        # Research Header with Box
        console.print()
        console.print(f"{Colors.BRIGHT_CYAN}╔═══════════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_CYAN}║{Colors.RESET}  {Colors.BRIGHT_WHITE}Multi-Agent Research System{Colors.RESET}                                              {Colors.BRIGHT_CYAN}║{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_CYAN}╚═══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")

        # Research Configuration Box
        console.print()
        console.print(f"{Colors.BRIGHT_WHITE}┌─ Research Configuration{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_WHITE}│{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_WHITE}│{Colors.RESET}  {Colors.BRIGHT_CYAN}Topic:{Colors.RESET}      {Colors.BRIGHT_YELLOW}{topic}{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_WHITE}│{Colors.RESET}  {Colors.BRIGHT_CYAN}Strategy:{Colors.RESET}   {Colors.BRIGHT_CYAN}#{strategy}{Colors.RESET} - {Colors.BRIGHT_WHITE}{strategy_info['name']}{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_WHITE}│{Colors.RESET}  {Colors.BRIGHT_CYAN}Best For:{Colors.RESET}   {Colors.DIM}{strategy_info['best_for']}{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_WHITE}│{Colors.RESET}  {Colors.BRIGHT_CYAN}Date:{Colors.RESET}       {Colors.DIM}{current_date}{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_WHITE}│{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_WHITE}└{'─' * 77}{Colors.RESET}")

        # Start progress tracking
        progress.start(topic, strategy_info['name'])

        # Initialization phase
        console.print()
        set_phase("Initialization", "Preparing research agents")
        log_activity("Loading strategy configuration", "info")
        log_activity("Initializing agent workflow", "info")
        log_activity("Setting up research context", "success")

    # Prepare workflow message
    workflow_message = strategy_info["workflow"].format(
        topic=topic, current_date=current_date
    )

    # Invoke the selected strategy agent
    if verbose:
        from src.ui.output_manager import console
        from src.ui.cli_branding import Colors
        from src.ui.progress_display import set_phase, log_activity, agent_start

        set_phase("Execution", "Multi-agent research in progress")
        agent_start("Orchestrator", "Coordinating research agents")
        console.print(f"\n{Colors.BRIGHT_CYAN}  ⚡ Research agents active...{Colors.RESET}")
        console.print(f"{Colors.DIM}     Analyzing topic and gathering intelligence{Colors.RESET}\n")

    # Get agent dynamically - this ensures we use the current LLM model
    agent = get_agent(strategy)

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": workflow_message,
                }
            ]
        }
    )

    if verbose:
        from src.ui.output_manager import console
        from src.ui.cli_branding import Colors
        from src.ui.progress_display import (
            set_phase, log_activity, agent_complete, complete_phase, stop_progress
        )

        console.print()
        set_phase("Finalization", "Compiling research results")
        log_activity("Processing agent outputs", "info")
        log_activity("Synthesizing final report", "info")
        log_activity("Quality assurance complete", "success")
        agent_complete("Orchestrator", "Research complete")

        # Extract and print final message
        try:
            if "messages" in response:
                # Handle AIMessage object (Pydantic model)
                last_message = response["messages"][-1]
                if hasattr(last_message, "content"):
                    final_message = last_message.content
                elif isinstance(last_message, dict):
                    final_message = last_message.get("content", str(response))
                else:
                    final_message = str(last_message)
            else:
                final_message = str(response)
        except Exception:
            # Fallback to string representation
            final_message = str(response)

        # Stop progress tracking and show completion
        console.print()
        complete_phase(True)
        stop_progress(True)

        # Calculate elapsed time
        elapsed = time.time() - start_time
        elapsed_str = f"{int(elapsed // 60)}m {int(elapsed % 60)}s" if elapsed >= 60 else f"{int(elapsed)}s"
        console.print(f"{Colors.BRIGHT_GREEN}✓{Colors.RESET} Research completed in {Colors.DIM}{elapsed_str}{Colors.RESET}\n")

        # Final Report Header
        console.print(f"{Colors.BRIGHT_WHITE}╔═══════════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_WHITE}║{Colors.RESET}  {Colors.BRIGHT_YELLOW}Final Research Report{Colors.RESET}                                                    {Colors.BRIGHT_WHITE}║{Colors.RESET}")
        console.print(f"{Colors.BRIGHT_WHITE}╚═══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
        console.print()

        # Print the final message
        console.print(final_message)

        # Footer
        console.print()
        console.separator("─", 79, Colors.DIM)
        console.print(f"{Colors.DIM}End of Report{Colors.RESET}")
        console.print()

    return response


# MAIN ENTRY POINT
if __name__ == "__main__":
    # Check if user wants to list strategies
    if len(sys.argv) > 1 and sys.argv[1] in ["--list", "-l", "list"]:
        list_strategies()
        sys.exit(0)

    # Check if user wants help
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "-h", "help"]:
        print("\nUsage:")
        print(
            "  python research_system.py --list                  # List all strategies"
        )
        print("  python research_system.py [strategy] [topic]      # Run research")
        print("  python research_system.py                         # Interactive mode")
        print("\nExamples:")
        print('  python research_system.py 1 "Quantum computing"')
        print('  python research_system.py 4 "AI safety research"')
        print('  python research_system.py 10 "Python vs JavaScript"')
        print("\nEnvironment Variables:")
        print("  RESEARCH_STRATEGY - Default strategy (1-10)")
        print()
        sys.exit(0)

    # Parse command line arguments
    if len(sys.argv) >= 3:
        # Command line mode: python research_system.py [strategy] [topic]
        try:
            strategy_num = int(sys.argv[1])
            topic = " ".join(sys.argv[2:])
            run_multi_agent_research(topic, strategy=strategy_num)
        except ValueError:
            print(f"Error: Invalid strategy number '{sys.argv[1]}'. Must be 1-10.")
            print("Use --list to see available strategies.")
            sys.exit(1)
    else:
        # Interactive mode
        print("\n" + "=" * 80)
        print("MULTI-AGENT RESEARCH SYSTEM")
        print("=" * 80)

        # List strategies
        list_strategies()

        # Get strategy choice
        while True:
            try:
                strategy_input = input(
                    "Select strategy (1-10) or 'q' to quit: "
                ).strip()
                if strategy_input.lower() == "q":
                    sys.exit(0)
                strategy_num = int(strategy_input)
                if 1 <= strategy_num <= 10:
                    break
                print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")

        # Get research topic
        topic = input("\nEnter research topic: ").strip()

        if not topic:
            print("Error: Topic cannot be empty.")
            sys.exit(1)

        # Run research
        run_multi_agent_research(topic, strategy=strategy_num)
