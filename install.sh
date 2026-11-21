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
# skills directory by Cursor and Codex. Flat skill repositories land directly
# at <root>/<name>; repositories with a nested skill path are linked from that
# path into the same location.
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
  screenshotting-gui
  gpu-server-setup
  server-discovery
  server-onboarding
  server-healthcheck
  rdp-agent
  crossreview
  og-preview
  diagram-authoring
  nd-search
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

install_nested_skill() {
  local name="$1"
  local url="$2"
  local skill_path="$3"
  local dest="$SKILLS_DIR/$name"
  local repo_dir="$SKILLS_DIR/.rpa-skill-sources/$name"
  local link_target=".rpa-skill-sources/$name/$skill_path"
  local migrated_legacy=0

  mkdir -p "$SKILLS_DIR/.rpa-skill-sources"

  # Migrate the previous full-repository clone without discarding local files.
  if [ -d "$dest/.git" ] && [ ! -e "$repo_dir" ]; then
    echo "↻ updating legacy $name checkout"
    if ! git -C "$dest" pull --ff-only --quiet; then
      echo "  ! could not update $name; keeping the existing installation" >&2
      return
    fi
    if [ ! -f "$dest/$skill_path/SKILL.md" ]; then
      echo "  ! $name repository does not have $skill_path/SKILL.md yet; keeping the existing installation" >&2
      return
    fi
    mv "$dest" "$repo_dir"
    migrated_legacy=1
  fi

  if [ -d "$repo_dir/.git" ]; then
    if [ "$migrated_legacy" -eq 0 ]; then
      echo "↻ updating $name source"
      git -C "$repo_dir" pull --ff-only --quiet || echo "  ! could not fast-forward $name (local changes?)" >&2
    fi
  elif [ ! -e "$repo_dir" ]; then
    echo "↓ cloning  $name source"
    git clone --depth 1 --quiet "$url" "$repo_dir" || {
      echo "  ! failed to clone $name ($url)" >&2
      return
    }
  else
    echo "  ! source path exists but is not a Git checkout: $repo_dir" >&2
    return
  fi

  if [ ! -f "$repo_dir/$skill_path/SKILL.md" ]; then
    echo "  ! $name skill path not found: $skill_path/SKILL.md" >&2
    return
  fi

  if [ -L "$dest" ]; then
    if [ "$(readlink "$dest")" != "$link_target" ]; then
      echo "  ! $dest is a symlink to an unexpected location; leaving it unchanged" >&2
    fi
  elif [ -e "$dest" ]; then
    echo "  ! $dest exists and is not a managed symlink; leaving it unchanged" >&2
  else
    if ! ln -s "$link_target" "$dest"; then
      echo "  ! could not link $name; copy $repo_dir/$skill_path to $dest manually" >&2
    fi
  fi
}

for name in "${SKILLS[@]}"; do
  dest="$SKILLS_DIR/$name"
  url="https://github.com/$OWNER/$name.git"
  if [ "$name" = "logika" ]; then
    install_nested_skill "$name" "$url" "skills/logika"
    continue
  fi

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
