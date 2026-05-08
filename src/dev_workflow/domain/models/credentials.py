"""Credentials domain models for Jira and GitHub authentication."""
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import os


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


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid."""

    def __init__(self, message: str, missing_vars: Optional[List[str]] = None):
        super().__init__(message)
        self.missing_vars = missing_vars or []

    def __repr__(self) -> str:
        return f"ConfigurationError({super().__repr__()})"


class ConfigLoader:
    """
    Loads and validates all credentials from environment variables.

    Validates at initialization. Raises ConfigurationError with clear messages
    if any required environment variable is missing.
    """

    REQUIRED_JIRA_VARS = ["JIRA_EMAIL", "JIRA_API_TOKEN", "JIRA_URL"]

    def __init__(self, lazy: bool = False) -> None:
        """
        Initialize ConfigLoader.

        Args:
            lazy: If True, defer loading until first access. If False, load now.
        """
        self._jira_credentials: Optional[JiraCredentials] = None
        self._lazy = lazy

        if not lazy:
            self._load_jira_credentials()

    def _load_jira_credentials(self) -> None:
        """Load and validate Jira credentials from environment."""
        missing = []
        values = {}

        for var in self.REQUIRED_JIRA_VARS:
            val = os.environ.get(var)
            if not val:
                missing.append(var)
            else:
                values[var] = val

        if missing:
            joined = ", ".join(sorted(missing))
            raise ConfigurationError(
                f"Missing required environment variables: {joined}. "
                f"Please set {joined} in your environment.",
                missing_vars=missing,
            )

        self._jira_credentials = JiraCredentials(
            email=values["JIRA_EMAIL"],
            api_token=values["JIRA_API_TOKEN"],
            url=values["JIRA_URL"],
        )

    @property
    def jira_credentials(self) -> JiraCredentials:
        """Access Jira credentials (lazy-load if configured)."""
        if self._jira_credentials is None:
            self._load_jira_credentials()
        return self._jira_credentials

    def get_jira(self) -> JiraCredentials:
        """Get Jira credentials — alias for jira_credentials property."""
        return self.jira_credentials