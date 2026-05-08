# Phase 2: Authentication - Discussion Log

**Date:** 2026-05-08

## Areas Discussed

### Config Source

**Question:** How should the system load credentials? Just environment variables or also support config file?

**Options presented:**
1. Environment variables only — Keep it simple: JIRA_EMAIL, JIRA_API_TOKEN, JIRA_URL. No config file support.
2. Config file support — Also support .env file or config.yaml for local development convenience.

**Decision:** Environment variables only

**Rationale:** Keep authentication simple for v1. Users set credentials directly in their environment.

---

## Deferred Ideas

- Config file support (.env, config.yaml) — Future phase enhancement if needed

---

*Discussion log created: 2026-05-08*