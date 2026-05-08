---
phase: 03
slug: jira-integration-flow-orchestration
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-08
---

# Phase 03 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x |
| **Config file** | pyproject.toml |
| **Quick run command** | `pytest tests/unit/domain tests/unit/application -v` |
| **Full suite command** | `pytest tests/ -v` |
| **Estimated runtime** | ~2 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/unit/infrastructure/adapters/test_jira_adapter.py -v`
- **After every plan wave:** Run `pytest tests/ -v`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | JIRA-01 | — | N/A | unit | `pytest tests/` | ❌ W0 | ⬜ pending |
| 03-01-02 | 01 | 1 | JIRA-02 | — | N/A | unit | `pytest tests/` | ❌ W0 | ⬜ pending |
| 03-01-03 | 01 | 1 | JIRA-04 | — | N/A | unit | `pytest tests/` | ❌ W0 | ⬜ pending |
| 03-01-04 | 01 | 1 | JIRA-05 | — | N/A | unit | `pytest tests/` | ❌ W0 | ⬜ pending |
| 03-02-01 | 02 | 2 | FLOW-01 | — | N/A | unit | `pytest tests/` | ❌ W0 | ⬜ pending |
| 03-02-02 | 02 | 2 | FLOW-02 | — | N/A | unit | `pytest tests/` | ❌ W0 | ⬜ pending |
| 03-02-03 | 02 | 2 | FLOW-03 | — | N/A | unit | `pytest tests/` | ❌ W0 | ⬜ pending |
| 03-02-04 | 02 | 2 | FLOW-04 | — | N/A | unit | `pytest tests/` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/unit/infrastructure/adapters/test_jira_adapter.py` — stubs for JIRA-*
- [ ] `tests/unit/application/test_delivery_flow.py` — stubs for FLOW-* (some exist from Phase 1, need expansion)
- [ ] `tests/conftest.py` — shared fixtures for Jira tickets and Mock CrewAI Flow

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| CLI interaction | JIRA-01 | End-to-end integration | Run `python -m src.dev_workflow PROJ-123` with mock environment variables |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
