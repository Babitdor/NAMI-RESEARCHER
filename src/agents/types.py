"""
Type definitions for the NAMI Multi-Agent Research System.

This module defines type-safe dataclasses for agent configurations,
ensuring proper validation and clear interfaces.
"""

from dataclasses import dataclass, field
from typing import List, Callable, Any, Optional, Dict


@dataclass
class SubagentConfig:
    """
    Type-safe configuration for a subagent.

    This replaces the plain dict approach with a validated structure
    that ensures all required fields are present and properly typed.

    Attributes:
        name: Unique identifier for the subagent (lowercase, hyphenated)
        description: Brief description for delegation decisions
        system_prompt: The full system prompt for the subagent
        tools: List of tool functions the subagent can use

    Usage:
        config = SubagentConfig(
            name="researcher",
            description="Gathers information from web and academic sources",
            system_prompt=RESEARCH_AGENT_PROMPT.format(name="Scout"),
            tools=[search_tavily, think_tool]
        )

        # Convert to dict for deepagents compatibility
        subagent_dict = config.to_dict()
    """
    name: str
    description: str
    system_prompt: str
    tools: List[Callable[..., Any]]

    def __post_init__(self):
        """Validate the configuration after initialization."""
        if not self.name:
            raise ValueError("Subagent name cannot be empty")
        if not self.description:
            raise ValueError("Subagent description cannot be empty")
        if not self.system_prompt:
            raise ValueError("Subagent system_prompt cannot be empty")

        # Normalize name to lowercase with hyphens
        self.name = self.name.lower().replace(" ", "-").replace("_", "-")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary format for deepagents compatibility.

        Returns:
            Dictionary with name, description, system_prompt, and tools
        """
        return {
            "name": self.name,
            "description": self.description,
            "system_prompt": self.system_prompt,
            "tools": self.tools,
        }

    def with_tools(self, tools: List[Callable[..., Any]]) -> "SubagentConfig":
        """
        Create a copy with different tools.

        Args:
            tools: New list of tools to use

        Returns:
            New SubagentConfig with updated tools
        """
        return SubagentConfig(
            name=self.name,
            description=self.description,
            system_prompt=self.system_prompt,
            tools=tools,
        )

    def with_prompt_suffix(self, suffix: str) -> "SubagentConfig":
        """
        Create a copy with additional prompt content.

        Args:
            suffix: Additional prompt content to append

        Returns:
            New SubagentConfig with extended prompt
        """
        return SubagentConfig(
            name=self.name,
            description=self.description,
            system_prompt=f"{self.system_prompt}\n\n{suffix}",
            tools=self.tools,
        )


@dataclass
class StrategyConfig:
    """
    Configuration for a research strategy.

    Defines the orchestrator prompt, subagent composition, and
    execution parameters for a research strategy.

    Attributes:
        id: Unique strategy number (1-10)
        name: Human-readable strategy name
        description: Brief description of the strategy approach
        orchestrator_prompt: System prompt for the orchestrator agent
        subagent_names: List of subagent names to include (from registry)
        max_iterations: Maximum iteration cycles (default: 3)
        parallel_execution: Whether subagents run in parallel (default: False)
    """
    id: int
    name: str
    description: str
    orchestrator_prompt: str
    subagent_names: List[str]
    max_iterations: int = 3
    parallel_execution: bool = False

    def __post_init__(self):
        """Validate the configuration after initialization."""
        if not 1 <= self.id <= 10:
            raise ValueError(f"Strategy ID must be 1-10, got {self.id}")
        if not self.name:
            raise ValueError("Strategy name cannot be empty")
        if not self.orchestrator_prompt:
            raise ValueError("Strategy orchestrator_prompt cannot be empty")
        if not self.subagent_names:
            raise ValueError("Strategy must have at least one subagent")


@dataclass
class ResearchConfig:
    """
    Runtime configuration for a research execution.

    Combines strategy configuration with runtime parameters
    like the current LLM model and user preferences.

    Attributes:
        strategy: The strategy configuration to use
        topic: Research topic or query
        verbose: Whether to enable verbose output
        save_report: Whether to save the final report
    """
    strategy: StrategyConfig
    topic: str
    verbose: bool = True
    save_report: bool = True
