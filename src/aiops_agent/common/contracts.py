from __future__ import annotations

from typing import Protocol

from aiops_agent.common.models import (
    ActionExecutionResult,
    ActionRecommendation,
    EvidenceRecord,
    Incident,
    RcaResult,
    VerificationResult,
)


class IncidentDetector(Protocol):
    def detect(self) -> list[Incident]:
        """Return new incidents from the latest telemetry window."""


class Retriever(Protocol):
    def retrieve(self, incident: Incident) -> list[EvidenceRecord]:
        """Return supporting evidence for RCA."""


class RcaEngine(Protocol):
    def analyze(self, incident: Incident, evidence: list[EvidenceRecord]) -> RcaResult:
        """Build probable cause and confidence."""


class DecisionEngine(Protocol):
    def recommend(self, incident: Incident, rca: RcaResult) -> ActionRecommendation:
        """Recommend a validated action."""


class ActionExecutor(Protocol):
    def execute(self, recommendation: ActionRecommendation, incident: Incident) -> ActionExecutionResult:
        """Execute a whitelisted action."""


class Verifier(Protocol):
    def verify(self, incident: Incident, result: ActionExecutionResult) -> VerificationResult:
        """Check whether the action resolved the incident."""
