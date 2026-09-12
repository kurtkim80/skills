# EARS Format

The single format for acceptance criteria. Both the compact and full paths use it. Do not
invent a variant, reword the keywords, or switch format between specs.

| Pattern | Shape |
|---|---|
| Ubiquitous | THE SYSTEM SHALL [response] |
| Event | WHEN [trigger] THE SYSTEM SHALL [response] |
| State | WHILE [ongoing state] THE SYSTEM SHALL [response] |
| Conditional | IF [condition] THEN THE SYSTEM SHALL [response] |
| Optional feature | WHERE [feature is included] THE SYSTEM SHALL [response] |

Rules:

- One observable behavior per criterion
- `SHALL` — not "should", "will", or "must"
- The subject is the system, not a function, class, or file
- The trigger and the response are both observable from outside the system
- If a criterion needs "and" to join two behaviors, it is two criteria

When a requirement genuinely does not fit any pattern — a constraint, a non-functional
threshold — write it as plain prose with the same ID scheme rather than forcing it.
