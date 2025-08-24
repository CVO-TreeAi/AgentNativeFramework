# Service Down - Incident Response Runbook

## Summary
Complete service outage where AgentNativeFramework is unresponsive or returning 5xx errors consistently.

## Prerequisites
- Kubernetes cluster access
- Monitoring system access (Grafana/Prometheus)
- Log aggregation access
- PagerDuty/alerting system access

## Detection

### Alert Conditions
- `ServiceDown` alert firing
- `up{job="agent-native-framework"} == 0`
- Health check endpoints returning 5xx or timing out
- User reports of complete service unavailability

### Symptoms
- All pods showing as `NotReady` or `CrashLoopBackOff`
- Health endpoints (`/health/live`, `/health/ready`) unreachable
- Zero successful requests in monitoring dashboards
- High number of 5xx responses

## Investigation

### Step 1: Check Pod Status
```bash
# Check deployment status
kubectl get deployment agent-native-framework
kubectl describe deployment agent-native-framework

# Check pod status
kubectl get pods -l app=agent-native-framework
kubectl describe pods -l app=agent-native-framework
```

### Step 2: Review Pod Logs
```bash
# Get logs from all pods
kubectl logs -l app=agent-native-framework --tail=100

# Check for specific error patterns
kubectl logs -l app=agent-native-framework --tail=500 | grep -i "error\|exception\|fatal"

# Check previous pod logs if pods are restarting
kubectl logs -l app=agent-native-framework --previous
```

### Step 3: Check Resource Utilization
```bash
# Check node resources
kubectl describe nodes

# Check pod resource usage
kubectl top pods -l app=agent-native-framework

# Check for resource quotas
kubectl describe resourcequota
```

### Step 4: Validate Configuration
```bash
# Check ConfigMaps
kubectl get configmap agent-config -o yaml

# Check Secrets
kubectl get secret agent-secrets

# Validate environment variables
kubectl exec -it deployment/agent-native-framework -- env | grep -E "(ANTHROPIC|LOG|AGENT)"
```

### Step 5: Check Dependencies
```bash
# Test external API connectivity
kubectl exec -it deployment/agent-native-framework -- curl -I https://api.anthropic.com/v1/health

# Check service accounts and RBAC
kubectl get serviceaccount agent-native-framework
kubectl describe rolebinding,clusterrolebinding | grep agent-native-framework
```

## Response

### Immediate Actions

#### If Pods are CrashLoopBackOff:
1. **Identify the crash cause**:
   ```bash
   kubectl logs -l app=agent-native-framework --previous | tail -50
   ```

2. **Check for common issues**:
   - Missing or invalid API keys
   - Configuration errors
   - Resource limits too low
   - Dependency connectivity issues

3. **Quick fixes for known issues**:
   ```bash
   # Increase memory limits if OOMKilled
   kubectl patch deployment agent-native-framework -p '{"spec":{"template":{"spec":{"containers":[{"name":"agent-manager","resources":{"limits":{"memory":"4Gi"}}}]}}}}'
   
   # Restart deployment if configuration issue
   kubectl rollout restart deployment agent-native-framework
   ```

#### If No Pods Running:
1. **Check deployment scaling**:
   ```bash
   kubectl get deployment agent-native-framework
   kubectl scale deployment agent-native-framework --replicas=2
   ```

2. **Check for scheduling issues**:
   ```bash
   kubectl describe pods -l app=agent-native-framework | grep -A5 "Events:"
   ```

#### If Pods Running but Unhealthy:
1. **Check health endpoints locally**:
   ```bash
   kubectl port-forward deployment/agent-native-framework 8080:8080 &
   curl http://localhost:8080/health/live
   curl http://localhost:8080/health/ready
   ```

2. **Check service and ingress**:
   ```bash
   kubectl get service agent-native-framework
   kubectl describe service agent-native-framework
   kubectl get ingress
   ```

### Emergency Mitigation

#### Option 1: Rollback to Previous Version
```bash
# Check rollout history
kubectl rollout history deployment agent-native-framework

# Rollback to previous version
kubectl rollout undo deployment agent-native-framework

# Monitor rollback progress
kubectl rollout status deployment agent-native-framework
```

#### Option 2: Scale Up Replicas
```bash
# Scale up to increase availability
kubectl scale deployment agent-native-framework --replicas=4

# Monitor pod creation
kubectl get pods -l app=agent-native-framework -w
```

#### Option 3: Emergency Configuration Fix
```bash
# Update critical configuration
kubectl patch configmap agent-config -p '{"data":{"LOG_LEVEL":"DEBUG"}}'

# Force pod restart to pick up changes
kubectl rollout restart deployment agent-native-framework
```

## Resolution

### Step 1: Root Cause Analysis
1. **Analyze logs for errors**:
   ```bash
   # Extract and analyze error logs
   kubectl logs -l app=agent-native-framework --since=1h | grep -B5 -A5 "ERROR\|FATAL"
   ```

2. **Check system events**:
   ```bash
   kubectl get events --sort-by=.metadata.creationTimestamp | tail -20
   ```

3. **Review recent changes**:
   - Check deployment history
   - Review recent commits
   - Verify configuration changes

### Step 2: Implement Fix
Based on root cause:

#### Configuration Issues:
```bash
# Update ConfigMap
kubectl edit configmap agent-config

# Update Secret
kubectl edit secret agent-secrets

# Apply changes
kubectl rollout restart deployment agent-native-framework
```

#### Resource Issues:
```bash
# Update resource limits
kubectl patch deployment agent-native-framework -p '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "agent-manager",
          "resources": {
            "requests": {"memory": "1Gi", "cpu": "500m"},
            "limits": {"memory": "4Gi", "cpu": "2000m"}
          }
        }]
      }
    }
  }
}'
```

#### Code Issues:
```bash
# Deploy hotfix
kubectl set image deployment/agent-native-framework agent-manager=agent-native-framework:hotfix-v1.0.1

# Monitor deployment
kubectl rollout status deployment agent-native-framework
```

### Step 3: Verification
```bash
# Verify pods are healthy
kubectl get pods -l app=agent-native-framework

# Test health endpoints
curl http://agent-native-framework:8080/health/live
curl http://agent-native-framework:8080/health/ready

# Verify metrics endpoint
curl http://agent-native-framework:8000/metrics | head -20

# Test basic functionality
# (Add specific API tests here)
```

### Step 4: Monitor Recovery
1. **Watch key metrics**:
   - Pod restart count
   - Response time
   - Error rate
   - Active agent count

2. **Monitor for 30 minutes** to ensure stability

3. **Update monitoring dashboards** if needed

## Prevention

### Immediate Improvements
1. **Enhanced Health Checks**:
   - Add more comprehensive readiness checks
   - Implement startup probes for slow-starting pods
   - Add health check for external dependencies

2. **Improved Resource Management**:
   - Set appropriate resource requests and limits
   - Implement Horizontal Pod Autoscaler
   - Add resource monitoring alerts

3. **Configuration Management**:
   - Implement configuration validation
   - Add configuration drift detection
   - Use GitOps for configuration management

### Long-term Improvements
1. **Chaos Engineering**:
   - Regular chaos testing
   - Automated failure injection
   - Recovery time measurement

2. **Observability Enhancement**:
   - Distributed tracing implementation
   - Enhanced logging with correlation IDs
   - Custom metrics for business logic

3. **Deployment Pipeline**:
   - Automated testing in staging
   - Canary deployments
   - Automated rollback triggers

## Escalation

### Level 1: Immediate Escalation (0-15 minutes)
- **Trigger**: Service completely down
- **Action**: Page on-call engineer
- **Contact**: PagerDuty incident escalation

### Level 2: Management Escalation (15-30 minutes)
- **Trigger**: Cannot restore service within 15 minutes
- **Action**: Escalate to team lead and incident commander
- **Contact**: [Team Lead Contact], [Incident Commander]

### Level 3: Executive Escalation (30+ minutes)
- **Trigger**: Extended outage affecting customers
- **Action**: Escalate to engineering management
- **Contact**: [Engineering Manager], [CTO if applicable]

## Communication

### Internal Communication
1. **Update incident channel**: Post status updates every 15 minutes
2. **Update status page**: If customer-facing impact
3. **Notify stakeholders**: Keep relevant teams informed

### External Communication
1. **Customer notification**: If SLA breach imminent
2. **Status page update**: For planned maintenance or extended outages
3. **Post-incident communication**: Summary and prevention measures

## Post-Incident Actions

### Immediate (Within 24 hours)
1. **Write incident summary**
2. **Schedule postmortem meeting**
3. **Create action items for immediate fixes**

### Follow-up (Within 1 week)
1. **Conduct blameless postmortem**
2. **Document lessons learned**
3. **Update runbooks based on learnings**
4. **Implement immediate prevention measures**

### Long-term (Within 1 month)
1. **Complete all action items**
2. **Review and improve monitoring**
3. **Update disaster recovery procedures**
4. **Conduct training if needed**