"""Infrastructure layer: GitHub CLI authentication verification."""
import subprocess
from typing import Optional

from src.dev_workflow.domain.models.credentials import GitHubCredentials


class GitHubAuthError(Exception):
    """Raised when GitHub authentication verification fails."""

    def __init__(self, message: str, reason: str):
        super().__init__(message)
        self.reason = reason


class GitHubAuth:
    """
    Verifies GitHub CLI authentication status.

    Checks if gh CLI is installed and authenticated by running `gh auth status`.
    """

    def verify(self) -> GitHubCredentials:
        """
        Verify GitHub CLI authentication.

        Returns:
            GitHubCredentials with verified=True if authenticated.

        Raises:
            GitHubAuthError: If gh CLI is not installed or not authenticated.
        """
        # Check if gh is installed
        try:
            result = subprocess.run(
                ["gh", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                raise GitHubAuthError(
                    "GitHub CLI (gh) is not properly installed. "
                    "Please install gh: https://github.com/cli/cli#installation",
                    reason="not_installed",
                )
        except FileNotFoundError:
            raise GitHubAuthError(
                "GitHub CLI (gh) is not installed. "
                "Please install gh: https://github.com/cli/cli#installation",
                reason="not_installed",
            )
        except subprocess.TimeoutExpired:
            raise GitHubAuthError(
                "GitHub CLI (gh) check timed out. Please verify gh is installed correctly.",
                reason="timeout",
            )

        # Check authentication status
        try:
            result = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            raise GitHubAuthError(
                "GitHub CLI authentication check timed out. Please verify gh is working.",
                reason="timeout",
            )

        output = result.stdout + result.stderr

        # Check for "Logged in" indicator
        # gh auth status outputs different formats based on state
        if result.returncode == 0 and (
            "Logged in to" in output
            or "you are authenticated as" in output.lower()
            or "✓" in output
        ):
            # Extract username if present
            username = None
            for line in output.split("\n"):
                # Format 1: "Logged in to github.com as <username>"
                if " as " in line and "Logged in to" in line:
                    parts = line.split(" as ")
                    if len(parts) > 1:
                        username = parts[1].strip().split()[0]
                        break
                # Format 2: "Logged in to github.com account <username>"
                elif " account " in line and "Logged in to" in line:
                    parts = line.split(" account ")
                    if len(parts) > 1:
                        username = parts[1].strip().split()[0]
                        break

            return GitHubCredentials(verified=True, username=username)
        else:
            # Not authenticated
            if "not logged in" in output.lower():
                raise GitHubAuthError(
                    "GitHub CLI (gh) is not authenticated. "
                    "Please run: gh auth login",
                    reason="not_authenticated",
                )
            else:
                raise GitHubAuthError(
                    f"GitHub CLI authentication check failed. "
                    f"Please verify gh is properly configured. "
                    f"Run 'gh auth login' to authenticate.",
                    reason="unknown",
                )

    def is_verified(self) -> bool:
        """
        Quick check if gh CLI is authenticated.

        Returns:
            True if authenticated, False if not authenticated.
            Raises GitHubAuthError for installation issues (timeout, not installed).
        """
        creds = self.verify()
        return creds.verified