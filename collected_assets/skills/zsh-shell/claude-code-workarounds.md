# Claude Code Shell Workarounds

Practical fixes for known issues when Claude Code or Cowork runs shell commands on macOS. Each entry includes the symptom, root cause, and fix.

---

## Diagnostic Script

Run this first when any shell-related issue occurs in Claude Code:

```zsh
echo "=== Shell Identity ==="
echo "  \$0: $0"
echo "  \$SHELL: $SHELL"
echo "  ZSH_VERSION: ${ZSH_VERSION:-not zsh}"
echo "  BASH_VERSION: ${BASH_VERSION:-not bash}"
echo "  Interactive: $(case $- in *i*) echo YES;; *) echo NO;; esac)"

echo "=== Architecture ==="
echo "  Arch: $(uname -m)"
echo "  macOS: $(sw_vers -productVersion 2>/dev/null || echo 'not macOS')"

echo "=== Key Tools ==="
for cmd in brew node npm npx nvm uv python3 git ssh ruby; do
  printf "  %-10s %s\n" "$cmd:" "$(which $cmd 2>/dev/null || echo 'NOT FOUND')"
done

echo "=== PATH (first 15 entries) ==="
echo $PATH | tr ':' '\n' | head -15 | while read p; do echo "  $p"; done

echo "=== Oh My Zsh ==="
echo "  ZSH dir: ${ZSH:-NOT SET}"
echo "  Theme: ${ZSH_THEME:-NOT SET}"
if [ -n "${ZSH_VERSION:-}" ]; then
  echo "  Plugins: ${plugins[*]:-NONE}"
fi

echo "=== Config Files ==="
for f in ~/.zshenv ~/.zprofile ~/.zshrc ~/.zlogin; do
  [ -f "$f" ] && echo "  $f: EXISTS ($(wc -l < "$f") lines)" || echo "  $f: not found"
done
```

---

## Issue: Tools Not Found (command not found)

**Symptom:** `brew: command not found`, `node: command not found`, `nvm: command not found` in Claude Code, but they work in your terminal.

**Root cause:** Claude Code runs as a non-interactive shell. Only `~/.zshenv` is loaded. Homebrew PATH, nvm initialization, and other tool setup live in `~/.zshrc`.

**Fix (immediate):** Run the command in a login shell:
```bash
/bin/zsh --login -c 'node --version'
/bin/zsh --login -c 'brew list'
```

**Fix (permanent):** Move critical PATH entries to `~/.zshenv`:
```zsh
# Add to ~/.zshenv (loaded in ALL contexts)
# Apple Silicon Homebrew
[ -d "/opt/homebrew" ] && export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:$PATH"
# User local binaries
export PATH="$HOME/.local/bin:$PATH"
```

**Fix (nvm specifically):** nvm is slow to source, so it's usually in `.zshrc`. Two options:

Option A — Add nvm to `.zshenv` (adds ~200ms to every script):
```zsh
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

Option B — Add just the active Node version to PATH in `.zshenv`:
```zsh
# Add the currently-active Node to PATH without loading full nvm
[ -d "$HOME/.nvm/versions/node" ] && \
  export PATH="$(ls -d $HOME/.nvm/versions/node/*/bin 2>/dev/null | tail -1):$PATH"
```

---

## Issue: ralph-loop Plugin Crash

**Symptom:** `PROMPT_PARTS[*]: unbound variable` when running `/ralph-loop`.

**Root cause:** The plugin script uses `set -u` (strict mode) and `${PROMPT_PARTS[*]}` on an empty array. Bash 3.2 (macOS default) treats empty arrays as unset under strict mode.

**Fix:**
```bash
# Find the script
SCRIPT="$HOME/.claude/plugins/cache/claude-plugins-official/ralph-loop/*/scripts/setup-ralph-loop.sh"

# Edit line 113
# Change:
#   PROMPT="${PROMPT_PARTS[*]}"
# To:
#   PROMPT="${PROMPT_PARTS[*]:-}"

# One-liner fix (find and replace):
sed -i '' 's/PROMPT="${PROMPT_PARTS\[\*\]}"/PROMPT="${PROMPT_PARTS[*]:-}"/' $SCRIPT
```

**Note:** This fix gets overwritten when the plugin cache updates. After a Claude Code update, check if the issue returns and re-apply.

---

## Issue: Glob Errors in Shell Commands

**Symptom:** `zsh: no matches found: *.xyz` when running a command that works in bash.

**Root cause:** Zsh throws an error when a glob pattern matches nothing. Bash passes the literal glob string.

**Fix (per-command):** Quote the glob or use `noglob`:
```zsh
ls '*.xyz' 2>/dev/null
noglob ls *.xyz
```

**Fix (per-script):** Add to the top of the script:
```zsh
setopt NULL_GLOB     # No matches → empty (silent)
# OR
setopt NO_NOMATCH    # No matches → pass literal (bash behavior)
```

**Fix (for Claude Code):** When Claude writes scripts that use globs, always include `setopt NULL_GLOB` at the top.

---

## Issue: zoxide / starship / Custom Hooks Crash

**Symptom:** `__zoxide_z: command not found` or similar errors for shell enhancements.

**Root cause:** Tools like zoxide, starship, and custom shell hooks initialize in `~/.zshrc`. Claude Code's non-interactive shell doesn't load `.zshrc`.

**Fix:** Use absolute paths instead of shell-enhanced commands:
```bash
# Instead of: z project-dir (zoxide)
cd /Users/username/code/project-dir

# Instead of: relying on starship prompt
# Claude Code doesn't need a pretty prompt — this is cosmetic only
```

**Prevention:** Claude Code should never assume shell enhancements are available. Always use standard commands (`cd`, `ls`, `find`) rather than plugin-provided alternatives.

---

## Issue: Bash Tool Defaults to Bash (Not Zsh)

**Symptom:** Claude Code commands run in bash even though the user's default shell is zsh. `echo $0` shows `/bin/bash`.

**Root cause:** Claude Code's bash tool uses bash as the execution shell on macOS, regardless of user's configured default.

**Workaround:** When zsh-specific features are needed:
```bash
/bin/zsh -c 'your zsh command here'
/bin/zsh --login -c 'command needing full env'
```

**Note:** This is an open issue on the Claude Code repo (multiple reports). The workaround is functional but not ideal.

---

## Issue: Shell Script Runs Differently in Claude Code vs Terminal

**Symptom:** A script works when the user runs it manually but produces different results when Claude Code runs it.

**Diagnosis checklist:**

1. **Which shell is executing?** Check shebang line: `#!/usr/bin/env bash` vs `#!/usr/bin/env zsh`
2. **Is the environment loaded?** Compare `echo $PATH` in both contexts
3. **Is it interactive?** Check `$-` — Claude Code runs non-interactive
4. **Are aliases available?** Aliases are off by default in non-interactive zsh. Use functions instead.
5. **Is Oh My Zsh loaded?** Check `echo $ZSH` — if empty, Oh My Zsh plugins aren't available

**Universal fix header for scripts that must work in Claude Code:**
```bash
#!/usr/bin/env zsh

# Ensure core environment is available
[ -f "$HOME/.zshenv" ] && source "$HOME/.zshenv"

# If we need Oh My Zsh functions/aliases
# (only if script truly depends on them)
[ -f "$HOME/.zshrc" ] && source "$HOME/.zshrc" 2>/dev/null

# Compatibility
setopt NO_NOMATCH 2>/dev/null  # bash-like glob behavior
setopt SH_WORD_SPLIT 2>/dev/null  # bash-like word splitting
```

---

## Issue: Plugin Cache Overwrites Fixes

**Symptom:** A fix you applied to a Claude Code plugin script reverts after a Claude Code update.

**Prevention strategy:** Keep a patch directory:

```bash
# Create patch storage
mkdir -p ~/.claude/patches

# After fixing a plugin, save the patch
diff original.sh fixed.sh > ~/.claude/patches/ralph-loop-prompt-parts.patch

# Create a re-apply script
cat > ~/.claude/patches/apply-all.sh << 'EOF'
#!/bin/zsh
echo "Applying Claude Code plugin patches..."

# ralph-loop PROMPT_PARTS fix
RALPH_SCRIPT=$(ls ~/.claude/plugins/cache/claude-plugins-official/ralph-loop/*/scripts/setup-ralph-loop.sh 2>/dev/null)
if [ -n "$RALPH_SCRIPT" ]; then
  sed -i '' 's/PROMPT="${PROMPT_PARTS\[\*\]}"/PROMPT="${PROMPT_PARTS[*]:-}"/' "$RALPH_SCRIPT"
  echo "  ✓ ralph-loop PROMPT_PARTS fix applied"
fi

# Add more patches here as needed

echo "Done."
EOF
chmod +x ~/.claude/patches/apply-all.sh
```

After any Claude Code update:
```bash
~/.claude/patches/apply-all.sh
```

---

## Writing Claude Code-Compatible Commands

### Guidelines for Claude

When writing shell commands in Claude Code on macOS:

1. **Don't assume zsh features** — the bash tool may execute in bash
2. **Use POSIX-compatible syntax** for simple commands
3. **Use explicit paths** when a tool might not be in PATH: `/opt/homebrew/bin/node` instead of `node`
4. **Never rely on aliases** — they don't load in non-interactive shells
5. **Test with `which`** before using a tool: `which node >/dev/null 2>&1 && node --version`
6. **Quote everything** — prevents both bash and zsh word splitting surprises
7. **Avoid globs without protection** — use `setopt NULL_GLOB` or check matches first

### Template for Reliable Commands

```bash
# Check if tool exists before using it
if command -v node >/dev/null 2>&1; then
  node --version
else
  echo "node not found. Try: /bin/zsh --login -c 'node --version'"
fi
```

---

-----
March 4, 2026

#AI/Claude
