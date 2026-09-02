# Zsh Environment Setup Guide

How zsh loads configuration, where tools live on macOS, and how to ensure your development environment works everywhere — including inside Claude Code.

---

## Config File Loading Order

Zsh loads different config files depending on how the shell was started. Understanding this is essential for diagnosing "works in my terminal but not in Claude Code" issues.

### Login Interactive Shell (opening Terminal.app)

```
/etc/zshenv       → System-wide, always runs first
~/.zshenv         → User, always runs (MOST RELIABLE)
/etc/zprofile     → System-wide login setup
~/.zprofile       → User login setup
/etc/zshrc        → System-wide interactive config
~/.zshrc          → User interactive config (OH MY ZSH LIVES HERE)
/etc/zlogin       → System-wide post-login
~/.zlogin         → User post-login
```

### Non-Login Interactive Shell (new tab in existing terminal)

```
/etc/zshenv       → System-wide
~/.zshenv         → User
/etc/zshrc        → System-wide interactive
~/.zshrc          → User interactive (OH MY ZSH LIVES HERE)
```

### Non-Interactive Shell (running a script, Claude Code bash tool)

```
/etc/zshenv       → System-wide
~/.zshenv         → User — THIS IS THE ONLY USER FILE THAT LOADS
```

### What This Means in Practice

| If you put it in... | It's available in... | Use for... |
|---|---|---|
| `~/.zshenv` | Every context: scripts, Claude Code, cron, interactive | PATH, critical env vars, language settings |
| `~/.zprofile` | Login shells only (terminal app open, SSH login) | One-time login messages, login-specific setup |
| `~/.zshrc` | Interactive shells only (terminal tabs, new windows) | Oh My Zsh, aliases, prompt, plugins, completions |
| `~/.zlogin` | After .zshrc in login shells | Rarely needed — post-login tasks |

### The Golden Rule

**If Claude Code needs to see it, put it in `~/.zshenv`.** Everything else goes in `~/.zshrc`.

Recommended `~/.zshenv`:
```zsh
# ~/.zshenv — loaded in ALL contexts including scripts and Claude Code

# Homebrew (Apple Silicon)
if [ -d "/opt/homebrew" ]; then
  export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:$PATH"
fi

# Homebrew (Intel)
if [ -d "/usr/local/Homebrew" ]; then
  export PATH="/usr/local/bin:/usr/local/sbin:$PATH"
fi

# User local binaries (pip, npm global, Claude Code)
export PATH="$HOME/.local/bin:$PATH"

# Editor
export EDITOR="code"  # or vim, nano, etc.
```

---

## macOS-Specific Paths

### Architecture Detection

```bash
arch=$(uname -m)
if [ "$arch" = "arm64" ]; then
  echo "Apple Silicon (M1/M2/M3/M4)"
  # Homebrew: /opt/homebrew/bin
elif [ "$arch" = "x86_64" ]; then
  echo "Intel Mac"
  # Homebrew: /usr/local/bin
fi
```

### Standard macOS PATH Order

After Homebrew and user additions, a typical macOS PATH looks like:

```
/opt/homebrew/bin          # Homebrew binaries (Apple Silicon)
/opt/homebrew/sbin         # Homebrew system binaries
~/.local/bin               # User local (pip, Claude Code)
~/.nvm/versions/node/v20/bin  # Active Node version (from nvm)
/usr/local/bin             # System local binaries
/usr/bin                   # System binaries
/bin                       # Core binaries
/usr/sbin                  # System admin
/sbin                      # Core admin
```

**PATH order matters:** First match wins. If Homebrew's `python3` is in `/opt/homebrew/bin` and the system `python3` is in `/usr/bin`, the Homebrew version runs because it appears earlier in PATH.

---

## Tool-Specific Setup

### Homebrew

```zsh
# Install (if not present)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Apple Silicon post-install (add to ~/.zshenv)
eval "$(/opt/homebrew/bin/brew shellenv)"

# Essential maintenance
brew update          # Update Homebrew itself
brew upgrade         # Upgrade all packages
brew cleanup         # Remove old versions
brew doctor          # Diagnose issues
```

### nvm (Node Version Manager)

```zsh
# Install
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Add to ~/.zshrc (NOT .zshenv — nvm is slow to load)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Lazy loading (faster startup — recommended for Oh My Zsh users)
# Use the nvm plugin instead of manual setup:
# plugins=(... nvm ...)
# The Oh My Zsh nvm plugin supports lazy loading automatically

# Usage
nvm install 20       # Install Node 20 LTS
nvm use 20           # Switch to Node 20
nvm alias default 20 # Set default version
node --version       # Verify

# .nvmrc per project
echo "20" > .nvmrc   # In project root
nvm use              # Reads .nvmrc automatically
```

WHY nvm matters: Different projects need different Node versions. Without nvm, you're stuck on one version system-wide, and updating Node can break existing projects.

### uv (Python Package Manager)

```zsh
# Install
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to ~/.zshenv
export PATH="$HOME/.local/bin:$PATH"

# Usage
uv python install 3.12    # Install Python 3.12
uv python list             # Show installed versions
uv init my-project         # Create new project with pyproject.toml
uv add requests            # Add dependency
uv sync                    # Install all dependencies
uv run python script.py    # Run with project's Python

# Virtual environments
uv venv                    # Create .venv
source .venv/bin/activate  # Activate (works in both bash and zsh)
```

WHY uv matters: It's 10-100x faster than pip for dependency resolution and installation. It replaces pip, virtualenv, pip-tools, and pipx with a single tool. It uses lockfiles for reproducible installs, which pip doesn't support natively.

### git Configuration

```zsh
# Identity
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Default branch
git config --global init.defaultBranch main

# Useful defaults
git config --global pull.rebase true
git config --global push.autoSetupRemote true
git config --global core.editor "code --wait"

# SSH key (Ed25519 — current best practice)
ssh-keygen -t ed25519 -C "your@email.com"
eval "$(ssh-agent -s)"
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# Add to ~/.ssh/config
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

---

## Environment Variables

### Best Practices

```zsh
# Project-specific: use .env files (never commit these)
echo "DATABASE_URL=postgres://localhost/mydb" > .env
echo ".env" >> .gitignore

# Load .env in scripts:
set -a                    # Auto-export all variables
source .env
set +a

# System-wide: use ~/.zshenv for persistent vars
export EDITOR="code"
export LANG="en_US.UTF-8"
```

### Common Environment Variables

| Variable | Purpose | Where to set |
|---|---|---|
| `PATH` | Command search path | `~/.zshenv` |
| `EDITOR` | Default text editor | `~/.zshenv` |
| `SHELL` | Current shell path | Set by system |
| `HOME` | User home directory | Set by system |
| `LANG` | Locale settings | `~/.zshenv` |
| `NVM_DIR` | nvm installation | `~/.zshrc` |
| `ZSH` | Oh My Zsh installation | `~/.zshrc` |
| `NODE_ENV` | Node environment | Per-project `.env` |
| `DATABASE_URL` | Database connection | Per-project `.env` (NEVER in shell config) |

### Secrets Management

**Never put secrets in shell config files.** These files are often backed up, synced, or accidentally committed.

- API keys → project `.env` files (gitignored)
- SSH keys → `~/.ssh/` with proper permissions (700 for dir, 600 for keys)
- Database passwords → project `.env` or a secrets manager
- Tokens → macOS Keychain via `security` command

```bash
# Store a secret in macOS Keychain
security add-generic-password -a "$USER" -s "my-api-key" -w "secret-value"

# Retrieve it
security find-generic-password -a "$USER" -s "my-api-key" -w
```

---

-----
March 4, 2026

#AI/Claude
