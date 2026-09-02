# Smart Deployment Manager

Environment-aware deployment orchestrator with support for multiple strategies, automatic rollback, and health monitoring.

## Purpose
- Deploy to dev/staging/production environments
- Support blue-green and canary deployments
- Automatic rollback on failure
- Health checks and smoke tests
- Container and serverless deployment

## Workflow

### Step 1: Environment Selection
1. **STOP** → "Select deployment target:"
   ```
   1. Development - Local/dev environment
   2. Staging - Pre-production testing
   3. Production - Live environment
   4. Custom - Specify environment
   
   Choose environment (1-4):
   ```

2. **Deployment Strategy**
   - STOP → "Select deployment strategy:"
   ```
   1. Rolling update - Gradual replacement
   2. Blue-green - Instant switchover
   3. Canary - Percentage-based rollout
   4. Recreate - Stop old, start new
   5. Feature flag - Toggle-based
   
   Choose strategy (1-5):
   ```

3. **Deployment Options**
   - STOP → "Run pre-deployment tests? (y/n):"
   - STOP → "Enable automatic rollback? (y/n):"
   - STOP → "Send deployment notifications? (y/n):"

### Step 2: Pre-Deployment Checks
1. **Verify Build**
   ```bash
   # Check if build exists
   if [ ! -f "dist/index.js" ] && [ ! -d "build" ]; then
     echo "No build found. Running build..."
     npm run build || make build || cargo build --release
   fi
   ```

2. **Run Tests**
   ```bash
   # Critical tests only
   npm run test:smoke || pytest tests/smoke || go test ./tests/smoke
   ```

3. **Check Dependencies**
   ```bash
   # Verify all dependencies are installed
   npm ci --production || pip install -r requirements.txt --no-dev
   ```

4. **Security Scan**
   ```bash
   # Quick security check
   npm audit --production || safety check
   ```

### Step 3: Container Deployment
1. **Build Docker Image**
   ```bash
   # Build with version tag
   VERSION=$(git describe --tags --always)
   docker build -t myapp:$VERSION .
   docker tag myapp:$VERSION myapp:latest
   ```

2. **Push to Registry**
   ```bash
   # Push to registry (ECR, DockerHub, GCR)
   docker push myapp:$VERSION
   docker push myapp:latest
   ```

3. **Deploy to Kubernetes**
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: myapp
   spec:
     replicas: 3
     strategy:
       type: RollingUpdate
       rollingUpdate:
         maxSurge: 1
         maxUnavailable: 0
     template:
       spec:
         containers:
         - name: myapp
           image: myapp:VERSION
           livenessProbe:
             httpGet:
               path: /health
               port: 8080
           readinessProbe:
             httpGet:
               path: /ready
               port: 8080
   ```

4. **Apply Deployment**
   ```bash
   kubectl apply -f deployment.yaml
   kubectl rollout status deployment/myapp
   ```

### Step 4: Serverless Deployment
1. **AWS Lambda**
   ```bash
   # Package function
   zip -r function.zip . -x "*.git*"
   
   # Deploy
   aws lambda update-function-code \
     --function-name myapp \
     --zip-file fileb://function.zip
   
   # Update alias
   aws lambda update-alias \
     --function-name myapp \
     --name production \
     --function-version $LATEST
   ```

2. **Vercel/Netlify**
   ```bash
   # Vercel
   vercel --prod
   
   # Netlify
   netlify deploy --prod
   ```

3. **Cloud Functions**
   ```bash
   # Google Cloud
   gcloud functions deploy myapp \
     --runtime nodejs18 \
     --trigger-http \
     --allow-unauthenticated
   
   # Azure
   func azure functionapp publish myapp
   ```

### Step 5: Blue-Green Deployment
1. **Setup Blue Environment**
   ```bash
   # Deploy to blue environment
   kubectl apply -f blue-deployment.yaml
   kubectl wait --for=condition=available deployment/myapp-blue
   ```

2. **Run Smoke Tests**
   ```bash
   # Test blue environment
   BLUE_URL="http://blue.myapp.com"
   curl -f $BLUE_URL/health || exit 1
   npm run test:e2e -- --url=$BLUE_URL
   ```

3. **Switch Traffic**
   ```yaml
   # Update service to point to blue
   apiVersion: v1
   kind: Service
   metadata:
     name: myapp
   spec:
     selector:
       app: myapp
       version: blue
   ```

4. **Verify and Cleanup**
   ```bash
   # Monitor metrics
   kubectl top pods -l app=myapp,version=blue
   
   # Remove green after success
   kubectl delete deployment myapp-green
   ```

### Step 6: Canary Deployment
1. **Deploy Canary Version**
   ```bash
   # Deploy with 10% traffic
   kubectl apply -f canary-deployment.yaml
   kubectl scale deployment/myapp-canary --replicas=1
   kubectl scale deployment/myapp-stable --replicas=9
   ```

2. **Monitor Metrics**
   ```javascript
   // Check error rates
   const canaryErrors = await getMetrics('canary', 'errors');
   const stableErrors = await getMetrics('stable', 'errors');
   
   if (canaryErrors > stableErrors * 1.5) {
     console.log('Canary failing, rolling back');
     rollback();
   }
   ```

3. **Progressive Rollout**
   ```bash
   # Increase canary traffic
   for percent in 10 25 50 75 100; do
     updateTrafficSplit(canary: $percent, stable: $((100-$percent)))
     sleep 300  # Wait 5 minutes
     checkHealth() || rollback
   done
   ```

### Step 7: Health Checks
1. **Liveness Check**
   ```bash
   # Basic health endpoint
   curl -f http://app.com/health || exit 1
   ```

2. **Readiness Check**
   ```bash
   # Check if app is ready for traffic
   curl -f http://app.com/ready || exit 1
   ```

3. **Smoke Tests**
   ```javascript
   // Critical path testing
   const tests = [
     () => checkHomepage(),
     () => checkLogin(),
     () => checkAPI(),
     () => checkDatabase()
   ];
   
   for (const test of tests) {
     await test();
   }
   ```

4. **Performance Check**
   ```bash
   # Response time check
   response_time=$(curl -w "%{time_total}" -o /dev/null -s http://app.com)
   if (( $(echo "$response_time > 2" | bc -l) )); then
     echo "Performance degraded"
     rollback
   fi
   ```

### Step 8: Rollback Procedures
1. **Automatic Rollback Triggers**
   ```yaml
   rollback_conditions:
     - health_check_failures: 3
     - error_rate: > 5%
     - response_time: > 2s
     - memory_usage: > 90%
     - crash_loop: true
   ```

2. **Rollback Execution**
   ```bash
   # Kubernetes rollback
   kubectl rollout undo deployment/myapp
   
   # Docker rollback
   docker service update --image myapp:previous myapp
   
   # Lambda rollback
   aws lambda update-alias \
     --function-name myapp \
     --function-version $PREVIOUS_VERSION
   ```

3. **Database Rollback**
   ```bash
   # Rollback migrations
   npm run migrate:down || python manage.py migrate previous_migration
   ```

### Step 9: Post-Deployment
1. **Monitoring Setup**
   ```javascript
   // Set up alerts
   createAlert({
     metric: 'error_rate',
     threshold: 1,
     duration: '5m',
     action: 'notify'
   });
   ```

2. **Performance Baseline**
   ```bash
   # Capture metrics
   kubectl top pods > metrics-baseline.txt
   curl -X POST monitoring.api/baseline \
     -d "{\"deployment\": \"$VERSION\", \"metrics\": $(cat metrics-baseline.txt)}"
   ```

3. **Notification**
   ```markdown
   ## Deployment Successful
   
   **Environment**: Production
   **Version**: v2.3.1
   **Strategy**: Blue-Green
   **Duration**: 4m 32s
   
   ### Health Status
   - API: ✅ Healthy
   - Database: ✅ Connected
   - Cache: ✅ Available
   
   ### Performance
   - Response Time: 145ms (↓ 12%)
   - Error Rate: 0.01% (→ 0%)
   - Throughput: 1,200 req/s (↑ 8%)
   
   ### Next Steps
   - Monitor for 30 minutes
   - Check user feedback
   - Review error logs
   ```

### Step 10: Deployment Report
```markdown
# Deployment Report

## Summary
- **Application**: MyApp
- **Version**: 2.3.1
- **Environment**: Production
- **Status**: SUCCESS
- **Duration**: 4m 32s

## Deployment Steps
| Step | Status | Duration |
|------|--------|----------|
| Pre-deployment tests | ✅ | 45s |
| Build Docker image | ✅ | 1m 20s |
| Push to registry | ✅ | 30s |
| Deploy to K8s | ✅ | 1m 15s |
| Health checks | ✅ | 42s |
| Traffic switch | ✅ | 10s |

## Validation Results
- Unit Tests: 156/156 passed
- Integration Tests: 42/42 passed
- Smoke Tests: 8/8 passed
- Security Scan: No issues

## Resource Usage
- CPU: 2.4 cores (60% of limit)
- Memory: 512MB (40% of limit)
- Pods: 3 running

## Rollback Plan
If issues occur:
1. Run: kubectl rollout undo deployment/myapp
2. Verify: kubectl rollout status deployment/myapp
3. Check: curl http://app.com/health
```

## Deployment Strategies

### Rolling Update
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 25%
    maxUnavailable: 25%
```

### Blue-Green
```yaml
# Two identical environments
# Instant traffic switch
# Zero downtime
# Easy rollback
```

### Canary
```yaml
# Gradual traffic shift
# Risk mitigation
# A/B testing capable
# Metric-based promotion
```

## Platform Support

### Container Platforms
- Kubernetes
- Docker Swarm
- Amazon ECS
- Google GKE
- Azure AKS

### Serverless Platforms
- AWS Lambda
- Google Cloud Functions
- Azure Functions
- Vercel
- Netlify

### Traditional Servers
- SSH deployment
- FTP upload
- rsync
- Git hooks

## Configuration

### .claude/deploy-config.json
```json
{
  "environments": {
    "development": {
      "url": "https://dev.myapp.com",
      "strategy": "recreate",
      "tests": "smoke"
    },
    "staging": {
      "url": "https://staging.myapp.com",
      "strategy": "rolling",
      "tests": "full"
    },
    "production": {
      "url": "https://myapp.com",
      "strategy": "blue-green",
      "tests": "smoke",
      "approvals": ["lead", "qa"]
    }
  },
  "rollback": {
    "automatic": true,
    "conditions": {
      "errorRate": 0.05,
      "responseTime": 2000
    }
  },
  "notifications": {
    "slack": "#deployments",
    "email": ["team@company.com"]
  }
}
```

## Best Practices

1. **Pre-Deployment**
   - Always test in staging
   - Backup databases
   - Check dependencies
   - Review changes

2. **During Deployment**
   - Monitor actively
   - Keep rollback ready
   - Communicate status
   - Document issues

3. **Post-Deployment**
   - Verify functionality
   - Monitor metrics
   - Gather feedback
   - Update documentation

## Notes
- Supports multiple cloud providers
- Integrates with CI/CD pipelines
- Automatic rollback on failure
- Never deploys without tests
- Maintains deployment history