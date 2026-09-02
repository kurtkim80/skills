# Close Azure DevOps Work Item

Closes Azure DevOps work item after verifying completion, running final checks, and documenting resolution.

## Purpose
- Safely close completed work items
- Verify all acceptance criteria met
- Document final resolution and verification
- Run quality checks before closure
- Maintain completion audit trail

## Required MCP Setup
This command requires Azure DevOps MCP server to be installed and configured.

If not installed, follow: https://github.com/microsoft/azure-devops-mcp-server

## Execution Steps

### Step 1: Validate Input

Check if work item number was provided as argument.

If no work item number provided:
Output: "Usage: /close-azure-task [work_item_number]

Example: /close-azure-task 12345"
Exit command.

### Step 2: Fetch Work Item Details

Use mcp__azuredevops__get_work_item tool (if available):
- work_item_id: [provided work item number]

If tool not available:
Output: "Azure DevOps MCP server not configured.

Install and configure following: /fetch-azure-task documentation"
Exit command.

If work item not found:
Output: "Work item [number] not found or access denied."
Exit command.

Extract work item information:
- Current state
- Work item type
- Title and description
- Acceptance criteria
- Related work items
- Assigned to

### Step 3: Verify Work Item State

Check current state of work item.

If state is already "Closed":
Output: "Work item #[ID] is already closed.

**Closed Date**: [closed date]
**Closed By**: [closed by]

No action needed."
Exit command.

If state is "New" or "Active":
Output: "Warning: Work item #[ID] is currently '[state]', not 'Resolved'.

Typically work items should be:
1. Developed (Active)
2. Code reviewed (Resolved)
3. Tested and verified
4. Then closed

Do you want to proceed with closure anyway? (yes/no):"
WAIT for user confirmation.

If user says no:
Output: "Closure cancelled. Consider using /update-azure-task to set status to 'Resolved' first."
Exit command.

### Step 4: Run Pre-Closure Checks

Use Bash tool to check git status:
- Command: `git status --porcelain`
- Description: "Check for uncommitted changes"

If uncommitted changes exist:
Output: "Warning: You have uncommitted changes.

Uncommitted files:
[list of uncommitted files]

Commit these changes before closing work item? (yes/no/ignore):"
WAIT for user response.

If user chooses 'yes', exit command and suggest running `/commit` first.
If user chooses 'ignore', continue with warning.

Use Bash tool to check current branch:
- Command: `git branch --show-current`
- Description: "Get current branch name"

Use Bash tool to check if branch has been pushed:
- Command: `git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "not-pushed"`
- Description: "Check for unpushed commits"

If branch has unpushed commits:
Output: "Warning: Current branch has unpushed commits.

Push commits before closing work item? (yes/no/ignore):"
WAIT for user response.

If user chooses 'yes':
Output: "Please run: git push

Then re-run this command."
Exit command.

### Step 5: Load Work Context

Use Bash tool to check for saved work item context:
- Command: `ls .claude/azure-tasks/work-item-[ID].md 2>/dev/null`
- Description: "Check for work item context"

If context file exists, use Read tool to read it.

Check if acceptance criteria was defined in work item.

If acceptance criteria exists:
Output: "## Acceptance Criteria Verification

[Display acceptance criteria]

---

Have all acceptance criteria been met? (yes/no):"
WAIT for user confirmation.

If user says no:
Output: "Work item closure cancelled.

Remaining acceptance criteria should be completed before closing.

Options:
1. Complete remaining criteria
2. Update work item to remove/modify criteria
3. Add comment explaining partial completion

Closure aborted."
Exit command.

### Step 6: Run Quality Checks

Output: "Running quality checks before closure..."

Use Bash tool to run tests (if test command exists):
- Command: `make test 2>/dev/null || npm test 2>/dev/null || pytest 2>/dev/null || go test ./... 2>/dev/null || echo "no-test-found"`
- Description: "Run project tests"

If tests fail:
Output: "Warning: Tests are failing!

Failing tests detected. Work items should only be closed when all tests pass.

Proceed with closure anyway? (yes/no):"
WAIT for user confirmation.

If user says no:
Output: "Closure cancelled. Fix failing tests first."
Exit command.

Use Bash tool to run linter (if available):
- Command: `make lint 2>/dev/null || npm run lint 2>/dev/null || rye run lint 2>/dev/null || echo "no-lint-found"`
- Description: "Run code linter"

If linter shows errors:
Output: "Warning: Linter found issues.

Consider fixing linting issues before closing work item."

### Step 7: Analyze Completed Work

Use Bash tool to find base branch:
- Command: `for base in main master develop development staging; do git rev-parse --verify $base >/dev/null 2>&1 && echo $base && break; done`
- Description: "Find base branch"

Use Bash tool to get all commits for this work:
- Command: `git log --oneline [base_branch]..HEAD`
- Description: "Get commits for work item"

Use Bash tool to get file change summary:
- Command: `git diff --stat [base_branch]..HEAD`
- Description: "Get file changes summary"

Generate completion summary:
```
## Work Item Closure Summary

### Completed Work
[Brief description of work completed]

### Commits
[List of commit hashes and messages]

### Changes
- [N] files modified
- [N] files added
- [N] files deleted
- [Total lines changed]

### Quality Checks
- Tests: [Passed/Failed/Not Run]
- Linting: [Passed/Issues Found/Not Run]
- Code Review: [Indicate if reviewed]

### Verification
- All acceptance criteria met: [Yes/Partial/No]
- Branch merged to: [branch name or "Not merged"]

### Resolution Notes
[Additional notes about completion]
```

### Step 8: Confirm Closure

Output: "## Ready to Close Work Item #[ID]

**Title**: [work item title]
**Type**: [work item type]
**Current State**: [current state]

### Closure Summary:
[Display generated closure summary]

---

This action will:
1. Set work item state to 'Closed'
2. Add completion comment to work item
3. Record closure timestamp
4. Update work item history

Close work item #[ID]? (yes/no):"

WAIT for final user confirmation.

If user says no:
Output: "Closure cancelled."
Exit command.

### Step 9: Close Work Item

Use mcp__azuredevops__update_work_item tool:
- work_item_id: [ID]
- state: "Closed"

Use mcp__azuredevops__add_work_item_comment tool:
- work_item_id: [ID]
- comment: [Generated closure summary with completion details]

### Step 10: Verify Closure

Use mcp__azuredevops__get_work_item tool to fetch updated work item:
- work_item_id: [ID]

Confirm work item is now closed.

Output: "Work item #[ID] closed successfully!

**Status**: Closed
**Closed Date**: [closure timestamp]
**Closed By**: [user]

View in Azure DevOps: [work_item_url]"

### Step 11: Clean Up Local Context

Output: "Archive local work item context? (yes/no):"
WAIT for user response.

If user says yes:

Use Bash tool to create archive directory:
- Command: `mkdir -p .claude/azure-tasks/archived`
- Description: "Create archive directory"

Use Bash tool to move work item file to archive:
- Command: `mv .claude/azure-tasks/work-item-[ID].md .claude/azure-tasks/archived/work-item-[ID]-$(date +%Y%m%d).md`
- Description: "Archive work item context"

Output: "Work item context archived to: .claude/azure-tasks/archived/"

If user says no:
Output: "Work item context kept in: .claude/azure-tasks/work-item-[ID].md"

### Step 12: Branch Cleanup Suggestion

If on feature branch related to work item:

Output: "You're currently on branch: [branch_name]

This work item is now closed. Would you like to:
1. Switch to main/master branch
2. Delete this feature branch (if merged)
3. Keep current branch

Choose option (1-3):"

WAIT for user choice.

If option 1:
Use Bash tool: `git checkout [main_branch]`, description: "Switch to main branch"

If option 2:
Output: "Confirm deletion of branch '[branch_name]'? This cannot be undone. (yes/no):"
WAIT for confirmation.

If confirmed:
Use Bash tool: `git checkout [main_branch] && git branch -D [branch_name]`, description: "Delete feature branch"

If option 3: Continue without branch cleanup.

## Advanced Features

### Automatic Parent Work Item Update

If work item has parent work items:
- Check if all child work items are closed
- Suggest updating parent status
- Offer to add comment to parent

### Merge Request Verification

Check for associated merge/pull requests:
- Verify MR/PR is merged
- Link merged MR/PR in closure comment
- Warn if MR/PR still open

### Time Tracking

If Azure DevOps has time tracking:
- Display total time logged
- Show original estimate vs actual
- Include in closure summary

## Error Handling

### Permission Issues
If user lacks permission to close:
- Display permission error
- Suggest who can close (team lead, etc.)
- Exit gracefully

### Failed Quality Checks
If critical checks fail:
- Block closure
- Display failed checks
- Provide remediation steps

### Network Issues
If Azure DevOps API fails:
- Retry once automatically
- Display clear error message
- Suggest checking connection
- Exit without partial updates

## Integration with Workflow

### Full Workflow
```
/fetch-azure-task [ID] → development → /commit → /update-azure-task [ID] → code review → /close-azure-task [ID]
```

### Prerequisites Checklist
Before closure, verify:
- [ ] All code committed and pushed
- [ ] Tests passing
- [ ] Code reviewed and approved
- [ ] Merged to target branch
- [ ] Acceptance criteria met
- [ ] Documentation updated
- [ ] No blocking dependencies

## Best Practices

1. **Always Verify First**: Run quality checks before closing
2. **Document Thoroughly**: Include detailed completion comments
3. **Check Dependencies**: Ensure no blocking work items
4. **Archive Context**: Keep local history for reference
5. **Clean Branches**: Delete merged feature branches
6. **Update Parents**: Keep parent work items in sync

## Safety Features

- Multiple confirmation prompts
- Automatic quality checks
- Acceptance criteria verification
- Uncommitted changes warning
- Unpushed commits detection
- Failed tests blocking
- State transition validation

## Notes
- Closure is final and should only be done when work is fully complete
- All updates are audited in Azure DevOps history
- Local context can be archived for future reference
- Quality gates help prevent premature closure
- Always verify acceptance criteria before closing
