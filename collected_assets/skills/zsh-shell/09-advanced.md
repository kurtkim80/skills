# Chapter 9: Advanced — Custom Plugins, Debugging & Optimization

## WHY This Matters

Every developer has workflows unique to their team, project, or role. Off-the-shelf plugins get you 80% of the way. The last 20% — the part that makes YOUR terminal feel like it was built for YOU — requires writing your own tools.

This chapter takes you from user to toolmaker. You'll learn to debug shell scripts systematically, profile and optimize performance, and build an Oh My Zsh plugin that your team could install and benefit from. These are the skills that differentiate someone who uses the terminal from someone who shapes it.

---

## Exploration

### Exercise 1: Debugging with Trace Mode

```zsh
# Run any script with -x to see every command as it executes
zsh -x ~/bin/greet.sh
```

Each line prefixed with `+` shows the command after expansion. You see exactly what the shell is doing — variable values resolved, globs expanded, conditionals evaluated.

```zsh
# Debug a specific section of a script
cat > /tmp/debug-demo.sh << 'EOF'
#!/usr/bin/env zsh
echo "Before debug section"

setopt XTRACE    # Turn on tracing
name="world"
greeting="Hello, $name"
echo $greeting
unsetopt XTRACE  # Turn off tracing

echo "After debug section (not traced)"
EOF
zsh /tmp/debug-demo.sh
```

WHY trace debugging matters: When a script behaves unexpectedly, `echo` debugging is slow and incomplete. Trace mode shows you the actual execution flow — every branch taken, every variable expanded, every command run. It's `console.log` for the shell, but automatic.

### Exercise 2: Profiling Startup Time

```zsh
# Detailed startup profiling
# Add to TOP of ~/.zshrc (temporarily):
#   zmodload zsh/zprof
# Add to BOTTOM of ~/.zshrc (temporarily):
#   zprof

# Alternative: time individual sections
cat > /tmp/profile-zshrc.sh << 'EOF'
#!/usr/bin/env zsh
echo "Profiling .zshrc load times..."
echo "================================"

start_total=$EPOCHREALTIME

# Test Oh My Zsh load
start=$EPOCHREALTIME
source "$HOME/.oh-my-zsh/oh-my-zsh.sh" 2>/dev/null
end=$EPOCHREALTIME
printf "Oh My Zsh:     %.0fms\n" $(( ($end - $start) * 1000 ))

# Test compinit
start=$EPOCHREALTIME
autoload -Uz compinit && compinit -C
end=$EPOCHREALTIME
printf "Completions:   %.0fms\n" $(( ($end - $start) * 1000 ))

end_total=$EPOCHREALTIME
printf "================================\n"
printf "Total:         %.0fms\n" $(( ($end_total - $start_total) * 1000 ))
EOF
zsh /tmp/profile-zshrc.sh
```

### Exercise 3: Signal Handling and Cleanup

```zsh
cat > ~/bin/graceful.sh << 'EOF'
#!/usr/bin/env zsh

TEMP_DIR=$(mktemp -d)
echo "Working in: $TEMP_DIR"

# Cleanup function — runs on exit, interrupt, or error
cleanup() {
  echo "Cleaning up $TEMP_DIR..."
  rm -rf "$TEMP_DIR"
  echo "Done."
}

# Register cleanup for multiple signals
trap cleanup EXIT        # Normal exit
trap cleanup INT         # Ctrl+C
trap cleanup TERM        # Kill signal

# Simulate work
echo "Creating temporary files..."
touch "$TEMP_DIR"/{file1,file2,file3}.tmp
ls "$TEMP_DIR"

echo "Working... (press Ctrl+C to test cleanup)"
sleep 10

echo "Finished normally"
EOF
chmod +x ~/bin/graceful.sh
```

Run it and press Ctrl+C partway through. The cleanup function runs regardless of how the script exits. WHY: Scripts that create temp files, lock resources, or start background processes MUST clean up after themselves. `trap` guarantees it.

### Exercise 4: The Zsh Completion System

```zsh
# See how completion works
echo $fpath | tr ' ' '\n' | head -10
```

The `fpath` variable lists directories where zsh looks for completion functions. Every file named `_commandname` in these directories provides tab completion for that command.

```zsh
# Write a simple completion function
cat > ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/my-tools/_my-greet << 'EOF'
#compdef my-greet

# Completion for the greet script
_my-greet() {
  local -a names
  names=(
    'Alice:Team lead'
    'Bob:Backend developer'
    'Carol:Frontend developer'
    'Dave:DevOps engineer'
  )
  _describe 'team member' names
}

_my-greet "$@"
EOF
```

After reloading, typing `my-greet <TAB>` would show team member names with descriptions.

### Exercise 5: Building a Complete Oh My Zsh Plugin

Now put it all together — a real plugin with functions, aliases, completions, and configuration.

```zsh
# Create plugin directory
PLUGIN_DIR="${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/project-tools"
mkdir -p "$PLUGIN_DIR"

# Create the main plugin file
cat > "$PLUGIN_DIR/project-tools.plugin.zsh" << 'PLUGIN'
# project-tools — Oh My Zsh plugin for project workflow automation
# Author: Your Name
# Version: 1.0.0

# ============================================================
# Configuration (override in .zshrc before sourcing Oh My Zsh)
# ============================================================
PROJECT_TOOLS_DIR=${PROJECT_TOOLS_DIR:-"$HOME/code"}
PROJECT_TOOLS_EDITOR=${PROJECT_TOOLS_EDITOR:-"$EDITOR"}

# ============================================================
# Core Functions
# ============================================================

# Quick project navigation
proj() {
  local target="$PROJECT_TOOLS_DIR/$1"
  if [ -d "$target" ]; then
    cd "$target"
    echo "📂 $(basename $target)"
    
    # Show project context
    [ -f "package.json" ] && echo "   Node: $(node -v 2>/dev/null) | $(jq -r .name package.json 2>/dev/null)"
    [ -f "pyproject.toml" ] && echo "   Python: $(python3 --version 2>/dev/null)"
    [ -d ".git" ] && echo "   Git: $(git branch --show-current 2>/dev/null) | $(git log --oneline -1 2>/dev/null)"
  else
    echo "Project not found: $1"
    echo "Available projects:"
    ls -1 "$PROJECT_TOOLS_DIR" | sed 's/^/  /'
  fi
}

# Project status overview
proj-status() {
  local dir="${1:-$PROJECT_TOOLS_DIR}"
  echo "Project Status Report — $(date '+%Y-%m-%d %H:%M')"
  echo "════════════════════════════════════════════════"
  
  for project in "$dir"/*(N/); do
    local name=$(basename "$project")
    local branch="" dirty="" unpushed=""
    
    if [ -d "$project/.git" ]; then
      branch=$(git -C "$project" branch --show-current 2>/dev/null)
      dirty=$(git -C "$project" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
      unpushed=$(git -C "$project" log @{u}.. --oneline 2>/dev/null | wc -l | tr -d ' ')
      
      local status_icon="✓"
      [ "$dirty" -gt 0 ] && status_icon="●"
      [ "$unpushed" -gt 0 ] && status_icon="↑"
      
      printf "  %s %-20s  %-15s  %s changes  %s unpushed\n" \
        "$status_icon" "$name" "($branch)" "$dirty" "$unpushed"
    fi
  done
}

# Quick project search
proj-find() {
  local query=$1
  if [ -z "$query" ]; then
    echo "Usage: proj-find <search-term>"
    return 1
  fi
  
  grep -rl "$query" "$PROJECT_TOOLS_DIR" \
    --include="*.ts" --include="*.js" --include="*.py" --include="*.md" \
    2>/dev/null | head -20
}

# ============================================================
# Aliases
# ============================================================
alias pp="proj"
alias ps="proj-status"
alias pf="proj-find"

# ============================================================
# Completions
# ============================================================
_proj() {
  local -a projects
  projects=(${(f)"$(ls -1 $PROJECT_TOOLS_DIR 2>/dev/null)"})
  _describe 'project' projects
}
compdef _proj proj
compdef _proj pp

PLUGIN
```

Enable the plugin — add `project-tools` to your plugins array in `~/.zshrc`:
```zsh
plugins=(... project-tools)
```

Reload and test:
```zsh
source ~/.zshrc
proj <TAB>        # Tab completion shows your projects
proj-status       # Overview of all projects
```

---

## Discovery

### Discovery 1
```zsh
# What happens inside Oh My Zsh when it loads a plugin?
cat ~/.oh-my-zsh/lib/plugins.zsh 2>/dev/null || echo "Check oh-my-zsh source"
```
Understanding the plugin loading mechanism helps you debug when plugins don't work as expected.

### Discovery 2
```zsh
# How many functions does your shell currently have loaded?
print -l ${(k)functions} | wc -l
print -l ${(k)functions} | grep "^git" | head -10
```
Every plugin adds functions. How many are from the git plugin alone?

---

## Capstone: Your Workflow Plugin

Build a custom Oh My Zsh plugin tailored to your specific workflow. It should include:

1. **At least 3 functions** that automate tasks you do repeatedly
2. **Tab completion** for at least one function (project names, common arguments)
3. **Configuration variables** that users can override in `.zshrc`
4. **A prompt segment** (optional) that shows relevant context (project name, status indicator)
5. **A README.md** explaining installation and usage

Package it as an installable plugin:
```
~/.oh-my-zsh/custom/plugins/your-plugin/
├── your-plugin.plugin.zsh
├── _your-command               # Completion file
└── README.md
```

**Ideas for plugin focus:**
- Training coordination (status of training sessions, upcoming deadlines)
- Code review helper (list open PRs, show review status)
- Deploy assistant (environment checks, version bumps, release notes)
- Database toolkit (connection shortcuts, backup triggers, migration status)

**Stretch goal:** Publish to GitHub so others can install it with:
```zsh
git clone https://github.com/you/your-plugin \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/your-plugin
```

**What this connects to:** Everything. This capstone uses terminal foundations (Ch 1), file management (Ch 2), text processing (Ch 3), scripting (Ch 4), zsh features (Ch 5), Oh My Zsh (Ch 6), dev environment knowledge (Ch 7), and automation patterns (Ch 8). It's the synthesis of the entire curriculum.

---

## Key Takeaways

- `zsh -x` (trace mode) shows every command as it executes — the best debugging tool for shell scripts
- `zprof` profiles startup time. Optimize what's slow, remove what's unused.
- `trap` ensures cleanup happens regardless of how a script exits
- The zsh completion system (`compdef`, `_describe`) adds tab completion to any function
- Oh My Zsh plugins are just directories with a `.plugin.zsh` file — there's no magic
- Building your own tools is how you go from terminal user to terminal power user
- Every capstone in this curriculum produced a real tool. Together, they form your personal toolkit.

---

## What's Next

You've completed the curriculum. Here's where to go from here:

- **Polish your dotfiles** — put your `.zshrc`, custom plugins, and scripts in a git repo. This is your portable environment.
- **Contribute to Oh My Zsh** — found a bug? Missing a feature? The framework is open source.
- **Share your plugin** — if it solves a real problem, others probably have the same problem.
- **Keep exploring** — `man zshall` is 30,000+ lines of documentation. There's always more to discover.

---

-----
March 4, 2026

#AI/Claude
