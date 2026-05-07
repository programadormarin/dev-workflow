# Domain Pitfalls

**Domain:** CrewAI-based Software Delivery Orchestration
**Researched:** 2026-05-07

## Critical Pitfalls

### Pitfall 1: Skipping Structured Outputs (output_pydantic)

**What goes wrong:** Tasks produce unstructured text that downstream tasks cannot reliably parse. The LLM may output JSON that doesn't match expected schema, causing `json.decoder.JSONDecodeError` or Pydantic validation errors.

**Why it happens:** Default task output is raw string. Developers assume LLM will "just work" for JSON output.

**Consequences:**
- Pipeline fails mid-execution
- No type safety between pipeline stages
- Debugging requires reading raw LLM outputs
- Production deployments become unstable

**Prevention:**
```python
# ALWAYS use structured output for inter-stage contracts
class RequirementsAnalysis(BaseModel):
    summary: str
    acceptance_criteria: list[str]

task = Task(
    description="Analyze requirements",
    expected_output="Structured analysis",
    agent=agent,
    output_pydantic=RequirementsAnalysis  # Required!
)
```

**Detection:** Watch for `ValidationError`, `JSONDecodeError` in logs.

---

### Pitfall 2: Missing @CrewBase Decorator

**What goes wrong:** Crew class doesn't load YAML configuration. Deployment fails with "Config not found" or "agents_config not defined".

**Why it happens:** Forgetting to add `@CrewBase` decorator on crew class, or forgetting to define `agents_config` and `tasks_config` class attributes.

**Consequences:**
- Deployment to CrewAI AMP fails
- Local development works but production doesn't
- YAML config is ignored

**Prevention:**
```python
@CrewBase
class RequirementsCrew:
    """Requirements analysis crew"""

    agents_config = "config/agents.yaml"  # Required!
    tasks_config = "config/tasks.yaml"    # Required!

    @agent
    def analyzer(self) -> Agent:
        return Agent(config=self.agents_config['analyzer'], ...)
```

---

### Pitfall 3: Wrong pyproject.toml Type

**What goes wrong:** Flow project declared as `type = "crew"` or vice versa. Deployment succeeds but runtime fails with entry point errors.

**Why it happens:** Copy-pasting from crew template to flow project without updating type.

**Consequences:**
- Build succeeds but automation doesn't start
- Confusing "Entry point not found" errors

**Prevention:**
```toml
# For Flow projects (recommended for production)
[tool.crewai]
type = "flow"

# For standalone Crew projects
[tool.crewai]
type = "crew"
```

---

### Pitfall 4: Breaking Context Chain Between Tasks

**What goes wrong:** Task B doesn't receive output from Task A because `context` parameter wasn't set. Downstream agent works with empty context.

**Why it happens:** Assuming CrewAI automatically passes outputs between all tasks. Sequential process does pass output, but explicit `context` is needed for specific referencing.

**Consequences:**
- Downstream agents make assumptions without data
- Incomplete analysis or implementation
- Silent failures (agent "completes" but with wrong context)

**Prevention:**
```python
# Explicitly pass context when needed
task_a = Task(description="First", agent=agent_a, output_pydantic=OutputA)
task_b = Task(
    description="Second with context",
    agent=agent_b,
    context=[task_a]  # Required to pass task_a's output
)
```

---

### Pitfall 5: No Flow State Persistence (@persist)

**What goes wrong:** Flow crashes mid-execution (e.g., API timeout, LLM rate limit) and restarts from beginning, losing all progress.

**Why it happens:** Forgetting to add `@persist` decorator on Flow class.

**Consequences:**
- Expensive LLM calls repeated
- No recovery from transient failures
- Cannot resume after human intervention

**Prevention:**
```python
from crewai.flow import Flow
from crewai.flow.flow import persist

@persist
class DeliveryFlow(Flow[DeliveryState]):
    # Flow methods...
    pass
```

---

### Pitfall 6: Audit Trail Gaps in Hierarchical Process

**What goes wrong:** Using hierarchical process with manager delegation, but tool call audit logs don't show the delegation chain. Tool calls appear as top-level calls by worker agent.

**Why it happens:** CrewAI's internal task scheduling doesn't propagate agent chain context to tool call audit metadata.

**Consequences:**
- Cannot trace which agent chain led to a tool call
- Security review becomes impossible
- Compliance requirements fail

**Prevention:**
```python
# Use sequential process for audit-sensitive workflows
crew = Crew(
    agents=[...],
    tasks=[...],
    process=Process.sequential  # Preferred for auditability
)
```

---

## Moderate Pitfalls

### Pitfall 7: Hardcoded Credentials

**What goes wrong:** API keys, tokens, or secrets hardcoded in Python files or YAML configs. Accidentally committed to version control.

**Why it happens:** Convenience during development, forgetting to move to .env.

**Consequences:**
- Security breach
- Revoked credentials
- Potential data exposure

**Prevention:**
```python
# GOOD: Use environment variables
api_key = os.getenv("JIRA_API_TOKEN")

# BAD: Hardcoded
api_key = "eyJhbGciOiJIUzI1NiJ9..."
```

---

### Pitfall 8: Missing uv.lock File

**What goes wrong:** Deployment fails during dependency resolution. Works locally but fails on CrewAI AMP.

**Why it happens:** Forgetting to run `uv lock` or not committing `uv.lock`.

**Consequences:**
- Build fails in production
- Non-deterministic dependency resolution

**Prevention:**
```bash
# Always generate and commit lock file
uv lock
git add uv.lock
```

---

### Pitfall 9: Files at Root Instead of src/

**What goes wrong:** Deployment fails with "Entry point not found" or "Module not found".

**Why it happens:** Placing crew.py, main.py at project root instead of `src/project_name/`.

**Consequences:**
- Deployment fails
- Works locally but not in production

**Prevention:**
```
# Correct structure
src/
  project_name/
    main.py
    crew.py

# Wrong - will fail deployment
main.py    # At root!
crew.py    # At root!
```

---

### Pitfall 10: No Task Guardrails

**What goes wrong:** Task produces low-quality output (too short, missing fields) that passes to downstream tasks and causes failures there instead.

**Why it happens:** No validation before task output is accepted.

**Consequences:**
- Cascading failures
- Hard to identify root cause (failure appears in task N but cause is in task N-1)

**Prevention:**
```python
def validate_output(result: TaskOutput) -> Tuple[bool, Any]:
    if not result.pydantic:
        return (False, "No output received")

    if len(result.raw) < 100:
        return (False, "Output too short")

    return (True, None)

task = Task(
    description="Generate report",
    expected_output="Detailed report",
    agent=agent,
    guardrail=validate_output
)
```

---

### Pitfall 11: Mixing Context Windows

**What goes wrong:** LLM receives prompt exceeding context window limit. Tasks fail with "Prompt too long" or truncated outputs.

**Why it happens:** Large context from previous tasks accumulates, or artifacts (code files) are too large.

**Consequences:**
- Task failures mid-pipeline
- Truncated outputs losing critical data

**Prevention:**
- Use `respect_context_window=True` (default)
- Chunk large artifacts
- Monitor token usage
- Use models with appropriate context windows

---

### Pitfall 12: Allow Code Execution Without Security

**What goes wrong:** Agent with code execution tool makes unintended changes to codebase (deletes files, breaks tests).

**Why it happens:** Enabling `allow_code_execution=True` without sandboxing or approval gates.

**Consequences:**
- Data loss
- Broken builds
- Security vulnerabilities

**Prevention:**
```python
# For production, consider:
# 1. Use "safe" mode (default)
# 2. Add human-in-the-loop before code execution
# 3. Use guardrails to validate code changes before applying
agent = Agent(
    role="Implementer",
    allow_code_execution=True,
    code_execution_mode="safe"  # Default: sandboxed
)
```

---

## Minor Pitfalls

### Pitfall 13: Verbose Logging in Production

**What goes wrong:** Excessive logging from `verbose=True` on all agents creates massive logs, costs more, slower execution.

**Why it happens:** Default verbose=True inherited from examples.

**Consequences:**
- High log storage costs
- Slower execution
- Hard to find relevant logs

**Prevention:**
```python
# Set verbose only where needed
agent = Agent(
    config=self.agents_config['researcher'],
    verbose=False  # Default to false in production
)
```

---

### Pitfall 14: No Error Handling in Tools

**What goes wrong:** Tool (Jira, GitHub) fails with network error, whole pipeline stops.

**Why it happens:** No try/except around tool calls, no retry logic.

**Consequences:**
- Single point of failure crashes entire flow
- No graceful degradation

**Prevention:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

class JiraTool:
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_ticket(self, key: str) -> dict:
        # API call with retry
        pass
```

---

### Pitfall 15: Ignoring Token Limits on QA Stage

**What goes wrong:** QA task checks thousands of lines of code, exceeds token limit, truncates analysis.

**Why it happens:** Not chunking or limiting code context.

**Consequences:**
- Incomplete QA checks
- False positives (passed QA but missed issues)

**Prevention:**
- Pass only relevant changed files to QA agent
- Use file filters
- Chunk large codebases

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Foundation | Wrong pyproject.toml type, missing @CrewBase | Follow deployment checklist |
| Agent Definitions | No structured outputs, missing guardrails | Always use output_pydantic |
| Pipeline Implementation | Breaking context chain, audit gaps | Use context=[task], prefer sequential |
| Production Hardening | No @persist, security issues | Add persistence, review tool access |
| QA Stage | Token limit exceeded, no error handling | Chunk code, add retries |

---

## Sources

- [CrewAI Deployment Checklist](https://docs.crewai.com/enterprise/guides/prepare-for-deployment) - HIGH
- [Community: Task Handoffs Audit Trail](https://agenticcontrolplane.com/blog/crewai-task-handoffs-lose-audit-trail) - MEDIUM
- [CrewAI Production Architecture](https://docs.crewai.com/concepts/production-architecture) - HIGH
- [CrewAI Tasks - Guardrails](https://docs.crewai.com/concepts/tasks) - HIGH