"""dev_workflow — CrewAI-powered Jira-to-PR delivery orchestrator.

Sequential pipeline: Fetch → Analyze → Enrich → Document → Implement → QA → PR

Quick start:
    from src.dev_workflow import DeliveryFlow

    flow = DeliveryFlow(jira_port=jira_adapter, github_port=github_adapter)
    result = flow.run(ticket_key="PROJ-123")
"""
from src.dev_workflow.application.delivery_flow import DeliveryFlow
from src.dev_workflow.domain.models import JiraTicket, GitHubPR
from src.dev_workflow.infrastructure.adapters import (
    JiraAdapter,
    GitHubAdapter,
    LoggingAdapter,
)

__all__ = [
    "DeliveryFlow",
    "JiraTicket",
    "GitHubPR",
    "JiraAdapter",
    "GitHubAdapter",
    "LoggingAdapter",
]
__version__ = "0.1.0"
