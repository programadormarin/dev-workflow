---
phase: 02
slug: authentication
status: verified
threats_open: 0
asvs_level: 1
created: 2026-05-08
---

# Phase 02 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| environment → config loader | Untrusted env vars validated at boundary | JIRA_EMAIL, JIRA_API_TOKEN, JIRA_URL |
| config → domain models | Validated data enters domain layer | JiraCredentials, GitHubCredentials |

---

## Threat Register

| Threat ID | Category | Component | Disposition | Mitigation | Status |
|-----------|----------|-----------|-------------|------------|--------|
| T-02-01 | Information Disclosure | Credentials in logs | mitigate | `domain/models/credentials.py:39-43` — `model_dump()` masks `api_token` with "***" | closed |
| T-02-02 | Tampering | Env var injection | accept | User controls their own environment — not a threat to application | closed |
| T-02-03 | Denial of Service | Missing env vars | mitigate | `infrastructure/config.py:54-60` — `ConfigurationError` raises with exact missing var names | closed |

*Status: open · closed*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-02-01 | T-02-02 | Env var injection from user-controlled environment is not a threat to the application — users set their own env vars | GSD audit | 2026-05-08 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-05-08 | 3 | 3 | 0 | gsd-secure-phase |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-05-08