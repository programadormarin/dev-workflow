"""GitHub Pull Request domain model."""
from typing import Optional
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
    ticket_key: Optional[str] = Field(
        default=None, description="Jira ticket key if linked"
    )
