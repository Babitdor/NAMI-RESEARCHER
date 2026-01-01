"""
Factory for creating subagent configurations.

This module provides factory methods to create subagent configurations
with consistent defaults and reduced code duplication.
"""

from typing import List, Callable, Any, Optional

from src.agents.types import SubagentConfig
from src.tools.tool_sets import ToolSets
from src.prompts.subagent_prompts import (
    RESEARCH_AGENT_PROMPT,
    RESEARCHER_INSTRUCTIONS,
    WRITER_AGENT_PROMPT,
    CRITIC_AGENT_PROMPT,
    ANALYST_AGENT_PROMPT,
    MAPPER_AGENT_PROMPT,
    DIVER_AGENT_PROMPT,
    SYNTHESIZER_AGENT_PROMPT,
)
from src.config import current_date


class SubagentFactory:
    """
    Factory for creating subagent configurations with shared defaults.

    This factory reduces duplication by providing role-specific creation
    methods that apply common patterns and tool sets automatically.

    Usage:
        # Create a basic researcher
        researcher = SubagentFactory.create_researcher("Scout")

        # Create a specialized researcher
        academic = SubagentFactory.create_researcher(
            name="Academic",
            specialization="Focus on peer-reviewed academic papers.",
            tools=ToolSets.RESEARCHER_ACADEMIC
        )

        # Create using the generic method
        critic = SubagentFactory.create(
            role="critic",
            name="Judge",
            description="Evaluates research quality"
        )
    """

    # ═══════════════════════════════════════════════════════════════
    # ROLE-SPECIFIC FACTORY METHODS
    # ═══════════════════════════════════════════════════════════════

    @classmethod
    def create_researcher(
        cls,
        name: str,
        specialization: str = "",
        description: Optional[str] = None,
        tools: Optional[List[Callable[..., Any]]] = None,
    ) -> SubagentConfig:
        """
        Create a researcher subagent configuration.

        Args:
            name: Name for the researcher (e.g., "Scout", "Academic")
            specialization: Additional prompt content for specialization
            description: Custom description (auto-generated if not provided)
            tools: Custom tool list (defaults to full researcher tools)

        Returns:
            SubagentConfig for a researcher subagent
        """
        base_prompt = RESEARCH_AGENT_PROMPT.format(name=name)

        if specialization:
            full_prompt = f"{base_prompt}\n\n{specialization}"
        else:
            full_prompt = base_prompt

        return SubagentConfig(
            name=f"researcher-{name.lower()}",
            description=description
            or f"Research specialist: {specialization or 'general research'}",
            system_prompt=full_prompt,
            tools=tools or ToolSets.RESEARCHER_GENERAL,
        )

    @classmethod
    def create_simple_researcher(
        cls,
        name: str,
        focus: str = "",
        tools: Optional[List[Callable[..., Any]]] = None,
    ) -> SubagentConfig:
        """
        Create a simple researcher using RESEARCHER_INSTRUCTIONS prompt.

        This is a lighter-weight researcher for strategies that don't
        need the full RESEARCH_AGENT_PROMPT.

        Args:
            name: Name for the researcher
            focus: Additional focus instructions
            tools: Custom tool list

        Returns:
            SubagentConfig for a simple researcher
        """
        base_prompt = RESEARCHER_INSTRUCTIONS.format(date=current_date)

        if focus:
            full_prompt = f"{base_prompt}\n\n{focus}"
        else:
            full_prompt = base_prompt

        return SubagentConfig(
            name=name.lower().replace(" ", "-"),
            description=f"Research assistant: {focus or 'general research'}",
            system_prompt=full_prompt,
            tools=tools or ToolSets.RESEARCHER_GENERAL,
        )

    @classmethod
    def create_writer(
        cls,
        name: str = "Writer",
        style: str = "",
        description: Optional[str] = None,
        tools: Optional[List[Callable[..., Any]]] = None,
    ) -> SubagentConfig:
        """
        Create a writer subagent configuration.

        Args:
            name: Name for the writer
            style: Additional style instructions
            description: Custom description
            tools: Custom tool list

        Returns:
            SubagentConfig for a writer subagent
        """
        base_prompt = WRITER_AGENT_PROMPT.format(name=name)

        if style:
            full_prompt = f"{base_prompt}\n\n{style}"
        else:
            full_prompt = base_prompt

        return SubagentConfig(
            name="writer",
            description=description
            or "Creates well-structured research reports with proper citations",
            system_prompt=full_prompt,
            tools=tools or ToolSets.WRITER,
        )

    @classmethod
    def create_critic(
        cls,
        name: str = "Judge",
        focus: str = "",
        description: Optional[str] = None,
        tools: Optional[List[Callable[..., Any]]] = None,
    ) -> SubagentConfig:
        """
        Create a critic subagent configuration.

        Args:
            name: Name for the critic
            focus: Additional evaluation focus
            description: Custom description
            tools: Custom tool list

        Returns:
            SubagentConfig for a critic subagent
        """
        base_prompt = CRITIC_AGENT_PROMPT.format(name=name)

        if focus:
            full_prompt = f"{base_prompt}\n\n{focus}"
        else:
            full_prompt = base_prompt

        return SubagentConfig(
            name="critic",
            description=description
            or "Evaluates research quality and provides constructive feedback",
            system_prompt=full_prompt,
            tools=tools or ToolSets.CRITIC,
        )

    @classmethod
    def create_analyst(
        cls,
        name: str = "Pooch",
        focus: str = "",
        description: Optional[str] = None,
        tools: Optional[List[Callable[..., Any]]] = None,
    ) -> SubagentConfig:
        """
        Create an analyst subagent configuration.

        Args:
            name: Name for the analyst
            focus: Additional analysis focus
            description: Custom description
            tools: Custom tool list

        Returns:
            SubagentConfig for an analyst subagent
        """
        base_prompt = ANALYST_AGENT_PROMPT.format(name=name)

        if focus:
            full_prompt = f"{base_prompt}\n\n{focus}"
        else:
            full_prompt = base_prompt

        return SubagentConfig(
            name="analyst",
            description=description
            or "Analyzes and synthesizes research findings into actionable insights",
            system_prompt=full_prompt,
            tools=tools or ToolSets.ANALYST,
        )

    @classmethod
    def create_mapper(
        cls,
        name: str = "Atlas",
        description: Optional[str] = None,
        tools: Optional[List[Callable[..., Any]]] = None,
    ) -> SubagentConfig:
        """
        Create a mapper subagent configuration.

        Args:
            name: Name for the mapper
            description: Custom description
            tools: Custom tool list

        Returns:
            SubagentConfig for a mapper subagent
        """
        return SubagentConfig(
            name="mapper",
            description=description
            or "Creates topic maps, search strategies, and identifies sub-topics for research",
            system_prompt=MAPPER_AGENT_PROMPT.format(name=name),
            tools=tools or ToolSets.MAPPER,
        )

    @classmethod
    def create_diver(
        cls,
        name: str = "Deep",
        description: Optional[str] = None,
        tools: Optional[List[Callable[..., Any]]] = None,
    ) -> SubagentConfig:
        """
        Create a diver subagent configuration.

        Args:
            name: Name for the diver
            description: Custom description
            tools: Custom tool list

        Returns:
            SubagentConfig for a diver subagent
        """
        return SubagentConfig(
            name="diver",
            description=description
            or "Deep-dives into specific sub-topics with thorough investigation",
            system_prompt=DIVER_AGENT_PROMPT.format(name=name),
            tools=tools or ToolSets.DIVER,
        )

    @classmethod
    def create_synthesizer(
        cls,
        name: str = "Synth",
        description: Optional[str] = None,
        tools: Optional[List[Callable[..., Any]]] = None,
    ) -> SubagentConfig:
        """
        Create a synthesizer subagent configuration.

        Args:
            name: Name for the synthesizer
            description: Custom description
            tools: Custom tool list

        Returns:
            SubagentConfig for a synthesizer subagent
        """
        return SubagentConfig(
            name="synthesizer",
            description=description
            or "Integrates findings into comprehensive, publication-ready reports",
            system_prompt=SYNTHESIZER_AGENT_PROMPT.format(name=name),
            tools=tools or ToolSets.SYNTHESIZER,
        )

    # ═══════════════════════════════════════════════════════════════
    # STRATEGY-SPECIFIC SUBAGENT FACTORIES
    # ═══════════════════════════════════════════════════════════════

    @classmethod
    def create_consensus_agent(cls) -> SubagentConfig:
        """Create a consensus agent for Strategy 4 (Parallel Swarm)."""
        return SubagentConfig(
            name="consensus",
            description="Analyzes findings from multiple researchers, identifies agreement and contradictions",
            system_prompt="""You are a consensus builder and research synthesizer.

Your role is to analyze findings from multiple parallel researchers and:
1. Identify areas of AGREEMENT (findings confirmed by multiple researchers)
2. Identify CONTRADICTIONS (where researchers disagree)
3. Flag UNIQUE FINDINGS (from only one researcher)
4. Assess overall CONFIDENCE based on cross-validation

OUTPUT FORMAT:

## Consensus Analysis

### High Confidence Findings (Confirmed by 2-3 researchers)
- [Finding]: Confirmed by [Researcher X, Researcher Y]
- [Source citations from multiple researchers]

### Medium Confidence Findings (Confirmed by 2 researchers)
- [Finding]: Supported by [Researcher X, Researcher Y]

### Low Confidence Findings (Single source)
- [Finding]: Only found by [Researcher X]
- Note: Requires additional verification

### Contradictions Identified
- **Topic**: [What researchers disagree about]
  - Researcher X says: [Position] [Source]
  - Researcher Y says: [Different position] [Source]
  - Analysis: [Why they might disagree]

### Confidence Scores by Topic
| Topic | Confidence | Reasoning |
|-------|-----------|-----------|
| [Topic 1] | High (3/3) | All researchers agree |
| [Topic 2] | Medium (2/3) | Two confirm, one doesn't mention |

Use your analytical skills to cross-validate claims and build a reliable consensus view.""",
            tools=ToolSets.CONSENSUS,
        )

    @classmethod
    def create_moderator_agent(cls) -> SubagentConfig:
        """Create a moderator agent for Strategy 7 (Debate)."""
        return SubagentConfig(
            name="moderator",
            description="Facilitates structured debate between advocate and skeptic positions",
            system_prompt="""You are a debate moderator ensuring fair, structured discussion.

Your role is to:
1. Present arguments from BOTH sides fairly
2. Identify key points of disagreement
3. Prevent strawman arguments
4. Ensure evidence-based claims
5. Highlight genuine debates in the field

OUTPUT FORMAT:

## Moderated Debate Summary

### Opening Positions

**ADVOCATE Position:**
- Main argument: [Summary]
- Key supporting evidence: [3-5 points with sources]

**SKEPTIC Position:**
- Main argument: [Summary]
- Key counterarguments: [3-5 points with sources]

### Points of Genuine Disagreement

1. **Issue**: [What they disagree about]
   - Advocate view: [Position] [Evidence]
   - Skeptic view: [Position] [Evidence]
   - Assessment: [Why this disagreement exists]

### Areas of Agreement (if any)
- [Where both sides agree despite overall opposition]

### Evidence Quality Assessment

**Advocate's Evidence:**
- Strongest arguments: [Which have best support]
- Weakest arguments: [Which lack strong support]

**Skeptic's Evidence:**
- Strongest arguments: [Which have best support]
- Weakest arguments: [Which lack strong support]

### Fair Representation Check
✓ Both sides given equal space
✓ No strawman arguments
✓ Evidence-based claims only
✓ Genuine disagreements identified

Your goal: Facilitate fair debate, not to pick a winner.""",
            tools=ToolSets.MODERATOR,
        )

    @classmethod
    def create_judge_agent(cls) -> SubagentConfig:
        """Create a judge agent for Strategy 7 (Debate)."""
        base_prompt = CRITIC_AGENT_PROMPT.format(name="Judge")

        specialization = """
DEBATE EVALUATION SPECIALIZATION:

Your role is to assess argument strength, NOT to pick a winner.

Evaluation criteria:
1. **Evidence Quality**: Peer-reviewed > Industry reports > Blog posts
2. **Evidence Strength**: Data and statistics > Case studies > Anecdotes
3. **Logic Soundness**: Valid reasoning without fallacies
4. **Relevance**: Arguments directly address the topic

For each major argument from BOTH sides, assess:
- Evidence quality: [High/Medium/Low]
- Logic soundness: [Valid/Flawed]
- Relevance: [On-topic/Tangential]
- Overall strength: [Strong/Moderate/Weak]

Present balanced assessment showing which arguments have merit regardless of which side presented them."""

        return SubagentConfig(
            name="judge",
            description="Evaluates the strength of arguments from both sides based on evidence quality",
            system_prompt=f"{base_prompt}\n\n{specialization}",
            tools=ToolSets.JUDGE,
        )

    @classmethod
    def create_aggregator_agent(cls) -> SubagentConfig:
        """Create an aggregator agent for Strategy 9 (Real-Time)."""
        return SubagentConfig(
            name="aggregator",
            description="Quickly combines and summarizes findings for real-time intelligence",
            system_prompt="""You are a rapid aggregator for real-time intelligence.

Your role: QUICK summarization, NOT deep analysis

Tasks:
1. Extract key headlines from research findings
2. Identify main themes (2-4 max)
3. Flag urgent or critical information
4. Create concise bullet-point summary

Time limit: 1-2 minutes for your work

OUTPUT FORMAT:

## Quick Summary (2-3 sentences)
[What happened and why it matters]

## Key Points
- [Point 1]
- [Point 2]
- [Point 3]
- [Point 4 if needed]

## Critical/Urgent Info (if any)
- [Flag anything time-sensitive or urgent]

## Main Themes
1. [Theme 1]
2. [Theme 2]

NO deep analysis required - just extract and organize quickly.""",
            tools=ToolSets.AGGREGATOR,
        )

    @classmethod
    def create_recommendation_agent(cls) -> SubagentConfig:
        """Create a recommendation agent for Strategy 10 (Comparative)."""
        return SubagentConfig(
            name="recommendation",
            description="Provides context-specific recommendations based on comparison analysis",
            system_prompt="""You are a recommendation specialist for comparative analysis.

Your role: Provide context-specific recommendations, NOT universal "winners"

Tasks:
1. Identify different use case scenarios
2. Recommend best option for EACH scenario
3. Provide clear reasoning for each recommendation
4. Acknowledge when there's no clear winner

OUTPUT FORMAT:

## Recommendations by Use Case

### Choose Option A if:
- [Condition 1]
- [Condition 2]
- [Condition 3]

### Choose Option B if:
- [Condition 1]
- [Condition 2]
- [Condition 3]

### Choose Option C if:
- [Condition 1]
- [Condition 2]
- [Condition 3]

## Scenario-Based Recommendations

**For beginners:**
Recommendation: [Option X]
Reasoning: [Why]

**For performance-critical applications:**
Recommendation: [Option Y]
Reasoning: [Why]

**For budget-conscious users:**
Recommendation: [Option Z]
Reasoning: [Why]

## Overall Assessment

[If clear winner exists]:
**Winner:** [Option X] is the best choice for [primary scenario] because [reasons].

[If no clear winner]:
**No Clear Winner:** The choice depends on your specific needs. Refer to scenario recommendations above.

Make recommendations evidence-based and context-dependent.""",
            tools=ToolSets.RECOMMENDATION,
        )

    # ═══════════════════════════════════════════════════════════════
    # GENERIC FACTORY METHOD
    # ═══════════════════════════════════════════════════════════════

    @classmethod
    def create(
        cls,
        role: str,
        name: str,
        description: str,
        specialization: str = "",
        tools: Optional[List[Callable[..., Any]]] = None,
    ) -> SubagentConfig:
        """
        Generic factory method for creating any subagent type.

        Args:
            role: Role type (researcher, writer, critic, analyst, mapper, diver, synthesizer)
            name: Name for the subagent
            description: Description for delegation decisions
            specialization: Additional prompt content
            tools: Custom tool list

        Returns:
            SubagentConfig for the specified role

        Raises:
            ValueError: If role is not recognized
        """
        role_lower = role.lower()

        if role_lower in ("researcher", "research"):
            return cls.create_researcher(name, specialization, description, tools)
        elif role_lower == "writer":
            return cls.create_writer(name, specialization, description, tools)
        elif role_lower == "critic":
            return cls.create_critic(name, specialization, description, tools)
        elif role_lower == "analyst":
            return cls.create_analyst(name, specialization, description, tools)
        elif role_lower == "mapper":
            return cls.create_mapper(name, description, tools)
        elif role_lower == "diver":
            return cls.create_diver(name, description, tools)
        elif role_lower == "synthesizer":
            return cls.create_synthesizer(name, description, tools)
        else:
            raise ValueError(
                f"Unknown role: {role}. Valid roles: researcher, writer, critic, analyst, mapper, diver, synthesizer"
            )
