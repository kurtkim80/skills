# Chapter 3: Text Processing

## WHY This Matters

Software development runs on text. Code is text. Configs are text. Logs are text. API responses are text. Data exports are text. The developer who can slice, search, filter, transform, and combine text from the command line can debug in minutes what takes others hours.

When a production server throws 10,000 lines of logs and your app is down, the ability to instantly find the relevant error, extract the stack trace, and identify the pattern is not optional — it's the skill that gets the system back up.

---

## Concepts

### Pipes: The Unix Superpower

The single most important concept in shell productivity is the **pipe** (`|`). A pipe takes the output of one command and feeds it as input to the next. This lets you build processing chains from simple tools.

```zsh
command1 | command2 | command3
```

Each command does one thing well. Pipes compose them into workflows. This is the Unix philosophy in action: small, focused tools that combine into powerful pipelines.

### Streams: stdin, stdout, stderr

Every command has three streams:
- **stdin** (0) — input (usually your keyboard, or piped data)
- **stdout** (1) — normal output (what you see on screen)
- **stderr** (2) — error output (also on screen, but a separate stream)

```zsh
command > file.txt     # stdout → file (overwrite)
command >> file.txt    # stdout → file (append)
command 2> errors.txt  # stderr → file
command &> all.txt     # both → file
command < input.txt    # file → stdin
```

WHY this matters: When a CI/CD pipeline runs your tests, it captures stdout and stderr separately. Understanding streams is how you control what gets logged, what gets displayed, and what gets ignored.

---

## Exploration

### Exercise 1: Reading Files

```zsh
cat ~/.zshrc
```
`cat` outputs the entire file. Good for short files. For your `.zshrc`, it shows your complete shell configuration.

```zsh
head -20 ~/.zshrc
```
First 20 lines. Use when you want to see a file's structure without reading all of it.

```zsh
tail -20 ~/.zshrc
```
Last 20 lines. In log files, the most recent entries are at the bottom — `tail` shows you what just happened.

```zsh
tail -f /var/log/system.log
```
`-f` means "follow" — it keeps watching the file and shows new lines as they appear. This is how you monitor live logs. Press `Ctrl+C` to stop.

```zsh
wc -l ~/.zshrc
```
Line count. `wc` stands for "word count" but `-l` counts lines. Quick way to measure file size in human terms.

```zsh
less ~/.zshrc
```
Interactive reader — same as what `man` uses. Navigate with Space, `b`, `/search`, `q` to quit. Use `less` for files too long to `cat`.

### Exercise 2: grep — Finding Text

`grep` searches for patterns in text. It's the most-used text processing tool in software development.

```zsh
grep "alias" ~/.zshrc
```
Find every line containing "alias" in your zsh config. Instantly see all your aliases.

```zsh
grep -n "export" ~/.zshrc
```
`-n` adds line numbers. When you need to edit a specific line, this tells you exactly where to go.

```zsh
grep -r "TODO" ~/code/ 2>/dev/null | head -20
```
`-r` searches recursively through all files in a directory. Find every TODO comment in your codebase. `2>/dev/null` silences permission errors on directories you can't read.

```zsh
grep -i "error" /var/log/system.log | tail -10
```
`-i` means case-insensitive. Find errors regardless of capitalization (Error, ERROR, error).

```zsh
grep -c "import" ~/code/my-project/src/*.ts 2>/dev/null
```
`-c` counts matches per file instead of showing them. Quick way to see which files have the most imports — a rough complexity indicator.

```zsh
grep -v "^#" ~/.zshrc | grep -v "^$"
```
`-v` inverts the match — shows lines that DON'T match. `^#` means "starts with #" (comments). `^$` means "empty line." This pipeline strips comments and blanks, showing only active configuration.

WHY `grep` matters: In a 5,000-line log file from a failed deployment, `grep "ERROR"` reduces it to the 12 lines that matter. In a codebase with 500 files, `grep -r "deprecated"` finds every place you need to update. It's the developer's search engine for text.

### Exercise 3: Pipes in Action

```zsh
ls -la ~ | head -20
```
List home directory, show only first 20 items. This is the simplest pipe — one command's output becomes another's input.

```zsh
history | grep "git" | tail -10
```
Find your 10 most recent git commands. Three commands chained: history → filter → show last 10.

```zsh
ps aux | grep -i node | grep -v grep
```
Find running Node.js processes. The second `grep -v grep` removes the grep command itself from results (a classic trick — grep always finds itself in the process list).

```zsh
cat ~/.zshrc | wc -l
```
Count the lines in your zsh config. (You could also do `wc -l < ~/.zshrc` — same result, different style.)

```zsh
echo $PATH | tr ':' '\n' | sort | uniq
```
Show your PATH entries, one per line, sorted and deduplicated. `tr ':' '\n'` translates colons to newlines. `sort | uniq` removes duplicates (or use `sort -u`).

### Exercise 4: sort, uniq, cut — Data Shaping

Create a sample data file to work with:

```zsh
cat > /tmp/sample.csv << 'EOF'
name,department,city
Alice,Engineering,Chicago
Bob,Marketing,New York
Carol,Engineering,Chicago
Dave,Marketing,Chicago
Eve,Engineering,New York
Frank,HR,Chicago
Grace,Engineering,Chicago
Hank,Marketing,New York
EOF
```

Now process it:

```zsh
cut -d',' -f2 /tmp/sample.csv | tail -n +2 | sort | uniq -c | sort -rn
```

Break this down:
- `cut -d',' -f2` — extract the 2nd column (comma-delimited)
- `tail -n +2` — skip the header row
- `sort` — alphabetize (required before `uniq`)
- `uniq -c` — count consecutive duplicates
- `sort -rn` — sort numerically, descending

Result: how many people per department, ranked.

```zsh
cut -d',' -f3 /tmp/sample.csv | tail -n +2 | sort | uniq -c | sort -rn
```
Same pipeline, column 3: people per city. Change one number, get a different analysis.

### Exercise 5: sed — Stream Editing

`sed` transforms text as it flows through. It's the search-and-replace tool of the terminal.

```zsh
echo "Hello World" | sed 's/World/Terminal/'
```
`s/old/new/` substitutes the first match on each line.

```zsh
echo "error error error" | sed 's/error/warning/g'
```
`g` flag means global — replace ALL matches, not just the first.

```zsh
cat /tmp/sample.csv | sed 's/Chicago/CHI/g; s/New York/NYC/g'
```
Multiple substitutions in one sed. Abbreviate city names.

```zsh
cat /tmp/sample.csv | sed '1d'
```
Delete line 1 (the header). `1d` means "line 1, delete."

```zsh
sed -n '/Engineering/p' /tmp/sample.csv
```
`-n` suppresses default output. `/pattern/p` prints only matching lines. This is grep-like behavior in sed — useful when you need sed's other features in the same pipeline.

### Exercise 6: awk — Column Processing

`awk` processes text column by column. Where `grep` finds lines and `sed` transforms text, `awk` understands structure.

```zsh
awk -F',' '{print $1, $2}' /tmp/sample.csv
```
`-F','` sets comma as field separator. `$1` is column 1, `$2` is column 2. Print name and department.

```zsh
awk -F',' '$2 == "Engineering" {print $1}' /tmp/sample.csv
```
Print names of people in Engineering. `$2 == "Engineering"` is a condition — only matching rows are processed.

```zsh
awk -F',' 'NR > 1 {count[$2]++} END {for (dept in count) print dept, count[dept]}' /tmp/sample.csv
```
Count people per department using awk alone. `NR > 1` skips the header. `count[$2]++` builds a counter per department. `END` block runs after all input is processed.

WHY `awk` matters: When you need to process structured data (CSVs, TSVs, log files with fixed columns), awk does it in one line. No Python script needed, no imports, no file I/O boilerplate.

---

## Discovery

### Discovery 1
```zsh
echo "one\ntwo\nthree" | sort -r
```
What does `sort -r` do? What would `sort -rn` do differently on a list of numbers?

### Discovery 2
```zsh
echo "aaa\nbbb\naaa\nccc\nbbb\naaa" | sort | uniq -c | sort -rn
```
Predict the output. Why does `uniq` require `sort` first? What happens if you skip the sort?

### Discovery 3
```zsh
ls -la /usr/bin | awk '{print $5}' | sort -rn | head -5
```
What are the 5 largest files in `/usr/bin`? What is `$5` in `ls -la` output?

### Discovery 4
```zsh
grep -rl "function" ~/.oh-my-zsh/plugins/git/ 2>/dev/null | head -5
```
`-l` shows filenames only (not the matching lines). What does adding `-r` do? Why would you want filenames without content?

---

## Capstone: CSV Analysis Pipeline

Download or create a more substantial dataset (or use the sample above), then build a single pipeline that answers three questions. Your pipeline should:

1. **Count:** How many records per unique value in a chosen column?
2. **Filter:** Show only records matching a specific condition
3. **Transform:** Output the results in a different format (e.g., "Department: Engineering — 4 people")

**The pipeline should chain at least 4 commands with pipes.**

**Example using our sample data:**
```zsh
# How many people per city, formatted as a report?
tail -n +2 /tmp/sample.csv | cut -d',' -f3 | sort | uniq -c | sort -rn | awk '{printf "  %s: %d people\n", $2, $1}'
```

**Stretch goal:** Build a pipeline that processes your actual `.zsh_history` file to find your 10 most-used commands:
```zsh
# Hint: history entries have a format. You need to extract just the command name.
```

**What this connects to:** In Chapter 4 (Scripting), you'll wrap pipelines like these in functions and scripts with error handling. In Chapter 8 (Automation), you'll schedule them to run automatically.

---

## Key Takeaways

- Pipes (`|`) are the Unix superpower — they compose simple tools into powerful workflows
- `grep` finds text, `sed` transforms text, `awk` processes structured text
- Streams (stdin/stdout/stderr) control where data flows. Redirection (`>`, `>>`, `2>`) sends it to files.
- `sort | uniq -c | sort -rn` is the universal "count and rank" pattern
- `cut` extracts columns, `head`/`tail` extract rows, `wc` counts
- `man` + `apropos` tell you everything about these tools — check them when you need a flag you haven't used before
- Every data analysis question can be answered by composing these tools

---

-----
March 4, 2026

#AI/Claude
