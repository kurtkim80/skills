# Intelligent Debugging Helper

Advanced debugging assistant that analyzes errors, suggests fixes, traces root causes, and sets up debugging environments.

## Purpose
- Analyze error logs and stack traces
- Suggest fixes based on error patterns
- Set up debugging environments
- Generate reproduction steps
- Track down root causes with specialized agents

## Workflow

### Step 1: Error Input
1. **STOP** → "How would you like to provide the error?"
   ```
   1. Paste error message/stack trace
   2. Point to log file
   3. Describe the issue
   4. Run failing command
   5. Analyze recent crashes
   
   Choose method (1-5):
   ```

2. **Context Gathering**
   - STOP → "When did this error start? (timestamp/commit/today):"
   - STOP → "Is it reproducible? (always/sometimes/once):"
   - STOP → "What were you doing when it occurred?:"

### Step 2: Error Analysis
1. **Parse Error Information**
   ```javascript
   // Extract key information
   const errorInfo = {
     type: "TypeError",
     message: "Cannot read property 'x' of undefined",
     file: "src/components/UserList.jsx",
     line: 45,
     column: 12,
     stack: [...],
     timestamp: "2024-01-15T10:30:00Z"
   };
   ```

2. **Categorize Error Type**
   ```yaml
   error_categories:
     - Runtime Errors:
       - TypeError
       - ReferenceError
       - RangeError
     - Async Errors:
       - Promise rejection
       - Callback errors
       - Race conditions
     - Network Errors:
       - Connection refused
       - Timeout
       - CORS issues
     - Build Errors:
       - Compilation failure
       - Module not found
       - Syntax errors
   ```

3. **Deploy Analysis Agents**
   - **debugger**: Deep error analysis
   - **backend-architect**: System-level debugging
   - **test-automator**: Create reproduction test
   - **performance-engineer**: Performance-related issues

### Step 3: Root Cause Analysis
1. **Trace Error Source**
   ```bash
   # Git blame to find when introduced
   git blame -L 40,50 src/components/UserList.jsx
   
   # Check recent changes
   git log -p --since="2 days ago" src/components/UserList.jsx
   ```

2. **Analyze Code Context**
   ```javascript
   // Problem code
   function UserList({ users }) {
     return users.map(user => (
       <div>{user.profile.name}</div>  // Error here
     ));
   }
   
   // Analysis:
   // - user.profile might be undefined
   // - users might be null
   // - Missing null checks
   ```

3. **Check Dependencies**
   ```bash
   # Did dependencies change?
   git diff HEAD~1 package-lock.json
   
   # Check for breaking changes
   npm outdated
   ```

### Step 4: Solution Generation
1. **Generate Fix Options**
   ```javascript
   // Option 1: Add null checks
   function UserList({ users = [] }) {
     return users.map(user => (
       <div>{user?.profile?.name || 'Unknown'}</div>
     ));
   }
   
   // Option 2: Add validation
   function UserList({ users }) {
     if (!users || !Array.isArray(users)) {
       return <div>No users</div>;
     }
     return users.map(user => (
       <div>{user.profile?.name}</div>
     ));
   }
   
   // Option 3: Add default props
   UserList.defaultProps = {
     users: []
   };
   ```

2. **Test Fixes**
   ```javascript
   // Generate test cases
   describe('UserList fix validation', () => {
     test('handles null users', () => {
       expect(() => UserList({ users: null })).not.toThrow();
     });
     
     test('handles users without profile', () => {
       const users = [{ id: 1 }];
       expect(() => UserList({ users })).not.toThrow();
     });
   });
   ```

### Step 5: Debugging Environment Setup
1. **Configure Debugger**
   ```json
   // .vscode/launch.json
   {
     "version": "0.2.0",
     "configurations": [{
       "type": "node",
       "request": "launch",
       "name": "Debug Error",
       "program": "${workspaceFolder}/src/index.js",
       "stopOnEntry": false,
       "breakpoints": ["src/components/UserList.jsx:45"]
     }]
   }
   ```

2. **Add Debug Logging**
   ```javascript
   // Temporary debug code
   console.log('DEBUG: users =', JSON.stringify(users, null, 2));
   console.log('DEBUG: user =', user);
   console.log('DEBUG: user.profile =', user?.profile);
   ```

3. **Set Up Remote Debugging**
   ```bash
   # Node.js
   node --inspect-brk=0.0.0.0:9229 app.js
   
   # Chrome DevTools
   chrome://inspect
   
   # VS Code attach
   ```

### Step 6: Reproduction Steps
1. **Generate Minimal Reproduction**
   ```markdown
   ## Steps to Reproduce
   
   1. Start the application: `npm start`
   2. Navigate to /users
   3. Click "Load More"
   4. Error appears in console
   
   ## Expected Behavior
   Users list should load additional items
   
   ## Actual Behavior
   TypeError: Cannot read property 'x' of undefined
   
   ## Environment
   - Node: 18.17.0
   - Browser: Chrome 120
   - OS: macOS 14.0
   ```

2. **Create Reproduction Script**
   ```javascript
   // reproduce-error.js
   const UserList = require('./src/components/UserList');
   
   // This triggers the error
   const problematicData = [
     { id: 1, name: 'User 1' },  // Missing profile
     { id: 2, profile: { name: 'User 2' } }
   ];
   
   UserList({ users: problematicData });
   ```

### Step 7: Common Error Patterns

#### JavaScript/TypeScript
```javascript
// Cannot read property of undefined
obj?.property?.nested

// Array is not iterable
[...(array || [])]

// Async errors
try {
  await someAsyncFunction();
} catch (error) {
  console.error('Async error:', error);
}
```

#### Python
```python
# KeyError
value = dict.get('key', default_value)

# AttributeError
if hasattr(obj, 'attribute'):
    obj.attribute

# IndexError
if len(array) > index:
    array[index]
```

#### Database
```sql
-- Connection timeout
SET statement_timeout = '30s';

-- Deadlock
BEGIN;
LOCK TABLE users IN SHARE ROW EXCLUSIVE MODE;

-- Missing index
CREATE INDEX idx_users_email ON users(email);
```

### Step 8: Performance Debugging
1. **Profile Performance**
   ```javascript
   console.time('operation');
   // Slow operation
   console.timeEnd('operation');
   
   // Memory profiling
   console.log(process.memoryUsage());
   ```

2. **Identify Bottlenecks**
   ```bash
   # Node.js profiling
   node --prof app.js
   node --prof-process isolate-*.log
   
   # Browser profiling
   performance.mark('start');
   // Code
   performance.mark('end');
   performance.measure('operation', 'start', 'end');
   ```

### Step 9: Fix Verification
1. **Test the Fix**
   ```bash
   # Run specific test
   npm test -- UserList.test.js
   
   # Run regression tests
   npm test
   ```

2. **Verify in Multiple Environments**
   ```bash
   # Different Node versions
   nvm use 16 && npm test
   nvm use 18 && npm test
   
   # Different browsers
   npm run test:chrome
   npm run test:firefox
   ```

### Step 10: Documentation
```markdown
# Debug Report

## Issue Summary
**Error**: TypeError: Cannot read property 'name' of undefined
**Location**: src/components/UserList.jsx:45
**Severity**: High
**Status**: RESOLVED

## Root Cause
Missing null check for user.profile object when users array contains items without profile data.

## Solution Applied
Added optional chaining and default values:
```javascript
<div>{user?.profile?.name || 'Unknown'}</div>
```

## Prevention
1. Add TypeScript for type safety
2. Implement prop validation
3. Add unit tests for edge cases
4. Use default props

## Lessons Learned
- Always validate external data
- Use optional chaining for nested properties
- Test with incomplete data

## Related Issues
- #123: Similar error in UserCard component
- #456: Add global error boundary
```

## Error Pattern Database

### Common Patterns
```yaml
patterns:
  - pattern: "Cannot read property .* of undefined"
    solution: "Add null checks or optional chaining"
    
  - pattern: "Module not found"
    solution: "Check import paths and install dependencies"
    
  - pattern: "ECONNREFUSED"
    solution: "Check if service is running and port is correct"
    
  - pattern: "CORS policy"
    solution: "Configure CORS headers on server"
    
  - pattern: "Maximum call stack"
    solution: "Check for infinite recursion or circular dependencies"
```

## Integration

### With `/test-suite`
- Create tests for bug fixes
- Verify fixes don't break existing tests

### With `/review-code`
- Review fix for best practices
- Check for similar issues

### With `/tech-debt`
- Track recurring errors
- Identify systemic issues

## Configuration

### .claude/debug-config.json
```json
{
  "autoFix": {
    "enabled": true,
    "types": ["null-check", "import", "syntax"]
  },
  "logging": {
    "level": "debug",
    "output": "debug.log"
  },
  "breakpoints": {
    "onError": true,
    "onWarning": false
  }
}
```

## Best Practices

1. **Systematic Approach**
   - Reproduce first
   - Isolate the issue
   - Fix root cause, not symptoms
   - Test thoroughly

2. **Documentation**
   - Document the fix
   - Share with team
   - Update runbook

3. **Prevention**
   - Add tests for the bug
   - Improve error handling
   - Add monitoring

## Notes
- Uses specialized debugging agents
- Maintains error pattern database
- Can auto-fix common issues
- Generates comprehensive debug reports
- Never ignores error patterns