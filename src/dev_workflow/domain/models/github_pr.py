"""GitHub Pull Request domain model."""
from pydantic import BaseModel, Field


class GitHubPR(BaseModel):
    """Domain model representing a GitHub Pull Request."""
    number: int
    title: str
    body: str
    head_branch: str
    base_branch: str = "main"
    status: str
    url: str
    ticket_key: str | None = Field(default=None, description="Jira ticket key if linked")
