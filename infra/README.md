# Infrastructure Notes

Prefer managed AWS services for the production deployment path:

- EventBridge for incident events
- Step Functions for orchestration
- Lambda for task execution
- DynamoDB for incident state
- OpenSearch for retrieval
- S3 for artifacts
- Bedrock for reasoning
- ECS Fargate or App Runner for sample workloads

Add Terraform or CDK here once implementation begins.
