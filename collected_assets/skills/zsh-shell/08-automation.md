# Chapter 8: Automation for Real Work

## WHY This Matters

A script you run manually is a tool. A script that runs itself is infrastructure. The difference is reliability — humans forget, get busy, or make mistakes. Automated scripts run on schedule, every time, the same way.

Monitoring your project's health, cleaning up old files, backing up databases, checking for dependency vulnerabilities — these are tasks that matter most when you forget to do them. Automation makes "I forgot" impossible.

---

## Concepts

### Scheduling on macOS

macOS has two scheduling systems:
- **cron** — the traditional Unix scheduler. Simple, well-documented, works everywhere.
- **launchd** — Apple's replacement. More powerful, macOS-native, survives reboots better.

Both work. Cron is simpler to learn; launchd is more robust for always-on tasks.

### Argument Parsing

Real scripts need flags and options (`--verbose`, `--output file.txt`). Zsh provides `zparseopts` for this — more capable than bash's `getopts`.

### Logging

Scripts that run unattended need logs. When something fails at 3 AM, the log is all you have to figure out what happened.

---

## Exploration

### Exercise 1: Argument Parsing with zparseopts

```zsh
cat > ~/bin/demo-args.sh << 'EOF'
#!/usr/bin/env zsh

# Parse arguments
local -a verbose output help
zparseopts -D -E v=verbose -verbose=verbose o:=output -output:=output h=help -help=help

if [[ -n $help ]]; then
  echo "Usage: demo-args.sh [-v|--verbose] [-o|--output FILE] [args...]"
  echo "  -v, --verbose    Show detailed output"
  echo "  -o, --output     Write output to file"
  echo "  -h, --help       Show this help"
  exit 0
fi

[[ -n $verbose ]] && echo "Verbose mode ON"
[[ -n $output ]] && echo "Output file: ${output[2]}"
echo "Remaining args: $@"
EOF
chmod +x ~/bin/demo-args.sh
```

Try:
```zsh
~/bin/demo-args.sh --help
~/bin/demo-args.sh -v --output report.txt file1 file2
~/bin/demo-args.sh file1 file2
```

### Exercise 2: Logging Pattern

```zsh
cat > ~/bin/with-logging.sh << 'EOF'
#!/usr/bin/env zsh
setopt ERR_EXIT NO_UNSET PIPE_FAIL

LOG_FILE="${HOME}/logs/$(basename $0 .sh)-$(date +%Y%m%d).log"
mkdir -p "$(dirname $LOG_FILE)"

log() {
  local level=$1; shift
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOG_FILE"
}

log INFO "Script started"
log INFO "User: $USER, Host: $(hostname)"

# Your work here
if command -v node > /dev/null 2>&1; then
  log INFO "Node version: $(node --version)"
else
  log WARN "Node not found"
fi

log INFO "Script completed"
EOF
chmod +x ~/bin/with-logging.sh
```

The `log()` function writes to both screen AND file. When this runs unattended, you can check the log later. The date-stamped filename means each day gets its own log.

### Exercise 3: File Watching

```zsh
cat > ~/bin/watch-changes.sh << 'EOF'
#!/usr/bin/env zsh
# Watch a directory for changes and run a command

dir=${1:-.}
echo "Watching $dir for changes... (Ctrl+C to stop)"

# Get initial state
last_hash=$(find "$dir" -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -exec stat -f "%m %N" {} \; 2>/dev/null | md5)

while true; do
  sleep 2
  current_hash=$(find "$dir" -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -exec stat -f "%m %N" {} \; 2>/dev/null | md5)
  
  if [ "$current_hash" != "$last_hash" ]; then
    echo "[$(date '+%H:%M:%S')] Change detected!"
    last_hash=$current_hash
    # Run your command here, e.g.:
    # npm test
  fi
done
EOF
chmod +x ~/bin/watch-changes.sh
```

WHY file watching matters: "Run tests when code changes" is the fastest feedback loop in development. Professional tools (nodemon, chokidar) do this, but understanding the mechanism helps you build custom watchers for any workflow.

### Exercise 4: Cron Jobs

```zsh
# View current cron jobs
crontab -l

# Edit cron jobs
crontab -e
```

Cron syntax:
```
┌──── minute (0-59)
│ ┌── hour (0-23)
│ │ ┌── day of month (1-31)
│ │ │ ┌── month (1-12)
│ │ │ │ ┌── day of week (0-7, 0 and 7 are Sunday)
│ │ │ │ │
* * * * *  command
```

Examples:
```
# Every day at 9 AM
0 9 * * * ~/bin/health-check.sh >> ~/logs/health.log 2>&1

# Every Monday at 8 AM
0 8 * * 1 ~/bin/weekly-report.sh >> ~/logs/weekly.log 2>&1

# Every 30 minutes
*/30 * * * * ~/bin/quick-check.sh >> ~/logs/check.log 2>&1
```

**Important:** Cron runs in a minimal environment. Your `.zshrc` isn't loaded. Use absolute paths for everything, or source your environment at the top of cron scripts.

### Exercise 5: launchd (macOS Native)

```zsh
cat > ~/Library/LaunchAgents/com.user.healthcheck.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.healthcheck</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/zsh</string>
        <string>-l</string>
        <string>-c</string>
        <string>$HOME/bin/health-check.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$HOME/logs/health-launchd.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/logs/health-launchd-error.log</string>
</dict>
</plist>
EOF

# Load the job
launchctl load ~/Library/LaunchAgents/com.user.healthcheck.plist

# Check it's loaded
launchctl list | grep healthcheck

# Unload when done
# launchctl unload ~/Library/LaunchAgents/com.user.healthcheck.plist
```

WHY launchd over cron: launchd survives reboots, can trigger on file changes or network events (not just time), and integrates with macOS power management. For developer tasks, either works. For reliable scheduled work, launchd is more robust.

---

## Discovery

### Discovery 1
```zsh
crontab -l 2>/dev/null | wc -l
ls ~/Library/LaunchAgents/ 2>/dev/null
```
Do you have any scheduled tasks already? What might be running that you don't know about?

### Discovery 2
```zsh
# What environment does cron see?
echo '* * * * * env > /tmp/cron-env.txt' | crontab -
sleep 70
cat /tmp/cron-env.txt
crontab -r  # Remove the test job
```
Compare that environment to `env` in your terminal. What's missing?

---

## Capstone: Project Health Check

Build `~/bin/health-check.sh` — a weekly diagnostic for any git project:

1. Check for uncommitted changes (`git status`)
2. Check for unpushed commits (`git log @{u}..`)
3. Check for outdated dependencies (`npm outdated` or `uv pip list --outdated`)
4. Run the test suite and report pass/fail
5. Check disk usage of the project directory
6. Check for TODO/FIXME/HACK comments and count them
7. Generate a markdown report saved to `~/reports/health-YYYY-MM-DD.md`
8. Accept `--project <path>` argument, default to current directory

**Schedule it:** Set up a cron job or launchd agent to run weekly.

**What this connects to:** This is a real monitoring tool. In Chapter 9, you could extend it into an Oh My Zsh plugin that shows health status in your prompt.

---

## Key Takeaways

- `zparseopts` gives scripts professional argument parsing
- Logging with timestamps and levels makes unattended scripts debuggable
- Cron handles time-based scheduling. Launchd adds event-based triggers and survives reboots.
- Cron runs in a minimal environment — use absolute paths and source your config
- File watching enables automatic responses to changes
- The best automation is invisible — it runs, logs results, and only alerts you when something's wrong

---

-----
March 4, 2026

#AI/Claude
