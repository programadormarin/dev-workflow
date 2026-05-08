# Phase 03: Jira Integration & Flow Orchestration - Research

## Context Overview
Phase 3 requires replacing the `JiraAdapter` stub with a real Jira Cloud REST API implementation using `httpx`, handling rate limits with `tenacity`, and auto-paginating results. It also requires orchestrating a `DeliveryFlow` pipeline where `CrewAI` `@persist` handles state recovery and output passing.

## 1. Jira Cloud REST API Details
- **Endpoint for Ticket + Comments + Linked Issues:** `GET /rest/api/3/issue/{issueIdOrKey}?expand=comment,issuelinks`
- **Pagination Strategy:** Jira uses `startAt` and `maxResults`. For comments specifically, if there are many, the `comment` block itself is paginated and provides a `total`, `startAt`, and `maxResults`. The adapter can loop through requests by modifying `startAt` until `startAt + maxResults >= total`.
- **Authentication:** Jira Cloud requires HTTP Basic Auth with an email and an API token. The `httpx.Client` supports this naturally with `auth=(email, api_token)`.

## 2. Resilience with Tenacity & HTTPX
- **Tenacity:** The requirement (D-03) calls for `tenacity` with exponential backoff on 429 and 5xx.
- **Implementation Pattern:**
```python
import httpx
from tenacity import retry, wait_exponential_jitter, stop_after_attempt, retry_if_exception

def is_retryable(exception: Exception) -> bool:
    if isinstance(exception, httpx.HTTPStatusError):
        # Retry on 429 (Too Many Requests) or 5xx server errors
        return exception.response.status_code in (429, 500, 502, 503, 504)
    if isinstance(exception, (httpx.ConnectError, httpx.ReadTimeout, httpx.RemoteProtocolError)):
        return True
    return False

@retry(
    wait=wait_exponential_jitter(initial=1, max=60),
    stop=stop_after_attempt(5),
    retry=retry_if_exception(is_retryable),
    reraise=True
)
def fetch_something():
    ...
```
This handles JIRA-04 completely cleanly.

## 3. CrewAI Flow & @persist Strategy
- **Usage:** CrewAI Flows (`from crewai.flow.flow import Flow, start, listen`) manage state transitions.
- **Persistence:** By applying `@persist()` to the class or specific methods, the flow automatically saves its state to SQLite locally. If a crash happens, passing the `state.id` (if tracked) or using the same configured flow ID allows resumption.
- **Output Passing:** The requirement FLOW-03 explicitly says: "Each stage receives explicit outputs from previous stage via context (not implicit state)." In CrewAI Flows, methods decorated with `@listen(previous_method)` receive the return value of `previous_method` as an argument.
- **Halt on Failure:** (FLOW-04) A stage can raise an exception. Since `DeliveryFlow.run` calls the stages sequentially, an exception naturally stops the pipeline before reaching the PR stage.

## 4. Architectural Integration
- **Dependency Inversion:** `JiraAdapter` must inherit from `JiraPort`.
- **Orchestration:** `DeliveryFlow` will act as a coordinator. It might encapsulate a CrewAI `Flow` inside it or be implemented directly as a `Flow` itself.
- **Logging/CLI:** `__main__.py` will instantiate the adapters, pass them to `DeliveryFlow`, and call `run(ticket_key)`.

## Validation Architecture

### Dimensions of Validation
1. **API Integration Validation:** Verify that `JiraAdapter` correctly parses a real (or mocked) Jira REST API response with expanded comments and issuelinks.
2. **Resilience Validation:** Verify that `tenacity` retries exactly 5 times when `httpx` returns a 429 response, and does not retry on a 404 response.
3. **Flow State Validation:** Verify that `DeliveryFlow` passes explicit Pydantic models between stages, not generic dictionaries.
4. **Execution Flow:** Ensure that if `_run_implement_stage` raises an error, `_run_qa_stage` and `_run_pr_stage` are never invoked.
