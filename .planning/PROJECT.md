# CrewAI Jira-Driven Software Delivery Orchestrator

## What This Is

A production-ready Python system that orchestrates a multi-agent software delivery workflow starting from a Jira ticket. It uses CrewAI to coordinate specialized AI agents through a sequential handoff pipeline that analyzes requirements, creates technical documentation, prepares implementation tasks, executes code changes across a codebase, runs full QA validation, and only creates a GitHub Pull Request upon QA approval.

## Core Value

Deliver production-ready code changes from Jira tickets with zero manual intervention between ticket selection and merged PR — with full traceability and audit trail.

## Requirements

### Active

- [ ] Jira Integration: Fetch, parse, and track Jira tickets via Cloud REST API with API token authentication
- [ ] Requirements Analysis: Agent analyzes ticket description, acceptance criteria, linked issues, and comments to build context
- [ ] Requirements Enrichment: Agent enriches sparse tickets with clarifications, edge cases, and technical considerations
- [ ] Technical Documentation: Agent generates ADRs, technical specs, or runbooks based on enriched requirements
- [ ] Implementation Preparation: Agent breaks work into concrete tasks with file-level assignments
- [ ] Inter-Agent Handoffs: Explicit CrewAI task outputs passed between agents with validation
- [ ] Code Implementation: Agent executes code changes across codebase with strong typing and clean architecture
- [ ] QA Validation: Automated test suite execution, coverage threshold checks, and CI pipeline validation
- [ ] PR Creation: GitHub CLI integration that only creates PR after QA approval gate passes
- [ ] Secure Configuration: Environment-based secrets, no hardcoded credentials, audit logging
- [ ] Traceability: Full audit trail from Jira ticket → AI analysis → implementation → QA → PR

### Out of Scope

- Jira write-back (comments, transitions) — read-only integration
- GitLab support — GitHub only per config
- Visual UI/dashboard — CLI-driven workflow
- Multi-repository PRs — single repository at a time
- Jira OAuth 2.0 — API token only for v1

## Context

- **Orchestration Framework:** CrewAI with sequential agent handoffs and explicit task outputs
- **Multi-Agent Model:** Each agent specializes in one phase with clear input/output contracts
- **Trigger:** Jira ticket key (e.g., `PROJ-123`) passed as CLI argument or config
- **Issue Types:** Stories, Bugs, Tasks — all types supported
- **Team Size:** Small (<10) engineering team, production-grade expectations
- **AI Model Strategy:** Per-agent model selection for optimal cost/quality balance

## Constraints

- **Tech Stack:** Python 3.11+, CrewAI, Jira Cloud REST API, GitHub CLI, pytest
- **Architecture:** Clean architecture with dependency injection for testability
- **Typing:** Full type hints, mypy strict mode, Pydantic for data validation
- **Security:** API tokens via environment variables, no plaintext secrets
- **Git Host:** GitHub only (gh CLI for PR operations)

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| CrewAI orchestration | Built-in multi-agent coordination with handoff primitives | — Pending |
| Jira Cloud REST API | Standard integration, well-documented, API token auth | — Pending |
| GitHub CLI (gh) | Native PR creation, branch management, no API key needed | — Pending |
| Sequential handoffs | Predictable pipeline, clear QA gate before PR | — Pending |
| Per-agent model selection | Small team, different tasks need different capabilities | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-07 after initialization*
