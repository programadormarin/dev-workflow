"""Unit tests for JiraTicket domain model."""
from src.dev_workflow.domain.models.jira_ticket import JiraTicket, IssueType


class TestJiraTicket:
    """Test suite for JiraTicket Pydantic model."""

    def test_create_minimal_ticket(self):
        """Should create a JiraTicket with required fields only."""
        ticket = JiraTicket(
            key="PROJ-123",
            summary="Implement login feature",
            description="Add login functionality",
            issue_type=IssueType.STORY,
            status="To Do",
        )
        assert ticket.key == "PROJ-123"
        assert ticket.summary == "Implement login feature"
        assert ticket.issue_type == IssueType.STORY

    def test_create_ticket_with_optional_fields(self):
        """Should create a JiraTicket with all optional fields."""
        ticket = JiraTicket(
            key="PROJ-456",
            summary="Fix bug",
            description="Fix login bug",
            issue_type=IssueType.BUG,
            status="In Progress",
            assignee="dev@example.com",
            acceptance_criteria=["Login works", "No errors in console"],
            comments=["First comment"],
            linked_issues=["PROJ-100"],
        )
        assert ticket.assignee == "dev@example.com"
        assert len(ticket.acceptance_criteria) == 2
        assert "PROJ-100" in ticket.linked_issues

    def test_ticket_serialization(self):
        """Should serialize JiraTicket to JSON."""
        ticket = JiraTicket(
            key="PROJ-789",
            summary="Test",
            description="Test ticket",
            issue_type=IssueType.TASK,
            status="Done",
        )
        json_str = ticket.model_dump_json()
        assert "PROJ-789" in json_str
        assert "Test" in json_str

    def test_issue_type_enum_values(self):
        """Should accept all supported issue types."""
        for issue_type in [IssueType.STORY, IssueType.BUG, IssueType.TASK]:
            ticket = JiraTicket(
                key="PROJ-1",
                summary="x",
                description="y",
                issue_type=issue_type,
                status="Open",
            )
            assert ticket.issue_type == issue_type
