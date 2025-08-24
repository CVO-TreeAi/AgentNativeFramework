# AgentNativeFramework Operational Runbooks

## Overview

This directory contains operational runbooks for managing the AgentNativeFramework in production environments. Each runbook provides step-by-step procedures for common operational scenarios.

## Runbook Index

### Incident Response
- [Service Down](./incident-response/service-down.md)
- [High Error Rate](./incident-response/high-error-rate.md)
- [Performance Degradation](./incident-response/performance-degradation.md)
- [Agent Coordination Failures](./incident-response/coordination-failures.md)
- [Memory Leaks](./incident-response/memory-leaks.md)

### Routine Operations
- [Health Check Procedures](./routine/health-checks.md)
- [Log Analysis](./routine/log-analysis.md)
- [Capacity Planning](./routine/capacity-planning.md)
- [Agent Registry Management](./routine/agent-registry.md)

### Emergency Procedures
- [Emergency Shutdown](./emergency/emergency-shutdown.md)
- [Traffic Failover](./emergency/traffic-failover.md)
- [Data Recovery](./emergency/data-recovery.md)
- [Security Incident Response](./emergency/security-incident.md)

### Troubleshooting
- [Agent Activation Issues](./troubleshooting/agent-activation.md)
- [Circuit Breaker Issues](./troubleshooting/circuit-breakers.md)
- [Memory and Resource Issues](./troubleshooting/resource-issues.md)
- [Integration Problems](./troubleshooting/integrations.md)

## Runbook Template

Each runbook follows this standard template:

```markdown
# [Title]

## Summary
Brief description of the scenario and when to use this runbook.

## Prerequisites
- Required access levels
- Tools needed
- System requirements

## Detection
How to identify this issue:
- Alert conditions
- Symptoms
- Monitoring signals

## Investigation
Step-by-step investigation process:
1. First check
2. Secondary validation
3. Root cause analysis

## Response
Immediate response actions:
1. Containment
2. Mitigation
3. Recovery

## Resolution
Long-term resolution:
1. Root cause fix
2. Verification
3. Documentation

## Prevention
How to prevent recurrence:
- Process improvements
- System changes
- Monitoring enhancements

## Escalation
When and how to escalate:
- Contact information
- Escalation criteria
- Communication procedures
```

## Quick Reference

### Emergency Contacts
- **On-Call Engineer**: [PagerDuty/Slack Channel]
- **Team Lead**: [Contact Information]
- **Infrastructure Team**: [Contact Information]

### Key Systems
- **Monitoring**: Grafana Dashboard
- **Alerting**: Prometheus Alertmanager
- **Logs**: Elasticsearch/Kibana
- **Metrics**: Prometheus
- **Tracing**: Jaeger (if implemented)

### Common Commands

```bash
# Check service status
kubectl get pods -l app=agent-native-framework

# View recent logs
kubectl logs -l app=agent-native-framework --tail=100

# Check health endpoints
curl http://agent-native-framework:8080/health/live
curl http://agent-native-framework:8080/health/ready

# View metrics
curl http://agent-native-framework:8000/metrics

# Scale deployment
kubectl scale deployment agent-native-framework --replicas=N

# Restart pods
kubectl rollout restart deployment agent-native-framework
```

## Best Practices

1. **Always follow the runbook**: Don't improvise during incidents
2. **Document actions**: Log all actions taken during incidents
3. **Communicate status**: Keep stakeholders informed
4. **Post-incident review**: Always conduct postmortems
5. **Update runbooks**: Keep procedures current based on learnings

## Metrics and SLOs

### Service Level Objectives
- **Availability**: 99.9% uptime (8.77 hours downtime/year)
- **Response Time**: 95th percentile < 2 seconds
- **Agent Activation**: 99.5% success rate
- **Coordination Success**: 99% consensus achievement

### Error Budget Policy
- **Monthly Error Budget**: 43.2 minutes of downtime
- **Burn Rate Thresholds**:
  - Critical: >10x normal rate
  - High: >5x normal rate
  - Medium: >2x normal rate

### Key Metrics
- `agent_activations_total` - Agent activation counter
- `coordination_duration_seconds` - Coordination latency
- `active_agents_count` - Current active agents
- `circuit_breaker_state` - Circuit breaker status
- `health_status` - Overall system health

## Training

All team members should:
1. Complete runbook familiarization training
2. Practice incident response scenarios
3. Understand escalation procedures
4. Know how to access all necessary tools and systems

## Review Schedule

- **Weekly**: Review active incidents and runbook usage
- **Monthly**: Update runbooks based on new issues or changes
- **Quarterly**: Comprehensive runbook review and testing
- **Annually**: Full operational procedures audit