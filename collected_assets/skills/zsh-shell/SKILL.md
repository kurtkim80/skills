---
name: zsh-shell
description: "Zsh shell skill for macOS environments. Use this skill whenever: writing or running shell commands on macOS, debugging shell errors (glob failures, unbound variables, command not found), working with Oh My Zsh (plugins, themes, custom configs), the user mentions .zshrc/.zprofile/terminal customization, shell scripts fail with zsh-specific errors, the user asks about Homebrew/nvm/uv/dev environment setup, the user wants to learn terminal or shell scripting skills, Claude Code hits PATH or environment issues on macOS. This skill prevents the #1 class of macOS Claude Code failures: bash/zsh incompatibility. Also triggers for any request mentioning 'terminal', 'shell', 'command line', 'zsh', 'oh my zsh', or references to curriculum chapters."
---

# Zsh Shell — Operations + Learning

A skill for working correctly in zsh environments and learning shell mastery through bidirectional exploration with Claude.

## When to Use This Skill

**Operational (Layers 1-3):** Any time Claude writes or runs shell commands on macOS, or when a shell command fails unexpectedly. Claude should silently consult Layer 1 (syntax) when writing commands and Layer 3 (workarounds) when diagnosing failures.

**Educational (Layer 4):** When the user asks to learn shell skills, references a curriculum chapter, or wants to understand WHY a shell concept matters. The learning mode is collaborative — Claude and the user explore together.

## Critical Context

macOS defaults to zsh (since Catalina 2019). Claude Code's bash tool often runs in bash or a non-interactive zsh that lacks the user's configuration. This mismatch causes the most common class of macOS Claude Code failures. This skill fixes that.

---

# Layer 1: Syntax — Bash ↔ Zsh Translation

Consult `references/syntax-cheatsheet.md` for the full translation table. Here are the critical differences Claude must internalize:

### The Big Five Gotchas

**1. Array indexing — zsh is 1-based, bash is 0-based**
```bash
# bash: first element
echo "${arr[0]}"
# zsh: first element
echo "${arr[1]}"
```
WHY this matters: Every loop over an array, every index-based access, every `${#arr[@]}` pattern can silently return wrong results. This is the #1 porting bug.

**2. Empty arrays crash bash strict mode**
```bash
# bash 3.2 with set -u: CRASHES
arr=()
echo "${arr[*]}"  # unbound variable error

# Fix for bash:
echo "${arr[*]:-}"  # provide default

# zsh: handles this correctly — no crash
```
WHY this matters: This is the exact bug that breaks the ralph-loop plugin and many CI scripts.

**3. Glob no-match behavior**
```bash
# bash: passes literal "*.xyz" if no matches
ls *.xyz  # shows: *.xyz: No such file or directory

# zsh: throws an error
ls *.xyz  # zsh: no matches found: *.xyz

# Fix for zsh scripts:
setopt NULL_GLOB    # no matches → empty
# or
setopt NO_NOMATCH   # no matches → pass literal (bash behavior)
```
WHY this matters: Scripts that use globs as "try to find files" patterns break in zsh unless you handle no-match explicitly.

**4. Word splitting — zsh does NOT split by default**
```bash
# bash: splits into three words
files="one two three"
for f in $files; do echo $f; done  # prints three lines

# zsh: treats as one word
for f in $files; do echo $f; done  # prints one line: "one two three"

# zsh fix: explicit split
for f in ${=files}; do echo $f; done  # prints three lines
```
WHY this matters: Any script that relies on unquoted variable expansion to split strings will behave differently in zsh.

**5. Extended globbing uses different syntax**
```bash
# bash:
shopt -s extglob
ls !(*.log)        # everything except .log files

# zsh:
setopt EXTENDED_GLOB
ls ^*.log          # everything except .log files
```
WHY this matters: Complex file selection patterns in build scripts, cleanup scripts, and CI pipelines use extended globs heavily.

### Quick Compatibility Check

Before writing any shell command, Claude should ask: "Am I in bash or zsh?" Detection:
```bash
echo $0          # Shows current shell
echo $ZSH_VERSION  # Non-empty = zsh
echo $BASH_VERSION  # Non-empty = bash
```

For commands that must work in both shells, stick to POSIX syntax. For zsh-specific power features, use them when confirmed in zsh.

---

# Layer 2: Environment & Configuration

Consult `references/environment-setup.md` for the full guide. Key points:

### Config File Loading Order

```
Login shell (opening Terminal.app):
  ~/.zshenv → ~/.zprofile → ~/.zshrc → ~/.zlogin

Non-login interactive (new tab):
  ~/.zshenv → ~/.zshrc

Non-interactive (script execution):
  ~/.zshenv ONLY
```

**The critical insight:** Claude Code often runs as non-interactive, meaning it only reads `~/.zshenv`. If the user's tools are initialized in `~/.zshrc` (where Oh My Zsh lives, where nvm loads, where PATH gets built), Claude Code won't see them.

### What Goes Where

| File | What belongs here | WHY |
|---|---|---|
| `~/.zshenv` | PATH additions, essential env vars | Only file guaranteed to load in ALL contexts including scripts and Claude Code |
| `~/.zshrc` | Oh My Zsh, aliases, prompt, plugins, interactive tools | Only loads for interactive shells — keeps script execution fast |
| `~/.zprofile` | Login-only setup (rare) | Runs once per login session |

### macOS-Specific Paths

```bash
# Apple Silicon (M1/M2/M3/M4)
/opt/homebrew/bin    # Homebrew binaries
/opt/homebrew/sbin   # Homebrew system binaries

# Intel Mac
/usr/local/bin       # Homebrew binaries
/usr/local/sbin      # Homebrew system binaries
```

Claude should check `uname -m` to determine architecture when diagnosing PATH issues.

---

# Layer 3: Claude Code Workarounds

Consult `references/claude-code-workarounds.md` for the full fix list. Critical patterns:

### When Tools Are Missing

If a command returns "command not found" in Claude Code but works in the user's terminal:

```bash
# Step 1: Check what shell Claude Code is using
echo $0 && echo "ZSH: $ZSH_VERSION" && echo "BASH: $BASH_VERSION"

# Step 2: Check PATH
echo $PATH | tr ':' '\n'

# Step 3: If tools are missing, source the user's config
source ~/.zshrc 2>/dev/null

# Step 4: Or run command in a login shell
/bin/zsh --login -c 'your-command-here'
```

### Diagnostic Script

When Claude Code encounters shell issues, run this first:
```zsh
echo "=== Shell Environment ==="
echo "Shell: $0 | ZSH: $ZSH_VERSION | BASH: $BASH_VERSION"
echo "SHELL var: $SHELL"
echo "=== Key Tools ==="
for cmd in brew node npm nvm uv python git; do
  echo "$cmd: $(which $cmd 2>/dev/null || echo 'NOT FOUND')"
done
echo "=== Oh My Zsh ==="
echo "ZSH dir: ${ZSH:-NOT SET}"
echo "Theme: ${ZSH_THEME:-NOT SET}"
echo "Plugins: ${plugins[*]:-NONE}"
echo "=== Architecture ==="
echo "Arch: $(uname -m)"
```

### Fixing Plugin Bugs

When Claude Code plugins (like ralph-loop) fail with bash-specific errors:

1. Locate the failing script in `~/.claude/plugins/cache/`
2. Check for bash strict mode issues (`set -euo pipefail` + empty arrays)
3. Apply the `${array[*]:-}` fix for empty array expansion
4. Note: plugin cache overwrites fixes on update — keep a record of patches applied

### Writing Cross-Compatible Scripts

When Claude writes shell scripts that might run in either bash or zsh:

```bash
#!/usr/bin/env bash
# OR
#!/usr/bin/env zsh

# If the script must work in both, add a compatibility header:
if [ -n "$ZSH_VERSION" ]; then
  setopt SH_WORD_SPLIT    # bash-compatible word splitting
  setopt NO_NOMATCH        # bash-compatible glob behavior
fi
```

---

# Layer 4: Learning Curriculum

## How the Curriculum Works

The curriculum lives in `curriculum/` as 9 progressive chapters plus an overview. Each chapter is a markdown file designed to be worked through collaboratively with Claude.

### Bidirectional Learning Model

This is not "Claude teaches you." It's "you and Claude explore together."

- Claude is expert at syntax and reference material
- The user is expert at their own environment and workflow
- Together, you discover how concepts apply to the user's real work
- When something unexpected happens, both learn from it
- Claude asks genuine questions: "What did that output? I expected X."

### The WHY Principle

Every concept connects to real development work. No abstract commands without context. Before explaining HOW to do something, explain WHY a developer would need it. Before showing syntax, show the problem it solves.

### Chapter Structure

Every chapter follows this pattern:

1. **WHY this matters** — the development problem this chapter solves
2. **Concepts** — key ideas with real-world connections
3. **Exploration** — hands-on exercises in the user's real terminal
4. **Discovery** — experiments where the user predicts outcomes before running commands
5. **Capstone** — a practical project combining this chapter's skills with all prior chapters

### Curriculum Map

| Ch | Title | WHY It Matters | Capstone |
|---|---|---|---|
| 1 | Terminal Foundations | Your terminal is your most powerful dev tool — understanding it multiplies everything else | System info one-liner |
| 2 | Navigation & Files | Every dev task starts with finding and organizing files — speed here saves hours weekly | Project scaffolding script |
| 3 | Text Processing | Logs, data, configs — 80% of debugging is finding the right text in the right file | CSV analysis pipeline |
| 4 | Scripting Basics | Automation turns a 10-minute manual task into a 1-second script you run forever | Backup script with error handling |
| 5 | Zsh-Specific Power | Zsh features that bash lacks — why Apple chose it and what you gain | Lines-of-code analyzer |
| 6 | Oh My Zsh | Plugins and themes that save 30+ minutes daily for developers who live in the terminal | Custom theme + aliases + startup optimization |
| 7 | Dev Environment | nvm, uv, Homebrew, git — the tools under your tools, and why version management prevents disasters | Team onboarding script |
| 8 | Automation | Scripts that run themselves — monitoring, health checks, scheduled tasks | Weekly project health check |
| 9 | Advanced | Custom plugins, debugging, profiling — building tools for your specific workflow | Custom Oh My Zsh plugin |

### Starting a Lesson

When a user asks to learn or references a chapter:

1. Read the relevant chapter from `curriculum/`
2. Start with the WHY section — connect it to the user's work
3. Run the diagnostic script to understand their current environment
4. Adapt examples to their actual setup (their plugins, their theme, their tools)
5. Follow the chapter's exercise sequence, pausing for the user to run commands
6. At discovery points, ask the user to PREDICT before executing
7. At the capstone, the user should be able to complete it with minimal hints

### Prerequisite Check

Before Chapter 1, verify:
```bash
# What shell?
echo $SHELL
# What OS?
sw_vers 2>/dev/null || uname -a
# Is Oh My Zsh installed?
[ -d "$HOME/.oh-my-zsh" ] && echo "Oh My Zsh: YES" || echo "Oh My Zsh: NOT INSTALLED"
```

If Oh My Zsh isn't installed, Chapter 6 covers installation. Chapters 1-5 work without it.

---

# Oh My Zsh Awareness

Claude should detect and adapt to the user's Oh My Zsh configuration.

### Detection

```bash
echo "Theme: ${ZSH_THEME:-not set}"
echo "Plugins: ${plugins[*]:-none}"
ls ~/.oh-my-zsh/custom/plugins/ 2>/dev/null
ls ~/.oh-my-zsh/custom/themes/ 2>/dev/null
```

### Plugin Interactions

Before defining an alias or function, check if an Oh My Zsh plugin already provides it. The `git` plugin alone defines 80+ aliases. Running `alias | grep git` reveals what's already available.

When a user says "command not found" for something that should exist, check if it's provided by a plugin that isn't loaded in the current context (common in Claude Code's non-interactive shell).

### Common Plugin Reference

| Plugin | Key Aliases/Functions | Note |
|---|---|---|
| `git` | `gst`=status, `gco`=checkout, `gp`=push, `gl`=pull | Most comprehensive — check before adding git aliases |
| `virtualenv` | Shows active env in prompt | Requires virtualenvwrapper or venv |
| `node` | `node-docs` command | Shows Node.js version in prompt |
| `postgres` | `pgstart`, `pgstop`, `pgstatus` | Aliases for pg_ctl operations |

Consult `references/oh-my-zsh-guide.md` for the full plugin reference and troubleshooting guide.

---

# Keeping Current

### Update Path

This skill tracks zsh versions and features. Consult `references/zsh-changelog.md` for version-specific features.

When a user's zsh version is detected, Claude should note any features that are or aren't available:

```bash
# Check version
echo $ZSH_VERSION
# macOS typically ships: 5.8.1 (Monterey), 5.9 (Ventura+)
```

### When to Update This Skill

- New zsh release with user-facing features
- New Oh My Zsh plugins reaching widespread adoption
- New Claude Code issues or fixes for shell compatibility
- New macOS release changing default shell behavior or zsh version
- New dev tools (like uv) becoming standard in workflows

---

## Reference Files

Read these when deeper detail is needed:

| File | When to Read |
|---|---|
| `references/syntax-cheatsheet.md` | Writing shell commands, translating bash↔zsh |
| `references/environment-setup.md` | Diagnosing PATH issues, configuring dev tools |
| `references/claude-code-workarounds.md` | Fixing shell failures in Claude Code/Cowork |
| `references/oh-my-zsh-guide.md` | Plugin recommendations, theme customization, troubleshooting |
| `references/zsh-changelog.md` | Checking version-specific features |
| `curriculum/00-overview.md` | Starting the learning curriculum |

---

*Last verified: March 2026 | zsh 5.9 | Oh My Zsh current*

-----
March 4, 2026

#AI/Claude
