---
name: new-claude-tab
description: >
  Open a new Warp terminal tab and start a fresh Claude Code session,
  automatically pre-loaded with a hand-off file and/or prompt.
  Use when the current session should delegate a task to a parallel session
  without blocking the current one.
---

# new-claude-tab

A zsh plugin that opens a new Warp tab with a Claude Code session, pre-loaded with a hand-off file and/or prompt.

## Usage

```bash
new-claude-tab                                   # plain new session
new-claude-tab handoff.md                        # file as first message
new-claude-tab handoff.md "extra instruction"    # file + prompt
new-claude-tab "" "just a quick task"            # prompt only
```

## Let the new tab delete the hand-off file itself

The new session receives the hand-off **content** as its first message, so it never needs the file
again. The delete instruction lives **only** inside the hand-off file (its `## First step` section).
Never put `rm` in the `new-claude-tab` command line — the launching shell/permission check flags it
before the tab opens. The destination agent runs the `rm` itself after it starts.

```bash
new-claude-tab ~/path/HANDOFF.md "Read the hand-off above and follow it."
```

## Hand-off file format

```markdown
## Context
<what has been done and why>

## Task
<what the new session must do>

## Key files
- path/to/file

## First step
This hand-off is already in your first message. Delete the file now: `rm -f <absolute path of this file>`
```

## Prerequisite

Requires the `new-claude-tab` shell function, from the oh-my-zsh plugin:
- Plugin file: `~/.oh-my-zsh/custom/plugins/zsh-warp-claude-tab/zsh-warp-claude-tab.plugin.zsh`
- Registered in `~/.zshrc`: `plugins=(... zsh-warp-claude-tab)`

If the command is not found, the plugin is not installed — add it before running.

## Notes

- New session starts in the same working directory
- The plugin deletes only its own temporary copy (`/tmp/.ct_msg_*`), **not** the hand-off file — see "Let the new tab delete the hand-off file itself"
- Relative paths are resolved to absolute at call time

## Creating multiple tabs at once

**Never fire multiple `new-claude-tab` calls back-to-back with no delay** — launching them immediately one after another causes issues (observed launching 6 at once; a 1s gap was still too fast and dropped tabs, 3s confirmed reliable). Space them out: run one, wait 3 seconds, run the next, and so on — sequential Bash calls with `sleep 3` in between, not a batch of parallel/simultaneous invocations.

```bash
new-claude-tab handoff-1.md
sleep 3
new-claude-tab handoff-2.md
sleep 3
new-claude-tab handoff-3.md
```
