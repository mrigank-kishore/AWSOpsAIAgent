# Architecture

## Overview

This project should implement an AWS-first, production-style AIOps architecture that is safe by default and demoable end to end.

The core workflow is:

Observe -> Analyze -> Plan -> Act -> Verify

The system should maximize use of managed AWS services and minimize bespoke orchestration code.

## Architecture Principles

- Prefer AWS managed services over custom components
- Separate reasoning from execution
- Keep remediation safe through policy validation and approvals
- Make local simulation mode and AWS mode share the same contracts
- Preserve strong observability and auditability

## Reference Architecture

```text
Simulated Services / AWS Workloads
        |
        v
CloudWatch Logs/Metrics + Events
        |
        v
EventBridge Incident Event
        |
        v
Step Functions Incident Workflow
        |
        +--> Detection / Enrichment Lambda
        |
        +--> Retrieval + RCA Lambda
        |        |
        |        +--> OpenSearch
        |        +--> DynamoDB Incident Memory
        |        +--> S3 Raw Artifacts
        |        +--> Bedrock
        |
        +--> Policy + Decision Lambda
        |
        +--> Approval Step
        |        |
        |        +--> CLI / API approval adapter
        |
        +--> Action Executor Lambda
        |
        +--> Verification Lambda
        |
        +--> Incident Outcome Writer
                 |
                 +--> DynamoDB
                 +--> S3
                 +--> OpenSearch
```

## Component Breakdown

### Workload Layer

Use 2-3 services to simulate realistic failure modes. Recommended examples are `gateway-service`, `orders-service`, and `checkout-service`.

Recommended hosting:

- `ECS Fargate` for the AWS version
- local Docker Compose or in-process simulation for local mode

### Telemetry Layer

Responsibilities:

- Collect logs, metrics, and deployment events
- Collect CI/CD workflow evidence and change records needed for diagnosis
- Normalize telemetry for analysis
- Persist raw and searchable forms

AWS services:

- `CloudWatch Logs`
- `CloudWatch Metrics`
- `EventBridge`
- `S3`
- `OpenSearch`

### Detection Layer

Responsibilities:

- Evaluate incoming signals
- Detect threshold breaches and simple patterns
- Generate a normalized incident object

Detection types:

- sustained CPU threshold breach
- rising memory trend
- HTTP 5xx spike

### Retrieval and RCA Layer

Responsibilities:

- Fetch relevant current telemetry
- Retrieve similar incidents
- Correlate deployment history and system events
- Correlate GitHub Actions workflow logs with incident timing
- Pull remediation runbooks and known-fix documentation
- Pull recent change-management records for approved changes
- Produce a probable cause with confidence and evidence summary

AWS services:

- `OpenSearch`
- `DynamoDB`
- `S3`
- `Bedrock`

Recommended indexed evidence sources:

- CloudWatch and application telemetry
- historical incident memory and action outcomes
- exported GitHub Actions logs and workflow metadata
- remediation runbooks and incident documentation
- change-management records and deployment approvals

### Decision and Policy Layer

Responsibilities:

- Choose from approved actions only
- Enforce risk and approval policies
- Reject unsupported or unsafe actions
- Provide a clear rationale

Important boundary:

The decision engine can recommend. It cannot directly execute.

### Execution Layer

Responsibilities:

- Validate action payloads
- Execute approved remediations in simulation or AWS mode
- Return execution result and metadata

Initial actions:

- restart service
- scale service
- rollback deployment

### Verification Layer

Responsibilities:

- Re-check telemetry after remediation
- Compare pre-action and post-action state
- Decide resolved, retry, or escalate

### Memory Layer

Responsibilities:

- Persist incidents and outcomes
- Store action history
- Support future retrieval

AWS services:

- `DynamoDB`
- `S3`
- `OpenSearch`

### Approval Layer

Responsibilities:

- Pause workflow when high-risk action requires approval
- Collect approve/reject decision
- Resume workflow with audit trail

Initial interface:

- CLI approval flow

## Security and Guardrails

- LLM has no direct infrastructure permissions
- actions come from a fixed registry
- payload validation before execution
- rollback requires approval
- audit logs for all decisions and actions
- least-privilege IAM roles

## Local Mode vs AWS Mode

Design a thin adapter boundary:

- local mode
  - local files instead of S3
  - local search stub instead of OpenSearch if needed at first
  - local state machine instead of Step Functions if needed at first
  - local action adapters instead of Lambda-backed actions

- AWS mode
  - real managed services with the same interfaces

This keeps development fast without losing the target architecture.
