---
name: design-research
description: >
  Conducts user experience research to inform mobile product and design decisions,
  and translates research findings into high-leverage product opportunities.
  Reviews user data and analytics, analyzes App Store reviews, plans user research
  studies, creates personas, customer segments, design principles, and research
  discussion guides. Includes a structured opportunity analysis phase (10x
  thinking) that identifies game-changing product moves from research evidence
  rather than intuition alone. Use when: understanding who your users are, why
  they use the app, what jobs they're hiring the app to do, planning user
  interviews, synthesizing existing feedback, defining design principles before
  starting UI work, or identifying the highest-leverage next features.

  SCOPE BOUNDARY:
  This skill answers "What should we build and for whom?" (research and strategy).
  For "How should it look and feel?" use mobile-ui-ux.
  For "How should we build it?" use mobile-architecture or flutter-implementation-planner.
version: 3.0.0
merged-from:
  - design-research v2.0.0
  - game-changing-features v2.0.0
---

# Design Research — Mobile UX Research and Opportunity Analysis

> Research informs design. Design informs development. Always in this order.
> This skill produces insights and product opportunities, not interfaces.

---

## Skill Boundary

| Question                                     | Skill to Use                                           |
| -------------------------------------------- | ------------------------------------------------------ |
| **Who are our users and what do they need?** | ✅ **This skill** — design-research                    |
| **What are the highest-leverage moves?**     | ✅ **This skill** — opportunity analysis section       |
| **How should the app look and feel?**        | → mobile-ui-ux                                         |
| **How should we build this feature?**        | → mobile-architecture / flutter-implementation-planner |
| **How do we reach users?**                   | → mobile-gtm-strategy                                  |

---

## Core Methodology: Jobs-to-be-Done (JTBD)

Every research activity focuses on understanding what "job" users are hiring the
app to do. Research uncovers functional jobs (the practical tasks users need to
accomplish), emotional jobs (how users want to feel or avoid feeling), social jobs
(how users want to be perceived by others), and the context that triggers each job.

---

## When to Start Here

Use this skill when starting a new product or major feature before any wireframes
are produced, when user research or App Store review data exists but has not been
synthesised, when existing personas feel outdated or were never grounded in actual
users, when design decisions are being made from intuition, or when planning user
interviews or usability studies.

Do not use this skill when personas and design principles already exist and are
recent (under 6 months), during an active development sprint, or when the team
needs visual mockups — use mobile-ui-ux for that.

---

## Phase 1: Research Process

### 1.1 Scoping and Planning

Before any analysis, inventory available resources: existing analytics (Firebase,
Mixpanel, Amplitude), App Store reviews (AppFollow, Sensor Tower), support tickets
or user emails, previous user interviews or surveys, and competitor apps with
visible review patterns.

**Define research questions.**

```markdown
## Research Questions

Primary:

- What job are users hiring [app] to do?
- When and where does this job typically arise?
- What are current pain points and workarounds?

Secondary:

- Who gets the most value from the app today?
- Who uses the app but shouldn't (wrong fit)?
- What would make a user recommend this app?
```

### 1.2 App Store Review Analysis

App Store reviews are free, abundant, and represent users who cared enough to
write. Mine them systematically before conducting any primary research.

What to look for: patterns in 1–3 star reviews (what is consistently broken),
patterns in 4–5 star reviews (what is genuinely valued), feature requests that
appear three or more times (what users are desperate for), and competitor mentions
(where users are coming from and going to).

```markdown
## App Store Review Analysis — [App Name]

**Reviews analysed:** X (1-star: X, 2-star: X, 3-star: X, 4-star: X, 5-star: X)
**Date range:** YYYY-MM to YYYY-MM

### Top Pain Points (1–3 star reviews)

1. [Issue] — mentioned X times — Example quote: "..."
2. [Issue] — mentioned X times — Example quote: "..."

### Top Delighters (4–5 star reviews)

1. [Feature/Experience] — mentioned X times — Example quote: "..."
2. [Feature/Experience] — mentioned X times — Example quote: "..."

### Feature Requests (any rating)

1. [Request] — mentioned X times

### Competitive Mentions

- Coming from: [competitor] (X mentions)
- Switching to: [competitor] (X mentions)
```

### 1.3 Quantitative Data Analysis

When analytics data is available, examine onboarding completion rate and which
step has the largest drop-off, feature adoption for features with under 20% usage,
session length and frequency distribution, and D1/D7/D30 retention broken down
by cohort and acquisition channel.

```markdown
## Analytics Insights

Drop-off point: [Step X] of onboarding — [Y]% complete past this point
Implication: [What this suggests about user confusion or friction]

Feature blindspot: [Feature Y] — only [Z]% of users have used it once
Implication: [Discoverability issue or wrong ICP assumption]
```

### 1.4 User Interviews

Recruit a minimum of five interviews to identify patterns; eight to twelve for
confidence. Include active users (for usability research), churned users (for
retention research), and target users who have not yet downloaded the app (for
acquisition research).

**Discussion Guide Template.**

```markdown
# User Interview Discussion Guide — [Research Goal]

## Introduction (5 min)

- Thank participant
- Explain purpose: "We're trying to understand how you use [app], not to evaluate you"
- Get consent to record

## Context Questions (10 min)

Walk me through the last time you [core app action].

- What were you trying to accomplish?
- What triggered you to open the app then?
- What alternatives did you consider?

## Problem Exploration (20 min)

- What's the most frustrating part of [job-to-be-done] today?
- How did you handle this before [app] existed?
- If [app] disappeared tomorrow, what would you use instead?
- What would have to be true for you to recommend this app?

## Feature Probing (if needed) (10 min)

- [Specific hypothesis to test]
- "Have you ever tried [feature X]?" → If no: why not / didn't know

## Closing (5 min)

- Is there anything important we haven't covered?
- Who else do you know who uses apps like this?
- Can we follow up with you?
```

### 1.5 Synthesis

After data collection, identify patterns using the JTBD framework.

```markdown
## Synthesis Summary

### Core Jobs Identified

1. [Job statement: "When I [situation], I want to [motivation], so I can [outcome]"]
   Evidence: [quote + data point]

### Underserved Jobs (opportunity)

1. [Job that current solution addresses poorly]
   Evidence: [pattern from reviews or interviews]

### Overserved Jobs (simplification opportunity)

1. [Job that is more complex than it needs to be]
   Evidence: [complexity complaints in reviews]
```

---

## Phase 2: Opportunity Analysis

Once the research synthesis is complete, translate findings into prioritised
product opportunities. This phase prevents the common failure mode of research
that sits in a document and never informs a single decision.

The goal is not to generate ideas — it is to identify the moves that would make
this product 10× more valuable to the users the research has described. Not 10%
better. The kind of feature that makes users say "how did I live without this?"

### 2.1 Understand Current Value Before Proposing Additions

Before proposing anything, answer these questions using research data:

What problem does this app solve today? Who uses it and why, and what is the
primary job-to-be-done? What is the core action users take every session? Where
do users spend most time, and where do they drop off? What do users complain about
most, and what do they request most? What does the current D1/D7/D30 retention
signal about product-market fit?

### 2.2 Evaluate Across Three Scales

For each finding, generate opportunities at three levels of ambition. Do not
self-censor at this stage — capture the idea, evaluate it afterward.

**Massive (high effort, potentially transformative).** Features that fundamentally
expand what the product can do. New markets, new use cases, new platform
capabilities. Ask: what adjacent problem could be solved that would make the app
indispensable? What would make this a platform rather than a tool? What would
make competitors nervous?

Mobile-specific massive bets to consider: going offline-first when competitors
require connectivity, building a Home Screen widget layer that keeps users
connected without opening the app, Siri or Shortcuts integration that makes the
app part of device workflows, Watch app for a genuinely new use case, or
platform-native collaboration via SharePlay.

**Medium (moderate effort, high leverage).** Features that significantly enhance
the core experience. Force multipliers on what already works. Ask: what would
make the core action 10× faster or easier? What data exists that could personalise
the experience? What workflow is painful and could be automated?

Mobile-specific medium bets: personalised push notifications that predict when a
user wants to act rather than sending scheduled blasts, onboarding that adapts
based on the user's first action rather than following a fixed linear flow, Dynamic
Island integration for real-time glanceable data, or Spotlight Search integration
so users find content without opening the app.

**Small (low effort, disproportionate value).** Changes that punch above their
weight. Often overlooked because they appear too simple. Ask: what single button
or shortcut would save users a minute every session? What information are users
hunting for that could be surfaced immediately on open? What do users do manually
every day that could be remembered or automated?

Mobile-specific small bets: review prompt at the exact right moment (after a
successful action, never mid-task), keyboard shortcuts for iPad or Mac Catalyst
power users, drag-and-drop support for content-heavy apps, contextual empty states
that guide the first action, or smart defaults based on user history.

### 2.3 Evaluate Each Opportunity

For every candidate opportunity, assess the following dimensions.

**Impact.** How much more valuable would this make the product for mobile users?
**Reach.** What percentage of users would this affect, and does the iOS/Android
split matter for this feature? **Frequency.** How often would users encounter
this value per session or per week? **Differentiation.** Does this set the app
apart from competitors, or does it merely match them? **Defensibility.** Is this
easy to copy, or does it compound over time as users invest more in it?
**Feasibility.** Can this be built within Flutter and native interop constraints?
**Platform fit.** Is this a natural pattern for iOS and Android users, or does
it work against platform conventions?

Score each opportunity: 🔥 must do, 👍 strong, 🤔 needs more thought, ❌ pass.

### 2.4 Prioritise

Stack-rank opportunities into a recommended sequence.

```markdown
## Recommended Priority

### Do Now (quick wins — low effort, disproportionate value)

1. [Feature] — Why: [reason] — Impact: [what changes] — Effort: [rough estimate]

### Do Next (high leverage — moderate effort, clear return)

1. [Feature] — Why: [reason] — Unlocks: [what becomes possible]

### Explore (strategic bets — high effort, transformative upside)

1. [Feature] — Why: [reason] — Risk: [what could go wrong] — Upside: [what is gained]

### Backlog (good but not now)

1. [Feature] — Why later: [reason]
```

### 2.5 Opportunity Categories to Force Through

When generating opportunities, explicitly consider each category to avoid blind
spots common in mobile product thinking.

| Category           | Question                                          |
| ------------------ | ------------------------------------------------- |
| Speed              | What interaction takes too many taps or too long? |
| Automation         | What do users do manually every session?          |
| Native Integration | What platform capability is unused?               |
| Personalisation    | How does each user's usage pattern differ?        |
| Offline            | What breaks without internet?                     |
| Notifications      | What push would users actually look forward to?   |
| Collaboration      | How do users involve others?                      |
| Confidence         | What creates user anxiety?                        |
| Delight            | What could spark a genuine talking point?         |
| Accessibility      | Who cannot use this well today?                   |
| App Store          | What would lift rating and conversion?            |
| Retention          | What makes users come back tomorrow?              |

---

## Deliverable Formats

File organisation:

```
docs/design/{feature-name}-research-{MMDDYY}/
├── {feature-name}-personas.md
├── {feature-name}-customer-segments.md
├── {feature-name}-design-principles.md
├── {feature-name}-research-discussion-guide.md
└── {feature-name}-opportunities.md
```

### Personas

A good persona includes: a fictional name and one-sentence job title, the primary
JTBD (the main reason they use the app), pain points with real user quotes citing
source and date, success criteria in the user's own words, device and usage context,
and technical comfort level.

```markdown
## [Name] — [Job Title / User Type]

> "[Direct quote from a real user that captures this persona's mindset]"

**Primary Job:** [One sentence — what they hire the app to do]

**Context:** [When and where they use the app]

**Pain Points:**

- [Pain 1] — User quote: "..." (source: App Store review, MM/YYYY)
- [Pain 2] — User quote: "..."

**What success looks like:**
"[Outcome in their words]"

**Tech comfort:** High / Medium / Low
**Platform:** iOS / Android
**Usage frequency:** Daily / Weekly / Event-triggered
```

Avoid generic demographics without JTBD. "Sarah, 34, lives in Seattle, likes yoga"
tells designers nothing actionable.

### Customer Segments

Group users by behaviour, not demographics.

```markdown
## Customer Segments

| Segment | Size (est.)  | Primary Job | Characteristics | Design Implications          |
| ------- | ------------ | ----------- | --------------- | ---------------------------- |
| [Name]  | ~X% of users | [JTBD]      | [Behaviours]    | [What this means for the UI] |
```

### Design Principles

Good design principles are specific to this product (not generic "be simple"),
tied to a research insight, actionable so designers can use them to resolve
disagreements, and limited to three to seven. Each principle should be traceable
to a specific finding.

```markdown
## Design Principles — [Feature / Product]

### 1. [Principle Title]

_[Tagline — one sentence that makes this memorable]_

**Insight:** [What research finding does this come from?]
**In practice:** [One example of this principle applied]
**Not:** [What this principle rules out]
```

### Opportunities Document

```markdown
## Opportunity Analysis — [Feature / Product]

Date: YYYY-MM-DD | Platform: iOS / Android / Both

### Current Value

What the app does today, for whom, and what the core loop is.
Current retention: D1 X%, D7 X%, D30 X%.

### The Question

What would make this 10× more valuable to the users we researched?

---

### Massive Opportunities

### Medium Opportunities

### Small Gems

---

### Recommended Priority

#### Do Now

#### Do Next

#### Explore

---

### Open Questions

- [Question requiring user input or further research]
```

---

## Handoff to Design

After completing research, produce a brief handoff document connecting every
finding to a design or backlog decision.

```markdown
## Research → Design Handoff

**Key finding for designers:**
[1–3 things every designer touching this feature must know]

**Primary user:** [Persona name] doing [JTBD]

**Design principles to apply:**

1. [Principle 1]
2. [Principle 2]

**Top opportunities to explore:**

1. [Opportunity 1] — Score: 🔥/👍
2. [Opportunity 2] — Score: 🔥/👍

**Open questions for design to answer:**

- [Question that research revealed but did not resolve]

**Next skill:** mobile-ui-ux → [specific component or flow to design first]
```

---

## Common Pitfalls

**Solution-first research.** Always start with "what problem?" before "what
feature?". Research that begins with a predetermined answer produces confirmation,
not insight.

**Demographic-only personas.** Age, location, and occupation tell designers nothing
without JTBD, context, and real quotes.

**Only interviewing happy users.** Include churned users for retention research —
they will tell you things active users won't.

**Ignoring App Store reviews.** They are free, abundant, and represent the most
motivated segment of your user base. Always start there.

**Analysis paralysis.** Timebox research. Five interviews produce initial patterns.
Validate later rather than perfecting the research before acting.

**Generic design principles.** A principle that could apply to any app provides
no decision-making value.

**Research that never touches a decision.** Every finding must connect to a design
decision, a backlog item, or an opportunity in the priority list. If it connects
to nothing, either the research question was wrong or the synthesis is incomplete.

**10x thinking without research grounding.** Generating "game-changing" ideas from
intuition alone produces lists of plausible-sounding features with no evidence
of user value. The opportunity analysis in Phase 2 is only valuable when it draws
from the research in Phase 1.
