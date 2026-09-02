# Performance Analysis

Comprehensive performance profiler that identifies bottlenecks, analyzes database queries, detects memory leaks, and suggests optimizations.

## Purpose
- Profile code for performance bottlenecks
- Compare performance against baseline
- Suggest optimizations
- Analyze database queries
- Detect memory leaks

## Workflow

### Step 1: Performance Target
1. **STOP** → "Select performance analysis type:"
   ```
   1. Application profiling - Overall performance
   2. Database analysis - Query optimization
   3. Memory profiling - Leak detection
   4. API performance - Endpoint analysis
   5. Frontend performance - Browser metrics
   6. Load testing - Stress test
   
   Choose type (1-6):
   ```

2. **Analysis Options**
   - STOP → "Compare with baseline? (y/n):"
   - STOP → "Generate flame graphs? (y/n):"
   - STOP → "Include memory snapshots? (y/n):"
   - STOP → "Run under load? (y/n):"

### Step 2: Performance Profiling

#### Application Profiling
```bash
# Node.js CPU profiling
node --cpu-prof app.js
node --cpu-prof-dir=profiles app.js

# Memory profiling
node --heap-prof app.js
node --trace-gc app.js

# V8 profiling
node --prof app.js
node --prof-process isolate-*.log > processed.txt
```

#### Python Profiling
```python
import cProfile
import pstats

# Profile code
profiler = cProfile.Profile()
profiler.enable()
# Code to profile
profiler.disable()

# Generate report
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

#### Go Profiling
```go
import _ "net/http/pprof"

// CPU profiling
go tool pprof http://localhost:6060/debug/pprof/profile

// Memory profiling
go tool pprof http://localhost:6060/debug/pprof/heap

// Goroutine profiling
go tool pprof http://localhost:6060/debug/pprof/goroutine
```

### Step 3: Database Performance

#### Query Analysis
```sql
-- PostgreSQL
EXPLAIN ANALYZE
SELECT * FROM users u
JOIN posts p ON u.id = p.user_id
WHERE u.created_at > '2024-01-01';

-- MySQL
EXPLAIN FORMAT=JSON
SELECT * FROM users WHERE email LIKE '%@example.com';

-- MongoDB
db.users.explain("executionStats").find({ age: { $gt: 25 } });
```

#### Slow Query Detection
```javascript
// Log slow queries
const startTime = Date.now();
const result = await db.query(sql);
const duration = Date.now() - startTime;

if (duration > 1000) {
  console.warn(`Slow query (${duration}ms):`, sql);
}
```

#### Index Analysis
```sql
-- Missing indexes
SELECT 
  schemaname,
  tablename,
  attname,
  n_distinct,
  correlation
FROM pg_stats
WHERE schemaname = 'public'
  AND n_distinct > 100
  AND correlation < 0.1;

-- Unused indexes
SELECT
  indexname,
  tablename,
  idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

### Step 4: Memory Analysis

#### Memory Leak Detection
```javascript
// Node.js heap snapshot
const v8 = require('v8');
const fs = require('fs');

// Take snapshot
const heapSnapshot = v8.writeHeapSnapshot();
fs.writeFileSync('heap.heapsnapshot', heapSnapshot);

// Monitor memory usage
setInterval(() => {
  const usage = process.memoryUsage();
  console.log({
    rss: `${Math.round(usage.rss / 1024 / 1024)}MB`,
    heap: `${Math.round(usage.heapUsed / 1024 / 1024)}MB`,
    external: `${Math.round(usage.external / 1024 / 1024)}MB`
  });
}, 5000);
```

#### Common Memory Issues
```javascript
// ❌ Memory leak - Event listeners
class Component {
  constructor() {
    document.addEventListener('click', this.handleClick);
    // Never removed!
  }
}

// ✅ Proper cleanup
class Component {
  constructor() {
    this.handleClick = this.handleClick.bind(this);
    document.addEventListener('click', this.handleClick);
  }
  
  destroy() {
    document.removeEventListener('click', this.handleClick);
  }
}

// ❌ Retaining large objects
const cache = {};
function processData(id, data) {
  cache[id] = data;  // Never cleared
}

// ✅ Bounded cache
const cache = new Map();
const MAX_CACHE_SIZE = 100;

function processData(id, data) {
  if (cache.size >= MAX_CACHE_SIZE) {
    const firstKey = cache.keys().next().value;
    cache.delete(firstKey);
  }
  cache.set(id, data);
}
```

### Step 5: API Performance

#### Endpoint Analysis
```javascript
// Middleware for timing
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log({
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: `${duration}ms`
    });
  });
  
  next();
});
```

#### Response Time Optimization
```javascript
// ❌ Slow: Sequential operations
async function getData() {
  const user = await fetchUser();
  const posts = await fetchPosts();
  const comments = await fetchComments();
  return { user, posts, comments };
}

// ✅ Fast: Parallel operations
async function getData() {
  const [user, posts, comments] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchComments()
  ]);
  return { user, posts, comments };
}
```

### Step 6: Frontend Performance

#### Browser Metrics
```javascript
// Core Web Vitals
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    console.log({
      name: entry.name,
      value: entry.value,
      rating: entry.rating
    });
  }
});

observer.observe({ entryTypes: ['largest-contentful-paint'] });
observer.observe({ entryTypes: ['first-input'] });
observer.observe({ entryTypes: ['layout-shift'] });
```

#### Bundle Analysis
```bash
# Webpack bundle analyzer
webpack --profile --json > stats.json
webpack-bundle-analyzer stats.json

# Rollup visualizer
rollup -c --plugin visualizer
```

#### Rendering Performance
```javascript
// ❌ Forced reflow
for (let i = 0; i < elements.length; i++) {
  elements[i].style.left = elements[i].offsetLeft + 10 + 'px';
}

// ✅ Batch DOM reads/writes
const positions = elements.map(el => el.offsetLeft);
elements.forEach((el, i) => {
  el.style.left = positions[i] + 10 + 'px';
});
```

### Step 7: Load Testing

#### Stress Testing
```bash
# Apache Bench
ab -n 1000 -c 100 http://localhost:3000/api/users

# wrk
wrk -t12 -c400 -d30s --latency http://localhost:3000/

# k6
k6 run --vus 100 --duration 30s load-test.js
```

#### Load Test Script
```javascript
// k6 load test
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Stay at 100
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.1'],     // Error rate under 10%
  },
};

export default function() {
  const res = http.get('http://localhost:3000/api/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

### Step 8: Optimization Suggestions

#### Code Optimizations
```javascript
// ❌ Inefficient array search
const user = users.find(u => u.id === userId);

// ✅ Use Map for O(1) lookup
const userMap = new Map(users.map(u => [u.id, u]));
const user = userMap.get(userId);

// ❌ Repeated calculations
function calculate(items) {
  return items.map(item => {
    const tax = item.price * 0.1;
    const discount = item.price * 0.2;
    return item.price + tax - discount;
  });
}

// ✅ Memoization
const memoize = (fn) => {
  const cache = new Map();
  return (...args) => {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
};
```

#### Caching Strategies
```javascript
// Memory cache
const cache = new NodeCache({ stdTTL: 600 });

// Redis cache
const redis = require('redis').createClient();

async function getCachedData(key, fetchFn) {
  // Check cache
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);
  
  // Fetch and cache
  const data = await fetchFn();
  await redis.setex(key, 600, JSON.stringify(data));
  return data;
}
```

### Step 9: Performance Report

```markdown
# Performance Analysis Report

## Executive Summary
- **Overall Performance**: ⚠️ Needs Improvement
- **Response Time (P95)**: 1,234ms (Target: <500ms)
- **Memory Usage**: 412MB (Stable)
- **Database Queries**: 23 slow queries detected

## Performance Metrics

### Application Performance
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Startup Time | 3.2s | <2s | ❌ |
| API Response (P50) | 234ms | <200ms | ⚠️ |
| API Response (P95) | 1,234ms | <500ms | ❌ |
| API Response (P99) | 2,456ms | <1000ms | ❌ |

### Database Performance
| Query | Time | Calls/min | Impact |
|-------|------|-----------|--------|
| getUserPosts | 845ms | 120 | HIGH |
| searchProducts | 623ms | 80 | HIGH |
| updateInventory | 234ms | 200 | MEDIUM |

### Memory Analysis
- **Heap Used**: 312MB (75% of limit)
- **Heap Growth**: +2MB/hour (acceptable)
- **GC Frequency**: Every 12s
- **Memory Leaks**: None detected

## Critical Issues

### 1. N+1 Query in User Posts
**Impact**: 80% of API response time
**Solution**: 
```sql
-- Current: 1 + N queries
SELECT * FROM users WHERE id = ?;
SELECT * FROM posts WHERE user_id = ?;  -- Called N times

-- Optimized: 1 query
SELECT u.*, p.*
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.id = ?;
```

### 2. Missing Database Index
**Table**: products
**Column**: category_id, status
**Impact**: 623ms full table scan
**Solution**:
```sql
CREATE INDEX idx_products_category_status 
ON products(category_id, status);
```

### 3. Unoptimized Bundle Size
**Current**: 2.3MB
**Target**: <500KB
**Issues**:
- Lodash fully imported (328KB)
- Moment.js included (232KB)
- Source maps in production (1.2MB)

## Optimization Recommendations

### Immediate Actions
1. Add database indexes (Est. 70% improvement)
2. Implement query batching (Est. 50% improvement)
3. Enable gzip compression (Est. 60% size reduction)
4. Remove unused dependencies (Est. 300KB reduction)

### Short-term Improvements
1. Implement Redis caching
2. Optimize images with CDN
3. Enable HTTP/2
4. Implement connection pooling

### Long-term Strategy
1. Migrate to microservices
2. Implement GraphQL for efficient data fetching
3. Consider database sharding
4. Implement edge caching

## Baseline Comparison
| Metric | Previous | Current | Change |
|--------|----------|---------|--------|
| Response Time | 892ms | 1,234ms | +38% ❌ |
| Memory Usage | 380MB | 412MB | +8% ⚠️ |
| Error Rate | 0.8% | 0.3% | -62% ✅ |
| Throughput | 450 req/s | 520 req/s | +15% ✅ |

## Action Items
- [ ] Apply database indexes
- [ ] Fix N+1 queries
- [ ] Optimize bundle size
- [ ] Implement caching layer
- [ ] Add performance monitoring
```

## Performance Monitoring

### Real-time Monitoring
```javascript
// Custom performance monitoring
class PerformanceMonitor {
  constructor() {
    this.metrics = {
      requests: new Map(),
      queries: new Map(),
      memory: []
    };
  }
  
  trackRequest(url, duration) {
    if (!this.metrics.requests.has(url)) {
      this.metrics.requests.set(url, []);
    }
    this.metrics.requests.get(url).push(duration);
  }
  
  getP95(url) {
    const times = this.metrics.requests.get(url) || [];
    times.sort((a, b) => a - b);
    return times[Math.floor(times.length * 0.95)];
  }
}
```

## Configuration

### .claude/perf-config.json
```json
{
  "thresholds": {
    "responseTime": {
      "p50": 200,
      "p95": 500,
      "p99": 1000
    },
    "memory": {
      "heapUsed": 512,
      "rss": 1024
    },
    "database": {
      "queryTime": 100,
      "connectionPool": 20
    }
  },
  "profiling": {
    "cpu": true,
    "memory": true,
    "network": true
  },
  "reporting": {
    "format": "html",
    "output": "performance-report.html"
  }
}
```

## Best Practices

1. **Measure First**
   - Profile before optimizing
   - Focus on bottlenecks
   - Set performance budgets

2. **Optimize Wisely**
   - Fix biggest issues first
   - Avoid premature optimization
   - Test optimizations

3. **Monitor Continuously**
   - Track performance over time
   - Alert on degradation
   - Regular performance reviews

## Notes
- Profiles all major languages
- Generates flame graphs
- Compares with baselines
- Suggests specific optimizations
- Never ignores performance regression