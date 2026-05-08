"""Infrastructure layer: configuration loading."""
import os
from typing import List, Optional

from src.dev_workflow.domain.models.credentials import JiraCredentials


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
    if any required environment variable is missing (not generic).
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

        # Use domain model for validated credentials
        from src.dev_workflow.domain.models.credentials import JiraCredentials as DomainJiraCredentials

        self._jira_credentials = DomainJiraCredentials(
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

    def validate(self) -> None:
        """Explicit validation — raises ConfigurationError if missing."""
        self._load_jira_credentials()