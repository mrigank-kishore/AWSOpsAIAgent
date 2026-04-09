from __future__ import annotations


def build_workflow_summary() -> dict[str, object]:
    return {
        "workflow": ["observe", "analyze", "plan", "act", "verify"],
        "aws_targets": {
            "event_bus": "Amazon EventBridge",
            "orchestrator": "AWS Step Functions",
            "actions": "AWS Lambda",
            "memory": "Amazon DynamoDB",
            "search": "Amazon OpenSearch Service",
            "artifacts": "Amazon S3",
            "reasoning": "Amazon Bedrock",
        },
        "required_actions": ["restart_service", "scale_service", "rollback_deployment"],
        "required_incidents": ["high_cpu", "memory_leak", "service_crash"],
    }
