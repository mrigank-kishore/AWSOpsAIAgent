# AWS AIOps Agent Requirements

## 1. Purpose

Build a production-style, agentic AIOps system that can detect, diagnose, remediate, and verify cloud incidents with guardrails. The solution should be interview-friendly, demo-friendly, and architected with AWS managed services wherever practical.

The system must show an end-to-end loop:

Observe -> Analyze -> Plan -> Act -> Verify

The implementation should default to safe simulation for remediation while still using cloud-native patterns and production-ready operational controls.

## 2. Product Goals

### Primary Goal

Create an AWS-first incident response platform that:

- Ingests telemetry from simulated or real services
- Detects anomalies for a limited set of common incidents
- Performs RCA using telemetry and historical incident memory
- Chooses a validated remediation action through an agentic loop
- Requires approval for high-risk actions
- Verifies whether remediation worked
- Stores the full incident lifecycle for future retrieval

### Secondary Goals

- Maximize use of managed AWS services
- Keep scope small enough to complete and demo well
- Make architecture extensible for future incident types and actions
- Preserve strong operational guardrails around LLM usage and execution

## 3. Scope

### In Scope

- AWS-centric architecture
- 2-3 simulated microservices
- 3 incident types:
  - High CPU
  - Memory leak
  - Service crash / HTTP 5xx spike
- Local demo mode and AWS deployment mode
- Agent reasoning trace and action justification
- Human approval flow for high-risk actions
- Incident memory for future RCA and recommendations

### Out of Scope

- Multi-cloud support
- Full real-time streaming platform
- Advanced ML anomaly detection
- Full visual dashboard
- Unrestricted LLM tool execution
- Real destructive production operations without explicit approval and safety checks

## 4. AWS-First Architecture Requirements

The solution should prefer managed services over custom infrastructure. The reference architecture should use the following as defaults unless a strong reason exists not to:

- `Amazon CloudWatch` for metrics, logs, alarms, and dashboards
- `Amazon EventBridge` for incident and workflow events
- `AWS Step Functions` for orchestration of the incident lifecycle
- `AWS Lambda` for lightweight analysis, action adapters, and verification tasks
- `Amazon S3` for raw logs, incident artifacts, and replayable simulation data
- `Amazon OpenSearch Service` or `OpenSearch Serverless` for indexed log search and retrieval
- `Amazon DynamoDB` for incident memory, action history, and state tracking
- `Amazon Bedrock` for RCA and action recommendation reasoning
- `Amazon ECS Fargate` or `AWS App Runner` for simulated services
- `AWS Systems Manager Parameter Store` or `AWS Secrets Manager` for config and secrets
- `AWS IAM` for least-privilege execution roles
- `AWS KMS` for encryption at rest where relevant
- `AWS X-Ray` and CloudWatch structured logs for tracing and observability

### AWS Usage Principle

The project should demonstrate cloud-native thinking by composing managed services instead of building bespoke schedulers, pipelines, or state engines in application code.

## 5. Functional Requirements

## 5.1 Telemetry Ingestion

The system must ingest logs, metrics, and events from simulated or real workloads.

### Required Signals

- CPU utilization spikes
- Memory growth / leak trend
- HTTP 5xx error spikes

### Required Sources

- Application logs
- Service metrics
- Incident and deployment events
- GitHub Actions workflow and job logs for recent build or deploy runs
- Incident remediation documentation and runbooks
- Change management records for recent approved changes and rollouts

### Required Storage

- Raw logs in `S3` or local file storage in local-dev mode
- Indexed/searchable logs in `OpenSearch`
- Time-series metrics in `CloudWatch`

## 5.2 Anomaly Detection

The system must detect abnormal patterns and trigger incident workflows.

### Initial Detection Methods

- Static threshold detection
- Simple moving average or rolling baseline anomaly detection

### Required Behavior

- Trigger an incident when conditions are met
- Capture the signal, threshold, service, and detection timestamp
- Emit a normalized incident event onto EventBridge or equivalent local event bus

## 5.3 Root Cause Analysis

The system must generate a probable cause using retrieval-augmented reasoning over current telemetry and historical incidents.

### Inputs

- Current metrics and logs
- Recent deployment / change events
- GitHub Actions logs tied to recent CI/CD activity
- Historical incidents
- Past actions and outcomes
- Incident remediation documentation and runbooks
- Change management records

### Outputs

- Probable cause
- Confidence score
- Evidence summary
- Similar prior incidents if available

### LLM Usage Constraints

- LLM may be used for RCA reasoning and summarization
- LLM must not execute commands or choose arbitrary tools
- All retrieval context must come from approved indexed sources
- Approved indexed sources must include telemetry, incident memory, GitHub Actions logs, remediation docs, and change management data when available

## 5.4 Agentic Decision Engine

The system must implement a transparent decision loop:

Observe -> Analyze -> Plan -> Act -> Verify

### Required Agent Capabilities

- Evaluate current incident state
- Select from a predefined set of safe actions
- Justify why the selected action is preferable to alternatives
- Consider confidence, blast radius, and estimated cost
- Respect retry limits and escalation rules

## 5.5 Remediation Execution

The system must support at least three remediation actions:

- Restart service
- Scale service
- Rollback deployment

### Execution Layer

- `Lambda` functions in AWS mode
- Local Python action adapters in local mode

### Action Constraints

- Actions must come from a whitelist
- Inputs must be schema-validated
- Actions must be logged with request, outcome, and timing
- Real execution must be separable from simulation mode

## 5.6 Verification Layer

The system must verify whether remediation improved the incident.

### Required Behavior

- Re-check key metrics after action execution
- Compare before vs after state
- Decide one of:
  - Resolved
  - Retry
  - Escalate

## 5.7 Human-in-the-Loop Approval

Human approval is mandatory for high-risk actions.

### Minimum Required Approval Cases

- Rollback deployment
- Any action marked high blast radius

### Approval Interfaces

- CLI approval flow is required
- Optional minimal web UI may be added later

## 5.8 Incident Memory

The system must persist incident knowledge for reuse.

### Required Stored Fields

- Incident metadata
- Detection signals
- RCA summary
- Confidence score
- Action taken
- Approval status
- Verification result
- Final outcome
- Timestamps

### Storage Targets

- Structured state in `DynamoDB`
- Supporting artifacts in `S3`
- Searchable context in `OpenSearch`

## 6. Non-Functional Requirements

### Reliability

- The system must prevent infinite remediation loops
- Retry count must be capped, default `max 2`
- Every workflow execution must be idempotent where practical

### Observability

Every workflow step must emit structured logs, including:

- Incident id
- Service name
- Detection details
- RCA result
- Agent reasoning summary
- Action request
- Approval status
- Verification result
- Final disposition

### Security

- Least-privilege IAM roles
- No direct LLM access to infrastructure APIs
- Action execution only through validated adapters
- Secrets stored in Parameter Store or Secrets Manager

### Cost Awareness

The system must estimate the cost impact of actions, even if approximate.

Examples:

- Scaling from 2 to 4 tasks on ECS Fargate
- Additional OpenSearch usage
- Bedrock invocation cost
- Extra Lambda / Step Functions executions

## 7. Guardrails

- LLM only reasons over provided context
- Final action execution must always pass through deterministic policy code
- Maximum remediation attempts per incident: `2`
- Rollback requires approval
- Verification must complete before incident is marked resolved

## 8. Target Demo Scenarios

### Scenario 1: High CPU

- Detect CPU spike
- RCA identifies probable capacity issue
- Agent recommends `scale_service`
- Verification shows CPU decreased

### Scenario 2: Memory Leak

- Detect increasing memory trend
- RCA identifies memory leak pattern
- Agent recommends `restart_service`
- Verification shows memory reset

### Scenario 3: Service Crash / 5xx Spike

- Detect error spike
- RCA links failure to recent deployment
- Agent recommends `rollback_deployment`
- Human approval is requested
- Verification shows error rate normalizes

## 9. Success Criteria

### Functional Success

The system is successful when all three target scenarios can be demonstrated end-to-end with:

- Detection
- RCA
- Action recommendation
- Safe execution
- Verification
- Final outcome recording

### Agent Quality

For each incident, the system must expose:

- Reasoning trace
- Evidence used
- Why the chosen action was selected
- Why other actions were not selected
- Whether approval was required and why

### Architecture Quality

The repository should clearly demonstrate:

- Separation of concerns
- AWS managed service alignment
- Safety boundaries between reasoning and execution
- A clean path to add new actions and incident types

### Demonstration Quality

A reviewer should be able to:

- Start the simulation or local stack
- Trigger each incident scenario
- View incident and agent logs
- See action decisions
- Compare before vs after metrics
- Inspect incident memory records

## 10. Recommended Production-Style Capabilities

- Dead-letter handling for failed workflow steps
- Idempotency keys for incident workflows
- Structured JSON logging
- Environment-based configuration
- Infrastructure as code
- CI checks and tests
- Prompt versioning
- Audit trail for approvals and actions
- Feature flag to switch between simulation and AWS execution
- Runbooks and architecture documentation

## 11. Acceptance Criteria

The first complete version is accepted when:

- All three target scenarios run successfully
- Approval gating exists for rollback
- Retry limit prevents infinite loops
- Incident memory is persisted and reused
- Agent reasoning is visible in logs or CLI output
- The architecture clearly favors AWS managed services
- Another coding agent can continue implementation without guesswork
