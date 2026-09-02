# Sync Configuration to GitHub

Sync all Claude Code configuration files and skills to the GitHub repository.

## Purpose
- Sync global CLAUDE.md instructions to version control
- Sync settings.json and editor configuration
- Sync all custom slash commands
- Sync all specialized subagents
- Sync all global skills from ~/.claude/skills/
- Never mention AI/automation in commit messages

## Execution Steps

### Step 1: Verify Repository Location

Use Bash tool to verify repository exists:
- Command: `ls -la ~/github/claude-config`
- Description: "Verify claude-config repository location"

If directory doesn't exist:
Output: "Error: Repository not found at ~/github/claude-config. Please clone the repository first."
Exit command.

### Step 2: Copy Configuration Files

Use Bash tool to copy global instructions:
- Command: `cp ~/.claude/CLAUDE.md ~/github/claude-config/`
- Description: "Copy global CLAUDE.md"

Use Bash tool to copy settings:
- Command: `cp ~/.claude/settings.json ~/github/claude-config/`
- Description: "Copy settings.json"

Use Bash tool to copy editor configuration:
- Command: `cp ~/.claude.json ~/github/claude-config/ 2>/dev/null || echo "No .claude.json found"`
- Description: "Copy editor configuration if exists"

Use Bash tool to copy all slash commands:
- Command: `cp -r ~/.claude/commands ~/github/claude-config/`
- Description: "Copy all slash commands"

Use Bash tool to copy all subagents:
- Command: `cp -r ~/.claude/agents ~/github/claude-config/ 2>/dev/null || echo "No agents directory found"`
- Description: "Copy all subagents if directory exists"

### Step 3: Copy Global Skills

Use Bash tool to check if skills directory exists:
- Command: `test -d ~/.claude/skills && echo "exists" || echo "not-found"`
- Description: "Check if global skills directory exists"

If result is "exists":

Use Bash tool to copy all global skills:
- Command: `cp -r ~/.claude/skills ~/github/claude-config/`
- Description: "Copy all global skills"

Output: "✓ Copied global skills from ~/.claude/skills/"

If result is "not-found":
Output: "ℹ No global skills directory found, skipping skills sync"

### Step 4: Check Git Status

Use Bash tool to check git status:
- Command: `cd ~/github/claude-config && git status --porcelain`
- Description: "Check git status for changes"

Store output as `GIT_STATUS`.

If `GIT_STATUS` is empty:
Output: "No changes to commit. Configuration is already up to date."
Exit command.

Output the git status to show what changed:
Use Bash tool:
- Command: `cd ~/github/claude-config && git status`
- Description: "Show detailed git status"

### Step 5: Stage All Changes

Use Bash tool to stage all changes:
- Command: `cd ~/github/claude-config && git add .`
- Description: "Stage all configuration changes"

### Step 6: Generate Commit Message

Analyze `GIT_STATUS` to determine what changed:

Check for patterns:
- If "commands/" files changed: Note "slash commands updated"
- If "agents/" files changed: Note "subagents updated"
- If "skills/" files changed: Note "global skills updated"
- If "CLAUDE.md" changed: Note "global instructions updated"
- If "settings.json" changed: Note "settings updated"

Construct commit message based on changes found.

Examples:
- "Update slash commands and global instructions"
- "Add new global skills and update commands"
- "Update configuration settings and subagents"
- "Update configuration files - [current date]"

IMPORTANT: NEVER mention "Claude", "AI", "Generated", or "Co-Authored" in commit messages.

### Step 7: Commit Changes

Use Bash tool to create commit:
- Command: `cd ~/github/claude-config && git commit -m "[generated commit message]"`
- Description: "Commit configuration changes"

Store commit hash from output.

### Step 8: Push to GitHub

Use Bash tool to push changes:
- Command: `cd ~/github/claude-config && git push`
- Description: "Push changes to GitHub"

### Step 9: Verify Success

Use Bash tool to verify last commit:
- Command: `cd ~/github/claude-config && git log --oneline -1`
- Description: "Show last commit"

### Step 10: Provide Summary

Count files changed:
Use Bash tool:
- Command: `cd ~/github/claude-config && git diff --stat HEAD~1 | tail -1`
- Description: "Get diff statistics"

Output summary:

```
## Sync Complete

**Files synced**:
- Global instructions (CLAUDE.md)
- Settings (settings.json)
- Slash commands (commands/)
[- Subagents (agents/) - if exists]
[- Global skills (skills/) - if exists]
[- Editor config (.claude.json) - if exists]

**Changes**:
[Show git diff statistics]

**Commit**: [commit hash]
**Pushed to**: github.com/nagawa/claude-config

✓ Configuration successfully synced to GitHub!
```

## Error Handling

### Repository Not Found
- Provide clear error message
- Suggest cloning the repository
- Exit gracefully

### No Changes Detected
- Inform user configuration is up to date
- Exit without committing

### Git Push Failure
- Show error message
- Suggest checking remote connection
- Offer to retry

### File Copy Errors
- Log which files failed to copy
- Continue with other files
- Report failures in summary

## Notes
- Never mentions AI/automation in commits
- Syncs both configuration and skills
- Handles missing directories gracefully
- Provides clear feedback on what changed
- Verifies successful push to remote
