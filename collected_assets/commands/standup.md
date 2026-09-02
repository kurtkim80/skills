# Daily Status Generator

Automatically generates standup notes from yesterday's commits, today's planned tasks, and identifies blockers.

## Purpose
- Generate standup notes from git history
- List today's planned tasks from todos
- Identify blockers from error logs
- Create team activity dashboard
- Prepare daily status updates

## Workflow

### Phase 1: Standup Format
1. **STOP** → "Select standup format:"
   ```
   1. Standard - Yesterday/Today/Blockers
   2. Detailed - Include metrics and code
   3. Brief - One-line summaries
   4. Custom - Specify format
   
   Choose format (1-4):
   ```

2. **Report Options**
   - STOP → "Include code metrics? (y/n):"
   - STOP → "Add PR/MR links? (y/n):"
   - STOP → "Include time tracking? (y/n):"
   - STOP → "Generate for team? (y/n):"

### Phase 2: Yesterday's Activity

#### Git History Analysis
```bash
# Get yesterday's commits
yesterday=$(date -d "yesterday" +%Y-%m-%d)
today=$(date +%Y-%m-%d)

git log --since="$yesterday 00:00" --until="$yesterday 23:59" \
  --pretty=format:"- %s" --author="$(git config user.name)"

# Get merged PRs
gh pr list --state merged --search "merged:$yesterday"

# Get code changes
git log --since="$yesterday" --until="$today" \
  --pretty=tformat: --numstat | \
  awk '{ add += $1; del += $2 } END { print "+"add" -"del }'
```

#### Task Completion
```javascript
// Check completed todos
const completedYesterday = todos.filter(todo => {
  const completedDate = new Date(todo.completedAt);
  return isYesterday(completedDate);
});
```

### Phase 3: Today's Plan

#### Planned Tasks
```javascript
// Read from todos
const todayTasks = todos.filter(todo => 
  todo.status === 'pending' || 
  todo.status === 'in-progress'
).slice(0, 5);  // Top 5 priority items

// Check calendar/sprint tasks
const sprintTasks = getSprintTasks(currentSprint);
```

#### Meetings & Reviews
```javascript
// Parse calendar (if integrated)
const meetings = [
  "10:00 - Team standup",
  "14:00 - Code review session",
  "16:00 - 1:1 with manager"
];
```

### Phase 4: Blocker Detection

#### Error Log Analysis
```bash
# Check for recent errors
tail -n 1000 error.log | grep -E "ERROR|FATAL|CRITICAL" | tail -5

# Check CI/CD failures
gh run list --workflow=ci.yml --status=failure --limit=5

# Check failing tests
npm test 2>&1 | grep -E "FAIL|Error" || echo "All tests passing"
```

#### System Issues
```javascript
// Check service health
const healthChecks = {
  database: checkDatabaseConnection(),
  redis: checkRedisConnection(),
  api: checkAPIHealth(),
  dependencies: checkDependencyStatus()
};

const blockers = Object.entries(healthChecks)
  .filter(([_, status]) => !status)
  .map(([service]) => `${service} is down`);
```

### Phase 5: Standup Generation

#### Standard Format
```markdown
# Daily Standup - [Date]

## 👤 [Your Name]

### ✅ Yesterday
- Completed user authentication feature (#PR-123)
- Fixed critical bug in payment processing
- Reviewed 3 pull requests
- Updated API documentation
- **Commits**: 8 | **Lines**: +245 -123

### 📅 Today
- [ ] Complete integration tests for auth module
- [ ] Start working on user profile feature
- [ ] Code review for team members
- [ ] Deploy hotfix to production
- [ ] Team meeting at 2 PM

### 🚧 Blockers
- Waiting for API credentials from DevOps
- Database migration script failing in staging
- Need clarification on business requirements

### 💭 Notes
- Discovered performance issue in search endpoint
- Suggested new approach for caching strategy
```

#### Detailed Format
```markdown
# Detailed Standup Report - [Date]

## Work Completed

### Feature Development
**Authentication Module** ✅
- Implemented JWT-based authentication
- Added refresh token mechanism
- Created middleware for route protection
- Files: `auth.service.ts`, `auth.controller.ts`
- PR: #123 (Merged)
- Coverage: 92%

### Bug Fixes
**Payment Processing Error** 🐛
- Issue: Decimal precision in currency calculation
- Root cause: Float arithmetic errors
- Solution: Used decimal.js library
- Impact: Fixed for 100% of transactions
- Commit: abc123f

### Code Reviews
1. **PR #456** - Database optimization
   - Suggested index improvements
   - Approved with comments
2. **PR #789** - New feature flag system
   - Requested changes for error handling

## Today's Objectives

### High Priority
1. **Integration Tests** (2-3 hours)
   - Write tests for auth endpoints
   - Mock external services
   - Target: 90% coverage

2. **User Profile Feature** (4-5 hours)
   - Design database schema
   - Implement CRUD operations
   - Create API endpoints

### Medium Priority
- Review team PRs
- Update documentation
- Refactor user service

## Metrics & Performance

### Code Metrics
- **Commits**: 8
- **Lines Added**: 524
- **Lines Removed**: 232
- **Files Changed**: 15
- **Test Coverage**: ↑ 2.3% (now 87%)

### Performance Improvements
- API response time: ↓ 23% (450ms → 347ms)
- Database queries: ↓ 5 queries per request
- Bundle size: ↓ 12KB after tree-shaking

## Blockers & Dependencies

### Critical Blockers
1. **AWS Credentials Missing**
   - Impact: Cannot deploy to staging
   - Needed from: DevOps team
   - ETA: Today afternoon

### Waiting On
- Product decision on email templates
- QA sign-off for release
- Security audit results

## Risk & Mitigation
- **Risk**: Deployment window closing
- **Mitigation**: Prepared rollback plan
- **Contingency**: Can deploy tomorrow morning
```

#### Team Dashboard Format
```markdown
# Team Standup Dashboard - [Date]

## 📊 Team Overview
**Sprint**: 23 | **Day**: 5/10 | **Velocity**: 34/50 points

## 👥 Team Status

### Alice (Frontend)
✅ **Yesterday**: Completed dashboard UI
📅 **Today**: Working on responsive design
🚧 **Blockers**: Waiting for API endpoints

### Bob (Backend)
✅ **Yesterday**: Implemented auth system
📅 **Today**: Database optimization
🚧 **Blockers**: None

### Charlie (DevOps)
✅ **Yesterday**: Set up CI/CD pipeline
📅 **Today**: Configure monitoring
🚧 **Blockers**: AWS quota limit

## 📈 Sprint Progress

### Completed (12 items)
- ✅ User authentication
- ✅ Database setup
- ✅ CI/CD pipeline

### In Progress (5 items)
- 🔄 User profiles (60%)
- 🔄 Payment integration (30%)
- 🔄 Email service (80%)

### Blocked (2 items)
- ❌ Third-party API integration
- ❌ Production deployment

## 🎯 Sprint Goals
| Goal | Status | Progress |
|------|--------|----------|
| Launch MVP | On Track | 70% |
| 90% test coverage | At Risk | 84% |
| Zero critical bugs | Achieved | ✅ |

## 📅 Today's Schedule
- 10:00 - Daily standup
- 11:00 - Architecture review
- 14:00 - Sprint planning
- 16:00 - Demo preparation

## ⚠️ Risks & Issues
1. **Deployment deadline tight**
   - Mitigation: Parallel testing
2. **API rate limits discovered**
   - Solution: Implement caching

## 🔗 Quick Links
- [Sprint Board](link)
- [Burndown Chart](link)
- [Team Calendar](link)
- [Documentation](link)
```

### Phase 6: Time Tracking

```markdown
## ⏱️ Time Breakdown

### Yesterday (8 hours)
- Feature development: 4h 30m
- Bug fixes: 1h 15m
- Code reviews: 1h
- Meetings: 45m
- Documentation: 30m

### This Week (32 hours)
- Development: 22h (69%)
- Meetings: 5h (16%)
- Reviews: 3h (9%)
- Planning: 2h (6%)
```

### Phase 7: Automated Insights

#### Productivity Analysis
```javascript
function generateInsights(commits, tasks) {
  const insights = [];
  
  // Commit patterns
  const commitHours = commits.map(c => new Date(c.date).getHours());
  const peakHour = mode(commitHours);
  insights.push(`Most productive hour: ${peakHour}:00`);
  
  // Task completion rate
  const completionRate = (tasks.completed / tasks.total) * 100;
  insights.push(`Task completion rate: ${completionRate}%`);
  
  // Velocity trend
  const velocity = calculateVelocity(tasks);
  if (velocity > lastWeekVelocity) {
    insights.push(`Velocity increased by ${velocity - lastWeekVelocity} points`);
  }
  
  return insights;
}
```

### Phase 8: Communication Integration

#### Slack Format
```
*Daily Standup - Jan 15*

*Yesterday:* ✅
• Completed auth feature
• Fixed payment bug
• 8 commits, +245 -123 lines

*Today:* 📋
• Integration tests
• User profile feature
• Deploy hotfix

*Blockers:* 🚧
• Need AWS credentials
• DB migration failing

*Meetings:* 📅
• 10 AM - Team standup
• 2 PM - Architecture review
```

#### Email Format
```html
<h2>Daily Status Update</h2>

<h3>Accomplishments</h3>
<ul>
  <li>✅ Authentication module complete</li>
  <li>✅ Critical bug resolved</li>
</ul>

<h3>Today's Focus</h3>
<ul>
  <li>Integration testing</li>
  <li>User profile development</li>
</ul>

<h3>Need Assistance With</h3>
<ul>
  <li>🚨 AWS credentials for deployment</li>
</ul>
```

## Standup Analytics

### Patterns Detection
```javascript
// Identify recurring blockers
const recurringBlockers = blockers.filter(blocker => {
  return previousStandups.some(standup => 
    standup.blockers.includes(blocker)
  );
});

// Track estimation accuracy
const estimationAccuracy = tasks.filter(task => {
  return task.actualTime <= task.estimatedTime * 1.2;
}).length / tasks.length;
```

### Team Metrics
```yaml
team_health:
  velocity: 85%
  blocker_resolution: 2.5 days avg
  pr_review_time: 4 hours avg
  test_coverage: 87%
  deployment_frequency: 3/week
```

## Configuration

### .claude/standup-config.json
```json
{
  "format": "standard",
  "includeMetrics": true,
  "timeTracking": false,
  "team": {
    "enabled": false,
    "members": ["alice", "bob", "charlie"]
  },
  "schedule": {
    "time": "09:30",
    "timezone": "America/New_York",
    "days": ["mon", "tue", "wed", "thu", "fri"]
  },
  "integrations": {
    "slack": {
      "enabled": true,
      "channel": "#standups"
    },
    "email": {
      "enabled": false,
      "recipients": ["team@company.com"]
    }
  }
}
```

## Best Practices

1. **Be Concise**
   - Focus on key items
   - Avoid technical jargon
   - Use bullet points

2. **Be Specific**
   - Include ticket numbers
   - Mention collaborators
   - Quantify when possible

3. **Be Honest**
   - Report real blockers
   - Share concerns early
   - Ask for help

## Notes
- Generates from git history
- Tracks task completion
- Identifies blockers automatically
- Creates team dashboards
- Never misses important updates