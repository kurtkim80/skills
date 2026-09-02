# Test Suite Runner

Automated testing orchestrator that intelligently runs tests based on changed files, generates coverage reports, and can create missing tests.

## Purpose
- Run appropriate tests based on file changes
- Generate coverage reports with visual diffs
- Auto-fix simple test failures
- Create missing tests using specialized agents
- Ensure quality before commits

## Execution Steps

### Step 1: Detect Test Framework

Use Bash tool to check for test frameworks:
- Command: `[ -f "package.json" ] && cat package.json | grep -q "jest\|mocha\|vitest\|cypress" && echo "js" || echo ""`
- Description: "Detect JavaScript test framework"

Use Glob tool to find test configuration files:
- Pattern: `pytest.ini` or `setup.cfg` (Python)
- Pattern: `go.mod` (Go)
- Pattern: `Cargo.toml` (Rust)

Use Glob tool to locate test files:
- Pattern: `**/*.test.*` or `**/*.spec.*` or `**/*_test.*`

### Step 2: Analyze Changed Files

Use Bash tool to get modified files:
- Command: `git diff --name-only HEAD`
- Description: "Get uncommitted changed files"

Use Bash tool to get staged files:
- Command: `git diff --staged --name-only`
- Description: "Get staged files"

### Step 3: Select Test Strategy

Output: "Select test scope:
1. Changed files only - Test files related to modifications
2. Unit tests - Fast, isolated component tests
3. Integration tests - Component interaction tests
4. E2E tests - Full user workflow tests
5. Full suite - All available tests
6. Custom pattern - Specify test pattern

Choose scope (1-6):"

WAIT for user's choice.

Output: "Enable coverage report? (y/n):"
WAIT for user's response.

Output: "Auto-fix simple failures? (y/n):"
WAIT for user's response.

Output: "Create missing tests? (y/n):"
WAIT for user's response.

Output: "Fail on coverage decrease? (y/n):"
WAIT for user's response.

### Step 4: Execute Tests

Run tests based on detected framework and user's scope choice.

For JavaScript/TypeScript, use Bash tool:
- Command: `npm test -- --coverage --watchAll=false` (Jest)
- Or: `npm run test -- --coverage --run` (Vitest)
- Or: `npm test -- --reporter spec` (Mocha)
- Or: `npx cypress run` (E2E)
- Description: "Run test suite with coverage"

For Python, use Bash tool:
- Command: `pytest --cov=. --cov-report=html --cov-report=term`
- Or: `python -m unittest discover`
- Description: "Run Python tests with coverage"

For Go, use Bash tool:
- Command: `go test -v -cover ./...`
- Or: `go test -race -coverprofile=coverage.out ./...`
- Description: "Run Go tests with coverage"

For Rust, use Bash tool:
- Command: `cargo test --all`
- Or: `cargo tarpaulin --out Html`
- Description: "Run Rust tests"

Parse test output to extract:
- Failed tests
- Coverage metrics
- Flaky tests

### Step 5: Analyze Test Results with Agents

If tests failed, use Task tool to launch agents for analysis:

Use Task tool to launch 2 agents IN PARALLEL (single message with 2 Task tool invocations):

1. Task tool call:
   - subagent_type: "debugger"
   - prompt: "Analyze these test failures and identify root causes: [test output]"

2. Task tool call:
   - subagent_type: "test-automator"
   - prompt: "Suggest fixes for these failing tests: [test output]"

Wait for both agents to complete.

If user requested missing tests to be created:

Use Task tool to launch 2 agents IN PARALLEL (single message with 2 Task tool invocations):

1. Task tool call:
   - subagent_type: "test-automator"
   - prompt: "Generate test cases for this uncovered code: [code content]"

2. Task tool call:
   - subagent_type: "backend-architect"
   - prompt: "Validate these test approaches for correctness: [proposed tests]"

Wait for both agents to complete.

### Step 6: Apply Auto-Fixes

For common test failures, attempt auto-fixes:
- Update snapshots if needed
- Fix import paths
- Update mocked data
- Adjust timeouts
- Fix async handling

### Step 7: Generate Missing Tests
If missing tests detected:

1. **Analyze Untested Code**
   ```javascript
   // Example: Function without tests
   function calculateDiscount(price, percentage) {
     if (percentage < 0 || percentage > 100) {
       throw new Error('Invalid percentage');
     }
     return price * (1 - percentage / 100);
   }
   ```

2. **Generate Test Cases**
   ```javascript
   // Generated test
   describe('calculateDiscount', () => {
     test('applies correct discount', () => {
       expect(calculateDiscount(100, 20)).toBe(80);
     });
     
     test('handles zero discount', () => {
       expect(calculateDiscount(100, 0)).toBe(100);
     });
     
     test('throws on invalid percentage', () => {
       expect(() => calculateDiscount(100, -10)).toThrow();
       expect(() => calculateDiscount(100, 110)).toThrow();
     });
   });
   ```

3. **Review Generated Tests**

Output: "Review generated tests above. Accept? (y/n/edit):"
WAIT for user's response.

### Step 8: Generate Coverage Report
1. **Generate Visual Report**
   ```markdown
   ## Test Coverage Report
   
   ### Summary
   - **Statements**: 85.2% (1247/1463)
   - **Branches**: 78.4% (421/537)
   - **Functions**: 91.3% (189/207)
   - **Lines**: 86.1% (1198/1391)
   
   ### Coverage Change
   📈 +2.3% from previous run
   
   ### Uncovered Files
   | File | Coverage | Missing Lines |
   |------|----------|---------------|
   | auth.service.ts | 67% | 45-52, 78-81 |
   | payment.processor.ts | 72% | 123-145 |
   
   ### Critical Gaps
   - Authentication error handling (auth.service.ts:45-52)
   - Payment retry logic (payment.processor.ts:123-145)
   ```

2. **Coverage Diff**
   ```diff
   File: src/services/user.service.ts
   - Coverage: 78% → 85% (+7%)
   + Lines covered: 45-67 (new)
   - Uncovered: 89-92 (error handling)
   ```

### Step 9: Check Quality Gates
1. **Check Test Results**
   ```yaml
   quality_gates:
     tests_passing: true
     coverage_threshold: 80%
     no_console_logs: true
     no_skip_tests: true
     performance_benchmarks: pass
   ```

2. **Generate Report**
   ```markdown
   ## Test Suite Results
   
   ✅ **Passed**: 156/162 tests
   ❌ **Failed**: 6 tests
   ⏭️ **Skipped**: 3 tests
   
   ### Failed Tests
   1. UserService › should handle invalid email
      - Expected: ValidationError
      - Received: undefined
   
   ### Recommendations
   - Fix authentication tests before commit
   - Add tests for new payment module
   - Remove skipped tests or fix them
   ```

3. **Decision Point**

If tests failed:

Output: "Tests failed. Options: (fix/ignore/debug):"
WAIT for user's choice.

If user chooses 'fix': Attempt auto-fix or provide manual fix suggestions
If user chooses 'debug': Suggest running `/debug-assistant`
If user chooses 'ignore': Ask for reason and document

## Test Patterns

### Unit Test Detection
```javascript
// Matches: *.test.js, *.spec.ts, *.unit.js
const unitTestPattern = /\.(test|spec|unit)\.(js|ts|jsx|tsx)$/;
```

### Integration Test Detection
```javascript
// Matches: *.integration.js, *.int.test.js
const integrationPattern = /\.(integration|int\.test)\.(js|ts)$/;
```

### E2E Test Detection
```javascript
// Matches: *.e2e.js, cypress/*, playwright/*
const e2ePattern = /\.(e2e|cy)\.(js|ts)$|cypress|playwright/;
```

## Smart Test Selection

### Changed File Mapping
```javascript
// Map source files to their tests
const testMapping = {
  'src/services/user.service.ts': [
    'tests/unit/user.service.test.ts',
    'tests/integration/user.api.test.ts'
  ],
  'src/api/auth.controller.ts': [
    'tests/unit/auth.controller.test.ts',
    'tests/e2e/auth.e2e.ts'
  ]
};
```

### Dependency Analysis
- Detect which files import changed modules
- Run tests for dependent components
- Skip unrelated test suites

## Auto-Fix Strategies

### Snapshot Updates
```bash
# Jest
npm test -- -u

# Vitest
npm test -- --update
```

### Async Timeouts
```javascript
// Increase timeout for slow tests
jest.setTimeout(10000);
```

### Mock Updates
```javascript
// Update mocked responses
jest.mock('./api', () => ({
  fetchUser: jest.fn(() => Promise.resolve(updatedMockData))
}));
```

## Integration Points

### With `/commit`
- Runs automatically before commit
- Blocks commit on test failure (configurable)
- Includes test results in commit message

### With `/review-code`
- Suggests tests for new code
- Reviews test quality
- Identifies test anti-patterns

### With `/security-scan`
- Runs security tests
- Validates input sanitization
- Tests authentication/authorization

## Error Handling

### Test Timeout
- Kill long-running tests
- Report timeout location
- Suggest timeout increase

### Missing Dependencies
- Detect missing test packages
- Offer to install them
- Update package.json

### Flaky Tests
- Track intermittent failures
- Retry flaky tests (configurable)
- Report flakiness patterns

## Configuration

### .claude/test-config.json
```json
{
  "framework": "jest",
  "coverage": {
    "threshold": 80,
    "failOnDecrease": true
  },
  "autoFix": {
    "snapshots": true,
    "imports": true,
    "timeouts": false
  },
  "testPattern": "**/*.test.ts",
  "excludePattern": "**/node_modules/**",
  "parallel": true,
  "maxWorkers": 4
}
```

## Best Practices

1. **Test Pyramid**
   - Many unit tests (fast)
   - Some integration tests (moderate)
   - Few E2E tests (slow)

2. **Coverage Goals**
   - Aim for 80%+ coverage
   - Focus on critical paths
   - Don't chase 100%

3. **Test Quality**
   - Descriptive test names
   - Single assertion per test
   - Independent test cases

4. **Performance**
   - Run tests in parallel
   - Use test doubles
   - Minimize I/O operations

## Notes
- Integrates with all major test frameworks
- Supports multiple languages
- Can generate tests using AI
- Never commits failing tests
- Maintains test history for trend analysis