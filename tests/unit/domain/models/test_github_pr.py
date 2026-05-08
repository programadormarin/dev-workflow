"""Unit tests for GitHubPR domain model."""
from src.dev_workflow.domain.models.github_pr import GitHubPR


class TestGitHubPR:
    """Test suite for GitHubPR Pydantic model."""

    def test_create_pr_with_required_fields(self):
        """Should create a GitHubPR with required fields."""
        pr = GitHubPR(
            number=42,
            title="Implement feature",
            body="Adds a new feature.",
            head_branch="feature/new-feature",
            status="open",
            url="https://github.com/org/repo/pull/42",
        )
        assert pr.number == 42
        assert pr.base_branch == "main"
        assert pr.ticket_key is None

    def test_pr_serialization(self):
        """Should serialize GitHubPR to JSON."""
        pr = GitHubPR(
            number=101,
            title="Fix bug",
            body="Fixes a bug.",
            head_branch="bugfix/issue-101",
            status="merged",
            url="https://github.com/org/repo/pull/101",
            ticket_key="PROJ-101",
        )
        json_str = pr.model_dump_json()
        assert "101" in json_str
        assert "PROJ-101" in json_str
