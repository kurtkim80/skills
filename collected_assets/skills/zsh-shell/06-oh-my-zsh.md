# Chapter 6: Oh My Zsh

## WHY This Matters

Every time you type `git status` instead of `gst`, you spend 9 extra keystrokes. Do that 50 times a day, 250 days a year — that's 112,500 unnecessary keystrokes annually. Oh My Zsh reclaims that time with aliases, completions, and visual feedback that makes the terminal feel like an IDE.

But Oh My Zsh isn't just about saving keystrokes. It's about **information density** — seeing your git branch, Python environment, Node version, and directory all in your prompt without running separate commands. It's about **discoverability** — tab completing commands you didn't know existed. And it's about **community** — 300+ plugins maintained by thousands of contributors solving the same problems you're solving.

---

## Exploration

### Exercise 1: Installation (Skip if Already Installed)

Check first:
```zsh
[ -d "$HOME/.oh-my-zsh" ] && echo "Already installed" || echo "Not installed"
```

If not installed:
```zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

After installation, open a new terminal tab. Your prompt will look different — that's the `robbyrussell` default theme.

### Exercise 2: Understanding Your Configuration

```zsh
grep "^ZSH_THEME" ~/.zshrc
grep "^plugins" ~/.zshrc
```

For Marty's setup, this shows `gnzh` and `(git virtualenv node postgres)`. Whatever yours shows, that's your starting point.

Now see what Oh My Zsh actually provides:

```zsh
# How many plugins are available?
ls ~/.oh-my-zsh/plugins/ | wc -l

# How many themes?
ls ~/.oh-my-zsh/themes/ | wc -l

# What's in your current plugin set?
echo "Loaded plugins: ${plugins[*]}"
```

### Exercise 3: The git Plugin Deep Dive

The git plugin is probably already in your config. See what it gives you:

```zsh
# List all git aliases
alias | grep "^g" | head -30
```

Try these in any git repo:
```zsh
gst          # git status
glog         # git log --oneline --decorate --graph
gd           # git diff
ga .         # git add .
gcmsg "test" # git commit -m "test" (careful — this actually commits)
```

```zsh
# See the full alias definition
alias gst
alias glog
```

WHY these aliases matter: `gst` → `git status` saves 7 keystrokes. But more importantly, it reduces friction. When checking status is effortless, you check it more often, which means fewer accidental commits to the wrong branch and fewer "I forgot to add that file" moments.

### Exercise 4: Adding Plugins

Edit your `.zshrc` — find the `plugins=(...)` line:

```zsh
# Before (example):
plugins=(git)

# After (add useful ones):
plugins=(
  git
  virtualenv
  node
  postgres
  z
  zsh-autosuggestions
  zsh-syntax-highlighting
)
```

**Install the external plugins first** (they're not built-in):

```zsh
# zsh-autosuggestions — fish-like ghost text suggestions
git clone https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# zsh-syntax-highlighting — real-time command coloring
git clone https://github.com/zsh-users/zsh-syntax-highlighting \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Reload:
```zsh
source ~/.zshrc
```

Now type a command slowly and watch: autosuggestions show ghost text from your history. Syntax highlighting colors your input — green means valid, red means the command doesn't exist.

### Exercise 5: Theme Customization

See your current theme:
```zsh
echo $ZSH_THEME
```

Try a different one temporarily:
```zsh
# Preview without editing .zshrc
source ~/.oh-my-zsh/themes/af-magic.zsh-theme
```

Not permanent — just for this session. Open a new tab to go back to your configured theme.

**Create your own theme:**

```zsh
cat > ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/my-dev.zsh-theme << 'THEME'
# Custom dev theme
# Shows: user, directory, git branch+status, node version, time

# Colors
local user_color="%F{cyan}"
local dir_color="%F{yellow}"
local git_color="%F{green}"
local time_color="%F{gray}"
local reset="%f"

# Git prompt config
ZSH_THEME_GIT_PROMPT_PREFIX="${git_color}("
ZSH_THEME_GIT_PROMPT_SUFFIX=")${reset} "
ZSH_THEME_GIT_PROMPT_DIRTY=" %F{red}✗%f"
ZSH_THEME_GIT_PROMPT_CLEAN=" %F{green}✓%f"

# Node version (only in directories with package.json)
node_version() {
  if [ -f "package.json" ]; then
    echo "%F{green}⬡ $(node -v 2>/dev/null)%f "
  fi
}

# Left prompt
PROMPT='${user_color}%n${reset} ${dir_color}%~${reset} $(git_prompt_info)$(node_version)
%F{magenta}❯%f '

# Right prompt
RPROMPT='${time_color}%T${reset}'
THEME
```

Activate it:
```zsh
# In ~/.zshrc, change:
ZSH_THEME="my-dev"
# Then:
source ~/.zshrc
```

### Exercise 6: Custom Aliases and Functions

The best place for personal customizations is `~/.oh-my-zsh/custom/`. Any `.zsh` file here auto-loads.

```zsh
cat > ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/my-aliases.zsh << 'EOF'
# Project navigation
alias code="cd ~/code"
alias dots="cd ~/.dotfiles 2>/dev/null || echo 'No dotfiles dir'"

# Shortcuts that save real time
alias ll="ls -lah"
alias ..="cd .."
alias ...="cd ../.."
alias cls="clear"

# Git extras beyond the plugin
alias gs="gst"                    # Even shorter git status
alias yolo="git push --force"     # Use wisely

# Dev workflow
alias nr="npm run"
alias nt="npm test"
alias ni="npm install"

# Quick edit configs
alias zshrc="$EDITOR ~/.zshrc"
alias reload="source ~/.zshrc && echo 'Reloaded!'"

# Safety nets
alias rm="rm -i"                  # Confirm before delete
alias mv="mv -i"                  # Confirm before overwrite
alias cp="cp -i"                  # Confirm before overwrite
EOF

source ~/.zshrc
```

### Exercise 7: Measuring Startup Performance

```zsh
# Time your shell startup
time zsh -i -c exit

# Goal: under 500ms
# If over 1 second, you have a performance problem
```

If startup is slow, profile it:
```zsh
# Add to TOP of ~/.zshrc:
zmodload zsh/zprof

# Add to BOTTOM of ~/.zshrc:
zprof
```

Open a new tab — the profiling output shows which functions took the most time. Common culprits: nvm (200-500ms), compinit (100-300ms), too many plugins.

**Fixes for common slow starters:**

```zsh
# Lazy-load nvm (saves 200-500ms)
# Use the Oh My Zsh nvm plugin instead of manual init
# It lazy-loads nvm on first use

# Cache completions (saves 100-300ms)
autoload -Uz compinit
if [ "$(find ~/.zcompdump -mtime +1 2>/dev/null)" ]; then
  compinit
else
  compinit -C    # Use cached completions
fi
```

---

## Discovery

### Discovery 1
```zsh
# With the z plugin loaded, navigate to a few directories:
cd ~/code
cd ~/Documents
cd ~/.oh-my-zsh

# Now try:
z code
z doc
```
How does `z` know where to go? It uses "frecency" — a combination of frequency and recency. The more you visit a directory, the higher it ranks.

### Discovery 2
```zsh
# With syntax highlighting, type these slowly:
echo "hello"     # What color?
echoo "hello"    # What color?
```
The color difference tells you whether a command exists BEFORE you run it. When is this most valuable?

### Discovery 3
```zsh
# Check the difference
time zsh -i -c exit                    # With all plugins
time zsh --no-rcs -i -c exit           # Without any config
```
The difference is your config's cost. Is it worth it?

---

## Capstone: Optimized Shell Environment

Configure Oh My Zsh to be both powerful and fast:

1. **Theme:** Create or customize a theme that shows: directory, git branch + status, node version (only when relevant), and time. Use your own color preferences.

2. **Plugins:** Enable at least 5 plugins. Document WHY each one earns its place (what time it saves, what errors it prevents).

3. **Aliases:** Create at least 5 custom aliases for commands you use daily. Put them in a custom `.zsh` file.

4. **Performance:** Measure startup time. Target under 500ms. If over, identify and fix the bottleneck.

5. **Document it:** Create a `~/.dotfiles/README.md` listing your theme, plugins, aliases, and startup time. This is the beginning of your dotfiles — a portable configuration you can replicate on any machine.

**What this connects to:** In Chapter 9 (Advanced), you'll write your own Oh My Zsh plugin. The theme and aliases you create here are the foundation.

---

## Key Takeaways

- Oh My Zsh provides 300+ plugins and 150+ themes through a managed framework
- The `git` plugin alone saves significant daily time with 80+ aliases
- External plugins (`autosuggestions`, `syntax-highlighting`) add IDE-like features to your terminal
- Custom themes put essential info (branch, version, env) in your prompt
- Custom aliases and functions go in `~/.oh-my-zsh/custom/*.zsh`
- Startup performance matters — profile with `zprof`, target under 500ms
- Your shell configuration is a tool. Invest in it like you invest in your editor config.

---

-----
March 4, 2026

#AI/Claude
