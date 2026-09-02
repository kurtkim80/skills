# Team Handoff Assistant

Facilitates smooth task transitions between team members by generating comprehensive handoff documentation and status summaries.

## Purpose
- Generate handoff documentation
- Create status summary from git history
- List open blockers and dependencies
- Generate onboarding guide for new developers
- Ensure seamless task transitions

## Workflow

### Phase 1: Handoff Type
1. **STOP** → "Select handoff type:"
   ```
   1. Task handoff - Transfer specific task
   2. Project handoff - Full project transfer
   3. Shift handoff - End of day/shift summary
   4. Vacation handoff - Extended absence prep
   5. Onboarding - New team member setup
   
   Choose type (1-5):
   ```

2. **Handoff Options**
   - STOP → "Include code walkthrough? (y/n):"
   - STOP → "Generate setup instructions? (y/n):"
   - STOP → "Include known issues? (y/n):"
   - STOP → "Create follow-up tasks? (y/n):"

### Phase 2: Context Gathering

#### Current Work Status
```bash
# Get current branch and status
git branch --show-current
git status --short

# Recent commits
git log --oneline -10

# Uncommitted changes
git diff --stat

# Active worktrees
git worktree list
```

#### Task Progress
```javascript
// Read task history
const taskFiles = fs.readdirSync('.claude/task-history')
  .sort((a, b) => b.localeCompare(a))
  .slice(0, 5);

// Parse todos
const todos = parseTodoFile('todos/todos.md');
const completed = todos.filter(t => t.status === 'completed');
const inProgress = todos.filter(t => t.status === 'in-progress');
const pending = todos.filter(t => t.status === 'pending');
```

### Phase 3: Documentation Generation

#### Task Handoff Document
```markdown
# Task Handoff: [Task Name]

## Handoff Summary
- **From**: [Your Name]
- **To**: [Recipient Name]
- **Date**: [Current Date]
- **Task**: [Task Description]
- **Priority**: High/Medium/Low
- **Deadline**: [If applicable]

## Current Status

### ✅ Completed
- Implemented user authentication
- Added database migrations
- Created API endpoints
- Written unit tests (80% coverage)

### 🔄 In Progress
- Integration testing (50% complete)
- Documentation updates
- Performance optimization

### 📋 Remaining Work
- [ ] Complete integration tests
- [ ] Add error handling for edge cases
- [ ] Deploy to staging environment
- [ ] Security review

## Technical Context

### Architecture Decisions
- Chose JWT for authentication (see: auth.service.ts)
- Using Redis for session storage
- Implemented repository pattern for data access

### Key Files Modified
```
src/
├── services/
│   ├── auth.service.ts (Main authentication logic)
│   └── user.service.ts (User management)
├── controllers/
│   └── auth.controller.ts (API endpoints)
└── tests/
    └── auth.test.ts (Test suite)
```

### Dependencies Added
- jsonwebtoken: ^9.0.0
- bcrypt: ^5.1.0
- redis: ^4.5.0

## Known Issues & Blockers

### 🚨 Critical
1. **Redis connection timeout in production**
   - Occurs under high load
   - Temporary fix: Increased timeout to 30s
   - Permanent solution: Need connection pooling

### ⚠️ Important
2. **Password reset flow incomplete**
   - Email service not configured
   - Template missing
   - Needs SMTP credentials

## Development Environment

### Setup Instructions
```bash
# Clone and install
git clone [repo]
cd [project]
npm install

# Environment variables needed
cp .env.example .env
# Edit .env with:
# - DATABASE_URL
# - REDIS_URL
# - JWT_SECRET

# Run migrations
npm run migrate

# Start development
npm run dev
```

### Required Tools
- Node.js 18+
- Redis 7.0+
- PostgreSQL 14+

### Access Needed
- GitHub repository access
- Database credentials
- Staging server SSH
- Monitoring dashboard

## Current Branch Structure
```
main
├── feature/authentication (current)
├── feature/user-management (merged)
└── fix/database-connection (merged)
```

## Testing Instructions

### Run Tests
```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# Specific test file
npm test auth.test.ts
```

### Manual Testing
1. Start server: `npm run dev`
2. Test login: POST /api/auth/login
   ```json
   {
     "email": "test@example.com",
     "password": "Test123!"
   }
   ```
3. Verify token in response
4. Test protected route with token

## Communication & Contacts

### Related Discussions
- Slack thread: #dev-authentication (Jan 15)
- Design doc: [link to doc]
- Meeting notes: [link to notes]

### Key Stakeholders
- Product Owner: [Name] - Requirements clarification
- DevOps: [Name] - Deployment assistance
- QA: [Name] - Testing coordination

## Recommended Next Steps

### Immediate (Today)
1. Review this handoff document
2. Pull latest changes from feature branch
3. Run tests to verify environment
4. Continue with integration tests

### Short-term (This Week)
1. Complete remaining test cases
2. Fix Redis timeout issue
3. Deploy to staging
4. Schedule security review

### Questions to Clarify
- Preferred error message format?
- Should we log failed login attempts?
- Rate limiting requirements?

## Additional Resources
- [API Documentation](docs/api.md)
- [Database Schema](docs/database.md)
- [Architecture Diagram](docs/architecture.png)
- [Original Specification](specs/auth-spec.md)

## Handoff Checklist
- [x] Code committed and pushed
- [x] Tests passing locally
- [x] Documentation updated
- [x] Known issues documented
- [ ] Recipient confirmed understanding
- [ ] Access verified
- [ ] Questions answered
```

### Phase 4: Project Handoff

```markdown
# Project Handoff: [Project Name]

## Project Overview
**Purpose**: [Brief description]
**Stage**: Development/Testing/Production
**Timeline**: Started [date], Due [date]
**Tech Stack**: [List technologies]

## Team & Responsibilities
| Team Member | Role | Responsibilities |
|-------------|------|------------------|
| [Name] | Backend | API, Database |
| [Name] | Frontend | UI, UX |
| [Name] | DevOps | Infrastructure |

## Current Sprint
**Sprint**: [Number]
**Duration**: [Start] - [End]
**Goals**:
- Complete user authentication
- Implement payment processing
- Deploy to staging

## Codebase Structure
```
project/
├── backend/        # Node.js API
├── frontend/       # React application
├── database/       # Migrations and seeds
├── scripts/        # Utility scripts
├── docs/          # Documentation
└── tests/         # Test suites
```

## Environment Status
| Environment | URL | Status | Last Deploy |
|-------------|-----|--------|-------------|
| Development | dev.app.com | ✅ Running | Today |
| Staging | staging.app.com | ✅ Running | Yesterday |
| Production | app.com | ✅ Running | Last week |

## Key Features Status
| Feature | Status | Owner | Notes |
|---------|--------|-------|-------|
| Authentication | ✅ Complete | [Name] | Using JWT |
| User Management | 🔄 In Progress | [Name] | 70% done |
| Payment | 📋 Planned | TBD | Stripe integration |
| Notifications | 📋 Planned | TBD | Email + Push |

## Recent Activity
### Last Week
- Completed authentication module
- Fixed critical security bug
- Added integration tests
- Updated documentation

### This Week's Plan
- Complete user management
- Start payment integration
- Deploy to staging
- Security audit

## Critical Information

### Passwords & Secrets
- Stored in 1Password vault: [Vault Name]
- Environment variables in .env files
- Production secrets in AWS Secrets Manager

### Important Decisions
1. **Chose PostgreSQL over MongoDB**
   - Reason: Strong consistency requirements
   - Date: Jan 10
   - Decided by: Team consensus

2. **Microservices architecture**
   - Reason: Scalability requirements
   - Date: Jan 5
   - Impact: Increased complexity

### Known Technical Debt
1. Missing error boundaries in React
2. No request rate limiting
3. Incomplete logging setup
4. Manual deployment process

## Dependencies & Services
| Service | Purpose | Credentials |
|---------|---------|-------------|
| PostgreSQL | Database | In .env |
| Redis | Caching | In .env |
| AWS S3 | File storage | IAM role |
| Stripe | Payments | Dashboard |
| SendGrid | Email | API key |

## Monitoring & Alerts
- **APM**: DataDog - [dashboard link]
- **Logs**: CloudWatch - [log group]
- **Uptime**: Pingdom - [status page]
- **Errors**: Sentry - [project link]

## Deployment Process
```bash
# Staging deployment
git checkout staging
git merge main
npm run test
npm run deploy:staging

# Production deployment
git checkout production
git merge staging
npm run test
npm run deploy:production
```

## Support & Escalation
1. **Level 1**: Check logs and monitoring
2. **Level 2**: Contact on-call developer
3. **Level 3**: Escalate to team lead
4. **Emergency**: Page DevOps team

## Handoff Actions
- [ ] Share all credentials
- [ ] Grant repository access
- [ ] Add to Slack channels
- [ ] Schedule knowledge transfer call
- [ ] Update documentation ownership
```

### Phase 5: Shift Handoff

```markdown
# End of Day Handoff

## Today's Summary
**Date**: [Current Date]
**Developer**: [Name]

## ✅ Completed Today
- Fixed authentication bug (#123)
- Merged PR #456
- Deployed hotfix to production
- Updated API documentation

## 🔄 In Progress
- User profile feature (75% complete)
  - Backend API done
  - Frontend in progress
  - Tests pending

## 🚨 Blockers/Issues
- Database connection pool exhaustion
  - Temporary fix applied
  - Need permanent solution tomorrow
  
## 📝 For Tomorrow
- Complete user profile feature
- Review PR #789
- Team standup at 10 AM
- Deploy to staging after tests pass

## Notes
- Customer reported slow response times
- Check monitoring dashboard in morning
- QA found edge case in payment flow
```

### Phase 6: Onboarding Guide

```markdown
# Developer Onboarding Guide

## Welcome to [Project Name]!

### Day 1: Environment Setup
- [ ] Get repository access
- [ ] Install required tools:
  - Node.js 18+
  - Docker Desktop
  - VS Code + extensions
- [ ] Clone repositories
- [ ] Set up local environment
- [ ] Run test suite

### Day 2: Architecture Overview
- [ ] Read architecture documentation
- [ ] Review database schema
- [ ] Understand service boundaries
- [ ] Learn deployment process

### Day 3: First Contribution
- [ ] Pick starter issue
- [ ] Create feature branch
- [ ] Make changes
- [ ] Submit PR
- [ ] Address review feedback

### Resources
- [Architecture Docs](docs/architecture.md)
- [API Reference](docs/api.md)
- [Coding Standards](docs/standards.md)
- [Testing Guide](docs/testing.md)

### Key Contacts
- Tech Lead: [Name] - Architecture questions
- DevOps: [Name] - Infrastructure help
- Product: [Name] - Requirements clarification

### Common Tasks
```bash
# Start development
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Deploy to staging
npm run deploy:staging
```

### Tips for Success
1. Ask questions early and often
2. Read existing code before writing new
3. Follow established patterns
4. Write tests for your changes
5. Document as you go
```

## Integration Points

### With `/task-init`
- Reference previous handoffs
- Continue from handoff point

### With `/standup`
- Use handoff for standup notes
- Track handoff items

### With `/commit`
- Include handoff reference in commits

## Best Practices

1. **Be Thorough**
   - Document all context
   - Include "why" not just "what"
   - List all blockers

2. **Be Clear**
   - Use simple language
   - Provide examples
   - Include commands

3. **Be Helpful**
   - Anticipate questions
   - Provide resources
   - Offer assistance

## Notes
- Generates comprehensive handoffs
- Tracks work progress
- Ensures smooth transitions
- Creates onboarding guides
- Never forgets critical context