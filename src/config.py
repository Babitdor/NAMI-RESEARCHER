"""
NAMI Configuration Module

Centralized configuration for the Multi-Agent Research System.
This module manages all settings including LLM configuration, research strategies,
and system parameters.

Usage:
    from src.config import llm, get_llm, update_llm_model, Config

    # Get current LLM instance
    model = get_llm()

    # Update LLM model dynamically (used by /llm command)
    update_llm_model("mistral:latest")
"""

from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os
from datetime import datetime
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Centralized configuration class for NAMI system."""

    # =============================================================================
    # LLM Configuration
    # =============================================================================
    MODEL_NAME = os.getenv("MODEL_NAME", "glm-4.6:cloud")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))

    # =============================================================================
    # Research Configuration
    # =============================================================================
    RESEARCH_STRATEGY = int(os.getenv("RESEARCH_STRATEGY", "4"))
    MAX_CONCURRENT_RESEARCH_UNITS = int(os.getenv("MAX_CONCURRENT_RESEARCH_UNITS", "3"))
    MAX_RESEARCHER_ITERATIONS = int(os.getenv("MAX_RESEARCHER_ITERATIONS", "3"))

    # =============================================================================
    # Strategy-Specific Iteration Limits
    # =============================================================================
    MAX_DIVER_ITERATIONS = int(os.getenv("MAX_DIVER_ITERATIONS", "3"))
    MAX_WORKFLOW_ITERATIONS = int(os.getenv("MAX_WORKFLOW_ITERATIONS", "3"))
    MAX_SWARM_ITERATIONS = int(os.getenv("MAX_SWARM_ITERATIONS", "2"))
    MAX_REFINEMENT_ITERATIONS = int(os.getenv("MAX_REFINEMENT_ITERATIONS", "3"))
    MAX_DOMAIN_ITERATIONS = int(os.getenv("MAX_DOMAIN_ITERATIONS", "2"))
    MAX_DEBATE_ITERATIONS = int(os.getenv("MAX_DEBATE_ITERATIONS", "2"))
    MAX_HIERARCHICAL_ITERATIONS = int(os.getenv("MAX_HIERARCHICAL_ITERATIONS", "2"))
    MAX_REALTIME_ITERATIONS = int(os.getenv("MAX_REALTIME_ITERATIONS", "1"))
    MAX_COMPARISON_ITERATIONS = int(os.getenv("MAX_COMPARISON_ITERATIONS", "2"))

    # =============================================================================
    # UI/Display Configuration
    # =============================================================================
    PERSONA_MODE = os.getenv("PERSONA_MODE", "false").lower() == "true"
    CLI_STYLE = os.getenv("CLI_STYLE", "fancy")
    VERBOSE = os.getenv("VERBOSE", "true").lower() == "true"

    # =============================================================================
    # Advanced Settings
    # =============================================================================
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # =============================================================================
    # API Keys
    # =============================================================================
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    E2B_API_KEY = os.getenv("E2B_API_KEY", "")
    POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "")

    # LangSmith
    LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
    LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "")

    # =============================================================================
    # Directories
    # =============================================================================
    RAG_DIR = os.getenv("RAG_DIR", "./knowledge")

    # =============================================================================
    # System Information
    # =============================================================================
    CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

    @classmethod
    def reload_from_env(cls):
        """Reload configuration from environment variables."""
        load_dotenv(override=True)
        cls.MODEL_NAME = os.getenv("MODEL_NAME", "glm-4.6:cloud")
        cls.TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))
        cls.MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
        cls.RESEARCH_STRATEGY = int(os.getenv("RESEARCH_STRATEGY", "4"))
        # ... reload other configs as needed

    @classmethod
    def get_config_dict(cls) -> dict:
        """Get all configuration as a dictionary."""
        return {
            "model_name": cls.MODEL_NAME,
            "temperature": cls.TEMPERATURE,
            "max_tokens": cls.MAX_TOKENS,
            "research_strategy": cls.RESEARCH_STRATEGY,
            "max_concurrent_units": cls.MAX_CONCURRENT_RESEARCH_UNITS,
            "max_iterations": cls.MAX_RESEARCHER_ITERATIONS,
            "persona_mode": cls.PERSONA_MODE,
            "cli_style": cls.CLI_STYLE,
            "verbose": cls.VERBOSE,
            "debug": cls.DEBUG,
        }


# =============================================================================
# LLM Instance Management
# =============================================================================

# Global LLM instance
_llm_instance: Optional[ChatOllama] = None


def get_llm(
    model: Optional[str] = None,
    temperature: Optional[float] = None,
) -> ChatOllama:
    """
    Get or create LLM instance.

    This function provides a singleton-like pattern for the LLM instance,
    but allows for dynamic reconfiguration when needed (e.g., via /llm command).

    Args:
        model: Model name to use. If None, uses Config.MODEL_NAME or current model.
        temperature: Temperature setting. If None, uses Config.TEMPERATURE.

    Returns:
        ChatOllama instance configured with specified or default parameters.

    Example:
        >>> llm = get_llm()  # Use defaults
        >>> llm = get_llm(model="mistral:latest")  # Override model
        >>> llm = get_llm(temperature=0.7)  # Override temperature

    Note:
        max_tokens parameter not currently supported by ChatOllama.
        Use Config.MAX_TOKENS for reference if needed in future.
    """
    global _llm_instance

    # Determine which model to use
    target_model = model or os.getenv("MODEL_NAME") or Config.MODEL_NAME
    target_temp = temperature if temperature is not None else Config.TEMPERATURE

    # Check if we need to create or recreate the instance
    if _llm_instance is None or model is not None:
        _llm_instance = ChatOllama(
            model=target_model,
            temperature=target_temp,
        )

    return _llm_instance


def update_llm_model(model_name: str) -> ChatOllama:
    """
    Update the LLM model dynamically.

    This is used by the /llm command to switch models without restarting.
    Updates both the environment variable and recreates the LLM instance.

    Args:
        model_name: Name of the new model to use.

    Returns:
        New ChatOllama instance with the updated model.

    Example:
        >>> new_llm = update_llm_model("llama3:latest")
    """
    global _llm_instance

    # Update environment variable for the session
    os.environ["MODEL_NAME"] = model_name
    Config.MODEL_NAME = model_name

    # Create new LLM instance with updated model
    _llm_instance = ChatOllama(
        model=model_name,
        temperature=Config.TEMPERATURE,
    )

    return _llm_instance


def reset_llm():
    """
    Reset LLM instance to use default configuration.

    Forces recreation of the LLM instance with settings from Config.
    """
    global _llm_instance
    _llm_instance = None
    return get_llm()


# =============================================================================
# Legacy/Backward Compatibility
# =============================================================================

# Create default LLM instance for backward compatibility
llm = get_llm()

# Export current_date for backward compatibility
current_date = Config.CURRENT_DATE


# =============================================================================
# Public API
# =============================================================================

__all__ = [
    "Config",
    "get_llm",
    "update_llm_model",
    "reset_llm",
    "llm",  # Legacy support
    "current_date",  # Legacy support
]
