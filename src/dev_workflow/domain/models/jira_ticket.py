"""Jira ticket domain model."""
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class IssueType(str, Enum):
    STORY = "Story"
    BUG = "Bug"
    TASK = "Task"


class JiraTicket(BaseModel):
    """Domain model representing a Jira ticket."""
    key: str = Field(description="Jira ticket key, e.g. PROJ-123")
    summary: str = Field(description="Ticket title/summary")
    description: str = Field(description="Full ticket description")
    issue_type: IssueType
    status: str
    assignee: Optional[str] = None
    acceptance_criteria: List[str] = Field(default_factory=list)
    comments: List[str] = Field(default_factory=list)
    linked_issues: List[str] = Field(default_factory=list)
