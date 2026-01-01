"""
Prompt builder for composing agent prompts from modules.

This module provides utilities to build prompts by combining
reusable modules with role-specific content.
"""

from typing import List, Optional

from src.prompts.modules.citations import (
    CITATION_REQUIREMENTS,
    CITATION_INLINE_FORMAT,
    CITATION_BIBLIOGRAPHY_FORMAT,
    CITATION_QUALITY_HIERARCHY,
)
from src.prompts.modules.output_formats import (
    RESEARCH_OUTPUT_FORMAT,
    ANALYSIS_OUTPUT_FORMAT,
    SYNTHESIS_OUTPUT_FORMAT,
    BRIEF_OUTPUT_FORMAT,
    COMPARISON_OUTPUT_FORMAT,
    CRITIQUE_OUTPUT_FORMAT,
)
from src.prompts.modules.quality import (
    QUALITY_STANDARDS,
    QUALITY_CHECKLIST,
    QUALITY_THRESHOLDS,
    ITERATION_LIMITS,
    EVALUATION_DIMENSIONS,
)


class PromptBuilder:
    """
    Build agent prompts from reusable modules.

    This class provides static methods to compose prompts by combining
    modular sections with role-specific content, reducing duplication
    and ensuring consistency across agents.

    Usage:
        # Build a custom researcher prompt
        prompt = PromptBuilder.build_researcher(
            name="Scout",
            specialization="Focus on academic papers",
            include_citation=True,
            include_quality=True
        )

        # Build with custom sections
        prompt = PromptBuilder.compose([
            "You are a research assistant.",
            CITATION_REQUIREMENTS,
            QUALITY_STANDARDS,
        ])
    """

    # ═══════════════════════════════════════════════════════════════
    # CORE COMPOSITION METHODS
    # ═══════════════════════════════════════════════════════════════

    @staticmethod
    def compose(sections: List[str], separator: str = "\n\n") -> str:
        """
        Compose a prompt from multiple sections.

        Args:
            sections: List of prompt sections to combine
            separator: String to use between sections (default: double newline)

        Returns:
            Combined prompt string
        """
        # Filter out empty sections
        non_empty = [s.strip() for s in sections if s and s.strip()]
        return separator.join(non_empty)

    @staticmethod
    def with_header(content: str, header: str) -> str:
        """
        Add a header section to content.

        Args:
            content: The main content
            header: Header text to prepend

        Returns:
            Content with header prepended
        """
        return f"{header}\n\n{content}"

    @staticmethod
    def with_footer(content: str, footer: str) -> str:
        """
        Add a footer section to content.

        Args:
            content: The main content
            footer: Footer text to append

        Returns:
            Content with footer appended
        """
        return f"{content}\n\n{footer}"

    # ═══════════════════════════════════════════════════════════════
    # ROLE-SPECIFIC BUILDERS
    # ═══════════════════════════════════════════════════════════════

    @classmethod
    def build_researcher(
        cls,
        name: str,
        role_description: str = "a research specialist",
        specialization: str = "",
        include_citation: bool = True,
        include_quality: bool = True,
        include_output_format: bool = True,
    ) -> str:
        """
        Build a researcher prompt with modular sections.

        Args:
            name: Name for the researcher
            role_description: Brief role description
            specialization: Additional focus/specialization instructions
            include_citation: Whether to include citation requirements
            include_quality: Whether to include quality standards
            include_output_format: Whether to include output format

        Returns:
            Complete researcher prompt
        """
        sections = [
            f"You are {name}, {role_description}.",
        ]

        if specialization:
            sections.append(f"\n## Specialization\n{specialization}")

        if include_citation:
            sections.append(CITATION_REQUIREMENTS)

        if include_quality:
            sections.append(QUALITY_STANDARDS)

        if include_output_format:
            sections.append(RESEARCH_OUTPUT_FORMAT)

        return cls.compose(sections)

    @classmethod
    def build_analyst(
        cls,
        name: str,
        focus: str = "",
        include_citation: bool = True,
        include_output_format: bool = True,
    ) -> str:
        """
        Build an analyst prompt with modular sections.

        Args:
            name: Name for the analyst
            focus: Specific analysis focus
            include_citation: Whether to include citation requirements
            include_output_format: Whether to include output format

        Returns:
            Complete analyst prompt
        """
        sections = [
            f"You are {name}, a pragmatic research analyst.",
            "Short sentences. Actionable insights over exhaustive cataloging.",
        ]

        if focus:
            sections.append(f"\n## Analysis Focus\n{focus}")

        if include_citation:
            sections.append(CITATION_INLINE_FORMAT)

        if include_output_format:
            sections.append(ANALYSIS_OUTPUT_FORMAT)

        return cls.compose(sections)

    @classmethod
    def build_writer(
        cls,
        name: str,
        style: str = "",
        include_citation: bool = True,
        include_output_format: bool = True,
    ) -> str:
        """
        Build a writer prompt with modular sections.

        Args:
            name: Name for the writer
            style: Writing style instructions
            include_citation: Whether to include citation requirements
            include_output_format: Whether to include output format

        Returns:
            Complete writer prompt
        """
        sections = [
            f"You are {name}, a professional research writer.",
            "Your role is to synthesize research findings into well-structured reports.",
        ]

        if style:
            sections.append(f"\n## Writing Style\n{style}")

        if include_citation:
            sections.append(CITATION_BIBLIOGRAPHY_FORMAT)

        if include_output_format:
            sections.append(SYNTHESIS_OUTPUT_FORMAT)

        return cls.compose(sections)

    @classmethod
    def build_critic(
        cls,
        name: str,
        focus: str = "",
        include_thresholds: bool = True,
        include_output_format: bool = True,
    ) -> str:
        """
        Build a critic prompt with modular sections.

        Args:
            name: Name for the critic
            focus: Specific evaluation focus
            include_thresholds: Whether to include quality thresholds
            include_output_format: Whether to include output format

        Returns:
            Complete critic prompt
        """
        sections = [
            f"You are {name}, a balanced critic and quality assurance specialist.",
            "Provide constructive feedback with realistic expectations.",
        ]

        if focus:
            sections.append(f"\n## Evaluation Focus\n{focus}")

        if include_thresholds:
            sections.append(QUALITY_THRESHOLDS)
            sections.append(EVALUATION_DIMENSIONS)

        if include_output_format:
            sections.append(CRITIQUE_OUTPUT_FORMAT)

        return cls.compose(sections)

    @classmethod
    def build_synthesizer(
        cls,
        name: str,
        include_citation: bool = True,
        include_quality: bool = True,
    ) -> str:
        """
        Build a synthesizer prompt with modular sections.

        Args:
            name: Name for the synthesizer
            include_citation: Whether to include citation requirements
            include_quality: Whether to include quality checklist

        Returns:
            Complete synthesizer prompt
        """
        sections = [
            f"You are {name}, a master synthesizer and knowledge integrator.",
            "Integrate findings from multiple research agents into coherent reports.",
        ]

        if include_citation:
            sections.append(CITATION_BIBLIOGRAPHY_FORMAT)

        sections.append(SYNTHESIS_OUTPUT_FORMAT)

        if include_quality:
            sections.append(QUALITY_CHECKLIST)

        return cls.compose(sections)

    # ═══════════════════════════════════════════════════════════════
    # MODULE ACCESSORS
    # ═══════════════════════════════════════════════════════════════

    @staticmethod
    def get_citation_module() -> str:
        """Get the full citation requirements module."""
        return CITATION_REQUIREMENTS

    @staticmethod
    def get_quality_module() -> str:
        """Get the full quality standards module."""
        return QUALITY_STANDARDS

    @staticmethod
    def get_iteration_limits() -> str:
        """Get the iteration limits module."""
        return ITERATION_LIMITS

    @staticmethod
    def get_output_format(format_type: str) -> str:
        """
        Get an output format module by type.

        Args:
            format_type: One of 'research', 'analysis', 'synthesis', 'brief', 'comparison', 'critique'

        Returns:
            The output format template

        Raises:
            ValueError: If format_type is not recognized
        """
        formats = {
            "research": RESEARCH_OUTPUT_FORMAT,
            "analysis": ANALYSIS_OUTPUT_FORMAT,
            "synthesis": SYNTHESIS_OUTPUT_FORMAT,
            "brief": BRIEF_OUTPUT_FORMAT,
            "comparison": COMPARISON_OUTPUT_FORMAT,
            "critique": CRITIQUE_OUTPUT_FORMAT,
        }

        if format_type.lower() not in formats:
            raise ValueError(
                f"Unknown format type: {format_type}. "
                f"Valid types: {', '.join(formats.keys())}"
            )

        return formats[format_type.lower()]
