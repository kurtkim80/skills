# Update Azure DevOps Work Item

Updates Azure DevOps work item with progress, comments, and status changes based on local development work.

## Purpose
- Update work item status based on development progress
- Add detailed comments documenting changes
- Link commits and branches to work item
- Maintain work item history and audit trail

## Required MCP Setup
This command requires Azure DevOps MCP server to be installed and configured.

If not installed, follow: https://github.com/microsoft/azure-devops-mcp-server

## Execution Steps

### Step 1: Validate Input

Check if work item number was provided as argument.

If no work item number provided:
Output: "Usage: /update-azure-task [work_item_number]

Example: /update-azure-task 12345"
Exit command.

### Step 2: Fetch Current Work Item State

Use mcp__azuredevops__get_work_item tool (if available):
- work_item_id: [provided work item number]

If tool not available:
Output: "Azure DevOps MCP server not configured.

Install and configure following: /fetch-azure-task documentation"
Exit command.

If work item not found:
Output: "Work item [number] not found or access denied."
Exit command.

Extract current state:
- Current status
- Current assigned to
- Existing description and comments

### Step 3: Analyze Local Changes

Use Bash tool to get current branch:
- Command: `git branch --show-current`
- Description: "Get current branch name"

If not in a git repository:
Output: "Not in a git repository. Work item updates require git context."
Exit command.

Use Bash tool to identify base branch:
- Command: `for base in main master develop development staging; do git rev-parse --verify $base >/dev/null 2>&1 && echo $base && break; done`
- Description: "Find base branch"

Use Bash tool to get recent commits for this branch:
- Command: `git log --oneline [base_branch]..HEAD`
- Description: "Get commits on current branch"

Use Bash tool to get detailed commit info:
- Command: `git log --format="%H|%s|%b|%ad" --date=short [base_branch]..HEAD`
- Description: "Get detailed commit information"

Use Bash tool to get change statistics:
- Command: `git diff --stat [base_branch]..HEAD`
- Description: "Get file change statistics"

### Step 4: Check for Task History

Use Bash tool to find saved work item context:
- Command: `ls -t .claude/azure-tasks/work-item-[ID].md 2>/dev/null`
- Description: "Check for saved work item context"

If context file exists, use Read tool to read it.

Use Bash tool to find related task history:
- Command: `ls -t .claude/task-history/*.md 2>/dev/null | head -1`
- Description: "Find most recent task history"

If task history exists, use Read tool to read it.

### Step 5: Generate Update Summary

Compile update information:

1. **Work Summary**: Brief description of work completed based on:
   - Commit messages
   - Files changed
   - Task history if available

2. **Technical Changes**:
   - Number of commits
   - Files modified/added/deleted
   - Key functional changes

3. **Commit References**:
   - List commit hashes and messages
   - Link to branch name

Format update content:
```
## Development Update - [Current Date]

### Work Completed
[Summary of work done]

### Changes Made
- [N] commits pushed
- [N] files modified
- [N] files added
- [N] files deleted

### Commits
[List of commit hashes and messages]

### Branch
Branch: [branch_name]

### Files Changed
[Summary of file changes]

### Technical Details
[Additional technical context from commits]
```

### Step 6: Present Update Options

Output: "## Work Item Update for #[ID]

**Current State**: [current status]
**Branch**: [branch name]
**Commits**: [N] commits ready to link

### Suggested Update:
[Generated update summary]

---

What would you like to update?
1. Add comment with development summary (recommended)
2. Update status to 'Active' (if not already)
3. Update status to 'Resolved' (if work complete)
4. Update status to 'Closed' (if fully done)
5. Add comment + update status
6. Custom update

Choose option (1-6):"

WAIT for user's choice.

### Step 7: Execute Update

Based on user's choice:

**If option 1 (Add comment only):**

Use mcp__azuredevops__add_work_item_comment tool:
- work_item_id: [ID]
- comment: [Generated update summary]

**If option 2 (Update to Active):**

Use mcp__azuredevops__update_work_item tool:
- work_item_id: [ID]
- state: "Active"

**If option 3 (Update to Resolved):**

Use mcp__azuredevops__update_work_item tool:
- work_item_id: [ID]
- state: "Resolved"

Also add comment with resolution summary.

**If option 4 (Update to Closed):**

Output: "Are you sure you want to close work item #[ID]? This should only be done when work is fully complete and verified. (yes/no):"
WAIT for confirmation.

If user confirms:
Use mcp__azuredevops__update_work_item tool:
- work_item_id: [ID]
- state: "Closed"

Also add comment with closure summary.

If user says no, return to options menu.

**If option 5 (Comment + Status):**

Output: "Select new status:
1. Active
2. Resolved
3. Closed

Choose status (1-3):"
WAIT for status choice.

First add comment, then update status based on choice.

**If option 6 (Custom):**

Output: "Enter custom comment (or 'skip' to skip comment):"
WAIT for comment input.

Output: "Enter new status (Active/Resolved/Closed) or 'skip' to keep current:"
WAIT for status input.

Apply custom comment and/or status as provided.

### Step 8: Verify Update

Use mcp__azuredevops__get_work_item tool to fetch updated work item:
- work_item_id: [ID]

Display confirmation:
Output: "Work item #[ID] updated successfully!

**New Status**: [updated status]
**Last Updated**: [timestamp]

View in Azure DevOps: [work_item_url]"

### Step 9: Save Update Record

Use Bash tool to append update to local history:
- Command: `echo "## Update $(date '+%Y-%m-%d %H:%M:%S')\n[update summary]\n" >> .claude/azure-tasks/work-item-[ID].md`
- Description: "Record update in local history"

Output: "Update recorded locally in: .claude/azure-tasks/work-item-[ID].md"

## Advanced Features

### Automatic Work Item Detection

If work item ID not provided, attempt to detect from:
1. Branch name (e.g., `feature/AB#12345-description`)
2. Recent commit messages (e.g., `AB#12345: commit message`)

Use Bash tool to check branch name:
- Command: `git branch --show-current | grep -oE 'AB#[0-9]+'`
- Description: "Extract work item from branch name"

If found, use detected ID and confirm with user.

### Commit Linking

Automatically format commits as Azure DevOps links in comments:
- `[commit_hash]` → Link to commit in Azure Repos
- Include branch reference

### Smart Status Detection

Suggest status based on:
- Commit messages containing "fix", "resolve", "complete"
- Presence of tests
- PR/MR creation
- Tag keywords

## Error Handling

### Update Conflicts
If work item was updated by someone else:
- Display conflict warning
- Show what changed
- Ask user to confirm update

### Permission Issues
If PAT lacks update permissions:
- Display clear permission error
- List required permissions:
  - Work Items (Read, Write)
- Exit gracefully

### Invalid State Transitions
If requested state change is invalid:
- Display allowed transitions
- Ask user to choose valid state

## Integration with Workflow

### Command Flow
```
/fetch-azure-task [ID] → development → /commit → /update-azure-task [ID]
```

### Cross-Integration
Works with:
- `/commit` - Uses commit messages for update context
- `/mr-draft` - Can reference work item in MR
- `/task-init` - Can initialize from work item

## Best Practices

1. **Update Frequently**: Keep work item in sync with development
2. **Meaningful Comments**: Provide technical context, not just "updated"
3. **Status Accuracy**: Only mark resolved when truly complete
4. **Link Everything**: Include branch, commits, PRs in comments
5. **Verify Updates**: Check Azure DevOps after update

## Notes
- Updates are immediately visible in Azure DevOps
- All updates are audited in work item history
- Local history maintained in `.claude/azure-tasks/`
- Never close work items until fully verified
