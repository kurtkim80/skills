# tailor-spec

An agent-agnostic skill that turns fuzzy feature requests into concrete implementation plans.
Works with any coding agent that follows a SKILL.md / AGENTS.md convention (Claude Code,
Codex, Agy, Cursor, and others).

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

## Installation

The skill is a folder: `SKILL.md` plus `references/`. Install it by placing that folder where
your agent loads skills from.

Clone the repository into your agent's skills directory, either per user (every project) or
per repository (shared with a team by committing it):

```bash
git clone https://github.com/leonardopordeus/tailor-spec.git <skills-dir>/tailor-spec
```

| Agent | Per-user `<skills-dir>` | Per-repository `<skills-dir>` |
|---|---|---|
| Claude Code | `~/.claude/skills` | `.claude/skills` |
| Codex | `~/.agents/skills` | `.agents/skills` |
| Cursor | `~/.agents/skills` or `~/.cursor/skills` | `.agents/skills` or `.cursor/skills` |
| Agy (Antigravity) | `~/.gemini/config/skills` | `.agents/skills` |

`.agents/skills` is read by Codex, Cursor, and Agy, so it is the one location to use if you want a
single install for all three. Claude Code reads only `.claude/skills`; Cursor also reads that one.
Agy still honors the legacy `.agent/skills` and `~/.gemini/antigravity/skills`. These locations
change between versions, so confirm against your agent's documentation. On Windows, `~` is
`%USERPROFILE%`. Start a new session so the skill is picked up,
and check that it shows up in the skills list.

**Any other agent** — copy the folder into the agent's skills directory, or point its rule file
(`AGENTS.md`, Cursor rules, or equivalent) at `SKILL.md`. The skill reads only its own
`references/` and the target repository, so it needs no other setup.

**Optional — repository guidance.** The preflight reads the target repository's `AGENTS.md` /
`CLAUDE.md`. If it has none, [`references/AGENTS.md`](references/AGENTS.md) is a starting point:
copy it to the repository root and fill in the *Project Commands* section with real commands.

## Usage

Ask for what you want in plain language. Naming the skill is optional; agents with slash-command
or mention syntax for skills (for example `/tailor-spec`) can invoke it explicitly.

```text
> Plan a CSV export for the invoices list. Users filter the list and want to download what they see.
```

The agent runs the preflight, asks only what the repository and the request leave open, then
says which weight it picked and why:

```text
Compact: one screen, one endpoint inside the existing API, no new dependency, no auth change.
I weighed "public contract" — the endpoint is new and alongside the existing ones, so it is not a break.
Draft at .specs/invoice-csv-export/compact-spec.md. Does this look right? Should I start implementing?
```

An excerpt of the draft:

```markdown
# Spec: Invoice CSV Export

Status: Draft

## Intent

As a finance user
I want to download the invoices I have filtered as CSV
So that I can reconcile them in a spreadsheet without retyping

- **Current pain point:** invoices are copied by hand from the screen
- **Desired outcome:** one click exports exactly the filtered rows
- **Out of scope:** scheduled exports, formats other than CSV

## Acceptance Criteria

- **R1:** WHEN the user selects Export THE SYSTEM SHALL download a CSV containing exactly the rows matching the active filters
- **R2:** IF no rows match the active filters THEN THE SYSTEM SHALL disable Export
- **R3:** THE SYSTEM SHALL return the export of 10,000 rows within 5 seconds

## Verification

| ID | Level | Mode | Means | Observable evidence | Status |
|---|---|---|---|---|---|
| R1 | Acceptance | Automated | `export_matches_filters` e2e | Downloaded rows equal the filtered list | [ ] |
| R2 | Acceptance | Automated | `export_disabled_when_empty` e2e | Button disabled with an empty result | [ ] |
| R3 | Integration | Automated | Load test on the export endpoint | p95 under 5 s at 10,000 rows | [ ] |
```

From there, the conversation drives the workflow:

| You say | The agent |
|---|---|
| "Looks good, implement it." | Sets `Status: Approved`, works through the plan, closes the matrix, and ends at `Verified` — or at `Implemented`, saying which row is still open |
| "This touches the billing schema too." | Weighs the migration trigger and, if it holds, promotes to the full path with the IDs kept and the documents back at `Draft` |
| "Use the full process." / "Only write the requirements." | Follows the requested weight or phase instead of choosing |
| "Continue the invoice export spec." | Reads `.specs/invoice-csv-export/`, re-runs the preflight, and resumes from the current `Status` without re-asking for approvals |

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

## Relation to the AI-Native SDLC and/or Agentic Development Lifecycle (ADLC)

The vocabulary follows Anthropic's [AI-Native SDLC Playbook][playbook], where each stage
commits an artifact the next stage reads and a human approves it before work moves on. The
skill covers the playbook's **Plan**, **Design**, **Build**, and **Test** stages for a single
feature. **Deploy** and **Maintain** stay with the project's own process.

| Playbook artifact | Compact — section of `compact-spec.md` | Full — document |
|---|---|---|
| `intent.md` — what and why | `## Intent` | `requirements.md` → `## Intent` |
| `spec.md` — requirements | `## Acceptance Criteria` | `requirements.md` → `## Acceptance Criteria` |
| `spec.md` — design | `## Design` | `design.md` |
| `plan.md` — risks | `## Risks` | `design.md` → `## Risks / Open Questions` |
| `plan.md` — proof | `## Verification` | `test-plan.md` |
| `plan.md` — order of work | `## Plan` | `tasks.md` |

Compact is the default, so most features carry the playbook's three artifacts as sections of one
document behind one approval gate. Promotion to the full path splits those sections into
separate documents along the same lines.

Where the skill is stricter than the playbook:

- **Traceability.** Every design decision, risk, verification row, and task references a stable
  `R<n>` ID, so a requirement change points straight at what it affects.
- **Proof is planned before implementation.** A requirement closes at acceptance or integration
  level, never on a unit test, and `S<n>` rows cover seams no requirement names.
- **Divergence stops the work.** Where the playbook updates `plan.md` in the same commit as the
  diverging code, the skill surfaces the gap first, and changing what a document specifies sends
  it back to `Draft` for approval.

The skill also follows the playbook's principle that controls belong in code: skills are
advisory, so standing gates are enforced by the repository's hooks and CI rather than restated in
a spec (see [What belongs in your repo](#what-belongs-in-your-repo-not-in-a-spec)).

[playbook]: https://claude.com/resources/articles/the-ai-native-sdlc-playbook

## Structure

```text
tailor-spec/
├── SKILL.md                  # Workflow, phase rules, and the full ruleset
├── README.md                 # This file
└── references/               # Spec templates and optional repository-guidance starter
    ├── AGENTS.md             # Optional starting point when a repository has no agent guidance
    ├── ears.md               # The acceptance-criteria format, defined once for both paths
    ├── compact-spec.md       # Compact path, whole spec: intent, criteria, design, risks, verification, plan
    ├── requirements.md       # Full path: intent, criteria, out of scope
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
