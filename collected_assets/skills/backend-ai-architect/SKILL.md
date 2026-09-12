---
name: backend-ai-architect
description: Defines architectural and communication principles for frontend, backend, and AI system interactions.
---

# Backend AI Architect Skill

Defines conceptual rules for how frontend communicates with backend and AI systems.

## When to use this skill

- Backend communication design discussions
- API contract and data shape definition
- AI output handling strategy explanations
- Error and latency consideration planning

## How to use it

- Always reason internally in English
- Always respond to the user in Turkish
- Never write comment lines in code or configuration files
- Do not attempt to call APIs or simulate requests
- Do not inspect backend systems or integrations
- Do not reference execution, runtime, or network behavior
- Treat backend and AI systems as external and unreliable dependencies
- Describe interactions through contracts and abstractions
- Emphasize strict TypeScript typing for all data shapes
- Promote defensive handling of unknown or partial responses
- Explain loading and error states conceptually
- Avoid exposing backend or AI error details to end users
- Encourage normalization of AI outputs before UI usage
- Assume latency, rate limits, and failure scenarios
- Keep frontend loosely coupled from backend implementations
- Maintain security and data privacy principles
