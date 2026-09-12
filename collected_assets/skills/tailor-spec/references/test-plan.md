# Test Plan: [Feature Name]

Status: Draft

## Scope

[What this plan verifies and what it deliberately leaves unverified.]

<!-- Out-of-scope items in `requirements.md` have no IDs and no rows here — repeat any a
reader might expect to find. -->

## Verification Matrix

<!-- `R<n>` rows are the active requirement IDs, one row each. `S<n>` rows are seams the
design introduces that no requirement names, where a break would otherwise surface as an
acceptance failure that does not say which component broke. Status is filled during
implementation, not while planning. -->

| ID | Level | Mode | Means | Observable evidence | Status |
|---|---|---|---|---|---|
| R1 | Acceptance | Automated | [Test name] | [What is observed] | [ ] |
| R2 | Integration | Automated | [Test name] | [What is observed] | [ ] |
| R3 | Acceptance | Manual | [Procedure below] | [What is observed] | [ ] |
| S1 | Integration | Automated | [Test name] | [What is observed] | [ ] |

## Test Environment & Data

- **Fixtures / seed data:** [What state must exist before tests run]
- **External dependencies:** [Real, stubbed, or faked — and why]
- **Environment:** [Local, CI, staging, or a specific configuration]

## Manual Procedures

<!-- One per `Mode: Manual` row. Delete this section if every row is automated. -->

### [R3] — [Short name]

1. [Step]
2. [Step]

**Expected:** [Observable result that closes the requirement]

## Non-Functional Verification

- [Requirement ID]: [Threshold] measured by [method]

## Feature-Triggered Reviews

<!-- Only reviews this feature triggers that a routine change would not — a new auth path
needing a threat model, say. Standing gates belong to the repo's rule files and run in CI. -->

- [What about this feature triggers it] — [review needed, and who performs it]

## Regression Risk

[Existing behavior this feature could break, and what already covers it. Name the suites that
must still pass.]

## Gaps & Deferrals

<!-- Delete if empty. Each entry needs the user's agreement. -->

- [Requirement ID or seam]: [Blocker] — [proposed follow-up]
