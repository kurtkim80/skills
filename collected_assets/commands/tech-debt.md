# Technical Debt Tracker

Scans for code that needs refactoring, tracks TODO/FIXME comments, prioritizes cleanup tasks, and estimates maintenance costs.

## Purpose
- Scan for code needing refactoring
- Track TODO/FIXME comments
- Generate refactoring priorities
- Estimate debt "interest" (maintenance cost)
- Create cleanup tasks

## Workflow

### Step 1: Debt Analysis Type
1. **STOP** → "Select technical debt analysis:"
   ```
   1. Quick scan - TODO/FIXME comments only
   2. Code quality - Complexity and duplication
   3. Dependencies - Outdated and vulnerable
   4. Architecture - Design and structure issues
   5. Full analysis - Complete debt assessment
   
   Choose type (1-5):
   ```

2. **Analysis Options**
   - STOP → "Generate refactoring plan? (y/n):"
   - STOP → "Estimate effort/cost? (y/n):"
   - STOP → "Create cleanup tasks? (y/n):"
   - STOP → "Track debt trends? (y/n):"

### Step 2: Code Annotation Scanning

#### TODO/FIXME Detection
```bash
# Find all TODO comments
grep -rn "TODO\|FIXME\|HACK\|XXX\|OPTIMIZE\|REFACTOR" \
  --include="*.js" --include="*.ts" --include="*.py" \
  --exclude-dir=node_modules --exclude-dir=.git

# Parse and categorize
rg "TODO|FIXME|HACK" --json | jq -r '.data.lines.text'
```

#### Comment Analysis
```javascript
const annotations = {
  TODO: [],      // General tasks
  FIXME: [],     // Bugs to fix
  HACK: [],      // Temporary workarounds
  OPTIMIZE: [],  // Performance improvements
  REFACTOR: [],  // Code cleanup needed
  DEPRECATED: [] // Code to remove
};

// Parse comments
function parseAnnotations(file, content) {
  const lines = content.split('\n');
  lines.forEach((line, index) => {
    const match = line.match(/(TODO|FIXME|HACK|XXX|OPTIMIZE|REFACTOR|DEPRECATED):\s*(.*)/);
    if (match) {
      annotations[match[1]].push({
        file,
        line: index + 1,
        type: match[1],
        message: match[2],
        priority: calculatePriority(match[1], match[2])
      });
    }
  });
}
```

### Step 3: Code Quality Analysis

#### Complexity Metrics
```javascript
// Cyclomatic complexity
function calculateComplexity(ast) {
  let complexity = 1;
  
  traverse(ast, {
    IfStatement: () => complexity++,
    ConditionalExpression: () => complexity++,
    ForStatement: () => complexity++,
    WhileStatement: () => complexity++,
    DoWhileStatement: () => complexity++,
    CatchClause: () => complexity++,
    CaseClause: () => complexity++,
    LogicalExpression: (node) => {
      if (node.operator === '&&' || node.operator === '||') {
        complexity++;
      }
    }
  });
  
  return complexity;
}

// High complexity functions (> 10)
const complexFunctions = functions.filter(fn => 
  calculateComplexity(fn.ast) > 10
);
```

#### Code Duplication
```javascript
// Detect duplicate code blocks
function findDuplicates(files) {
  const hashes = new Map();
  const duplicates = [];
  
  files.forEach(file => {
    const blocks = extractCodeBlocks(file);
    blocks.forEach(block => {
      const hash = crypto.createHash('md5')
        .update(normalizeCode(block.code))
        .digest('hex');
      
      if (hashes.has(hash)) {
        duplicates.push({
          original: hashes.get(hash),
          duplicate: block,
          lines: block.code.split('\n').length
        });
      } else {
        hashes.set(hash, block);
      }
    });
  });
  
  return duplicates;
}
```

#### Code Smells
```yaml
code_smells:
  long_method:
    threshold: 50 lines
    severity: medium
    
  large_class:
    threshold: 500 lines
    severity: high
    
  long_parameter_list:
    threshold: 4 parameters
    severity: low
    
  god_class:
    threshold: 20 methods
    severity: critical
    
  duplicate_code:
    threshold: 20 lines
    severity: medium
    
  dead_code:
    detection: unused exports
    severity: low
```

### Step 4: Dependency Debt

#### Outdated Dependencies
```bash
# npm/yarn
npm outdated --json
yarn outdated --json

# Python
pip list --outdated

# Go
go list -u -m all
```

#### Vulnerability Scan
```javascript
// Check for known vulnerabilities
async function checkVulnerabilities() {
  const audit = await exec('npm audit --json');
  const vulnerabilities = JSON.parse(audit);
  
  return {
    critical: vulnerabilities.metadata.vulnerabilities.critical,
    high: vulnerabilities.metadata.vulnerabilities.high,
    moderate: vulnerabilities.metadata.vulnerabilities.moderate,
    low: vulnerabilities.metadata.vulnerabilities.low,
    packages: Object.keys(vulnerabilities.vulnerabilities)
  };
}
```

#### Unused Dependencies
```javascript
// Find unused packages
const depcheck = require('depcheck');

depcheck(process.cwd(), {}, (unused) => {
  console.log('Unused dependencies:', unused.dependencies);
  console.log('Unused devDependencies:', unused.devDependencies);
  console.log('Missing dependencies:', unused.missing);
});
```

### Step 5: Architecture Debt

#### Design Pattern Violations
```javascript
// Check for anti-patterns
const antiPatterns = {
  // Circular dependencies
  circular: findCircularDependencies(),
  
  // Tight coupling
  coupling: calculateCoupling(),
  
  // God objects
  godObjects: findGodObjects(),
  
  // Anemic domain models
  anemicModels: findAnemicModels(),
  
  // Spaghetti code
  spaghetti: measureCodeOrganization()
};
```

#### Layer Violations
```javascript
// Check architecture boundaries
function checkLayerViolations() {
  const violations = [];
  
  // Controller shouldn't access database directly
  if (importsIn('controllers/').include('database/')) {
    violations.push({
      type: 'layer_violation',
      message: 'Controller accessing database directly',
      severity: 'high'
    });
  }
  
  // Domain shouldn't depend on infrastructure
  if (importsIn('domain/').include('infrastructure/')) {
    violations.push({
      type: 'dependency_inversion',
      message: 'Domain depends on infrastructure',
      severity: 'critical'
    });
  }
  
  return violations;
}
```

### Step 6: Debt Quantification

#### Interest Calculation
```javascript
function calculateDebtInterest(debt) {
  const hourlyRate = 100; // $100/hour
  
  // Time cost of working around debt
  const workaroundTime = debt.instances * debt.avgWorkaroundMinutes;
  
  // Increased bug risk
  const bugRisk = debt.complexity * 0.1 * hourlyRate;
  
  // Onboarding cost
  const onboardingCost = debt.complexity * 0.5 * hourlyRate;
  
  // Monthly interest
  const monthlyInterest = (workaroundTime / 60) * hourlyRate + bugRisk;
  
  return {
    principal: debt.estimatedFixHours * hourlyRate,
    monthlyInterest,
    breakEvenMonths: debt.estimatedFixHours * hourlyRate / monthlyInterest
  };
}
```

#### Debt Categories
```markdown
## Technical Debt Summary

### 🔴 Critical (Fix immediately)
| Item | Type | Effort | Monthly Cost |
|------|------|--------|--------------|
| SQL injection vulnerability | Security | 4h | $2,000 |
| Memory leak in user service | Performance | 8h | $1,500 |
| No error boundaries | Reliability | 6h | $1,200 |

### 🟠 High (Fix this sprint)
| Item | Type | Effort | Monthly Cost |
|------|------|--------|--------------|
| Duplicate payment logic | Maintenance | 12h | $800 |
| Missing API tests | Quality | 16h | $600 |
| Hardcoded configuration | Flexibility | 4h | $400 |

### 🟡 Medium (Plan for next quarter)
| Item | Type | Effort | Monthly Cost |
|------|------|--------|--------------|
| Inconsistent naming | Readability | 8h | $200 |
| TODO comments (47) | Completion | 20h | $150 |
| Outdated dependencies | Maintenance | 6h | $300 |

### Total Debt
- **Principal**: $4,200 (42 hours)
- **Monthly Interest**: $7,150
- **Break-even**: 0.6 months
```

### Step 7: Refactoring Plan

#### Priority Matrix
```
        Effort →
    Low         High
High ┌─────────┬─────────┐
  ↑  │ Quick   │ Major   │
Value│ Wins    │ Projects│
     ├─────────┼─────────┤
Low  │ Maybe   │ Avoid   │
     │ Later   │         │
     └─────────┴─────────┘
```

#### Refactoring Tasks
```markdown
## Refactoring Plan

### Week 1: Quick Wins
- [ ] Remove dead code (2h)
- [ ] Fix naming inconsistencies (3h)
- [ ] Update deprecated APIs (2h)
- [ ] Extract magic numbers (1h)

### Week 2-3: Medium Tasks
- [ ] Extract duplicate code to utilities (8h)
- [ ] Simplify complex conditionals (6h)
- [ ] Add missing error handling (8h)
- [ ] Improve test coverage (12h)

### Month 2: Major Refactoring
- [ ] Redesign authentication module (24h)
- [ ] Implement repository pattern (20h)
- [ ] Migrate to new framework version (16h)
- [ ] Restructure database schema (32h)

### Continuous Improvements
- [ ] Add linting rules for new patterns
- [ ] Document architecture decisions
- [ ] Create refactoring guidelines
- [ ] Automate debt tracking
```

### Step 8: Debt Prevention

#### Quality Gates
```yaml
quality_gates:
  complexity:
    max: 10
    action: block_merge
    
  duplication:
    max: 3%
    action: warning
    
  coverage:
    min: 80%
    action: block_merge
    
  todos:
    max_age: 30 days
    action: create_issue
```

#### Automated Checks
```javascript
// Pre-commit hook
function preCommitCheck() {
  const checks = [
    checkComplexity(),
    checkDuplication(),
    checkTODOAge(),
    checkTestCoverage()
  ];
  
  const failures = checks.filter(c => !c.passed);
  if (failures.length > 0) {
    console.error('Debt checks failed:', failures);
    process.exit(1);
  }
}
```

### Step 9: Reporting

```markdown
# Technical Debt Report

## Executive Summary
- **Total Debt**: 142 items
- **Estimated Cost**: $42,000
- **Monthly Interest**: $7,150
- **Debt Ratio**: 23% of codebase

## Debt Trends
```
Debt Score
100 │
 90 │      ╱╲
 80 │     ╱  ╲
 70 │    ╱    ╲___
 60 │   ╱          ╲___
 50 │__╱                ╲
    └────────────────────
    J F M A M J J A S O N D
```

## Top Debt Sources
1. **Legacy authentication system** (30% of debt)
2. **Untested payment module** (20% of debt)
3. **Database N+1 queries** (15% of debt)
4. **Duplicate business logic** (10% of debt)
5. **Outdated dependencies** (8% of debt)

## Recommendations

### Immediate Actions
1. Fix security vulnerabilities
2. Add error boundaries
3. Update critical dependencies

### Short-term (1-3 months)
1. Refactor authentication
2. Add comprehensive tests
3. Remove duplicate code

### Long-term (3-6 months)
1. Migrate to microservices
2. Implement design system
3. Automate debt tracking

## ROI Analysis
- **Investment**: 142 hours ($14,200)
- **Monthly Savings**: $7,150
- **Payback Period**: 2 months
- **Annual ROI**: 500%
```

## Integration

### With `/review-code`
- Track debt during reviews
- Prevent new debt

### With `/task-init`
- Create debt cleanup tasks
- Prioritize refactoring

### With `/standup`
- Report debt metrics
- Track cleanup progress

## Configuration

### .claude/debt-config.json
```json
{
  "scanning": {
    "includePaths": ["src/", "lib/"],
    "excludePaths": ["node_modules/", "dist/"],
    "annotations": ["TODO", "FIXME", "HACK", "XXX"]
  },
  "thresholds": {
    "complexity": 10,
    "duplication": 20,
    "fileLength": 500,
    "methodLength": 50
  },
  "reporting": {
    "format": "markdown",
    "output": "tech-debt-report.md",
    "frequency": "weekly"
  },
  "automation": {
    "createIssues": true,
    "assignOwners": true,
    "trackTrends": true
  }
}
```

## Best Practices

1. **Track Continuously**
   - Monitor debt trends
   - Set debt budgets
   - Regular reviews

2. **Prioritize Wisely**
   - Fix high-interest debt first
   - Bundle related refactoring
   - Balance with features

3. **Prevent Accumulation**
   - Quality gates
   - Code reviews
   - Refactoring sprints

## Notes
- Quantifies technical debt
- Calculates maintenance costs
- Prioritizes refactoring
- Tracks debt trends
- Never ignores critical debt