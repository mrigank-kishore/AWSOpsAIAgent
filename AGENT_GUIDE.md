# Coding Agent Guide

## Purpose

This file is for the coding agent that will implement the system. Use it as a practical build guide, not a marketing document.

Read [requirement.md](/c:/workspaces/AwsAIOpsAgent/requirement.md) first. Then use this guide to decide implementation order and constraints.

## Primary Objective

Build a demoable, production-style AWS AIOps system with:

- Clear separation of concerns
- Strong safety boundaries
- AWS managed-service alignment
- End-to-end functionality for 3 incidents

## Build Priorities

Prioritize in this order:

1. End-to-end workflow correctness
2. Safety and guardrails
3. Clear architecture and interfaces
4. Demo quality and observability
5. AWS managed-service integrations
6. Polish and optimizations

## Key Assumptions

- Start with local simulation mode so the workflow is runnable without full AWS setup.
- Design all modules behind interfaces that can map to AWS implementations later.
- Default language can be Python unless the repo later needs a different stack.
- Infrastructure should be represented as code from early in the project.

## Non-Negotiable Constraints

- Do not let the LLM execute arbitrary shell commands or AWS APIs.
- Do not hardcode action behavior inside prompts.
- Do not couple decision logic directly to infrastructure SDK calls.
- Do not skip approval gating for rollback.
- Do not leave retries unbounded.

## Required Modules

Create explicit modules for:

- `ingestion`
- `detection`
- `rca`
- `agent`
- `execution`
- `verification`
- `memory`
- `policy`
- `approval`
- `common`

## Suggested Interfaces

Define contracts early. At minimum, create interfaces or abstract types for:

- telemetry provider
- incident detector
- retriever
- RCA engine
- decision engine
- action registry
- action executor
- verifier
- incident repository
- approval provider

This will make local and AWS-backed implementations swappable.

## Data Models to Introduce Early

Create stable schemas for:

- telemetry sample
- incident
- RCA result
- action recommendation
- action request
- action execution result
- verification result
- incident outcome
- approval request

Use typed models and validation.

## Minimal V1 Execution Flow

1. Simulator emits telemetry.
2. Detector raises incident.
3. Incident context is assembled.
4. RCA retrieves similar incidents and recent logs.
   It should also retrieve GitHub Actions logs, remediation runbooks, and change-management records when they are relevant to the incident.
5. Agent recommends one whitelisted action.
6. Policy checks whether approval is required.
7. Executor runs local simulation action.
8. Verifier evaluates post-action telemetry.
9. Incident memory is updated.

## Action Design Rules

Every action must declare:

- `action_id`
- `description`
- `risk_level`
- `allowed_targets`
- `input_schema`
- `requires_approval`
- `estimated_cost_model`
- `verification_strategy`

Recommended initial actions:

- `restart_service`
- `scale_service`
- `rollback_deployment`

## Reasoning Trace Requirements

For each decision, log:

- triggering signal
- supporting evidence
- similar historical incidents
- GitHub Actions evidence when CI/CD activity may be involved
- remediation guidance used
- recent change records considered
- chosen action
- rejected alternatives
- confidence score
- risk level
- whether approval is required

Keep the trace concise and structured.

## Production-Ready Capabilities to Include

- structured JSON logs
- environment-based config
- idempotency strategy
- retry policy
- audit trail
- secrets/config separation
- IaC placeholders or real templates
- test coverage for decision and policy logic

## Recommended Build Phases

### Phase 1

Create the domain models, folder structure, and local simulation pipeline.

### Phase 2

Implement threshold detection and incident persistence.

### Phase 3

Implement retrieval-backed RCA and agent decision logic.

### Phase 4

Implement action execution, approval gating, and verification.

### Phase 5

Integrate AWS managed services behind the same interfaces.

### Phase 6

Add observability, tests, IaC, and demo scripts.

## AWS Mapping Guidance

Prefer these mappings:

- telemetry metrics -> `CloudWatch`
- incident event bus -> `EventBridge`
- orchestration -> `Step Functions`
- action adapters -> `Lambda`
- artifact storage -> `S3`
- incident state -> `DynamoDB`
- searchable logs and memory -> `OpenSearch`
- reasoning model -> `Bedrock`

Use local adapters only where they simplify early development.

## Anti-Patterns to Avoid

- monolithic `main.py` orchestration
- action logic embedded inside prompt strings
- implicit state transitions
- untyped dictionaries passed across the system
- mixing simulator code with production adapters
- letting the agent reason without access to evidence

## Recommended Next Files to Add After This

Once implementation begins, add:

- `.env.example`
- `pyproject.toml` or language equivalent
- `infra/` templates
- `tests/`
- `scripts/demo_*`
- seed incident data under `data/` or `fixtures/`
