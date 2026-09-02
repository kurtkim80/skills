# Smart Git Commit Command

Intelligent git commit system that stages only task-related changes and generates meaningful commit messages without AI tool references.

## Purpose
- Stage only files related to the current task
- Generate professional commit messages
- Exclude any mention of AI/agent tools
- Maintain clean git history

## Execution Steps

### Step 1: Check for Task Context

Use Bash tool to find most recent task file:
- Command: `ls -t .claude/task-history/*.md 2>/dev/null | head -1`
- Description: "Find most recent task history file"

If no task file exists, output: "No task history found. Proceeding with manual file selection."

If task file exists:
- Use Read tool to read the task file
- Extract: task title, objective, files mentioned, success criteria

### Step 2: Analyze Git Status

Use Bash tool to check git status:
- Command: `git status --porcelain`
- Description: "Check git repository status"

Parse output to categorize:
- Modified files (M prefix)
- Added files (A or ?? prefix)
- Deleted files (D prefix)
- Renamed files (R prefix)

### Step 3: Identify Task-Related Files

Based on task context (if available), identify files that:
- Match file patterns from task description
- Are in directories mentioned in task
- Match technology/framework patterns from task

If no task context, consider all changed files as candidates.

### Step 4: Present Staging Plan

Output a categorized list of changes:
```markdown
## Task: [Task Title or "Manual Commit"]

### Will stage:
- file1.js (modified) - implements feature X
- file2.test.js (added) - tests for feature X

### Possibly related (confirm):
- config.json (modified) - may contain task settings

### Will skip:
- .env (modified) - local environment
- debug.log (added) - temporary file
```

Then output: "Review staging plan. Adjust? (Reply with files to add/remove, or 'ok' to proceed):"

WAIT for user response.

### Step 5: Stage Files

Use Bash tool to stage selected files:
- Command: `git add [space-separated file paths]`
- Description: "Stage task-related files"

### Step 6: Generate Commit Message

Based on staged changes, generate a conventional commit message:

Format:
```
[type]: [concise description]

[optional body with details]
```

Types: feat, fix, docs, style, refactor, perf, test, chore

IMPORTANT: Never mention AI, agents, Claude, automation, or AI-assistance in the message.

### Step 7: Present Commit Message

Output:
```markdown
## Proposed Commit Message:
```
[generated message]
```
```

Then output: "Use this commit message? (Reply 'yes' to commit, 'no' to edit, 'abort' to cancel):"

WAIT for user response.

If user says 'no', ask: "Enter your commit message:"
WAIT for user's message.

If user says 'abort':
- Use Bash tool to unstage: `git reset`
- Exit command

### Step 8: Create Commit

If user approves:

1. Use Bash tool to create commit:
   - Command: `git commit -m "[message]"`
   - Description: "Create git commit"

2. Use Bash tool to show result:
   - Command: `git log --oneline -1 && git status`
   - Description: "Show commit result and status"

3. If task history file exists, append commit info using Edit tool

### Step 9: Create Merge Request (Optional)

Output: "Commit successful! Create a Merge Request / Pull Request? (y/n):"
WAIT for user's response.

If user says yes:

Output: "Starting /mr-draft command..."

Execute the `/mr-draft` slash command.

If user says no, command complete.

## Smart Detection Rules

### File Pattern Matching
Automatically detect task-related files based on:

1. **Direct Mentions**
   - Files explicitly mentioned in task description
   - Files in paths specified in task

2. **Technology Patterns**
   - React task → *.jsx, *.tsx, components/
   - API task → controllers/, routes/, *.api.*
   - Database task → migrations/, models/, *.sql
   - Testing task → *.test.*, *.spec.*, __tests__/
   - Documentation task → *.md, docs/

3. **Temporal Correlation**
   - Files modified after task start time
   - Files in same directory as other task files

4. **Dependency Chain**
   - Files that import/require task files
   - Files imported by task files
   - Config files affecting task files

### Exclusion Rules
Always exclude:
- `.env`, `.env.local`, `.env.*`
- `*.log`, `*.tmp`, `*.cache`
- `.DS_Store`, `Thumbs.db`
- `node_modules/`, `vendor/`, `target/`
- Build outputs unless specifically part of task
- Personal IDE settings (`.vscode/settings.json`, `.idea/`)

## Error Handling

### No Git Repository
- Check if in git repository
- Suggest `git init` if appropriate
- Exit gracefully

### No Changes to Commit
- Show current status
- Suggest checking task completion
- Exit gracefully

### Merge Conflicts
- Detect merge conflict markers
- Warn user to resolve conflicts first
- Provide guidance on conflict resolution

### Task File Issues
- If no task history: Offer to proceed with manual file selection
- If corrupt task file: Use fallback to git status only
- If multiple active tasks: Ask which task to commit for

## Command Options

### Basic Usage
```
/commit
```
Runs full smart commit workflow

### Manual Override
If no task context or user wants manual control:
1. STOP → "No task context. Enter files to stage (space-separated) or 'all' for git add -A:"
2. STOP → "Enter commit message:"
3. Proceed with standard commit

## Integration with /task-init

### Task Continuity
- Reads task context from `.claude/task-history/`
- Uses task success criteria to validate changes
- Links commits back to original task

### Workflow Connection
```
/task-init → [work on task] → /commit → [repeat as needed]
```

## Best Practices

1. **One Task, One Commit**
   - Keep commits focused on single task
   - Use multiple commits for complex tasks
   - Each commit should be independently valid

2. **Message Quality**
   - First line: 50 chars or less
   - Use imperative mood ("add" not "added")
   - Explain what and why, not how

3. **Clean History**
   - No WIP commits
   - No debugging artifacts
   - No commented code

## Notes
- Commit messages never mention AI assistance
- Task history helps maintain commit context
- Smart staging prevents accidental commits
- Works with any git workflow (feature branches, trunk-based, etc.)