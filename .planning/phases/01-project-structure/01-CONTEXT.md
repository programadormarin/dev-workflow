# 01-Project-Structure Context

**Phase:** 1  
**Project:** CrewAI Jira-Driven Software Delivery Orchestrator  
**Date:** 2026-05-07  

---

## Domain

Scaffold production-ready project layout following clean architecture conventions

## Requirements

Requirements locked by ROADMAP.md:
- STRU-01: Project follows `src/dev_workflow/` layout with `pyproject.toml`
- STRU-02: Domain models in `src/dev_workflow/domain/models/`
- STRU-03: Ports (protocols) in `src/dev_workflow/ports/`
- STRU-04: Infrastructure adapters in `src/dev_workflow/infrastructure/`
- STRU-05: Crews in `src/dev_workflow/crews/` with YAML configs
- STRU-07: `uv.lock` file present for reproducible builds

## Decisions

### Crew Configuration

| Decision | Choice |
|----------|--------|
| Execution model | Sequential — one agent completes before next starts |
| Output coupling | Pydantic models — type-safe handoffs between stages |
| Crew definition format | YAML files — declarative, version-controlled |
| Crew granularity | One crew per pipeline stage |

**Pipeline stages:** Fetch → Analyze → Enrich → Document → Implement → QA → PR

### Testing Setup

| Decision | Choice |
|----------|--------|
| Test organization | By feature — mirrors `src/` structure |
| Test isolation | Mock external services (Jira, GitHub) |
| Coverage threshold | 80% |

## Canonical Refs

No external specs/ADRs referenced — this is the first phase.

## Deferred Ideas

None noted.

## Code Context

Clean architecture pattern:
- `src/dev_workflow/domain/models/` — Domain entities
- `src/dev_workflow/ports/` — Protocol definitions (interfaces)
- `src/dev_workflow/infrastructure/` — Adapters (Jira, GitHub)
- `src/dev_workflow/crews/` — YAML crew definitions
- `src/dev_workflow/application/` — Flow orchestration

---

*Created via /gsd-discuss-phase 1*