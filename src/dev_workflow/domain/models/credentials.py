"""Credentials domain models for Jira and GitHub authentication."""
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from src.dev_workflow.infrastructure.config import ConfigurationError, ConfigLoader


class JiraCredentials(BaseModel):
    """Jira credentials loaded from environment variables."""

    email: str = Field(description="Jira account email")
    api_token: str = Field(description="Jira API token")
    url: str = Field(description="Jira Cloud instance URL")

    @field_validator("email")
    @classmethod
    def email_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("JIRA_EMAIL cannot be empty")
        if "@" not in v:
            raise ValueError("JIRA_EMAIL must be a valid email address")
        return v.strip()

    @field_validator("url")
    @classmethod
    def url_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("JIRA_URL cannot be empty")
        if not v.startswith(("http://", "https://")):
            raise ValueError("JIRA_URL must start with http:// or https://")
        return v.strip().rstrip("/")

    @field_validator("api_token")
    @classmethod
    def api_token_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("JIRA_API_TOKEN cannot be empty")
        return v.strip()

    def model_dump(self, **kwargs) -> dict:
        """Omit sensitive data when serializing."""
        data = super().model_dump(**kwargs)
        data["api_token"] = "***" if data["api_token"] else ""
        return data


class GitHubCredentials(BaseModel):
    """GitHub credentials verified via gh CLI."""

    verified: bool = Field(default=False, description="Whether gh CLI is authenticated")
    username: Optional[str] = Field(
        default=None, description="GitHub username if authenticated"
    )

    def __repr__(self) -> str:
        return f"GitHubCredentials(verified={self.verified}, username={self.username})"


# Re-export ConfigurationError and ConfigLoader from infrastructure layer
__all__ = [
    "JiraCredentials",
    "GitHubCredentials",
    "ConfigurationError",
    "ConfigLoader",
]