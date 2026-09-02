# Emergency Rollback

Quick recovery system for production failures with intelligent rollback to last stable state, database migration reversal, and incident reporting.

## Purpose
- Intelligent rollback to last stable state
- Database migration rollback
- Cache invalidation
- Team notification
- Incident report generation

## Workflow

### Phase 1: Rollback Trigger
1. **STOP** → "What needs to be rolled back?"
   ```
   1. Application deployment - Code and services
   2. Database changes - Migrations and data
   3. Configuration - Settings and environment
   4. Infrastructure - Servers and containers
   5. Everything - Full system rollback
   
   Choose scope (1-5):
   ```

2. **Urgency Assessment**
   - STOP → "Severity level? (critical/high/medium/low):"
   - STOP → "Users affected? (all/some/few):"
   - STOP → "Automatic rollback? (y/n):"
   - STOP → "Notify team? (y/n):"

### Phase 2: System State Assessment

#### Health Check
```bash
# Check service status
curl -f http://app.com/health || echo "Service DOWN"

# Check error rates
tail -n 1000 error.log | grep -c "ERROR"

# Check response times
curl -w "%{time_total}" -o /dev/null -s http://app.com

# Check database
psql -c "SELECT 1" || echo "Database DOWN"
```

#### Identify Last Stable State
```bash
# Find last successful deployment
kubectl rollout history deployment/app | grep "REVISION"

# Git tags for releases
git tag -l "v*" --sort=-version:refname | head -5

# Docker images
docker images myapp --format "table {{.Tag}}\t{{.CreatedAt}}"
```

### Phase 3: Application Rollback

#### Kubernetes Rollback
```bash
# Immediate rollback to previous
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=3

# Check rollback status
kubectl rollout status deployment/myapp

# Verify pods
kubectl get pods -l app=myapp
```

#### Docker Rollback
```bash
# Stop current containers
docker-compose down

# Update image tags
sed -i 's/myapp:latest/myapp:v1.2.3/' docker-compose.yml

# Start previous version
docker-compose up -d

# Verify
docker ps
```

#### Serverless Rollback
```bash
# AWS Lambda
aws lambda update-alias \
  --function-name myapp \
  --function-version $PREVIOUS_VERSION \
  --name production

# Vercel
vercel rollback

# Netlify
netlify rollback --site-id $SITE_ID
```

### Phase 4: Database Rollback

#### Migration Reversal
```bash
# Rails
rake db:rollback STEP=1

# Django
python manage.py migrate app_name previous_migration

# Node.js (Knex)
npx knex migrate:rollback

# Flyway
flyway undo
```

#### Data Recovery
```sql
-- PostgreSQL point-in-time recovery
SELECT pg_switch_wal();
SELECT pg_start_backup('rollback');

-- Restore from backup
pg_restore -d mydb backup_20240115.dump

-- MySQL binary log recovery
mysqlbinlog --stop-datetime="2024-01-15 10:30:00" \
  mysql-bin.000001 | mysql -u root -p
```

#### Transaction Rollback
```sql
-- Find and rollback long transactions
SELECT pid, now() - pg_stat_activity.query_start AS duration, query
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes';

-- Kill and rollback
SELECT pg_cancel_backend(pid);
SELECT pg_terminate_backend(pid);
```

### Phase 5: Configuration Rollback

#### Environment Variables
```bash
# Restore previous .env
cp .env.backup .env

# Kubernetes ConfigMap
kubectl rollout history configmap/app-config
kubectl apply -f configmap-previous.yaml

# AWS Parameter Store
aws ssm get-parameter-history --name /myapp/config
aws ssm put-parameter --name /myapp/config --value "$PREVIOUS_VALUE"
```

#### Feature Flags
```javascript
// Disable problematic features
const featureFlags = {
  newPaymentFlow: false,  // Rolled back
  improvedSearch: true,
  betaFeatures: false     // Disabled
};

// Update flag service
await flagService.update('newPaymentFlow', false);
```

### Phase 6: Cache and CDN

#### Clear Caches
```bash
# Redis
redis-cli FLUSHALL

# Memcached
echo "flush_all" | nc localhost 11211

# Application cache
curl -X POST http://app.com/api/cache/clear

# CDN purge
curl -X POST https://api.cloudflare.com/client/v4/zones/$ZONE/purge_cache \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"purge_everything":true}'
```

#### Invalidate Sessions
```javascript
// Clear all user sessions
await redis.del('sessions:*');

// Force re-authentication
app.post('/api/sessions/invalidate-all', async (req, res) => {
  await sessionStore.clear();
  res.json({ message: 'All sessions invalidated' });
});
```

### Phase 7: Traffic Management

#### Load Balancer Update
```bash
# Remove bad instances
aws elb deregister-instances-from-load-balancer \
  --load-balancer-name myapp \
  --instances i-bad1 i-bad2

# Update health check
aws elb configure-health-check \
  --load-balancer-name myapp \
  --health-check Target=HTTP:80/health
```

#### Blue-Green Switch
```yaml
# Switch traffic back to blue
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Changed from green
```

#### Circuit Breaker
```javascript
// Activate circuit breaker
const circuitBreaker = new CircuitBreaker(apiCall, {
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000
});

// Fallback to cached data
circuitBreaker.fallback(() => {
  return getCachedData();
});
```

### Phase 8: Monitoring and Verification

#### Health Monitoring
```javascript
// Continuous health check
setInterval(async () => {
  const health = await checkHealth();
  
  if (!health.ok) {
    console.error('Rollback verification failed:', health);
    await notifyOncall('Rollback health check failed');
  } else {
    console.log('System stable after rollback');
  }
}, 30000);  // Every 30 seconds
```

#### Metric Comparison
```javascript
// Compare metrics before/after
async function verifyRollback() {
  const currentMetrics = await getMetrics();
  const baselineMetrics = await getBaselineMetrics();
  
  const comparison = {
    errorRate: currentMetrics.errorRate / baselineMetrics.errorRate,
    responseTime: currentMetrics.responseTime / baselineMetrics.responseTime,
    throughput: currentMetrics.throughput / baselineMetrics.throughput
  };
  
  if (comparison.errorRate > 1.1) {
    console.warn('Error rate still elevated after rollback');
  }
  
  return comparison;
}
```

### Phase 9: Communication

#### Team Notification
```markdown
## 🚨 ROLLBACK INITIATED

**Time**: [Timestamp]
**Severity**: CRITICAL
**Component**: Production API
**Reason**: 500 errors spike to 80%

### Actions Taken
- ✅ Rolled back to v2.3.1
- ✅ Database migrations reversed
- ✅ Cache cleared
- ✅ CDN purged

### Current Status
- API: Recovering (30% errors → 2%)
- Database: Stable
- Response Time: Normalizing

### Next Steps
- Monitor for 30 minutes
- Root cause analysis
- Prepare hotfix

**On-call**: @alice
**Escalation**: @teamlead
```

#### Status Page Update
```javascript
// Update public status page
await statusPage.createIncident({
  name: 'Service Degradation',
  status: 'identified',
  impact: 'major',
  body: 'We are experiencing issues and have initiated a rollback.'
});

// Update after rollback
await statusPage.updateIncident(incidentId, {
  status: 'monitoring',
  body: 'Rollback complete. System recovering.'
});
```

### Phase 10: Incident Report

```markdown
# Incident Report #2024-001

## Summary
- **Date**: 2024-01-15
- **Duration**: 14:30 - 15:15 (45 minutes)
- **Impact**: 30% of users experienced errors
- **Root Cause**: Memory leak in v2.4.0

## Timeline
- 14:30 - Error rate spike detected
- 14:32 - On-call engineer paged
- 14:35 - Decision to rollback
- 14:37 - Rollback initiated
- 14:45 - Service recovering
- 15:00 - Metrics normalized
- 15:15 - Incident resolved

## Root Cause
Memory leak in payment processing module introduced in v2.4.0.
Garbage collection couldn't keep up with object creation rate.

## Resolution
1. Rolled back to v2.3.1
2. Cleared all caches
3. Restarted affected services
4. Monitored recovery

## Lessons Learned
1. Need better memory profiling in staging
2. Canary deployment would have caught this
3. Alert thresholds were too high

## Action Items
- [ ] Add memory leak detection to CI/CD
- [ ] Implement canary deployments
- [ ] Lower alert thresholds
- [ ] Add automatic rollback triggers

## Metrics
- **MTTR**: 45 minutes
- **Users Affected**: ~3,000
- **Error Rate Peak**: 80%
- **Revenue Impact**: ~$5,000
```

## Rollback Strategies

### Immediate Rollback
```bash
#!/bin/bash
# emergency-rollback.sh

echo "🚨 EMERGENCY ROLLBACK INITIATED"

# Stop bad deployment
kubectl scale deployment/myapp --replicas=0

# Rollback
kubectl rollout undo deployment/myapp

# Scale back up
kubectl scale deployment/myapp --replicas=3

# Clear caches
redis-cli FLUSHALL

# Notify team
curl -X POST $SLACK_WEBHOOK -d '{"text":"Emergency rollback completed"}'

echo "✅ Rollback complete"
```

### Gradual Rollback
```javascript
// Percentage-based rollback
async function gradualRollback() {
  const steps = [90, 70, 50, 25, 0];  // Traffic percentages
  
  for (const percentage of steps) {
    await updateTrafficSplit({
      new: percentage,
      old: 100 - percentage
    });
    
    await sleep(60000);  // Wait 1 minute
    
    const health = await checkHealth();
    if (health.ok) {
      console.log(`System stable at ${percentage}% new version`);
      break;
    }
  }
}
```

## Configuration

### .claude/rollback-config.json
```json
{
  "triggers": {
    "autoRollback": {
      "errorRate": 0.1,
      "responseTime": 2000,
      "availability": 0.95
    }
  },
  "strategies": {
    "default": "immediate",
    "canary": "gradual"
  },
  "notifications": {
    "slack": "#incidents",
    "pagerduty": true,
    "email": ["oncall@company.com"]
  },
  "recovery": {
    "healthCheckInterval": 30,
    "stabilizationPeriod": 300
  }
}
```

## Best Practices

1. **Speed Over Perfection**
   - Roll back first, investigate later
   - Use automatic triggers
   - Have rollback scripts ready

2. **Clear Communication**
   - Notify immediately
   - Update status page
   - Document everything

3. **Learn and Improve**
   - Conduct post-mortems
   - Update runbooks
   - Improve monitoring

## Notes
- Supports multiple platforms
- Automatic health verification
- Database migration reversal
- Comprehensive incident reporting
- Never delays critical rollbacks