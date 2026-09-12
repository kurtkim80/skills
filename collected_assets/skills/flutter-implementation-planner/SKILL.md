---
name: flutter-implementation-planner
description: >
  Generate phased, specification-driven implementation plans for Flutter mobile
  features. Creates structured plans with objectives, checkbox-format tasks,
  TDD steps, verification criteria, and risk assessments. Follows Flutter
  project conventions (lib/features/, domain/, data/, presentation/),
  build_runner workflow, and Clean Architecture patterns. Use when: planning
  a new feature, breaking down a complex task before implementation, creating
  a roadmap from requirements or wireframes, or writing a structured plan
  to hand off to another developer or agent.
version: 1.0.0
---

# Flutter Implementation Planner

Generate comprehensive, phased implementation plans for Flutter features.
Plans are description-only (no code), structured for TDD, and follow the
project's Clean Architecture conventions.

> **Planning-only skill.** This skill produces plans. It does not modify code,
> run tests, or create implementations.

---

## When to Use

- User explicitly requests a plan, roadmap, or implementation strategy
- Complex task requiring structured breakdown before implementation
- Handing a plan to another developer or implementation agent
- Risk assessment and alternative approach analysis before committing

---

## Planning Process

### Step 1: Analyse the Codebase

Before writing anything, explore the project to understand:

- Project structure (`lib/core/`, `lib/features/`, `lib/app/`)
- Existing patterns and conventions (state management, error handling, routing)
- Related features or modules that will be affected
- Existing tests and coverage approach
- `pubspec.yaml` dependencies already available

Use file reading to examine the codebase. Cite sources using `filepath:line` format in the plan.

**Flutter Template Standard Structure:**

```
lib/
├── core/
│   ├── config/        # AppConfig, Flavor
│   ├── errors/        # Failure, AppException
│   ├── logging/       # AppLogger, ErrorReporter
│   ├── network/       # ApiClient, interceptors
│   ├── result/        # Result<T>
│   ├── storage/       # AppPreferences
│   ├── theme/         # AppColors, AppSpacing, AppTheme
│   └── widgets/       # Core widget library
├── features/
│   └── [feature_name]/
│       ├── data/
│       │   ├── data_sources/
│       │   ├── models/        # DTOs with .fromJson / toEntity()
│       │   └── repositories/  # Repository implementations
│       ├── domain/
│       │   ├── entities/      # Pure Dart, no external deps
│       │   ├── repositories/  # Abstract interfaces
│       │   └── use_cases/     # Single-responsibility use cases
│       └── presentation/
│           ├── notifiers/     # Riverpod controllers
│           ├── providers/     # Provider declarations
│           └── screens/       # ConsumerWidget screens
├── bootstrap/         # bootstrap.dart
└── app/
    ├── app.dart
    ├── router/
    └── shell/
```

### Step 2: Clarify Requirements

Make no assumptions. Ask for clarification when any of the following are undefined:

- Target platform (iOS / Android / both)?
- State management approach already in use (Riverpod / BLoC)?
- Does this feature need offline support?
- Are there existing design tokens / widgets to use, or new ones needed?
- API: existing endpoint or needs to be defined?
- Estimated complexity: single screen, full feature, or cross-cutting change?

### Step 3: Identify Phases

Group work into logical phases:

1. **Foundation** — Domain entities, abstract repository interfaces, use case signatures
2. **Data Layer** — DTOs, data sources (remote/local), repository implementations
3. **State & Providers** — Riverpod controllers, provider declarations
4. **UI Layer** — Screens, widgets using core widget library
5. **Integration** — Route registration, navigation, error handling wiring
6. **Polish** — Localisation strings, empty/error states, accessibility

Not all phases are required for every feature. Small features may collapse into 2–3 phases.

### Step 4: Map Dependencies

For each phase, determine:

- Which phases must complete first
- Which phases can run in parallel
- The critical path through the implementation

### Step 5: Generate the Plan

Create the plan file at `docs/plans/YYYY-MM-DD-{feature-name}-v{N}.md`

Example: `docs/plans/2026-03-21-add-task-feature-v1.md`

---

## Plan Document Structure

Every plan MUST follow this structure exactly:

````markdown
# [Feature Name] Implementation Plan

> **For implementation agent:** Follow tasks in order. Each task must be
> committed before moving to the next. TDD: write the failing test first.

**Goal:** [One sentence describing what this builds and for whom]

**Architecture:** [2–3 sentences about the approach — which layers are affected,
which patterns are used, how it connects to existing code]

**Flutter Stack:**

- State management: [Riverpod / BLoC]
- Navigation: [GoRouter route path]
- Key packages: [list relevant packages from pubspec.yaml]

**Affected Files:** [list key files to be created or modified]

---

## Phase 1: [Phase Name]

### Task 1.1: [Task Title]

**Files:**

- Create: `lib/features/[feature]/domain/entities/[entity].dart`
- Modify: `lib/features/[feature]/domain/repositories/[repo].dart`

**Step 1.1.1: Write the failing test**
[Describe what the test should verify, which file it goes in]

**Step 1.1.2: Run test to verify it fails**
Command: `flutter test test/features/[feature]/domain/[file]_test.dart`
Expected: FAIL — [specific error message to expect]

**Step 1.1.3: Implement**
[Describe what needs to be implemented to make the test pass — in plain language, no code]

**Step 1.1.4: Run test to verify it passes**
Command: `flutter test test/features/[feature]/domain/[file]_test.dart`
Expected: PASS

**Step 1.1.5: Commit**

```bash
git add [relevant files]
git commit -m "feat([feature]): add [entity] domain entity"
```
````

---

## Verification Criteria

- [ ] [Criterion 1: Specific, measurable outcome]
- [ ] [Criterion 2: Specific, measurable outcome]
- [ ] All new code has unit or widget tests
- [ ] `flutter analyze` passes with no warnings
- [ ] `build_runner` output is up to date (`dart run build_runner build --delete-conflicting-outputs`)
- [ ] Feature is reachable via GoRouter navigation
- [ ] Light and dark mode tested visually
- [ ] No hardcoded strings (all in `l10n/`)

## Potential Risks and Mitigations

1. **[Risk Description]**
   Mitigation: [Specific strategy]

2. **[Risk Description]**
   Mitigation: [Specific strategy]

## Alternative Approaches

1. [Alternative 1]: [Brief description and trade-offs]
2. [Alternative 2]: [Brief description and trade-offs]

```

---

## Task Granularity Rules

Each step is one concrete action (2–5 minutes):

✅ Correct granularity:
- "Write the failing test for `LoginUseCase` with empty email"
- "Run the test to verify it fails"
- "Implement the empty email validation in `LoginUseCase.call()`"
- "Run the test to verify it passes"
- "Commit"

❌ Too coarse:
- "Implement the login feature"
- "Write all the tests"
- "Set up state management"

**TDD Sequence (repeat for every unit of logic):**
```

Write failing test → Verify it fails → Implement minimum code
→ Verify it passes → Refactor if needed → Commit

```

---

## Flutter-Specific Conventions

### Naming Conventions

| Type | Pattern | Example |
|---|---|---|
| Entity | `[Name].dart` (no suffix) | `task.dart` |
| DTO | `[name]_dto.dart` | `task_dto.dart` |
| Repository interface | `[name]_repository.dart` | `task_repository.dart` |
| Repository impl | `[name]_repository_impl.dart` | `task_repository_impl.dart` |
| Use case | `[verb]_[name]_use_case.dart` | `create_task_use_case.dart` |
| Controller | `[name]_controller.dart` | `task_list_controller.dart` |
| Screen | `[name]_screen.dart` | `task_list_screen.dart` |
| Test | mirrors source path in `test/` | `test/features/tasks/domain/...` |

### Code Generation Steps

When adding Freezed models or Riverpod generators, include this step:

```

Step X.X.X: Run build_runner
Command: dart run build_runner build --delete-conflicting-outputs
Expected: No errors. Generated files updated.

```

### Result Type Usage

All async operations that can fail return `Result<T>`:
```

Result.success(data) or Result.failure(Failure.network(...))

```
Never throw raw exceptions from repository implementations — catch and convert.

### Error Handling Chain

```

Exception (thrown in data layer)
→ mapErrorToFailure()
→ Failure (sealed class)
→ ResultFailure<T>
→ AsyncViewState.error(failure)
→ AsyncViewStateBuilder renders error UI

```

---

## Phase Templates

### Domain Phase Template

Tasks in order:
1. Define entity (pure Dart, Equatable, immutable)
2. Define repository interface (abstract, returns `Future<Result<T>>`)
3. Define use case (single public method, validates inputs, calls repository)
4. Write unit tests for entity and use case
5. Commit

### Data Phase Template

Tasks in order:
1. Define DTO with `fromJson` factory and `toEntity()` mapper
2. Define remote data source (calls `ApiClient`)
3. Define local data source (calls `AppPreferences` or Hive)
4. Implement repository (orchestrates remote + local, handles exceptions)
5. Write unit tests with mock data sources
6. Commit

### State & Providers Phase Template

Tasks in order:
1. Define Riverpod controller (`@riverpod` class extending `_$Name`)
2. Define provider declarations file
3. Add view state provider (`AsyncViewState<T>`)
4. Write unit tests for controller state transitions
5. Commit

### UI Phase Template

Tasks in order:
1. Create screen scaffold using `AppAppBar`, `Scaffold` with `extendBody: true`
2. Integrate with `AsyncViewStateBuilder`
3. Build data widget (list, card, form)
4. Handle empty state with `AppEmptyState`
5. Handle error state with `AppErrorState`
6. Write widget tests
7. Commit

### Route Registration Template

Tasks in order:
1. Add route path constant in `lib/app/router/app_routes.dart`
2. Add `GoRouteData` class in `lib/app/router/app_route_data.dart`
3. Run `dart run build_runner build --delete-conflicting-outputs`
4. Verify deep link navigates to screen
5. Commit

---

## Critical Requirements

- **ALWAYS use checkbox format** (`- [ ]`) for all verification criteria
- **NEVER use numbered lists** in the Implementation Plan task section — use `###` headings
- **NEVER write code snippets** in the plan — describe what needs to be done in plain language
- **ALWAYS cite file paths** for every task using `filepath:line` format
- **ALWAYS include TDD steps** (write failing test → verify fails → implement → verify passes → commit)
- **ALWAYS include build_runner step** when Freezed or Riverpod codegen is involved
- **NEVER assume** a pattern without confirming it exists in the codebase

---

## Boundaries

This is a **planning-only** skill:

✅ Research codebase and analyse structure
✅ Create phased plans and documentation
✅ Assess risks and propose alternatives
✅ Describe implementations in natural language
✅ Specify file paths and test commands

❌ Make actual code changes
❌ Modify files or create implementations
❌ Run tests or build commands
❌ Write code, code snippets, or code examples in plans

If the user requests implementation, switch to direct development mode or hand off the plan to an implementation agent.
```
