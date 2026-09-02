# Zsh Shell Curriculum — Overview

A progressive learning path from terminal basics to custom plugin development. Designed for bidirectional learning — you and Claude explore together.

---

## Before You Start

Run this in your terminal to confirm your setup:

```zsh
echo "Shell: $SHELL"
echo "Zsh version: $ZSH_VERSION"
echo "OS: $(sw_vers -productVersion 2>/dev/null || uname -s)"
echo "Architecture: $(uname -m)"
echo "Oh My Zsh: $([ -d "$HOME/.oh-my-zsh" ] && echo "Installed - Theme: ${ZSH_THEME:-unknown}" || echo "Not installed")"
```

Share the output with Claude to personalize your learning experience.

**Requirements:** macOS with zsh (default since Catalina 2019). No prior terminal experience needed — Chapter 1 starts from scratch.

**Oh My Zsh:** Not required for Chapters 1-5. Chapter 6 covers installation if you don't have it. If you already have it, Chapter 6 deepens your configuration.

---

## How to Use This Curriculum

**Start a lesson:** Tell Claude "Let's work on Chapter 1" or "I want to learn about shell scripting" and Claude will find the right chapter.

**Pace yourself:** Each chapter is designed for one focused session (30-60 minutes). The capstone may take an additional 15-30 minutes.

**Run everything in your real terminal.** These aren't theoretical exercises. You'll build real tools, write real scripts, and configure your real environment.

**Predict before you execute.** At discovery points, Claude will ask you to guess what a command will output. This is where the deepest learning happens — whether you're right or wrong.

**There are no wrong answers.** If something produces unexpected output, that's a learning moment for both you and Claude. Your environment is unique — what happens on your machine is data, not failure.

---

## Curriculum Map

| Ch | Title | You'll Learn WHY... | Capstone: You Build... |
|---|---|---|---|
| 1 | Terminal Foundations | ...your terminal is the most powerful tool in your dev environment | A system info one-liner that reports your full setup |
| 2 | Navigation & Files | ...speed with files saves hours weekly across every project | A project scaffolding script that creates standardized structures |
| 3 | Text Processing | ...80% of debugging is finding the right text in the right file | A CSV analysis pipeline that extracts insights in seconds |
| 4 | Scripting Basics | ...automation turns 10-minute tasks into 1-second scripts forever | A backup script with error handling and logging |
| 5 | Zsh-Specific Power | ...Apple chose zsh and what you gain over bash | A lines-of-code analyzer using zsh-only features |
| 6 | Oh My Zsh | ...plugins save 30+ minutes daily for developers who live in the terminal | Custom theme + aliases + startup optimization under 500ms |
| 7 | Dev Environment | ...version management prevents the "works on my machine" disaster | A team onboarding script that sets up a complete dev environment |
| 8 | Automation | ...scripts that run themselves are the foundation of reliable systems | A weekly project health check with scheduled execution |
| 9 | Advanced | ...building your own tools is how you go from user to power user | A custom Oh My Zsh plugin for your workflow |

---

## Dependencies Between Chapters

```
Ch 1 (Foundations)
 └─ Ch 2 (Navigation & Files)
     └─ Ch 3 (Text Processing)
         └─ Ch 4 (Scripting Basics)
             ├─ Ch 5 (Zsh Power)
             │   └─ Ch 6 (Oh My Zsh)
             │       └─ Ch 9 (Advanced)
             ├─ Ch 7 (Dev Environment)
             └─ Ch 8 (Automation)
```

Chapters 1-4 are sequential — each builds directly on the last. After Chapter 4, Chapters 5-8 can be taken in any order based on interest. Chapter 9 requires Chapter 6.

---

## Capstone Philosophy

Every capstone produces something you'll actually use. Not a toy exercise — a real tool that solves a real problem. Each capstone combines skills from its chapter AND all prior chapters, reinforcing the full learning path.

By Chapter 9, you'll have built: a system reporter, a project scaffolder, a data pipeline, a backup tool, a code analyzer, a customized shell environment, an onboarding script, an automated health check, and a custom plugin. That's a real toolkit.

---

-----
March 4, 2026

#AI/Claude
