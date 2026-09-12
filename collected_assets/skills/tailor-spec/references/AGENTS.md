# AGENTS.md

<!--
Suggested starting point for a repository's agent guidance. This file does not govern the
tailor-spec skill repository. Before copying it into another repository, replace every
placeholder, remove sections that do not apply, and add stable project-specific rules that an
agent cannot reliably infer from the codebase.
-->

Repository guidance for coding agents. Higher-priority system, developer, or user instructions
override this file. More deeply nested agent guidance overrides it within that subtree.

## Scope

- Follow the conventions already established in the area being changed.
- Keep changes focused on the requested outcome; do not clean up unrelated code.
- Preserve existing behavior and public contracts unless the task explicitly changes them.

## Working Principles

- Apply `KISS`: prefer the simplest solution that satisfies the requirement.
- Apply `DRY`: remove real duplication, but do not abstract too early.
- Apply SOLID principles pragmatically, not mechanically.
- Prefer small, focused functions and modules over broad abstractions.

## Implementation

- Prefer clear names and straightforward control flow over clever abstractions.
- Follow the project's existing type, error-handling, logging, and dependency patterns.
- Add dependencies only when they provide clear value and fit the project's existing policy.
- Never commit secrets or place credentials in source code, tests, fixtures, logs, error messages,
  examples, or documentation. Report suspected secrets by location without reproducing the value.
- Do not edit generated files directly when the repository provides a generation workflow.
- Comment intent, constraints, or non-obvious decisions rather than restating the code.

## Testing

- Use TDD when adding or fixing behavior: write a failing test, make it pass, then refactor.
- Add or update tests when behavior changes and the behavior can reasonably be exercised
  automatically.
- For a reproducible bug, add a regression test that fails without the fix when practical.
- Keep tests focused on observable behavior rather than implementation details.
- Use the project's established fixtures, fakes, or test helpers for external I/O.
- Treat a task as complete only after the tests associated with that task pass.

## Verification and Quality Gates

- Treat the nearest applicable repository guidance, documented project scripts, and CI
  configuration as the source of truth for required checks.
- When current design guidance is available, review the implementation against the applicable
  approved specification, architecture documentation, ADRs, or design-system rules. Report any
  divergence instead of silently redefining the design.
- During implementation, run the smallest relevant checks for fast feedback.
- Before reporting work complete or marking a specification `Verified`, run every documented,
  locally runnable gate applicable to the changed scope. These may include tests, build or
  typechecking, linting, formatting, coverage, security, or dependency checks.
- Respect existing thresholds and policies. Do not weaken tests, snapshots, thresholds, or
  checks merely to make verification pass.
- Run every configured security and supply-chain gate applicable to the changed scope, including
  SAST, SCA, secret scanning, and license checks when the repository defines them.
- Do not suppress, exclude, or downgrade a finding merely to make a gate pass. Fix it or report it
  for explicit acceptance according to the repository's security policy.
- Do not claim a check passed unless it was actually run successfully.
- If a required check cannot be run, report the exact command, the blocker or failure, and what
  remains for CI or a maintainer to verify.
- Summarize the commands run and their outcomes when handing off the work.

### Project Commands

<!-- Replace every placeholder. Delete commands and categories that do not apply. -->

- **Tests:** `[command]`
- **Build / typecheck:** `[command]`
- **Lint / format check:** `[command]`
- **Design conformance:** `[review command or procedure, with applicable documents]`
- **Coverage:** `[command and required threshold]`
- **SAST:** `[static application security testing command or CI job]`
- **SCA / dependency audit:** `[dependency vulnerability command or CI job]`
- **Secret scanning:** `[credential and secret scanning command or CI job]`
- **License compliance:** `[command or CI job]`
- **Other required gates:** `[IaC, container, migration, or project-specific checks]`

## Documentation and Output

- Update documentation when behavior, interfaces, setup, or operational steps change.
- Keep user-facing messages and command output clear, concise, and actionable.
- Preserve useful existing comments and documentation unless they are wrong or stale.

## Maintaining This File

- Keep these instructions short, consistent, and enforceable.
- Record stable repository decisions, not preferences an agent can infer from nearby code.
- Keep concrete commands and thresholds current when project tooling changes.
