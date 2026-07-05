#!/usr/bin/env bash
#
# install.sh — install the RPA Skills catalog into a directory that
# directory-based agents read as Agent Skills.
#
# Use this for agents that have NO remote plugin marketplace (Cursor, and any
# other tool that discovers skills from a folder). Claude Code and Codex users
# should prefer the native marketplace instead — see README.md:
#   Claude Code:  /plugin marketplace add EvilFreelancer/rpa-skills
#   Codex:        codex plugin marketplace add EvilFreelancer/rpa-skills
#
# What it does: clones (or updates) each split-out skill repository into a
# skills root. The default root is ~/.agents/skills, which is read as a global
# skills directory by Cursor and Codex. Each skill repo keeps SKILL.md at its
# root, so it lands as <root>/<name>/SKILL.md and the agent picks it up by name.
#
# Usage:
#   ./install.sh                      # install/update all skills into ~/.agents/skills
#   ./install.sh -d ~/.cursor/skills  # install into a specific skills root
#   ./install.sh -d .agents/skills    # vendor into the current project (repo-scoped)
#   ./install.sh logika rpa-init      # install only the named skills
#   SKILLS_DIR=~/.cursor/skills ./install.sh   # same as -d, via env var
#
set -euo pipefail

OWNER="EvilFreelancer"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.agents/skills}"

ALL_SKILLS=(
  rpa-init
  rpa-gen-rules
  rpa-feat
  rpa-bugfix
  logika
  token-cost
  mikrotik-config-gen
)

usage() {
  sed -n '2,25p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

while [ $# -gt 0 ]; do
  case "$1" in
    -d|--dir) SKILLS_DIR="$2"; shift 2 ;;
    -h|--help) usage 0 ;;
    -*) echo "unknown option: $1" >&2; usage 1 ;;
    *) break ;;
  esac
done

# Positional args (if any) select a subset of skills.
if [ $# -gt 0 ]; then
  SKILLS=("$@")
else
  SKILLS=("${ALL_SKILLS[@]}")
fi

command -v git >/dev/null 2>&1 || { echo "error: git is required" >&2; exit 1; }

mkdir -p "$SKILLS_DIR"
echo "Installing RPA Skills into: $SKILLS_DIR"
echo

for name in "${SKILLS[@]}"; do
  dest="$SKILLS_DIR/$name"
  url="https://github.com/$OWNER/$name.git"
  if [ -d "$dest/.git" ]; then
    echo "↻ updating $name"
    git -C "$dest" pull --ff-only --quiet || echo "  ! could not fast-forward $name (local changes?)" >&2
  else
    echo "↓ cloning  $name"
    git clone --depth 1 --quiet "$url" "$dest" || echo "  ! failed to clone $name ($url)" >&2
  fi
done

echo
echo "Done. Reload your agent to pick up the skills:"
echo "  Cursor:  Cmd/Ctrl+Shift+P → \"Developer: Reload Window\""
echo "  Codex:   restart Codex (or run: codex plugin marketplace add $OWNER/rpa-skills)"
