from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class IncidentType(str, Enum):
    HIGH_CPU = "high_cpu"
    MEMORY_LEAK = "memory_leak"
    SERVICE_CRASH = "service_crash"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DecisionStatus(str, Enum):
    RESOLVED = "resolved"
    RETRY = "retry"
    ESCALATE = "escalate"


class EvidenceSourceType(str, Enum):
    TELEMETRY = "telemetry"
    INCIDENT_MEMORY = "incident_memory"
    GITHUB_ACTIONS = "github_actions"
    REMEDIATION_DOC = "remediation_doc"
    CHANGE_MANAGEMENT = "change_management"


class TelemetrySample(BaseModel):
    service: str
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    dimensions: dict[str, str] = Field(default_factory=dict)


class EvidenceRecord(BaseModel):
    source_type: EvidenceSourceType
    source_id: str
    summary: str
    content: str
    collected_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class Incident(BaseModel):
    incident_id: str
    incident_type: IncidentType
    service: str
    summary: str
    detected_at: datetime
    evidence: list[EvidenceRecord] = Field(default_factory=list)
    retry_count: int = 0


class RcaResult(BaseModel):
    probable_cause: str
    confidence_score: float
    evidence_summary: str
    evidence_sources: list[EvidenceSourceType] = Field(default_factory=list)
    related_incident_ids: list[str] = Field(default_factory=list)


class ActionRecommendation(BaseModel):
    action_id: str
    rationale: str
    confidence_score: float
    risk_level: RiskLevel
    requires_approval: bool
    estimated_cost_impact: str
    rejected_alternatives: list[str] = Field(default_factory=list)


class ActionExecutionResult(BaseModel):
    action_id: str
    target: str
    success: bool
    message: str
    executed_at: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)


class VerificationResult(BaseModel):
    status: DecisionStatus
    summary: str
    checked_at: datetime
    metrics: dict[str, float] = Field(default_factory=dict)
