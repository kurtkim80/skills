# Design: [Feature Name]

Status: Draft

## Overview

[1-2 paragraphs describing the technical approach and why it fits the requirements.]

## Architecture

[Components, modules, services, and how data or control flows between them.]

## Data Model

[New or modified data structures, schemas, storage changes, or types.]

## Key Decisions

- **[Decision]:** [Rationale] _(Requirements: R1, R3)_
- **[Decision]:** [Rationale] _(Requirements: R2)_

## Interfaces / API Changes

- [Endpoint, function, event, CLI contract, or UI contract and how it changes] _(Requirements: R1)_

## Edge Cases & Error Handling

- [Scenario]: [How it's handled] _(Requirements: R3)_

## Requirements Coverage

| Requirement | Addressed by |
|---|---|
| R1 | [Section or decision] |
| R2 | [Section or decision] |
| R3 | [Section or decision] |

<!-- Every active requirement needs a row. If existing behavior already satisfies one, name
that behavior as its coverage rather than leaving it out. -->

## Testability

[Anything here that constrains how requirements can be verified — a boundary with no seam to
test against, an external dependency that cannot be faked, state that is hard to observe.
Note design changes made to keep a requirement verifiable.]

<!-- How each requirement is actually verified belongs in `test-plan.md`. -->

## Dependencies

- [Library / service / module and why it's needed]

## Risks / Open Questions

- [Risk, tradeoff, or unresolved question]
