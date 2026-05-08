"""Jira Cloud REST API adapter — implements JiraPort protocol.

To be fully implemented in Phase 3. This stub provides the class
signature and docstring so other modules can import it now.
"""
from src.dev_workflow.domain.models.jira_ticket import JiraTicket


class JiraAdapter:
    """Jira Cloud REST API adapter.

    Implements JiraPort protocol. Full implementation with httpx
    client, rate limiting, and pagination in Phase 3.

    Attributes:
        base_url: Jira Cloud instance URL
        email: Auth email
        api_token: Jira API token
    """

    def __init__(self, base_url: str, email: str, api_token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.api_token = api_token

    def fetch_ticket(self, ticket_key: str) -> JiraTicket:
        """Fetch a Jira ticket by key.

        Args:
            ticket_key: Jira ticket key, e.g. 'PROJ-123'

        Returns:
            JiraTicket domain model

        Raises:
            NotImplementedError: Full implementation in Phase 3
        """
        raise NotImplementedError("JiraAdapter.fetch_ticket() implemented in Phase 3")

    def fetch_ticket_comments(self, ticket_key: str) -> list[str]:
        """Fetch comments for a Jira ticket."""
        raise NotImplementedError(
            "JiraAdapter.fetch_ticket_comments() implemented in Phase 3"
        )

    def fetch_linked_issues(self, ticket_key: str) -> list[str]:
        """Fetch linked issues for a Jira ticket."""
        raise NotImplementedError(
            "JiraAdapter.fetch_linked_issues() implemented in Phase 3"
        )
