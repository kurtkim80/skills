# Chapter 4: Scripting Basics

## WHY This Matters

Every time you run the same sequence of commands more than twice, you've found a script waiting to be written. A script takes a 10-minute manual process and turns it into a 1-second automated one — and it runs the same way every time, without typos, without forgotten steps, without "I think I did this last time."

Scripts are how individual productivity becomes team productivity. When you write a setup script, every new team member gets the same environment. When you write a deploy script, every release follows the same process. Automation is reliability.

---

## Concepts

### What Is a Script?

A script is a text file containing shell commands that run in sequence. Instead of typing commands one at a time, you write them in a file and run the file. That's it — no compilation, no special tooling.

```zsh
#!/usr/bin/env zsh
# This line (shebang) tells the system which shell to use
echo "Hello from a script"
```

### Variables: Storing and Reusing Values

Variables store text (strings) or numbers. They eliminate repetition and make scripts flexible.

```zsh
name="World"
echo "Hello, $name"    # Hello, World
```

**Quoting rules** — this trips up everyone at some point:
- Double quotes `"$var"` — expands variables (use this most of the time)
- Single quotes `'$var'` — literal text, no expansion
- No quotes `$var` — expands AND splits on whitespace (dangerous in bash, safe in zsh)

### Exit Codes: How Commands Report Success or Failure

Every command returns a number when it finishes: 0 means success, anything else means failure. This is how scripts make decisions.

```zsh
ls /tmp          # exits 0 (success)
ls /nonexistent  # exits 1 or 2 (failure)
echo $?          # shows the exit code of the last command
```

---

## Exploration

### Exercise 1: Your First Script

Create a file:
```zsh
cat > ~/bin/greet.sh << 'EOF'
#!/usr/bin/env zsh
echo "Hello, $USER!"
echo "Today is $(date +%A), $(date +%B) $(date +%d)."
echo "You're in: $(pwd)"
EOF
chmod +x ~/bin/greet.sh
```

Run it:
```zsh
~/bin/greet.sh
```

You just wrote and executed a script. The `chmod +x` makes it executable — without that, the system won't run it.

### Exercise 2: Variables and Arguments

```zsh
cat > ~/bin/welcome.sh << 'EOF'
#!/usr/bin/env zsh

# Script arguments are $1, $2, $3...
name=${1:-"stranger"}    # Use first argument, or "stranger" as default
greeting=${2:-"Hello"}   # Second argument, or "Hello"

echo "$greeting, $name!"
echo "Script name: $0"
echo "Number of arguments: $#"
echo "All arguments: $*"
EOF
chmod +x ~/bin/welcome.sh
```

Try:
```zsh
~/bin/welcome.sh
~/bin/welcome.sh Marty
~/bin/welcome.sh Marty "Good morning"
```

`${1:-default}` is the **default value** pattern. If the argument is missing, use the default. This prevents scripts from crashing on missing input.

### Exercise 3: Conditionals

```zsh
cat > ~/bin/check-tool.sh << 'EOF'
#!/usr/bin/env zsh

tool=${1:?"Usage: check-tool.sh <tool-name>"}

if command -v "$tool" > /dev/null 2>&1; then
  echo "✓ $tool is installed at: $(which $tool)"
  echo "  Version: $($tool --version 2>/dev/null | head -1)"
else
  echo "✗ $tool is NOT installed"
  echo "  Try: brew install $tool"
fi
EOF
chmod +x ~/bin/check-tool.sh
```

Try:
```zsh
~/bin/check-tool.sh git
~/bin/check-tool.sh node
~/bin/check-tool.sh nonexistent-tool
~/bin/check-tool.sh
```

The `${1:?message}` pattern exits with an error if the argument is missing. The `command -v` check is the portable way to test if a command exists — more reliable than `which`.

**Conditional syntax:**
```zsh
if [ condition ]; then
  # true branch
elif [ other-condition ]; then
  # other branch
else
  # default
fi
```

Common test operators:
- `-z "$var"` — string is empty
- `-n "$var"` — string is not empty
- `-f "$path"` — file exists
- `-d "$path"` — directory exists
- `-eq`, `-ne`, `-gt`, `-lt` — numeric comparisons
- `=`, `!=` — string comparisons

### Exercise 4: Loops

```zsh
# For loop — iterate over a list
for fruit in apple banana cherry; do
  echo "I like $fruit"
done
```

```zsh
# For loop — iterate over files
for file in ~/bin/*.sh; do
  echo "Script: $(basename $file) — $(wc -l < $file) lines"
done
```

```zsh
# While loop — repeat until condition is false
count=1
while [ $count -le 5 ]; do
  echo "Count: $count"
  ((count++))
done
```

```zsh
# Loop over command output
for dir in $(ls -d ~/code/*/ 2>/dev/null); do
  echo "Project: $(basename $dir)"
done
```

### Exercise 5: Functions

Functions are reusable blocks of code within a script (or your `.zshrc`).

```zsh
# Define a function
mkcd() {
  mkdir -p "$1" && cd "$1"
  echo "Created and moved to: $(pwd)"
}

# Use it
mkcd ~/playground/new-project
```

Add useful functions to your `~/.zshrc` and they're available in every terminal session. Functions are better than aliases for anything with logic — aliases are simple text substitution, functions can have conditionals, loops, and local variables.

### Exercise 6: Error Handling

```zsh
cat > ~/bin/safe-delete.sh << 'EOF'
#!/usr/bin/env zsh
setopt ERR_EXIT      # Exit on any error
setopt NO_UNSET      # Error on undefined variables
setopt PIPE_FAIL     # Pipeline fails if any command fails

target=${1:?"Usage: safe-delete.sh <path>"}

# Safety checks
if [ ! -e "$target" ]; then
  echo "Error: $target does not exist" >&2
  exit 1
fi

if [ "$target" = "/" ] || [ "$target" = "$HOME" ]; then
  echo "Error: Refusing to delete $target" >&2
  exit 1
fi

# Confirm before deletion
echo "About to delete: $target"
echo -n "Are you sure? (y/N) "
read response
if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
  rm -rf "$target"
  echo "Deleted: $target"
else
  echo "Cancelled."
fi
EOF
chmod +x ~/bin/safe-delete.sh
```

Key patterns:
- `setopt ERR_EXIT` — stop immediately on errors (don't keep running broken code)
- `>&2` — send error messages to stderr (separate from normal output)
- `exit 1` — exit with failure code
- Confirm destructive actions with user input

---

## Discovery

### Discovery 1
```zsh
echo "Exit code: $?"
false
echo "Exit code: $?"
true
echo "Exit code: $?"
```
What exit codes do `true` and `false` return? Why do these commands exist?

### Discovery 2
```zsh
[ -f ~/.zshrc ] && echo "exists" || echo "missing"
[ -f ~/.nonexistent ] && echo "exists" || echo "missing"
```
This is the **short-circuit** pattern: `A && B || C` means "if A succeeds, do B; otherwise do C." Where have you seen this pattern in other programming languages?

### Discovery 3
```zsh
for i in {1..5}; do echo $i; done
for i in {01..12}; do echo "month-$i.csv"; done
for letter in {a..z}; do echo -n "$letter "; done; echo
```
Brace expansion generates sequences. What would `{1..100..5}` produce?

---

## Capstone: Backup Script

Write a script called `~/bin/backup.sh` that:

1. Takes a directory path as an argument
2. Validates the directory exists
3. Creates a timestamped zip archive (e.g., `backup-2026-03-04-143022.zip`)
4. Saves the archive to `~/backups/`
5. Logs the backup to `~/backups/backup.log` with timestamp, source, archive name, and size
6. Reports success or failure with appropriate exit codes
7. Handles errors gracefully (missing directory, zip failure, disk space)

**Stretch goal:** Add a `--dry-run` flag that shows what would happen without doing it.

**What this connects to:** In Chapter 8 (Automation), you'll schedule this script to run automatically. In Chapter 5 (Zsh Power), you'll enhance it with zsh-specific features.

---

## Key Takeaways

- Scripts are text files of shell commands with a shebang (`#!/usr/bin/env zsh`) at the top
- Variables store values. Arguments (`$1`, `$2`) make scripts flexible. Defaults (`${1:-value}`) prevent crashes.
- Exit codes (0=success, non-zero=failure) drive conditional logic
- `if/elif/else/fi` for branching. `for/while/do/done` for looping.
- Functions are reusable blocks — put common ones in `~/.zshrc`
- Error handling (`setopt ERR_EXIT`, exit codes, stderr) makes scripts reliable
- Always validate input and confirm destructive actions

---

-----
March 4, 2026

#AI/Claude
