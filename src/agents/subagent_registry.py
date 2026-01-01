"""
Central registry for subagent configurations.

This module provides a registry pattern for managing subagent
configurations, enabling consistent access and easy customization.
"""

from typing import Dict, List, Optional, Any

from src.agents.types import SubagentConfig
from src.agents.subagent_factory import SubagentFactory
from src.tools.tool_sets import ToolSets


class SubagentRegistry:
    """
    Central registry for all subagent configurations.

    The registry provides:
    - Registration of subagent configurations
    - Retrieval by name
    - Listing of all registered subagents
    - Lazy initialization with factory defaults

    Usage:
        # Get a registered subagent
        researcher = SubagentRegistry.get("researcher")

        # Get multiple subagents for a strategy
        subagents = SubagentRegistry.get_multiple(["mapper", "diver", "synthesizer"])

        # Register a custom subagent
        SubagentRegistry.register(custom_config)

        # Get as dict for deepagents
        subagent_dict = SubagentRegistry.get_as_dict("researcher")
    """

    # Internal registry storage
    _registry: Dict[str, SubagentConfig] = {}
    _initialized: bool = False

    @classmethod
    def _ensure_initialized(cls) -> None:
        """Initialize the registry with default subagents if not already done."""
        if cls._initialized:
            return

        # Register all base subagents using the factory
        cls._register_defaults()
        cls._initialized = True

    @classmethod
    def _register_defaults(cls) -> None:
        """Register all default subagent configurations."""

        # ═══════════════════════════════════════════════════════════════
        # CORE RESEARCH ROLES
        # ═══════════════════════════════════════════════════════════════

        # General researcher
        cls._registry["researcher"] = SubagentFactory.create_researcher(
            name="Scout",
            specialization="General research across web and academic sources",
        )

        # Academic researcher
        cls._registry["researcher-academic"] = SubagentFactory.create_researcher(
            name="Scholar",
            specialization="Focus on peer-reviewed academic papers and citations",
            tools=ToolSets.RESEARCHER_ACADEMIC,
        )

        # Industry researcher
        cls._registry["researcher-industry"] = SubagentFactory.create_researcher(
            name="Analyst",
            specialization="Focus on industry reports, news, and practical applications",
            tools=ToolSets.RESEARCHER_INDUSTRY,
        )

        # Technical researcher
        cls._registry["researcher-technical"] = SubagentFactory.create_researcher(
            name="Tech",
            specialization="Focus on technical documentation and implementations",
            tools=ToolSets.RESEARCHER_TECHNICAL,
        )

        # Critical researcher
        cls._registry["researcher-critical"] = SubagentFactory.create_researcher(
            name="Skeptic",
            specialization="Focus on finding limitations, criticisms, and counterarguments",
        )

        # ═══════════════════════════════════════════════════════════════
        # SPECIALIZED ROLES
        # ═══════════════════════════════════════════════════════════════

        # Mapper
        cls._registry["mapper"] = SubagentFactory.create_mapper(name="Atlas")

        # Diver
        cls._registry["diver"] = SubagentFactory.create_diver(name="Deep")

        # Synthesizer
        cls._registry["synthesizer"] = SubagentFactory.create_synthesizer(name="Synth")

        # Writer
        cls._registry["writer"] = SubagentFactory.create_writer(name="Scribe")

        # Critic
        cls._registry["critic"] = SubagentFactory.create_critic(name="Judge")

        # Analyst
        cls._registry["analyst"] = SubagentFactory.create_analyst(name="Pooch")

        # ═══════════════════════════════════════════════════════════════
        # STRATEGY-SPECIFIC ROLES
        # ═══════════════════════════════════════════════════════════════

        # Consensus agent (Strategy 4)
        cls._registry["consensus"] = SubagentFactory.create_consensus_agent()

        # Debate agents (Strategy 7)
        cls._registry["moderator"] = SubagentFactory.create_moderator_agent()
        cls._registry["judge"] = SubagentFactory.create_judge_agent()

        # Advocate and Skeptic for debate (Strategy 7)
        cls._registry["advocate"] = SubagentFactory.create_researcher(
            name="Advocate",
            specialization="""You are the ADVOCATE position in a structured debate.

Your role is to present the STRONGEST CASE FOR the topic/technology/approach.

Focus on:
- Benefits and advantages
- Success stories and positive outcomes
- Potential improvements and optimizations
- Evidence supporting adoption/use
- Addressing common criticisms with counterarguments

Present evidence-based arguments, not blind optimism.
Acknowledge valid criticisms but explain why benefits outweigh costs.""",
            description="Presents the strongest case FOR the topic in debates",
        )

        cls._registry["skeptic"] = SubagentFactory.create_researcher(
            name="Skeptic",
            specialization="""You are the SKEPTIC position in a structured debate.

Your role is to present the STRONGEST CASE AGAINST or raise important concerns.

Focus on:
- Limitations and drawbacks
- Failure cases and risks
- Alternative approaches that might be better
- Hidden costs or unintended consequences
- Evidence challenging the main claims

Present evidence-based criticism, not cynicism.
Acknowledge genuine benefits but explain concerns that should be considered.""",
            description="Raises concerns and presents the case against in debates",
        )

        # Real-time agents (Strategy 9)
        cls._registry["live-researcher"] = SubagentFactory.create_simple_researcher(
            name="live-researcher",
            focus="Focus on breaking news, recent developments, and time-sensitive information. Speed over depth.",
            tools=ToolSets.LIVE_RESEARCHER,
        )

        cls._registry["aggregator"] = SubagentFactory.create_aggregator_agent()

        cls._registry["brief-writer"] = SubagentConfig(
            name="brief-writer",
            description="Creates concise intelligence briefs for rapid consumption",
            system_prompt="""You are a brief writer for real-time intelligence.

Create SHORT, ACTIONABLE briefs (200-400 words max).

FORMAT:
## [Topic] - [Timestamp]

**WHAT HAPPENED:**
[1-2 sentences]

**WHY IT MATTERS:**
[1-2 sentences]

**KEY DETAILS:**
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

**SOURCES:**
- [Link 1]
- [Link 2]

**CONFIDENCE:** [High/Medium/Low]
**BASED ON:** [X sources, Y hours old]

NO lengthy analysis. NO extensive background. Just the essentials.""",
            tools=ToolSets.BRIEF_WRITER,
        )

        # Comparison agents (Strategy 10)
        cls._registry["comparison-researcher"] = SubagentFactory.create_researcher(
            name="Comparator",
            specialization="Focus on finding direct comparisons, benchmarks, and side-by-side analyses.",
            tools=ToolSets.COMPARISON_RESEARCHER,
        )

        cls._registry["recommendation"] = SubagentFactory.create_recommendation_agent()

        # ═══════════════════════════════════════════════════════════════
        # NUMBERED RESEARCHERS (for strategies needing multiple)
        # ═══════════════════════════════════════════════════════════════

        # For Strategy 4 (Parallel Swarm)
        for i in range(1, 4):
            focus_areas = [
                "broad coverage across general sources",
                "technical depth and academic rigor",
                "critical analysis and limitations",
            ]
            cls._registry[f"researcher-{i}"] = SubagentFactory.create_simple_researcher(
                name=f"researcher-{i}",
                focus=f"Focus on {focus_areas[i-1]}. Work independently and thoroughly.",
            )

        # For Strategy 6 (Multi-Domain)
        domains = [
            ("domain-expert-1", "technical implementation and engineering perspectives"),
            ("domain-expert-2", "business and market perspectives"),
            ("domain-expert-3", "user experience and adoption perspectives"),
        ]
        for name, domain in domains:
            cls._registry[name] = SubagentFactory.create_researcher(
                name=name,
                specialization=f"Specialize in {domain}. Provide domain-specific insights.",
            )

        # Domain synthesizer
        cls._registry["domain-synthesizer"] = SubagentFactory.create_synthesizer(
            name="Domain-Synth",
            description="Integrates findings from multiple domain experts into unified analysis",
        )

    # ═══════════════════════════════════════════════════════════════
    # PUBLIC API
    # ═══════════════════════════════════════════════════════════════

    @classmethod
    def register(cls, config: SubagentConfig) -> None:
        """
        Register a subagent configuration.

        Args:
            config: SubagentConfig to register

        Note:
            This will overwrite any existing config with the same name.
        """
        cls._ensure_initialized()
        cls._registry[config.name] = config

    @classmethod
    def get(cls, name: str) -> SubagentConfig:
        """
        Get a subagent configuration by name.

        Args:
            name: Name of the subagent

        Returns:
            SubagentConfig for the named subagent

        Raises:
            KeyError: If subagent not found
        """
        cls._ensure_initialized()

        if name not in cls._registry:
            available = ", ".join(sorted(cls._registry.keys()))
            raise KeyError(
                f"Subagent '{name}' not found. Available: {available}"
            )

        return cls._registry[name]

    @classmethod
    def get_as_dict(cls, name: str) -> Dict[str, Any]:
        """
        Get a subagent as a dictionary (for deepagents compatibility).

        Args:
            name: Name of the subagent

        Returns:
            Dictionary with name, description, system_prompt, tools
        """
        return cls.get(name).to_dict()

    @classmethod
    def get_multiple(cls, names: List[str]) -> List[SubagentConfig]:
        """
        Get multiple subagent configurations.

        Args:
            names: List of subagent names

        Returns:
            List of SubagentConfig objects
        """
        return [cls.get(name) for name in names]

    @classmethod
    def get_multiple_as_dicts(cls, names: List[str]) -> List[Dict[str, Any]]:
        """
        Get multiple subagents as dictionaries.

        Args:
            names: List of subagent names

        Returns:
            List of subagent dictionaries
        """
        return [cls.get_as_dict(name) for name in names]

    @classmethod
    def list_all(cls) -> List[str]:
        """
        List all registered subagent names.

        Returns:
            Sorted list of subagent names
        """
        cls._ensure_initialized()
        return sorted(cls._registry.keys())

    @classmethod
    def exists(cls, name: str) -> bool:
        """
        Check if a subagent exists.

        Args:
            name: Name to check

        Returns:
            True if subagent exists
        """
        cls._ensure_initialized()
        return name in cls._registry

    @classmethod
    def reset(cls) -> None:
        """
        Reset the registry to defaults.

        Useful for testing or reloading configurations.
        """
        cls._registry.clear()
        cls._initialized = False
        cls._ensure_initialized()
