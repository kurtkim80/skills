# Chapter 7: Dev Environment Mastery

## WHY This Matters

"Works on my machine" is the most expensive sentence in software development. It means the gap between your environment and production (or your teammate's machine, or CI) is wide enough for bugs to hide in. Every tool version mismatch, every missing environment variable, every undocumented dependency is a potential hours-long debugging session.

Managing your dev environment explicitly — knowing exactly what's installed, at which version, configured how — turns that chaos into reproducibility. When a new team member can run one script and have a working environment in 10 minutes, that's the payoff.

---

## Exploration

### Exercise 1: Homebrew Mastery

```zsh
# What's installed?
brew list | head -20
brew list --cask | head -10     # GUI apps installed via Homebrew

# What's outdated?
brew outdated

# Full maintenance cycle
brew update          # Update Homebrew itself and formulae list
brew upgrade         # Upgrade all outdated packages
brew cleanup         # Remove old versions (reclaim disk space)
brew doctor          # Diagnose problems
```

```zsh
# Search for tools
brew search node
brew info node           # Version, dependencies, caveats

# Install with specific version
brew install node@20     # Install Node 20 specifically
```

WHY Homebrew matters: Without it, installing developer tools on macOS means hunting for `.dmg` files, dragging apps, and losing track of versions. Homebrew makes tools manageable, updatable, and removable through one interface.

### Exercise 2: Node Version Management with nvm

```zsh
# Check current setup
node --version
which node
echo $NVM_DIR

# List installed versions
nvm ls

# Install and switch
nvm install 20       # Install latest Node 20
nvm install 22       # Install latest Node 22
nvm use 20           # Switch to 20

# Set default
nvm alias default 20

# Per-project version
echo "20" > .nvmrc   # In project root
nvm use              # Reads .nvmrc
```

WHY version management matters: Your production server runs Node 20. Your legacy project requires Node 18. A new library needs Node 22. Without nvm, you're stuck on one version. With it, you switch in one command.

### Exercise 3: Python Management with uv

```zsh
# Check if uv is installed
which uv || echo "Install: curl -LsSf https://astral.sh/uv/install.sh | sh"

# List available Python versions
uv python list

# Install a specific Python
uv python install 3.12

# Create a new project
mkdir ~/playground/py-demo && cd ~/playground/py-demo
uv init

# Add dependencies (10-100x faster than pip)
uv add requests
uv add pytest --dev

# Run with project's Python
uv run python -c "import requests; print(requests.__version__)"

# Sync environment from lockfile (reproducible installs)
uv sync
```

WHY uv matters: pip installs packages globally by default, has no lockfile, and dependency resolution can take minutes. uv is 10-100x faster, creates lockfiles for reproducibility, and manages virtual environments automatically. It's replacing the pip+virtualenv+pip-tools stack.

### Exercise 4: Git Configuration

```zsh
# View current config
git config --global --list

# Essential settings
git config --global core.editor "code --wait"
git config --global pull.rebase true
git config --global push.autoSetupRemote true
git config --global init.defaultBranch main

# Useful aliases (beyond Oh My Zsh plugin)
git config --global alias.unstage "reset HEAD --"
git config --global alias.last "log -1 HEAD"
git config --global alias.visual "log --oneline --graph --all"
```

### Exercise 5: SSH Key Setup

```zsh
# Check existing keys
ls -la ~/.ssh/

# Generate Ed25519 key (current best practice)
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to SSH agent with Keychain (macOS)
eval "$(ssh-agent -s)"
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# Configure SSH for GitHub
cat >> ~/.ssh/config << 'EOF'
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
EOF

# Copy public key to clipboard (add to GitHub)
pbcopy < ~/.ssh/id_ed25519.pub
echo "Public key copied to clipboard — paste in GitHub settings"
```

### Exercise 6: Environment Variables and .env Patterns

```zsh
# Create a project .env file
cat > ~/playground/py-demo/.env << 'EOF'
DATABASE_URL=postgres://localhost:5432/mydb
API_KEY=dev-key-not-real
NODE_ENV=development
EOF

# Add to .gitignore (CRITICAL — never commit .env files)
echo ".env" >> ~/playground/py-demo/.gitignore

# Load in a script
set -a
source ~/playground/py-demo/.env
set +a
echo "DB: $DATABASE_URL"
```

WHY `.env` matters: Hardcoding a database URL or API key means it ends up in git history — permanently. `.env` files keep secrets local, configurable per environment (dev/staging/prod), and out of version control.

---

## Discovery

### Discovery 1
```zsh
brew deps --tree node
```
What does this show? Why does knowing dependency trees matter when debugging "something broke after I updated"?

### Discovery 2
```zsh
echo $PATH | tr ':' '\n' | grep -n "node\|nvm\|homebrew\|opt"
```
Where do your dev tools sit in PATH? Which would win if two versions of `node` existed in different PATH entries?

---

## Capstone: Team Onboarding Script

Write `~/bin/setup-dev-env.sh` — a script a new team member runs to go from a fresh Mac to a working dev environment:

1. Check/install Homebrew
2. Install core tools via Homebrew (git, wget, jq)
3. Install/configure nvm and a default Node version
4. Install/configure uv and a default Python version
5. Configure git (prompt for name and email)
6. Set up Oh My Zsh with recommended plugins
7. Verify everything works — run each tool and report status
8. Output a summary of what was installed and configured

Each step should check if the tool is already present before installing. Use color output for status (green=OK, yellow=skipped, red=failed). Log everything to `~/setup-dev-env.log`.

**What this connects to:** This is a real deliverable. You can give this to a teammate on day one.

---

## Key Takeaways

- Homebrew manages tools. nvm manages Node versions. uv manages Python. Use all three.
- Version management prevents "works on my machine" — pin versions per project
- SSH keys (Ed25519) and proper git config are one-time setup with permanent benefits
- `.env` files keep secrets out of git. Never commit credentials.
- An onboarding script turns hours of manual setup into minutes of automation
- Your dev environment is infrastructure — treat it as code, version it, document it

---

-----
March 4, 2026

#AI/Claude
