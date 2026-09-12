# tailor-spec

An agent-agnostic skill that turns fuzzy feature requests into concrete implementation plans.
Works with any coding agent that follows a SKILL.md / AGENTS.md convention (Claude Code,
Cursor, and others).

## What it does

The agent picks the weight of the spec from the shape of the work, and says which it chose:

- **Compact** — one `compact-spec.md`, one approval gate. The default, and where a borderline
  call lands.
- **Full** — requirements, design + test plan, tasks. Four documents, three gates. Escalated to
  when the change spans separately deployed or owned components, breaks compatibility on a public
  contract, migrates data, decides or stores auth or PII, adds an external dependency or
  integration, or would outlive a revert. Every trigger carries a limit that keeps it from
  swallowing ordinary work — a backward-compatible addition is not a break, several files inside
  one deployable unit is not multiple components, and one more call against a service already in
  use is not a new integration.

A compact spec that outgrows itself gets split into the full set, keeping its requirement IDs;
the expanded documents go back to `Draft` for review rather than inheriting the approval. The
reverse runs only while the full documents are still `Draft`, so an approval already given is
never thrown away.

Acceptance criteria carry stable `R<n>` IDs, and every design decision, verification row, and
task references them — so a requirement change points straight at the work it affects. Every
document tracks `Status: Draft | Approved`, so a spec picked up days later resumes where it
left off instead of re-asking for approvals; the document owning the task list carries
`Implemented` and `Verified` on top of that.

Verification is planned before implementation, and each requirement is matched to the level
that can actually close it. A passing unit test is not evidence that a requirement holds at
the system boundary — unit tests close a *task*, the verification matrix closes a
*requirement*, and both are required.

Once, before the first phase is drafted, a repo-rule preflight reads `AGENTS.md`, `CLAUDE.md`,
or equivalent agent-native guidance so specs align with local conventions — re-run when a spec
is resumed later or repo guidance changes, not on every phase.

Output lands in `.specs/<feature-name>/` and is committed alongside the code.

## The process

The full path is a V. The left arm decomposes the feature; the right arm closes it. Each level
is checked by the level facing it, at the boundary that level actually claims — not at whatever
is easiest to write.

```text
  ↓ SPECIFY                         VERIFY ↑

  requirements.md ─────────────────────────→ R<n> rows in the matrix
  externally visible behaviour               acceptance or integration level
    \                                    /
      design.md + test-plan.md ────────→ S<n> rows in the matrix
      components, decisions, seams       seams no requirement names
        \                            /
         tasks.md ─────────────────→ unit tests
         ordered work                close a task, never a requirement
           \                      /
            ─── implementation ───
```

Every row on the right arm exists before implementation starts. `test-plan.md` is written beside
`design.md` because deciding how a requirement will be observed often changes the design that has
to support it; the unit tests come one level lower, owned by the task that produces the code.

Each level of the left arm ends in an approval gate recorded on the document's `Status` line. The
repo-rule preflight runs once before the arm begins, and the project's standing gates sit outside
the V entirely.

The compact path is the same V folded into one document — the same levels and the same pairings
at lower fidelity, with one approval gate instead of three.

## Structure

```text
tailor-spec/
├── SKILL.md                  # Workflow, phase rules, and the full ruleset
├── README.md                 # This file
└── references/               # Spec templates and optional repository-guidance starter
    ├── AGENTS.md             # Optional starting point when a repository has no agent guidance
    ├── ears.md               # The acceptance-criteria format, defined once for both paths
    ├── compact-spec.md       # Compact path, whole spec: goal, criteria, approach, verification, tasks
    ├── requirements.md       # Full path: problem statement, criteria, out of scope
    ├── design.md             # Full path: architecture, data model, decisions, coverage, testability
    ├── test-plan.md          # Full path: verification matrix, environment, manual procedures, gaps
    └── tasks.md              # Full path: ordered plan with per-task unit tests
```

Each template produces a file of the same name under `.specs/<feature-name>/`. Acceptance
criteria come from `ears.md` on both paths, so the format cannot drift between them.

## What belongs in your repo, not in a spec

Standing verification is a project decision, so the skill deliberately does not define it:
SAST, SCA, dependency and license scanning, lint, coverage thresholds, mandatory review,
branch protection, CI stages, commit and PR conventions.

Document these in your `AGENTS.md` / `CLAUDE.md` and enforce them in CI. The preflight reads
those files before any phase is drafted, so they are respected without the skill hardcoding
tools it cannot see or run.

If a repository has no agent-native guidance, [`references/AGENTS.md`](references/AGENTS.md) is
an optional, standalone starting point. It separates reusable working rules from a project-command
section that must be filled with the repository's actual commands and thresholds. The skill does
not depend on this example: its preflight works with whatever agent-native guidance the target
repository already uses.

The reason for the split is enforcement: a spec cannot make a scan happen. Listing gates it
does not control turns a spec into decoration that reads like authority — and an agent can
tick "SAST: passed" having run nothing. What a spec *can* own is the per-feature case: a
review this change triggers that a routine change would not, such as a new auth path needing
a threat model. That goes in the test plan.

## Triggering

The skill activates when the user asks to plan a feature, write or update a spec, define
requirements, work through design, plan verification, break work into tasks, or references
`.specs/`.
