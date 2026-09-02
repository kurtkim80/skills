# Documentation Writer Command

Comprehensive documentation generator that delegates to specialized agents for creating detailed project documentation with diagrams, flowcharts, and complete technical specifications.

## Purpose
- Generate various types of documentation (task-specific or full project)
- Create visual diagrams and flowcharts
- Document APIs, architecture, business logic, and data flows
- Produce professional technical documentation
- Support multiple output formats

## Workflow

### Phase 1: Documentation Scope Selection
1. **STOP** → "What type of documentation do you need?"
   ```
   1. Task Documentation - Document current task implementation
   2. API Documentation - Complete API reference with examples
   3. Architecture Documentation - System design and architecture
   4. Full Project Documentation - Comprehensive project docs
   5. Database Documentation - Schema, relationships, queries
   6. Business Logic Documentation - Rules, workflows, processes
   7. Deployment Documentation - Infrastructure and deployment
   8. Custom Documentation - Specify your needs
   ```

2. **Based on Selection, Ask Follow-ups:**
   
   **For Task Documentation:**
   - STOP → "Include implementation details? (y/n)"
   - STOP → "Include test scenarios? (y/n)"
   - STOP → "Include performance metrics? (y/n)"
   
   **For API Documentation:**
   - STOP → "Include request/response examples? (y/n)"
   - STOP → "Include authentication flows? (y/n)"
   - STOP → "Include error handling? (y/n)"
   - STOP → "Generate OpenAPI/Swagger spec? (y/n)"
   
   **For Architecture Documentation:**
   - STOP → "Include system diagrams? (y/n)"
   - STOP → "Include data flow diagrams? (y/n)"
   - STOP → "Include sequence diagrams? (y/n)"
   - STOP → "Include deployment diagrams? (y/n)"
   
   **For Full Project Documentation:**
   - STOP → "Documentation depth: (basic/standard/comprehensive)"
   - STOP → "Include all diagrams? (y/n)"
   - STOP → "Include code examples? (y/n)"
   - STOP → "Include troubleshooting guide? (y/n)"

### Phase 2: Project Analysis
1. **Gather Project Information**
   ```bash
   # Detect project type
   project_type=""
   [ -f package.json ] && project_type="Node.js"
   [ -f requirements.txt ] || [ -f pyproject.toml ] && project_type="Python"
   [ -f go.mod ] && project_type="Go"
   [ -f Cargo.toml ] && project_type="Rust"
   [ -f pom.xml ] && project_type="Java/Maven"
   [ -f build.gradle ] && project_type="Java/Gradle"
   ```

2. **Analyze Project Structure**
   ```bash
   # Get directory structure
   find . -type d -name .git -prune -o -type d -print | head -50
   
   # Count files by type
   find . -type f -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" | wc -l
   ```

3. **Load Existing Documentation**
   - Read README.md
   - Read CLAUDE.md
   - Check docs/ directory
   - Check .claude/task-history/

### Phase 3: Agent Delegation for Analysis
Deploy specialized agents in parallel based on documentation needs:

1. **Core Analysis Agents** (Always Used):
   - **backend-architect**: Analyze system architecture and design patterns
   - **frontend-developer**: Analyze UI components and user flows (if applicable)
   - **database-optimizer**: Analyze database schema and queries
   - **api-documenter**: Analyze API endpoints and contracts

2. **Specialized Agents** (Based on Scope):
   
   **For Business Logic:**
   - **backend-architect**: Extract business rules and workflows
   - **data-engineer**: Document data pipelines and transformations
   
   **For Security Documentation:**
   - **security-auditor**: Document security measures and authentication
   
   **For Performance Documentation:**
   - **performance-engineer**: Analyze and document performance characteristics
   
   **For Testing Documentation:**
   - **test-automator**: Document test strategies and coverage
   
   **For Infrastructure:**
   - **deployment-engineer**: Document deployment and CI/CD
   - **cloud-architect**: Document cloud infrastructure

3. **Agent Instructions Template:**
   ```
   Analyze the codebase and provide:
   1. [Specific aspect to analyze]
   2. Key components and their relationships
   3. Data flows and dependencies
   4. Important patterns and conventions
   5. Potential improvements or issues
   6. Code examples for documentation
   ```

### Phase 4: Diagram Generation
1. **Mermaid Diagram Types**
   
   **Architecture Diagram:**
   ```mermaid
   graph TB
     subgraph "Frontend"
       UI[User Interface]
       COMP[Components]
     end
     
     subgraph "Backend"
       API[API Layer]
       BL[Business Logic]
       DB[(Database)]
     end
     
     UI --> API
     API --> BL
     BL --> DB
   ```
   
   **Sequence Diagram:**
   ```mermaid
   sequenceDiagram
     participant User
     participant Frontend
     participant API
     participant Database
     
     User->>Frontend: Request
     Frontend->>API: API Call
     API->>Database: Query
     Database-->>API: Result
     API-->>Frontend: Response
     Frontend-->>User: Display
   ```
   
   **Flow Chart:**
   ```mermaid
   flowchart LR
     Start([Start]) --> Input{Input Valid?}
     Input -->|Yes| Process[Process Data]
     Input -->|No| Error[Show Error]
     Process --> Save[(Save to DB)]
     Save --> End([End])
     Error --> End
   ```
   
   **Entity Relationship Diagram:**
   ```mermaid
   erDiagram
     USER ||--o{ ORDER : places
     ORDER ||--|{ ORDER_ITEM : contains
     PRODUCT ||--o{ ORDER_ITEM : includes
     
     USER {
       int id PK
       string email
       string name
     }
     ORDER {
       int id PK
       int user_id FK
       date created_at
       string status
     }
   ```

2. **PlantUML Diagrams** (Alternative)
   ```plantuml
   @startuml
   !define RECTANGLE class
   
   package "System Architecture" {
     [Frontend] --> [API Gateway]
     [API Gateway] --> [Service A]
     [API Gateway] --> [Service B]
     [Service A] --> [Database A]
     [Service B] --> [Database B]
   }
   @enduml
   ```

### Phase 5: Documentation Generation
Based on scope and agent analysis, generate documentation sections:

1. **Standard Structure Template**
   ```markdown
   # [Project Name] Documentation
   
   ## Table of Contents
   1. [Overview](#overview)
   2. [Architecture](#architecture)
   3. [Getting Started](#getting-started)
   4. [API Reference](#api-reference)
   5. [Business Logic](#business-logic)
   6. [Database Schema](#database-schema)
   7. [Deployment](#deployment)
   8. [Testing](#testing)
   9. [Troubleshooting](#troubleshooting)
   
   ## Overview
   [Project description and purpose]
   
   ### Key Features
   - [Feature 1]
   - [Feature 2]
   
   ### Technology Stack
   - **Backend**: [Technologies]
   - **Frontend**: [Technologies]
   - **Database**: [Technologies]
   - **Infrastructure**: [Technologies]
   
   ## Architecture
   
   ### System Architecture
   [Architecture diagram]
   [Architecture description]
   
   ### Component Overview
   [Component descriptions and relationships]
   
   ### Data Flow
   [Data flow diagram]
   [Flow description]
   
   ## API Reference
   
   ### Authentication
   [Authentication method and flow]
   
   ### Endpoints
   
   #### [Endpoint Group]
   
   ##### GET /api/resource
   [Description]
   
   **Request:**
   ```json
   {
     "param": "value"
   }
   ```
   
   **Response:**
   ```json
   {
     "data": "value"
   }
   ```
   
   **Error Codes:**
   - 400: Bad Request
   - 401: Unauthorized
   - 404: Not Found
   
   ## Business Logic
   
   ### Core Workflows
   
   #### [Workflow Name]
   [Workflow diagram]
   [Business rules and logic]
   
   ### Business Rules
   1. [Rule 1]
   2. [Rule 2]
   
   ## Database Schema
   
   ### Entity Relationship
   [ER Diagram]
   
   ### Tables
   
   #### [Table Name]
   | Column | Type | Description |
   |--------|------|-------------|
   | id | INTEGER | Primary key |
   | name | VARCHAR(255) | Name field |
   
   ### Key Queries
   ```sql
   -- [Query description]
   SELECT * FROM table WHERE condition;
   ```
   
   ## Deployment
   
   ### Requirements
   - [Requirement 1]
   - [Requirement 2]
   
   ### Environment Variables
   | Variable | Description | Example |
   |----------|-------------|---------|
   | API_KEY | API authentication key | abc123 |
   
   ### Deployment Process
   [Deployment diagram]
   [Step-by-step deployment guide]
   
   ## Testing
   
   ### Test Strategy
   [Testing approach and coverage]
   
   ### Running Tests
   ```bash
   # Unit tests
   npm test
   
   # Integration tests
   npm run test:integration
   
   # E2E tests
   npm run test:e2e
   ```
   
   ### Test Scenarios
   | Scenario | Description | Expected Result |
   |----------|-------------|-----------------|
   | [Test 1] | [Description] | [Result] |
   
   ## Troubleshooting
   
   ### Common Issues
   
   #### [Issue 1]
   **Problem**: [Description]
   **Solution**: [Steps to resolve]
   
   #### [Issue 2]
   **Problem**: [Description]
   **Solution**: [Steps to resolve]
   
   ### Debugging Tips
   - [Tip 1]
   - [Tip 2]
   
   ### Logs
   - **Application Logs**: `/var/log/app.log`
   - **Error Logs**: `/var/log/error.log`
   ```

2. **Task-Specific Documentation Template**
   ```markdown
   # Task: [Task Name]
   
   ## Implementation Overview
   [What was implemented and why]
   
   ## Technical Details
   
   ### Changes Made
   [List of files and changes]
   
   ### Architecture Impact
   [How this affects the system]
   
   ### Code Structure
   ```
   src/
   ├── feature/
   │   ├── component.js
   │   └── service.js
   └── tests/
       └── feature.test.js
   ```
   
   ## Implementation Flow
   [Sequence diagram or flowchart]
   
   ## Testing
   [Test cases and coverage]
   
   ## Performance Considerations
   [Performance impacts and optimizations]
   
   ## Security Considerations
   [Security implications]
   
   ## Future Improvements
   [Suggested enhancements]
   ```

### Phase 6: Output Generation
1. **Create Documentation Directory**
   ```bash
   mkdir -p docs/generated
   timestamp=$(date +%Y%m%d_%H%M%S)
   ```

2. **Generate Multiple Formats**
   
   **Markdown (Primary):**
   ```bash
   output_file="docs/generated/${doc_type}_${timestamp}.md"
   ```
   
   **HTML (Optional):**
   - Convert Markdown to HTML with syntax highlighting
   - Include CSS for professional styling
   
   **PDF (Optional):**
   - Convert to PDF using pandoc or similar
   
   **API Spec (If applicable):**
   ```yaml
   # OpenAPI 3.0 specification
   openapi: 3.0.0
   info:
     title: API Documentation
     version: 1.0.0
   paths:
     /endpoint:
       get:
         summary: Endpoint description
   ```

3. **Present Generated Documentation**
   ```markdown
   ## Documentation Generated Successfully
   
   **Type**: [Documentation Type]
   **Files Created**:
   - Main: docs/generated/[filename].md
   - Diagrams: docs/generated/diagrams/
   - Examples: docs/generated/examples/
   
   **Sections Included**:
   - [Section 1]
   - [Section 2]
   
   **Statistics**:
   - Total Lines: [N]
   - Diagrams: [N]
   - Code Examples: [N]
   - API Endpoints Documented: [N]
   ```

4. **STOP** → "Documentation complete. Options: (view/edit/regenerate/done):"
   - view: Display documentation
   - edit: Open in editor
   - regenerate: Generate with different options
   - done: Finalize

### Phase 7: Integration and Updates
1. **Update Project Files**
   ```bash
   # Update README.md with link to new docs
   echo "📚 [Full Documentation](docs/generated/[filename].md)" >> README.md
   
   # Create/Update docs index
   cat > docs/INDEX.md << EOF
   # Documentation Index
   
   ## Generated Documentation
   - [Latest Full Docs](generated/[filename].md)
   - [API Reference](generated/api_reference.md)
   - [Architecture Guide](generated/architecture.md)
   EOF
   ```

2. **Git Integration**
   ```bash
   # Add to git
   git add docs/generated/
   git status
   ```

## Agent Delegation Strategy

### Parallel Analysis Pattern
```
Phase 1: Broad Analysis (All agents in parallel)
├── backend-architect: System overview
├── frontend-developer: UI analysis
├── database-optimizer: Data structure
├── api-documenter: Endpoint mapping
└── test-automator: Test coverage

Phase 2: Deep Dive (Specialized agents)
├── security-auditor: Security analysis
├── performance-engineer: Performance metrics
├── deployment-engineer: Infrastructure
└── cloud-architect: Cloud resources

Phase 3: Integration (Lead agent)
└── backend-architect: Compile and organize all findings
```

### Agent Prompts
**Backend Architect:**
```
Analyze the codebase architecture and provide:
1. System design patterns used
2. Service layer organization
3. Dependency injection setup
4. Middleware and interceptors
5. Error handling patterns
6. Suggested architecture diagram in Mermaid format
```

**API Documenter:**
```
Document all API endpoints with:
1. Complete endpoint list with methods
2. Request/response schemas
3. Authentication requirements
4. Rate limiting and quotas
5. Error response formats
6. OpenAPI specification draft
```

**Database Optimizer:**
```
Analyze database structure and provide:
1. Complete schema documentation
2. Table relationships (ER diagram)
3. Index analysis
4. Common query patterns
5. Migration history
6. Performance considerations
```

## Documentation Quality Standards

### Completeness Checklist
- [ ] All public APIs documented
- [ ] All configuration options explained
- [ ] Installation steps verified
- [ ] Examples provided for common use cases
- [ ] Troubleshooting section included
- [ ] Performance considerations noted
- [ ] Security best practices documented
- [ ] Deployment process detailed

### Clarity Guidelines
1. **Use Clear Headers**: Hierarchical and descriptive
2. **Provide Examples**: Code snippets for every concept
3. **Include Visuals**: Diagrams for complex flows
4. **Define Terms**: Glossary for domain-specific terms
5. **Link References**: Cross-reference related sections

### Maintenance
- Version documentation with project
- Update documentation with each feature
- Review quarterly for accuracy
- Track documentation debt

## Output Formats

### Markdown Features
- GitHub Flavored Markdown
- Syntax highlighting for code blocks
- Collapsible sections for details
- Tables for structured data
- Mermaid diagrams embedded

### HTML Generation
```html
<!DOCTYPE html>
<html>
<head>
  <title>Project Documentation</title>
  <link rel="stylesheet" href="style.css">
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
</head>
<body>
  <!-- Converted Markdown -->
</body>
</html>
```

### PDF Options
- Table of contents with page numbers
- Header/footer with project info
- Syntax highlighted code
- Embedded diagrams
- Professional typography

## Error Handling

### No Project Detected
- Ask user to specify project type
- Provide manual structure input option

### Large Codebases
- Implement sampling strategy
- Focus on core modules
- Generate incrementally

### Missing Information
- Flag undocumented areas
- Suggest TODO items
- Provide templates for completion

## Best Practices

1. **Keep Documentation Close to Code**
   - Inline comments for complex logic
   - README in each module
   - API docs near endpoints

2. **Automate Where Possible**
   - Generate from code annotations
   - Extract from tests
   - Update from CI/CD

3. **Focus on Why, Not Just What**
   - Explain design decisions
   - Document trade-offs
   - Include historical context

4. **Make It Searchable**
   - Use consistent terminology
   - Include keywords
   - Create index pages

5. **Version Control**
   - Track documentation changes
   - Link to code versions
   - Maintain changelog

## Notes
- Documentation is generated based on current codebase state
- Agents work in parallel for efficiency
- Multiple output formats supported
- Integrates with existing documentation
- Never mentions AI/automation in output