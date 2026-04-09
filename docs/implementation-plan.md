# Implementation Plan

## Goal

Deliver a demoable AWS-first AIOps agent with clear production-ready patterns and guardrails, without overbuilding.

## Phase 1: Foundations

### Outcomes

- repository structure established
- typed domain models created
- configuration pattern defined
- local simulation mode bootstrapped

### Tasks

- create source folders by domain
- define schemas for incidents, RCA, actions, and verification
- add config loading for local and AWS modes
- define action registry and policy interfaces

## Phase 2: Simulation and Telemetry

### Outcomes

- 2-3 sample services exist
- telemetry can be produced consistently
- the 3 required incident scenarios can be triggered

### Tasks

- implement service simulators
- emit CPU, memory, and error signals
- persist raw logs
- add searchable log indexing abstraction

## Phase 3: Detection

### Outcomes

- threshold-based incident detection works
- incidents are normalized and persisted

### Tasks

- implement CPU threshold detector
- implement memory trend detector
- implement HTTP 5xx spike detector
- emit normalized incident events

## Phase 4: RCA and Retrieval

### Outcomes

- incident context can be assembled
- relevant history can be retrieved
- RCA outputs cause, confidence, and evidence

### Tasks

- define incident memory schema
- seed historical incidents
- implement retrieval against telemetry, incident memory, GitHub Actions logs, remediation docs, and change-management records
- add Bedrock-ready prompt contract or local stub

## Phase 5: Decision, Policy, and Approval

### Outcomes

- safe action recommendation works
- high-risk actions are gated

### Tasks

- implement decision engine
- implement cost and risk annotations
- add approval flow for rollback
- log rejected alternatives and rationale

## Phase 6: Execution and Verification

### Outcomes

- remediation actions run in local mode
- verification closes the loop

### Tasks

- implement restart adapter
- implement scale adapter
- implement rollback adapter
- implement post-action verification
- enforce retry limits and escalation

## Phase 7: AWS Integration

### Outcomes

- core interfaces have AWS-backed implementations
- the project clearly demonstrates managed-service usage

### Tasks

- map event bus to EventBridge
- map orchestration to Step Functions
- map memory to DynamoDB
- map artifacts to S3
- map search to OpenSearch
- map reasoning to Bedrock
- map action adapters to Lambda

## Phase 8: Production Readiness and Demo

### Outcomes

- architecture is reviewable
- system is testable
- demo scripts are smooth

### Tasks

- add unit tests for detectors, policy, and verification
- add integration tests for the 3 scenarios
- add IaC templates
- add demo scripts and seed data
- add structured logging and tracing

## Minimum Acceptance Gate

Do not move to polish until these are true:

- all 3 scenarios complete end-to-end
- rollback approval works
- retry cap works
- incident memory persists outcomes
- action reasoning is visible
- AWS target architecture is reflected in code boundaries
