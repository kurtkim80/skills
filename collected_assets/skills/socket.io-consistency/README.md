# socket.io-consistency

[![skills.sh](https://skills.sh/b/guidogl/socket.io-consistency)](https://skills.sh/guidogl/socket.io-consistency)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](./LICENSE.txt)
[![Agent Skills Spec](https://img.shields.io/badge/Agent%20Skills-Specification-blue)](https://agentskills.io)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-4.x-010101?logo=socketdotio&logoColor=white)](https://socket.io)

An agent skill that makes generated socket.io code consistent: one canonical, modern idiom set
instead of a mix of legacy and current APIs.

## What it does

Socket.IO is stable, but generated code confuses it with raw WebSocket, omits the now-required CORS config, tracks sockets in hand-rolled arrays instead of rooms, and re-registers handlers on every reconnect. This skill pins the canonical v4 idioms — event design, acknowledgements, broadcast variants, auth middleware — and catalogs the duplicate-listener and state-desync traps.

## Install

**skills.sh**

```bash
npx skills add guidogl/socket.io-consistency
```

**Claude Code plugin marketplace**

```
/plugin marketplace add guidogl/socket.io-consistency
```

## Contents

- `SKILL.md` — the skill instructions: canonical idioms, pitfalls, version notes, workflow.
- `references/socket.io-patterns.md` — deep reference: legacy→modern migration map and
  expanded per-topic patterns, gotchas, and code examples.

## License

Apache-2.0 — see [`LICENSE.txt`](./LICENSE.txt).
