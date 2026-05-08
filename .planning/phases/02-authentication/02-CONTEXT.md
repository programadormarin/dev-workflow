# Phase 2: Authentication - Context

**Gathered:** 2026-05-08
**Status:** Ready for planning
**Source:** discuss-phase

<domain>
## Phase Boundary

System loads and validates credentials from environment with secure configuration. This phase sets up the authentication layer that all subsequent phases depend on for Jira and GitHub access.

**Requirements:**
- AUTH-01: System loads Jira credentials from environment variables (JIRA_EMAIL, JIRA_API_TOKEN, JIRA_URL)
- AUTH-02: System verifies gh CLI authentication before PR operations
- AUTH-03: System validates all required environment variables on startup with clear error messages
- AUTH-04: No hardcoded credentials anywhere in codebase

</domain>

<decisions>
## Implementation Decisions

### Configuration Source
- **Environment variables only** — No config file support. Simplicity for v1. Users set JIRA_EMAIL, JIRA_API_TOKEN, JIRA_URL directly in their environment.

### OpenCode's Discretion
- Validation timing: Validate at startup or lazy-load per operation (planner decides)
- Error message detail level: How specific (planner decides)
- Secret handling during runtime: os.environ, dataclasses, or other (planner decides)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

- `.planning/REQUIREMENTS.md` — All AUTH-* requirements (AUTH-01 through AUTH-04)
- `.planning/ROADMAP.md` — Phase 2 success criteria and goals

No external specs — requirements fully captured in decisions above.

</canonical_refs>

<specifics>
## Specific Ideas

- Jira credentials: JIRA_EMAIL, JIRA_API_TOKEN, JIRA_URL
- GitHub CLI: gh must be authenticated via `gh auth status`
- Clear error messages on validation failure — not generic errors

</specifics>

<deferred>
## Deferred Ideas

- Config file support (.env, config.yaml) — noted for future phases if needed

</deferred>

---

*Phase: 02-authentication*
*Context gathered: 2026-05-08 via discuss-phase*