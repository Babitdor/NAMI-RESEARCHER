"""
Core agent factory functions for the NAMI Multi-Agent Research System.

This module provides factory functions that create research agents dynamically,
ensuring they always use the current LLM configuration (supports /llm command).

The agents are created using:
- Strategy configurations from src.agents.strategies
- Subagent definitions from src.agents.subagent_registry
- Tool sets from src.tools.tool_sets
"""

from deepagents import create_deep_agent

from src.config import get_llm
from src.agents.strategies import STRATEGIES, get_strategy
from src.agents.subagent_registry import SubagentRegistry
from src.tools.tool_sets import ToolSets


# =============================================================================
# Strategy-Driven Agent Creation
# =============================================================================

def create_agent_for_strategy(strategy_id: int):
    """
    Create an agent for a specific strategy using its configuration.

    This is the preferred method for creating agents as it uses the
    declarative strategy configurations.

    Args:
        strategy_id: Strategy number (1-10)

    Returns:
        Configured agent instance
    """
    strategy = get_strategy(strategy_id)

    # Get subagents from registry
    subagents = SubagentRegistry.get_multiple_as_dicts(strategy.subagent_names)

    # Get tools based on strategy
    tools = _get_tools_for_strategy(strategy_id)

    # Format the prompt with iteration limits
    prompt = _format_strategy_prompt(strategy_id, strategy.orchestrator_prompt)

    return create_deep_agent(
        model=get_llm(),
        tools=tools,
        system_prompt=prompt,
        subagents=subagents,  # type: ignore
    )


def _get_tools_for_strategy(strategy_id: int) -> list:
    """Get the appropriate tools for a strategy.

    All strategies include save_report_and_ingest for the COMPLETION phase
    where reports are saved and ingested into the RAG knowledge base.
    """
    strategy_tools = {
        1: ToolSets.ORCHESTRATOR_MINIMAL,       # Includes save_report_and_ingest
        2: ToolSets.ORCHESTRATOR_STANDARD,      # Includes save_report_and_ingest
        3: ToolSets.ORCHESTRATOR_SWARM,         # Includes save_report_and_ingest
        4: ToolSets.ORCHESTRATOR_SWARM,         # Includes save_report_and_ingest
        5: ToolSets.THINKING_WITH_SAVE,         # Thinking + save for delegating orchestrators
        6: ToolSets.THINKING_WITH_SAVE,         # Thinking + save for delegating orchestrators
        7: ToolSets.THINKING_WITH_SAVE,         # Thinking + save for delegating orchestrators
        8: ToolSets.THINKING_WITH_SAVE,         # Thinking + save for delegating orchestrators
        9: ToolSets.ORCHESTRATOR_SWARM,         # Includes save_report_and_ingest
        10: ToolSets.THINKING_WITH_SAVE,        # Thinking + save for delegating orchestrators
    }
    return strategy_tools.get(strategy_id, ToolSets.THINKING_WITH_SAVE)


def _format_strategy_prompt(strategy_id: int, prompt: str) -> str:
    """Format a strategy prompt with iteration limits."""
    format_params = {
        1: {"max_diver_iterations": 3},
        2: {"max_workflow_iterations": 3},
        3: {},  # No params
        4: {"max_swarm_iterations": 2},
        5: {"max_refinement_iterations": 3},
        6: {"max_domain_iterations": 2},
        7: {"max_debate_iterations": 2},
        8: {"max_hierarchical_iterations": 2},
        9: {"max_realtime_iterations": 1},
        10: {"max_comparison_iterations": 2},
    }

    params = format_params.get(strategy_id, {})
    if params:
        return prompt.format(**params)
    return prompt


# =============================================================================
# Legacy Factory Functions (Backward Compatibility)
# These explicit factory functions are kept for backward compatibility
# with existing code that calls them directly.
# =============================================================================

def create_research_orchestrator():
    """Create Strategy 1 - Multi-Agent Research Orchestrator"""
    return create_agent_for_strategy(1)


def create_supervisor_researcher_agent():
    """Create Strategy 2 - Supervisor Researcher Agent"""
    return create_agent_for_strategy(2)


def create_delegation_research_agent():
    """Create Strategy 3 - Delegation Research Agent"""
    return create_agent_for_strategy(3)


def create_parallel_swarm_agent():
    """Create Strategy 4 - Parallel Swarm Research"""
    return create_agent_for_strategy(4)


def create_iterative_refinement_agent():
    """Create Strategy 5 - Iterative Refinement Research"""
    return create_agent_for_strategy(5)


def create_domain_specific_agent():
    """Create Strategy 6 - Domain-Specific Research"""
    return create_agent_for_strategy(6)


def create_debate_research_agent():
    """Create Strategy 7 - Debate-Driven Research"""
    return create_agent_for_strategy(7)


def create_hierarchical_deep_dive():
    """Create Strategy 8 - Hierarchical Deep Dive"""
    return create_agent_for_strategy(8)


def create_realtime_collaborative_agent():
    """Create Strategy 9 - Real-Time Collaborative Research"""
    return create_agent_for_strategy(9)


def create_comparative_research_agent():
    """Create Strategy 10 - Comparative Research"""
    return create_agent_for_strategy(10)


# =============================================================================
# Main Accessor Function
# =============================================================================

def get_agent(strategy_number: int):
    """
    Get or create agent for the given strategy.

    Creates a fresh agent instance using the current LLM model configuration.
    This ensures agents always use the model selected via the /llm command.

    Args:
        strategy_number: Strategy ID (1-10)

    Returns:
        Agent instance for the strategy

    Raises:
        ValueError: If strategy_number is not valid

    Usage:
        agent = get_agent(4)  # Gets Parallel Swarm agent
        result = agent.invoke({"query": "research topic"})
    """
    if strategy_number not in STRATEGIES:
        available = ", ".join(str(k) for k in sorted(STRATEGIES.keys()))
        raise ValueError(
            f"Invalid strategy number: {strategy_number}. "
            f"Available strategies: {available}"
        )

    return create_agent_for_strategy(strategy_number)


# =============================================================================
# Utility Functions
# =============================================================================

def list_available_strategies() -> list:
    """
    List all available research strategies.

    Returns:
        List of dicts with id, name, description for each strategy
    """
    return [
        {
            "id": s.id,
            "name": s.name,
            "description": s.description,
        }
        for s in STRATEGIES.values()
    ]


def get_strategy_info(strategy_id: int) -> dict:
    """
    Get detailed information about a strategy.

    Args:
        strategy_id: Strategy number (1-10)

    Returns:
        Dict with strategy details including subagents
    """
    strategy = get_strategy(strategy_id)
    return {
        "id": strategy.id,
        "name": strategy.name,
        "description": strategy.description,
        "subagents": strategy.subagent_names,
        "max_iterations": strategy.max_iterations,
        "parallel_execution": strategy.parallel_execution,
    }


def clear_agent_cache():
    """
    Clear any cached agent instances.

    Note: With the current implementation, agents are always created fresh,
    so this function exists for API compatibility but has no effect.
    """
    pass  # No-op since we create fresh agents every time


# =============================================================================
# Public API
# =============================================================================

__all__ = [
    # Main accessor
    "get_agent",
    "create_agent_for_strategy",
    # Legacy factory functions
    "create_research_orchestrator",
    "create_supervisor_researcher_agent",
    "create_delegation_research_agent",
    "create_parallel_swarm_agent",
    "create_iterative_refinement_agent",
    "create_domain_specific_agent",
    "create_debate_research_agent",
    "create_hierarchical_deep_dive",
    "create_realtime_collaborative_agent",
    "create_comparative_research_agent",
    # Utility functions
    "list_available_strategies",
    "get_strategy_info",
    "clear_agent_cache",
]
