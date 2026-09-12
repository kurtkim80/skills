---
name: deep-research
description: Multi-agent parallel investigation for complex VCV Rack problems
model: claude-opus-4-1-20250805
allowed-tools:
  - Read # Local troubleshooting docs
  - Grep # Search docs
  - Task # Spawn parallel research subagents (Level 3)
  - WebSearch # Web research (Level 2-3)
preconditions:
  - Problem is non-trivial (quick lookup insufficient)
extended-thinking: false # Level 1-2, true for Level 3 (15k budget)
timeout: 3600 # 60 min max
---

# deep-research Skill

**Purpose:** Multi-level autonomous investigation for complex VCV Rack module development problems using graduated research depth protocol.

## Overview

This skill performs thorough research on technical problems by consulting multiple knowledge sources with automatic escalation based on confidence. Starts fast (5 min local lookup) and escalates as needed (up to 60 min parallel investigation).

**Why graduated protocol matters:**

Most problems have known solutions (Level 1: 5 min). Complex problems need deep research (Level 3: 60 min). Graduated protocol prevents over-researching simple problems while ensuring complex problems get thorough investigation.

**Key innovation:** Stops as soon as confident answer found. User controls depth via decision menus.

---

## Read-Only Protocol

**CRITICAL:** This skill is **read-only** and **advisory only**. It NEVER:

- Edits code files
- Runs builds
- Modifies contracts or configurations
- Implements solutions

**Workflow handoff:**

1. Research completes and presents findings with decision menu
2. User selects "Apply solution"
3. Output routing instruction: "User selected: Apply solution. Next step: Invoke module-improve skill."
4. Main conversation (orchestrator) sees routing instruction and invokes module-improve skill
5. module-improve reads research findings from conversation history
6. module-improve handles all implementation (with versioning, backups, testing)

**Note:** The routing instruction is a directive to the main conversation. When the orchestrator sees "Invoke module-improve skill", it will use the Skill tool to invoke module-improve. This is the standard handoff protocol.

**Why separation matters:**

- Research uses Opus + extended thinking (expensive)
- Implementation needs codebase context (different focus)
- Clear decision gate between "here are options" and "making changes"
- Research can't break anything (safe exploration)

---

## Entry Points

**Invoked by:**

- troubleshooter agent (Level 4 investigation)
- User manual: `/research [topic]`
- build-automation "Investigate" option
- Natural language: "research [topic]", "investigate [problem]"

**Entry parameters:**

- **Topic/question**: What to research
- **Context** (optional): Module name, stage, error message
- **Starting level** (optional): Skip to Level 2/3 if explicitly requested

---

## Level 1: Quick Check (5-10 min, Sonnet, no extended thinking)

**Goal:** Find solution in local knowledge base or basic Rack SDK docs

### Process

1. **Parse research topic/question**
   - Extract keywords
   - Identify VCV Rack components involved
   - Classify problem type (build, runtime, API usage, panel, CV, etc.)

2. **Search local troubleshooting docs:**

   ```bash
   # Search by keywords
   grep -r "[topic keywords]" troubleshooting/


   # Check relevant categories
   ls troubleshooting/[category]/


   # Search for module-specific or general issues
   ```

3. **Check Rack SDK documentation for direct answers:**
   - Query for relevant class/API
   - Check method signatures
   - Review basic usage examples
   - Look for known limitations

4. **Assess confidence:**
   - **HIGH:** Exact match in local docs OR clear API documentation
   - **MEDIUM:** Similar issue found but needs adaptation
   - **LOW:** No relevant matches or unclear documentation

5. **Decision point:**

   **If HIGH confidence:**

   ```
   ✓ Level 1 complete (found solution)


   Solution: [Brief description]
   Source: [Local doc or Rack SDK API]


   What's next?
   1. Apply solution (recommended)
   2. Review details - See full explanation
   3. Continue deeper - Escalate to Level 2 for more options
   4. Other
   ```

   **If MEDIUM/LOW confidence:**
   Auto-escalate to Level 2 with notification:

   ```
   Level 1: No confident solution found
   Escalating to Level 2 (moderate investigation)...
   ```

---

## Level 2: Moderate Investigation (15-30 min, Sonnet, no extended thinking)

**Goal:** Find authoritative answer through comprehensive documentation and community knowledge

### Process

1. **Rack SDK deep-dive:**
   - Full module documentation
   - Code examples and patterns
   - Related classes and methods
   - Best practices sections
   - Migration guides (if version-related)

2. **VCV Rack community forum search via WebSearch:**

   ```
   Query: "site:community.vcvrack.com [topic]"


   Look for:
   - Recent threads (last 2 years)
   - Accepted solutions
   - VCV team responses
   - Multiple user confirmations
   ```

3. **GitHub issue search:**

   ```
   Query: "site:github.com/VCVRack/Rack [topic]"


   Look for:
   - Closed issues with solutions
   - Pull requests addressing problem
   - Code examples in discussions
   - Version-specific fixes
   ```

4. **Synthesize findings:**
   - Compare multiple sources
   - Verify version compatibility (Rack SDK 2.x)
   - Assess solution quality (proper fix vs workaround)
   - Identify common recommendations

5. **Decision point:**

   **If HIGH/MEDIUM confidence:**

   ```
   ✓ Level 2 complete (found N solutions)


   Investigated sources:
   - Rack SDK docs: [Finding]
   - VCV Community: [N threads]
   - GitHub: [N issues]


   Solutions found:
   1. [Solution 1] (recommended)
   2. [Solution 2] (alternative)


   What's next?
   1. Apply recommended solution
   2. Review all options - Compare approaches
   3. Continue deeper - Escalate to Level 3 (parallel investigation)
   4. Other
   ```

   **If LOW confidence OR novel problem:**
   Auto-escalate to Level 3 with notification:

   ```
   Level 2: Complex problem detected (requires original implementation)
   Escalating to Level 3 (deep research with parallel investigation)...


   Switching to Opus model + extended thinking (may take up to 60 min)
   ```

---

## Level 3: Deep Research (30-60 min, Opus, extended thinking 15k budget)

**Goal:** Comprehensive investigation with parallel subagent research for novel/complex problems

### Process

1. **Switch to Opus model with extended thinking:**

   ```yaml
   extended_thinking: true
   thinking_budget: 15000
   timeout: 3600 # 60 min
   ```

2. **Identify research approaches:**

   Analyze problem and determine 2-3 investigation paths:

   **For DSP algorithm questions:**
   - Algorithm A investigation (e.g., anti-aliasing methods)
   - Algorithm B investigation (e.g., oversampling approach)
   - Commercial implementation research (industry standards)

   **For novel feature implementation:**
   - VCV Rack native approach (using built-in APIs)
   - External library approach (e.g., integration patterns)
   - Custom implementation approach (from scratch)

   **For performance optimization:**
   - Algorithm optimization (better complexity)
   - Caching/pre-computation (trade memory for CPU)
   - SIMD/parallel processing (vectorization)

3. **Spawn parallel research subagents:**

   Use Task tool to spawn 2-3 specialized research agents in fresh contexts:

   ```typescript
   // Example: CV scaling research for V/Oct tracking

   Task(
     (subagent_type = 'general-purpose'),
     (description = 'Research V/Oct standard'),
     (prompt = `
       Investigate 1V/octave CV standard for pitch tracking in VCV Rack.
   
   
       Research:
       1. Voltage-to-frequency conversion formula
       2. VCV Rack API support (dsp::FREQ_* constants?)
       3. Implementation complexity (1-5 scale)
       4. Common pitfalls and edge cases
       5. Reference implementations
       6. Code examples
   
   
       Return structured findings:
       {
         "approach": "V/Oct conversion",
         "rack_support": "description",
         "complexity": 2,
         "formula": "...",
         "pros": ["...", "..."],
         "cons": ["...", "..."],
         "references": ["...", "..."]
       }
     `),
   );

   Task(
     (subagent_type = 'general-purpose'),
     (description = 'Research exponential FM'),
     (prompt = `
       Investigate exponential frequency modulation for VCV Rack oscillators.
   
   
       Research:
       1. Linear vs exponential FM differences
       2. VCV Rack conventions (how much FM range?)
       3. Implementation complexity (1-5 scale)
       4. CPU performance characteristics
       5. Code examples or references
   
   
       Return structured findings:
       {
         "approach": "Exponential FM",
         "rack_conventions": "description",
         "complexity": 3,
         "typical_range": "...",
         "pros": ["...", "..."],
         "cons": ["...", "..."],
         "references": ["...", "..."]
       }
     `),
   );

   Task(
     (subagent_type = 'general-purpose'),
     (description = 'Research polyphony implementation'),
     (prompt = `
       Research polyphonic voice allocation for VCV Rack modules.
   
   
       Investigate:
       1. VCV Rack polyphony API (16 channels max)
       2. Voice allocation strategies
       3. Common patterns from existing modules
       4. Performance considerations
   
   
       Return structured findings:
       {
         "approach": "Polyphony",
         "max_channels": 16,
         "allocation_strategy": "...",
         "rack_patterns": "...",
         "references": ["...", "..."]
       }
     `),
   );
   ```

   **Each subagent:**
   - Runs in fresh context (no accumulated conversation)
   - Has focused research goal
   - Returns structured findings
   - Takes 10-20 minutes
   - Runs in parallel (3 agents = 20 min total, not 60 min)

4. **Main context synthesis (extended thinking):**

   After all subagents return, use extended thinking to synthesize:
   - **Aggregate findings** from all subagents
   - **Compare approaches:**
     - Pros/cons for each
     - Implementation complexity (1-5 scale)
     - CPU cost vs quality trade-offs
     - VCV Rack integration ease
   - **Recommend best fit:**
     - For this specific use case
     - Considering complexity budget
     - Balancing CPU and quality
   - **Implementation roadmap:**
     - Step-by-step approach
     - VCV Rack APIs to use
     - Potential pitfalls
     - Testing strategy

5. **Academic paper search (if applicable):**

   For DSP algorithms, search for authoritative papers:
   - "Digital Audio Signal Processing"
   - "Real-Time Audio Programming"
   - "Modular Synthesis Techniques"

6. **Generate comprehensive report:**

   Use structured format with populated values:

   ```json
   {
     "agent": "deep-research",
     "status": "success",
     "level": 3,
     "topic": "[research topic]",
     "findings": [
       {
         "solution": "[Approach 1]",
         "confidence": "high|medium|low",
         "description": "...",
         "pros": ["...", "..."],
         "cons": ["...", "..."],
         "implementation_complexity": 3,
         "references": ["...", "..."]
       },
       {
         "solution": "[Approach 2]",
         ...
       }
     ],
     "recommendation": 0,  // Index into findings
     "reasoning": "Why this approach is recommended...",
     "sources": [
       "Rack SDK: ...",
       "VCV Community: ...",
       "Paper: ...",
       "Subagent findings: ..."
     ],
     "time_spent_minutes": 45,
     "escalation_path": [1, 2, 3]
   }
   ```

7. **Present findings:**

   ```
   ✓ Level 3 complete (comprehensive investigation)


   Investigated N approaches:
   1. [Approach 1] - Complexity: 3/5, CPU: Low, Quality: High
   2. [Approach 2] - Complexity: 2/5, CPU: Medium, Quality: High
   3. [Approach 3] - Complexity: 4/5, CPU: Low, Quality: Very High


   Recommendation: [Approach 2]
   Reasoning: [Why this is the best fit]


   What's next?
   1. Apply recommended solution (recommended)
   2. Review all findings - See detailed comparison
   3. Try alternative approach - [Approach N name]
   4. Document findings - Save to troubleshooting/
   5. Other
   ```

---

## Report Generation

All levels return structured report. Format depends on level:

### Level 1 Report (Quick)

```markdown
## Research Report: [Topic]

**Level:** 1 (Quick Check)
**Time:** 5 minutes
**Confidence:** HIGH

**Source:** troubleshooting/[category]/[file].md

**Solution:**
[Direct answer from local docs or Rack SDK API]

**How to apply:**
[Step-by-step]

**Reference:** [Source file path or Rack SDK API link]
```

### Level 2 Report (Moderate)

```markdown
## Research Report: [Topic]

**Level:** 2 (Moderate Investigation)
**Time:** 18 minutes
**Confidence:** MEDIUM-HIGH

**Sources:**

- Rack SDK docs: [Finding]
- VCV Community: 3 threads reviewed
- GitHub: 2 issues reviewed

**Solutions:**

### Option 1: [Recommended]

**Approach:** ...
**Pros:** ...
**Cons:** ...
**Implementation:** ...

### Option 2: [Alternative]

**Approach:** ...
**Pros:** ...
**Cons:** ...
**Implementation:** ...

**Recommendation:** Option 1
**Reasoning:** [Why recommended]

**References:**

- [Source 1]
- [Source 2]
```

### Level 3 Report (Comprehensive)

```markdown
## Research Report: [Topic]

**Level:** 3 (Deep Research)
**Time:** 45 minutes
**Confidence:** HIGH
**Model:** Opus + Extended Thinking

**Investigation approach:**

- Spawned 3 parallel research subagents
- Investigated 3 distinct approaches
- Synthesized findings with extended thinking

**Findings:**

### Approach 1: [Name]

**Description:** ...
**VCV Rack support:** [API/pattern details]
**Complexity:** 2/5
**CPU cost:** Medium
**Quality:** High
**Pros:**

- Works for all cases
- VCV Rack native API
  **Cons:**
- Higher CPU than alternatives
  **References:**
- Rack SDK documentation
- Subagent findings

### Approach 2: [Name]

**Description:** ...
[Same structure]

### Approach 3: [Name]

**Description:** ...
[Same structure]

**Recommendation:** Approach 1
**Reasoning:**
[Detailed explanation of why this approach is best for the use case]

**Implementation Roadmap:**

1. [Step 1 with Rack API details]
2. [Step 2 with code pattern]
3. [Step 3 with integration notes]
4. [Step 4 with testing approach]

**Sources:**

- Rack SDK: [specific API documentation]
- Paper/Reference: [if applicable]
- VCV Community: [relevant threads]
- Subagent research: 3 parallel investigations

**Testing strategy:**

- [Test 1 description]
- [Test 2 description]
- [Validation approach]
```

---

## Decision Menus

After each level, present decision menu (user controls depth):

### After Level 1

```
What's next?
1. Apply solution (recommended) - [One-line description]
2. Review details - See full explanation
3. Continue deeper - Escalate to Level 2 for more options
4. Other
```

**Handle responses:**

- **Option 1 ("Apply solution"):**
  Output: "User selected: Apply solution. Next step: Invoke module-improve skill."
  The orchestrator will see this directive and invoke module-improve, which reads research findings from history and skips investigation phase.
- **Option 2:** Display full report, then re-present menu
- **Option 3:** Escalate to Level 2
- **Option 4:** Ask what they'd like to do

**IMPORTANT:** This skill is **read-only**. Never edit code, run builds, or modify files. All implementation happens through module-improve skill after research completes.

### After Level 2

```
What's next?
1. Apply recommended solution - [Solution name]
2. Review all options - Compare N approaches
3. Continue deeper - Escalate to Level 3 (may take up to 60 min)
4. Other
```

**Handle responses:**

- **Option 1 ("Apply recommended solution"):**
  Output: "User selected: Apply recommended solution. Next step: Invoke module-improve skill."
- **Option 2:** Display detailed comparison, then re-present menu
- **Option 3:** Escalate to Level 3
- **Option 4:** Ask what they'd like to do

### After Level 3

```
What's next?
1. Apply recommended solution (recommended) - [Solution name]
2. Review all findings - See detailed comparison
3. Try alternative approach - [Alternative name]
4. Document findings - Save to troubleshooting/ knowledge base
5. Other
```

**Handle responses:**

- **Option 1 ("Apply recommended solution"):**
  Output: "User selected: Apply recommended solution. Next step: Invoke module-improve skill."
- **Option 2:** Display comprehensive report with all approaches, then re-present menu
- **Option 3:** User wants to try different approach - update recommendation, then output: "Next step: Invoke module-improve skill with alternative approach."
- **Option 4:** Invoke troubleshooting-docs skill to capture findings in knowledge base
- **Option 5:** Ask what they'd like to do

---

## Integration with troubleshooter

**troubleshooter Level 4:**

When troubleshooter agent exhausts Levels 0-3, it invokes deep-research:

```markdown
## troubleshooter - Level 4

If Levels 0-3 insufficient, escalate to deep-research skill:

"I need to investigate this more deeply. Invoking deep-research skill..."

[Invoke deep-research with problem context]

deep-research handles:

- Graduated research protocol (Levels 1-3)
- Parallel investigation (Level 3)
- Extended thinking budget
- Returns structured report with recommendations
```

**Integration flow:**

1. troubleshooter detects complex problem (Level 3 insufficient)
2. Invokes deep-research skill
3. deep-research starts at Level 1 (may escalate)
4. Returns structured report to troubleshooter
5. troubleshooter presents findings to user

---

## Integration with troubleshooting-docs

After successful application of Level 2-3 findings:

**Auto-suggest documentation:**

```
✓ Solution applied successfully


This was a complex problem (Level N research). Document for future reference?


1. Yes - Create troubleshooting doc (recommended)
2. No - Skip documentation
3. Other
```

If user chooses "Yes":

- Invoke troubleshooting-docs skill
- Pass research report + solution as context
- Creates categorized documentation
- Future Level 1 searches will find it instantly

**The feedback loop:**

1. Level 3 research solves complex problem (45 min)
2. Document solution → troubleshooting/
3. Similar problem occurs → Level 1 finds it (5 min)
4. Knowledge compounds, research gets faster over time

---

## Success Criteria

Research is successful when:

- ✅ Appropriate level reached (no over-research)
- ✅ Confidence level clearly stated
- ✅ Solution(s) provided with pros/cons
- ✅ Implementation steps included
- ✅ References cited
- ✅ User controls depth via decision menus

**Level-specific:**

**Level 1:**

- ✅ Local docs or Rack SDK checked
- ✅ HIGH confidence OR escalated

**Level 2:**

- ✅ SDK docs, community, GitHub searched
- ✅ Multiple sources compared
- ✅ MEDIUM-HIGH confidence OR escalated

**Level 3:**

- ✅ Parallel subagents spawned (2-3)
- ✅ Extended thinking used for synthesis
- ✅ Comprehensive report generated
- ✅ Clear recommendation with rationale

---

## Error Handling

**Timeout (>60 min):**

```
⚠️ Research timeout (60 min limit)


Returning best findings based on investigation so far:
[Partial findings]


What's next?
1. Use current findings - Proceed with partial answer
2. Retry with extended timeout - Continue research (80 min)
3. Other
```

**No solution found:**

```
Research exhausted (Level 3 complete, no definitive solution)


Attempted:
✓ Local troubleshooting docs (0 matches)
✓ Rack SDK documentation (API exists but undocumented)
✓ VCV Community + GitHub (no clear consensus)
✓ Parallel investigation (3 approaches, all have significant drawbacks)


Recommendations:
1. Post to VCV Community with detailed investigation
2. Try experimental approach: [Suggestion]
3. Consider alternative feature: [Workaround]


I can help formulate community post if needed.
```

**Subagent failure (Level 3):**

```
⚠️ Subagent [N] failed to complete research


Proceeding with findings from other subagents (N-1 completed)...
```

Continue with available findings, note partial investigation in report.

**WebSearch unavailable:**
Level 2 proceeds with SDK docs only:

```
⚠️ Web search unavailable


Proceeding with Rack SDK documentation only.
Results may be incomplete for community knowledge.
```

---

## Notes for Claude

**When executing this skill:**

1. Always start at Level 1 (never skip directly to Level 3)
2. Stop as soon as HIGH confidence achieved (don't over-research)
3. Switch to Opus + extended thinking at Level 3 (architecture requirement)
4. Spawn parallel subagents at Level 3 (2-3 concurrent, not serial)
5. Use relative confidence (HIGH/MEDIUM/LOW based on sources)
6. Present decision menus (user controls escalation)
7. Integration with troubleshooting-docs (capture complex solutions)
8. Timeout at 60 min (return best findings)

**Common pitfalls:**

- Skipping Level 1 local docs check (always fastest path)
- Serial subagent invocation at Level 3 (use parallel Task calls)
- Using Sonnet for Level 3 (must switch to Opus)
- Forgetting extended thinking at Level 3 (critical for synthesis)
- Over-researching simple problems (stop at HIGH confidence)
- Not presenting decision menus (user should control depth)

---

## Performance Budgets

**Level 1:**

- Time: 5-10 min
- Extended thinking: No
- Success rate: 40% of problems (known solutions)

**Level 2:**

- Time: 15-30 min
- Extended thinking: No
- Success rate: 40% of problems (documented solutions)

**Level 3:**

- Time: 30-60 min
- Extended thinking: Yes (15k budget)
- Success rate: 20% of problems (novel/complex)

**Overall:**

- Average resolution time: 15 min (weighted by success rates)
- 80% of problems solved at Level 1-2 (fast)
- 20% require Level 3 (deep research justified)

---

## VCV Rack Specific Research Areas

**Common research topics:**

1. **CV Standards:**
   - 1V/octave pitch tracking
   - 0-10V modulation range
   - Polyphonic voltage conventions

2. **DSP Patterns:**
   - Anti-aliasing for oscillators
   - Oversampling techniques
   - Exponential vs linear response

3. **Rack SDK APIs:**
   - Module lifecycle (process, onReset, etc.)
   - Port configuration (configParam, configInput)
   - Widget registration patterns

4. **Panel Design:**
   - SVG constraints and best practices
   - Component positioning conventions
   - helper.py usage patterns

5. **Performance:**
   - CPU optimization strategies
   - SIMD vectorization
   - Memory allocation patterns

6. **Build System:**
   - Rack SDK Makefile integration
   - CMake configuration
   - Cross-platform compatibility

## skill57:

name: market-research-reports
description: "Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey, BCG, Gartner). Features professional LaTeX formatting, extensive visual generation with scientific-schematics and generate-image, deep integration with research-lookup for data gathering, and multi-framework strategic analysis including Porter's Five Forces, PESTLE, SWOT, TAM/SAM/SOM, and BCG Matrix."
allowed-tools: [Read, Write, Edit, Bash]

---

# Market Research Reports

## Overview

Market research reports are comprehensive strategic documents that analyze industries, markets, and competitive landscapes to inform business decisions, investment strategies, and strategic planning. This skill generates **professional-grade reports of 50+ pages** with extensive visual content, modeled after deliverables from top consulting firms like McKinsey, BCG, Bain, Gartner, and Forrester.

**Key Features:**

- **Comprehensive length**: Reports are designed to be 50+ pages with no token constraints
- **Visual-rich content**: 5-6 key diagrams generated at start (more added as needed during writing)
- **Data-driven analysis**: Deep integration with research-lookup for market data
- **Multi-framework approach**: Porter's Five Forces, PESTLE, SWOT, BCG Matrix, TAM/SAM/SOM
- **Professional formatting**: Consulting-firm quality typography, colors, and layout
- **Actionable recommendations**: Strategic focus with implementation roadmaps

**Output Format:** LaTeX with professional styling, compiled to PDF. Uses the `market_research.sty` style package for consistent, professional formatting.

## When to Use This Skill

This skill should be used when:

- Creating comprehensive market analysis for investment decisions
- Developing industry reports for strategic planning
- Analyzing competitive landscapes and market dynamics
- Conducting market sizing exercises (TAM/SAM/SOM)
- Evaluating market entry opportunities
- Preparing due diligence materials for M&A activities
- Creating thought leadership content for industry positioning
- Developing go-to-market strategy documentation
- Analyzing regulatory and policy impacts on markets
- Building business cases for new product launches

## Visual Enhancement Requirements

**CRITICAL: Market research reports should include key visual content.**

Every report should generate **6 essential visuals** at the start, with additional visuals added as needed during writing. Start with the most critical visualizations to establish the report framework.

### Visual Generation Tools

**Use `scientific-schematics` for:**

- Market growth trajectory charts
- TAM/SAM/SOM breakdown diagrams (concentric circles)
- Porter's Five Forces diagrams
- Competitive positioning matrices
- Market segmentation charts
- Value chain diagrams
- Technology roadmaps
- Risk heatmaps
- Strategic prioritization matrices
- Implementation timelines/Gantt charts
- SWOT analysis diagrams
- BCG Growth-Share matrices

```bash
# Example: Generate a TAM/SAM/SOM diagram
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circle diagram showing Total Addressable Market $50B outer circle, Serviceable Addressable Market $15B middle circle, Serviceable Obtainable Market $3B inner circle, with labels and arrows pointing to each segment" \
  -o figures/tam_sam_som.png --doc-type report


# Example: Generate Porter's Five Forces
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Porter's Five Forces diagram with center box 'Competitive Rivalry' connected to four surrounding boxes: 'Threat of New Entrants' (top), 'Bargaining Power of Suppliers' (left), 'Bargaining Power of Buyers' (right), 'Threat of Substitutes' (bottom). Each box should show High/Medium/Low rating" \
  -o figures/porters_five_forces.png --doc-type report
```

**Use `generate-image` for:**

- Executive summary hero infographics
- Industry/sector conceptual illustrations
- Abstract technology visualizations
- Cover page imagery

```bash
# Example: Generate executive summary infographic
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for market research report, showing key metrics in modern data visualization style, blue and green color scheme, clean minimalist design with icons representing market size, growth rate, and competitive landscape" \
  --output figures/executive_summary.png
```

### Recommended Visuals by Section (Generate as Needed)

| Section                   | Priority Visuals                                         | Optional Visuals                     |
| ------------------------- | -------------------------------------------------------- | ------------------------------------ |
| Executive Summary         | Executive infographic (START)                            | -                                    |
| Market Size & Growth      | Growth trajectory (START), TAM/SAM/SOM (START)           | Regional breakdown, segment growth   |
| Competitive Landscape     | Porter's Five Forces (START), Positioning matrix (START) | Market share chart, strategic groups |
| Risk Analysis             | Risk heatmap (START)                                     | Mitigation matrix                    |
| Strategic Recommendations | Opportunity matrix                                       | Priority framework                   |
| Implementation Roadmap    | Timeline/Gantt                                           | Milestone tracker                    |
| Investment Thesis         | Financial projections                                    | Scenario analysis                    |

**Start with 6 priority visuals** (marked as START above), then generate additional visuals as specific sections are written and require visual support.

---

## Report Structure (50+ Pages)

### Front Matter (~5 pages)

#### Cover Page (1 page)

- Report title and subtitle
- Hero visualization (generated)
- Date and classification
- Prepared for / Prepared by

#### Table of Contents (1-2 pages)

- Automated from LaTeX
- List of Figures
- List of Tables

#### Executive Summary (2-3 pages)

- **Market Snapshot Box**: Key metrics at a glance
- **Investment Thesis**: 3-5 bullet point summary
- **Key Findings**: Major discoveries and insights
- **Strategic Recommendations**: Top 3-5 actionable recommendations
- **Executive Summary Infographic**: Visual synthesis of report highlights

---

### Core Analysis (~35 pages)

#### Chapter 1: Market Overview & Definition (4-5 pages)

**Content Requirements:**

- Market definition and scope
- Industry ecosystem mapping
- Key stakeholders and their roles
- Market boundaries and adjacencies
- Historical context and evolution

**Required Visuals (2):**

1. Market ecosystem/value chain diagram
2. Industry structure diagram

**Key Data Points:**

- Market definition criteria
- Included/excluded segments
- Geographic scope
- Time horizon for analysis

---

#### Chapter 2: Market Size & Growth Analysis (6-8 pages)

**Content Requirements:**

- Total Addressable Market (TAM) calculation
- Serviceable Addressable Market (SAM) definition
- Serviceable Obtainable Market (SOM) estimation
- Historical growth analysis (5-10 years)
- Growth projections (5-10 years forward)
- Growth drivers and inhibitors
- Regional market breakdown
- Segment-level analysis

**Required Visuals (4):**

1. Market growth trajectory chart (historical + projected)
2. TAM/SAM/SOM concentric circles diagram
3. Regional market breakdown (pie chart or treemap)
4. Segment growth comparison (bar chart)

**Key Data Points:**

- Current market size (with source)
- CAGR (historical and projected)
- Market size by region
- Market size by segment
- Key assumptions for projections

**Data Sources:**
Use `research-lookup` to find:

- Market research reports (Gartner, Forrester, IDC, etc.)
- Industry association data
- Government statistics
- Company financial reports
- Academic studies

---

#### Chapter 3: Industry Drivers & Trends (5-6 pages)

**Content Requirements:**

- Macroeconomic factors
- Technology trends
- Regulatory drivers
- Social and demographic shifts
- Environmental factors
- Industry-specific trends

**Analysis Frameworks:**

- **PESTLE Analysis**: Political, Economic, Social, Technological, Legal, Environmental
- **Trend Impact Assessment**: Likelihood vs Impact matrix

**Required Visuals (3):**

1. Industry trends timeline or radar chart
2. Driver impact matrix
3. PESTLE analysis diagram

**Key Data Points:**

- Top 5-10 growth drivers with quantified impact
- Emerging trends with timeline
- Disruption factors

---

#### Chapter 4: Competitive Landscape (6-8 pages)

**Content Requirements:**

- Market structure analysis
- Major player profiles
- Market share analysis
- Competitive positioning
- Barriers to entry
- Competitive dynamics

**Analysis Frameworks:**

- **Porter's Five Forces**: Comprehensive industry analysis
- **Competitive Positioning Matrix**: 2x2 matrix on key dimensions
- **Strategic Group Mapping**: Cluster competitors by strategy

**Required Visuals (4):**

1. Porter's Five Forces diagram
2. Market share pie chart or bar chart
3. Competitive positioning matrix (2x2)
4. Strategic group map

**Key Data Points:**

- Market share by company (top 10)
- Competitive intensity rating
- Entry barriers assessment
- Supplier/buyer power assessment

---

#### Chapter 5: Customer Analysis & Segmentation (4-5 pages)

**Content Requirements:**

- Customer segment definitions
- Segment size and growth
- Buying behavior analysis
- Customer needs and pain points
- Decision-making process
- Value drivers by segment

**Analysis Frameworks:**

- **Customer Segmentation Matrix**: Size vs Growth
- **Value Proposition Canvas**: Jobs, Pains, Gains
- **Customer Journey Mapping**: Awareness to Advocacy

**Required Visuals (3):**

1. Customer segmentation breakdown (pie/treemap)
2. Segment attractiveness matrix
3. Customer journey or value proposition diagram

**Key Data Points:**

- Segment sizes and percentages
- Growth rates by segment
- Average deal size / revenue per customer
- Customer acquisition cost by segment

---

#### Chapter 6: Technology & Innovation Landscape (4-5 pages)

**Content Requirements:**

- Current technology stack
- Emerging technologies
- Innovation trends
- Technology adoption curves
- R&D investment analysis
- Patent landscape

**Analysis Frameworks:**

- **Technology Readiness Assessment**: TRL levels
- **Hype Cycle Positioning**: Where technologies sit
- **Technology Roadmap**: Evolution over time

**Required Visuals (2):**

1. Technology roadmap diagram
2. Innovation/adoption curve or hype cycle

**Key Data Points:**

- R&D spending in the industry
- Key technology milestones
- Patent filing trends
- Technology adoption rates

---

#### Chapter 7: Regulatory & Policy Environment (3-4 pages)

**Content Requirements:**

- Current regulatory framework
- Key regulatory bodies
- Compliance requirements
- Upcoming regulatory changes
- Policy trends
- Impact assessment

**Required Visuals (1):**

1. Regulatory timeline or framework diagram

**Key Data Points:**

- Key regulations and effective dates
- Compliance costs
- Regulatory risks
- Policy change probability

---

#### Chapter 8: Risk Analysis (3-4 pages)

**Content Requirements:**

- Market risks
- Competitive risks
- Regulatory risks
- Technology risks
- Operational risks
- Financial risks
- Risk mitigation strategies

**Analysis Frameworks:**

- **Risk Heatmap**: Probability vs Impact
- **Risk Register**: Comprehensive risk inventory
- **Mitigation Matrix**: Risk vs Mitigation strategy

**Required Visuals (2):**

1. Risk heatmap (probability vs impact)
2. Risk mitigation matrix

**Key Data Points:**

- Top 10 risks with ratings
- Risk probability scores
- Impact severity scores
- Mitigation cost estimates

---

### Strategic Recommendations (~10 pages)

#### Chapter 9: Strategic Opportunities & Recommendations (4-5 pages)

**Content Requirements:**

- Opportunity identification
- Opportunity sizing
- Strategic options analysis
- Prioritization framework
- Detailed recommendations
- Success factors

**Analysis Frameworks:**

- **Opportunity Attractiveness Matrix**: Attractiveness vs Ability to Win
- **Strategic Options Framework**: Build, Buy, Partner, Ignore
- **Priority Matrix**: Impact vs Effort

**Required Visuals (3):**

1. Opportunity matrix
2. Strategic options framework
3. Priority/recommendation matrix

**Key Data Points:**

- Opportunity sizes
- Investment requirements
- Expected returns
- Timeline to value

---

#### Chapter 10: Implementation Roadmap (3-4 pages)

**Content Requirements:**

- Phased implementation plan
- Key milestones and deliverables
- Resource requirements
- Timeline and sequencing
- Dependencies and critical path
- Governance structure

**Required Visuals (2):**

1. Implementation timeline/Gantt chart
2. Milestone tracker or phase diagram

**Key Data Points:**

- Phase durations
- Resource requirements
- Key milestones with dates
- Budget allocation by phase

---

#### Chapter 11: Investment Thesis & Financial Projections (3-4 pages)

**Content Requirements:**

- Investment summary
- Financial projections
- Scenario analysis
- Return expectations
- Key assumptions
- Sensitivity analysis

**Required Visuals (2):**

1. Financial projection chart (revenue, growth)
2. Scenario analysis comparison

**Key Data Points:**

- Revenue projections (3-5 years)
- CAGR projections
- ROI/IRR expectations
- Key financial assumptions

---

### Back Matter (~5 pages)

#### Appendix A: Methodology & Data Sources (1-2 pages)

- Research methodology
- Data collection approach
- Data sources and citations
- Limitations and assumptions

#### Appendix B: Detailed Market Data Tables (2-3 pages)

- Comprehensive market data tables
- Regional breakdowns
- Segment details
- Historical data series

#### Appendix C: Company Profiles (1-2 pages)

- Brief profiles of key competitors
- Financial highlights
- Strategic focus areas

#### References/Bibliography

- All sources cited
- BibTeX format for LaTeX

---

## Workflow

### Phase 1: Research & Data Gathering

**Step 1: Define Scope**

- Clarify market definition
- Set geographic boundaries
- Determine time horizon
- Identify key questions to answer

**Step 2: Conduct Deep Research**

Use `research-lookup` extensively to gather market data:

```bash
# Market size and growth data
python skills/research-lookup/scripts/research_lookup.py \
  "What is the current market size and projected growth rate for [MARKET] industry? Include TAM, SAM, SOM estimates and CAGR projections"


# Competitive landscape
python skills/research-lookup/scripts/research_lookup.py \
  "Who are the top 10 competitors in the [MARKET] market? What is their market share and competitive positioning?"


# Industry trends
python skills/research-lookup/scripts/research_lookup.py \
  "What are the major trends and growth drivers in the [MARKET] industry for 2024-2030?"


# Regulatory environment
python skills/research-lookup/scripts/research_lookup.py \
  "What are the key regulations and policy changes affecting the [MARKET] industry?"
```

**Step 3: Data Organization**

- Create `sources/` folder with research notes
- Organize data by section
- Identify data gaps
- Conduct follow-up research as needed

### Phase 2: Analysis & Framework Application

**Step 4: Apply Analysis Frameworks**

For each framework, conduct structured analysis:

- **Market Sizing**: TAM → SAM → SOM with clear assumptions
- **Porter's Five Forces**: Rate each force High/Medium/Low with rationale
- **PESTLE**: Analyze each dimension with trends and impacts
- **SWOT**: Internal strengths/weaknesses, external opportunities/threats
- **Competitive Positioning**: Define axes, plot competitors

**Step 5: Develop Insights**

- Synthesize findings into key insights
- Identify strategic implications
- Develop recommendations
- Prioritize opportunities

### Phase 3: Visual Generation

**Step 6: Generate All Visuals**

Generate visuals BEFORE writing the report. Use the batch generation script:

```bash
# Generate all standard market report visuals
python skills/market-research-reports/scripts/generate_market_visuals.py \
  --topic "[MARKET NAME]" \
  --output-dir figures/
```

Or generate individually:

```bash
# 1. Market growth trajectory
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Bar chart showing market growth from 2020 to 2034, with historical bars in dark blue (2020-2024) and projected bars in light blue (2025-2034). Y-axis shows market size in billions USD. Include CAGR annotation" \
  -o figures/01_market_growth.png --doc-type report


# 2. TAM/SAM/SOM breakdown
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circles diagram. Outer circle TAM Total Addressable Market, middle circle SAM Serviceable Addressable Market, inner circle SOM Serviceable Obtainable Market. Each labeled with acronym and description. Blue gradient" \
  -o figures/02_tam_sam_som.png --doc-type report


# 3. Porter's Five Forces
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Porter's Five Forces diagram with center box 'Competitive Rivalry' connected to four surrounding boxes: Threat of New Entrants (top), Bargaining Power of Suppliers (left), Bargaining Power of Buyers (right), Threat of Substitutes (bottom). Color code by rating: High=red, Medium=yellow, Low=green" \
  -o figures/03_porters_five_forces.png --doc-type report


# 4. Competitive positioning matrix
python skills/scientific-schematics/scripts/generate_schematic.py \
  "2x2 competitive positioning matrix with X-axis 'Market Focus (Niche to Broad)' and Y-axis 'Solution Approach (Product to Platform)'. Plot 8-10 competitors as labeled circles of varying sizes. Include quadrant labels" \
  -o figures/04_competitive_positioning.png --doc-type report


# 5. Risk heatmap
python skills/scientific-schematics/scripts/generate_schematic.py \
  "Risk heatmap matrix. X-axis Impact (Low to Critical), Y-axis Probability (Unlikely to Very Likely). Color gradient: Green (low risk) to Red (critical risk). Plot 10-12 risks as labeled points" \
  -o figures/05_risk_heatmap.png --doc-type report


# 6. (Optional) Executive summary infographic
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for market research report, modern data visualization style, blue and green color scheme, clean minimalist design" \
  --output figures/06_exec_summary.png
```

### Phase 4: Report Writing

**Step 7: Initialize Project Structure**

Create the standard project structure:

```
writing_outputs/YYYYMMDD_HHMMSS_market_report_[topic]/
├── progress.md
├── drafts/
│   └── v1_market_report.tex
├── references/
│   └── references.bib
├── figures/
│   └── [all generated visuals]
├── sources/
│   └── [research notes]
└── final/
```

**Step 8: Write Report Using Template**

Use the `market_report_template.tex` as a starting point. Write each section following the structure guide, ensuring:

- **Comprehensive coverage**: Every subsection addressed
- **Data-driven content**: Claims supported by research
- **Visual integration**: Reference all generated figures
- **Professional tone**: Consulting-style writing
- **No token constraints**: Write fully, don't abbreviate

**Writing Guidelines:**

- Use active voice where possible
- Lead with insights, support with data
- Use numbered lists for recommendations
- Include data sources for all statistics
- Create smooth transitions between sections

### Phase 5: Compilation & Review

**Step 9: Compile LaTeX**

```bash
cd writing_outputs/[project_folder]/drafts/
xelatex v1_market_report.tex
bibtex v1_market_report
xelatex v1_market_report.tex
xelatex v1_market_report.tex
```

**Step 10: Quality Review**

Verify the report meets quality standards:

- [ ] Total page count is 50+ pages
- [ ] All essential visuals (5-6 core + any additional) are included and render correctly
- [ ] Executive summary captures key findings
- [ ] All data points have sources cited
- [ ] Analysis frameworks are properly applied
- [ ] Recommendations are actionable and prioritized
- [ ] No orphaned figures or tables
- [ ] Table of contents, list of figures, list of tables are accurate
- [ ] Bibliography is complete
- [ ] PDF renders without errors

**Step 11: Peer Review**

Use the peer-review skill to evaluate the report:

- Assess comprehensiveness
- Verify data accuracy
- Check logical flow
- Evaluate recommendation quality

---

## Quality Standards

### Page Count Targets

| Section                   | Minimum Pages | Target Pages |
| ------------------------- | ------------- | ------------ |
| Front Matter              | 4             | 5            |
| Market Overview           | 4             | 5            |
| Market Size & Growth      | 5             | 7            |
| Industry Drivers          | 4             | 6            |
| Competitive Landscape     | 5             | 7            |
| Customer Analysis         | 3             | 5            |
| Technology Landscape      | 3             | 5            |
| Regulatory Environment    | 2             | 4            |
| Risk Analysis             | 2             | 4            |
| Strategic Recommendations | 3             | 5            |
| Implementation Roadmap    | 2             | 4            |
| Investment Thesis         | 2             | 4            |
| Back Matter               | 4             | 5            |
| **TOTAL**                 | **43**        | **66**       |

### Visual Quality Requirements

- **Resolution**: All images at 300 DPI minimum
- **Format**: PNG for raster, PDF for vector
- **Accessibility**: Colorblind-friendly palettes
- **Consistency**: Same color scheme throughout
- **Labeling**: All axes, legends, and data points labeled
- **Source Attribution**: Sources cited in figure captions

### Data Quality Requirements

- **Currency**: Data no older than 2 years (prefer current year)
- **Sourcing**: All statistics attributed to specific sources
- **Validation**: Cross-reference multiple sources when possible
- **Assumptions**: All projections state underlying assumptions
- **Limitations**: Acknowledge data limitations and gaps

### Writing Quality Requirements

- **Objectivity**: Present balanced analysis, acknowledge uncertainties
- **Clarity**: Avoid jargon, define technical terms
- **Precision**: Use specific numbers over vague qualifiers
- **Structure**: Clear headings, logical flow, smooth transitions
- **Actionability**: Recommendations are specific and implementable

---

## LaTeX Formatting

### Using the Style Package

The `market_research.sty` package provides professional formatting. Include it in your document:

```latex
\documentclass[11pt,letterpaper]{report}
\usepackage{market_research}
```

### Box Environments

Use colored boxes to highlight key content:

```latex
% Key insight box (blue)
\begin{keyinsightbox}[Key Finding]
The market is projected to grow at 15.3% CAGR through 2030.
\end{keyinsightbox}


% Market data box (green)
\begin{marketdatabox}[Market Snapshot]
\begin{itemize}
    \item Market Size (2024): \$45.2B
    \item Projected Size (2030): \$98.7B
    \item CAGR: 15.3%
\end{itemize}
\end{marketdatabox}


% Risk box (orange/warning)
\begin{riskbox}[Critical Risk]
Regulatory changes could impact 40% of market participants.
\end{riskbox}


% Recommendation box (purple)
\begin{recommendationbox}[Strategic Recommendation]
Prioritize market entry in the Asia-Pacific region.
\end{recommendationbox}


% Callout box (gray)
\begin{calloutbox}[Definition]
TAM (Total Addressable Market) represents the total revenue opportunity.
\end{calloutbox}
```

### Figure Formatting

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.9\textwidth]{../figures/market_growth.png}
\caption{Market Growth Trajectory (2020-2030). Source: Industry analysis, company data.}
\label{fig:market_growth}
\end{figure}
```

### Table Formatting

```latex
\begin{table}[htbp]
\centering
\caption{Market Size by Region (2024)}
\begin{tabular}{@{}lrrr@{}}
\toprule
\textbf{Region} & \textbf{Size (USD)} & \textbf{Share} & \textbf{CAGR} \\
\midrule
North America & \$18.2B & 40.3\% & 12.5\% \\
\rowcolor{tablealt} Europe & \$12.1B & 26.8\% & 14.2\% \\
Asia-Pacific & \$10.5B & 23.2\% & 18.7\% \\
\rowcolor{tablealt} Rest of World & \$4.4B & 9.7\% & 11.3\% \\
\midrule
\textbf{Total} & \textbf{\$45.2B} & \textbf{100\%} & \textbf{15.3\%} \\
\bottomrule
\end{tabular}
\label{tab:market_by_region}
\end{table}
```

For complete formatting reference, see `assets/FORMATTING_GUIDE.md`.

---

## Integration with Other Skills

This skill works synergistically with:

- **research-lookup**: Essential for gathering market data, statistics, and competitive intelligence
- **scientific-schematics**: Generate all diagrams, charts, and visualizations
- **generate-image**: Create infographics and conceptual illustrations
- **peer-review**: Evaluate report quality and completeness
- **citation-management**: Manage BibTeX references

---

## Example Prompts

### Market Overview Section

```
Write a comprehensive market overview section for the [Electric Vehicle Charging Infrastructure] market. Include:
- Clear market definition and scope
- Industry ecosystem with key stakeholders
- Value chain analysis
- Historical evolution of the market
- Current market dynamics


Generate 2 supporting visuals using scientific-schematics.
```

### Competitive Landscape Section

```
Analyze the competitive landscape for the [Cloud Computing] market. Include:
- Porter's Five Forces analysis with High/Medium/Low ratings
- Top 10 competitors with market share
- Competitive positioning matrix
- Strategic group mapping
- Barriers to entry analysis


Generate 4 supporting visuals including Porter's Five Forces diagram and positioning matrix.
```

### Strategic Recommendations Section

```
Develop strategic recommendations for entering the [Renewable Energy Storage] market. Include:
- 5-7 prioritized recommendations
- Opportunity sizing for each
- Implementation considerations
- Risk factors and mitigations
- Success criteria


Generate 3 supporting visuals including opportunity matrix and priority framework.
```

---

## Checklist: 50+ Page Validation

Before finalizing the report, verify:

### Structure Completeness

- [ ] Cover page with hero visual
- [ ] Table of contents (auto-generated)
- [ ] List of figures (auto-generated)
- [ ] List of tables (auto-generated)
- [ ] Executive summary (2-3 pages)
- [ ] All 11 core chapters present
- [ ] Appendix A: Methodology
- [ ] Appendix B: Data tables
- [ ] Appendix C: Company profiles
- [ ] References/Bibliography

### Visual Completeness (Core 5-6)

- [ ] Market growth trajectory chart (Priority 1)
- [ ] TAM/SAM/SOM diagram (Priority 2)
- [ ] Porter's Five Forces (Priority 3)
- [ ] Competitive positioning matrix (Priority 4)
- [ ] Risk heatmap (Priority 5)
- [ ] Executive summary infographic (Priority 6, optional)

### Additional Visuals (Generate as Needed)

- [ ] Market ecosystem diagram
- [ ] Regional breakdown chart
- [ ] Segment growth chart
- [ ] Industry trends/PESTLE diagram
- [ ] Market share chart
- [ ] Customer segmentation chart
- [ ] Technology roadmap
- [ ] Regulatory timeline
- [ ] Opportunity matrix
- [ ] Implementation timeline
- [ ] Financial projections chart
- [ ] Other section-specific visuals

### Content Quality

- [ ] All statistics have sources
- [ ] Projections include assumptions
- [ ] Frameworks properly applied
- [ ] Recommendations are actionable
- [ ] Writing is professional quality
- [ ] No placeholder or incomplete sections

### Technical Quality

- [ ] PDF compiles without errors
- [ ] All figures render correctly
- [ ] Cross-references work
- [ ] Bibliography complete
- [ ] Page count exceeds 50

---

## Resources

### Reference Files

Load these files for detailed guidance:

- **`references/report_structure_guide.md`**: Detailed section-by-section content requirements
- **`references/visual_generation_guide.md`**: Complete prompts for generating all visual types
- **`references/data_analysis_patterns.md`**: Templates for Porter's, PESTLE, SWOT, etc.

### Assets

- **`assets/market_research.sty`**: LaTeX style package
- **`assets/market_report_template.tex`**: Complete LaTeX template
- **`assets/FORMATTING_GUIDE.md`**: Quick reference for box environments and styling

### Scripts

- **`scripts/generate_market_visuals.py`**: Batch generate all report visuals

---

## Troubleshooting

### Common Issues

**Problem**: Report is under 50 pages

- **Solution**: Expand data tables in appendices, add more detailed company profiles, include additional regional breakdowns

**Problem**: Visuals not rendering

- **Solution**: Check file paths in LaTeX, ensure images are in figures/ folder, verify file extensions

**Problem**: Bibliography missing entries

- **Solution**: Run bibtex after first xelatex pass, check .bib file for syntax errors

**Problem**: Table/figure overflow

- **Solution**: Use `\resizebox` or `adjustbox` package, reduce image width percentage

**Problem**: Poor visual quality from generation

- **Solution**: Use `--doc-type report` flag, increase iterations with `--iterations 5`

---

Use this skill to create comprehensive, visually-rich market research reports that rival top consulting firm deliverables. The combination of deep research, structured frameworks, and extensive visualization produces documents that inform strategic decisions and demonstrate analytical rigor.
