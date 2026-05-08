"""Smoke tests for DeliveryFlow orchestrator."""
from unittest.mock import MagicMock
from src.dev_workflow.application.delivery_flow import (
    DeliveryFlow,
    DeliveryFlowError,
)


class TestDeliveryFlow:
    """Smoke tests for DeliveryFlow.

    These tests verify the orchestrator interface. Full pipeline tests
    require infrastructure adapters implemented in later phases.
    """

    def test_instantiation_with_ports(self):
        """Should instantiate DeliveryFlow with Jira and GitHub ports."""
        mock_jira = MagicMock()
        mock_github = MagicMock()
        flow = DeliveryFlow(
            jira_port=mock_jira,
            github_port=mock_github,
            verbose=False,
        )
        assert flow.jira_port is mock_jira
        assert flow.github_port is mock_github
        assert flow.verbose is False

    def test_instantiation_verbose(self):
        """Should instantiate with verbose=True."""
        mock_jira = MagicMock()
        mock_github = MagicMock()
        flow = DeliveryFlow(
            jira_port=mock_jira,
            github_port=mock_github,
            verbose=True,
        )
        assert flow.verbose is True

    def test_run_method_exists(self):
        """Should have a run method accepting ticket_key."""
        mock_jira = MagicMock()
        mock_github = MagicMock()
        flow = DeliveryFlow(jira_port=mock_jira, github_port=mock_github)
        assert hasattr(flow, "run")
        assert callable(flow.run)

    def test_stage_methods_exist(self):
        """Should have all 7 stage methods."""
        flow = DeliveryFlow(MagicMock(), MagicMock())
        stage_methods = [
            "_run_fetch_stage",
            "_run_analyze_stage",
            "_run_enrich_stage",
            "_run_document_stage",
            "_run_implement_stage",
            "_run_qa_stage",
            "_run_pr_stage",
        ]
        for method_name in stage_methods:
            assert hasattr(flow, method_name), f"Missing method: {method_name}"

    def test_delivery_flow_error_exists(self):
        """DeliveryFlowError exception should be importable."""
        assert issubclass(DeliveryFlowError, Exception)
