---
name: mobile-product-leadership
description: >
  Unified product and engineering leadership toolkit for mobile application teams.
  Covers OKR cascade generation, sprint planning, RICE prioritisation, technical
  debt management, code review culture, DORA metrics, team scaling, competitive
  analysis, product vision, and stakeholder communication. Use when: planning
  sprints, defining OKRs, prioritising features, conducting retrospectives,
  making technology or architecture decisions, mentoring developers, writing
  product roadmaps, performing competitive analysis, or scaling a 2–10 person
  mobile-first team.
version: 3.0.0
merged-from:
  - mobile-product-leadership v2.0.0
  - product-strategist v1.0.0
  - product-manager-toolkit v1.0.0
---

# Mobile Product Leadership

> Unified toolkit for technical and product leadership on a mobile application team.
> Covers the full loop: strategy → planning → execution → measurement → iteration.

---

## Scope

This skill addresses two interlocking responsibilities that, on small mobile teams,
typically belong to the same person: **product strategy** (what to build and why)
and **engineering leadership** (how to build it reliably and sustainably).

Use the sections independently as needed. The OKR and prioritisation sections are
useful without touching the sprint or code-review sections, and vice versa.

---

## 1. Product Vision and OKR Cascade

### Vision Statement Template

```
For [target user] who [has this problem],
[App name] is a [category] that [key benefit].
Unlike [primary alternative], our product [differentiator].
```

### OKR Cascade (Company → Product → Team)

OKRs align the team to business goals. Cascade top-down, build bottom-up with
team input.

```
Company OKR
└── Product OKR (contributes to company goal)
    └── Team OKR (engineering / design / QA level)
        └── Individual Sprint Goals
```

**OKR quality checklist.** Objectives must be qualitative and inspiring, achievable
within a quarter, and meaningful to the mobile product. Key Results must be
measurable with a specific number, owned by a named person, and set at a level
where a 70% hit rate is considered healthy.

### Strategy Templates by Focus Area

**Growth:** Become the go-to app for [target segment]. KRs: DAU target, App Store
rating ≥ 4.5, D30 retention improvement.

**Retention:** Make users unable to imagine their day without the app. KRs: D7
retention improvement, session length increase, push opt-in rate target.

**Revenue:** Reach sustainable unit economics. KRs: LTV:CAC ≥ 3:1, trial-to-paid
conversion target, annual plan uptake percentage.

**Operational:** Ship faster without breaking things. KRs: lead time under 3 days,
change failure rate below 15%, MTTR for critical bugs under 4 hours.

---

## 2. Feature Prioritisation

### RICE Framework

```
Score = (Reach × Impact × Confidence) / Effort

Reach:      Number of users affected per quarter
Impact:     massive=3x / high=2x / medium=1x / low=0.5x / minimal=0.25x
Confidence: high=100% / medium=80% / low=50%
Effort:     Person-months
```

### Value vs Effort Matrix

```
              Low Effort    High Effort
High Value    QUICK WINS    BIG BETS
              [Do Now]      [Plan Carefully]

Low Value     FILL-INS      TIME SINKS
              [Maybe]       [Avoid]
```

### MoSCoW Method

- **Must Have** — Critical for launch or sprint
- **Should Have** — Important but not blocking
- **Could Have** — Nice to have if capacity allows
- **Won't Have** — Explicitly out of scope this cycle

### Effective Prioritisation Principles

Mix quick wins with strategic bets. Account for dependencies and sequence them
correctly. Buffer 20% of sprint capacity for unexpected work. Revisit RICE scores
quarterly as market conditions and user data evolve. Communicate deprioritisation
decisions proactively — silence is not a strategy.

---

## 3. Weekly Rhythm

**Monday — Sprint Planning (45 min).** Order work by priority. Estimate in hours,
not story points. Identify dependencies and blockers before development begins.

**Wednesday — Technical Sync (30 min).** Resolve active blockers and architectural
disagreements. This is not a progress report.

**Friday — Week Review (20 min).** Review completed work. Note estimation divergence
and any unplanned technical debt discovered.

**Biweekly — Retrospective (45 min).** Two questions: what went well and should be
repeated, and what should change. Limit action items to three — more than that will
go unimplemented.

---

## 4. Technical Debt Management

Assess every piece of debt across two dimensions: **impact** (how much it slows
development or generates defects) and **effort** (how long to fix).

| Impact / Effort | Low Effort                                  | High Effort                                     |
| --------------- | ------------------------------------------- | ----------------------------------------------- |
| **High Impact** | Fix this sprint                             | Add to backlog, address with next major feature |
| **Low Impact**  | Fix when touching the file (boy scout rule) | Defer or remove from consideration              |

Reserve 15–20% of sprint capacity for technical debt. When this allocation is not
maintained, debt accumulates to the point of becoming critical.

**Mobile-specific debt to monitor.** Outdated Flutter or Dart SDK versions that
block new features. Deprecated packages, particularly Riverpod, GoRouter, and Dio.
Navigation patterns that do not support deep linking. Missing `dispose()` calls
causing memory leaks. Hardcoded strings that block localisation.

---

## 5. Code Review Culture

Code review is a knowledge-sharing environment, not a quality gate.

### Reviewer Rules

Label every comment with one of three categories:

- **🚫 Blocking** — Must change before merge: security vulnerability, memory leak,
  incorrect business logic
- **💡 Suggestion** — Could improve but does not block: readability, alternative
  approach
- **❓ Question** — Asked for understanding, no blocking effect

When blocking comments exceed five, the PR is likely too large — discuss with the
author rather than resolving through review comments.

**Flutter-specific blocking items.** Missing `dispose()` on `AnimationController`,
`StreamSubscription`, or `TextEditingController`. `setState()` called after
`dispose()`. Network calls inside `build()`. `const` constructors absent where
applicable. Platform-specific code without proper guards (`Platform.isIOS`).

### Author Rules

Every PR has a single purpose. Changes exceeding 400 lines should be split. Every
PR description includes what changed, why it changed, and how it was tested.

---

## 6. DORA Metrics (Adapted for Small Mobile Teams)

| Metric                          | Small Team Target           | Alarm Signal           |
| ------------------------------- | --------------------------- | ---------------------- |
| Deployment Frequency            | 1+ production push per week | Fewer than 1 per month |
| Lead Time (commit → production) | Under 3 days                | Over 2 weeks           |
| MTTR (detection → resolution)   | Under 4 hours for critical  | Over 1 day             |
| Change Failure Rate             | Under 15%                   | Over 30%               |

**Mobile additions.** App Store review time: track the average and plan releases
around it (typically 24–48 hours). Crash-free rate: target 99.5%+ via Firebase
Crashlytics or Sentry. TestFlight → Production lag: under 1 week for validated
builds.

---

## 7. Market and Competitive Analysis

### Competitor Review Framework

For each competitor, examine four areas. App Store positioning: title, subtitle,
and first three screenshots — what is their primary message? Review pattern
analysis: most frequently mentioned positives and negatives, which reveal gaps
you can exploit. Keyword overlap: which terms do they rank for, and where are they
weak? Update frequency: last six months of release notes reveal what they are
prioritising.

### Product Discovery: Customer Interview Guide

```
Context Questions (5 min)
  — Role, current workflow, tools used

Problem Exploration (15 min)
  — Pain points, frequency, current workarounds

Solution Validation (10 min)
  — Reaction to concepts, perceived value

Wrap-up (5 min)
  — Other thoughts, referrals, follow-up permission
```

### Hypothesis Template

```
We believe that [building this feature]
For [these users]
Will [achieve this outcome]
We will know we are right when [metric]
```

---

## 8. Roadmap and Communication

### Horizon Planning

- **Now (0–6 weeks)** — Sprint-level, committed, detailed
- **Next (6–12 weeks)** — Quarter-level, directional, high confidence
- **Later (12+ weeks)** — Annual bets, exploratory, subject to change

Communicate roadmap changes proactively. Users, stakeholders, and team members
need advance notice for deprioritisation decisions.

### Stakeholder Communication Principles

Identify RACI for decisions. Prefer async updates over recurring meetings. Demo
over documentation wherever possible. Address concerns early — a concern raised
at launch is ten times more expensive than one raised in planning.

---

## 9. Team Communication

### 1-on-1 Meetings (Every 2 weeks, 30 min)

Not progress reports. Two standard questions every session:

1. "What is slowing you down most?"
2. "Is there something you would like to work on in the coming month?"

### Decision Documentation

```markdown
## Decision: [Title]

**Date:** YYYY-MM-DD
**Context:** Why a decision was needed
**Decision:** What was chosen
**Rationale:** Why this option over the alternatives
**Consequences:** What changes, and which trade-offs are accepted
```

All architectural decisions, tool selections, and process changes must be recorded
in writing — ADR, README update, or pinned channel message. A developer returning
from leave should be able to reconstruct decisions made in their absence.

---

## 10. Team Scaling

The first response to capacity pressure is always to increase output with the
existing team. Hire when the team is consistently operating above 90% capacity
for more than two consecutive sprints.

**Onboarding a junior developer.** Weeks 1–4: read code, understand tests, observe
PRs, small bug fixes only. Week 5 onward: independently completable small features
with a designated senior reviewer. This is responsible onboarding, not gatekeeping.

---

## Pre-Delivery Checklist

**Sprint Planning**

- [ ] All items estimated in hours
- [ ] Dependencies identified
- [ ] 15–20% capacity reserved for technical debt

**OKR Quality**

- [ ] Each KR is measurable with a specific number
- [ ] Each KR has a named owner
- [ ] Cascade from company → product → team is visible

**Code Review**

- [ ] Comments labelled (blocking / suggestion / question)
- [ ] PR size under 400 lines or split justified
- [ ] Flutter-specific blocking items checked

**Market Intelligence**

- [ ] Competitor App Store positioning reviewed last quarter
- [ ] RICE scores updated for new feature requests
- [ ] Roadmap communicated to stakeholders
