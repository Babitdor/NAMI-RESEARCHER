"""
Strategy configurations for the NAMI Multi-Agent Research System.

This module defines all research strategies as declarative configurations,
making it easy to understand and modify strategy compositions.
"""

from typing import Dict, List
from dataclasses import dataclass

from src.agents.types import StrategyConfig
from src.prompts.core_agent_prompts import (
    STRATEGY_1,
    STRATEGY_2,
    STRATEGY_3,
    STRATEGY_4,
    STRATEGY_5,
    STRATEGY_6,
    STRATEGY_7,
    STRATEGY_8,
    STRATEGY_9,
    STRATEGY_10,
)


# ═══════════════════════════════════════════════════════════════════════════
# STRATEGY DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════

STRATEGIES: Dict[int, StrategyConfig] = {
    1: StrategyConfig(
        id=1,
        name="Multi-Agent Research Orchestrator",
        description=(
            "Sequential workflow: Mapper → Diver → Critic → Synthesizer. "
            "Best for thorough, methodical research with quality checks."
        ),
        orchestrator_prompt=STRATEGY_1,
        subagent_names=["mapper", "diver", "critic", "synthesizer"],
        max_iterations=3,
        parallel_execution=False,
    ),

    2: StrategyConfig(
        id=2,
        name="Supervisor-Researcher Workflow",
        description=(
            "Supervisor directs multiple phases: Research → Analyze → Write. "
            "Best for adaptive, quality-focused research."
        ),
        orchestrator_prompt=STRATEGY_2,
        subagent_names=["researcher", "analyst", "writer", "critic"],
        max_iterations=3,
        parallel_execution=False,
    ),

    3: StrategyConfig(
        id=3,
        name="Delegation Research Agent",
        description=(
            "Simple orchestrator with researcher delegation. "
            "Best for straightforward research queries."
        ),
        orchestrator_prompt=STRATEGY_3,
        subagent_names=["researcher", "writer"],
        max_iterations=3,
        parallel_execution=False,
    ),

    4: StrategyConfig(
        id=4,
        name="Parallel Swarm Research",
        description=(
            "Multiple researchers work in parallel, then consensus building. "
            "Best for comprehensive coverage with cross-validation."
        ),
        orchestrator_prompt=STRATEGY_4,
        subagent_names=[
            "researcher-1",
            "researcher-2",
            "researcher-3",
            "consensus",
            "writer",
        ],
        max_iterations=2,
        parallel_execution=True,
    ),

    5: StrategyConfig(
        id=5,
        name="Iterative Refinement Research",
        description=(
            "Research → Critique → Refine cycles until quality threshold. "
            "Best for high-quality, polished outputs."
        ),
        orchestrator_prompt=STRATEGY_5,
        subagent_names=["researcher", "critic", "writer"],
        max_iterations=3,
        parallel_execution=False,
    ),

    6: StrategyConfig(
        id=6,
        name="Multi-Domain Expert Research",
        description=(
            "Domain specialists provide expert perspectives. "
            "Best for complex topics spanning multiple fields."
        ),
        orchestrator_prompt=STRATEGY_6,
        subagent_names=[
            "domain-expert-1",
            "domain-expert-2",
            "domain-expert-3",
            "domain-synthesizer",
        ],
        max_iterations=2,
        parallel_execution=True,
    ),

    7: StrategyConfig(
        id=7,
        name="Structured Debate Research",
        description=(
            "Advocate vs Skeptic debate with moderation and judgment. "
            "Best for controversial topics needing balanced analysis."
        ),
        orchestrator_prompt=STRATEGY_7,
        subagent_names=["advocate", "skeptic", "moderator", "judge", "writer"],
        max_iterations=2,
        parallel_execution=False,
    ),

    8: StrategyConfig(
        id=8,
        name="Hierarchical Research Network",
        description=(
            "Coordinator manages specialized research teams. "
            "Best for large-scale, multi-faceted research projects."
        ),
        orchestrator_prompt=STRATEGY_8,
        subagent_names=[
            "researcher-academic",
            "researcher-industry",
            "researcher-technical",
            "synthesizer",
        ],
        max_iterations=2,
        parallel_execution=True,
    ),

    9: StrategyConfig(
        id=9,
        name="Real-Time Research",
        description=(
            "Fast, lightweight research for current events. "
            "Best for breaking news and time-sensitive queries."
        ),
        orchestrator_prompt=STRATEGY_9,
        subagent_names=["live-researcher", "aggregator", "brief-writer"],
        max_iterations=1,
        parallel_execution=False,
    ),

    10: StrategyConfig(
        id=10,
        name="Comparative Analysis Research",
        description=(
            "Side-by-side comparison of multiple options/technologies. "
            "Best for decision-making and technology selection."
        ),
        orchestrator_prompt=STRATEGY_10,
        subagent_names=["comparison-researcher", "analyst", "recommendation", "writer"],
        max_iterations=2,
        parallel_execution=False,
    ),
}


# ═══════════════════════════════════════════════════════════════════════════
# STRATEGY ACCESS FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def get_strategy(strategy_id: int) -> StrategyConfig:
    """
    Get a strategy configuration by ID.

    Args:
        strategy_id: Strategy number (1-10)

    Returns:
        StrategyConfig for the specified strategy

    Raises:
        KeyError: If strategy ID is not valid
    """
    if strategy_id not in STRATEGIES:
        available = ", ".join(str(k) for k in sorted(STRATEGIES.keys()))
        raise KeyError(
            f"Strategy {strategy_id} not found. Available: {available}"
        )
    return STRATEGIES[strategy_id]


def list_strategies() -> List[Dict]:
    """
    List all available strategies with their metadata.

    Returns:
        List of dictionaries with id, name, and description
    """
    return [
        {
            "id": s.id,
            "name": s.name,
            "description": s.description,
            "subagents": s.subagent_names,
            "parallel": s.parallel_execution,
        }
        for s in STRATEGIES.values()
    ]


def get_strategy_description(strategy_id: int) -> str:
    """
    Get a human-readable description of a strategy.

    Args:
        strategy_id: Strategy number

    Returns:
        Formatted description string
    """
    strategy = get_strategy(strategy_id)
    return (
        f"Strategy {strategy.id}: {strategy.name}\n"
        f"  {strategy.description}\n"
        f"  Subagents: {', '.join(strategy.subagent_names)}\n"
        f"  Parallel: {strategy.parallel_execution}"
    )


def print_all_strategies() -> None:
    """Print all available strategies to console."""
    print("\n" + "=" * 60)
    print("AVAILABLE RESEARCH STRATEGIES")
    print("=" * 60 + "\n")

    for strategy in STRATEGIES.values():
        print(f"[{strategy.id}] {strategy.name}")
        print(f"    {strategy.description}")
        print(f"    Agents: {', '.join(strategy.subagent_names)}")
        if strategy.parallel_execution:
            print("    Mode: Parallel execution")
        print()


# ═══════════════════════════════════════════════════════════════════════════
# STRATEGY RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════

def recommend_strategy(query: str) -> int:
    """
    Recommend a strategy based on the research query.

    This is a simple heuristic-based recommendation.
    For production, consider using an LLM for better classification.

    Args:
        query: The research query

    Returns:
        Recommended strategy ID
    """
    query_lower = query.lower()

    # Real-time / breaking news
    if any(word in query_lower for word in ["news", "today", "latest", "breaking", "current"]):
        return 9

    # Comparison queries
    if any(word in query_lower for word in ["vs", "versus", "compare", "comparison", "better", "which"]):
        return 10

    # Controversial / debate topics
    if any(word in query_lower for word in ["debate", "controversial", "pros and cons", "should we"]):
        return 7

    # Multi-domain / complex
    if any(word in query_lower for word in ["comprehensive", "all aspects", "multi-disciplinary"]):
        return 6

    # Simple / quick queries
    if len(query.split()) < 5:
        return 3

    # Default: Parallel Swarm for good coverage
    return 4
