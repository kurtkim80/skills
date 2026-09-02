# Interview Context Storage System

## Overview
This system stores interview generation context in natural language for future reference and pattern learning.

## Storage Location
`/Users/nagawa/.claude/interviews-nlp/`

## File Naming Convention
`[YYYY-MM-DD]-[candidate-name]-[role].txt`

Example: `2024-01-15-lucas-germano-mobile-developer.txt`

## Context File Structure

```
================================
INTERVIEW CONTEXT
================================

Candidate: [Full Name]
Date: [ISO Date]
Role: [Position]
Seniority: [Level]
Interview Type: [Type Selected]
Duration: [Minutes]

================================
RESUME ANALYSIS SUMMARY
================================

Key Strengths Identified:
- [Strength 1 with specific evidence from resume]
- [Strength 2 with specific evidence from resume]
- [Strength 3 with specific evidence from resume]

Technical Skills Assessment:
- Strong in: [Technologies/Frameworks]
- Moderate in: [Technologies/Frameworks]
- Gap/Learning needed: [Technologies/Frameworks]

Experience Highlights:
- [Notable project or achievement]
- [Relevant industry experience]
- [Leadership or mentoring experience]

================================
AREAS EXPLORED IN INTERVIEW
================================

Technical Deep-Dives:
- [Technology/Concept 1]: [Specific questions asked]
- [Technology/Concept 2]: [Specific questions asked]

Behavioral Questions:
- [Scenario 1]: [Question approach]
- [Scenario 2]: [Question approach]

Problem-Solving:
- [Type of problem]: [Complexity level]

================================
QUESTION PATTERNS USED
================================

Opening Questions:
- [Pattern used for warm-up]

Technical Assessment:
- [Pattern for skill verification]
- [Pattern for depth assessment]

Code Review:
- [Type of code shown]
- [Issues to identify]

System Design:
- [Scenario type]
- [Complexity level]

================================
CUSTOMIZATIONS APPLIED
================================

Based on Resume:
- [Specific customization 1]
- [Specific customization 2]

Based on Role Requirements:
- [Customization for role]

Based on Seniority:
- [Level-appropriate adjustments]

================================
INTERVIEWER NOTES
================================

Effective Questions:
- [Question that worked well]
- [Why it was effective]

Areas of Concern:
- [Potential red flag]
- [How it was addressed]

Follow-up Recommendations:
- [If advancing, what to probe deeper]
- [If not advancing, why]

================================
PATTERNS FOR FUTURE USE
================================

For Similar Candidates:
- [Reusable pattern 1]
- [Reusable pattern 2]

For This Role Type:
- [Role-specific insight]

For This Seniority Level:
- [Level-specific approach]

================================
METADATA
================================

Generation Time: [Timestamp]
Command Version: 1.0
Template Used: [Template name if applicable]
Previous Context Files Referenced: [List if any]

================================
```

## Context Learning System

### Pattern Extraction
When generating new interviews, the system will:
1. Search for similar roles in context history
2. Identify successful question patterns
3. Learn from previous assessments
4. Adapt based on feedback

### Search Patterns
The system looks for:
- Same role type (e.g., "Mobile Developer")
- Similar seniority level
- Matching technology stacks
- Industry overlap

### Context Aggregation
Over time, the system builds knowledge of:
- Effective questions per role
- Common strengths/weaknesses patterns
- Technology-specific assessments
- Seniority-appropriate challenges

## Usage in Command Pipeline

### Writing Context
After interview generation:
```python
def save_interview_context(candidate_info, analysis, questions_generated):
    timestamp = datetime.now().isoformat()
    filename = f"{date}-{candidate_name}-{role}.txt"

    context = generate_context_narrative(
        candidate_info,
        analysis,
        questions_generated,
        patterns_used
    )

    with open(f"~/.claude/interviews-nlp/{filename}", "w") as f:
        f.write(context)
```

### Reading Context
When generating new interview:
```python
def load_relevant_contexts(role, seniority, tech_stack):
    contexts = []

    for file in context_directory:
        if matches_criteria(file, role, seniority, tech_stack):
            contexts.append(read_context(file))

    return aggregate_patterns(contexts)
```

## Context Evolution

### Version 1.0 (Current)
- Basic context storage
- Manual pattern identification
- Role-based retrieval

### Future Versions
- Automatic pattern extraction
- Success rate tracking
- Team feedback integration
- Cross-role insights
- Difficulty calibration

## Privacy Considerations
- No sensitive candidate data stored
- Focus on patterns, not personal details
- Anonymization of specific answers
- Retention policy: 1 year

## Example Context File

```
================================
INTERVIEW CONTEXT
================================

Candidate: Lucas Germano
Date: 2024-01-15
Role: Mobile Developer
Seniority: Mid-level (Pleno)
Interview Type: Chat with Code Review
Duration: 30 minutes

================================
RESUME ANALYSIS SUMMARY
================================

Key Strengths Identified:
- Multi-platform experience: React Native (Flashed), Flutter (Ez Soluções), iOS Native (Gira Santander)
- Production app deployment: Managed apps on App Store and TestFlight
- SDK Integration: Experience with Firebase, MoEngage, IAP configuration

Technical Skills Assessment:
- Strong in: React Native, Swift, Flutter, JavaScript/TypeScript
- Moderate in: Backend (some Python experience at LIMSI)
- Gap/Learning needed: Advanced state management, native module development

Experience Highlights:
- Current role at Flashed with React Native hybrid app development
- iOS native development with UIKit, Mapbox, Realm at Gira Santander
- International education (Polytech Paris-Saclay)

================================
AREAS EXPLORED IN INTERVIEW
================================

Technical Deep-Dives:
- React Native Performance: FlatList optimization, native module integration
- Cross-platform Trade-offs: When to choose RN vs Flutter vs Native
- iOS Specifics: Offline-first with Realm, background location tracking

Behavioral Questions:
- Transition from electrical engineering to mobile development
- Learning approach for new technologies
- Remote collaboration experience

Problem-Solving:
- Android cold start performance debugging
- App Store rejection handling

================================
[continues...]
```

## Integration with Command

The `/generate-interview` command automatically:
1. Saves context after each generation
2. Searches relevant past contexts
3. Applies learned patterns
4. Evolves question bank

This creates a continuously improving interview generation system.