"""Delivery Flow orchestrator — coordinates the Jira-to-PR pipeline.

Sequential pipeline: Fetch → Analyze → Enrich → Document → Implement → QA → PR

Each stage runs one crew. Crews receive explicit outputs from the previous stage
(via context) — no implicit shared state. Flow state persists for crash recovery
(@persist decorator) so interrupted runs can resume.

Per FLOW-01, FLOW-02, FLOW-03, FLOW-04:
- Sequential pipeline with explicit stage outputs
- State persistence for crash recovery
- Halt on stage failure with clear error

Usage:
    flow = DeliveryFlow(jira_port=jira_adapter, github_port=github_adapter)
    result = flow.run(ticket_key="PROJ-123")
"""
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.dev_workflow.ports import JiraPort, GitHubPort

CREWS_DIR = Path(__file__).parent.parent / "crews"


class DeliveryFlow:
    """Main orchestrator for the Jira-to-PR delivery pipeline.

    Coordinates all 7 pipeline stages sequentially. Each stage:
    1. Receives explicit context from the previous stage
    2. Runs its crew with that context
    3. Produces output consumed by the next stage

    State is persisted after each stage for crash recovery.

    Attributes:
        jira_port: Jira service adapter implementing JiraPort
        github_port: GitHub service adapter implementing GitHubPort
        verbose: Enable verbose logging for all stages
    """

    def __init__(
        self,
        jira_port: "JiraPort",
        github_port: "GitHubPort",
        verbose: bool = False,
    ) -> None:
        self.jira_port = jira_port
        self.github_port = github_port
        self.verbose = verbose
        self._stage_results: dict[str, object] = {}

    def run(self, ticket_key: str) -> dict:
        """Execute the full delivery pipeline for a Jira ticket.

        Args:
            ticket_key: Jira ticket key, e.g. 'PROJ-123'

        Returns:
            dict with pipeline results including:
            - ticket: JiraTicket
            - analysis: AnalysisOutput (Pydantic model)
            - enriched: EnrichedRequirements (Pydantic model)
            - documentation: str (path to generated docs)
            - implementation: ImplementationPlan (Pydantic model)
            - qa_results: QAResults (Pydantic model)
            - pr_url: str (GitHub PR URL)

        Raises:
            DeliveryFlowError: If any stage fails
            JiraNotFoundError: If ticket does not exist
        """
        raise NotImplementedError(
            "DeliveryFlow.run() implemented in Phase 3. "
            "This stub provides the interface for Phase 1 structure validation."
        )

    def _run_fetch_stage(self, ticket_key: str) -> dict:
        """Run Fetch crew — fetch Jira ticket data."""
        raise NotImplementedError("Fetch stage implemented in Phase 3")

    def _run_analyze_stage(self, ticket_data: dict) -> dict:
        """Run Analyze crew — extract requirements from ticket."""
        raise NotImplementedError("Analyze stage implemented in Phase 3")

    def _run_enrich_stage(self, analysis: dict) -> dict:
        """Run Enrich crew — fill gaps in sparse tickets."""
        raise NotImplementedError("Enrich stage implemented in Phase 3")

    def _run_document_stage(self, enriched: dict) -> dict:
        """Run Document crew — generate ADR/spec from requirements."""
        raise NotImplementedError("Document stage implemented in Phase 3")

    def _run_implement_stage(self, documentation: dict) -> dict:
        """Run Implement crew — break work into tasks."""
        raise NotImplementedError("Implement stage implemented in Phase 3")

    def _run_qa_stage(self, implementation: dict) -> dict:
        """Run QA crew — validate code changes."""
        raise NotImplementedError("QA stage implemented in Phase 3")

    def _run_pr_stage(self, qa_results: dict) -> dict:
        """Run PR crew — create GitHub Pull Request."""
        raise NotImplementedError("PR stage implemented in Phase 3")


class DeliveryFlowError(Exception):
    """Raised when the delivery flow encounters an error."""
    pass
