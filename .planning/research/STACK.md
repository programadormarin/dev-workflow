# Technology Stack

**Project:** CrewAI Jira-Driven Software Delivery Orchestrator
**Researched:** 2026-05-07

## Recommended Stack

### Core Framework

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **CrewAI** | >=0.90.0 | Multi-agent orchestration | Official Flow-first production architecture, sequential/hierarchical processes, built-in state management |
| **Pydantic** | >=2.0 | Data validation & schema | Required for `output_pydantic`, Flow state models, type-safe contracts |
| **python-dotenv** | >=1.0.0 | Environment variable loading | Standard for .env file handling in CrewAI projects |

### Orchestration Components

| Component | Technology | Purpose | Why |
|-----------|------------|---------|-----|
| **Flow** | CrewAI Flow class | Pipeline orchestration | State management, @start/@listen decorators, @persist for recovery |
| **Crew** | CrewAI Crew with @CrewBase | Agent grouping | Config loading from YAML, @agent/@task decorators, process management |
| **LLM** | Per-agent configuration | Language model | Support for OpenAI, Anthropic, Google, Groq, Ollama via environment variables |

### Infrastructure

| Technology | Purpose | Why |
|------------|---------|-----|
| **GitHub CLI (gh)** | PR creation and management | Native authentication, no API key needed for PR operations |
| **Jira Cloud REST API** | Ticket fetching | Standard integration, API token auth (per PROJECT.md out of scope for OAuth) |
| **SQLite (via @persist)** | Flow state persistence | Default CrewAI persistence, supports PostgreSQL for production |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| **crewai-tools** | >=0.10.0 | Pre-built tools for agents | Web search (SerperDevTool), file operations, custom tool wrappers |
| **pytest** | >=8.0 | Testing framework | Required for testability per clean architecture |
| **pytest-asyncio** | >=0.23.0 | Async test support | For testing async crew execution |
| **mypy** | >=1.8.0 | Type checking | Enforce strict typing per PROJECT.md "mypy strict mode" |
| **httpx** | >=0.27.0 | HTTP client | For Jira API calls, GitHub API integration |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Orchestration | CrewAI Flows | LangGraph | CrewAI Flows have 14x less code per DocuSign case study; better for role/task-based workflows |
| State management | CrewAI @persist | Custom Redis | @persist handles recovery automatically; Redis adds complexity |
| Agent definition | YAML + @CrewBase | Pure Python | YAML enables non-developer modification; @CrewBase loads config automatically |
| Config format | .env files | JSON config | CrewAI standard; python-dotenv integration; no hardcoded secrets |

## Installation

```bash
# Core dependencies
pip install "crewai>=0.90.0" "pydantic>=2.0" "python-dotenv>=1.0.0"

# Tools and integrations
pip install "crewai-tools>=0.10.0" "httpx>=0.27.0"

# Development dependencies
pip install -D "pytest>=8.0" "pytest-asyncio>=0.23.0" "mypy>=1.8.0"

# Type stubs
pip install -D "types-python-dotenv"
```

## Project Structure (via crewai create)

```text
project_name/
├── .gitignore
├── pyproject.toml          # Must include [tool.crewai] type = "flow"
├── uv.lock                 # REQUIRED for deployment
├── README.md
├── .env                    # API keys (never commit)
└── src/
    └── project_name/
        ├── __init__.py
        ├── main.py         # Flow class with kickoff()
        ├── crews/          # Embedded crews
        │   └── delivery_crew/
        │       ├── __init__.py
        │       ├── delivery_crew.py  # @CrewBase decorated
        │       └── config/
        │           ├── agents.yaml
        │           └── tasks.yaml
        └── tools/
            ├── __init__.py
            ├── jira_tool.py
            ├── github_tool.py
            └── code_exec_tool.py
```

## Configuration Variables

```env
# Model selection (provider/model-name format)
MODEL=anthropic/claude-3-sonnet-20240229

# LLM Providers (set provider-specific key)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...

# Tool APIs
SERPER_API_KEY=...          # Web search
JIRA_API_TOKEN=...          # Jira Cloud
JIRA_EMAIL=...              # Jira account email

# GitHub (gh CLI handles auth via gh auth)
# No API key needed - uses gh authentication

# Observability
CREWAI_TRACING_ENABLED=true
```

## Sources

- [CrewAI Production Architecture](https://docs.crewai.com/concepts/production-architecture) - HIGH (Official docs, verified with Context7)
- [CrewAI Flows Guide](https://docs.crewai.com/guides/flows/mastering-flow-state) - HIGH (Official docs)
- [CrewAI Tasks - Structured Outputs](https://docs.crewai.com/concepts/tasks) - HIGH (Official docs)
- [CrewAI Deployment Guide](https://docs.crewai.com/enterprise/guides/prepare-for-deployment) - HIGH (Official docs)
- [CrewAI Flows: Production Multi-Agent Guide](https://www.jahanzaib.ai/blog/crewai-flows-production-multi-agent-guide) - MEDIUM (2026, community expert)