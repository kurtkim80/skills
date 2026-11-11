# Spec: [Feature Name]

Status: Draft

## Intent

<!-- For infrastructure or platform work, state the capability instead: the system needs to
[capability] so that [operational value]. -->

As a [type of user]
I want [goal]
So that [reason / value]

- **Current pain point:**
- **Desired outcome:**
- **Out of scope:**

## Acceptance Criteria

- **R1:** [criterion]
- **R2:** [criterion]
- **R3:** [criterion covering an invalid or edge case]

## Design

[The technical approach in a few sentences: what changes, where, and why it fits.]

- **[Decision]:** [Rationale] _(R1, R3)_
- **[Data model change, new dependency, or constraint worth recording]** _(R2)_

## Risks

<!-- Delete if nothing here could plausibly go wrong beyond the criteria above. Tag the IDs a
risk threatens, when it threatens any. -->

- [Risk or regression exposure] — [mitigation, or accepted and why] _(R2)_

## Verification

<!-- The proof the plan commits to. Status is filled during implementation, not while planning. -->

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

## Plan

- [ ] 1. [Implementation task] _(R1, R2)_
  - [ ] Unit tests for [component] — [behavior they pin down]
- [ ] 2. [Implementation task] _(R3)_
  - [ ] Unit tests for [component] — [behavior they pin down]
- [ ] 3. [Tests for the `Automated` matrix rows] _(R1, R2)_

<!-- Manual rows get no task; they are executed through their procedures during verification. -->

## Assumptions / Open Questions

- [Assumption or unanswered question that could affect implementation]
