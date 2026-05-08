---
phase: 02
reviewers: [opencode, antigravity]
reviewed_at: 2026-05-08T19:55:00+01:00
plans_reviewed: [02-01-PLAN.md]
---

# Cross-AI Plan Review — Phase 2: Authentication

## OpenCode Review

### Summary

The plan addresses core authentication requirements with reasonable task breakdown, but has architectural ambiguity around ConfigLoader location and doesn't explicitly address the startup vs lazy-load decision. The threat model coverage is adequate though missing some edge cases around credential expiration and subprocess handling.

---

**Strengths**
- **Clear separation of concerns**: Jira and GitHub credentials modeled separately with domain-appropriate attributes
- **Security-first design**: No credentials in `__repr__` output, grep test for hardcoded secrets explicitly included
- **Error message clarity**: Custom `ConfigurationError` with detailed messages (addresses AUTH-03)
- **Test coverage**: Happy paths and failure cases covered, including subprocess mocking strategy

---

**Concerns**

1. **Architecture Violation** — ConfigLoader referenced in both `domain/models/credentials.py` and `infrastructure/config.py`
   - *Severity: MEDIUM*
   - Credential loading should live in **infrastructure layer**, not domain. Domain should only define credential **models**, not load them.
   - Current plan blurs this boundary.

2. **Validation Timing Not Addressed** — CONTEXT.md states "OpenCode's Discretion: Validation timing (startup vs lazy)"
   - *Severity: MEDIUM*
   - Plan doesn't specify which approach is taken or why. This affects startup performance and when errors surface.

3. **Missing Edge Cases**
   - Empty string vs missing env var not distinguished
   - `gh auth status` edge cases: expired token, partial auth, 2FA required
   - No subprocess timeout — could hang indefinitely
   - *Severity: LOW-MEDIUM*

4. **No Concurrent Access Handling** — If system runs long-lived, credentials accessed concurrently
   - *Severity: LOW*
   - Not critical for v1 but worth noting

---

**Suggestions**

1. **Fix ConfigLoader location**: Move `ConfigLoader` entirely to `infrastructure/config.py`. Domain should only define `JiraCredentials` and `GitHubCredentials` Pydantic models with validation.

2. **Document validation decision**: State explicitly in the plan whether validation happens at startup (eager) or on first use (lazy), with rationale.

3. **Add subprocess timeout**: Use `subprocess.run(timeout=5)` to prevent hangs:
   ```python
   result = subprocess.run(["gh", "auth", "status"], capture_output=True, timeout=5)
   ```

4. **Distinguish empty vs missing**: Treat empty string as invalid (not default to None):
   ```python
   if not os.getenv("JIRA_EMAIL"):  # catches both None and ""
   ```

5. **Handle gh edge cases**: Parse `gh auth status` output for "Logged in to GitHub" vs "not logged in" rather than just exit code.

**Risk Assessment: LOW-MEDIUM**

The plan achieves all four success criteria and the task breakdown is reasonable. Primary risks are architectural (ConfigLoader location) and decision documentation (validation timing). Both are fixable without plan restructuring. The threat model covers the stated concerns adequately for v1.

**Verdict: APPROVE WITH SUGGESTIONS** — Plan is solid for execution. Implement the architectural fix (ConfigLoader in infrastructure) and document the validation timing choice before starting.

---

## Antigravity (Internal) Review

### Summary

Phase 2 is a well-scoped, single-plan phase with clear requirements. The concern about ConfigLoader living in the domain layer is the most important structural issue — loading env vars is an I/O operation and belongs in the infrastructure layer by clean architecture convention. The existing 02-REVIEW.md and 02-REVIEW-FIX.md files in the phase directory suggest this issue was already caught and partially addressed; the implementation should verify those fixes were folded back into the plan.

**Strengths**
- 4 requirements, 4 tasks — clean 1:1 mapping is easy to audit
- STRIDE threat model is concise and accurate for this scope
- `test_no_hardcoded_secrets` is a great security regression test — rare to see this in unit tests
- subprocess mock strategy is correct approach for CI-safe tests

**Concerns**
- **HIGH: ConfigLoader in domain layer** — Task 1 says "Create Pydantic models for credentials" with "ConfigLoader: main class that loads and validates all credentials" — this puts I/O logic (env var reading) in the domain layer. Domain should only contain `JiraCredentials` and `GitHubCredentials` models. ConfigLoader belongs entirely in `infrastructure/config.py`.
- **MEDIUM: `gh auth status` output parsing** — The plan says "check for 'Logged in' or similar success indicators" — this is too vague. The exact output format of `gh auth status` varies between versions and GitHub instances. The implementation should parse stderr, not stdout, and check for exit code 0.
- **MEDIUM: Validation timing unspecified** — The plan defers to "planner decides" but then doesn't decide. Startup validation is strongly recommended: fail fast, fail loudly.
- **LOW: JIRA_URL validation** — Should verify it's a valid HTTPS URL (not HTTP, not trailing slash) at load time.
- **LOW: Credential model repr** — Plan says "No sensitive data in model repr" but doesn't specify HOW. Should explicitly use `model_config = ConfigDict(repr=False)` or custom `__repr__` that masks api_token.

**Suggestions**
1. Move ConfigLoader entirely to `infrastructure/config.py` — domain has only `JiraCredentials` and `GitHubCredentials`
2. Choose startup validation — add comment in plan: "Eager validation at `ConfigLoader.__init__` — fail fast"
3. Mask `api_token` in repr: use `SecretStr` from pydantic or custom `__repr__`
4. Add JIRA_URL format validation: must be HTTPS, must end without trailing slash
5. Use `subprocess.run(["gh", "auth", "status"], capture_output=True, timeout=5, check=False)` — check exit code, not stdout string

**Risk Assessment: LOW-MEDIUM** — Plan is fundamentally sound. ConfigLoader location is a clean architecture violation that should be fixed before execution. All other concerns are implementation-level choices that can be made during coding.

---

## Consensus Summary

Phase 2 reviewed by 2 AI systems (OpenCode + Antigravity).

### Agreed Strengths
- Security-first design: no credentials in repr, explicit grep test for hardcoded secrets
- Clean requirement mapping: 4 AUTH requirements → 4 tasks
- `ConfigurationError` with per-field detail is the right error design
- subprocess mocking strategy for gh CLI testing is correct

### Agreed Concerns (Priority Order)

1. **[HIGH] ConfigLoader in domain layer** — Both reviewers independently flagged this. `ConfigLoader` must live in `infrastructure/config.py`. Domain layer (`credentials.py`) should only contain the Pydantic models `JiraCredentials` and `GitHubCredentials`.

2. **[MEDIUM] Validation timing unspecified** — CONTEXT.md leaves this as "planner decides" but the plan doesn't decide. Both reviewers recommend startup (eager) validation.

3. **[MEDIUM] subprocess edge cases for `gh auth`** — No timeout, no handling of expired tokens, unclear output parsing strategy.

4. **[LOW] Empty string ≠ missing env var** — `os.environ.get("X")` returns `None` for missing but `""` for empty. Both should be treated as invalid.

### Divergent Views

- **`api_token` repr masking:** OpenCode simply says "no credentials in repr"; Antigravity recommends `SecretStr` from Pydantic — the Pydantic approach is more robust and auto-documents the intent.
- **JIRA_URL validation:** Antigravity flagged URL format validation (HTTPS required); OpenCode didn't mention it — worth adding as a low-effort safety check.

---

*To incorporate feedback: `/gsd-plan-phase 2 --reviews`*