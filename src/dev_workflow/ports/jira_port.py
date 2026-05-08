"""Jira service port — abstract interface for Jira adapters.

This protocol defines what the domain needs from a Jira service.
Infrastructure adapters (e.g., JiraAdapter) implement this protocol,
allowing the domain to remain independent of Jira API details.

Per clean architecture: domain defines interfaces (ports),
infrastructure implements them.
"""
from abc import ABC, abstractmethod
from src.dev_workflow.domain.models.jira_ticket import JiraTicket


class JiraPort(ABC):
    """Abstract interface for Jira service adapters.

    Implementations must provide:
    - Ticket fetching (basic data, comments, linked issues)
    - Support for Story, Bug, Task issue types

    The domain layer depends on this abstraction, not on concrete adapters.
    """

    @abstractmethod
    def fetch_ticket(self, ticket_key: str) -> JiraTicket:
        """Fetch a Jira ticket by key.

        Args:
            ticket_key: Jira ticket key, e.g. 'PROJ-123'

        Returns:
            JiraTicket with all fields populated

        Raises:
            JiraConnectionError: If Jira API is unreachable
            JiraAuthenticationError: If credentials are invalid
            JiraNotFoundError: If ticket does not exist
        """
        ...

    @abstractmethod
    def fetch_ticket_comments(self, ticket_key: str) -> list[str]:
        """Fetch all comments from a Jira ticket.

        Args:
            ticket_key: Jira ticket key

        Returns:
            List of comment strings
        """
        ...

    @abstractmethod
    def fetch_linked_issues(self, ticket_key: str) -> list[str]:
        """Fetch all linked issue keys from a Jira ticket.

        Args:
            ticket_key: Jira ticket key

        Returns:
            List of linked issue keys (e.g. ['PROJ-100', 'PROJ-200'])
        """
        ...
