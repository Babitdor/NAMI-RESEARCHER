# 🐝 NAMI - Multi-Agent Research Intelligence System

> An advanced AI-powered research assistant featuring 10 specialized research strategies and collaborative multi-agent orchestration.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0-green)](https://github.com/langchain-ai/langgraph)
[![LangChain](https://img.shields.io/badge/LangChain-1.0-blue)](https://github.com/langchain-ai/langchain)

## Overview

NAMI (Named Agent Multi-Agent Intelligence) is a sophisticated research system that leverages LangGraph and LangChain to orchestrate multiple specialized AI agents. With 10 distinct research strategies and a professional CLI interface, NAMI transforms how you conduct research—providing comprehensive, well-structured reports across diverse topics and domains.

Think of NAMI as having a team of specialized researchers, analysts, and writers working collaboratively on your research project—all powered by state-of-the-art AI models.

## Key Features

### 🧠 10 Specialized Research Strategies

NAMI offers 10 unique research strategies, each optimized for different research scenarios:

| # | Strategy | Best For |
|---|----------|----------|
| 1 | **Multi-Agent Orchestrator** | Complex topics requiring structured decomposition and quality assessment |
| 2 | **Supervisor Researcher** | Standard research reports with iterative refinement |
| 3 | **Delegation Research** | Token-efficient research with adaptive parallelization |
| 4 | **Parallel Swarm** | High-confidence findings through cross-validation (default) |
| 5 | **Iterative Refinement** | High-quality reports requiring progressive refinement |
| 6 | **Domain-Specific** | Multi-perspective research combining theory and practice |
| 7 | **Debate-Driven** | Balanced perspectives on controversial or debated topics |
| 8 | **Hierarchical Deep Dive** | Comprehensive documentation from broad to expert-level detail |
| 9 | **Real-Time Collaborative** | Speed-optimized research for breaking news |
| 10 | **Comparative Research** | Evaluating multiple options with recommendations |

### 🎯 Professional CLI Interface

- **Interactive REPL**: Claude Code-inspired interface with slash commands
- **Research History**: Persistent session history for tracking past research
- **Real-time Progress**: Visual indicators and status updates
- **Tab Completion**: Auto-completion for commands and topics
- **Professional Branding**: Clean, colorful terminal output

### ⚙️ Advanced Architecture

- **LangGraph Workflows**: State-of-the-art agent orchestration with LangGraph
- **Dynamic Agent Creation**: Lightweight subagents spawned on-demand
- **Multiple LLM Support**: Ollama, OpenAI, and other compatible models
- **RAG Integration**: Optional knowledge base for cumulative learning
- **MCP Tools**: Model Context Protocol support for extended capabilities

### 📊 Quality Assurance

- **Self-Critique System**: Agents evaluate their work across 5 quality dimensions
- **Confidence Scoring**: Self-assessment based on source quality
- **Iterative Refinement**: Automatic improvement loops until quality threshold is met

## Installation

### Prerequisites

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **Ollama** for local LLM hosting ([Install Ollama](https://ollama.ai/))
- **Git** (optional, for cloning)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd "Winter 2025 Projects/Proj-2 - Multi-Agent"
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install NAMI as a Package (Optional)

```bash
pip install -e .
```

This makes the `nami_research` CLI command available system-wide.

### Step 5: Set Up Ollama

Install and start Ollama, then pull your preferred model:

```bash
# Start Ollama service (in one terminal)
ollama serve

# In a new terminal, pull a model (recommended models)
ollama pull gemini-3-flash-preview:cloud
ollama pull glm-4.6:cloud
ollama pull kimi-k2-thinking:cloud

# Alternative open-source models
ollama pull llama3.1
ollama pull mistral
ollama pull qwen2.5
```

### Step 6: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Required: Tavily API key for web search
TAVILY_API_KEY=your_tavily_api_key_here

# Optional: LLM Configuration (defaults shown)
MODEL_NAME=gemini-3-flash-preview:cloud
TEMPERATURE=0.0
MAX_TOKENS=4096

# Optional: Research Configuration
RESEARCH_STRATEGY=4  # Default strategy (1-10)

# Optional: RAG Configuration
RAG_DIR=./knowledge

# Optional: LangSmith Tracing (for debugging)
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=your_langsmith_key_here
LANGSMITH_PROJECT=nami-research
```

**Get API Keys:**
- Tavily: [https://tavily.com/](https://tavily.com/) - Required for web search
- LangSmith: [https://smith.langchain.com/](https://smith.langchain.com/) - Optional for debugging/tracing

### Step 7: Create Required Directories

```bash
mkdir -p knowledge reports
```

## Quick Start

### Method 1: Using Python Script

```bash
python nami_cli.py
```

### Method 2: Using Installed CLI (if installed with pip install -e .)

```bash
nami_research
```

### Example Research Session

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║    ███╗   ██╗ █████╗ ███╗   ███╗██╗          )))                          ║
║    ████╗  ██║██╔══██╗████╗ ████║██║         (o o)                         ║
║    ██╔██╗ ██║███████║██╔████╔██║██║     ooO--(_)--Ooo                     ║
║    ██║╚██╗██║██╔══██║██║╚██╔╝██║██║         Bee                           ║
║    ██║ ╚████║██║  ██║██║ ╚═╝ ██║██║                                       ║
║    ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝                                       ║
║                                                                           ║
║           Multi-Agent Research Intelligence System                        ║
║                   Powered by LangGraph & Ollama                           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

╭───────────────────────────────────────────────────────────────────────────╮
│  System Mode: STANDARD MODE                                              │
│  Status: Ready                                                            │
╰───────────────────────────────────────────────────────────────────────────╯

---------------------------------------------------------------------------
Tips:
  - Ask research questions for comprehensive reports
  - Request code generation for technical implementations
  - Enable PERSONA_MODE in .env for enhanced workflows
  - Reports are auto-saved to knowledge base for future use
---------------------------------------------------------------------------

🐺 NAMI > What are the latest developments in quantum computing?

[Strategy 4: Parallel Swarm Research]
┌───────────────────────── Agent Team ──────────────────────────┐
│                                                                │
│  🐶 Researcher-1  - Research Agent (Strategy: Comprehensive)  │
│  🐶 Researcher-2  - Research Agent (Strategy: Technical)      │
│  🐶 Researcher-3  - Research Agent (Strategy: Practical)      │
│  🐯 Buddy       - Writer (Report Composer)                     │
│  ⚖️  Judge       - Critic (Quality Assessor)                    │
│                                                                │
└────────────────────────────────────────────────────────────────┘

[Researching...] 3 parallel researchers gathering information...
[Analyzing...] Consensus building and synthesis...
[Writing...] Generating comprehensive report...
[Quality Check...] Assessing report quality...

✓ Research complete!
  Report saved to: reports/Report_20250115_143022.md
  Quality Score: 8.5/10

🐺 NAMI >
```

## CLI Commands

NAMI provides a rich set of slash commands for research and configuration:

### Research Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/research <topic>` | Start a new research session | `/research artificial intelligence in healthcare` |
| `/r <topic>` | Alias for /research | `/r climate change solutions` |

### Configuration Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/strategy <num>` | Change research strategy (1-10) | `/strategy 7` |
| `/llm <model>` | Change LLM model | `/llm mistral:latest` |
| `/config --show` | Display current configuration | `/config --show` |

### Information Commands

| Command | Description |
|---------|-------------|
| `/help` | Display all available commands |
| `/strategies` | List all 10 research strategies |
| `/models` | Show available Ollama models |
| `/about` | Show NAMI version and info |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/history` | Show research session history |
| `/clear` | Clear the terminal screen |
| `/exit` or `/quit` | Exit NAMI |

### Command Examples

```bash
# Research a topic using current strategy
nami> /research latest developments in quantum computing

# Switch to debate-driven strategy for controversial topics
nami> /strategy 7
nami> /research benefits and drawbacks of nuclear energy

# Use a different LLM model
nami> /llm llama3.1:latest
nami> /r machine learning optimization techniques

# View available strategies
nami> /strategies

# Check current configuration
nami> /config --show
```

## Research Strategies

### Strategy 1: Multi-Agent Orchestrator

**Workflow:** Mapper → Diver → Critic → Synthesizer

**Best For:** Complex topics requiring structured decomposition and quality assessment

**Agents:** mapper, diver, critic, synthesizer

**Iterations:** 3

### Strategy 2: Supervisor Researcher

**Workflow:** Supervisor → Research → Analyze → Write → Critic

**Best For:** Standard research reports with iterative refinement

**Agents:** supervisor, researcher, analyst, writer, critic

**Iterations:** 3

### Strategy 3: Delegation Research

**Workflow:** Orchestrator with dynamic subagent delegation

**Best For:** Token-efficient research with adaptive parallelization

**Agents:** orchestrator, researcher, writer

**Iterations:** 3

### Strategy 4: Parallel Swarm *(Default)*

**Workflow:** 3 parallel researchers → Consensus builder → Writer

**Best For:** High-confidence findings through cross-validation

**Agents:** researcher-1, researcher-2, researcher-3, consensus, writer

**Iterations:** 2

### Strategy 5: Iterative Refinement

**Workflow:** Research → Critique → Refine (loop)

**Best For:** High-quality reports requiring progressive refinement

**Agents:** researcher, critic, refiner

**Iterations:** 3

### Strategy 6: Domain-Specific Research

**Workflow:** Academic + Industry + Technical → Synthesizer

**Best For:** Multi-perspective research combining theory and practice

**Agents:** academic-researcher, industry-researcher, technical-researcher, synthesizer

**Iterations:** 2

### Strategy 7: Debate-Driven Research

**Workflow:** Advocate ↔ Skeptic (debate) → Judge → Writer

**Best For:** Balanced perspectives on controversial or debated topics

**Agents:** advocate, skeptic, judge, writer

**Iterations:** 2

### Strategy 8: Hierarchical Deep Dive

**Workflow:** Overview → Detailed → Specialist (3-level hierarchy)

**Best For:** Comprehensive documentation from broad to expert-level detail

**Agents:** overview-researcher, detail-researcher, specialist, synthesizer

**Iterations:** 2

### Strategy 9: Real-Time Collaborative

**Workflow:** Speed-optimized single-pass research with multiple sources

**Best For:** Breaking news, time-sensitive topics

**Agents:** rapid-researcher, fact-checker, writer

**Iterations:** 1

### Strategy 10: Comparative Research

**Workflow:** Research Option A/B/C → Compare → Recommend

**Best For:** Evaluating alternatives and making decisions

**Agents:** researcher-a, researcher-b, researcher-c, comparator, writer

**Iterations:** 2

## Configuration

### Environment Variables

All configuration is managed through the `.env` file:

```bash
# =============================================================================
# LLM Configuration
# =============================================================================
MODEL_NAME=gemini-3-flash-preview:cloud
TEMPERATURE=0.0
MAX_TOKENS=4096

# =============================================================================
# Research Configuration
# =============================================================================
RESEARCH_STRATEGY=4  # Default strategy (1-10)
MAX_CONCURRENT_RESEARCH_UNITS=3

# =============================================================================
# Strategy-Specific Iteration Limits
# =============================================================================
MAX_DIVER_ITERATIONS=3         # Strategy 1
MAX_WORKFLOW_ITERATIONS=3      # Strategy 2
MAX_SWARM_ITERATIONS=2         # Strategy 4
MAX_REFINEMENT_ITERATIONS=3    # Strategy 5
MAX_DOMAIN_ITERATIONS=2        # Strategy 6
MAX_DEBATE_ITERATIONS=2        # Strategy 7
MAX_HIERARCHICAL_ITERATIONS=2  # Strategy 8
MAX_REALTIME_ITERATIONS=1      # Strategy 9
MAX_COMPARISON_ITERATIONS=2    # Strategy 10

# =============================================================================
# UI/Display Configuration
# =============================================================================
CLI_STYLE=fancy  # fancy, simple, ascii
PERSONA_MODE=false

# =============================================================================
# Advanced Settings
# =============================================================================
DEBUG=false
VERBOSE=true
```

### Changing Configuration

**Method 1: Via CLI Commands**
```bash
nami> /strategy 7
nami> /llm mistral:latest
```

**Method 2: Edit .env File**
```bash
# Edit .env
RESEARCH_STRATEGY=7
MODEL_NAME=mistral:latest

# Restart NAMI
python nami_cli.py
```

## Architecture

### Project Structure

```
Proj-2-Multi-Agent/
├── src/
│   ├── agents/
│   │   ├── core_agents.py          # Base agent creation
│   │   ├── research_system.py      # Research orchestration logic
│   │   ├── strategies.py           # Strategy definitions
│   │   ├── subagent_factory.py     # Dynamic subagent creation
│   │   ├── subagent_registry.py    # Agent registration
│   │   ├── subagents.py            # Subagent implementations
│   │   └── types.py                # Type definitions
│   ├── cli/
│   │   ├── commands.py             # CLI command registry
│   │   └── __init__.py
│   ├── config.py                   # Centralized configuration
│   ├── mcps/
│   │   ├── mcp_tools.py            # MCP tool loader
│   │   └── __init__.py
│   ├── prompts/
│   │   ├── core_agent_prompts.py   # Agent system prompts
│   │   └── __init__.py
│   ├── rag/
│   │   └── __init__.py
│   ├── states/
│   │   └── __init__.py
│   ├── tools/
│   │   └── __init__.py
│   ├── ui/
│   │   ├── cli_branding.py         # Terminal styling
│   │   ├── output_manager.py       # Output formatting
│   │   └── __init__.py
│   ├── utils/
│   │   └── __init__.py
│   └── tools_module.py             # Tool exports
├── knowledge/                      # RAG knowledge base
├── reports/                        # Generated research reports
├── nami_cli.py                     # Main entry point
├── pyproject.toml                  # Package configuration
├── requirements.txt                # Python dependencies
├── .env                            # Environment configuration
├── .env.example                    # Environment template
├── CONFIG_USAGE.md                 # Configuration guide
├── LLM_MODEL_SELECTION.md          # LLM selection guide
├── DYNAMIC_MODEL_SWITCHING.md      # Dynamic switching guide
└── README.md                       # This file
```

### System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      NAMI CLI                                │
│                    (nami_cli.py)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     v
         ┌──────────────────────┐
         │   Command Parser     │
         │  (/research, /llm...)│
         └──────────┬───────────┘
                    │
                    v
         ┌──────────────────────┐
         │  Strategy Selector   │
         │   (strategies.py)    │
         └──────────┬───────────┘
                    │
                    v
┌───────────────────────────────────────────┐
│        Research System                     │
│      (research_system.py)                  │
├───────────────────────────────────────────┤
│  1. Create Orchestrator Agent             │
│  2. Spawn Subagents (if needed)           │
│  3. Execute Research Workflow             │
│  4. Quality Assessment (critic)           │
│  5. Iterative Refinement                  │
└──────────────────┬────────────────────────┘
                   │
                   v
         ┌─────────────────────┐
         │   LLM Integration   │
         │ (Ollama/OpenAI/etc) │
         └─────────────────────┘
                   │
                   v
         ┌─────────────────────┐
         │  Save Report (MD)   │
         │  reports/ directory │
         └─────────────────────┘
```

## Troubleshooting

### Common Issues

#### 1. Ollama Connection Error

**Problem:** `Failed to connect to Ollama` or `Connection refused`

**Solution:**
```bash
# Start Ollama service
ollama serve

# Verify it's running in another terminal
curl http://localhost:11434/api/version
```

#### 2. Model Not Found

**Problem:** `Model 'xyz' not found`

**Solution:**
```bash
# Pull the required model
ollama pull gemini-3-flash-preview:cloud

# Verify installed models
ollama list

# Update .env if using a different model
MODEL_NAME=llama3.1
```

#### 3. Missing API Keys

**Problem:** `TAVILY_API_KEY not found` or `Invalid API key`

**Solution:**
1. Get API key from [https://tavily.com/](https://tavily.com/)
2. Add to `.env` file:
   ```bash
   TAVILY_API_KEY=your_key_here
   ```
3. Restart NAMI

#### 4. Slow Research Performance

**Problem:** Research takes too long

**Solutions:**
- Use a faster model: `ollama pull llama3.1`
- Reduce iterations in `.env`:
  ```bash
  MAX_SWARM_ITERATIONS=1
  ```
- Reduce context window:
  ```bash
  MAX_TOKENS=2048
  ```

#### 5. Import Errors

**Problem:** `ModuleNotFoundError: No module named 'src'`

**Solution:**
```bash
# Ensure you're in the project root
cd "Winter 2025 Projects/Proj-2 - Multi-Agent"

# Reinstall in development mode
pip install -e .
```

#### 6. Empty or Poor Quality Reports

**Problem:** Reports are too short or lack depth

**Solutions:**
- Switch to a more thorough strategy: `/strategy 1` or `/strategy 2`
- Increase iterations:
  ```bash
  MAX_SWARM_ITERATIONS=3
  ```
- Use a more capable model: `/llm mistral:latest`
- Enable verbose mode to debug: `DEBUG=true` in `.env`

### Debug Mode

Enable debug logging to troubleshoot issues:

```bash
# In .env
DEBUG=true
VERBOSE=true

# Restart NAMI
python nami_cli.py
```

## Examples

### Research a Technical Topic

```bash
nami> /research Explain transformer architecture in deep learning
```

**Strategy Suggestion:** Strategy 1 (Multi-Agent Orchestrator) or Strategy 8 (Hierarchical Deep Dive)

### Research a Controversial Topic

```bash
nami> /strategy 7
nami> /research Pros and cons of universal basic income
```

**Strategy:** 7 (Debate-Driven) for balanced perspectives

### Fast Research on Breaking News

```bash
nami> /strategy 9
nami> /research Latest developments in AI regulation
```

**Strategy:** 9 (Real-Time Collaborative) for speed

### Compare Multiple Options

```bash
nami> /strategy 10
nami> /research Compare React, Vue, and Angular for enterprise applications
```

**Strategy:** 10 (Comparative Research) for side-by-side evaluation

### Multi-Perspective Research

```bash
nami> /strategy 6
nami> /research Blockchain applications in supply chain management
```

**Strategy:** 6 (Domain-Specific) for academic, industry, and technical views

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **LangChain** - Agent framework
- **LangGraph** - Workflow orchestration
- **Ollama** - Local LLM hosting
- **Tavily** - Web search API

## Additional Documentation

- [CONFIG_USAGE.md](CONFIG_USAGE.md) - Detailed configuration guide
- [LLM_MODEL_SELECTION.md](LLM_MODEL_SELECTION.md) - LLM selection and optimization
- [DYNAMIC_MODEL_SWITCHING.md](DYNAMIC_MODEL_SWITCHING.md) - Runtime model switching

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation in `/docs/`
- Review troubleshooting section above

---

**NAMI: Transforming Research with Collaborative AI Intelligence** 🐝