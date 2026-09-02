# Oh My Zsh Guide

Installation, plugin ecosystem, theme customization, custom plugin authoring, and troubleshooting — with emphasis on how Oh My Zsh interacts with Claude Code.

---

## What Oh My Zsh Is

Oh My Zsh is an open-source framework for managing zsh configuration. It provides 300+ plugins, 150+ themes, and a structure for custom extensions. It's the most popular zsh framework, with 175k+ GitHub stars.

WHY it matters: Without Oh My Zsh, configuring zsh is manual and fragile. Oh My Zsh gives you a curated, community-maintained configuration system that saves hours of setup and provides features you didn't know you needed.

---

## Installation

```zsh
# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# This creates:
# ~/.oh-my-zsh/          — Framework installation
# ~/.zshrc               — Overwrites existing (backs up old as .zshrc.pre-oh-my-zsh)
```

After installation, your `~/.zshrc` will contain:
```zsh
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"       # Default theme
plugins=(git)                   # Default: only git plugin
source $ZSH/oh-my-zsh.sh
```

---

## Architecture

```
~/.oh-my-zsh/
├── themes/              # Built-in themes (150+)
├── plugins/             # Built-in plugins (300+)
├── lib/                 # Core library files
├── templates/           # Template .zshrc
├── tools/               # Installer, updater
└── custom/              # YOUR customizations (survives updates)
    ├── plugins/         # Custom plugins go here
    ├── themes/          # Custom themes go here
    └── *.zsh            # Any .zsh file here auto-loads
```

**The custom/ directory is sacred.** Everything in `~/.oh-my-zsh/custom/` survives Oh My Zsh updates. Put your personalizations here, not in the framework's directories.

---

## Plugins

### Enabling Plugins

In `~/.zshrc`, add plugin names to the plugins array:
```zsh
plugins=(
  git
  virtualenv
  node
  postgres
  zsh-autosuggestions
  zsh-syntax-highlighting
)
```

**Order matters** for some plugins. Put `zsh-syntax-highlighting` last — it needs to wrap all other widgets.

After editing, reload: `source ~/.zshrc` or open a new terminal tab.

### Recommended Plugin Stack

#### Development Workflow

| Plugin | What | WHY | Install |
|---|---|---|---|
| `git` | 80+ git aliases + prompt integration | Saves ~30 sec per git operation. `gst` instead of `git status`, `gco` instead of `git checkout`. | Built-in |
| `virtualenv` | Shows active Python venv in prompt | Prevents "wrong environment" debugging sessions. You see immediately which venv is active. | Built-in |
| `node` | Node.js version display + `node-docs` | Catches version mismatches before they cause cryptic errors. | Built-in |
| `postgres` | PostgreSQL aliases (`pgstart`, `pgstop`) | Database operations with long commands are error-prone. Aliases reduce mistakes on production. | Built-in |
| `npm` | npm completions + aliases | Tab-complete npm scripts, package names. `npmR` for `npm run`. | Built-in |
| `docker` | Docker completions | Tab-complete container names, image names, commands. Essential for containerized workflows. | Built-in |

#### Productivity

| Plugin | What | WHY | Install |
|---|---|---|---|
| `z` | Frecency directory jumping | `z project` instead of `cd ~/code/clients/acme/project`. Learns your patterns. | Built-in |
| `fzf` | Fuzzy finder integration | Search files, history, branches interactively. `Ctrl+R` becomes a searchable history. | Built-in (requires fzf: `brew install fzf`) |
| `zsh-autosuggestions` | Fish-like history suggestions | Shows ghost text of your most likely next command. Accept with right arrow. | External — see below |
| `zsh-syntax-highlighting` | Real-time command coloring | Red = broken command BEFORE you hit enter. Green = valid. Catches typos instantly. | External — see below |

#### Installing External Plugins

```zsh
# zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Then add to plugins array in `~/.zshrc`.

### Plugin Discovery

```zsh
# List all available built-in plugins
ls ~/.oh-my-zsh/plugins/

# See what a plugin provides (read its README)
cat ~/.oh-my-zsh/plugins/git/README.md

# List currently loaded plugins
echo ${plugins[*]}

# See all aliases from a specific plugin
alias | grep git     # Shows git plugin aliases
```

### Common git Plugin Aliases

| Alias | Command | When to use |
|---|---|---|
| `gst` | `git status` | Check what's changed |
| `gco` | `git checkout` | Switch branches |
| `gcb` | `git checkout -b` | Create + switch to new branch |
| `gp` | `git push` | Push to remote |
| `gl` | `git pull` | Pull from remote |
| `gd` | `git diff` | View changes |
| `ga` | `git add` | Stage files |
| `gc` | `git commit -v` | Commit with diff view |
| `gcmsg` | `git commit -m` | Commit with inline message |
| `glog` | `git log --oneline --decorate --graph` | Visual branch history |
| `gsta` | `git stash push` | Stash changes |
| `gstp` | `git stash pop` | Restore stashed changes |

---

## Themes

### Setting a Theme

In `~/.zshrc`:
```zsh
ZSH_THEME="gnzh"    # Or any theme name
```

### Theme: gnzh (Marty's theme)

The gnzh theme shows:
- Username and hostname
- Current directory (abbreviated)
- Git branch and status (when in a repo)
- Return code of last command (if non-zero)
- Timestamp

### Popular Themes

| Theme | Style | Shows |
|---|---|---|
| `robbyrussell` | Minimal | Arrow + directory + git branch |
| `gnzh` | Information-rich | User, host, dir, git, time, exit code |
| `agnoster` | Powerline-style | Segments with background colors (needs Powerline font) |
| `af-magic` | Clean two-line | Directory + git on line 1, prompt on line 2 |
| `powerlevel10k` | Highly configurable | Everything — requires separate install |

### Custom Theme Creation

Create a file in `~/.oh-my-zsh/custom/themes/mytheme.zsh-theme`:

```zsh
# Simple custom theme example
# Left prompt: directory + git
PROMPT='%F{cyan}%~%f $(git_prompt_info)%F{green}❯%f '

# Right prompt: time
RPROMPT='%F{gray}%T%f'

# Git prompt configuration
ZSH_THEME_GIT_PROMPT_PREFIX="%F{yellow}("
ZSH_THEME_GIT_PROMPT_SUFFIX=")%f "
ZSH_THEME_GIT_PROMPT_DIRTY=" %F{red}✗%f"
ZSH_THEME_GIT_PROMPT_CLEAN=" %F{green}✓%f"
```

Set in `~/.zshrc`: `ZSH_THEME="mytheme"`

### Prompt Variables Quick Reference

| Code | Output |
|---|---|
| `%n` | Username |
| `%m` | Hostname (short) |
| `%~` | Current directory (~ for home) |
| `%/` | Full path |
| `%T` | Time (HH:MM, 24h) |
| `%t` | Time (HH:MM, 12h) |
| `%D{%Y-%m-%d}` | Custom date format |
| `%?` | Last exit code |
| `%F{color}` | Start foreground color |
| `%f` | Reset foreground color |
| `%K{color}` | Start background color |
| `%k` | Reset background color |
| `%B` / `%b` | Bold on / off |

---

## Writing Custom Plugins

### Plugin Structure

```
~/.oh-my-zsh/custom/plugins/my-plugin/
├── my-plugin.plugin.zsh    # Required — main plugin file
├── _my-command              # Optional — completion file
└── README.md               # Optional but recommended
```

### Minimal Plugin Template

```zsh
# my-plugin.plugin.zsh

# ---- Configuration ----
MY_PLUGIN_DEFAULT=${MY_PLUGIN_DEFAULT:-"value"}

# ---- Functions ----
my-function() {
  echo "My plugin function: $1"
}

# ---- Aliases ----
alias mf='my-function'

# ---- Completions ----
# If you need tab completion for your functions:
_my-function() {
  local -a options
  options=('start:Start the service' 'stop:Stop the service' 'status:Check status')
  _describe 'my-function commands' options
}
compdef _my-function my-function
```

### Plugin with Project Detection

A useful pattern — detect if you're in a specific type of project and set up accordingly:

```zsh
# node-project.plugin.zsh
# Auto-detect Node.js projects and set up convenience functions

node-project-check() {
  [ -f "package.json" ] && return 0 || return 1
}

# Run when changing directories
chpwd_functions+=(node-project-check-prompt)

node-project-check-prompt() {
  if node-project-check; then
    # Show Node version in right prompt when in a Node project
    RPROMPT="%F{green}⬡ $(node -v 2>/dev/null)%f"
  else
    RPROMPT=""
  fi
}
```

---

## Troubleshooting

### Slow Startup

**Symptom:** New terminal tabs take 2+ seconds to open.

**Diagnosis:**
```zsh
# Time your startup
time zsh -i -c exit

# Profile line-by-line (shows which lines are slow)
# Add to top of ~/.zshrc:
zmodload zsh/zprof
# Add to bottom of ~/.zshrc:
zprof

# Open new tab — profiling output shows at the top
```

**Common culprits:**
- nvm initialization (~200-500ms). Fix: use Oh My Zsh nvm plugin with lazy loading
- Completion system rebuild. Fix: only rebuild weekly with `autoload -Uz compinit && compinit -C`
- Too many plugins. Fix: audit with `echo ${plugins[*]}` — disable unused ones
- External plugin checks (autosuggestions, syntax highlighting). Usually fast; update if slow.

**Target:** Under 500ms for comfortable interactive use.

### Claude Code Can't See Oh My Zsh

**Symptom:** Oh My Zsh aliases and functions don't work in Claude Code.

**Root cause:** Claude Code runs non-interactive. Oh My Zsh loads in `~/.zshrc` which only runs for interactive shells.

**Fix:** Don't try to load Oh My Zsh in Claude Code. Instead:
- Use full commands instead of aliases (`git status` not `gst`)
- If a function is essential, copy it to a standalone script
- Use `/bin/zsh --login -c 'command'` only when truly needed

**Philosophy:** Claude Code doesn't need a pretty prompt or alias shortcuts. It needs tools to be in PATH and scripts to execute correctly. Focus on `~/.zshenv` for Claude Code compatibility.

### Plugin Conflicts

**Symptom:** Unexpected behavior after adding a new plugin.

**Diagnosis:**
```zsh
# Check for duplicate aliases
alias | sort | uniq -d -f1

# Temporarily disable a plugin (comment it out in plugins array)
# Then source ~/.zshrc and test

# Check which plugin provides a function
whence -v function_name
type function_name
```

### Oh My Zsh Update

```zsh
# Update Oh My Zsh
omz update

# Update custom plugins manually
cd ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && git pull
cd ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting && git pull
```

---

## Navigating Unfamiliar Configurations

When Claude encounters a user's Oh My Zsh setup for the first time:

1. **Detect the setup:**
   ```zsh
   echo "Theme: $ZSH_THEME"
   echo "Plugins: ${plugins[*]}"
   ls ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/ 2>/dev/null
   ```

2. **Check for custom aliases that might conflict:**
   ```zsh
   alias | wc -l     # How many aliases are defined?
   alias | head -30   # What do the first 30 look like?
   ```

3. **Before defining anything new, check if it exists:**
   ```zsh
   # Before creating an alias
   alias | grep "^my-alias="
   # Before creating a function
   whence -v my-function
   ```

4. **Understand the user's prompt** to know what information they're used to seeing (git status, node version, Python env, etc.)

---

-----
March 4, 2026

#AI/Claude
