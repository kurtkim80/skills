# Zsh Version Changelog

Track zsh features by version. When Claude detects the user's zsh version via `echo $ZSH_VERSION`, use this reference to know what's available and what isn't.

**How to check:** `echo $ZSH_VERSION`

**macOS default versions:**

| macOS Version | Zsh Version | Year |
|---|---|---|
| Catalina (10.15) | 5.7.1 | 2019 |
| Big Sur (11) | 5.8 | 2020 |
| Monterey (12) | 5.8.1 | 2021 |
| Ventura (13) | 5.9 | 2022 |
| Sonoma (14) | 5.9 | 2023 |
| Sequoia (15) | 5.9 | 2024 |

Users can also install newer versions via Homebrew: `brew install zsh`

---

## Zsh 5.9 (May 2022)

**Available on:** macOS Ventura+, Homebrew

Notable features:
- **Improved `typeset -g` scoping** in anonymous functions — no longer leaks to parent scope. WHY: Safer variable handling in scripts, reduces accidental side effects from sourced files.
- **Better Unicode support** in completion system — handles emoji and CJK characters more reliably in tab completion.
- **`zle -F` improvements** for file descriptor watching — enables more responsive async plugins.
- **Regex improvements** — better PCRE support when compiled with `--enable-pcre`.

## Zsh 5.8.1 (November 2021)

**Available on:** macOS Monterey, Homebrew

Bug fix release. Key fixes:
- Fixed completion system crashes with certain plugin combinations
- Fixed `vared` behavior with multiline values
- Memory leak fixes in parameter expansion

## Zsh 5.8 (February 2020)

**Available on:** macOS Big Sur+, Homebrew

Notable features:
- **Improved `vared`** for interactive variable editing — better cursor handling and line editing. WHY: More usable for scripts that prompt users for input with editing capabilities.
- **`${(Z)var}`** flag for shell parsing of strings — splits a string the same way the shell would parse a command line.
- **`print -v`** to print into a variable (like bash's `printf -v`). WHY: Avoids subshell overhead for string formatting.
- **Completion improvements** — better handling of `--option=value` style completions.

## Zsh 5.7.1 (February 2019)

**Available on:** macOS Catalina, Homebrew

Bug fix release for 5.7. Key fixes:
- Fixed multibyte character handling in vi mode
- Fixed prompt redisplay issues

## Zsh 5.7 (December 2018)

Notable features:
- **`NO_UNSET` improvements** — better error messages for unset variables.
- **Improved `[[` operator** — better pattern matching diagnostics.
- **`zparseopts` improvements** — the zsh option parser became more robust. WHY: Makes writing CLI tools in zsh more practical.

## Zsh 5.6 (September 2018)

Notable features:
- **Floating point arithmetic** improvements — better precision in `(( ))`.
- **`zmodload zsh/system`** additions — `sysread`/`syswrite` for low-level I/O.
- **New glob qualifiers** — additional file-matching capabilities.

## Zsh 5.5 (April 2018)

Notable features:
- **`${var:offset:length}`** substring extraction now works consistently (matching bash behavior more closely).
- **Improved `autoload`** — better error handling for function loading.

---

## Feature Availability Matrix

Use this to quickly check if a feature is safe to use based on the user's zsh version:

| Feature | Minimum Version | Safe on macOS Catalina+ |
|---|---|---|
| Recursive glob (`**`) | 3.0+ | Yes |
| Extended glob (`^`, `~`) | 3.0+ | Yes |
| Associative arrays | 4.0+ | Yes |
| `zparseopts` | 4.0+ | Yes |
| `pcre` module | 4.3+ (with compile flag) | Depends on build |
| `print -v` | 5.8+ | macOS Big Sur+ only |
| Improved `typeset -g` scoping | 5.9+ | macOS Ventura+ only |
| Anonymous functions `() { }` | 4.3.11+ | Yes |
| `setopt PIPE_FAIL` | 5.0+ | Yes |
| `${(Z)var}` parsing flag | 5.8+ | macOS Big Sur+ only |

---

## Updating This File

When a new zsh version is released:

1. Check https://zsh.sourceforge.io/News/ for the release announcement
2. Add a new section above with version number and date
3. List user-facing features with WHY explanations
4. Update the macOS version table if Apple ships the new version
5. Update the Feature Availability Matrix

When a new macOS version ships:
1. Check which zsh version it includes: `sw_vers && zsh --version`
2. Update the macOS default versions table

---

-----
March 4, 2026

#AI/Claude
