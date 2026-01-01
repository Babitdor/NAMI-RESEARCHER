"""
Reusable prompt modules for the NAMI Multi-Agent Research System.

This package contains modular prompt sections that can be composed
together to build complete agent prompts without duplication.
"""

from src.prompts.modules.citations import CITATION_REQUIREMENTS
from src.prompts.modules.output_formats import (
    RESEARCH_OUTPUT_FORMAT,
    ANALYSIS_OUTPUT_FORMAT,
    SYNTHESIS_OUTPUT_FORMAT,
)
from src.prompts.modules.quality import (
    QUALITY_STANDARDS,
    QUALITY_CHECKLIST,
    QUALITY_THRESHOLDS,
)

__all__ = [
    "CITATION_REQUIREMENTS",
    "RESEARCH_OUTPUT_FORMAT",
    "ANALYSIS_OUTPUT_FORMAT",
    "SYNTHESIS_OUTPUT_FORMAT",
    "QUALITY_STANDARDS",
    "QUALITY_CHECKLIST",
    "QUALITY_THRESHOLDS",
]
