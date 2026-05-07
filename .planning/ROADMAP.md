# Roadmap: CrewAI Jira-Driven Software Delivery Orchestrator

**Created:** 2026-05-07
**Granularity:** standard (5-8 phases)
**Total Requirements:** 59 v1

## Phases

- [ ] **Phase 1: Project Structure** - Scaffold clean architecture with domain/ports/infrastructure layers
- [ ] **Phase 2: Authentication** - Environment-based credentials with validation
- [ ] **Phase 3: Jira Integration & Flow Orchestration** - Ticket fetching with CrewAI pipeline
- [ ] **Phase 4: Requirements Processing** - Analysis and enrichment agents with structured outputs
- [ ] **Phase 5: Technical Documentation** - ADR/Spec generation from enriched requirements
- [ ] **Phase 6: Implementation Planning** - Task breakdown with file-level assignments
- [ ] **Phase 7: Code Implementation** - Execute changes with clean architecture patterns
- [ ] **Phase 8: QA Validation & PR Creation** - Automated testing and GitHub PR after QA pass

## Phase Details

### Phase 1: Project Structure

**Goal:** Scaffold production-ready project layout following clean architecture conventions

**Depends on:** Nothing (first phase)

**Requirements:** STRU-01, STRU-02, STRU-03, STRU-04, STRU-05, STRU-06, STRU-07

**Success Criteria** (what must be TRUE):

1. Developer can run `python -m src.dev_workflow` without errors after setup
2. Project follows `src/dev_workflow/` layout with `pyproject.toml` at root
3. Domain models are in `src/dev_workflow/domain/models/` directory
4. Ports (protocols) are in `src/dev_workflow/ports/` directory
5. Infrastructure adapters are in `src/dev_workflow/infrastructure/` directory
6. Crews are in `src/dev_workflow/crews/` with YAML configs
7. Main flow exists in `src/dev_workflow/application/delivery_flow.py`
8. `uv.lock` file is present for reproducible builds

**Plans:** TBD

---

### Phase 2: Authentication

**Goal:** System loads and validates credentials from environment with secure configuration

**Depends on:** Phase 1

**Requirements:** AUTH-01, AUTH-02, AUTH-03, AUTH-04

**Success Criteria** (what must be TRUE):

1. User can set JIRA_EMAIL, JIRA_API_TOKEN, JIRA_URL environment variables and system loads them
2. System verifies gh CLI authentication before any PR operations
3. System validates all required environment variables on startup with clear error messages (not generic errors)
4. No hardcoded credentials exist anywhere in the codebase (verifiable via grep for secrets)

**Plans:** TBD

---

### Phase 3: Jira Integration & Flow Orchestration

**Goal:** User can trigger workflow with Jira ticket key and system fetches ticket data via sequential pipeline

**Depends on:** Phase 2

**Requirements:** JIRA-01, JIRA-02, JIRA-03, JIRA-04, JIRA-05, FLOW-01, FLOW-02, FLOW-03, FLOW-04, AUDI-01, AUDI-02, AUDI-03, STRU-06

**Success Criteria** (what must be TRUE):

1. User can run CLI with Jira ticket key (e.g., `PROJ-123`) and system starts workflow
2. System fetches ticket data including description, acceptance criteria, comments, and linked issues from Jira Cloud REST API
3. System handles Jira API rate limits with exponential backoff retry logic (not immediate failure)
4. System handles Jira API pagination for tickets with many comments/linked issues
5. Flow class orchestrates sequential pipeline: Fetch → Analyze → Enrich → Document → Implement → QA → PR
6. Flow state persists via @persist decorator for crash recovery (can resume after interruption)
7. Each stage receives explicit outputs from previous stage via context (not implicit state)
8. Flow halts before PR if any stage fails, with clear error message (not silent continuation)
9. System logs all pipeline stages with timestamps
10. System generates execution summary with Jira ticket → implementation → PR URL mapping

**Plans:** TBD

---

### Phase 4: Requirements Processing

**Goal:** Analysis and enrichment agents extract and refine requirements with structured Pydantic outputs

**Depends on:** Phase 3

**Requirements:** ANAL-01, ANAL-02, ANAL-03, ENRI-01, ENRI-02, ENRI-03, ENRI-04

**Success Criteria** (what must be TRUE):

1. Analysis agent extracts summary, acceptance criteria, edge cases, and technical considerations from ticket data
2. Analysis output is structured via Pydantic model with confidence score field
3. System rejects analysis outputs with confidence score below 0.7 threshold (low confidence = halt)
4. Enrichment agent identifies gaps in sparse tickets and fills with clarifications
5. Enrichment agent adds edge cases and technical considerations not explicitly stated in original ticket
6. Enriched requirements output includes title, description, scope, and acceptance criteria fields
7. Enrichment output is structured via Pydantic model (not raw text)

**Plans:** TBD

---

### Phase 5: Technical Documentation

**Goal:** System generates technical documentation (ADR or spec) based on enriched requirements

**Depends on:** Phase 4

**Requirements:** DOCS-01, DOCS-02, DOCS-03

**Success Criteria** (what must be TRUE):

1. System generates technical documentation (ADR or spec) based on enriched requirements (not raw ticket)
2. Documentation is written to `output/pr/{ticket_key}/docs/` directory
3. Documentation includes implementation approach, file-level assignments, and success criteria

**Plans:** TBD

---

### Phase 6: Implementation Planning

**Goal:** Implementation agent breaks work into concrete tasks with file-level assignments

**Depends on:** Phase 5

**Requirements:** IMPL-01, IMPL-02, IMPL-03, IMPL-04

**Success Criteria** (what must be TRUE):

1. Implementation agent breaks work into concrete tasks with file-level assignments
2. Implementation plan includes branch naming convention (`{ticket_key}/{short-description}`)
3. Implementation plan includes affected files list
4. Implementation plan output is structured via Pydantic model

**Plans:** TBD

---

### Phase 7: Code Implementation

**Goal:** Agent executes code changes following clean architecture with full type hints

**Depends on:** Phase 6

**Requirements:** CODE-01, CODE-02, CODE-03, CODE-04, CODE-05, CODE-06

**Success Criteria** (what must be TRUE):

1. Implementation agent executes code changes with clean architecture (domain/ports/infrastructure layers)
2. All new code includes full type hints (mypy/pyright compatible, no "Any" unless necessary)
3. Code changes follow existing project patterns and conventions
4. Implementation uses Pydantic models for data contracts between modules
5. Code execution runs in safe/sandboxed mode (no system-level operations like rm -rf)
6. Implementation agent creates branch via git before making changes

**Plans:** TBD

---

### Phase 8: QA Validation & PR Creation

**Goal:** Automated QA validation passes before GitHub PR is created

**Depends on:** Phase 7

**Requirements:** QA-01, QA-02, QA-03, QA-04, QA-05, QA-06, PR-01, PR-02, PR-03, PR-04, PR-05, AUDI-04

**Success Criteria** (what must be TRUE):

1. System runs pytest test suite on implemented changes
2. System enforces minimum coverage threshold (configurable, default 80%)
3. System runs type checking (mypy strict mode) and fails on errors
4. System runs linting (ruff or flake8) and fails on errors
5. QA results include pass/fail status, test count, coverage percentage, type errors, lint errors
6. QA results output is structured via Pydantic model with passed boolean
7. System creates GitHub PR via gh CLI only after QA validation passes (not before)
8. PR title follows format: `{ticket_key}: {short_description}`
9. PR body includes ticket summary, implementation summary, and QA results
10. System skips PR creation if QA validation fails, with clear error output
11. PR is created from feature branch to configured target branch (default: main)
12. PR body includes traceability link to Jira ticket

**Plans:** TBD

---

## Coverage Map

| Phase | Requirements | Status |
|-------|--------------|--------|
| 1 - Project Structure | STRU-01, STRU-02, STRU-03, STRU-04, STRU-05, STRU-06, STRU-07 | 7/7 |
| 2 - Authentication | AUTH-01, AUTH-02, AUTH-03, AUTH-04 | 4/4 |
| 3 - Jira Integration & Flow | JIRA-01, JIRA-02, JIRA-03, JIRA-04, JIRA-05, FLOW-01, FLOW-02, FLOW-03, FLOW-04, AUDI-01, AUDI-02, AUDI-03, STRU-06 | 13/13 |
| 4 - Requirements Processing | ANAL-01, ANAL-02, ANAL-03, ENRI-01, ENRI-02, ENRI-03, ENRI-04 | 7/7 |
| 5 - Technical Documentation | DOCS-01, DOCS-02, DOCS-03 | 3/3 |
| 6 - Implementation Planning | IMPL-01, IMPL-02, IMPL-03, IMPL-04 | 4/4 |
| 7 - Code Implementation | CODE-01, CODE-02, CODE-03, CODE-04, CODE-05, CODE-06 | 6/6 |
| 8 - QA & PR Creation | QA-01, QA-02, QA-03, QA-04, QA-05, QA-06, PR-01, PR-02, PR-03, PR-04, PR-05, AUDI-04 | 12/12 |

**Total:** 59/59 requirements mapped ✓

---

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Project Structure | 0/1 | Not started | - |
| 2. Authentication | 0/1 | Not started | - |
| 3. Jira Integration & Flow | 0/1 | Not started | - |
| 4. Requirements Processing | 0/1 | Not started | - |
| 5. Technical Documentation | 0/1 | Not started | - |
| 6. Implementation Planning | 0/1 | Not started | - |
| 7. Code Implementation | 0/1 | Not started | - |
| 8. QA & PR Creation | 0/1 | Not started | - |

---

*Roadmap created: 2026-05-07*