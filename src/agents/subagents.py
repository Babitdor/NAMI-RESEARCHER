"""
Subagent definitions for the NAMI Multi-Agent Research System.

This module provides backward-compatible access to subagent configurations.
The actual subagent definitions are now managed by the SubagentRegistry
which uses the SubagentFactory for consistent creation.

For new code, prefer using:
    from src.agents.subagent_registry import SubagentRegistry

    # Get a subagent configuration
    researcher = SubagentRegistry.get("researcher")

    # Get as dict for deepagents
    researcher_dict = SubagentRegistry.get_as_dict("researcher")

For backward compatibility, this module exports the same dict-based
subagent definitions that were previously defined here.
"""

from src.agents.subagent_registry import SubagentRegistry


def _get_dict(name: str) -> dict:
    """Helper to get subagent as dict from registry."""
    return SubagentRegistry.get_as_dict(name)


# ═══════════════════════════════════════════════════════════════════════════
# CORE SUBAGENTS (Backward Compatibility Exports)
# ═══════════════════════════════════════════════════════════════════════════

# Core research roles
research_subagent = _get_dict("researcher")
analyst_subagent = _get_dict("analyst")
writer_subagent = _get_dict("writer")
critic_subagent = _get_dict("critic")

# Specialized research roles
mapper_subagent = _get_dict("mapper")
diver_subagent = _get_dict("diver")
synthesizer_subagent = _get_dict("synthesizer")

# Domain-specific researchers
academic_subagent = _get_dict("researcher-academic")
web_subagent = _get_dict("researcher-industry")  # Maps to industry researcher

# ═══════════════════════════════════════════════════════════════════════════
# STRATEGY 4: PARALLEL SWARM RESEARCH SUBAGENTS
# ═══════════════════════════════════════════════════════════════════════════

researcher_1 = _get_dict("researcher-1")
researcher_2 = _get_dict("researcher-2")
researcher_3 = _get_dict("researcher-3")
consensus_agent = _get_dict("consensus")

# ═══════════════════════════════════════════════════════════════════════════
# STRATEGY 6: DOMAIN-SPECIFIC RESEARCH SUBAGENTS
# ═══════════════════════════════════════════════════════════════════════════

academic_researcher = _get_dict("researcher-academic")
industry_researcher = _get_dict("researcher-industry")
technical_researcher = _get_dict("researcher-technical")

# ═══════════════════════════════════════════════════════════════════════════
# STRATEGY 7: DEBATE-DRIVEN RESEARCH SUBAGENTS
# ═══════════════════════════════════════════════════════════════════════════

researcher_advocate = _get_dict("advocate")
researcher_skeptic = _get_dict("skeptic")
moderator_agent = _get_dict("moderator")
judge_agent = _get_dict("judge")

# ═══════════════════════════════════════════════════════════════════════════
# STRATEGY 8: HIERARCHICAL DEEP DIVE SUBAGENTS
# ═══════════════════════════════════════════════════════════════════════════

# Note: These map to existing specialized researchers
# The hierarchical structure is now handled by strategy configuration
overview_researcher = _get_dict("researcher")
detailed_researcher_1 = _get_dict("researcher-1")
detailed_researcher_2 = _get_dict("researcher-2")
specialist_researcher_1 = _get_dict("researcher-academic")
specialist_researcher_2 = _get_dict("researcher-technical")

# ═══════════════════════════════════════════════════════════════════════════
# STRATEGY 9: REAL-TIME COLLABORATIVE RESEARCH SUBAGENTS
# ═══════════════════════════════════════════════════════════════════════════

live_researcher = _get_dict("live-researcher")
aggregator_agent = _get_dict("aggregator")
brief_writer = _get_dict("brief-writer")

# ═══════════════════════════════════════════════════════════════════════════
# STRATEGY 10: COMPARATIVE RESEARCH SUBAGENTS
# ═══════════════════════════════════════════════════════════════════════════

# Note: For comparisons, we use the general comparison researcher
# The option-specific naming is handled at runtime
researcher_option_a = _get_dict("comparison-researcher")
researcher_option_b = _get_dict("comparison-researcher")
researcher_option_c = _get_dict("comparison-researcher")
comparison_analyst = _get_dict("analyst")
recommendation_agent = _get_dict("recommendation")


# ═══════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════

def get_subagent(name: str) -> dict:
    """
    Get a subagent configuration by name.

    This is the recommended way to get subagent configurations.

    Args:
        name: Name of the subagent

    Returns:
        Dictionary with name, description, system_prompt, tools

    Raises:
        KeyError: If subagent not found
    """
    return SubagentRegistry.get_as_dict(name)


def list_available_subagents() -> list:
    """
    List all available subagent names.

    Returns:
        Sorted list of subagent names
    """
    return SubagentRegistry.list_all()


# Export list for * imports
__all__ = [
    # Core subagents
    "research_subagent",
    "analyst_subagent",
    "writer_subagent",
    "critic_subagent",
    "mapper_subagent",
    "diver_subagent",
    "synthesizer_subagent",
    "academic_subagent",
    "web_subagent",
    # Strategy 4
    "researcher_1",
    "researcher_2",
    "researcher_3",
    "consensus_agent",
    # Strategy 6
    "academic_researcher",
    "industry_researcher",
    "technical_researcher",
    # Strategy 7
    "researcher_advocate",
    "researcher_skeptic",
    "moderator_agent",
    "judge_agent",
    # Strategy 8
    "overview_researcher",
    "detailed_researcher_1",
    "detailed_researcher_2",
    "specialist_researcher_1",
    "specialist_researcher_2",
    # Strategy 9
    "live_researcher",
    "aggregator_agent",
    "brief_writer",
    # Strategy 10
    "researcher_option_a",
    "researcher_option_b",
    "researcher_option_c",
    "comparison_analyst",
    "recommendation_agent",
    # Functions
    "get_subagent",
    "list_available_subagents",
]
