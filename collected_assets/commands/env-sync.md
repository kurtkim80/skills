# Environment Manager

Synchronizes environment variables across environments, validates configurations, manages secrets, and sets up development environments.

## Purpose
- Sync .env files across environments
- Validate environment variables
- Generate environment documentation
- Secret rotation management
- Docker/container environment setup

## Workflow

### Phase 1: Environment Selection
1. **STOP** → "Select environment operation:"
   ```
   1. Sync environments - Copy variables between environments
   2. Validate config - Check for missing/invalid variables
   3. Generate template - Create .env.example
   4. Rotate secrets - Update sensitive values
   5. Setup new environment - Initialize from template
   6. Compare environments - Diff between environments
   
   Choose operation (1-6):
   ```

2. **Environment Options**
   - STOP → "Include secret values? (y/n):"
   - STOP → "Validate against schema? (y/n):"
   - STOP → "Backup current config? (y/n):"

### Phase 2: Environment Discovery
1. **Find Environment Files**
   ```bash
   # Locate all env files
   find . -name ".env*" -type f | grep -v node_modules
   
   # Common patterns
   .env
   .env.local
   .env.development
   .env.staging
   .env.production
   .env.test
   ```

2. **Parse Environment Variables**
   ```javascript
   const dotenv = require('dotenv');
   const fs = require('fs');
   
   function parseEnvFile(filepath) {
     const content = fs.readFileSync(filepath, 'utf8');
     return dotenv.parse(content);
   }
   ```

### Phase 3: Environment Validation

#### Schema Definition
```javascript
// env.schema.json
{
  "required": [
    "NODE_ENV",
    "PORT",
    "DATABASE_URL",
    "JWT_SECRET"
  ],
  "properties": {
    "NODE_ENV": {
      "type": "string",
      "enum": ["development", "staging", "production"]
    },
    "PORT": {
      "type": "number",
      "minimum": 1000,
      "maximum": 65535
    },
    "DATABASE_URL": {
      "type": "string",
      "pattern": "^(postgres|mysql|mongodb)://.*"
    },
    "JWT_SECRET": {
      "type": "string",
      "minLength": 32
    }
  }
}
```

#### Validation Checks
```javascript
function validateEnvironment(env, schema) {
  const errors = [];
  
  // Check required variables
  schema.required.forEach(key => {
    if (!env[key]) {
      errors.push(`Missing required: ${key}`);
    }
  });
  
  // Validate types and patterns
  Object.keys(env).forEach(key => {
    const rule = schema.properties[key];
    if (rule) {
      if (rule.type === 'number' && isNaN(env[key])) {
        errors.push(`Invalid type for ${key}: expected number`);
      }
      if (rule.pattern && !new RegExp(rule.pattern).test(env[key])) {
        errors.push(`Invalid format for ${key}`);
      }
    }
  });
  
  return errors;
}
```

### Phase 4: Environment Synchronization

#### Sync Strategy
```javascript
// Sync from source to target
function syncEnvironments(source, target, options = {}) {
  const sourceVars = parseEnvFile(source);
  const targetVars = parseEnvFile(target);
  
  const updates = {};
  const additions = {};
  const removals = {};
  
  // Find additions and updates
  Object.keys(sourceVars).forEach(key => {
    if (!targetVars[key]) {
      additions[key] = sourceVars[key];
    } else if (targetVars[key] !== sourceVars[key]) {
      updates[key] = {
        old: targetVars[key],
        new: sourceVars[key]
      };
    }
  });
  
  // Find removals
  Object.keys(targetVars).forEach(key => {
    if (!sourceVars[key]) {
      removals[key] = targetVars[key];
    }
  });
  
  return { additions, updates, removals };
}
```

#### Selective Sync
```yaml
sync_rules:
  include:
    - API_*
    - DATABASE_*
    - REDIS_*
  exclude:
    - *_SECRET
    - *_KEY
    - *_TOKEN
  transform:
    DATABASE_URL: "postgres://localhost/dev_db"
```

### Phase 5: Secret Management

#### Secret Detection
```javascript
const secretPatterns = [
  /.*_SECRET$/,
  /.*_KEY$/,
  /.*_TOKEN$/,
  /.*_PASSWORD$/,
  /.*_PRIVATE$/
];

function isSecret(key) {
  return secretPatterns.some(pattern => pattern.test(key));
}
```

#### Secret Rotation
```javascript
async function rotateSecrets(env) {
  const updates = {};
  
  // Generate new JWT secret
  if (env.JWT_SECRET) {
    updates.JWT_SECRET = generateSecureToken(64);
  }
  
  // Rotate API keys
  if (env.API_KEY) {
    updates.API_KEY = await rotateAPIKey(env.API_KEY);
  }
  
  // Update database password
  if (env.DB_PASSWORD) {
    updates.DB_PASSWORD = generatePassword();
    await updateDatabasePassword(updates.DB_PASSWORD);
  }
  
  return updates;
}

function generateSecureToken(length) {
  return require('crypto')
    .randomBytes(length)
    .toString('base64')
    .replace(/[^a-zA-Z0-9]/g, '')
    .substr(0, length);
}
```

### Phase 6: Template Generation

#### Create .env.example
```javascript
function generateTemplate(envFile) {
  const vars = parseEnvFile(envFile);
  const template = [];
  
  Object.keys(vars).forEach(key => {
    if (isSecret(key)) {
      template.push(`${key}=your_${key.toLowerCase()}_here`);
    } else if (key.includes('URL')) {
      template.push(`${key}=http://localhost:3000`);
    } else if (key.includes('PORT')) {
      template.push(`${key}=3000`);
    } else {
      template.push(`${key}=${vars[key]}`);
    }
  });
  
  return template.join('\n');
}
```

#### Documentation Generation
```markdown
# Environment Variables

## Required Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| NODE_ENV | Application environment | production | ✅ |
| PORT | Server port | 3000 | ✅ |
| DATABASE_URL | Database connection string | postgres://... | ✅ |

## Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| LOG_LEVEL | Logging verbosity | info |
| CACHE_TTL | Cache timeout (seconds) | 3600 |

## Secret Variables

| Variable | Description | Rotation |
|----------|-------------|----------|
| JWT_SECRET | JWT signing secret | Monthly |
| API_KEY | External API key | On demand |

## Environment-Specific Values

### Development
```
NODE_ENV=development
DATABASE_URL=postgres://localhost/dev_db
DEBUG=true
```

### Production
```
NODE_ENV=production
DATABASE_URL=postgres://prod-server/prod_db
DEBUG=false
```
```

### Phase 7: Environment Comparison

```markdown
# Environment Comparison Report

## Development vs Production

### Missing in Production
- DEBUG
- VERBOSE_LOGGING
- TEST_MODE

### Different Values
| Variable | Development | Production |
|----------|-------------|------------|
| NODE_ENV | development | production |
| DATABASE_URL | localhost | prod-server |
| LOG_LEVEL | debug | error |
| CACHE_TTL | 60 | 3600 |

### Security Issues
⚠️ **Warning**: Production using development API key
⚠️ **Warning**: DEBUG=true in production
```

### Phase 8: Container Environment

#### Docker Environment
```dockerfile
# Dockerfile with env support
FROM node:18-alpine

# Build args for secrets
ARG API_KEY
ARG DATABASE_URL

# Runtime environment
ENV NODE_ENV=production \
    PORT=3000

# Use secrets during build only
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) \
    npm run build
```

#### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    env_file:
      - .env
      - .env.local
    environment:
      - NODE_ENV=production
      - PORT=${PORT:-3000}
    secrets:
      - api_key
      - db_password

secrets:
  api_key:
    file: ./secrets/api_key.txt
  db_password:
    file: ./secrets/db_password.txt
```

### Phase 9: Backup and Recovery

#### Backup Current Environment
```bash
# Create timestamped backup
timestamp=$(date +%Y%m%d_%H%M%S)
cp .env .env.backup.$timestamp

# Encrypt sensitive backup
openssl enc -aes-256-cbc -salt -in .env -out .env.enc
```

#### Recovery Procedure
```bash
# List backups
ls -la .env.backup.*

# Restore from backup
cp .env.backup.20240115_103000 .env

# Decrypt backup
openssl enc -d -aes-256-cbc -in .env.enc -out .env
```

### Phase 10: Reporting

```markdown
# Environment Sync Report

## Summary
- **Operation**: Sync development → staging
- **Variables Synced**: 24
- **Secrets Excluded**: 5
- **Validation**: ✅ Passed

## Changes Applied

### Added (3)
- FEATURE_FLAG_NEW_UI=true
- REDIS_URL=redis://localhost:6379
- ANALYTICS_ID=UA-123456

### Updated (5)
| Variable | Old Value | New Value |
|----------|-----------|-----------|
| API_VERSION | v1 | v2 |
| CACHE_TTL | 300 | 600 |
| MAX_WORKERS | 2 | 4 |

### Removed (1)
- DEPRECATED_FEATURE=true

## Validation Results
✅ All required variables present
✅ Types and formats valid
✅ No hardcoded secrets detected
✅ Schema compliance verified

## Security Check
✅ No secrets in plain text
✅ Sensitive values properly masked
✅ Rotation schedule up to date

## Next Steps
1. Test application with new config
2. Update documentation
3. Notify team of changes
```

## Integration

### With `/task-init`
- Load environment at task start
- Verify required variables

### With `/deploy`
- Validate environment before deploy
- Sync configs to target environment

### With `/rollback`
- Restore previous environment
- Revert configuration changes

## Configuration

### .claude/env-config.json
```json
{
  "environments": [
    "development",
    "staging",
    "production"
  ],
  "schema": "env.schema.json",
  "secrets": {
    "provider": "aws-secrets-manager",
    "rotation": {
      "enabled": true,
      "interval": "30d"
    }
  },
  "sync": {
    "excludePatterns": [
      "*_SECRET",
      "*_PRIVATE_KEY"
    ],
    "includePatterns": [
      "API_*",
      "FEATURE_*"
    ]
  },
  "backup": {
    "enabled": true,
    "retention": "30d",
    "encryption": true
  }
}
```

## Best Practices

1. **Security First**
   - Never commit .env files
   - Use secret managers
   - Rotate credentials regularly
   - Mask sensitive values

2. **Validation**
   - Define schemas
   - Validate before use
   - Type check values
   - Test configurations

3. **Documentation**
   - Document all variables
   - Explain purpose and format
   - Provide examples
   - Update regularly

## Notes
- Supports multiple environment formats
- Validates against schemas
- Manages secret rotation
- Generates documentation
- Never exposes secrets in logs