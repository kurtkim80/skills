# Spec: [Feature Name]

Status: Draft

## Goal

As a [type of user] I want [goal] so that [value].

- **Current pain point:**
- **Out of scope:**

## Acceptance Criteria

- **R1:** [criterion]
- **R2:** [criterion]
- **R3:** [criterion covering an invalid or edge case]

## Approach

[The technical approach in a few sentences: what changes, where, and why it fits.]

- **[Decision]:** [Rationale] _(R1, R3)_
- **[Data model change, new dependency, or constraint worth recording]** _(R2)_

## Verification

<!-- Status is filled during implementation, not while planning. -->

| ID | Level | Mode | Means | Observable evidence | Status |
|---|---|---|---|---|---|
| R1 | Acceptance | Automated | [Test name] | [What is observed] | [ ] |
| R2 | Acceptance | Automated | [Test name] | [What is observed] | [ ] |
| R3 | Acceptance | Manual | [Procedure below] | [What is observed] | [ ] |

### Manual Procedures

<!-- One per `Mode: Manual` row. Delete this section if every row is automated. -->

**[R3] — [Short name]**

1. [Step]
2. [Step]

**Expected:** [Observable result that closes the requirement]

### Gaps & Deferrals

<!-- Delete if empty. Each entry needs the user's agreement. -->

- [Requirement ID]: [Blocker] — [proposed follow-up]

## Tasks

- [ ] 1. [Implementation task] _(R1, R2)_
  - [ ] Unit tests for [component] — [behavior they pin down]
- [ ] 2. [Implementation task] _(R3)_
  - [ ] Unit tests for [component] — [behavior they pin down]
- [ ] 3. [Tests for the `Automated` matrix rows] _(R1, R2)_

<!-- Manual rows get no task; they are executed through their procedures during verification. -->

## Assumptions / Open Questions

- [Assumption or unanswered question that could affect implementation]
