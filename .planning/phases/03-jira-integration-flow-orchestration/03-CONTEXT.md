# Phase 3: Jira Integration & Flow Orchestration - Context

**Gathered:** 2026-05-08
**Status:** Ready for planning
**Source:** discuss-phase

<domain>
## Phase Boundary

This phase delivers two things:

1. **Jira API client** — A real `JiraAdapter` implementation replacing the Phase 1 stub. Fetches ticket data (description, acceptance criteria, comments, linked issues) from Jira Cloud REST API with proper authentication, rate limiting (exponential backoff), and transparent pagination.

2. **Working DeliveryFlow pipeline** — The `DeliveryFlow.run()` method and all 7 stage methods wired up, with flow state persistence for crash recovery and explicit stage-to-stage output passing.

This phase also wires the CLI entry point (`__main__.py`) so `python -m src.dev_workflow PROJ-123` triggers the full pipeline.

</domain>

<decisions>
## Implementation Decisions

### Jira HTTP Client
- **D-01: HTTP library** — `httpx` (sync mode for v1). Async-capable for future phases if needed.
- **D-02: Authentication** — HTTP Basic auth with `JIRA_EMAIL` + `JIRA_API_TOKEN` (base64). Credentials passed via constructor injection: `JiraAdapter(base_url, email, api_token)` — matches existing stub signature.
- **D-03: Rate limiting** — `tenacity` library with exponential backoff. `@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))` on all API calls. Retries on 429 and 5xx responses.
- **D-04: Pagination** — Auto-paginate transparently. `fetch_ticket_comments()` and `fetch_linked_issues()` loop through all pages internally using Jira's `startAt`/`maxResults`/`total` offsets. Callers receive the complete list — no pagination concern leaks through the `JiraPort` interface.

### the Agent's Discretion
- **Flow state persistence** — How `@persist` works, where state is stored, and resume behavior. Agent picks the cleanest approach compatible with CrewAI's `@persist` decorator.
- **CLI output verbosity** — Whether to print per-stage progress or stay silent until done. Agent picks what feels useful for a developer running the tool.
- **Error types and logging** — Structured log format for `logs/{ticket_key}_{timestamp}.log` and execution summary structure. Agent picks based on AUDI-01/02/03 requirements.
- **Connection timeout** — httpx client timeout value (agent picks; 30s is a reasonable default).
- **Page size** — `maxResults` per pagination request (agent picks; 50-100 is typical for Jira).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Jira Cloud REST API
- `.planning/REQUIREMENTS.md` §JIRA-01 through JIRA-05 — All Jira integration requirements
- `.planning/ROADMAP.md` §Phase 3 — Success criteria and phase goal

### Flow Orchestration
- `.planning/REQUIREMENTS.md` §FLOW-01 through FLOW-04 — Flow requirements
- `.planning/REQUIREMENTS.md` §AUDI-01 through AUDI-03 — Audit/logging requirements
- `src/dev_workflow/application/delivery_flow.py` — Existing stub with all 7 stage method signatures to implement

### Existing Contracts (must be preserved)
- `src/dev_workflow/ports/jira_port.py` — JiraPort protocol: `fetch_ticket`, `fetch_ticket_comments`, `fetch_linked_issues` (adapter MUST implement all three)
- `src/dev_workflow/infrastructure/adapters/jira_adapter.py` — Existing stub — Phase 3 replaces stub body
- `src/dev_workflow/infrastructure/config.py` — ConfigLoader with `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_URL`
- `src/dev_workflow/domain/models/jira_ticket.py` — JiraTicket Pydantic model — adapter must populate all fields

No external specs beyond the above — requirements fully captured in decisions.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `ConfigLoader` (infrastructure/config.py) — already loads and validates JIRA_EMAIL, JIRA_API_TOKEN, JIRA_URL. The adapter factory should pull from this.
- `LoggingAdapter` stub (infrastructure/adapters/logging_adapter.py) — implement alongside Phase 3 for AUDI-01/03.
- `JiraAdapter` stub (infrastructure/adapters/jira_adapter.py) — constructor signature `(base_url, email, api_token)` matches D-02 decision. Replace method bodies only.
- `DeliveryFlow` stub (application/delivery_flow.py) — all 7 `_run_*_stage()` method signatures exist. Phase 3 implements the fetch stage + wires the flow.

### Established Patterns
- Pydantic models for all data contracts (Phase 1 decision) — stage outputs must be typed Pydantic models, not raw dicts.
- Constructor injection for dependencies (Phase 2 pattern) — no global state, no singletons.
- Clean architecture layers respected — adapters in infrastructure/, not leaking into domain/.

### Integration Points
- `__main__.py` calls `DeliveryFlow.run(ticket_key)` — must be wired up so the CLI actually invokes the pipeline.
- `JiraAdapter` must formally inherit from `JiraPort` (not just duck-type) — this was flagged in Phase 1 reviews.

</code_context>

<specifics>
## Specific Ideas

- `tenacity` retry should specifically catch HTTP 429 (rate limited) and 5xx responses, not all exceptions — avoid retrying on 4xx auth errors.
- Phase 1 review flagged that `JiraAdapter` doesn't currently inherit from `JiraPort`. Phase 3 must fix this: `class JiraAdapter(JiraPort):`.

</specifics>

<deferred>
## Deferred Ideas

- Async httpx client — async support deferred to future phases if needed
- Jira write-back (posting comments, transitioning tickets) — explicitly out of scope per REQUIREMENTS.md
- Streaming pagination (generator-based) — deferred; transparent auto-pagination is sufficient for v1

</deferred>

---

*Phase: 03-jira-integration-flow-orchestration*
*Context gathered: 2026-05-08 via discuss-phase*
