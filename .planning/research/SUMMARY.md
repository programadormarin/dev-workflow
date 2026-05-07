# Research Summary: CrewAI Jira-Driven Software Delivery Orchestrator

**Project:** CrewAI Multi-Agent Software Delivery Orchestrator
**Date:** 2026-05-07
**Confidence:** HIGH

## Executive Summary

Production-ready Python system using CrewAI to orchestrate multi-agent software delivery workflow from Jira ticket to PR. Sequential handoffs with explicit outputs, full QA gate before PR creation.

## Key Findings

### Stack

| Component | Choice | Version |
|-----------|--------|---------|
| Orchestration | CrewAI Flow | >=0.90.0 |
| Data Validation | Pydantic | >=2.0 |
| Jira Client | atlassian-python-api | Latest |
| GitHub | gh CLI (native) | Latest |
| Testing | pytest + pytest-asyncio | >=8.0 / >=0.23.0 |
| Type Checking | pyright | Latest |

### Architecture

Flow-First Production Architecture:
- `Flow` wrapper for state management and persistence
- `@persist` for crash recovery
- Pydantic models for all inter-agent contracts
- `@CrewBase` decorators for YAML config loading
- Sequential process for auditability

### Pipeline Stages

1. **Fetch** → Jira ticket via REST API
2. **Analyze** → Requirements extraction with structured output
3. **Enrich** → Fill gaps, edge cases, technical considerations
4. **Implement** → Code execution with safe mode
5. **QA** → Test suite + coverage + CI validation
6. **PR** → GitHub CLI (only if QA passes)

### Table Stakes

- Multi-agent orchestration with CrewAI
- LLM integration (per-agent model selection)
- Structured outputs (output_pydantic)
- Tool support for Jira, GitHub, code execution
- Flow persistence for recovery

### Watch Out For

- **Agent looping** past max_iter limits (CrewAI bug)
- **Context stuffing** multiplies costs 20-30x
- **Rate limits** on Jira API (100 results cap)
- **Code execution** requires sandboxing (84% injection success rate)
- **Sequential process** preferred over hierarchical for audit trails

### Critical Patterns

- Always use `output_pydantic` for task outputs
- Pass `context=[task]` between tasks explicitly
- Use `@persist` on Flow class
- Set `verbose=False` in production
- Add retry logic with tenacity for external tools

## Roadmap Implications

**Phase structure recommended:**
- Phase 1-2: Flow setup, state management, basic agents with structured outputs
- Phase 3-4: Sequential handoffs, guardrails, error handling
- Phase 5: QA integration, coverage thresholds
- Phase 6: Production hardening, observability

## Open Questions

- CrewAI HallucinationGuardrails may be enterprise-only
- MicroVM latency for code execution (90-200ms cold start)
- Jira API rate limit exact behavior for Connect apps

## Sources

- CrewAI Official Docs (production-architecture, flows, tasks)
- Community: Flow-first production patterns
- OWASP: AI agent security guidelines
