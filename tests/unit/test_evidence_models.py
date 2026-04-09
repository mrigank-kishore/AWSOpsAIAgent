from datetime import datetime

from aiops_agent.common.models import EvidenceRecord, EvidenceSourceType, Incident, IncidentType


def test_incident_supports_source_aware_evidence() -> None:
    incident = Incident(
        incident_id="inc-123",
        incident_type=IncidentType.SERVICE_CRASH,
        service="checkout-service",
        summary="5xx spike after deployment",
        detected_at=datetime(2026, 1, 1, 12, 0, 0),
        evidence=[
            EvidenceRecord(
                source_type=EvidenceSourceType.GITHUB_ACTIONS,
                source_id="workflow-run-42",
                summary="Deployment workflow failed health checks",
                content="Health-check job failed after rollout.",
            ),
            EvidenceRecord(
                source_type=EvidenceSourceType.CHANGE_MANAGEMENT,
                source_id="chg-1001",
                summary="Approved production rollout for checkout-service",
                content="Change request approved for version 2026.01.01.",
            ),
        ],
    )

    assert incident.evidence[0].source_type == EvidenceSourceType.GITHUB_ACTIONS
    assert incident.evidence[1].source_type == EvidenceSourceType.CHANGE_MANAGEMENT
