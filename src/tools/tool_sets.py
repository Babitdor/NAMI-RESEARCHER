"""
Centralized tool groupings for the NAMI Multi-Agent Research System.

This module defines reusable tool sets that can be assigned to different
agent roles, reducing duplication and ensuring consistent tool access.
"""

from typing import List, Any

# Import all tools from the main tools module
from src.tools_module import (
    search_tavily,
    search_pubmed,
    search_arxiv,
    rag_tool,
    duck_duck_go_search,
    duck_duck_go_search_results,
    wiki_search,
    extract_pdf_content,
    fetch_webpage_content,
    think_tool,
    semantic_scholar_search,
    summarize_text,
    check_grammar,
    save_report_and_ingest,
)


class ToolSets:
    """
    Predefined tool combinations for different agent roles.

    Tool sets are organized by capability and role, making it easy to
    assign consistent tool access to agents without repetition.

    Usage:
        from src.tools.tool_sets import ToolSets

        # Get tools for a researcher role
        tools = ToolSets.RESEARCHER

        # Compose custom tool set
        custom = ToolSets.BASIC_SEARCH + ToolSets.DEEP_READING
    """

    # ═══════════════════════════════════════════════════════════════
    # CORE CAPABILITY GROUPS
    # ═══════════════════════════════════════════════════════════════

    # Basic web search tools
    BASIC_SEARCH: List[Any] = [
        search_tavily,
        duck_duck_go_search,
        duck_duck_go_search_results,
        wiki_search,
    ]

    # Academic/scholarly search tools
    ACADEMIC_SEARCH: List[Any] = [
        search_arxiv,
        search_pubmed,
        semantic_scholar_search,
    ]

    # Deep content extraction tools
    DEEP_READING: List[Any] = [
        extract_pdf_content,
        fetch_webpage_content,
    ]

    # Writing and output tools
    WRITING: List[Any] = [
        summarize_text,
        check_grammar,
        save_report_and_ingest,
    ]

    # Thinking/reflection tools
    THINKING: List[Any] = [
        think_tool,
    ]

    # Thinking tools with report saving capability (for orchestrators that delegate)
    THINKING_WITH_SAVE: List[Any] = [
        think_tool,
        save_report_and_ingest,
    ]

    # Knowledge base tools
    KNOWLEDGE_BASE: List[Any] = [
        rag_tool,
    ]

    # ═══════════════════════════════════════════════════════════════
    # ROLE-BASED TOOL SETS (computed at class definition time)
    # ═══════════════════════════════════════════════════════════════

    # Full research toolkit - web, academic, and deep reading
    RESEARCHER: List[Any] = BASIC_SEARCH + ACADEMIC_SEARCH + DEEP_READING + THINKING + WRITING

    # General researcher - broad web and academic search
    RESEARCHER_GENERAL: List[Any] = BASIC_SEARCH + ACADEMIC_SEARCH + THINKING + WRITING

    # Academic specialist - scholarly sources and PDFs
    RESEARCHER_ACADEMIC: List[Any] = ACADEMIC_SEARCH + DEEP_READING + THINKING + WRITING

    # Industry specialist - web search and content extraction
    RESEARCHER_INDUSTRY: List[Any] = BASIC_SEARCH + DEEP_READING + THINKING + WRITING

    # Technical specialist - documentation and web content
    RESEARCHER_TECHNICAL: List[Any] = [
        search_tavily,
        duck_duck_go_search,
        fetch_webpage_content,
        wiki_search,
        think_tool,
    ]

    # Analyst role - verification and thinking
    ANALYST: List[Any] = [
        wiki_search,
        duck_duck_go_search,
        duck_duck_go_search_results,
        think_tool,
    ]

    # Writer role - text processing and saving
    WRITER: List[Any] = WRITING

    # Critic role - just thinking/reflection
    CRITIC: List[Any] = THINKING

    # Synthesizer role - text processing, thinking, and saving
    SYNTHESIZER: List[Any] = WRITING + THINKING

    # Mapper role - quick search and planning
    MAPPER: List[Any] = [
        think_tool,
        wiki_search,
        duck_duck_go_search,
        duck_duck_go_search_results,
    ]

    # Diver role - comprehensive deep research
    DIVER: List[Any] = RESEARCHER

    # Consensus builder - just thinking
    CONSENSUS: List[Any] = THINKING

    # Debate moderator - just thinking
    MODERATOR: List[Any] = THINKING

    # Debate judge - just thinking
    JUDGE: List[Any] = THINKING

    # Real-time researcher - fast web search only
    LIVE_RESEARCHER: List[Any] = [
        search_tavily,
        duck_duck_go_search,
        duck_duck_go_search_results,
        think_tool,
    ]

    # Aggregator - thinking and summarizing
    AGGREGATOR: List[Any] = [think_tool, summarize_text, save_report_and_ingest]

    # Brief writer - just grammar checking
    BRIEF_WRITER: List[Any] = [check_grammar]

    # Comparison researcher - full research for option analysis
    COMPARISON_RESEARCHER: List[Any] = (
        BASIC_SEARCH + ACADEMIC_SEARCH + [fetch_webpage_content, think_tool]
    )

    # Recommendation agent - just thinking
    RECOMMENDATION: List[Any] = THINKING

    # ═══════════════════════════════════════════════════════════════
    # STRATEGY-SPECIFIC TOOL SETS
    # ═══════════════════════════════════════════════════════════════

    # Minimal orchestrator tools - delegates to subagents
    # Includes save_report_and_ingest for COMPLETION phase
    ORCHESTRATOR_MINIMAL: List[Any] = [
        think_tool,
        duck_duck_go_search,
        wiki_search,
        save_report_and_ingest,
    ]

    # Standard orchestrator tools
    # Includes save_report_and_ingest for COMPLETION phase
    ORCHESTRATOR_STANDARD: List[Any] = [
        search_tavily,
        think_tool,
        duck_duck_go_search,
        wiki_search,
        save_report_and_ingest,
    ]

    # Swarm orchestrator tools
    # Includes save_report_and_ingest for COMPLETION phase
    ORCHESTRATOR_SWARM: List[Any] = [think_tool, search_tavily, save_report_and_ingest]

    # ═══════════════════════════════════════════════════════════════
    # UTILITY METHODS
    # ═══════════════════════════════════════════════════════════════

    @classmethod
    def get_tool_names(cls, tools: List[Any]) -> List[str]:
        """Get the names of tools in a list."""
        return [t.__name__ if hasattr(t, "__name__") else str(t) for t in tools]

    @classmethod
    def combine(cls, *tool_sets: List[Any]) -> List[Any]:
        """Combine multiple tool sets, removing duplicates while preserving order."""
        seen = set()
        result = []
        for tool_set in tool_sets:
            for tool in tool_set:
                if tool not in seen:
                    seen.add(tool)
                    result.append(tool)
        return result
