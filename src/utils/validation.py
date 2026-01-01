"""
Research Output Validation Module

This module provides validation functions to ensure research phases produce
substantive, useful content before marking them as complete.
"""

import re
from typing import Tuple, List, Dict
import logging

logger = logging.getLogger(__name__)


class ResearchValidator:
    """Validates research output completeness and quality."""

    # Minimum requirements for acceptable research
    MIN_CONTENT_LENGTH = 500  # Minimum character count
    MIN_SOURCES = 2  # Minimum number of sources/URLs
    MIN_FINDINGS = 1  # Minimum number of key findings/insights

    # Patterns to identify content quality indicators
    URL_PATTERN = r'https?://[^\s\)]+|arxiv\.org[^\s\)]+|doi\.org[^\s\)]+'
    FINDING_KEYWORDS = [
        'retrieved insights', 'key concepts identified', 'unearthed papers',
        'found in the wild', 'findings', 'discovered', 'research shows',
        'study found', 'according to', 'reported', 'published'
    ]
    SECTION_MARKERS = [
        'using rag_tool', 'using search_arxiv', 'using search_pubmed',
        'using search_tool', 'search:', 'query:'
    ]

    @staticmethod
    def validate_research_completeness(research_results: str) -> Tuple[bool, str, Dict[str, any]]:
        """
        Validate if research output meets minimum requirements.

        Args:
            research_results: The research output to validate

        Returns:
            Tuple of (is_valid, reason, metrics_dict)
            - is_valid: True if research meets requirements
            - reason: Explanation of validation result
            - metrics_dict: Dictionary of computed metrics
        """
        issues = []
        metrics = {
            'length': 0,
            'sources_count': 0,
            'finding_indicators': 0,
            'section_markers': 0,
            'has_urls': False,
            'has_findings': False,
            'has_structure': False
        }

        # Handle empty or None input
        if not research_results or research_results.strip() == "":
            return False, "Research results are empty", metrics

        # Check 1: Minimum content length
        metrics['length'] = len(research_results)
        if metrics['length'] < ResearchValidator.MIN_CONTENT_LENGTH:
            issues.append(
                f"Content too short ({metrics['length']} chars, minimum {ResearchValidator.MIN_CONTENT_LENGTH})"
            )

        # Check 2: Presence of sources/URLs
        urls = re.findall(ResearchValidator.URL_PATTERN, research_results)
        metrics['sources_count'] = len(urls)
        metrics['has_urls'] = metrics['sources_count'] > 0

        if metrics['sources_count'] < ResearchValidator.MIN_SOURCES:
            issues.append(
                f"Insufficient sources ({metrics['sources_count']} found, minimum {ResearchValidator.MIN_SOURCES})"
            )

        # Check 3: Presence of findings/insights
        research_lower = research_results.lower()
        for keyword in ResearchValidator.FINDING_KEYWORDS:
            if keyword in research_lower:
                metrics['finding_indicators'] += 1

        metrics['has_findings'] = metrics['finding_indicators'] >= ResearchValidator.MIN_FINDINGS

        if not metrics['has_findings']:
            issues.append(
                f"No key findings identified (found {metrics['finding_indicators']} indicators, minimum {ResearchValidator.MIN_FINDINGS})"
            )

        # Check 4: Research structure (tool usage evidence)
        for marker in ResearchValidator.SECTION_MARKERS:
            if marker in research_lower:
                metrics['section_markers'] += 1

        metrics['has_structure'] = metrics['section_markers'] > 0

        if not metrics['has_structure']:
            issues.append("No evidence of research tool usage (missing structure markers)")

        # Check 5: Error messages in output
        error_indicators = ['❌', 'error:', 'failed', 'no results found', 'not found']
        error_count = sum(1 for indicator in error_indicators if indicator in research_lower)

        if error_count >= 3:  # Multiple errors suggest failed research
            issues.append(f"Multiple error messages detected ({error_count} found)")

        # Determine validity
        is_valid = len(issues) == 0

        if is_valid:
            reason = (
                f"✅ Research meets minimum requirements: "
                f"{metrics['length']} chars, {metrics['sources_count']} sources, "
                f"{metrics['finding_indicators']} findings, {metrics['section_markers']} tool sections"
            )
        else:
            reason = "❌ Research incomplete: " + "; ".join(issues)

        logger.info(f"Research validation: {'PASSED' if is_valid else 'FAILED'} - {reason}")

        return is_valid, reason, metrics


    @staticmethod
    def validate_analysis_completeness(analysis: str) -> Tuple[bool, str, Dict[str, any]]:
        """
        Validate if analysis output meets minimum requirements.

        Args:
            analysis: The analysis output to validate

        Returns:
            Tuple of (is_valid, reason, metrics_dict)
        """
        issues = []
        metrics = {
            'length': 0,
            'has_key_findings': False,
            'has_sources': False,
            'has_structure': False,
            'section_count': 0
        }

        if not analysis or analysis.strip() == "":
            return False, "Analysis is empty", metrics

        metrics['length'] = len(analysis)

        # Minimum length check (analysis should be substantive)
        if metrics['length'] < 300:
            issues.append(f"Analysis too brief ({metrics['length']} chars, minimum 300)")

        # Check for analysis sections
        analysis_lower = analysis.lower()
        expected_sections = ['key findings', 'trends', 'patterns', 'statistics', 'data', 'gaps']
        metrics['section_count'] = sum(1 for section in expected_sections if section in analysis_lower)
        metrics['has_structure'] = metrics['section_count'] >= 1

        if not metrics['has_structure']:
            issues.append("Missing analysis structure (no recognizable sections)")

        # Check for sources
        urls = re.findall(ResearchValidator.URL_PATTERN, analysis)
        metrics['has_sources'] = len(urls) > 0

        # Analysis doesn't strictly require sources if it's analyzing provided research
        # but having sources is a good sign

        # Check for key findings
        finding_indicators = ['finding', 'insight', 'shows', 'indicates', 'reveals', 'demonstrates']
        finding_count = sum(1 for indicator in finding_indicators if indicator in analysis_lower)
        metrics['has_key_findings'] = finding_count >= 2

        if not metrics['has_key_findings']:
            issues.append(f"Insufficient analytical insights (found {finding_count} indicators, minimum 2)")

        is_valid = len(issues) == 0

        if is_valid:
            reason = (
                f"✅ Analysis meets requirements: {metrics['length']} chars, "
                f"{metrics['section_count']} sections, {finding_count} insights"
            )
        else:
            reason = "❌ Analysis incomplete: " + "; ".join(issues)

        logger.info(f"Analysis validation: {'PASSED' if is_valid else 'FAILED'} - {reason}")

        return is_valid, reason, metrics


    @staticmethod
    def get_refinement_suggestions(
        phase: str,
        validation_metrics: Dict[str, any]
    ) -> List[str]:
        """
        Generate specific refinement suggestions based on validation metrics.

        Args:
            phase: The phase being validated ('research' or 'analysis')
            validation_metrics: Metrics from validation

        Returns:
            List of specific refinement targets
        """
        suggestions = []

        if phase == "research":
            if validation_metrics.get('sources_count', 0) < 3:
                suggestions.append(
                    "Find and cite at least 3 authoritative sources with URLs"
                )

            if not validation_metrics.get('has_findings'):
                suggestions.append(
                    "Extract and document key findings from sources"
                )

            if not validation_metrics.get('has_structure'):
                suggestions.append(
                    "Use research tools (rag_tool, search_arxiv, search_tool) and document the process"
                )

            if validation_metrics.get('length', 0) < 1000:
                suggestions.append(
                    "Expand research coverage to include more comprehensive information"
                )

        elif phase == "analysis":
            if not validation_metrics.get('has_key_findings'):
                suggestions.append(
                    "Identify and articulate key findings and insights"
                )

            if not validation_metrics.get('has_structure'):
                suggestions.append(
                    "Structure analysis with clear sections (findings, trends, data, gaps)"
                )

            if validation_metrics.get('length', 0) < 500:
                suggestions.append(
                    "Provide more detailed analysis and synthesis"
                )

        return suggestions


    @staticmethod
    def calculate_quality_adjusted_confidence(
        base_confidence: float,
        validation_metrics: Dict[str, any],
        phase: str = "research"
    ) -> float:
        """
        Adjust confidence score based on validation metrics.

        The issue was that confidence was 0.8 even with empty output.
        This function ensures confidence reflects actual content quality.

        Args:
            base_confidence: Initial confidence score from heuristics
            validation_metrics: Metrics from validation
            phase: The phase being validated

        Returns:
            Adjusted confidence score (0.0 - 1.0)
        """
        adjusted_confidence = base_confidence

        if phase == "research":
            # Penalize for missing sources
            if validation_metrics.get('sources_count', 0) == 0:
                adjusted_confidence *= 0.3  # Severe penalty for no sources
            elif validation_metrics.get('sources_count', 0) < ResearchValidator.MIN_SOURCES:
                adjusted_confidence *= 0.6  # Moderate penalty for few sources

            # Penalize for missing findings
            if not validation_metrics.get('has_findings'):
                adjusted_confidence *= 0.5

            # Penalize for missing structure
            if not validation_metrics.get('has_structure'):
                adjusted_confidence *= 0.7

            # Penalize for short content
            length = validation_metrics.get('length', 0)
            if length < 200:
                adjusted_confidence *= 0.2
            elif length < ResearchValidator.MIN_CONTENT_LENGTH:
                adjusted_confidence *= 0.5

        elif phase == "analysis":
            # Penalize for missing key findings
            if not validation_metrics.get('has_key_findings'):
                adjusted_confidence *= 0.5

            # Penalize for missing structure
            if not validation_metrics.get('has_structure'):
                adjusted_confidence *= 0.6

            # Penalize for short content
            length = validation_metrics.get('length', 0)
            if length < 200:
                adjusted_confidence *= 0.3
            elif length < 300:
                adjusted_confidence *= 0.6

        # Clamp to valid range
        return max(0.0, min(1.0, adjusted_confidence))


# Convenience functions for direct use in graph.py
def validate_research(research_results: str) -> Tuple[bool, str, Dict[str, any]]:
    """Convenience function to validate research output."""
    return ResearchValidator.validate_research_completeness(research_results)


def validate_analysis(analysis: str) -> Tuple[bool, str, Dict[str, any]]:
    """Convenience function to validate analysis output."""
    return ResearchValidator.validate_analysis_completeness(analysis)


def adjust_confidence_with_validation(
    base_confidence: float,
    validation_metrics: Dict[str, any],
    phase: str = "research"
) -> float:
    """Convenience function to adjust confidence based on validation."""
    return ResearchValidator.calculate_quality_adjusted_confidence(
        base_confidence, validation_metrics, phase
    )
