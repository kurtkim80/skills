---
name: sandbox-lifecycle-fastlane
description: |
  Fast preflight for sandbox lifecycle work: sync pins, create a worktree, and run the standard Docker + Chrome MCP verification path.

  Triggers when user mentions:
  - "sandbox lifecycle"
  - "sandbox stuck"
  - "docker + chrome mcp"
---

## Quick Usage (Already Configured)

### 1) Preflight (sync + sanity checks)
```bash
skills/sandbox-lifecycle-fastlane/scripts/preflight.sh
```

### 2) Create a worktree for this task
Recommended (uses a timestamped branch name):
```bash
skills/sandbox-lifecycle-fastlane/scripts/worktree.sh
```

Override branch name/base:
```bash
BRANCH="sandbox-lifecycle" BASE_REF="origin/main" \
  skills/sandbox-lifecycle-fastlane/scripts/worktree.sh
```

### 3) Verify the real flow
Use the existing end-to-end skill:

- `skills/openwork-docker-chrome-mcp/SKILL.md`

That flow is the source of truth for:
- starting the stack via `_repos/openwork/packaging/docker/dev-up.sh`
- verifying user flows via Chrome MCP

## What This Skill Optimizes For

- Snappy setup: one command preflight, one command worktree.
- Reliability: avoid accidental recursive submodule operations unless explicitly requested.
- Debuggability: print the minimum git context that matters when sandboxes behave oddly (pin drift, dirty state).

## Common Gotchas

- If a submodule is dirty, `git submodule update` may refuse to move it. Stash changes inside that submodule repo.
- If you *do* need recursive submodule checks, set `RECURSIVE=1` in `preflight.sh`.
