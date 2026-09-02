# Fetch Azure DevOps Work Item

Retrieves and displays Azure DevOps work item details including description, acceptance criteria, related work, and current status.

## Purpose
- Fetch work item data from Azure DevOps
- Display structured work item information
- Save work item context for reference during development
- Provide quick access to task requirements

## Required MCP Setup
This command requires Azure DevOps MCP server to be installed and configured.

If not installed, follow: https://github.com/microsoft/azure-devops-mcp-server

## Execution Steps

### Step 1: Validate Input

Check if work item number was provided as argument.

If no work item number provided:
Output: "Usage: /fetch-azure-task [work_item_number]

Example: /fetch-azure-task 12345"
Exit command.

### Step 2: Fetch Work Item Data

Use mcp__azuredevops__get_work_item tool (if available):
- work_item_id: [provided work item number]

If tool not available:
Output: "Azure DevOps MCP server not configured.

Install: https://github.com/microsoft/azure-devops-mcp-server

Add to ~/.claude/mcp.json:
{
  \"mcpServers\": {
    \"azuredevops\": {
      \"command\": \"npx\",
      \"args\": [\"-y\", \"@azure/azure-devops-mcp-server\"],
      \"env\": {
        \"AZURE_DEVOPS_ORG_URL\": \"https://dev.azure.com/your-org\",
        \"AZURE_DEVOPS_PAT\": \"your-personal-access-token\"
      }
    }
  }
}"
Exit command.

If work item not found or access denied:
Output: "Work item [number] not found or access denied.

Check:
- Work item number is correct
- You have permission to access this work item
- Azure DevOps PAT has sufficient permissions"
Exit command.

### Step 3: Parse Work Item Data

Extract from work item response:
- ID and title
- Work item type (User Story, Task, Bug, Feature)
- State (New, Active, Resolved, Closed)
- Assigned to
- Area path and iteration
- Description
- Acceptance criteria (if available)
- Related work items
- Tags
- Created date and updated date
- Priority and severity (if applicable)

### Step 4: Display Work Item Information

Output work item details in structured format:

"# Azure DevOps Work Item #[ID]

## [Work Item Type]: [Title]

**State**: [State]
**Assigned To**: [Assignee]
**Priority**: [Priority]
**Area**: [Area Path]
**Iteration**: [Iteration]
**Tags**: [Tags]

**Created**: [Created Date]
**Updated**: [Updated Date]

---

## Description

[Work item description]

## Acceptance Criteria

[Acceptance criteria if available, or "No acceptance criteria defined"]

## Related Work Items

[List of related items, or "No related work items"]

---

## Development Context

Work item context has been loaded. Use this information to guide your implementation.
"

### Step 5: Save Work Item Context

Use Bash tool to create task history directory:
- Command: `mkdir -p .claude/azure-tasks`
- Description: "Create Azure tasks directory"

Use Write tool to save work item context to `.claude/azure-tasks/work-item-[ID].md` with the formatted content from Step 4.

Use Bash tool to update gitignore:
- Command: `grep -q "^.claude/azure-tasks/" .gitignore || echo ".claude/azure-tasks/" >> .gitignore`
- Description: "Add Azure tasks to gitignore"

Output: "Work item details saved to: .claude/azure-tasks/work-item-[ID].md

Ready to start development!"

## Error Handling

### Network Issues
If Azure DevOps API request fails:
- Display connection error message
- Suggest checking network and credentials
- Exit gracefully

### Invalid Work Item ID
If work item ID is not a number:
- Display format error
- Show usage example
- Exit command

### Permission Issues
If PAT lacks permissions:
- Display permission error
- List required Azure DevOps permissions:
  - Work Items (Read)
  - Project and Team (Read)
- Exit command

## Integration with Workflow

### Command Flow
```
/fetch-azure-task [ID] → development → /update-azure-task [ID] → /close-azure-task [ID]
```

### Saved Context
Work item details are saved to `.claude/azure-tasks/work-item-[ID].md` for reference throughout development.

## Notes
- Work item context helps maintain alignment with requirements
- Saved files are automatically gitignored
- Use fetched context before implementing features
- Reference work item ID in commits for traceability
