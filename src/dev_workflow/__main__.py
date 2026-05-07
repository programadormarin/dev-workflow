"""CLI entry point for `python -m src.dev_workflow`.

Usage:
    python -m src.dev_workflow PROJ-123

Arguments:
    ticket_key: Jira ticket key to process (e.g. PROJ-123)

Environment variables required:
    JIRA_EMAIL: Jira account email
    JIRA_API_TOKEN: Jira API token
    JIRA_URL: Jira Cloud instance URL

The entry point validates environment variables and starts the DeliveryFlow.
Full implementation in Phase 2 (AUTH-01, AUTH-03).
"""
import sys
from src.dev_workflow import DeliveryFlow

__all__ = ["DeliveryFlow"]


def main() -> None:
    """Main entry point for python -m src.dev_workflow."""
    if len(sys.argv) < 2:
        print("Usage: python -m src.dev_workflow <ticket_key>")
        print("Example: python -m src.dev_workflow PROJ-123")
        sys.exit(1)

    ticket_key = sys.argv[1]
    print(f"[dev_workflow] Starting pipeline for {ticket_key}")
    print("[dev_workflow] Full implementation in Phase 3. For now, run:")
    print(f"  python -c 'from src.dev_workflow import DeliveryFlow; print(DeliveryFlow)'")


if __name__ == "__main__":
    main()
