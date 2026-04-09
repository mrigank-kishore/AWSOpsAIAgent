from aiops_agent.orchestration.workflow import build_workflow_summary


def test_workflow_summary_has_required_steps() -> None:
    summary = build_workflow_summary()
    assert summary["workflow"] == ["observe", "analyze", "plan", "act", "verify"]
