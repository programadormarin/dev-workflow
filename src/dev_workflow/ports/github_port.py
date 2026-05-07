"""GitHub service port — abstract interface for GitHub adapters.

This protocol defines what the domain needs from a GitHub service.
Infrastructure adapters (e.g., GitHubAdapter) implement this protocol,
allowing the domain to remain independent of GitHub API/CLI details.
"""
from abc import ABC, abstractmethod
from src.dev_workflow.domain.models.github_pr import GitHubPR


class GitHubPort(ABC):
    """Abstract interface for GitHub service adapters.

    Implementations must provide PR creation and status checking.
    """

    @abstractmethod
    def create_pr(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
    ) -> GitHubPR:
        """Create a GitHub Pull Request.

        Args:
            title: PR title following format '{ticket_key}: {description}'
            body: PR body with ticket summary, implementation summary, QA results
            head_branch: Feature branch name (e.g. 'PROJ-123/add-login')
            base_branch: Target branch (default: 'main')

        Returns:
            GitHubPR with created PR data including URL

        Raises:
            GitHubAuthenticationError: If gh CLI is not authenticated
            GitHubConflictError: If branch already exists
        """
        ...

    @abstractmethod
    def get_pr_status(self, pr_number: int) -> str:
        """Get the current status of a Pull Request.

        Args:
            pr_number: GitHub PR number

        Returns:
            Status string (e.g. 'open', 'closed', 'merged')
        """
        ...
