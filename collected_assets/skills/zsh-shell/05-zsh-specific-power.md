# Chapter 5: Zsh-Specific Power

## WHY This Matters

Everything in Chapters 1-4 works in both bash and zsh. This chapter is about what zsh does that bash can't — the features that made Apple switch macOS to zsh. These aren't obscure tricks. They're daily productivity multipliers: better globbing, smarter arrays, powerful parameter expansion, and built-in features that replace entire external tools.

Understanding zsh-specific features means writing shorter, faster, more readable scripts — and knowing exactly why something works in your terminal but breaks in a bash CI pipeline.

---

## Exploration

### Exercise 1: Recursive Globbing (Built-In)

Bash requires `shopt -s globstar` to enable `**`. Zsh has it by default.

```zsh
# Find all TypeScript files in a project (no find command needed)
ls **/*.ts 2>/dev/null | head -20

# Find all test files
ls **/*test* 2>/dev/null | head -20

# Find all package.json files (reveals nested dependencies)
ls **/package.json 2>/dev/null | head -20
```

WHY this matters: In bash, this requires `find`. In zsh, it's native glob syntax — faster to type, easier to read, and it works everywhere globs work (loops, conditionals, arguments).

### Exercise 2: Extended Globbing

```zsh
setopt EXTENDED_GLOB

# Everything EXCEPT .log files
ls ^*.log 2>/dev/null

# Files modified today (glob qualifiers)
ls *(m0) 2>/dev/null

# Only directories
ls *(/) 2>/dev/null

# Only executable files
ls *(x) 2>/dev/null

# Files larger than 1MB
ls *(Lm+1) 2>/dev/null

# Files owned by you, modified in the last week
ls *(u:$USER:mw-1) 2>/dev/null
```

Glob qualifiers (the `(...)` after the pattern) are unique to zsh. They replace complex `find` commands with concise inline expressions.

| Qualifier | Meaning |
|---|---|
| `/` | Directories only |
| `.` | Regular files only |
| `x` | Executable files |
| `m-N` | Modified within N days |
| `Lm+N` | Larger than N MB |
| `u:name:` | Owned by user |
| `on` | Sort by name |
| `OL` | Sort by size, largest first |

### Exercise 3: Arrays Done Right

```zsh
# Zsh arrays are 1-based (bash is 0-based)
fruits=(apple banana cherry date elderberry)

echo "First: ${fruits[1]}"       # apple (bash: ${fruits[0]})
echo "Last: ${fruits[-1]}"       # elderberry
echo "Count: ${#fruits[@]}"      # 5
echo "Slice: ${fruits[2,4]}"     # banana cherry date

# Loop
for fruit in "${fruits[@]}"; do
  echo "  - $fruit"
done

# Array operations
fruits+=(fig)                     # append
echo "After append: ${fruits[@]}"

# Check if element exists
if (( ${fruits[(Ie)banana]} )); then
  echo "banana is in the array"
fi
```

```zsh
# Associative arrays (key-value pairs)
typeset -A project
project[name]="my-app"
project[version]="1.0.0"
project[language]="typescript"

echo "Project: ${project[name]} v${project[version]}"

# Iterate keys and values
for key in ${(k)project}; do
  echo "  $key: ${project[$key]}"
done
```

WHY this matters: Bash 3.2 (macOS default) doesn't support associative arrays at all. Zsh handles them natively with richer key types. When your script needs to map filenames to results, or track counts by category, zsh associative arrays do it without external tools.

### Exercise 4: Parameter Expansion Magic

Zsh has expansion flags that transform strings inline — no external commands needed.

```zsh
name="hello world"

# Case transformation
echo "${(U)name}"          # HELLO WORLD (uppercase)
echo "${(L)name}"          # hello world (lowercase)
echo "${(C)name}"          # Hello World (capitalize words)

# String operations
text="path/to/some/file.txt"
echo "${text:h}"            # path/to/some (head — dirname)
echo "${text:t}"            # file.txt (tail — basename)
echo "${text:e}"            # txt (extension)
echo "${text:r}"            # path/to/some/file (root — no extension)

# Splitting and joining
path="/usr/local/bin"
parts=(${(s:/:)path})      # Split on /
echo "${parts[@]}"          # usr local bin
echo "${(j:-:)parts}"       # usr-local-bin (join with -)

# Length
echo "${#name}"             # 11 (character count)

# Padding
num=42
echo "${(l:5::0:)num}"     # 00042 (left-pad with zeros)
```

Compare to bash, where these require `tr`, `dirname`, `basename`, `cut`, or `printf` as external commands. In zsh, they're inline expansions — faster and more readable.

### Exercise 5: Spelling Correction

```zsh
setopt CORRECT
setopt CORRECT_ALL
```

Now try deliberately misspelling a command:
```zsh
sl       # Did you mean: ls?
gti      # Did you mean: git?
```

Zsh offers to correct typos before running them. In interactive use, this catches mistakes before they cause errors.

### Exercise 6: Anonymous Functions

```zsh
# Run a block of code in its own scope
() {
  local temp="I'm local"
  echo "$temp"
}
echo "${temp:-temp is not visible here}"
```

Anonymous functions create isolated scopes. Variables declared inside don't leak out. Use these when you need temporary variables without polluting the shell environment.

```zsh
# Practical: process a file with temporary variables
() {
  local count=0
  while IFS= read -r line; do
    ((count++))
  done < ~/.zshrc
  echo "Your .zshrc has $count lines"
}
```

---

## Discovery

### Discovery 1
```zsh
files=(*.txt(N))
echo "Found ${#files[@]} text files"
```
The `(N)` qualifier enables NULL_GLOB for just this one pattern. What happens without `(N)` when no `.txt` files exist? Why is this safer than setting `NULL_GLOB` globally?

### Discovery 2
```zsh
echo ${(o)$(echo "cherry apple banana date")}
echo ${(O)$(echo "cherry apple banana date")}
```
What do the `(o)` and `(O)` flags do? What would bash require to do this?

### Discovery 3
```zsh
# Create test files
touch /tmp/test-{a,b,c}.{txt,log,md}
# Now use glob qualifiers
ls /tmp/test-*(.om[1,3])
```
This shows the 3 most recently modified regular files. Can you predict which 3 before running it?

---

## Capstone: Lines-of-Code Analyzer

Write a zsh script (`~/bin/loc.sh`) that analyzes a project directory and reports:

1. File count by extension (using associative arrays)
2. Lines of code by extension (excluding blank lines and comments where possible)
3. Top 10 largest files by line count
4. Total project summary

**Requirements:** Must use at least 3 zsh-specific features (recursive glob, associative arrays, parameter expansion flags). Must work on any directory passed as an argument.

**Example output:**
```
Project: /Users/marty/code/my-app
─────────────────────────────
Files by type:
  .ts    24 files    1,847 lines
  .json   5 files      312 lines
  .md     3 files      156 lines
─────────────────────────────
Top 10 largest files:
  src/api/handler.ts         312 lines
  src/utils/parser.ts        245 lines
  ...
─────────────────────────────
Total: 32 files, 2,315 lines
```

**What this connects to:** This is a real developer tool. In Chapter 8 (Automation), you could schedule it to track code growth over time. In Chapter 9 (Advanced), you could turn it into an Oh My Zsh plugin that shows stats in your prompt.

---

## Key Takeaways

- Recursive globbing (`**/*.ts`) is built-in — no setup needed
- Glob qualifiers (`*(/)`, `*(m-1)`, `*(Lm+1)`) replace complex `find` commands
- Arrays are 1-based. Associative arrays work natively. Both are more capable than bash.
- Parameter expansion flags (`${(U)var}`, `${var:t}`, `${(s:/:)var}`) replace external commands
- Spelling correction (`setopt CORRECT`) catches typos interactively
- Anonymous functions `() { ... }` create safe, scoped code blocks
- Every zsh-specific feature you use is one less external command in your pipeline — faster and more portable within zsh environments

---

-----
March 4, 2026

#AI/Claude
