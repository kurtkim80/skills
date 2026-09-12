---
name: tailor-spec
description: "Spec-driven workflow for shaping a feature before coding. Use when the user wants to plan a feature, write or update a spec, define requirements, work through design, plan verification, break work into tasks, or references `.specs/`."
---

# Spec-Driven Development

Turn a fuzzy feature request into a concrete plan in `.specs/<feature-name>/`.

If a spec already exists, read it first, check its `Status` lines, and continue from the current phase instead of recreating everything.

Pick a short kebab-case feature name describing the capability — `user-auth`, `billing-export`, `search-filters` — and work under `.specs/<feature-name>/`.

## Choosing the Weight

Two shapes. Decide which, and say so in a sentence. The user should never have to pick process vocabulary.

**Compact** — one `compact-spec.md`, one gate. This is the default. Start here unless the work
escalates it.

**Full** — four documents, three review gates. Escalate when any of these hold:

- spans components that are deployed or owned separately — several files inside one deployable unit does not count
- breaks compatibility on a public contract: API, CLI, schema, event — a backward-compatible addition does not count: an optional flag, a new field, an endpoint alongside the existing one
- data migration or irreversible state change — a migration that only adds, and that the feature can run without, does not count
- auth, permissions, secrets, or PII — the feature decides or stores it, rather than passing through what an existing mechanism already decided
- new external dependency or integration — a new service, protocol, or vendor, rather than another call against one already in use
- rollback is hard, slow, or unproven — the change would outlive a revert, not merely that nobody has reverted this area before

When a trigger is borderline, stay compact and say which one you weighed and why it fell short.
A compact spec can be promoted mid-flight; a full one spent on small work is already spent.

The first review gate covers the weight as well as the draft. If the user says it is the wrong
shape, change shape before continuing.

If the user asks for a specific weight, or for a single phase, do that instead.

A compact spec that outgrows itself mid-flight gets split into the full set. Say why. Keep the
requirement IDs and their wording for every criterion whose meaning still holds, since
everything downstream references them; where the promotion changed what a criterion actually
demands, withdraw the old ID and add a new one rather than editing it in place. Everything
else was approved against a smaller understanding of the work, so carry it across only where
it still holds, and open the expanded documents at `Draft` for review rather than inheriting
the compact spec's approval.

The reverse is rarer but allowed: full-path documents still at `Draft`, on work that turns out
to hold no trigger, collapse into a single `compact-spec.md`. Anything already `Approved` stays
where it is — demoting past an approval throws away review the user already gave.

## Workflow

```text
compact:  preflight -> compact-spec.md -> review -> implement -> verify
full:     preflight -> requirements.md -> review -> design.md + test-plan.md -> review -> tasks.md -> review -> implement -> verify
```

Review before implementation because it reduces rework and exposes mistakes early. Complete one phase at a time and stop for approval before the next. On the full path, do not merge phases into a single draft — design and test plan are the one exception, written and reviewed together. The compact path is one phase by design, not a merged full path.

Do not start implementation unless the user has asked for it or approved moving past planning.

## Repo-Rule Preflight

Run this once, before the first phase is drafted — not again for each phase. Re-run it when
resuming a spec in a later session, or when repo guidance may have changed since.

- Read agent-native instruction files when present: `AGENTS.md`, `CLAUDE.md`, or the equivalent for the active tools
- Note standing verification the project already requires — SAST, SCA, lint, coverage thresholds, mandatory review — and treat it as in force rather than restating it in the spec
- Read related documents that could change the spec: `README`, `CONTRIBUTING`, architecture notes, existing approved specs
- Prefer repo-local instructions over generic assumptions
- Respect custom rule files the repo already uses; do not introduce a new constitution convention
- Surface conflicts between rule sources instead of silently picking one

Then check whether the request is missing anything that would materially change the spec — goals and success criteria, scope boundaries, constraints and integrations, edge cases and failure handling. Ask only what the preflight and the existing spec cannot answer. If the prompt is already clear, proceed.

## Requirement IDs

Every acceptance criterion gets a stable `R<n>` ID. Design decisions, verification rows, and tasks reference these IDs, so a requirement change points straight at the work it affects.

- Never renumber an approved ID. Append new criteria; mark removed ones `(withdrawn)`
- A withdrawn criterion keeps its ID but stops being active — no coverage, no verification row, no task
- Every rule below about "every requirement ID" means every active one
- Seams the design invents that no requirement names get `S<n>` IDs in the verification matrix

Acceptance criteria are written in the EARS patterns in `references/ears.md`. That format is
fixed — both paths use it, and a spec never defines its own variant.

## Status

Every spec document carries a status line under its title:

```text
Status: Draft
```

Every document moves `Draft` → `Approved`: set `Approved` when the user approves that phase.
On resume, read the status and continue — never re-ask for approval on a phase already marked
`Approved`.

Two further states belong only to the document that owns the task list — `tasks.md` on the
full path, `compact-spec.md` on the compact one. No other document goes past `Approved`.

| Status | Set when |
|---|---|
| `Implemented` | Every task is checked and its unit tests pass |
| `Verified` | Every active `R<n>` row and every planned `S<n>` row is closed, and the standing gates are green |

A deferral does not earn `Verified`. A document with an open row in Gaps & Deferrals stays
`Implemented` until that row closes or the obligation is formally dropped — an `R<n>` by the
user withdrawing the criterion, an `S<n>` by an approved revision to the design or test plan
that removes the seam. Both are scope changes and need the user's agreement. `Verified` must
never mean "verified except for the parts we skipped."

Progress itself lives in the task checkboxes and the matrix `Status` column. The document
status is a rollup of those, not a second place to record them.

## Compact — one document

Create `.specs/<feature-name>/compact-spec.md` using `references/compact-spec.md`. One
document covering goal, acceptance criteria, approach, verification, and tasks — the same
ground the four full-path documents cover, in one place.

Everything the full path requires still holds, at lower fidelity — testable criteria with IDs,
approach decisions tagged with the IDs they serve, a verification row per active ID, unit
tests owned by the task that produces the code, written steps for anything checked manually,
and an explicit deferral for anything that cannot be verified as planned.

Stop and ask: "Does this look right? Should I start implementing?"

## Full — Phase 1: Requirements

Use `references/requirements.md`. Focus on user value and externally visible behavior.

- Capture who benefits, what they need, and why it matters
- Write acceptance criteria that are testable and specific
- Include edge cases, failure modes, and explicit out-of-scope items
- Resolve ambiguity before moving on; call out assumptions the user has not confirmed

Stop and ask: "Does this look right? Should I proceed to design?"

## Full — Phase 2: Design and Test Plan

Only after requirements are approved. Use `references/design.md`.

- Describe the technical approach: components, interfaces, data flow, constraints
- Tie decisions back to requirement IDs and record the tradeoffs
- Fill the coverage table; every active ID is addressed. A criterion the feature no longer needs is withdrawn in requirements review, not excluded here; one that existing behavior already satisfies records that behavior as its coverage
- Cover data model changes, integration points, dependencies, error handling
- Call out risks, open questions, and decisions needing user confirmation

Then `references/test-plan.md`. It belongs in this phase because deciding how a requirement will be observed often changes the design that has to support it.

- Give every active requirement ID a matrix row
- Choose the level from the boundary the requirement claims, not from what is easy to write
- Requirements describe externally observable behavior, so they close at acceptance or integration level; a unit test is supporting evidence and never closes a requirement
- Set mode independently of level — a manual check is still acceptance or integration scoped
- State the observable evidence, not the name of the code under test
- Add `S<n>` rows for seams the design invents that no requirement names, so a break localizes to a component instead of surfacing as an acceptance failure with no cause
- Write real steps for anything verified manually
- Record thresholds and measurement methods for non-functional requirements
- Surface anything that cannot be verified, with the reason, instead of inventing a row

Feed anything that constrains verification back into the design's testability section.

Review both documents together. Stop and ask: "Does this design and test plan work? Should I proceed to tasks?"

## Full — Phase 3: Tasks

Only after the design and test plan are approved. Use `references/tasks.md`.

- Break work into ordered, implementable tasks that produce visible progress
- Tag each task with the requirement IDs it serves; every active ID appears at least once
- Give every code-producing task its own unit test sub-step, naming the behavior it pins down
- Derive acceptance and integration work from `test-plan.md`: every `Automated` row needs a task that produces it, plus tasks for the fixtures or environment it depends on
- Include migrations, docs, or rollout work when they matter
- Note dependencies and sequencing so implementation does not stall later

Unit tests are mandatory and belong to the task that produces the code — not deferred into a testing task at the end, and not required first; the order within a task is the implementer's choice. A task is not complete until its tests pass.

Do not restate the verification matrix here. It lives in `test-plan.md`.

Stop and ask: "Does this plan look good? Should I start implementing?"

## Implementation and Verification

Only after approval. Follow tasks in order, marking each `- [x]` when done. If implementation reveals missing or contradictory spec details, stop and surface the gap instead of silently deviating.

Each task closes when its own unit tests pass. That is not the finish line. Before reporting the feature complete, work through the verification matrix and fill its Status column:

- Check each requirement against what actually got built, not against the task list
- Run the means the plan names, at the level it names; do not substitute a lower level because it passes and the real check is not written yet
- Record the observable evidence, and run the manual procedures rather than assuming them
- Close the `S<n>` rows too; they are planned work, not optional
- Report failures plainly, with the output, instead of quietly widening the requirement
- If a requirement cannot be verified as planned, move it to the gaps section and let the user decide whether to defer it or revise the criteria

The project's standing gates still apply. Run what the rule files say to run locally, and do not report a feature complete while its pipeline checks are failing. Their results belong in the pipeline, not copied into the spec.

A feature is done when every task's unit tests pass, the standing gates are green, and every active `R<n>` row and planned `S<n>` row is closed. Set the task-owning document to `Verified`. Any deferred requirement or seam leaves the feature at `Implemented` — say so plainly rather than reporting it complete.

## Working with Existing Specs

- Read the existing documents and their status lines before editing
- Re-run the preflight if repo guidance may have changed
- Preserve `Approved` decisions unless the user asks to revisit them
- If newly discovered repo instructions conflict with approved decisions, surface the conflict before rewriting
- Update only the phases that need changes, but keep cross-file consistency
- If requirements change, follow the affected IDs into design, test plan, and tasks and update every place they appear instead of leaving them stale
- A new or reworded requirement needs a verification row before tasks are touched

Changing what a document *specifies* resets its status — a new or reworded criterion, a
different approach, an added or altered matrix row. That phase drops to `Draft` and needs
approval again, along with every downstream document the change propagates into, and a
task-owning document at `Implemented` or `Verified` drops with them: a feature cannot stay
`Verified` against criteria that did not exist when it was verified. Re-close only the
affected rows; rows the change does not touch keep their recorded evidence.

Recording progress is not a specification change. Ticking a task box, recording observed
evidence in the matrix and updating its `Status` cell, and advancing the document's status
line itself are the workflow running as designed, and reset nothing.

## Repo Integration

The spec is committed with the code it describes, and the change that implements it points back at the spec so reviewers can read the intent behind the diff.

- Reference the spec path in the pull request or change description
- Record the tracker issue in the spec when the project uses one

Everything else about how changes land — branch naming, commit format, PR templates, review requirements — belongs to the project. Take it from the rule files found during the preflight; do not invent a convention the repo has not chosen.

## Quality Bar

Replace every placeholder with concrete detail from the request, and delete sections that do not apply rather than leaving them holding a placeholder. An empty section reads as unfinished work and hides which parts were genuinely considered.

The templates carry authoring notes as HTML comments. Delete them once they have been
followed — a committed spec contains the spec, not the instructions for writing one.

Good specs are specific enough that another engineer could implement from them, honest about assumptions and open questions, scoped so the work is achievable, and consistent across every document.

## Rules

- Spec files are committed alongside code
- One spec per feature, in its own folder
