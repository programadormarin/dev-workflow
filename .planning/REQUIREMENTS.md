# Requirements: CrewAI Jira-Driven Software Delivery Orchestrator

**Defined:** 2026-05-07
**Core Value:** Deliver production-ready code changes from Jira tickets with zero manual intervention between ticket selection and merged PR — with full traceability and audit trail.

## v1 Requirements

### Authentication & Configuration

- [ ] **AUTH-01**: System loads Jira credentials from environment variables (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_URL)
- [ ] **AUTH-02**: System verifies gh CLI authentication before PR operations
- [ ] **AUTH-03**: System validates all required environment variables on startup with clear error messages
- [ ] **AUTH-04**: No hardcoded credentials anywhere in codebase

### Jira Integration

- [ ] **JIRA-01**: User can trigger workflow with Jira ticket key (e.g., `PROJ-123`) via CLI argument
- [ ] **JIRA-02**: System fetches ticket data from Jira Cloud REST API including description, acceptance criteria, comments, and linked issues
- [ ] **JIRA-03**: System extracts all supported issue types (Story, Bug, Task) from configured project
- [ ] **JIRA-04**: System handles Jira API rate limits with exponential backoff retry logic
- [ ] **JIRA-05**: System handles Jira API pagination for tickets with many comments/linked issues

### Requirements Analysis

- [ ] **ANAL-01**: Analysis agent extracts summary, acceptance criteria, edge cases, and technical considerations from ticket data
- [ ] **ANAL-02**: Analysis output is structured via Pydantic model with confidence score
- [ ] **ANAL-03**: System rejects analysis outputs with confidence score below 0.7 threshold

### Requirements Enrichment

- [ ] **ENRI-01**: Enrichment agent identifies gaps in sparse tickets and fills with clarifications
- [ ] **ENRI-02**: Enrichment agent adds edge cases and technical considerations not explicitly stated
- [ ] **ENRI-03**: Enriched requirements output includes title, description, scope, and acceptance criteria
- [ ] **ENRI-04**: Enrichment output is structured via Pydantic model

### Technical Documentation

- [ ] **DOCS-01**: System generates technical documentation (ADR or spec) based on enriched requirements
- [ ] **DOCS-02**: Documentation is written to `output/pr/{ticket_key}/docs/` directory
- [ ] **DOCS-03**: Documentation includes implementation approach, file-level assignments, and success criteria

### Implementation Preparation

- [ ] **IMPL-01**: Implementation agent breaks work into concrete tasks with file-level assignments
- [ ] **IMPL-02**: Implementation plan includes branch naming convention (`{ticket_key}/{short-description}`)
- [ ] **IMPL-03**: Implementation plan includes affected files list
- [ ] **IMPL-04**: Implementation plan output is structured via Pydantic model

### Code Implementation

- [ ] **CODE-01**: Implementation agent executes code changes with clean architecture (domain/ports/infrastructure layers)
- [ ] **CODE-02**: All new code includes full type hints (mypy/pyright compatible)
- [ ] **CODE-03**: Code changes follow existing project patterns and conventions
- [ ] **CODE-04**: Implementation uses Pydantic models for data contracts between modules
- [ ] **CODE-05**: Code execution runs in safe/sandboxed mode (no system-level operations)
- [ ] **CODE-06**: Implementation agent creates branch via git before making changes

### QA Validation

- [ ] **QA-01**: System runs pytest test suite on implemented changes
- [ ] **QA-02**: System enforces minimum coverage threshold (configurable, default 80%)
- [ ] **QA-03**: System runs type checking (mypy strict mode) and fails on errors
- [ ] **QA-04**: System runs linting (ruff or flake8) and fails on errors
- [ ] **QA-05**: QA results include pass/fail status, test count, coverage percentage, type errors, lint errors
- [ ] **QA-06**: QA results output is structured via Pydantic model with passed boolean

### PR Creation

- [ ] **PR-01**: System creates GitHub PR via gh CLI only after QA validation passes
- [ ] **PR-02**: PR title follows format: `{ticket_key}: {short_description}`
- [ ] **PR-03**: PR body includes ticket summary, implementation summary, and QA results
- [ ] **PR-04**: System skips PR creation if QA validation fails, with clear error output
- [ ] **PR-05**: PR is created from feature branch to configured target branch (default: main)

### Flow Orchestration

- [ ] **FLOW-01**: Flow class orchestrates sequential pipeline: Fetch → Analyze → Enrich → Document → Implement → QA → PR
- [ ] **FLOW-02**: Flow state persists via @persist decorator for crash recovery
- [ ] **FLOW-03**: Each stage receives explicit outputs from previous stage via context
- [ ] **FLOW-04**: Flow halts before PR if any stage fails, with clear error message

### Traceability & Audit

- [ ] **AUDI-01**: System logs all pipeline stages with timestamps
- [ ] **AUDI-02**: System generates execution summary with Jira ticket → implementation → PR URL mapping
- [ ] **AUDI-03**: Execution logs written to `logs/{ticket_key}_{timestamp}.log`
- [ ] **AUDI-04**: PR body includes traceability link to Jira ticket

### Project Structure

- [ ] **STRU-01**: Project follows `src/dev_workflow/` layout with `pyproject.toml`
- [ ] **STRU-02**: Domain models in `src/dev_workflow/domain/models/`
- [ ] **STRU-03**: Ports (protocols) in `src/dev_workflow/ports/`
- [ ] **STRU-04**: Infrastructure adapters in `src/dev_workflow/infrastructure/`
- [ ] **STRU-05**: Crews in `src/dev_workflow/crews/` with YAML configs
- [ ] **STRU-06**: Main flow in `src/dev_workflow/application/delivery_flow.py`
- [ ] **STRU-07**: uv.lock file committed for reproducible builds

## v2 Requirements

Deferred to future release.

### Jira Write-back

- **JIRA-WB-01**: System posts comment on Jira ticket with implementation status
- **JIRA-WB-02**: System transitions Jira ticket to configured state on PR merge

### Multi-Repository Support

- **MULTI-01**: System supports PR creation across multiple GitHub repositories
- **MULTI-02**: System maps tickets to target repositories via configuration

### Observability

- **OBS-01**: System sends traces to LangSmith for debugging
- **OBS-02**: System exposes Prometheus metrics for pipeline duration

### Human-in-the-Loop

- **HITL-01**: System pauses before PR creation for human approval
- **HITL-02**: System allows human to review and modify implementation before QA

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Jira OAuth 2.0 | API token sufficient for v1; OAuth adds complexity |
| GitLab support | GitHub only per user requirement |
| Visual UI/dashboard | CLI-driven workflow; dashboard adds significant complexity |
| Multi-repository PRs | Single repository at a time; multi-repo requires separate workflow |
| Jira write-back | Read-only integration for v1; write-back adds state management complexity |
| Direct code execution without sandboxing | Security risk; safe mode enforced |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUTH-01 | Phase 2 | Pending |
| AUTH-02 | Phase 2 | Pending |
| AUTH-03 | Phase 2 | Pending |
| AUTH-04 | Phase 2 | Pending |
| JIRA-01 | Phase 3 | Pending |
| JIRA-02 | Phase 3 | Pending |
| JIRA-03 | Phase 3 | Pending |
| JIRA-04 | Phase 3 | Pending |
| JIRA-05 | Phase 3 | Pending |
| ANAL-01 | Phase 4 | Pending |
| ANAL-02 | Phase 4 | Pending |
| ANAL-03 | Phase 4 | Pending |
| ENRI-01 | Phase 4 | Pending |
| ENRI-02 | Phase 4 | Pending |
| ENRI-03 | Phase 4 | Pending |
| ENRI-04 | Phase 4 | Pending |
| DOCS-01 | Phase 5 | Pending |
| DOCS-02 | Phase 5 | Pending |
| DOCS-03 | Phase 5 | Pending |
| IMPL-01 | Phase 6 | Pending |
| IMPL-02 | Phase 6 | Pending |
| IMPL-03 | Phase 6 | Pending |
| IMPL-04 | Phase 6 | Pending |
| CODE-01 | Phase 7 | Pending |
| CODE-02 | Phase 7 | Pending |
| CODE-03 | Phase 7 | Pending |
| CODE-04 | Phase 7 | Pending |
| CODE-05 | Phase 7 | Pending |
| CODE-06 | Phase 7 | Pending |
| QA-01 | Phase 8 | Pending |
| QA-02 | Phase 8 | Pending |
| QA-03 | Phase 8 | Pending |
| QA-04 | Phase 8 | Pending |
| QA-05 | Phase 8 | Pending |
| QA-06 | Phase 8 | Pending |
| PR-01 | Phase 9 | Pending |
| PR-02 | Phase 9 | Pending |
| PR-03 | Phase 9 | Pending |
| PR-04 | Phase 9 | Pending |
| PR-05 | Phase 9 | Pending |
| FLOW-01 | Phase 3 | Pending |
| FLOW-02 | Phase 3 | Pending |
| FLOW-03 | Phase 3 | Pending |
| FLOW-04 | Phase 3 | Pending |
| AUDI-01 | Phase 3 | Pending |
| AUDI-02 | Phase 3 | Pending |
| AUDI-03 | Phase 3 | Pending |
| AUDI-04 | Phase 9 | Pending |
| STRU-01 | Phase 2 | Pending |
| STRU-02 | Phase 2 | Pending |
| STRU-03 | Phase 2 | Pending |
| STRU-04 | Phase 2 | Pending |
| STRU-05 | Phase 2 | Pending |
| STRU-06 | Phase 3 | Pending |
| STRU-07 | Phase 2 | Pending |

**Coverage:**
- v1 requirements: 59 total
- Mapped to phases: 59
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-07*
*Last updated: 2026-05-07 after initial definition*
