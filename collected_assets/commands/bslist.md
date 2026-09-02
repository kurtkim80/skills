# Brainstorm List Viewer

Quick access command to view and retrieve recent brainstorm sessions with search and filtering capabilities.

## Purpose
- List recent brainstorm sessions
- Quick overview of ideas explored
- Search past brainstorms
- Resume or reference previous sessions
- Track ideation history

## Workflow

### Phase 1: Display Options
1. **STOP** → "Brainstorm list options:"
   ```
   1. Recent - Last 10 brainstorms (default)
   2. All - Complete list
   3. Search - Find by keyword
   4. Filter - By status/date/topic
   5. Detail - View specific brainstorm
   
   Choose option (1-5):
   ```

2. **List Options**
   - STOP → "Sort by? (date/name/status):"
   - STOP → "Include archived? (y/n):"
   - STOP → "Show full preview? (y/n):"

### Phase 2: Brainstorm Discovery

#### Find Brainstorm Files
```bash
# List all brainstorm files
find .claude/brainstorms -name "brainstorm-*.md" -type f | \
  xargs ls -lt | \
  head -10

# Get file metadata
for file in .claude/brainstorms/brainstorm-*.md; do
  if [ -f "$file" ]; then
    modified=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$file" 2>/dev/null || \
               stat -c "%y" "$file" 2>/dev/null | cut -d' ' -f1-2)
    echo "$modified|$file"
  fi
done | sort -r
```

#### Parse Brainstorm Metadata
```javascript
function parseBrainstormFile(filepath) {
  const content = fs.readFileSync(filepath, 'utf8');
  const lines = content.split('\n');
  
  // Extract metadata
  const title = lines.find(l => l.startsWith('#'))?.replace('#', '').trim();
  const sessionId = lines.find(l => l.includes('Session ID'))?.split(':')[1]?.trim();
  const date = lines.find(l => l.includes('Date:'))?.split(':', 2)[1]?.trim();
  const status = lines.find(l => l.includes('Status:'))?.split(':')[1]?.trim();
  const decision = lines.find(l => l.includes('Decision:'))?.split(':')[1]?.trim();
  
  // Get summary (first paragraph after metadata)
  const summaryStart = lines.findIndex(l => l.includes('## Original Concept'));
  const summary = lines[summaryStart + 1]?.substring(0, 100) + '...';
  
  return {
    file: filepath,
    title,
    sessionId,
    date,
    status,
    decision,
    summary
  };
}
```

### Phase 3: List Display Formats

#### Standard List View
```markdown
# Recent Brainstorms (Last 10)

## 1. 🧠 Authentication System Redesign
   **Date**: 2024-01-15 14:30
   **Status**: ✅ Implemented
   **Decision**: Proceed with JWT + OAuth2
   **Summary**: Exploring options for modernizing auth system...
   **File**: brainstorm-auth-system-redesign.md

## 2. 💡 Real-time Notifications Architecture  
   **Date**: 2024-01-14 10:15
   **Status**: 🔄 Active
   **Decision**: Pending
   **Summary**: Evaluating WebSockets vs SSE vs Long Polling...
   **File**: brainstorm-realtime-notifications.md

## 3. 🎯 Database Sharding Strategy
   **Date**: 2024-01-12 16:45
   **Status**: 📝 Researching
   **Decision**: Defer
   **Summary**: Analyzing horizontal scaling options for user data...
   **File**: brainstorm-database-sharding.md

## 4. 🚀 CI/CD Pipeline Optimization
   **Date**: 2024-01-10 09:00
   **Status**: ✅ Implemented
   **Decision**: Migrate to GitHub Actions
   **Summary**: Reducing build times and improving deployment...
   **File**: brainstorm-cicd-optimization.md

## 5. 🔐 Zero-Trust Security Model
   **Date**: 2024-01-08 13:20
   **Status**: 📋 Planned
   **Decision**: Approve for Q2
   **Summary**: Implementing principle of least privilege across...
   **File**: brainstorm-zero-trust-security.md

[Showing 5 of 23 total brainstorms]
```

#### Detailed List View
```markdown
# Brainstorm Sessions - Detailed View

## 1. Authentication System Redesign
**Session**: bs_20240115_143000
**Created**: 2024-01-15 14:30:00
**Modified**: 2024-01-15 16:45:32
**Status**: Implemented
**Decision**: Proceed

### Context
Exploring options for modernizing authentication system to support SSO, 
social login, and improved security with JWT tokens and OAuth2 flow.

### Key Decisions
- Chose JWT over sessions for stateless auth
- Implemented refresh token rotation
- Added OAuth2 for third-party integrations

### Outcomes
- Specification created: auth-redesign-spec.md
- Tasks generated: 12 tasks
- Implementation time: 3 days
- **Result**: Successfully deployed to production

### Related
- Commits: 8 commits referencing this brainstorm
- PR: #234 - Implement new auth system
- Documentation: /docs/auth/new-system.md

---

## 2. Real-time Notifications Architecture
**Session**: bs_20240114_101500
**Created**: 2024-01-14 10:15:00
**Modified**: 2024-01-14 12:30:45
**Status**: Active
**Decision**: Pending

### Context
Evaluating different approaches for implementing real-time notifications
including WebSockets, Server-Sent Events, and Long Polling.

### Current Analysis
- WebSockets: Best for bidirectional, high-frequency
- SSE: Simpler, unidirectional, good browser support  
- Long Polling: Fallback option, higher latency

### Open Questions
- Expected message volume?
- Need for bidirectional communication?
- Browser compatibility requirements?

### Next Steps
- Performance testing with each approach
- Cost analysis for infrastructure
- Review with frontend team

[More details available - run `/brainstorm` to resume]
```

#### Compact Table View
```markdown
# Brainstorm List

| # | Title | Date | Status | Decision | Summary |
|---|-------|------|--------|----------|---------|
| 1 | Auth System Redesign | 2024-01-15 | ✅ Implemented | Proceed | JWT + OAuth2... |
| 2 | Real-time Notifications | 2024-01-14 | 🔄 Active | Pending | WebSockets vs SSE... |
| 3 | Database Sharding | 2024-01-12 | 📝 Researching | Defer | Horizontal scaling... |
| 4 | CI/CD Optimization | 2024-01-10 | ✅ Implemented | Migrate | GitHub Actions... |
| 5 | Zero-Trust Security | 2024-01-08 | 📋 Planned | Q2 | Least privilege... |
| 6 | Microservices Split | 2024-01-05 | ❌ Rejected | No | Too complex... |
| 7 | GraphQL Migration | 2024-01-03 | 🔄 Active | Research | REST vs GraphQL... |
| 8 | Cache Strategy | 2023-12-28 | ✅ Implemented | Redis | Multi-tier cache... |
| 9 | Search Enhancement | 2023-12-22 | 📝 Researching | Pending | Elasticsearch... |
| 10 | Payment Integration | 2023-12-20 | ✅ Implemented | Stripe | Multiple gateways... |

Commands: 
- View details: `/brainstorm-detail [#]`
- Resume session: `/brainstorm-resume [#]`
- Search: `/bslist search [keyword]`
```

### Phase 4: Search and Filter

#### Keyword Search
```bash
# Search in brainstorm files
grep -l "keyword" .claude/brainstorms/brainstorm-*.md | \
  xargs ls -lt | \
  head -10

# Search with context
grep -A 3 -B 3 "keyword" .claude/brainstorms/brainstorm-*.md
```

#### Filter by Status
```javascript
function filterBrainstorms(criteria) {
  const allBrainstorms = getAllBrainstorms();
  
  return allBrainstorms.filter(bs => {
    // Status filter
    if (criteria.status && bs.status !== criteria.status) {
      return false;
    }
    
    // Date range filter
    if (criteria.dateFrom && new Date(bs.date) < new Date(criteria.dateFrom)) {
      return false;
    }
    
    // Decision filter
    if (criteria.decision && bs.decision !== criteria.decision) {
      return false;
    }
    
    // Tag filter
    if (criteria.tags && !criteria.tags.some(tag => bs.content.includes(tag))) {
      return false;
    }
    
    return true;
  });
}
```

### Phase 5: Brainstorm Statistics

```markdown
# Brainstorm Analytics

## Summary Statistics
- **Total Brainstorms**: 23
- **Active Sessions**: 3
- **Implemented Ideas**: 8 (35%)
- **Average Session Duration**: 45 minutes
- **Success Rate**: 73%

## Status Breakdown
```
Implemented  ████████████░░░░░░░░ 35%
Active       ███░░░░░░░░░░░░░░░░░ 13%
Planned      ██████░░░░░░░░░░░░░░ 26%
Researching  ████░░░░░░░░░░░░░░░░ 17%
Deferred     ██░░░░░░░░░░░░░░░░░░  9%
```

## Topics Distribution
1. Architecture (7 sessions)
2. Performance (5 sessions)
3. Security (4 sessions)
4. Features (4 sessions)
5. Infrastructure (3 sessions)

## Implementation Timeline
- Ideas to Implementation: Average 5.2 days
- Fastest: 1 day (CI/CD Optimization)
- Longest: 15 days (Auth System)

## Top Contributors
Based on brainstorm to implementation:
1. Auth System → 12 tasks completed
2. Cache Strategy → 8 tasks completed
3. CI/CD Pipeline → 6 tasks completed
```

### Phase 6: Quick Actions

#### Resume Brainstorm
```bash
# Get specific brainstorm
brainstorm_file=".claude/brainstorms/brainstorm-auth-system.md"

# Display current state
cat "$brainstorm_file"

# Resume with context
echo "Resuming brainstorm session..."
echo "Last updated: $(stat -f "%Sm" "$brainstorm_file")"
```

#### Export Brainstorm
```bash
# Export as specification
cp .claude/brainstorms/brainstorm-[name].md .claude/specs/[name]-spec.md

# Export as tasks
grep -A 100 "## Implementation Plan" .claude/brainstorms/brainstorm-[name].md | \
  grep "^- \[" >> todos/todos.md

# Export as documentation
cp .claude/brainstorms/brainstorm-[name].md docs/design/[name]-design.md
```

### Phase 7: Interactive Options

After displaying list:

1. **STOP** → "Select action:"
   ```
   1. View details (enter number)
   2. Resume session (enter number)
   3. Export to spec (enter number)
   4. Archive (enter number)
   5. Delete (enter number)
   6. Search different term
   7. Change filter
   8. Exit
   
   Choose action:
   ```

2. **Quick Commands**
   - `v5` - View details of item 5
   - `r3` - Resume brainstorm 3
   - `e2` - Export brainstorm 2
   - `s keyword` - Search for keyword
   - `f active` - Filter by active status

## Display Customization

### Status Indicators
```
✅ Implemented - Idea successfully implemented
🔄 Active - Currently being explored
📝 Researching - Gathering information
📋 Planned - Approved for future
⏸️ Deferred - On hold
❌ Rejected - Not proceeding
💭 Draft - Initial thoughts only
```

### Priority Markers
```
🔴 Critical - Urgent implementation needed
🟠 High - Important, plan soon
🟡 Medium - Standard priority
🟢 Low - Nice to have
⚪ Undefined - No priority set
```

## Integration

### With `/brainstorm`
- Resume any listed session
- Continue from last state
- Build on previous ideas

### With `/task-init`
- Convert brainstorms to tasks
- Use context for implementation

### With `/read-specs`
- Export brainstorms as specs
- Transition to development

## Configuration

### .claude/bslist-config.json
```json
{
  "display": {
    "default": "recent",
    "limit": 10,
    "format": "standard",
    "showArchived": false,
    "sortBy": "date",
    "sortOrder": "desc"
  },
  "filters": {
    "statuses": ["Active", "Planned", "Researching"],
    "daysBack": 30,
    "excludeImplemented": false
  },
  "export": {
    "formats": ["markdown", "json", "csv"],
    "includeMetadata": true,
    "includeHistory": false
  },
  "actions": {
    "quickView": true,
    "quickResume": true,
    "quickExport": true
  }
}
```

## Search Patterns

### Complex Searches
```bash
# Find brainstorms with multiple keywords
grep -l "auth" .claude/brainstorms/*.md | \
  xargs grep -l "oauth" | \
  xargs grep -l "jwt"

# Find by date range
find .claude/brainstorms -name "*.md" \
  -newermt "2024-01-01" \
  -not -newermt "2024-01-31"

# Find by status
grep -l "Status:.*Active" .claude/brainstorms/*.md
```

## Best Practices

1. **Regular Review**
   - Check active brainstorms weekly
   - Archive completed sessions
   - Update statuses

2. **Context Preservation**
   - Keep all brainstorms
   - Reference in commits
   - Link to implementations

3. **Knowledge Management**
   - Tag brainstorms consistently
   - Document decisions
   - Track outcomes

## Notes
- Lists up to 10 recent by default
- Searchable history
- Quick resume capability
- Export to various formats
- Never loses brainstorm context