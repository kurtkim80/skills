#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "$ROOT_DIR"

RECURSIVE="${RECURSIVE:-0}"

echo "== sandbox-lifecycle-fastlane: preflight =="
date "+%Y-%m-%dT%H:%M:%S%z"
echo

echo "-- git status (root)"
git status --porcelain || true
echo

echo "-- sync root (no submodules)"
git pull --recurse-submodules=no
echo

echo "-- sync/update top-level submodules"
git submodule sync
git submodule update --init
echo

echo "-- submodule status (top-level)"
git submodule status
echo

if [[ "$RECURSIVE" == "1" ]]; then
  echo "-- dirty state (recursive submodules)"
  # This is best-effort; nested submodules may not be configured in every pinned repo.
  git submodule foreach --recursive 'echo "--- $name ($path)"; git status --porcelain' || true
  echo
fi

echo "-- openwork nested gitlinks sanity (best-effort)"
if [[ -d "_repos/openwork/.git" ]]; then
  # If openwork contains gitlink entries (mode 160000) but does not track .gitmodules,
  # recursive traversal can fail. This is informational; we avoid recursive operations by default.
  if git -C _repos/openwork ls-files --stage | rg -q '^160000 '; then
    if ! git -C _repos/openwork ls-tree -r HEAD --name-only | rg -q '^\.gitmodules$'; then
      echo "note: _repos/openwork contains gitlink entries but no tracked .gitmodules; avoid recursive submodule ops there"
    fi
  fi
fi

echo
echo "ok: preflight complete"
