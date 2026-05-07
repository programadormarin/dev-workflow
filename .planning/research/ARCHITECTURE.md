# Architecture Patterns

**Domain:** CrewAI-based Software Delivery Orchestration
**Researched:** 2026-05-07

## Recommended Architecture

### Overall Pattern: Flow-First Production Architecture

The production-grade architecture wraps all Crews inside a Flow class for state management, control primitives, and observability.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Flow (Orchestrator)                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  FlowState (Pydantic BaseModel)                         │   │
│  │  - jira_ticket: JiraTicket                               │   │
│  │  - requirements: RequirementsAnalysis                   │   │
│  │  - implementation_plan: ImplementationPlan              │   │
│  │  - qa_results: QAResults                                 │   │
│  │  - pr_url: str                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  @start() → fetch_ticket()                                      │
│     ↓                                                            │
│  @listen(fetch_ticket) → analyze_requirements() [Crew]          │
│     ↓                                                            │
│  @listen(analyze_requirements) → enrich_requirements() [Crew]  │
│     ↓                                                            │
│  @listen(enrich_requirements) → implement_code() [Crew]       │
│     ↓                                                            │
│  @listen(implement_code) → run_qa() [Crew]                      │
│     ↓                                                            │
│  @listen(run_qa) → create_pr() [if QA passes]                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Crew (per stage)                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Agents: [RoleAgent, GoalAgent, BackstoryAgent]        │   │
│  │  Tasks: [Task1, Task2, Task3]                           │   │
│  │  Process: Sequential                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| **Flow** | Pipeline orchestration, state management, stage sequencing | Main.py (kickoff), Crews (kickoff) |
| **DeliveryCrew** | Agent grouping per pipeline stage | Flow (inputs, outputs), YAML configs |
| **Agent** | Specialized role execution with tools | Tasks (assigned), Tools (via tools=) |
| **Task** | Unit of work with output schema | Agents (assigned), Other Tasks (context=) |
| **Tool** | External capability (Jira, GitHub, code execution) | Agents (via tools=) |
| **Pydantic Models** | Data contracts between stages | Flow state, Task output_pydantic |

## Clean Architecture / Hexagonal Architecture for Agent Systems

### Layer Structure

```
┌────────────────────────────────────────────────────────────────┐
│                     Infrastructure Layer                       │
│  (Adapters: Jira API, GitHub CLI, File System, LLM clients)  │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                     Application Layer                           │
│  (Flow orchestration, Crew coordination, Use cases)            │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                       Domain Layer                               │
│  (Pydantic models, Task outputs, Agent roles - pure Python)   │
└────────────────────────────────────────────────────────────────┘
```

### Implementation with Dependency Injection

For testability, use dependency injection to decouple from external systems:

```python
# domain/ports.py - Define contracts (Protocols)
from typing import Protocol

class JiraClient(Protocol):
    def get_ticket(self, ticket_key: str) -> dict: ...
    def get_issues(self, query: str) -> list[dict]: ...

class GitHubClient(Protocol):
    def create_pr(self, title: str, body: str, branch: str) -> str: ...
    def get_diff(self, pr_url: str) -> str: ...

# application/service.py - Depends on ports, not implementations
class DeliveryService:
    def __init__(
        self,
        jira_client: JiraClient,
        github_client: GitHubClient,
        llm: LLM
    ):
        self._jira = jira_client
        self._github = github_client
        self._llm = llm

# infrastructure/adapters.py - Concrete implementations
class JiraRestAdapter:
    def __init__(self, base_url: str, api_token: str, email: str):
        self._client = httpx.Client(auth=(email, api_token))

    def get_ticket(self, ticket_key: str) -> dict:
        # Implementation
        pass

# Wiring (composition root in main.py or dependencies.py)
def get_delivery_service() -> DeliveryService:
    return DeliveryService(
        jira_client=JiraRestAdapter(
            base_url=os.getenv("JIRA_URL"),
            api_token=os.getenv("JIRA_API_TOKEN"),
            email=os.getenv("JIRA_EMAIL")
        ),
        github_client=GhCliAdapter(),  # Uses gh CLI
        llm=LLM(model=os.getenv("MODEL"))
    )
```

### Alternative: Use dioxide for DI (optional)

```python
from dioxide import service, adapter, Profile, Container
from domain.ports import JiraClient, GitHubClient

@service
class DeliveryService:
    def __init__(self, jira: JiraClient, github: GitHubClient):
        self.jira = jira
        self.github = github

@adapter.for_(JiraClient, profile=Profile.PRODUCTION)
class JiraRestAdapter:
    def __init__(self, token: str, email: str):
        ...

@adapter.for_(GitHubClient, profile=Profile.PRODUCTION)
class GhCliAdapter:
    ...

# Auto-wiring based on active profile
container = Container(profile=Profile.PRODUCTION)
service = container.resolve(DeliveryService)
```

## Agent Task Definitions and Output Schemas (Pydantic)

### Structured Output Pattern

Always use `output_pydantic` or `output_json` for inter-agent data passing:

```python
from pydantic import BaseModel
from crewai import Agent, Task

# Domain model for task output
class RequirementsAnalysis(BaseModel):
    summary: str
    acceptance_criteria: list[str]
    edge_cases: list[str]
    technical_considerations: list[str]
    confidence_score: float

# Task with structured output
analyze_task = Task(
    description="""
        Analyze the Jira ticket {ticket_key} for requirements.
        Extract:
        - Summary of the requested change
        - Acceptance criteria
        - Potential edge cases
        - Technical implementation considerations
    """,
    expected_output="A structured analysis with all extracted fields",
    agent=requirements_agent,
    output_pydantic=RequirementsAnalysis,  # Enforces schema
)

# Downstream task uses context
implement_task = Task(
    description="""
        Implement the requirements from {ticket_key}.
        Use the analysis from the previous task to guide implementation.
    """,
    expected_output="Code changes with file paths and descriptions",
    agent=implementation_agent,
    context=[analyze_task],  # Receives analyze_task.output.pydantic
)
```

### Agent Definition with @CrewBase

```python
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class DeliveryCrew:
    """Delivery crew for a single pipeline stage"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def requirements_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['requirements_agent'],
            verbose=True,
            tools=[],  # Add tools here
            output_pydantic=RequirementsAnalysis  # Optional: set on agent too
        )

    @task
    def analyze_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_task'],
            output_pydantic=RequirementsAnalysis
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
```

### YAML Configuration (agents.yaml)

```yaml
requirements_agent:
  role: >
    Senior Requirements Analyst
  goal: >
    Extract clear, complete requirements from Jira tickets with
    acceptance criteria, edge cases, and technical considerations
  backstory: >
    You are an experienced requirements analyst who has worked
    with agile teams for 10+ years. You excel at clarifying vague
    requirements and identifying gaps before implementation.
  allow_delegation: false
  verbose: true
  llm: anthropic/claude-3-sonnet-20240229
```

### YAML Configuration (tasks.yaml)

```yaml
analyze_task:
  description: >
    Analyze Jira ticket {ticket_key} and extract requirements.
    Review the description, acceptance criteria, linked issues,
    and comments. Identify edge cases and technical considerations.
  expected_output: >
    A structured analysis with summary, acceptance criteria,
    edge cases, technical considerations, and confidence score.
  agent: requirements_agent
  output_pydantic: RequirementsAnalysis
```

## Pipeline Stages for Jira → PR Workflow

### Stage Definitions

```python
from crewai.flow import Flow, listen, start
from pydantic import BaseModel
from typing import Optional

# Stage 1: State model
class DeliveryState(BaseModel):
    ticket_key: str = ""
    ticket_data: Optional[dict] = None
    requirements: Optional[RequirementsAnalysis] = None
    enriched_requirements: Optional[EnrichedRequirements] = None
    implementation_plan: Optional[ImplementationPlan] = None
    qa_results: Optional[QAResults] = None
    pr_url: Optional[str] = None
    stage_status: str = "pending"  # pending, running, completed, failed

class DeliveryFlow(Flow[DeliveryState]):
    @start()
    def fetch_ticket(self):
        """Stage 1: Fetch Jira ticket"""
        jira_tool = JiraTool()
        ticket_data = jira_tool.get_ticket(self.state.ticket_key)
        self.state.ticket_data = ticket_data
        self.state.stage_status = "fetched"
        return "Ticket fetched"

    @listen(fetch_ticket)
    def analyze_requirements(self):
        """Stage 2: Analyze requirements"""
        result = RequirementsCrew().crew().kickoff(
            inputs={"ticket_key": self.state.ticket_key}
        )
        self.state.requirements = result.tasks[0].output.pydantic
        self.state.stage_status = "analyzed"
        return "Requirements analyzed"

    @listen(analyze_requirements)
    def enrich_requirements(self):
        """Stage 3: Enrich sparse requirements"""
        result = EnrichmentCrew().crew().kickoff(
            inputs={
                "ticket_key": self.state.ticket_key,
                "analysis": self.state.requirements.model_dump_json()
            }
        )
        self.state.enriched_requirements = result.tasks[0].output.pydantic
        self.state.stage_status = "enriched"
        return "Requirements enriched"

    @listen(enrich_requirements)
    def implement_code(self):
        """Stage 4: Implement code changes"""
        result = ImplementationCrew().crew().kickoff(
            inputs={
                "ticket_key": self.state.ticket_key,
                "requirements": self.state.enriched_requirements.model_dump_json()
            }
        )
        self.state.implementation_plan = result.tasks[0].output.pydantic
        self.state.stage_status = "implemented"
        return "Code implemented"

    @listen(implement_code)
    def run_qa(self):
        """Stage 5: Run QA validation"""
        result = QACrew().crew().kickoff(
            inputs={
                "ticket_key": self.state.ticket_key,
                "implementation": self.state.implementation_plan.model_dump_json()
            }
        )
        self.state.qa_results = result.tasks[0].output.pydantic
        self.state.stage_status = "qa_completed"

        # QA gate: only proceed if passed
        if self.state.qa_results.passed:
            return "QA passed"
        else:
            return "QA failed - review needed"

    @listen(run_qa)
    def create_pr(self):
        """Stage 6: Create PR (only if QA passed)"""
        if not self.state.qa_results.passed:
            self.state.stage_status = "qa_failed"
            return "Skipped - QA failed"

        github_tool = GitHubTool()
        pr_url = github_tool.create_pr(
            title=f"{self.state.ticket_key}: {self.state.enriched_requirements.title}",
            body=self.state.qa_results.summary,
            branch=self.state.implementation_plan.branch_name
        )
        self.state.pr_url = pr_url
        self.state.stage_status = "pr_created"
        return f"PR created: {pr_url}"
```

### Context Passing Between Tasks

```python
# Task B receives output from Task A via context parameter
task_a = Task(
    description="First task",
    expected_output="Output X",
    agent=agent_a,
    output_pydantic=OutputX
)

task_b = Task(
    description="Second task that uses output from first",
    expected_output="Output Y based on Input X",
    agent=agent_b,
    context=[task_a],  # Receives task_a.output.pydantic as context
    output_pydantic=OutputY
)

task_c = Task(
    description="Third task uses outputs from both A and B",
    expected_output="Final output",
    agent=agent_c,
    context=[task_a, task_b]  # Multiple context sources
)
```

## Configuration Management

### Environment Variables (.env)

```env
# Required: Model configuration
MODEL=anthropic/claude-3-sonnet-20240229

# Required: LLM Provider API Key
ANTHROPIC_API_KEY=sk-ant-...

# Jira Configuration
JIRA_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-api-token

# GitHub (uses gh CLI - no API key needed)
# Ensure gh auth is configured: gh auth login

# Optional: Web search for research agents
SERPER_API_KEY=your-serper-key

# Observability
CREWAI_TRACING_ENABLED=true

# Flow persistence
CREWAI_PERSIST_DIR=.crewai-persistence
```

### Configuration Loading Pattern

```python
# src/project_name/config/settings.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    model: str = "anthropic/claude-3-sonnet-20240229"
    jira_url: str
    jira_email: str
    jira_api_token: str
    anthropic_api_key: str = ""
    crewai_tracing_enabled: bool = False

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from .env

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### pyproject.toml Requirements

```toml
[project]
name = "dev-workflow"
version = "0.1.0"
requires-python = ">=3.11"

[tool.crewai]
type = "flow"  # Required for Flow projects

[tool.crewai.flow]
# Flow-specific configuration if needed
```

## Sequential Agent Handoffs with Explicit Outputs

### Sequential Process Pattern

```python
from crewai import Crew, Process

# Sequential: Tasks execute in defined order
# Output of Task N becomes implicit context for Task N+1
delivery_crew = Crew(
    agents=[analyzer, enricher, implementer, qa_reviewer],
    tasks=[analyze_task, enrich_task, implement_task, qa_task],
    process=Process.sequential,  # Linear pipeline
    verbose=True
)
```

### Explicit Output Contract Pattern

```python
# Each task declares its output schema
class AnalysisOutput(BaseModel):
    findings: list[str]
    confidence: float

class ImplementationOutput(BaseModel):
    files_changed: list[str]
    summary: str

class QAOutput(BaseModel):
    passed: bool
    issues: list[str]
    test_results: dict

# Task definitions with explicit schemas
analyze_task = Task(
    description="Analyze requirements",
    expected_output="Analysis with findings and confidence",
    agent=analyzer,
    output_pydantic=AnalysisOutput
)

implement_task = Task(
    description="Implement the feature",
    expected_output="List of files changed",
    agent=implementer,
    output_pydantic=ImplementationOutput
)

qa_task = Task(
    description="Validate implementation",
    expected_output="QA results with pass/fail",
    agent=qa_reviewer,
    output_pydantic=QAOutput
)
```

### Output Access Pattern

```python
# Accessing task outputs after crew execution
result = delivery_crew.kickoff(inputs={"ticket_key": "PROJ-123"})

# Access individual task outputs
analysis_output: AnalysisOutput = result.tasks[0].output.pydantic
implementation_output: ImplementationOutput = result.tasks[1].output.pydantic
qa_output: QAOutput = result.tasks[2].output.pydantic

# Access viaCrewOutput
final_output = result.output.pydantic  # Last task's output
all_task_outputs = result.tasks_output  # List[TaskOutput]
```

### Task Guardrails for Validation

```python
def validate_analysis(result: TaskOutput) -> Tuple[bool, Any]:
    """Validate analysis output meets quality threshold"""
    if not result.pydantic:
        return (False, "No structured output received")

    analysis = result.pydantic
    if analysis.confidence < 0.7:
        return (False, f"Confidence too low: {analysis.confidence}")

    return (True, None)

analyze_task = Task(
    description="Analyze requirements",
    expected_output="Analysis with confidence score",
    agent=analyzer,
    output_pydantic=AnalysisOutput,
    guardrail=validate_analysis  # Validates before passing to next task
)
```

## Recommended Project Layout

### Complete Structure

```
dev-workflow/
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── .env                          # API keys (never commit)
├── .env.example                  # Template for collaborators
├── .dockerignore
├── logs/                         # Execution logs
├── output/                       # Generated artifacts
│   └── pr/
├── .crewai-persistence/          # Flow state (add to .gitignore)
│
└── src/
    └── dev_workflow/
        ├── __init__.py
        ├── main.py               # Flow entry point
        ├── config/
        │   └── settings.py       # Pydantic Settings
        ├── domain/               # Pure domain models
        │   ├── __init__.py
        │   └── models/           # Pydantic schemas for outputs
        │       ├── __init__.py
        │       ├── jira_ticket.py
        │       ├── requirements.py
        │       ├── implementation.py
        │       └── qa_results.py
        ├── ports/                # Protocol definitions (hexagonal)
        │   ├── __init__.py
        │   ├── jira_client.py
        │   └── github_client.py
        ├── application/          # Use cases / orchestration
        │   ├── __init__.py
        │   └── delivery_flow.py  # Main Flow class
        ├── infrastructure/       # Adapters
        │   ├── __init__.py
        │   ├── jira/
        │   │   ├── __init__.py
        │   │   └── rest_adapter.py
        │   └── github/
        │       ├── __init__.py
        │       └── cli_adapter.py
        ├── crews/                # Embedded crews (one per stage)
        │   ├── __init__.py
        │   ├── requirements_crew/
        │   │   ├── __init__.py
        │   │   ├── requirements_crew.py
        │   │   └── config/
        │   │       ├── agents.yaml
        │   │       └── tasks.yaml
        │   ├── enrichment_crew/
        │   │   ├── __init__.py
        │   │   ├── enrichment_crew.py
        │   │   └── config/
        │   │       ├── agents.yaml
        │   │       └── tasks.yaml
        │   ├── implementation_crew/
        │   │   ├── __init__.py
        │   │   ├── implementation_crew.py
        │   │   └── config/
        │   │       ├── agents.yaml
        │   │       └── tasks.yaml
        │   └── qa_crew/
        │       ├── __init__.py
        │       ├── qa_crew.py
        │       └── config/
        │           ├── agents.yaml
        │           └── tasks.yaml
        ├── tools/                # Custom tools
        │   ├── __init__.py
        │   ├── jira_tool.py
        │   ├── github_tool.py
        │   ├── code_execution_tool.py
        │   └── file_writer_tool.py
        └── utils/                # Helpers
            ├── __init__.py
            └── logging.py
```

### Key Principles

1. **Flow in application layer** - Main orchestration in `application/delivery_flow.py`
2. **Domain models in domain layer** - Pure Pydantic, no dependencies
3. **Crews in separate folders** - Each pipeline stage has its own crew with config
4. **Ports define contracts** - Protocols for Jira/GitHub in `ports/`
5. **Adapters implement ports** - Concrete implementations in `infrastructure/`
6. **Tools are separate** - Custom tools in `tools/` directory
7. **Config in YAML** - Agent/task definitions in `config/` subfolder per crew

## Sources

- [CrewAI Production Architecture](https://docs.crewai.com/concepts/production-architecture) - HIGH
- [CrewAI Flows State Management](https://docs.crewai.com/guides/flows/mastering-flow-state) - HIGH
- [CrewAI Tasks - Structured Outputs](https://docs.crewai.com/concepts/tasks) - HIGH
- [CrewAI Sequential Process](https://docs.crewai.com/learn/sequential-process) - HIGH
- [Python Hexagonal Architecture Template](https://github.com/impeller-tech/python-hexagonal-architecture-skeleton) - MEDIUM
- [Dioxide - Python DI Framework](https://dioxide.readthedocs.io/) - MEDIUM
- [Community: CrewAI Task Handoffs](https://agenticcontrolplane.com/blog/crewai-task-handoffs-lose-audit-trail) - MEDIUM (2026)