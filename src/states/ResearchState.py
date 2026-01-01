from typing import TypedDict, List, Dict, Optional, Literal, Any


class ResearchState(TypedDict):
    """State that flows through the graph."""

    # Core content fields
    topic: str
    research_results: str  # Legacy field - now populated from best_research_content
    code: str
    report: str
    research_done: bool
    report_done: bool
    code_done: bool

    # Parallel research fields (NEW)
    num_research_agents: int  # User-configurable, default 3
    research_reports: List[Dict[str, Any]]  # List of {agent_id, strategy, content, confidence, sources_count}
    critique_scores: Dict[str, float]  # {agent_id: score}
    critique_feedback: Dict[str, str]  # {agent_id: feedback_text}
    selected_report_id: str  # ID of best report
    best_research_content: str  # Content of selected report

    # Enhanced fields for smarter agents
    agent_memory: Dict[str, str]  # Each agent can store context
    key_findings: List[str]  # Accumulate key insights
    questions_raised: List[str]  # Track unanswered questions
    quality_score: Optional[int]  # Quality assessment (1-10)

    # Token tracking for preventing runaway costs
    total_tokens_used: int  # Total tokens consumed across all phases
    tokens_by_phase: Dict[str, int]  # Tokens consumed per phase
    token_budget: int  # Maximum allowed tokens (default 50000)

    # Advanced features
    confidence_scores: Dict[str, float]  # Agent confidence in their outputs (0-1)
    critique_results: Dict[str, Dict]  # Critique results for each phase
    debate_logs: List[Dict]  # Debate history for collaborative refinement

    # Dynamic workflow fields
    workflow_phase: Literal[
        "planning",
        "research",
        "analysis",
        "writing",
        "refinement",
        "validation",
        "completion",
    ]
    quality_thresholds: Dict[str, float]  # Minimum quality for each phase (0-10)
    pending_questions: List[str]  # Questions requiring follow-up
    workflow_history: List[
        Dict[str, str]
    ]  # Track execution path [{action, reason, timestamp}]
    parallel_tasks: List[str]  # Tasks that can execute in parallel
    min_quality_threshold: (
        float  # Minimum quality to proceed (default 3.0, very lenient)
    )
    current_phase_quality: Optional[float]  # Quality of current phase output
    research_error: str
    quality_history: List[
        float
    ]  # Track quality scores over time for diminishing returns detection
    validation_metrics: Dict[
        str, Dict
    ]  # Validation metrics for each phase (research, analysis, writing)

    # Intent detection and routing
    task_intent: Literal["research", "coding", "unknown"]  # Detected task intent
    intent_confidence: float  # Confidence in the detected intent (0-1)
