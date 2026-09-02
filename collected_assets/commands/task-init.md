# Task Initialization Command

Intelligent task initialization with deep codebase exploration, architecture design, and implementation planning.

## Purpose

Streamline task initialization by:
- Deeply exploring the codebase before making changes
- Designing architecture with multiple approaches
- Asking clarifying questions before implementation
- Providing explicit user approval gates at key decisions
- Maintaining task history and progress tracking

## Core Principles

- **Understand before acting**: Explore codebase patterns deeply before designing
- **Ask clarifying questions**: Resolve ambiguities before implementation, not during
- **Read files identified by agents**: Build deep context from actual code
- **User approval at key gates**: Get explicit confirmation at major decision points
- **Track progress**: Use TodoWrite throughout all phases

---

## Complexity Detection

Before running the full workflow, detect task complexity to adjust phases:

**Simple Task Indicators** (skip Phases 2 and 4):
- Single file mentioned
- Keywords: "fix typo", "update text", "small change", "rename"
- Bug fix in specific location
- Documentation update

**Complex Task Indicators** (run full 7 phases):
- Keywords: "refactor", "architecture", "migrate", "integrate", "system-wide", "redesign"
- Multiple components/files mentioned
- Cross-cutting concerns (auth, logging, caching, database)
- Database schema changes
- API changes affecting multiple consumers
- New feature spanning multiple layers

Output detected complexity and workflow path before proceeding.

---

## Phase 1: Discovery

**Goal**: Understand the project and the task

### Actions

1. **Launch Discovery Agent (Background)**

   Use Task tool with subagent_type="general-purpose" and run_in_background=true:
   - description: "Discover project context"
   - prompt: "Analyze this project for task initialization.

     Read and summarize these files (continue if any don't exist):
     - ./CLAUDE.md (project-specific instructions)
     - /Users/nagawa/.claude/CLAUDE.md (global instructions)
     - ./README.md (project overview)
     - ./ROADMAP.md (if exists)
     - ./CHECKLIST.md (if exists)

     Detect project type by checking for:
     - package.json (Node.js)
     - go.mod (Go)
     - pyproject.toml or requirements.txt (Python)
     - Cargo.toml (Rust)
     - pom.xml or build.gradle (Java)

     Analyze complexity indicators:
     - Number of source files
     - Presence of tests
     - Architecture hints from documentation

     Return JSON:
     {
       project_type: string,
       docs_found: string[],
       technologies: string[],
       complexity_indicators: string[],
       suggested_complexity: 'simple' | 'complex',
       key_patterns: string[],
       test_framework: string | null
     }"

2. Use TodoWrite tool to create initial phase tracking (while agent runs):
   ```
   - Phase 1: Discovery (in_progress)
   - Phase 2: Codebase Exploration (pending)
   - Phase 3: Clarifying Questions (pending)
   - Phase 4: Architecture Design (pending)
   - Phase 5: Plan & Task History (pending)
   - Phase 6: Implementation (pending)
   - Phase 7: Quality Review (pending)
   ```

3. Use TaskOutput to retrieve discovery results:
   - If wait exceeds 10s, output: "Analyzing project structure..."
   - Store results as DISCOVERY_CONTEXT for use in later phases.

4. Output context summary from agent results:
   - Project type detected
   - Documentation files found
   - Key technologies identified
   - Detected complexity level (simple/complex)
   - Workflow path (full 7 phases or simplified)

5. Use AskUserQuestion tool for input mode:
   - question: "How would you like to describe your task?"
   - header: "Input Mode"
   - multiSelect: false
   - options:
     1. label: "Guided (Recommended)", description: "Select task type first, then add details"
     2. label: "Free-text", description: "Describe your task in your own words"

6. If user selects "Guided":

   Use AskUserQuestion tool:
   - question: "What type of task is this?"
   - header: "Task Type"
   - multiSelect: false
   - options:
     1. label: "New Feature", description: "Add new functionality to the codebase"
     2. label: "Bug Fix", description: "Fix broken or incorrect behavior"
     3. label: "Refactor", description: "Improve code structure without changing behavior"
     4. label: "Other", description: "Integration, documentation, or other task type"

   Output: "Describe the specific task within this category:"
   WAIT for user's task description.

7. If user selects "Free-text":
   Output: "Please describe your task:"
   WAIT for user's task description.

---

## Phase 2: Codebase Exploration

**Goal**: Deeply understand relevant existing code and patterns

**SKIP this phase if task is detected as SIMPLE**

### Actions

1. **Launch Exploration Agents (Background)**

   Use Task tool to launch 2 `feature-dev:code-explorer` agents IN PARALLEL with run_in_background=true:

   **Task tool call 1:**
   - subagent_type: "feature-dev:code-explorer"
   - run_in_background: true
   - description: "Explore similar features"
   - prompt: "CRITICAL DATABASE INSTRUCTIONS:
     - For PostgreSQL queries: ALWAYS use mcp__postgres__query tool. NEVER use bash psql commands.
     - For MariaDB/MySQL queries: ALWAYS use mysql CLI via Bash tool with environment variables:
       mysql -h \"$MARIADB_HOST\" -P \"$MARIADB_PORT\" -u \"$MARIADB_USER\" -p\"$MARIADB_PASSWORD\" {DATABASE_NAME} -e \"YOUR_QUERY\"
     - Load environment variables first: set -a && source .env && set +a

     Find features similar to [USER'S TASK] and trace their implementation comprehensively. Focus on:
     - Entry points and call chains
     - Data flow and transformations
     - Existing patterns that should be followed

     Return a list of 5-10 key files that are essential to understand for this task."

   **Task tool call 2:**
   - subagent_type: "feature-dev:code-explorer"
   - run_in_background: true
   - description: "Explore architecture patterns"
   - prompt: "CRITICAL DATABASE INSTRUCTIONS:
     - For PostgreSQL queries: ALWAYS use mcp__postgres__query tool. NEVER use bash psql commands.
     - For MariaDB/MySQL queries: ALWAYS use mysql CLI via Bash tool with environment variables:
       mysql -h \"$MARIADB_HOST\" -P \"$MARIADB_PORT\" -u \"$MARIADB_USER\" -p\"$MARIADB_PASSWORD\" {DATABASE_NAME} -e \"YOUR_QUERY\"
     - Load environment variables first: set -a && source .env && set +a

     Map the architecture and abstractions relevant to [USER'S TASK]. Focus on:
     - Abstraction layers (presentation, business logic, data)
     - Design patterns and architectural decisions
     - Integration points and dependencies

     Return a list of 5-10 key files that are essential to understand the architecture."

2. Use TaskOutput to retrieve results from both exploration agents:
   - If wait exceeds 10s, output: "Exploring codebase for similar patterns..."
   - Store results as EXPLORATION_RESULTS.

3. Use Read tool to read ALL key files identified by both agents (up to 15 files).

4. **Launch Validation Agent (Background)**

   Use Task tool with subagent_type="Explore" and run_in_background=true:
   - description: "Validate exploration completeness"
   - prompt: "Review these exploration findings for completeness:

     [INSERT EXPLORATION RESULTS FROM BOTH AGENTS]

     For implementing: [USER'S TASK]

     Identify any gaps or missing context. If gaps exist, search for the missing information.
     Return JSON: { gaps_found: boolean, additional_findings: string[], confidence_level: 'high' | 'medium' | 'low' }"

5. Present initial exploration findings to user (don't wait for validation):
   - Similar features found with file:line references
   - Architecture patterns discovered
   - Key abstractions and conventions
   - Potential integration points
   - Files read and their significance

6. Use TaskOutput to retrieve validation results:
   - If wait exceeds 10s, output: "Validating exploration completeness..."
   - If gaps_found is true: Append additional_findings to the exploration summary.

7. Update TodoWrite: Mark Phase 2 as completed, Phase 3 as in_progress.

8. Use AskUserQuestion tool for exploration approval:
   - question: "Does this understanding of the codebase look complete?"
   - header: "Exploration"
   - multiSelect: false
   - options:
     1. label: "Yes, proceed", description: "Understanding is sufficient for this task"
     2. label: "Need more exploration", description: "Some aspects need deeper investigation"
     3. label: "Start over", description: "Misunderstood the task, re-explore"

9. If user selects "Need more exploration":

   Use AskUserQuestion tool:
   - question: "What aspects need more exploration?"
   - header: "Focus Area"
   - multiSelect: false
   - options:
     1. label: "Similar implementations", description: "Find more code examples"
     2. label: "Architecture patterns", description: "Explore design patterns"
     3. label: "Integration points", description: "Understand system boundaries"
     4. label: "Data flow", description: "Trace data through the system"

   Use Task tool with subagent_type="feature-dev:code-explorer":
   - prompt: "Focus on [SELECTED FOCUS AREA] for task: [USER'S TASK]

     Previous findings: [SUMMARY]

     Provide additional insights on the selected focus area."

   Return to step 6 (present updated findings).

10. If user selects "Start over":
    Return to Phase 1 step 6 (task input).

---

## Phase 3: Clarifying Questions

**Goal**: Resolve all ambiguities before designing

**CRITICAL: This phase must NOT be skipped**

### Actions (Hybrid Approach - Category-Grouped Questions)

1. Review exploration findings and original task description.

2. **Scope Category Questions**

   Use AskUserQuestion tool:
   - question: "What should be the scope boundaries for this task?"
   - header: "Scope"
   - multiSelect: true
   - options:
     1. label: "MVP only", description: "Minimum viable implementation"
     2. label: "Full feature", description: "Complete implementation with all edge cases"
     3. label: "Backward compatible", description: "Must not break existing functionality"
     4. label: "Greenfield", description: "No compatibility constraints"

3. **Quality Category Questions**

   Use AskUserQuestion tool:
   - question: "What quality aspects matter most for this task?"
   - header: "Quality"
   - multiSelect: true
   - options:
     1. label: "Test coverage", description: "Comprehensive unit and integration tests"
     2. label: "Performance", description: "Optimized for speed/memory"
     3. label: "Security", description: "Security-first implementation"
     4. label: "Maintainability", description: "Clean, documented code"

4. **Integration Category Questions** (ask only if task involves system integration)

   Use AskUserQuestion tool:
   - question: "What integration constraints apply to this task?"
   - header: "Integration"
   - multiSelect: true
   - options:
     1. label: "Existing patterns", description: "Must follow current codebase patterns"
     2. label: "External APIs", description: "Integrates with third-party services"
     3. label: "Database changes", description: "Requires schema modifications"
     4. label: "Cross-service", description: "Affects multiple services/components"

5. **Additional Context** (if selections suggest complexity)

   Based on user selections, identify if any need clarification:
   - If "Security" selected: Ask about specific security requirements
   - If "Database changes" selected: Ask about migration strategy
   - If "External APIs" selected: Ask about API documentation availability

   For each clarification needed:
   Output: "You selected [aspect]. Please provide more details about [specific question]:"
   WAIT for user's detailed response.

6. **Launch Requirements Analyzer Agent (Background)**

   Use Task tool with subagent_type="general-purpose" and run_in_background=true:
   - description: "Analyze requirements for completeness"
   - prompt: "Analyze these requirements for task: [USER'S TASK]

     Scope selections: [SCOPE SELECTIONS]
     Quality priorities: [QUALITY SELECTIONS]
     Integration constraints: [INTEGRATION SELECTIONS]
     Exploration context: [EXPLORATION_RESULTS SUMMARY]

     Identify:
     1. Missing considerations for this task type
     2. Conflicting requirements (e.g., MVP + full test coverage)
     3. Implicit dependencies not mentioned
     4. Risk areas based on integration selections

     Return JSON: { gaps: string[], conflicts: string[], dependencies: string[], risks: string[] }"

7. **Summarize Requirements** (don't wait for analyzer)

   Output summary of all gathered requirements:
   ```
   ## Requirements Summary
   - Scope: [selections]
   - Quality priorities: [selections]
   - Integration constraints: [selections]
   - Additional context: [user responses]
   ```

8. Use TaskOutput to retrieve analyzer results:
   - If wait exceeds 10s, output: "Analyzing requirements for completeness..."
   - If gaps, conflicts, or risks found: Append to requirements summary.

9. Use AskUserQuestion tool for requirements confirmation:
   - question: "Are these requirements correct?"
   - header: "Confirm"
   - multiSelect: false
   - options:
     1. label: "Yes, proceed to design", description: "Requirements are complete and accurate"
     2. label: "Need to modify", description: "Some requirements need adjustment"
     3. label: "Add more context", description: "Missing important requirements"

10. If user selects "Need to modify" or "Add more context":
    Output: "What needs to be changed or added?"
    WAIT for user's modification.
    Return to step 7 (summarize updated requirements).

11. Update TodoWrite: Mark Phase 3 as completed, Phase 4 as in_progress.

---

## Phase 4: Architecture Design

**Goal**: Design multiple implementation approaches with trade-offs

**SKIP this phase if task is detected as SIMPLE**

### Actions

1. **Launch Architecture Agents (Background)**

   Use Task tool to launch 2-3 `feature-dev:code-architect` agents IN PARALLEL with run_in_background=true:

   **Task tool call 1 (Minimal Approach):**
   - subagent_type: "feature-dev:code-architect"
   - run_in_background: true
   - description: "Design minimal implementation"
   - prompt: "CRITICAL DATABASE INSTRUCTIONS:
     - For PostgreSQL queries: ALWAYS use mcp__postgres__query tool. NEVER use bash psql commands.
     - For MariaDB/MySQL queries: ALWAYS use mysql CLI via Bash tool with environment variables:
       mysql -h \"$MARIADB_HOST\" -P \"$MARIADB_PORT\" -u \"$MARIADB_USER\" -p\"$MARIADB_PASSWORD\" {DATABASE_NAME} -e \"YOUR_QUERY\"
     - Load environment variables first: set -a && source .env && set +a

     Design the MINIMAL implementation for: [USER'S TASK]

     Context from exploration:
     [INSERT EXPLORATION FINDINGS]

     User answers to questions:
     [INSERT USER ANSWERS]

     Focus on: Smallest change possible, maximum reuse of existing code, fastest path to working solution.

     Provide: Patterns found, architecture decision, files to create/modify, build sequence."

   **Task tool call 2 (Clean Architecture Approach):**
   - subagent_type: "feature-dev:code-architect"
   - run_in_background: true
   - description: "Design clean architecture"
   - prompt: "CRITICAL DATABASE INSTRUCTIONS:
     - For PostgreSQL queries: ALWAYS use mcp__postgres__query tool. NEVER use bash psql commands.
     - For MariaDB/MySQL queries: ALWAYS use mysql CLI via Bash tool with environment variables:
       mysql -h \"$MARIADB_HOST\" -P \"$MARIADB_PORT\" -u \"$MARIADB_USER\" -p\"$MARIADB_PASSWORD\" {DATABASE_NAME} -e \"YOUR_QUERY\"
     - Load environment variables first: set -a && source .env && set +a

     Design a CLEAN ARCHITECTURE implementation for: [USER'S TASK]

     Context from exploration:
     [INSERT EXPLORATION FINDINGS]

     User answers to questions:
     [INSERT USER ANSWERS]

     Focus on: Elegant abstractions, maintainability, testability, proper separation of concerns.

     Provide: Patterns found, architecture decision, files to create/modify, build sequence."

   **Task tool call 3 (Pragmatic Balance) - optional for complex tasks:**
   - subagent_type: "feature-dev:code-architect"
   - run_in_background: true
   - description: "Design pragmatic balance"
   - prompt: "... Balance speed with quality, consider team context and project constraints..."

2. Use TaskOutput to retrieve results from all architecture agents:
   - If wait exceeds 10s, output: "Designing architecture approaches..."
   - Store all results for consolidation.

3. **Parallel Refinement - Consolidate AND Quality Review (Background)**

   Use Task tool to launch 2 agents IN PARALLEL with run_in_background=true:

   **Task 1 (Consolidation):**
   - subagent_type: "Plan"
   - run_in_background: true
   - description: "Consolidate architecture options"
   - prompt: "Review and consolidate these architecture options for: [USER'S TASK]

     Requirements from Phase 3:
     [INSERT REQUIREMENTS SUMMARY]

     Option 1 (Minimal Approach):
     [INSERT AGENT 1 RESULTS]

     Option 2 (Clean Architecture):
     [INSERT AGENT 2 RESULTS]

     Option 3 (Pragmatic Balance) - if provided:
     [INSERT AGENT 3 RESULTS]

     Your task:
     1. Analyze trade-offs for THIS SPECIFIC task context
     2. Identify the strongest approach with clear reasoning
     3. Note elements that could be borrowed from other approaches
     4. Produce a UNIFIED RECOMMENDATION with confidence level (high/medium/low)

     Return: recommended_approach, confidence, reasoning, hybrid_elements (optional)"

   **Task 2 (Pre-Quality Check):**
   - subagent_type: "feature-dev:code-reviewer"
   - run_in_background: true
   - description: "Pre-review architecture options"
   - prompt: "Review these architecture options for quality issues:

     Task: [USER'S TASK]
     Requirements: [REQUIREMENTS SUMMARY]

     Option 1 (Minimal): [SUMMARY]
     Option 2 (Clean Architecture): [SUMMARY]
     Option 3 (Pragmatic) - if provided: [SUMMARY]

     Check ALL options for:
     - Missing edge cases in the design
     - Security considerations not addressed
     - Performance implications overlooked
     - Integration risks with existing codebase
     - Alignment with stated requirements

     Return: issues_per_option[], common_issues[], suggestions[], overall_quality (excellent/good/needs_work)"

4. Use TaskOutput to retrieve results from both refinement agents:
   - If wait exceeds 10s, output: "Refining architecture recommendations..."
   - Store consolidation result and quality findings.

5. **Merge Findings**

   Combine consolidation recommendation with quality findings:
   - If quality check found issues with recommended approach: Note them in presentation
   - If quality check suggests alternative approach is better: Include reasoning
   - Incorporate suggestions into final recommendation

6. Present refined architecture comparison to user:
   ```markdown
   ## Architecture Analysis (Refined)

   ### Recommended: [APPROACH NAME]
   **Confidence**: [high/medium/low]
   **Files to modify/create**: [list]
   **Why this approach**: [consolidated reasoning]

   ### Key Trade-offs Considered
   - [trade-off 1]
   - [trade-off 2]

   ### Alternative Approaches Available
   - [Brief mention of other options]

   ### Quality Review Notes
   - [Any issues addressed or remaining considerations]
   ```

7. Use AskUserQuestion tool for architecture selection:
   - question: "Which architecture approach do you prefer?"
   - header: "Architecture"
   - multiSelect: false
   - options:
     1. label: "[Recommended approach] (Recommended)", description: "[Brief description based on consolidation]"
     2. label: "Alternative: Minimal", description: "Fastest path, maximum code reuse"
     3. label: "Alternative: Clean Architecture", description: "Better maintainability, more setup"
     4. label: "Custom requirements", description: "Specify your own priorities"

8. If user selects "Custom requirements":

   Use AskUserQuestion tool:
   - question: "What aspects should the architecture prioritize?"
   - header: "Priorities"
   - multiSelect: true
   - options:
     1. label: "Speed", description: "Fast to implement"
     2. label: "Testability", description: "Easy to test"
     3. label: "Scalability", description: "Handles growth"
     4. label: "Simplicity", description: "Easy to understand"

   Use Task tool with subagent_type="feature-dev:code-architect":
   - run_in_background: true
   - description: "Design custom architecture"
   - prompt: "Design architecture with these priorities: [SELECTED PRIORITIES]

     Task: [USER'S TASK]
     Requirements: [REQUIREMENTS SUMMARY]
     Exploration context: [EXPLORATION FINDINGS]

     Create a custom architecture design that prioritizes the selected aspects."

   Use TaskOutput to retrieve custom architecture results.

9. Update TodoWrite: Mark Phase 4 as completed, Phase 5 as in_progress.

---

## Phase 5: Plan & Task History

**Goal**: Create actionable implementation plan and persistent tracking

### Actions

1. **Launch Plan Generator Agent (Background)**

   Use Task tool with subagent_type="general-purpose" and run_in_background=true:
   - description: "Generate implementation plan"
   - prompt: "Generate complete implementation plan for: [USER'S TASK]

     Chosen Architecture: [CHOSEN ARCHITECTURE or 'Direct implementation' for simple tasks]
     Requirements Summary: [REQUIREMENTS_SUMMARY from Phase 3]
     Files Identified: [FILES from exploration/architecture phases]
     Project Context: [DISCOVERY_CONTEXT from Phase 1]

     Generate THREE outputs:

     1. **Implementation Plan Markdown** with sections:
        - Objective (clear statement of what will be built)
        - Architecture Approach (chosen approach or 'Direct implementation')
        - Files to Modify/Create (with brief description of changes)
        - Implementation Steps (numbered, actionable steps)
        - Success Criteria (specific measurable outcomes)
        - Regression Prevention (checks to ensure no breaking changes)
        - Testing Requirements (unit and integration tests needed)
        - Security Considerations (if applicable)

     2. **Task History File Content** for `.claude/task-history/[timestamp]-[slug].md`:
        - Task title and metadata (date, project, status, complexity)
        - Original task description
        - Exploration findings summary
        - Clarifying Q&A summary
        - Chosen architecture
        - Full implementation plan
        - Progress log with initialization timestamp

     3. **TodoWrite Items Array** (3-7 items):
        Each item needs:
        - content: Imperative form (e.g., 'Implement user validation')
        - activeForm: Present continuous (e.g., 'Implementing user validation')

     Return JSON:
     {
       plan_markdown: string,
       task_history_content: string,
       task_history_filename: string (format: YYYYMMDD-HHMMSS-slug.md),
       todo_items: [{content: string, activeForm: string}]
     }"

2. While agent generates plan, detect project root and create task history directory:

   Use Bash tool:
   - Command: `PROJECT_ROOT=$(pwd); if [ -f "$PROJECT_ROOT/CLAUDE.md" ] || [ -d "$PROJECT_ROOT/.git" ]; then TASK_HISTORY_DIR="$PROJECT_ROOT/.claude/task-history"; else TASK_HISTORY_DIR="$HOME/.claude/task-history"; fi; mkdir -p "$TASK_HISTORY_DIR" && echo "$TASK_HISTORY_DIR"`
   - Description: "Detect project root and create task history directory"
   - Store the output path as TASK_HISTORY_DIR for use in step 5.

3. Use TaskOutput to retrieve plan generator results:
   - If wait exceeds 10s, output: "Generating implementation plan..."

4. Use Bash tool to add task history to gitignore (only if in a git repo):
   - Command: `if [ -f .gitignore ]; then grep -q "^.claude/task-history/" .gitignore 2>/dev/null || echo ".claude/task-history/" >> .gitignore; fi`
   - Description: "Add task history to gitignore if applicable"

5. Use Write tool to create task history file from agent output:
   - file_path: `[TASK_HISTORY_DIR from step 2]/[task_history_filename from agent]`
   - content: [task_history_content from agent]
   - Note: Use the absolute path from step 2, not a relative path

6. Use TodoWrite tool to create implementation task breakdown from agent output:
   - Map each item from todo_items array to TodoWrite format with status: "pending"

7. Output implementation plan summary (plan_markdown from agent).

8. Use AskUserQuestion tool for plan approval:
   - question: "Review the implementation plan above. Ready to proceed?"
   - header: "Plan Approval"
   - multiSelect: false
   - options:
     1. label: "Approve and begin", description: "Plan looks good, start implementation"
     2. label: "Revise plan", description: "Some aspects need adjustment"
     3. label: "Need more details", description: "Plan is too high-level"
     4. label: "Start over", description: "Fundamentally rethink the approach"

9. If user selects "Revise plan":

   Use AskUserQuestion tool:
   - question: "What aspect of the plan needs revision?"
   - header: "Revision"
   - multiSelect: false
   - options:
     1. label: "Implementation steps", description: "Change the order or approach"
     2. label: "File selection", description: "Different files should be modified"
     3. label: "Success criteria", description: "Adjust what 'done' means"
     4. label: "Testing approach", description: "Change testing requirements"

   Output: "Please describe the specific changes needed:"
   WAIT for user's revision details.
   Apply revisions and return to step 7 (output updated plan).

10. If user selects "Need more details":
    Expand the implementation plan with more granular steps.
    Return to step 7 (output expanded plan).

11. If user selects "Start over":
    Return to Phase 4 step 1 (architecture design).

12. Update TodoWrite: Mark Phase 5 as completed, Phase 6 as in_progress.

---

## Phase 6: Implementation

**Goal**: Build the feature following approved architecture

**DO NOT START WITHOUT USER APPROVAL from Phase 5**

### Actions

1. **Launch Agent Preparation Analyzer (Background)**

   Use Task tool with subagent_type="general-purpose" and run_in_background=true:
   - description: "Prepare specialized agent prompts"
   - prompt: "Analyze this implementation plan and prepare specialized agent contexts:

     Implementation Plan: [PLAN_MARKDOWN from Phase 5]
     Files to Modify: [FILES LIST]
     Architecture Approach: [CHOSEN_ARCHITECTURE]

     For each file in the plan, determine if these specialized agents will be needed:

     1. **security-auditor**: Needed if file touches:
        - Authentication/authorization code
        - Password/credential handling
        - Permission checks
        - Input validation for user data

     2. **database-optimizer**: Needed if file touches:
        - SQL queries
        - Database schema changes
        - ORM models
        - Data migrations

     3. **test-automator**: Needed if:
        - File is new (needs test file created)
        - File has complex logic (needs comprehensive tests)
        - File has multiple code paths (needs edge case tests)

     4. **performance-engineer**: Needed if file touches:
        - Critical request paths
        - Large data processing
        - Loops or iterations over collections
        - Database queries with potential N+1

     For each needed agent, prepare a READY-TO-USE prompt with:
     - File context (which files to analyze)
     - Specific concerns for this implementation
     - Expected output format

     Return JSON:
     {
       security_auditor: { needed: boolean, files: string[], prompt: string },
       database_optimizer: { needed: boolean, files: string[], prompt: string },
       test_automator: { needed: boolean, files: string[], prompt: string },
       performance_engineer: { needed: boolean, files: string[], prompt: string },
       summary: string (brief overview of which agents are needed and why)
     }"

2. Mark first implementation todo item as "in_progress" using TodoWrite.

3. Use TaskOutput to retrieve prepared agent prompts:
   - If wait exceeds 10s, output: "Analyzing implementation requirements..."
   - Store PREPARED_PROMPTS for use during implementation.

4. Use Read tool to read all relevant files identified in previous phases.

5. Implement following the approved plan:
   - Follow chosen architecture strictly
   - Match existing codebase conventions
   - Write clean, well-documented code
   - Update TodoWrite status as each item completes

6. Use prepared specialized agents as needed:

   For each agent where PREPARED_PROMPTS.[agent].needed is true:
   - Use Task tool with subagent_type from PREPARED_PROMPTS
   - Use the prepared prompt from PREPARED_PROMPTS.[agent].prompt
   - Include database instructions in prompt if database-related

   Database instructions to include when using database-related agents:
   ```
   CRITICAL DATABASE INSTRUCTIONS:
   - For PostgreSQL queries: ALWAYS use mcp__postgres__query tool. NEVER use bash psql commands.
   - For MariaDB/MySQL queries: ALWAYS use mysql CLI via Bash tool with environment variables:
     mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" {DATABASE_NAME} -e "YOUR_QUERY"
   - Load environment variables first: set -a && source .env && set +a
   ```

7. After each major implementation step:
   - Run relevant tests if available
   - Verify changes work as expected
   - Update task history progress log

8. Update TodoWrite: Mark implementation items as completed, Phase 7 as in_progress.

---

## Phase 7: Quality Review

**Goal**: Ensure code quality and document accomplishments

### Actions

1. **Launch Quality Review Agents (Background - Parallel)**

   Use Task tool to launch 3 `feature-dev:code-reviewer` agents IN PARALLEL with run_in_background=true:

   **Task tool call 1 (Simplicity Focus):**
   - subagent_type: "feature-dev:code-reviewer"
   - run_in_background: true
   - description: "Review for simplicity"
   - prompt: "CRITICAL DATABASE INSTRUCTIONS:
     - For PostgreSQL queries: ALWAYS use mcp__postgres__query tool. NEVER use bash psql commands.
     - For MariaDB/MySQL queries: ALWAYS use mysql CLI via Bash tool with environment variables.

     Review the implementation for SIMPLICITY, DRY, and ELEGANCE.

     Files modified: [LIST OF FILES]

     Focus on: Code readability, unnecessary complexity, duplicated logic, elegant solutions.
     Only report issues with confidence >= 80."

   **Task tool call 2 (Correctness Focus):**
   - subagent_type: "feature-dev:code-reviewer"
   - run_in_background: true
   - description: "Review for correctness"
   - prompt: "... Review for BUGS and FUNCTIONAL CORRECTNESS. Focus on: Logic errors, edge cases, error handling, potential runtime issues..."

   **Task tool call 3 (Conventions Focus):**
   - subagent_type: "feature-dev:code-reviewer"
   - run_in_background: true
   - description: "Review for conventions"
   - prompt: "... Review for PROJECT CONVENTIONS and ARCHITECTURE FIT. Focus on: Consistency with existing patterns, proper abstractions, integration quality..."

2. Use TaskOutput to retrieve results from all 3 review agents:
   - If wait exceeds 10s, output: "Reviewing implementation quality..."

3. Consolidate findings and identify highest severity issues.

4. Present findings to user:
   ```markdown
   ## Quality Review Results

   ### Critical Issues (Must Fix)
   - [issue with file:line]

   ### Recommendations (Should Fix)
   - [issue with file:line]

   ### Minor Suggestions (Nice to Have)
   - [suggestion]
   ```

5. Use AskUserQuestion tool for quality review decision:
   - question: "How would you like to handle the review findings?"
   - header: "Review Action"
   - multiSelect: false
   - options:
     1. label: "Fix critical issues now", description: "Address must-fix issues before completing"
     2. label: "Fix all issues now", description: "Address all issues including recommendations"
     3. label: "Proceed as-is", description: "Accept current implementation, note issues for later"
     4. label: "Review specific issues", description: "Discuss specific findings before deciding"

6. If user selects "Fix critical issues now" or "Fix all issues now":
   - Address the selected issues
   - Run review agents again on modified files
   - Return to step 4 (present updated findings)

7. If user selects "Review specific issues":

   Use AskUserQuestion tool:
   - question: "Which issue category would you like to discuss?"
   - header: "Issue Category"
   - multiSelect: false
   - options:
     1. label: "Critical issues", description: "Must-fix bugs or security problems"
     2. label: "Recommendations", description: "Should-fix improvements"
     3. label: "Minor suggestions", description: "Nice-to-have enhancements"
     4. label: "All categories", description: "Review everything together"

   Present detailed explanation of selected issues.
   Output: "Would you like to fix these issues?"
   WAIT for user's decision.
   If yes, address issues and return to step 4.

8. Generate final summary:
   ```markdown
   ## Task Completed

   ### What Was Built
   - [description of implementation]

   ### Key Decisions Made
   - [architectural choices]
   - [trade-offs accepted]

   ### Files Modified
   - [list with brief descriptions]

   ### Tests Added/Updated
   - [test files]

   ### Suggested Next Steps
   - [recommendations for future work]
   ```

7. Update task history file with completion status and summary.

8. Update TodoWrite: Mark all items as completed.

---

## Error Handling

### Missing Documentation Files
- Continue with available context
- Note missing files in context summary
- Use AskUserQuestion tool to ask if user wants to provide additional context:
  - question: "Some documentation files are missing. Would you like to provide additional context?"
  - header: "Context"
  - options:
    1. label: "Continue without", description: "Proceed with available information"
    2. label: "Provide file paths", description: "Specify alternative documentation locations"
    3. label: "Describe context", description: "Manually provide project context"

### Agent Failures
- Note which agent failed and why
- Use AskUserQuestion tool for recovery:
  - question: "The [agent-name] agent failed. How would you like to proceed?"
  - header: "Agent Error"
  - options:
    1. label: "Retry agent", description: "Try running the agent again"
    2. label: "Skip and continue", description: "Proceed with partial results"
    3. label: "Use alternative agent", description: "Try a different agent for this task"
    4. label: "Manual input", description: "Provide the information manually"

- If retry selected: Re-launch the failed agent with same prompt
- If alternative selected: Use Task tool with backup agent type (e.g., "Explore" instead of "feature-dev:code-explorer")

### User Rejects Plan Multiple Times (3+ rejections)
- Use AskUserQuestion tool:
  - question: "The plan has been rejected multiple times. What's the main concern?"
  - header: "Concern"
  - options:
    1. label: "Scope is wrong", description: "Task boundaries need adjustment"
    2. label: "Approach is wrong", description: "Need fundamentally different solution"
    3. label: "Missing context", description: "Important information wasn't captured"
    4. label: "Start fresh", description: "Begin from scratch with new task description"

- Based on selection, return to appropriate phase

### No Git Repository
- Skip gitignore update automatically
- Still create task history locally
- Output: "Note: Git not detected - task history saved locally only"

### Complex Task Detection Disagreement
- Use AskUserQuestion tool:
  - question: "Task was detected as [simple/complex]. Would you like to override?"
  - header: "Complexity"
  - options:
    1. label: "Keep detection", description: "Proceed with detected complexity level"
    2. label: "Force Simple", description: "Skip exploration and architecture phases"
    3. label: "Force Complex", description: "Run full 7-phase workflow"

### Network/Tool Errors
- For transient errors: Automatically retry up to 3 times with exponential backoff
- For persistent errors: Use AskUserQuestion tool:
  - question: "A tool is experiencing errors. How would you like to proceed?"
  - header: "Tool Error"
  - options:
    1. label: "Retry", description: "Try the operation again"
    2. label: "Skip step", description: "Continue without this operation"
    3. label: "Pause task", description: "Save progress and stop for now"

---

## Notes

- Task history is saved to `.claude/task-history/`:
  - If in a project with CLAUDE.md or .git: saves to `PROJECT_ROOT/.claude/task-history/`
  - Otherwise: falls back to `~/.claude/task-history/` (global)
- Database tool instructions must be included in ALL agent prompts
- Use TodoWrite consistently to track progress through all phases
- Context is loaded fresh each time to ensure accuracy
- Feature-dev agents (code-explorer, code-architect, code-reviewer) provide deeper analysis than generic agents
- Simple tasks skip exploration and architecture phases for efficiency
- All phases have explicit user approval gates for transparency

### Tool Usage Patterns (Updated)

- **AskUserQuestion**: Used for all decision points with discrete options (max 4 options per question)
- **WAIT for user**: Only used for free-text input where structured options don't apply
- **3-Pass Refinement**: Agent outputs are validated, consolidated, and quality-reviewed before presenting to user
- **Hybrid Questions**: Category-grouped sequential AskUserQuestion calls for clarifying questions
- **Tool-based Error Recovery**: All error scenarios use AskUserQuestion for user-driven recovery decisions

### Async Agent Patterns (Coordinator + Worker Architecture)

This skill uses a **Coordinator + Worker Agents** pattern to optimize context usage:

**Main Conversation (Coordinator)**:
- Handles user interaction (AskUserQuestion, WAIT)
- Launches async agents for heavy work
- Passes context between phases
- Manages TodoWrite progress tracking
- Never performs heavy file reads or analysis directly

**Background Agents (Workers)**:
- Perform heavy file reading and analysis
- Generate plans, prompts, and structured outputs
- Run in parallel when independent
- Return JSON-structured results for easy parsing

**Async Patterns by Phase**:

| Phase | Background Agent | Purpose |
|-------|-----------------|---------|
| 1 | Discovery Agent | Read docs, detect project type, analyze complexity |
| 2 | Validation Agent | Verify exploration completeness (runs while presenting) |
| 3 | Requirements Analyzer | Identify gaps, conflicts, dependencies, risks |
| 4 | Consolidation + Quality (parallel) | Merge approaches + pre-review quality |
| 5 | Plan Generator | Generate plan, task history, and todos |
| 6 | Agent Preparation | Prepare prompts for specialized agents |
| 7 | Quality Reviewers (3 parallel) | Multi-perspective code review |

**Key Patterns**:

1. **Launch Early, Retrieve Later**:
   ```
   1. Use Task tool with run_in_background=true
   2. Do other work while agent runs
   3. Use TaskOutput to retrieve results
   ```

2. **Progress Indicators for Long Waits**:
   ```
   Use TaskOutput to retrieve results:
   - If wait exceeds 10s, output: "Processing message..."
   ```

3. **Parallel Independent Agents**:
   ```
   Use Task tool to launch N agents IN PARALLEL with run_in_background=true:
   - All agents run concurrently
   - Use TaskOutput for each to retrieve results
   ```

4. **Present While Validating**:
   ```
   1. Launch validation agent in background
   2. Present initial findings to user (don't wait)
   3. Use TaskOutput to get validation results
   4. Append additional findings if any
   ```

5. **Prepared Prompts Pattern**:
   ```
   1. Agent analyzes what specialized agents are needed
   2. Prepares ready-to-use prompts with file context
   3. Use prepared prompts during implementation
   ```

**Benefits**:
- Cleaner main conversation context
- Better token efficiency
- Parallel processing where possible
- User sees results faster
- Prepared contexts reduce agent setup time
