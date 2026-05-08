"""Tests for credential models and configuration."""
import os
from unittest.mock import patch
import pytest
from pydantic import ValidationError

from src.dev_workflow.domain.models.credentials import (
    JiraCredentials,
    GitHubCredentials,
    ConfigLoader,
    ConfigurationError,
)


class TestJiraCredentials:
    """Tests for JiraCredentials model."""

    def test_valid_credentials(self):
        """Valid email/token/url passes validation."""
        creds = JiraCredentials(
            email="test@example.com",
            api_token="testtoken123",
            url="https://test.atlassian.net",
        )
        assert creds.email == "test@example.com"
        assert creds.api_token == "testtoken123"
        assert creds.url == "https://test.atlassian.net"

    def test_email_validation(self):
        """Invalid email raises ValidationError."""
        with pytest.raises(ValidationError, match="valid email"):
            JiraCredentials(
                email="not-an-email",
                api_token="token",
                url="https://test.atlassian.net",
            )

    def test_url_requires_protocol(self):
        """URL without http/https raises ValidationError."""
        with pytest.raises(ValidationError, match="http"):
            JiraCredentials(
                email="test@example.com",
                api_token="token",
                url="test.atlassian.net",
            )

    def test_empty_email_raises(self):
        """Empty email raises ValidationError."""
        with pytest.raises(ValidationError):
            JiraCredentials(
                email="",
                api_token="token",
                url="https://test.atlassian.net",
            )

    def test_empty_token_raises(self):
        """Empty API token raises ValidationError."""
        with pytest.raises(ValidationError):
            JiraCredentials(
                email="test@example.com",
                api_token="",
                url="https://test.atlassian.net",
            )

    def test_sensitive_data_excluded_from_repr(self):
        """model_dump masks sensitive fields."""
        data = JiraCredentials(
            email="test@example.com",
            api_token="secret123",
            url="https://test.atlassian.net",
        ).model_dump()
        assert data["api_token"] == "***"
        assert data["email"] == "test@example.com"


class TestGitHubCredentials:
    """Tests for GitHubCredentials model."""

    def test_verified_credentials(self):
        """Authenticated gh CLI returns verified=True."""
        creds = GitHubCredentials(verified=True, username="testuser")
        assert creds.verified is True
        assert creds.username == "testuser"

    def test_not_verified_credentials(self):
        """Unauthenticated gh returns verified=False."""
        creds = GitHubCredentials(verified=False)
        assert creds.verified is False
        assert creds.username is None

    def test_repr_excludes_sensitive_data(self):
        """__repr__ shows verification status without secrets."""
        creds = GitHubCredentials(verified=True, username="testuser")
        repr_str = repr(creds)
        assert "testuser" in repr_str
        assert "token" not in repr_str.lower()


class TestConfigLoader:
    """Tests for ConfigLoader."""

    def test_loads_env_vars(self):
        """ConfigLoader loads from environment correctly."""
        with patch.dict(
            os.environ,
            {
                "JIRA_EMAIL": "test@example.com",
                "JIRA_API_TOKEN": "testtoken",
                "JIRA_URL": "https://test.atlassian.net",
            },
            clear=True,
        ):
            loader = ConfigLoader()
            creds = loader.jira_credentials
            assert creds.email == "test@example.com"
            assert creds.api_token == "testtoken"
            assert creds.url == "https://test.atlassian.net"

    def test_missing_env_raises_clear_error(self):
        """Missing env var raises ConfigurationError with clear message."""
        env = {k: v for k, v in os.environ.items() if k.startswith("JIRA_")}
        with patch.dict(os.environ, env, clear=True):
            with pytest.raises(ConfigurationError) as exc_info:
                ConfigLoader()
            error_msg = str(exc_info.value)
            assert "JIRA_EMAIL" in error_msg
            assert "JIRA_API_TOKEN" in error_msg
            assert "JIRA_URL" in error_msg

    def test_lazy_load(self):
        """Lazy ConfigLoader defers credential loading."""
        with patch.dict(
            os.environ,
            {
                "JIRA_EMAIL": "test@example.com",
                "JIRA_API_TOKEN": "testtoken",
                "JIRA_URL": "https://test.atlassian.net",
            },
            clear=True,
        ):
            loader = ConfigLoader(lazy=True)
            # Should not raise on init
            assert loader._jira_credentials is None
            # Access triggers load
            creds = loader.jira_credentials
            assert creds.email == "test@example.com"


class TestGitHubAuth:
    """Tests for GitHubAuth (requires mocking gh CLI)."""

    def test_github_auth_verified(self):
        """Successful gh auth returns verified=True."""
        from src.dev_workflow.infrastructure.auth import GitHubAuth

        mock_result = """github.com
  ✓ Logged in to github.com account testuser (keyring)
  - Active account: true"""

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = mock_run.return_value
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = mock_result
            mock_run.return_value.stderr = ""

            # Make subprocess.run work for both --version and auth status
            def run_side_effect(*args, **kwargs):
                cmd = args[0]
                if "--version" in cmd:
                    result = mock_run.return_value.__class__(
                        returncode=0, stdout="gh version 2.0.0", stderr=""
                    )
                else:
                    result = mock_run.return_value.__class__(
                        returncode=0, stdout=mock_result, stderr=""
                    )
                return result

            mock_run.side_effect = run_side_effect

            auth = GitHubAuth()
            result = auth.verify()
            assert result.verified is True
            assert result.username == "testuser"

    def test_github_auth_not_logged_in(self):
        """Clear error when gh not authenticated."""
        from src.dev_workflow.infrastructure.auth import GitHubAuth, GitHubAuthError

        mock_result = "gh: To use GitHub CLI commands, you need to authenticate."

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = mock_run.return_value
            mock_run.return_value.returncode = 4
            mock_run.return_value.stdout = ""
            mock_run.return_value.stderr = mock_result

            def run_side_effect(*args, **kwargs):
                cmd = args[0]
                if "--version" in cmd:
                    result = mock_run.return_value.__class__(
                        returncode=0, stdout="gh version 2.0.0", stderr=""
                    )
                else:
                    result = mock_run.return_value.__class__(
                        returncode=4, stdout="", stderr=mock_result
                    )
                return result

            mock_run.side_effect = run_side_effect

            auth = GitHubAuth()
            with pytest.raises(GitHubAuthError) as exc_info:
                auth.verify()
            assert "authenticate" in str(exc_info.value).lower()

    def test_github_auth_not_installed(self):
        """Clear error when gh CLI not installed."""
        from src.dev_workflow.infrastructure.auth import GitHubAuth, GitHubAuthError

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError("gh not found")

            auth = GitHubAuth()
            with pytest.raises(GitHubAuthError) as exc_info:
                auth.verify()
            assert "not installed" in str(exc_info.value).lower()


class TestNoHardcodedSecrets:
    """Tests verifying no hardcoded secrets exist."""

    def test_no_hardcoded_secrets_in_models(self):
        """Credentials models should not contain hardcoded secrets."""
        # Import the module
        from src.dev_workflow import domain

        # Check source for common secret patterns
        import inspect

        source = inspect.getsource(domain.models.credentials)
        forbidden = [
            "password",
            "secret",
            "api_key",
            "token",
            "credential",
        ]
        for pattern in forbidden:
            # Skip variable names, only catch string literals
            if (
                f'"{pattern}' in source.lower()
                or f"'{pattern}" in source.lower()
            ):
                # It's OK if it's a parameter name or variable
                # Just ensure it's not a hardcoded value
                lines = source.split("\n")
                for line in lines:
                    if pattern in line.lower() and "=" in line:
                        # Check if it's a hardcoded string value
                        if (
                            f'"{pattern}' in line.lower()
                            or f"'{pattern}" in line.lower()
                        ):
                            if "Field(" not in line and "description" not in line:
                                pytest.fail(f"Possible hardcoded secret in: {line}")