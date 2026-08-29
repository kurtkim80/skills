#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT_DIR"

BASE_REF="${BASE_REF:-origin/main}"
BRANCH="${BRANCH:-sandbox-lifecycle-$(date +%Y%m%d-%H%M%S)}"
WT_DIR="${WT_DIR:-_worktrees/$BRANCH}"

echo "== sandbox-lifecycle-fastlane: worktree =="
echo "branch:   $BRANCH"
echo "base ref: $BASE_REF"
echo "dir:      $WT_DIR"
echo

mkdir -p "$(dirname "$WT_DIR")"
git fetch origin --prune
git worktree add -b "$BRANCH" "$WT_DIR" "$BASE_REF"

echo
echo "ok: worktree created"
echo "next: cd '$WT_DIR'"
