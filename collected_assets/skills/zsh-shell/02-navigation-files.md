# Chapter 2: Navigation & File Management

## WHY This Matters

Every development task starts with files. Opening a project, finding a config, checking a log, moving assets, cleaning builds — it's all file work. A developer who navigates the filesystem slowly is slow at everything. A developer who can find any file in seconds and restructure a project in one command has a compounding advantage.

GUIs show you one folder at a time and require clicks for every action. The terminal shows you anything, anywhere, instantly — and lets you act on hundreds of files in one line.

---

## Concepts

### The Filesystem Is a Tree

Your entire computer is organized as a tree of directories (folders) starting from the root `/`. Every file has a unique path from that root.

```
/                          ← root (the top)
├── Users/
│   └── marty/             ← your home directory ($HOME or ~)
│       ├── Documents/
│       ├── Desktop/
│       ├── code/          ← where projects typically live
│       │   └── my-app/
│       │       ├── src/
│       │       ├── tests/
│       │       └── package.json
│       ├── .zshrc         ← hidden (starts with .)
│       └── .ssh/          ← hidden directory
├── opt/
│   └── homebrew/          ← Homebrew on Apple Silicon
├── usr/
│   ├── bin/               ← system commands
│   └── local/             ← user-installed tools (Intel Mac)
└── tmp/                   ← temporary files (cleared on reboot)
```

**Absolute paths** start from root: `/Users/marty/code/my-app`
**Relative paths** start from where you are: `code/my-app` (if you're in your home directory)

### Hidden Files

Files starting with `.` are hidden by default. They're not secret — they're just kept out of the way. Configuration files (`.zshrc`, `.gitignore`, `.env`) are almost always hidden. This is a Unix convention: settings shouldn't clutter your normal file view.

### Permissions

Every file has three permission sets: owner, group, everyone. Each set controls read (r), write (w), and execute (x). This is how Unix prevents one user from deleting another's files, and how your system stops you from accidentally modifying critical system files.

---

## Exploration

### Exercise 1: Moving Around

```zsh
cd ~
pwd
```
`cd ~` goes to your home directory. `~` is a shortcut for `$HOME`. You'll use this dozens of times a day.

```zsh
cd /
ls
```
Go to the filesystem root and see what's there. These top-level directories are the skeleton of your entire system.

```zsh
cd -
```
Go back to where you just were. This is like the "back" button. Incredibly useful when jumping between two directories.

```zsh
cd ~/Documents
cd ..
pwd
```
`..` means "parent directory" — one level up. Where are you now?

### Exercise 2: Listing Files

```zsh
cd ~
ls
```
Basic listing — just names.

```zsh
ls -l
```
Long format. Each line shows: permissions, link count, owner, group, size, date, name. This is the view you use when you need to know more than just names.

```zsh
ls -la
```
Long format + hidden files. Now you see `.zshrc`, `.ssh/`, `.gitconfig`, and all the configuration that makes your environment yours.

```zsh
ls -lah
```
Add human-readable sizes. `4.0K` instead of `4096`. Easier to scan.

```zsh
ls -lt
```
Sort by modification time, newest first. When you're looking for "what changed recently?" this is the answer.

### Exercise 3: Creating Structure

```zsh
mkdir -p ~/playground/project/{src,tests,docs,assets}
```
Creates the entire directory tree in one command. `-p` means "create parent directories as needed." The `{a,b,c}` syntax is **brace expansion** — it generates multiple arguments from a pattern.

```zsh
ls -R ~/playground/project
```
`-R` means recursive — show everything in all subdirectories.

```zsh
touch ~/playground/project/README.md
touch ~/playground/project/src/{index.ts,utils.ts,types.ts}
touch ~/playground/project/tests/{index.test.ts,utils.test.ts}
```
`touch` creates empty files (or updates timestamps on existing ones). Combined with brace expansion, you can scaffold a project's file structure in seconds.

### Exercise 4: Copying, Moving, Removing

```zsh
cp ~/playground/project/README.md ~/playground/project/docs/
```
Copy a file. The original stays.

```zsh
mv ~/playground/project/docs/README.md ~/playground/project/docs/guide.md
```
Move (or rename). The original is gone — this is a rename operation.

```zsh
rm ~/playground/project/docs/guide.md
```
Remove. **There is no trash can.** `rm` is permanent. This is why experienced developers pause before running `rm` with wildcards.

```zsh
rm -rf ~/playground
```
Remove a directory and everything inside it, without asking. `-r` is recursive, `-f` is force. **This is the most dangerous command in your toolkit.** Triple-check the path before running it.

WHY this matters: In CI/CD pipelines and deployment scripts, `rm -rf` cleans build artifacts. One wrong variable in the path and you delete the wrong thing. Understanding file operations deeply prevents disasters.

### Exercise 5: Finding Files

```zsh
find ~ -name "*.zshrc" -maxdepth 1
```
Find files by name. `-maxdepth 1` limits search to just the home directory (not subdirectories).

```zsh
find ~/code -name "*.ts" -type f | head -20
```
Find all TypeScript files in your code directory. `-type f` means files only (not directories). `head -20` shows only the first 20 results.

```zsh
find . -name "node_modules" -type d -prune
```
Find all `node_modules` directories. `-prune` stops descending into them (they're huge).

```zsh
find . -name "*.log" -mtime +30
```
Find log files not modified in the last 30 days. `-mtime +30` means "modified more than 30 days ago." This is how you find stale files for cleanup.

WHY `find` matters: When a build fails because of a stale config file somewhere in a nested directory, `find` locates it in seconds. When you need to clean up all `.DS_Store` files before a commit, `find` + `rm` does it in one line.

### Exercise 6: Permissions

```zsh
ls -la ~/.ssh/
```
Look at the permissions. SSH key files should be `600` (owner read/write only). If they're more permissive, SSH will refuse to use them — this is a security feature.

```zsh
stat -f "%Sp %N" ~/.zshrc
```
Show permissions in human-readable format for a specific file.

```zsh
chmod 755 ~/playground/project/src/index.ts 2>/dev/null || echo "Create the playground first"
```
`chmod` changes permissions. `755` means: owner can read/write/execute, everyone else can read/execute. This is the standard permission for scripts you want to run.

Permission numbers: read=4, write=2, execute=1. Add them: 7=rwx, 5=rx, 4=r.

---

## Discovery

### Discovery 1
```zsh
mkdir -p ~/playground/test
cd ~/playground/test
touch .hidden-file visible-file
ls
ls -a
```
How many files do you see with `ls` vs `ls -a`? Why would you want files to be hidden by default?

### Discovery 2
```zsh
ln -s ~/.zshrc ~/playground/zshrc-link
ls -la ~/playground/zshrc-link
cat ~/playground/zshrc-link
```
This creates a **symbolic link** — a pointer to another file. What happens when you read the link? What would happen if you deleted the original `.zshrc`? Symlinks are how your system connects tools to multiple locations (Homebrew uses them extensively).

### Discovery 3
```zsh
du -sh ~/Documents/* 2>/dev/null | sort -rh | head -10
```
What is this showing you? `du` measures disk usage, `-s` summarizes per directory, `-h` makes sizes human-readable, `sort -rh` sorts largest first. When your disk is full, this is how you find what's eating the space.

### Discovery 4
```zsh
file ~/.zshrc
file /bin/zsh
file ~/Desktop/*.png 2>/dev/null || echo "No PNG files on Desktop"
```
The `file` command tells you what a file actually IS, regardless of its extension. A `.txt` file might actually be a script. A file with no extension might be an image. `file` looks at the content, not the name.

---

## Capstone: Project Scaffolding Script

Write a script that creates a standardized project folder structure. When you run it with a project name, it should:

1. Create the project directory with subdirectories: `src/`, `tests/`, `docs/`, `assets/`, `scripts/`
2. Create starter files: `README.md` (with the project name as a heading), `.gitignore`, `src/index.ts`, `tests/index.test.ts`
3. Initialize a git repository
4. Report what it created (file count, directory count, total structure)

**Save it as:** `~/bin/scaffold.sh`

**Starter structure** (only if needed):
```zsh
#!/usr/bin/env zsh
# scaffold.sh — Create a new project structure
# Usage: scaffold.sh <project-name>

project_name=$1

if [ -z "$project_name" ]; then
  echo "Usage: scaffold.sh <project-name>"
  exit 1
fi

# Your code here...
```

**Make it executable:** `chmod +x ~/bin/scaffold.sh`

**Stretch goal:** Accept a second argument for project type (`node`, `python`, `static`) and adjust the file structure accordingly.

**What this connects to:** In Chapter 4 (Scripting), you'll learn conditionals and loops that make this script smarter. In Chapter 7 (Dev Environment), you'll build a full team onboarding script. This capstone is step one.

---

## Key Takeaways

- The filesystem is a tree rooted at `/`. Your home is `~`. Navigate with `cd`, see with `ls`, find with `find`.
- Hidden files (`.name`) store configuration. `ls -a` reveals them.
- `mkdir -p` and brace expansion `{a,b,c}` create complex structures in one command
- `rm` is permanent — there is no undo. Develop the habit of checking paths before deleting.
- `find` is your search engine for the filesystem — by name, type, size, age, permissions
- Permissions control who can read, write, and execute. SSH keys must be `600`, scripts must be `755`.
- Symlinks connect files across locations without duplicating them

---

-----
March 4, 2026

#AI/Claude
