# Zsh Shell Skill for Claude

A comprehensive skill for Claude Code, Claude.ai, and Cowork that eliminates bash/zsh compatibility issues on macOS and provides a progressive terminal mastery curriculum.

## The Problem

macOS defaults to zsh since 2019, but Claude Code's bash tool and many AI coding tools assume bash. This causes:

- **Silent script breakage** — array indexing, globbing, and word splitting behave differently
- **"Command not found" errors** — Claude Code can't see tools installed via Homebrew, nvm, or Oh My Zsh
- **Environment mismatch** — your terminal works fine, but Claude Code runs in a stripped-down shell

This skill fixes all of that, and teaches you terminal mastery along the way.

## Installation

### Claude Code (Plugin)

```bash
# From your local clone:
/plugin add /path/to/zsh-shell-skill/zsh-shell
```

### Claude.ai (Upload)

1. Download or clone this repo
2. ZIP the `zsh-shell/` folder
3. Go to Settings > Customize > Skills
4. Upload the ZIP file

### Manual (Claude Code)

Copy the `zsh-shell/` folder to `~/.claude/skills/`:

```bash
git clone https://github.com/martin-gleason/zsh-shell-skill.git
cp -r zsh-shell-skill/zsh-shell ~/.claude/skills/
```

## What's Inside

### Layer 1: Syntax — Bash ↔ Zsh Translation
Automatic detection and correction of the top compatibility issues: array indexing (0-based vs 1-based), empty array handling, glob behavior, word splitting, and extended globbing.

### Layer 2: Environment & Configuration
Understanding which config files load when (the key insight: Claude Code only reads `~/.zshenv`), macOS path differences, and tool initialization patterns.

### Layer 3: Claude Code Workarounds
Fixes for known issues: missing tools, ralph-loop plugin crash, glob errors, zoxide failures, and a diagnostic script for troubleshooting.

### Layer 4: Learning Curriculum
Nine progressive chapters from terminal basics to custom Oh My Zsh plugin development. Designed for bidirectional learning — you and Claude explore together.

## Curriculum

| Ch | Title | Capstone |
|---|---|---|
| 1 | Terminal Foundations | System info reporter |
| 2 | Navigation & Files | Project scaffolding script |
| 3 | Text Processing | CSV analysis pipeline |
| 4 | Scripting Basics | Backup script with error handling |
| 5 | Zsh-Specific Power | Lines-of-code analyzer |
| 6 | Oh My Zsh | Custom theme + aliases + startup optimization |
| 7 | Dev Environment | Team onboarding script |
| 8 | Automation | Weekly project health check |
| 9 | Advanced | Custom Oh My Zsh plugin |

Start any lesson by telling Claude: "Let's work on Chapter 1" (or any chapter number).

## Skill Structure

```
zsh-shell/
├── SKILL.md                          # Core skill file
├── references/
│   ├── syntax-cheatsheet.md          # Bash ↔ Zsh translation table
│   ├── environment-setup.md          # PATH, config files, tool setup
│   ├── claude-code-workarounds.md    # Fixes for known Claude Code issues
│   ├── oh-my-zsh-guide.md            # Plugin ecosystem and customization
│   └── zsh-changelog.md              # Version tracking and feature matrix
└── curriculum/
    ├── 00-overview.md                # Curriculum map
    ├── 01-terminal-foundations.md
    ├── 02-navigation-files.md
    ├── 03-text-processing.md
    ├── 04-scripting-basics.md
    ├── 05-zsh-specific-power.md
    ├── 06-oh-my-zsh.md
    ├── 07-dev-environment.md
    ├── 08-automation.md
    └── 09-advanced.md
```

## Requirements

- macOS with zsh (default since Catalina 2019)
- Oh My Zsh recommended but not required for Chapters 1-5
- Claude Code, Claude.ai, or Cowork

## Contributing

Issues and PRs welcome. If you've found a zsh/bash gotcha that isn't covered, or a Claude Code workaround that should be documented, please contribute.

## License

MIT — see [LICENSE](LICENSE)

---

Built with Claude by [Marty Gleason](https://github.com/martin-gleason)

#AI/Claude
