# /screen-resume Command

AI-powered resume screening tool for quickly evaluating candidate fit before scheduling interviews.

## Usage

```
/screen-resume [/path/to/resume or /path/to/directory]

[role]
[seniority level]
[must-have skills/requirements]

[optional: disqualifiers or red flags]
```

## Required Parameters
- **Resume path**: Path to candidate's PDF resume OR directory containing multiple resumes
- **Role**: Position being hired for (e.g., Mobile Developer, Backend Engineer, Full Stack Developer)
- **Seniority level**: Junior, Mid-level (Pleno), Senior, Lead, Principal
- **Must-have requirements**: Core skills/experience that are non-negotiable

## Optional Parameters
- **Disqualifiers**: Specific red flags or dealbreakers to watch for
- **Additional context**: Team needs, project specifics, culture fit considerations

## Command Pipeline

### Step 1: Input Validation
- Validate all required parameters are provided
- Check if path is file or directory
- If directory, collect all PDF files
- Prompt for missing required fields

### Step 2: File Processing
- For single file: Process immediately
- For directory: Batch process all PDFs
- Convert each PDF to markdown for analysis
- Create temporary workspace for screening

### Step 3: Resume Screening Analysis
Perform rapid assessment focusing on:
- **Role Match Score** (0-100%): How well experience matches the role
- **Seniority Alignment**: Does experience match the expected level?
- **Must-Have Skills Coverage**: Checklist of required skills
- **Red Flags**: Any disqualifiers or concerns
- **Green Flags**: Exceptional qualifications or experiences

### Step 4: Scoring & Decision
Generate screening verdict:
- **STRONG MATCH (80-100%)**: Definitely interview
- **GOOD MATCH (60-79%)**: Worth interviewing
- **MAYBE (40-59%)**: Consider if no better candidates
- **WEAK MATCH (20-39%)**: Likely not a fit
- **NO MATCH (0-19%)**: Does not meet requirements

### Step 5: Output Generation
Create structured screening report:
- Executive summary (3-5 bullet points)
- Detailed scoring breakdown
- Specific concerns or highlights
- Recommended interview focus areas (if proceeding)
- Salary expectations analysis (if mentioned)

### Step 6: Follow-up Actions
Based on screening results:
- **Strong/Good Match**: Prompt to run `/generate-interview`
- **Maybe**: Suggest specific areas to probe further
- **Weak/No Match**: Provide rejection template or feedback
- For batch processing: Generate ranked candidate list

## Output Structure

### Single Resume
```
/Users/nagawa/v2t/resume-screening/
└── [timestamp]-screening/
    ├── [candidate-name]-resume.pdf (original)
    ├── [candidate-name]-resume.md (converted)
    └── [candidate-name]-screening-report.md
```

### Batch Processing (Directory)
```
/Users/nagawa/v2t/resume-screening/
└── [timestamp]-batch-screening/
    ├── batch-summary.md (ranked list of all candidates)
    ├── strong-matches/
    │   └── [candidate-name]-screening.md
    ├── good-matches/
    │   └── [candidate-name]-screening.md
    ├── maybe/
    │   └── [candidate-name]-screening.md
    └── rejected/
        └── [candidate-name]-screening.md
```

## Screening Report Format

```markdown
# Resume Screening Report - [Candidate Name]
**Date:** [Date]
**Role:** [Position] - [Seniority]
**Verdict:** [STRONG MATCH/GOOD MATCH/MAYBE/WEAK MATCH/NO MATCH]

## Executive Summary
✅ **Score: [X]%**
- [Key qualification 1]
- [Key qualification 2]
- [Main concern if any]

## Detailed Analysis

### Role Match (X/100)
**Relevant Experience:** [Years] years
- [Specific relevant role/project]
- [Another relevant experience]

### Required Skills Coverage
✅ [Skill 1] - Strong evidence
✅ [Skill 2] - Some experience
❌ [Skill 3] - Not evident
⚠️ [Skill 4] - Unclear/needs verification

### Seniority Assessment
**Expected:** [Level]
**Actual:** [Assessment]
**Justification:** [Why they match or don't match the level]

### Red Flags
🚩 [Concern 1]
🚩 [Concern 2]

### Green Flags
💚 [Exceptional qualification 1]
💚 [Exceptional qualification 2]

## Recommendation
[PROCEED TO INTERVIEW / CONSIDER WITH CAUTION / REJECT]

### If Interviewing, Focus On:
1. [Area to probe deeply]
2. [Skill to verify]
3. [Experience to explore]

### Interview Type Suggestion:
- [Recommended interview format based on profile]
- [Duration recommendation]

---
💡 **Quick Action:** Run `/generate-interview [resume-path]` to create interview questions
```

## Batch Processing Report

```markdown
# Batch Resume Screening Summary
**Date:** [Date]
**Role:** [Position] - [Seniority]
**Total Screened:** [X] candidates

## Ranking

### 🏆 Strong Matches ([X] candidates)
1. **[Name]** - [Score]% - [Key strength]
2. **[Name]** - [Score]% - [Key strength]

### ✅ Good Matches ([X] candidates)
1. **[Name]** - [Score]% - [Note]
2. **[Name]** - [Score]% - [Note]

### 🤔 Maybe ([X] candidates)
1. **[Name]** - [Score]% - [Main concern]

### ❌ Rejected ([X] candidates)
1. **[Name]** - [Score]% - [Disqualifier]

## Recommendations
1. **Immediate interviews:** [Names]
2. **Second tier:** [Names]
3. **Only if needed:** [Names]

## Next Steps
Run `/generate-interview` for top candidates:
- `/generate-interview /path/to/[candidate1].pdf`
- `/generate-interview /path/to/[candidate2].pdf`
```

## Screening Criteria Framework

### Technical Skills Assessment
- **Direct match**: Exact technology/framework experience
- **Transferable**: Similar technologies (e.g., React → React Native)
- **Foundation**: Underlying concepts (e.g., any frontend → specific framework)
- **Missing**: No evidence of skill or related experience

### Experience Level Mapping
- **Junior**: 0-2 years, learning mindset, basic projects
- **Mid/Pleno**: 2-5 years, independent work, some complexity
- **Senior**: 5+ years, leadership, architecture, mentoring
- **Lead/Principal**: 8+ years, strategy, cross-team impact

### Red Flag Detection
- Frequent job hopping (< 1 year stays without explanation)
- Technology mismatch (e.g., only backend for frontend role)
- Overqualification (senior applying for junior role)
- Geographic/timezone incompatibility
- Salary expectation mismatch

### Green Flag Recognition
- Exact industry experience
- Open source contributions
- Relevant certifications
- Growth trajectory
- Cultural fit indicators
- Side projects showing passion

## Integration with /generate-interview

After screening completes with STRONG or GOOD match:

```
Screening complete! Candidate is a STRONG MATCH (85%).

Would you like to generate interview questions? (y/n)
> y

Proceeding to /generate-interview...
[Automatically passes candidate info and screening insights]

/generate-interview /path/to/resume.pdf
[Pre-fills candidate name from screening]
[Pre-fills role and seniority]
[Includes screening focus areas as context]
```

## Command Implementation

When invoked, Claude Code will:

1. **Parse Input**: Extract path and requirements
2. **Detect Type**: Single file vs directory
3. **Process Files**: Convert PDFs to markdown
4. **Quick Analysis**: Rapid pattern matching against requirements
5. **Score & Rank**: Generate match percentages
6. **Generate Reports**: Create screening summaries
7. **Prompt Next**: Offer to proceed with interview generation
8. **Store Context**: Save screening patterns for learning

## Screening Speed Optimizations

- **Parallel Processing**: For directories, screen multiple resumes simultaneously
- **Quick Scan**: Focus on keywords and patterns first
- **Smart Extraction**: Pull only relevant sections for deep analysis
- **Caching**: Store converted markdown for re-screening
- **Templates**: Pre-built assessment criteria by role

## Example Execution

### Single File
```
User: /screen-resume /Downloads/john_doe_resume.pdf

Backend Engineer
Senior
Python, Django, PostgreSQL, Docker, AWS

No consultancy experience, must have product company background

Claude:
🔍 Screening resume for Backend Engineer (Senior)...
✅ Resume converted and analyzed

## John Doe - STRONG MATCH (82%)

### Quick Summary:
✅ 7 years backend experience
✅ Python/Django expert (5 years)
✅ AWS certified, Docker proficient
✅ Product company background (Spotify, Uber)
⚠️ PostgreSQL experience limited (mostly MySQL)

### Recommendation: PROCEED TO INTERVIEW
Focus areas: PostgreSQL specifics, system design, scaling challenges

Generate interview questions now? (y/n)
```

### Directory Batch
```
User: /screen-resume /Downloads/backend_candidates/

Backend Engineer
Senior
Python, Django, PostgreSQL, Docker, AWS

Claude:
📁 Found 12 resumes to screen...
⏳ Processing batch screening...

## Screening Complete!

### Results Summary:
🏆 **Strong Matches (3)**
1. John Doe - 82% - Spotify/Uber experience
2. Maria Silva - 79% - Django expert, AWS certified
3. Carlos Santos - 77% - Strong PostgreSQL, Docker

✅ **Good Matches (2)**
4. Ana Costa - 65% - Good skills, less seniority
5. Pedro Lima - 61% - Solid backend, learning Python

🤔 **Maybe (2)**
❌ **Rejected (5)** - Wrong tech stack or junior level

View detailed reports in: /Users/nagawa/v2t/resume-screening/[timestamp]-batch-screening/

Generate interviews for top 3? (y/n)
```

## Error Handling

- **Missing file**: Prompt for valid path
- **Invalid PDF**: Try alternative conversion methods
- **Corrupted file**: Skip and note in batch report
- **Missing requirements**: Interactive prompt for criteria
- **Large batches**: Process in chunks with progress updates

## Performance Targets

- **Single resume**: < 10 seconds
- **Batch of 10**: < 60 seconds
- **Accuracy goal**: 90% agreement with human screening
- **False negative rate**: < 5% (avoid rejecting good candidates)

## Context Learning

Store screening patterns in `~/.claude/screening-patterns/`:
- Successful hire patterns by role
- Common red flags that proved accurate
- Green flags that correlate with performance
- Skill transferability mappings

## Future Enhancements

- Auto-detect role from job description
- LinkedIn profile integration
- GitHub profile analysis for developers
- Portfolio review for designers
- Salary benchmark comparison
- Diversity and inclusion metrics
- ATS integration for bulk processing