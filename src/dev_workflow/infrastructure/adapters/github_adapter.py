"""GitHub adapter — implements GitHubPort protocol.

To be fully implemented in Phase 8. This stub provides the class
signature and docstring so other modules can import it now.
"""
from src.dev_workflow.domain.models.github_pr import GitHubPR


class GitHubAdapter:
    """GitHub CLI/API adapter.

    Implements GitHubPort protocol. Full implementation with gh CLI
    and PR creation in Phase 8.

    Attributes:
        owner: GitHub repository owner
        repo: GitHub repository name
    """

    def __init__(self, owner: str, repo: str) -> None:
        self.owner = owner
        self.repo = repo

    def create_pr(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
    ) -> GitHubPR:
        """Create a GitHub Pull Request.

        Args:
            title: PR title
            body: PR body description
            head_branch: Source branch name
            base_branch: Target branch name (default: main)

        Returns:
            GitHubPR domain model

        Raises:
            NotImplementedError: Full implementation in Phase 8
        """
        raise NotImplementedError("GitHubAdapter.create_pr() implemented in Phase 8")

    def get_pr_status(self, pr_number: int) -> str:
        """Get the status of a Pull Request by number."""
        raise NotImplementedError(
            "GitHubAdapter.get_pr_status() implemented in Phase 8"
        )
