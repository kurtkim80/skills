# Bash ↔ Zsh Syntax Cheatsheet

A translation table for writing shell commands that work correctly in the target shell. Organized by category with side-by-side examples.

---

## Getting Help — The `man` Ecosystem

Before searching the web, check your local documentation. It's faster, works offline, and is guaranteed to match your installed version.

### `man` — The Manual

Every command on your system has a manual page. This is the authoritative reference — not Stack Overflow, not a blog post. The man page matches the exact version of the tool installed on YOUR machine.

```bash
man grep          # Full documentation for grep
man -k "search"   # Search all man pages for "search" keyword (same as apropos)
man 1 printf      # Shell command printf (section 1)
man 3 printf      # C library printf (section 3)
```

**Manual sections** — when a name exists in multiple contexts:

| Section | Content | Example |
|---|---|---|
| 1 | User commands | `man 1 test` — the shell `test` command |
| 2 | System calls | `man 2 open` — the kernel open() call |
| 3 | Library functions | `man 3 printf` — C library printf |
| 4 | Special files | `man 4 tty` — terminal device |
| 5 | File formats | `man 5 crontab` — crontab file syntax |
| 7 | Miscellaneous | `man 7 regex` — regular expression syntax |
| 8 | System admin | `man 8 mount` — mount command (admin) |

WHY sections matter: `man printf` might show you the C function when you wanted the shell builtin. `man 1 printf` gets you the right one. When you're debugging a cron job, `man 5 crontab` shows you the file format (what goes in the file), while `man 1 crontab` shows you the command (how to edit it).

**Navigating man pages:**

| Key | Action |
|---|---|
| `Space` / `f` | Page forward |
| `b` | Page backward |
| `/pattern` | Search forward for "pattern" |
| `?pattern` | Search backward |
| `n` | Next search match |
| `N` | Previous search match |
| `q` | Quit |
| `h` | Help (shows all navigation keys) |
| `g` | Go to top |
| `G` | Go to bottom |

Man pages use `less` as the pager. Everything you know about `less` navigation works in `man`.

### `apropos` — Find the Right Man Page

When you know what you want to do but not which command does it:

```bash
apropos "compress"      # Find commands related to compression
apropos "permission"    # Find commands related to file permissions
apropos "network"       # Find networking tools
```

WHY this matters: There are thousands of commands on your system you've never heard of. `apropos` is how you discover them. It's the equivalent of searching your local toolbox before driving to the hardware store.

### `whatis` — One-Line Command Summary

```bash
whatis grep        # grep(1) - file pattern searcher
whatis chmod       # chmod(1) - change file modes or Access Control Lists
whatis curl wget   # Shows one-line description for each
```

### `tldr` — Community-Maintained Short Examples

Not built-in but widely installed. Shows practical examples instead of exhaustive documentation:

```bash
# Install via Homebrew
brew install tldr

tldr tar       # Shows common tar usage patterns
tldr grep      # Shows common grep examples
```

WHY to use both: `man` is the authoritative reference when you need to understand every flag and edge case. `tldr` is the quick-start when you just need the common patterns. Use `tldr` first, `man` when you need depth.

### Zsh-Specific: `run-help`

Zsh has a built-in help system that Oh My Zsh enhances:

```zsh
# In zsh, press ESC then H (or Alt+H) while typing a command
# to open its man page without leaving your command line

# Enable enhanced run-help (usually in .zshrc via Oh My Zsh):
autoload -Uz run-help
unalias run-help 2>/dev/null
alias help=run-help

# Now you can:
help git        # Opens git man page
help zsh        # Opens zsh man page
```

The run-help system also understands subcommands:
```zsh
# Type "git commit" then press ESC+H
# It opens man page for "git-commit", not just "git"
```

WHY this is powerful: You never have to leave your command entry to check documentation. You're typing a complex `find` command, you forget a flag — ESC+H opens the man page, you find the flag, close it, and your partially-typed command is still there.

### Built-in Help for Shell Builtins

Man pages cover external commands, but shell builtins (like `cd`, `export`, `alias`) have their own help:

```bash
# Bash:
help cd           # Bash builtin help
help export       # Shows usage for bash builtins

# Zsh:
man zshbuiltins   # All zsh builtins documented here
# Or with run-help enabled:
run-help cd       # Jumps to cd in zshbuiltins man page
```

---

## Arrays

| Feature | Bash | Zsh |
|---|---|---|
| **Indexing start** | 0-based | 1-based |
| **First element** | `${arr[0]}` | `${arr[1]}` |
| **Last element** | `${arr[-1]}` (bash 4.3+) | `${arr[-1]}` |
| **All elements** | `${arr[@]}` or `${arr[*]}` | `${arr[@]}` or `${arr[*]}` |
| **Length** | `${#arr[@]}` | `${#arr[@]}` |
| **Slice** | `${arr[@]:1:3}` | `${arr[2,4]}` |
| **Append** | `arr+=(item)` | `arr+=(item)` |
| **Declare** | `declare -a arr` | `typeset -a arr` |
| **Associative** | `declare -A` (bash 4+) | `typeset -A` (richer key types) |
| **Empty array + strict** | Crashes with `set -u` (bash 3.2) | Handles correctly |

### Array Examples

```bash
# Bash
fruits=(apple banana cherry)
echo "${fruits[0]}"     # apple
echo "${#fruits[@]}"    # 3

# Zsh
fruits=(apple banana cherry)
echo "${fruits[1]}"     # apple
echo "${#fruits[@]}"    # 3
```

Portable pattern (works in both):
```bash
# Use ${arr[@]} for iteration — works identically
for item in "${arr[@]}"; do echo "$item"; done
```

---

## Globbing

| Feature | Bash | Zsh |
|---|---|---|
| **No match behavior** | Passes literal glob | Error: `no matches found` |
| **Fix no-match** | Default behavior | `setopt NULL_GLOB` or `setopt NO_NOMATCH` |
| **Recursive glob** | `shopt -s globstar` then `**/*.ts` | `**/*.ts` (built-in) |
| **Negate pattern** | `shopt -s extglob` then `!(*.log)` | `setopt EXTENDED_GLOB` then `^*.log` |
| **Case-insensitive** | N/A without extglob | `setopt NO_CASE_GLOB` |
| **Dotfiles** | `shopt -s dotglob` | `setopt GLOB_DOTS` |

### Common Glob Patterns

```bash
# Zsh recursive glob (built-in, no setup needed)
ls **/*.ts                    # All .ts files in all subdirectories
ls **/*test*                  # All files containing "test" in name
ls **/(*.js|*.ts)             # All .js and .ts files

# Zsh extended glob (needs setopt EXTENDED_GLOB)
ls ^*.log                     # Everything except .log files
ls *.txt~important*           # .txt files except those matching "important"
```

---

## Parameter Expansion

| Feature | Bash | Zsh |
|---|---|---|
| **Default value** | `${var:-default}` | `${var:-default}` |
| **Assign default** | `${var:=default}` | `${var:=default}` |
| **Error if unset** | `${var:?error msg}` | `${var:?error msg}` |
| **Substring** | `${var:0:5}` | `${var[1,5]}` |
| **Replace first** | `${var/old/new}` | `${var/old/new}` |
| **Replace all** | `${var//old/new}` | `${var//old/new}` |
| **Uppercase** | `${var^^}` (bash 4+) | `${(U)var}` |
| **Lowercase** | `${var,,}` (bash 4+) | `${(L)var}` |
| **Length** | `${#var}` | `${#var}` |
| **String split** | Automatic (unquoted) | `${=var}` (explicit) or `${(s:/:)var}` |

---

## Word Splitting

This is the most subtle difference. Bash splits unquoted variables on whitespace by default. Zsh does NOT.

```bash
# Bash
files="one two three"
for f in $files; do echo $f; done
# Output: one \n two \n three

# Zsh (same code, different result!)
files="one two three"
for f in $files; do echo $f; done
# Output: one two three

# Zsh: explicit split
for f in ${=files}; do echo $f; done
# Output: one \n two \n three

# Zsh: split on specific delimiter
path="/usr/local/bin"
for p in ${(s:/:)path}; do echo $p; done
# Output: usr \n local \n bin
```

To make zsh behave like bash for word splitting:
```zsh
setopt SH_WORD_SPLIT
```

---

## Conditionals and Tests

| Feature | Bash | Zsh |
|---|---|---|
| **Test command** | `[ ]` or `[[ ]]` | `[ ]` or `[[ ]]` |
| **Regex match** | `[[ $var =~ pattern ]]` | `[[ $var =~ pattern ]]` |
| **Regex captures** | `${BASH_REMATCH[1]}` | `${match[1]}` |
| **String comparison** | `[[ $a == $b ]]` | `[[ $a == $b ]]` |
| **Arithmetic** | `(( x > 5 ))` | `(( x > 5 ))` |

Note: Regex capture variable names differ! Scripts using `BASH_REMATCH` break in zsh.

---

## Loops

```bash
# These work identically in both shells:
for i in 1 2 3; do echo $i; done
for file in *.txt; do echo $file; done
while read line; do echo $line; done < file.txt

# C-style for loop (both shells):
for ((i=0; i<10; i++)); do echo $i; done
```

---

## Functions

```bash
# Both syntaxes work in both shells:
function greet() { echo "Hello, $1"; }
greet() { echo "Hello, $1"; }

# Zsh extras:
# Anonymous functions (no name needed):
() { echo "I run immediately"; }

# Autoloaded functions (loaded on first call):
autoload -Uz my_function
```

---

## Prompt Customization

| Feature | Bash | Zsh |
|---|---|---|
| **Variable** | `PS1` | `PROMPT` (or `PS1`) |
| **Username** | `\u` | `%n` |
| **Hostname** | `\h` | `%m` |
| **Working dir** | `\w` | `%~` |
| **Full path** | `\w` | `%/` |
| **Time** | `\t` | `%T` (24h) or `%t` (12h) |
| **Date** | `\d` | `%D{%Y-%m-%d}` |
| **Exit code** | `$?` in PS1 | `%?` |
| **Colors** | `\[\e[32m\]` | `%F{green}` ... `%f` |
| **Right prompt** | N/A | `RPROMPT` |

Zsh's color syntax is much cleaner:
```zsh
# Zsh
PROMPT='%F{green}%n%f@%F{blue}%m%f:%F{yellow}%~%f$ '
RPROMPT='%F{gray}%T%f'

# Bash (same result, much uglier)
PS1='\[\e[32m\]\u\[\e[0m\]@\[\e[34m\]\h\[\e[0m\]:\[\e[33m\]\w\[\e[0m\]$ '
```

---

## Shell Options

| Feature | Bash | Zsh |
|---|---|---|
| **Enable option** | `shopt -s optname` | `setopt OPTNAME` |
| **Disable option** | `shopt -u optname` | `unsetopt OPTNAME` |
| **List enabled** | `shopt -s` | `setopt` |
| **List all** | `shopt` | `set -o` |

### Common Options Translation

| Bash | Zsh | What it does |
|---|---|---|
| `shopt -s extglob` | `setopt EXTENDED_GLOB` | Advanced pattern matching |
| `shopt -s globstar` | *(built-in)* | Recursive `**` glob |
| `shopt -s dotglob` | `setopt GLOB_DOTS` | Include hidden files in globs |
| `shopt -s nocaseglob` | `setopt NO_CASE_GLOB` | Case-insensitive globs |
| `set -e` | `setopt ERR_EXIT` | Exit on error |
| `set -u` | `setopt NO_UNSET` | Error on undefined variables |
| `set -o pipefail` | `setopt PIPE_FAIL` | Pipeline fails if any command fails |

---

## Script Headers

### Bash-only script
```bash
#!/usr/bin/env bash
set -euo pipefail
```

### Zsh-only script
```zsh
#!/usr/bin/env zsh
setopt ERR_EXIT NO_UNSET PIPE_FAIL
```

### Cross-compatible script
```bash
#!/usr/bin/env bash
# Works in both bash and zsh
set -euo pipefail

# Add zsh compatibility if running in zsh
if [ -n "${ZSH_VERSION:-}" ]; then
  setopt SH_WORD_SPLIT
  setopt NO_NOMATCH
fi
```

---

-----
March 4, 2026

#AI/Claude
