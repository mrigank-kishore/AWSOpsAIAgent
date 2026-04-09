# AWS AIOps Agent

An AWS-first, production-style agentic incident response system that detects, diagnoses, remediates, and verifies cloud incidents with guardrails.

This project is intentionally scoped for a strong demo and interview story:

- Detect common service incidents from telemetry
- Use retrieval-augmented reasoning for RCA
- Choose from safe, predefined remediation actions
- Require approval for risky actions
- Verify whether remediation worked
- Store the full incident lifecycle for future retrieval

## What We Are Building

The target system handles three incident classes:

- High CPU
- Memory leak
- Service crash / HTTP 5xx spike

The target response loop is:

Observe -> Analyze -> Plan -> Act -> Verify

The implementation should use AWS managed services as much as possible while keeping remediation safe by default through simulation mode and guardrails.

For RCA, the agent should reason over approved evidence sources, including:

- service telemetry and indexed application logs
- historical incident memory and prior outcomes
- GitHub Actions logs for build and deployment failures
- incident remediation documentation and runbooks
- change management records for recent approved changes

## AWS-Managed-Service Bias

The reference implementation should prefer:

- `CloudWatch` for logs, metrics, alarms, and dashboards
- `EventBridge` for incident events
- `Step Functions` for orchestration
- `Lambda` for workflow tasks and action adapters
- `S3` for raw log and artifact storage
- `OpenSearch` for indexed logs and retrieval
- `DynamoDB` for incident memory and workflow state
- `Bedrock` for RCA and action reasoning
- `ECS Fargate` or `App Runner` for simulated workloads
- `Secrets Manager` or `SSM Parameter Store` for config and secrets

## Core Scenarios

### 1. High CPU

- Detect sustained CPU threshold breach
- Infer likely capacity issue
- Recommend scaling
- Verify CPU returns to normal

### 2. Memory Leak

- Detect upward memory trend
- Infer likely leak or stale process state
- Recommend restart
- Verify memory resets

### 3. Service Crash / 5xx Spike

- Detect error spike
- Correlate with recent deployment
- Recommend rollback
- Require approval
- Verify errors normalize

## Proposed Architecture

The system should be split into clear domains:

1. `ingestion`
2. `detection`
3. `rca`
4. `agent`
5. `execution`
6. `verification`
7. `memory`

For a fuller architecture view, see [docs/architecture.md](/c:/workspaces/AwsAIOpsAgent/docs/architecture.md).

## Recommended Repository Shape

```text
.
|-- README.md
|-- requirement.md
|-- AGENT_GUIDE.md
|-- docs/
|   |-- architecture.md
|   `-- implementation-plan.md
|-- infra/
|-- services/
|-- src/
|-- simulations/
|-- prompts/
|-- tests/
`-- scripts/
```

## Suggested Implementation Strategy

Build in layers:

1. Implement local simulation mode first so the full workflow can be demoed quickly.
2. Keep interfaces cloud-ready so local adapters can later map to AWS services.
3. Add AWS managed-service integrations behind those interfaces.
4. Preserve strict guardrails between LLM reasoning and action execution.

## Safety Rules

- The LLM may recommend actions, but never execute infrastructure changes directly.
- All actions must come from a deterministic whitelist.
- All action payloads must be validated before execution.
- Rollback requires approval.
- Retry attempts must be capped.
- Every decision and result must be logged.

## Definition of Done for V1

V1 is complete when:

- All three incident scenarios work end-to-end
- The agent outputs a readable reasoning trace
- Rollback requires approval
- Incident memory is persisted and reused for RCA
- The system supports `resolved`, `retry`, and `escalate` outcomes
- The architecture clearly uses AWS managed services by default

## Documents in This Repo

- [requirement.md](/c:/workspaces/AwsAIOpsAgent/requirement.md)
- [AGENT_GUIDE.md](/c:/workspaces/AwsAIOpsAgent/AGENT_GUIDE.md)
- [docs/architecture.md](/c:/workspaces/AwsAIOpsAgent/docs/architecture.md)
- [docs/implementation-plan.md](/c:/workspaces/AwsAIOpsAgent/docs/implementation-plan.md)

## Recommended First Build Slice

1. Create 2-3 sample services with emitted logs and metrics.
2. Add threshold-based detection for the three required incidents.
3. Persist incidents and historical outcomes.
4. Build a simple RCA pipeline using telemetry, GitHub Actions logs, remediation docs, change records, and incident memory.
5. Build a policy-driven decision engine with action whitelist.
6. Add local action adapters for restart, scale, and rollback.
7. Add verification logic and a CLI approval prompt.
8. Replace local adapters incrementally with AWS integrations.
