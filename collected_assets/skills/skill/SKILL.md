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

## Hand-off file format

```markdown
## Context
<what has been done and why>

## Task
<what the new session must do>

## Key files
- path/to/file
```

## Prerequisite

Requires the `new-claude-tab` oh-my-zsh plugin to be installed:
- Plugin file: `~/.oh-my-zsh/custom/plugins/new-claude-tab/new-claude-tab.plugin.zsh`
- Registered in `~/.zshrc`: `plugins=(... new-claude-tab)`

If the command is not found, the plugin is not installed — add it before running.

## Notes

- New session starts in the same working directory
- Hand-off file is deleted automatically after being read
- Relative paths are resolved to absolute at call time
