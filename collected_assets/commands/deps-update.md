# Dependency Manager

Comprehensive dependency updater that checks for outdated packages, tests compatibility, manages security patches, and handles lock files.

## Purpose
- Check for outdated packages
- Test compatibility before updating  
- Security vulnerability patches
- Generate update changelog
- Lock file management

## Workflow

### Step 1: Update Strategy
1. **STOP** → "Select update strategy:"
   ```
   1. Security only - Critical patches only
   2. Patch updates - Bug fixes (1.0.x)
   3. Minor updates - New features (1.x.0)
   4. Major updates - Breaking changes (x.0.0)
   5. Interactive - Choose each update
   6. Full update - Everything latest
   
   Choose strategy (1-6):
   ```

2. **Update Options**
   - STOP → "Run tests after update? (y/n):"
   - STOP → "Create separate branch? (y/n):"
   - STOP → "Update lock files? (y/n):"
   - STOP → "Generate changelog? (y/n):"

### Step 2: Dependency Analysis

#### Package Managers Detection
```bash
# Detect package managers
managers=()
[ -f "package.json" ] && managers+=("npm")
[ -f "yarn.lock" ] && managers+=("yarn")
[ -f "pnpm-lock.yaml" ] && managers+=("pnpm")
[ -f "requirements.txt" ] && managers+=("pip")
[ -f "Pipfile" ] && managers+=("pipenv")
[ -f "poetry.lock" ] && managers+=("poetry")
[ -f "go.mod" ] && managers+=("go")
[ -f "Cargo.toml" ] && managers+=("cargo")
[ -f "Gemfile" ] && managers+=("bundler")
[ -f "composer.json" ] && managers+=("composer")
```

#### Outdated Package Check

**JavaScript/Node.js**
```bash
# npm
npm outdated --json

# yarn
yarn outdated --json

# pnpm
pnpm outdated --format json
```

**Python**
```bash
# pip
pip list --outdated --format json

# poetry
poetry show --outdated

# pipenv
pipenv update --outdated
```

**Go**
```bash
go list -u -m -json all
```

### Step 3: Security Audit

#### Vulnerability Scanning
```javascript
// npm/yarn security audit
async function securityAudit() {
  const audit = await exec('npm audit --json');
  const report = JSON.parse(audit);
  
  return {
    critical: report.metadata.vulnerabilities.critical,
    high: report.metadata.vulnerabilities.high,
    moderate: report.metadata.vulnerabilities.moderate,
    low: report.metadata.vulnerabilities.low,
    packages: report.vulnerabilities
  };
}
```

#### CVE Database Check
```javascript
// Check against CVE database
async function checkCVE(package, version) {
  const response = await fetch(`https://api.cve.org/check/${package}/${version}`);
  const cves = await response.json();
  
  return cves.map(cve => ({
    id: cve.id,
    severity: cve.severity,
    description: cve.description,
    fixedIn: cve.fixed_versions
  }));
}
```

### Step 4: Compatibility Testing

#### Pre-Update Testing
```bash
# Save current state
cp package-lock.json package-lock.json.backup

# Run current tests as baseline
npm test > test-baseline.txt 2>&1
TEST_BASELINE_EXIT=$?
```

#### Update Simulation
```javascript
// Test updates in isolation
async function testUpdate(package, newVersion) {
  // Create temp directory
  const tempDir = await fs.mkdtemp('/tmp/dep-test-');
  
  // Copy project
  await exec(`cp -r . ${tempDir}`);
  
  // Update package
  await exec(`cd ${tempDir} && npm install ${package}@${newVersion}`);
  
  // Run tests
  const testResult = await exec(`cd ${tempDir} && npm test`).catch(e => e);
  
  // Cleanup
  await fs.rm(tempDir, { recursive: true });
  
  return {
    package,
    version: newVersion,
    compatible: testResult.code === 0,
    errors: testResult.stderr
  };
}
```

### Step 5: Update Execution

#### Selective Updates
```javascript
// Update by category
async function updateByCategory(category) {
  const updates = {
    security: [],
    patch: [],
    minor: [],
    major: []
  };
  
  // Categorize updates
  outdated.forEach(pkg => {
    const diff = semverDiff(pkg.current, pkg.latest);
    if (pkg.vulnerability) {
      updates.security.push(pkg);
    } else {
      updates[diff].push(pkg);
    }
  });
  
  // Apply updates
  for (const pkg of updates[category]) {
    await updatePackage(pkg);
  }
}
```

#### Batch Updates
```bash
# JavaScript
npm update # patch and minor
npm install package@latest # major

# Python
pip install --upgrade -r requirements.txt
poetry update

# Go
go get -u ./... # update all
go get -u=patch ./... # patch only
```

### Step 6: Breaking Change Detection

#### API Changes
```javascript
// Detect breaking changes
function detectBreakingChanges(package, oldVersion, newVersion) {
  const breaking = [];
  
  // Check CHANGELOG
  const changelog = readChangelog(package);
  const breakingSection = extractBreaking(changelog, oldVersion, newVersion);
  
  // Check TypeScript definitions
  if (hasTypeDefinitions(package)) {
    const apiChanges = compareAPIs(oldVersion, newVersion);
    breaking.push(...apiChanges.breaking);
  }
  
  // Check deprecations
  const deprecations = findDeprecations(newVersion);
  
  return {
    breaking,
    deprecations,
    migrations: findMigrationGuide(package, newVersion)
  };
}
```

#### Migration Assistance
```markdown
## Breaking Changes Detected

### Package: express (4.x → 5.x)

#### Removed Methods
- `app.del()` → Use `app.delete()`
- `req.param()` → Use `req.params`, `req.query`, or `req.body`

#### Changed Behavior
- Async route handlers now require explicit error handling

#### Migration Steps
1. Search and replace `app.del(` with `app.delete(`
2. Replace `req.param('name')` with `req.params.name || req.query.name`
3. Wrap async handlers:
   ```javascript
   // Before
   app.get('/', async (req, res) => {
     const data = await getData();
     res.json(data);
   });
   
   // After
   app.get('/', async (req, res, next) => {
     try {
       const data = await getData();
       res.json(data);
     } catch (error) {
       next(error);
     }
   });
   ```
```

### Step 7: Lock File Management

#### Update Lock Files
```bash
# npm
npm install # updates package-lock.json

# yarn
yarn install # updates yarn.lock

# pnpm
pnpm install # updates pnpm-lock.yaml
```

#### Lock File Verification
```javascript
// Verify lock file integrity
async function verifyLockFile() {
  // Check for conflicts
  const lockContent = await fs.readFile('package-lock.json', 'utf8');
  if (lockContent.includes('<<<<<<<')) {
    throw new Error('Lock file has merge conflicts');
  }
  
  // Verify against package.json
  const lock = JSON.parse(lockContent);
  const pkg = JSON.parse(await fs.readFile('package.json', 'utf8'));
  
  // Check all dependencies exist
  for (const [name, version] of Object.entries(pkg.dependencies)) {
    if (!lock.packages[`node_modules/${name}`]) {
      console.warn(`Missing in lock: ${name}`);
    }
  }
}
```

### Step 8: Changelog Generation

```markdown
# Dependency Updates - [Date]

## Security Updates 🔒
- **express**: 4.17.1 → 4.18.2
  - Fixes: CVE-2022-24999 (High severity)
  - Description: ReDoS vulnerability in query parser

## Major Updates ⚠️
- **react**: 17.0.2 → 18.2.0
  - Breaking: New JSX Transform
  - Breaking: Automatic batching
  - Feature: Concurrent features
  - [Migration Guide](https://react.dev/blog/2022/03/08/react-18-upgrade-guide)

## Minor Updates ✨
- **axios**: 0.27.0 → 0.28.0
  - Feature: Automatic object serialization
  - Feature: Form data automatic serialization

## Patch Updates 🐛
- **lodash**: 4.17.20 → 4.17.21
  - Fix: Prototype pollution vulnerability
- **jest**: 29.0.1 → 29.0.3
  - Fix: Memory leak in watch mode

## Development Dependencies 🔧
- **eslint**: 8.0.0 → 8.2.0
- **prettier**: 2.7.0 → 2.8.0
- **typescript**: 4.8.0 → 4.9.0

## Removed Dependencies 🗑️
- **moment**: Replaced with date-fns
- **request**: Replaced with axios

## Statistics
- Total packages: 847
- Updated: 34
- Security fixes: 3
- Major updates: 2
- Minor updates: 12
- Patch updates: 17
```

### Step 9: Rollback Plan

#### Backup Current State
```bash
# Create backup branch
git checkout -b deps-backup-$(date +%Y%m%d)
git add .
git commit -m "Backup before dependency update"

# Backup lock files
cp package-lock.json package-lock.json.backup
cp yarn.lock yarn.lock.backup
```

#### Rollback Procedure
```bash
#!/bin/bash
# rollback-deps.sh

echo "Rolling back dependencies..."

# Restore package.json
git checkout HEAD -- package.json

# Restore lock file
cp package-lock.json.backup package-lock.json

# Clean and reinstall
rm -rf node_modules
npm ci

# Verify
npm test

echo "Rollback complete"
```

### Step 10: Update Report

```markdown
# Dependency Update Report

## Summary
- **Date**: 2024-01-15
- **Strategy**: Security + Patch
- **Packages Updated**: 23/312
- **Breaking Changes**: 0
- **Test Status**: ✅ All passing

## Updates Applied

### Critical Security (3)
| Package | Old | New | CVE |
|---------|-----|-----|-----|
| express | 4.17.1 | 4.18.2 | CVE-2022-24999 |
| minimist | 1.2.5 | 1.2.8 | CVE-2021-44906 |
| json5 | 2.2.0 | 2.2.3 | CVE-2022-46175 |

### Dependencies (15)
| Package | Old | New | Type |
|---------|-----|-----|------|
| react | 17.0.2 | 17.0.3 | patch |
| axios | 0.27.2 | 0.28.0 | minor |
| lodash | 4.17.20 | 4.17.21 | patch |

### Dev Dependencies (5)
| Package | Old | New |
|---------|-----|-----|
| jest | 29.0.0 | 29.0.3 |
| eslint | 8.23.0 | 8.24.0 |

## Testing Results
- Unit Tests: ✅ 156/156 passing
- Integration Tests: ✅ 42/42 passing
- E2E Tests: ✅ 8/8 passing
- Build: ✅ Successful
- Bundle Size: ↓ 2.3KB smaller

## Compatibility Notes
- All updates backward compatible
- No API changes detected
- No deprecation warnings

## Recommendations
1. Monitor for 24 hours
2. Check error logs
3. Plan major updates for next sprint
4. Update documentation

## Next Steps
- [ ] Deploy to staging
- [ ] Monitor metrics
- [ ] Update changelog
- [ ] Notify team
```

## Update Strategies

### Conservative
```json
{
  "strategy": "conservative",
  "rules": {
    "security": "always",
    "patch": "auto",
    "minor": "manual",
    "major": "never"
  }
}
```

### Balanced
```json
{
  "strategy": "balanced",
  "rules": {
    "security": "always",
    "patch": "auto",
    "minor": "auto",
    "major": "manual"
  }
}
```

### Aggressive
```json
{
  "strategy": "aggressive",
  "rules": {
    "security": "always",
    "patch": "auto",
    "minor": "auto",
    "major": "quarterly"
  }
}
```

## Configuration

### .claude/deps-config.json
```json
{
  "strategy": "balanced",
  "autoUpdate": {
    "enabled": true,
    "schedule": "weekly",
    "branches": ["deps-update"]
  },
  "testing": {
    "required": true,
    "coverage": 80,
    "performance": true
  },
  "security": {
    "autoFix": true,
    "severity": "moderate"
  },
  "ignore": [
    "legacy-package",
    "@internal/*"
  ],
  "groups": {
    "react": ["react", "react-dom", "@types/react"],
    "testing": ["jest", "@testing-library/*"]
  }
}
```

## Best Practices

1. **Test Thoroughly**
   - Run full test suite
   - Test in staging
   - Check performance

2. **Update Regularly**
   - Weekly security updates
   - Monthly minor updates
   - Quarterly major updates

3. **Document Changes**
   - Keep changelog updated
   - Note breaking changes
   - Provide migration guides

## Notes
- Supports all major package managers
- Tests compatibility automatically
- Handles breaking changes
- Generates comprehensive reports
- Never updates without testing