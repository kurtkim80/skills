# Merge Request Draft Generator

Generates comprehensive merge request documentation in PT-BR compliance, analyzing commits and changes to create professional MR descriptions.

## Purpose
- Analyze branch commits and changes
- Generate detailed MR documentation in Portuguese (PT-BR)
- Extract technical details from git history
- Create structured, review-ready merge requests
- Never mention AI/automation tools

## Execution Steps

### Step 1: Analyze Branch

Use Bash tool to get current branch:
- Command: `git branch --show-current`
- Description: "Get current branch name"

If not on a branch, output: "Not on a branch. Please checkout your feature branch first." and exit.

Use Bash tool to identify base branch:
- Command: `for base in main master develop development staging; do git rev-parse --verify $base >/dev/null 2>&1 && echo $base && break; done`
- Description: "Find base branch"

If no base found:
Output: "What is the target branch for this MR? (main/master/develop):"
WAIT for user's response.

Use Bash tool to find task history:
- Command: `ls -t .claude/task-history/*.md 2>/dev/null | head -1`
- Description: "Find most recent task file"

If task file exists, use Read tool to read it and parse for objective and context.

### Step 2: Analyze Commits

Use Bash tool to get commit list:
- Command: `git log --oneline [base_branch]..HEAD`
- Description: "Get all commits from branch divergence"

Use Bash tool to get detailed commit info:
- Command: `git log --format="%H|%s|%b|%an|%ad" --date=short [base_branch]..HEAD`
- Description: "Get detailed commit information"

Parse output to extract:
- Commit hash, subject, body, author, date
- Categorize by conventional commit type (feat, fix, chore, docs, etc.)

Use Bash tool to get commit statistics:
- Command: `git show --stat --format="" [commit_hash]`
- Description: "Get files changed per commit"

### Step 3: Analyze File Changes

Use Bash tool to get overall statistics:
- Command: `git diff --stat [base_branch]..HEAD`
- Description: "Get total diff statistics"

Use Bash tool to get detailed file changes:
- Command: `git diff --name-status [base_branch]..HEAD`
- Description: "List all changed files with status"

Categorize changes:
- A: Added files
- M: Modified files
- D: Deleted files
- R: Renamed files

Output: "Run comprehensive review with specialized agents? This includes architecture, code quality, test coverage, database, and security analysis. (y/n):"
WAIT for user's response.

If user says yes or y:

Use Task tool to launch 5 agents IN PARALLEL (single message with 5 Task tool invocations):

1. Task tool call:
   - subagent_type: "backend-architect"
   - prompt: "Analyze architecture impacts of these changes: [file list and diffs]"

2. Task tool call:
   - subagent_type: "code-reviewer"
   - prompt: "Review code quality aspects of these changes: [file list and diffs]"

3. Task tool call:
   - subagent_type: "test-automator"
   - prompt: "Assess test coverage of these changes: [file list and diffs]"

4. Task tool call:
   - subagent_type: "database-optimizer"
   - prompt: "Identify database changes and implications: [file list and diffs]"

5. Task tool call:
   - subagent_type: "security-auditor"
   - prompt: "Identify security implications of these changes: [file list and diffs]"

Wait for all 5 agents to complete.

If user says no or n:
Skip specialized agent reviews and proceed with basic git analysis only.

### Step 4: Generate MR Content
1. **Generate PT-BR Content Structure**
   ```markdown
   # Merge Request #[number]: [Título Descritivo]
   
   ## Objetivo
   [Descrição clara do objetivo da MR]
   
   ## Resumo das Alterações
   - **[N] arquivos modificados/criados**
   - **[N] inserções (+)**
   - **[N] deleções (-)**
   - **[N] commits totais**
   - **[Principais funcionalidades/correções]**
   
   ## Commits Incluídos
   [Lista numerada de commits com hash e mensagem]
   
   ## Funcionalidades Implementadas
   
   ### 1. [Funcionalidade Principal]
   [Descrição detalhada]
   
   #### Características Técnicas
   [Detalhes técnicos]
   
   ### 2. [Segunda Funcionalidade]
   [Descrição]
   
   ## Arquitetura Implementada
   [Se aplicável, diagramas ou descrições de arquitetura]
   
   ## Arquivos Criados/Modificados
   
   ### [Categoria 1]
   1. **path/to/file.ext** ([N] linhas)
      - [Descrição da mudança]
   
   ## Validações e Testes
   
   ### Testes Implementados
   - [Lista de testes adicionados]
   
   ### Cobertura
   - [Informações sobre cobertura de testes]
   
   ## Como Testar
   ```bash
   # Comandos para testar a funcionalidade
   ```
   
   ## Impacto e Riscos
   - **Impacto**: [Baixo/Médio/Alto] - [Justificativa]
   - **Riscos**: [Descrição dos riscos]
   - **Mitigação**: [Como os riscos foram mitigados]
   
   ## Checklist de Review
   - [ ] Código segue padrões do projeto
   - [ ] Nomenclatura consistente
   - [ ] Testes implementados
   - [ ] Documentação atualizada
   - [ ] Sem quebras de compatibilidade
   - [ ] Performance aceitável
   - [ ] Segurança verificada
   
   ## Próximos Passos Sugeridos
   [Lista de melhorias ou trabalhos futuros]
   
   ## Conclusão
   [Resumo final do que a MR adiciona ao projeto]
   ```

2. **PT-BR Terminology Mapping**
   - feature → funcionalidade
   - bug fix → correção de bug
   - improvement → melhoria
   - performance → desempenho
   - security → segurança
   - database → banco de dados
   - cache → cache (mantém)
   - endpoint → endpoint (mantém)
   - request/response → requisição/resposta
   - merge request → merge request (mantém)
   - commit → commit (mantém)
   - branch → branch (mantém)

3. **Technical Analysis Sections**
   Based on changes detected, include relevant sections:
   
   **For API Changes:**
   - Endpoints criados/modificados
   - Schemas de request/response
   - Validações implementadas
   - Documentação OpenAPI
   
   **For Database Changes:**
   - Migrações executadas
   - Tabelas criadas/modificadas
   - Índices adicionados
   - Queries otimizadas
   
   **For Infrastructure:**
   - Configurações Docker
   - Variáveis de ambiente
   - Serviços adicionados
   - Dependências atualizadas

### Step 5: Review and Save MR Draft

Clean content by removing any references to:
- Claude, AI, agents, automation
- Generated content markers
- Task-init system references

Present draft to user:

Output: "## Merge Request Draft Generated

File will be saved to: .claude/mr-drafts/[timestamp]-[branch].md

Preview:
[First 50 lines of MR content]"

Output: "Review MR draft. Options: (edit/save/copy/discard):"
WAIT for user's choice.

If user chooses 'edit': Offer to make specific changes
If user chooses 'save' or default:

Use Bash tool to create directory:
- Command: `mkdir -p .claude/mr-drafts`
- Description: "Create MR drafts directory"

Use Write tool to save MR draft to `.claude/mr-drafts/[timestamp]-[branch].md`

Use Bash tool to update gitignore:
- Command: `grep -q "^.claude/mr-drafts/" .gitignore || echo ".claude/mr-drafts/" >> .gitignore`
- Description: "Add MR drafts to gitignore"

If user chooses 'discard': Exit without saving

### Step 6: Create MR/PR (Optional)

Output: "Create the Merge Request / Pull Request now? (y/n):"
WAIT for user's response.

If user says no, exit command.

If user says yes:

Output: "Choose your Git hosting platform:
1. GitHub (gh CLI)
2. GitLab (glab CLI)

Choose platform (1 or 2):"
WAIT for user's choice.

If user chooses GitHub (1):

Use Bash tool to check if gh CLI is installed:
- Command: `which gh`
- Description: "Check if gh CLI is installed"

If not installed, output: "gh CLI not installed. Install with: brew install gh" and exit.

Use Bash tool to create PR:
- Command: `gh pr create --title "[MR title]" --body-file .claude/mr-drafts/[timestamp]-[branch].md`
- Description: "Create GitHub Pull Request"

If user chooses GitLab (2):

Use Bash tool to check if glab CLI is installed:
- Command: `which glab`
- Description: "Check if glab CLI is installed"

If not installed, output: "glab CLI not installed. Install with: brew install glab" and exit.

Use Bash tool to check if glapi function exists in zsh:
- Command: `zsh -c "source ~/.zshrc 2>/dev/null; type glapi" 2>/dev/null`
- Description: "Check if glapi zsh function is available"

If glapi function is available:

Use Bash tool to create MR using glapi:
- Command: `zsh -c "source ~/.zshrc 2>/dev/null; glapi /merge_requests --method POST --field source_branch=[branch] --field target_branch=[base_branch] --field title='[MR title]' --field description=\"\$(cat .claude/mr-drafts/[timestamp]-[branch].md)\" --field remove_source_branch=true --field squash=true"`
- Description: "Create GitLab Merge Request via glapi"

If glapi function is NOT available:

Use Bash tool to create MR using glab CLI:
- Command: `glab mr create --title "[MR title]" --description "$(cat .claude/mr-drafts/[timestamp]-[branch].md)"`
- Description: "Create GitLab Merge Request via glab CLI"

Output the MR/PR URL returned by the CLI tool or API.

## Smart Detection Features

### Functionality Detection
Automatically identifies:
- **API Endpoints**: Routes, controllers, handlers
- **Database Changes**: Migrations, models, queries
- **Frontend Components**: React/Vue/Angular components
- **Tests**: Unit, integration, E2E tests
- **Configuration**: Environment, Docker, CI/CD
- **Documentation**: README, API docs, comments

### Impact Assessment
Calculates impact based on:
- Number of files changed
- Critical path modifications
- Database schema changes
- API contract changes
- Configuration updates

### Risk Analysis
Identifies risks from:
- Large file changes (>500 lines)
- Database migrations
- Security-related files
- Authentication/authorization changes
- External service integrations

## Integration with Workflow

### Command Flow
```
/task-init → development → /commit → /mr-draft → push → create MR
```

### Task Context
- Reads from `.claude/task-history/`
- Links MR to original task objective
- Includes success criteria in validation

### Commit History
- Uses commits from `/commit` command
- Maintains clean history narrative
- Groups related changes logically

## PT-BR Compliance Rules

### Language Standards
1. **Technical Terms**: Keep English where standard
   - API, REST, HTTP, JSON, etc.
   - Framework names (React, Django, etc.)
   - Git terminology (commit, branch, merge)

2. **Translate Common Terms**:
   - added → adicionado
   - removed → removido
   - updated → atualizado
   - fixed → corrigido
   - improved → melhorado
   - created → criado
   - deleted → deletado/removido

3. **Section Headers in Portuguese**:
   - Objetivo (Purpose)
   - Resumo (Summary)
   - Funcionalidades (Features)
   - Arquivos (Files)
   - Testes (Tests)
   - Riscos (Risks)
   - Conclusão (Conclusion)

### Formatting Standards
- Use Brazilian number format (1.234,56)
- Date format: DD/MM/YYYY
- Time format: HH:mm:ss
- Maintain formal tone ("foi implementado" not "implementamos")

## Error Handling

### No Commits
- Check if branch has commits
- Suggest checking branch or committing changes

### Merge Conflicts
- Detect if branch has conflicts with base
- Warn about need to resolve before MR

### Large MRs
- Warn if >20 files or >1000 lines changed
- Suggest breaking into smaller MRs

### Missing Tests
- Flag if no test files detected
- Remind about test requirements

## Advanced Features

### Template Customization
Check for project-specific template:
```bash
if [ -f .claude/mr-template.md ]; then
  # Use custom template
fi
```

### Auto-Detection
- Project type from files (package.json, pom.xml, etc.)
- Framework from imports/dependencies
- Testing framework from test files
- CI/CD from workflow files

### Statistics Generation
- Lines of code by language
- Test coverage delta (if available)
- Performance metrics (if measured)
- Security scan results (if available)

## Output Options

### File Output
Default: `.claude/mr-drafts/[timestamp]-[branch].md`

### Clipboard Copy
Option to copy directly for pasting into GitLab/GitHub

### Direct Integration
Future: Direct MR creation via API:
- GitLab API
- GitHub API
- Bitbucket API

## Best Practices

1. **One Feature Per MR**
   - Keep MRs focused and reviewable
   - Easier to track and rollback

2. **Clear Objectives**
   - State the problem being solved
   - Explain the solution approach

3. **Comprehensive Testing**
   - Document test scenarios
   - Include test commands

4. **Risk Assessment**
   - Be transparent about impacts
   - Provide mitigation strategies

5. **Review Readiness**
   - Complete checklist items
   - Ensure CI/CD passes

## Notes
- MR drafts are project-specific
- Never mentions AI assistance
- Maintains professional PT-BR tone
- Focuses on technical accuracy
- Provides actionable review guidance