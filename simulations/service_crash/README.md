# Service Crash Simulation

Target outcome:

- HTTP 5xx spike after deployment event
- detector raises `service_crash`
- agent recommends `rollback_deployment`
- approval is required
