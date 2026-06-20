# Agent project rules

## Purpose

Create or update **agent rules** for **Cursor** (`.cursor/rules/*.mdc`) and **Claude Code** (`.claude/` with modular `rules/`). Bundled examples live under `references/`.

Rules follow a **layered-cake** idea: implement **inner layers first** (no internal project dependencies), then the next layer, and so on. They also describe **BDD-style** work (behavior driven by tests). No long user brief is required; the agent infers from the repo.

Generated rules **must** include a mandatory **Rules Sync** step: any change to a rule for one agent (for example a Cursor `.mdc`) has to be mirrored to every other agent's tree (Claude `.md`, root `AGENTS.md` / `CLAUDE.md`, etc.) in the **same** commit. The skill also recommends keeping `CLAUDE.md` as a symlink to `AGENTS.md` at repo root (see `getconf`, `getconf-ui`, `sdm-client-proxy` for reference). See `SKILL.md` and `references/bdd-and-agents.md` for the exact wording and translation table.

## When to use

- User runs **`/rpa-gen-rules`** or asks to generate or refresh rules.

## Bundled references

| Path | Contents |
|------|----------|
| `references/bdd-and-agents.md` | BDD rules meaning, Cursor vs Claude |
| `references/cursor-examples/.cursor/rules/` | `.mdc` templates |
| `references/claude-examples/.claude/` | `CLAUDE.md` + `rules/*.md` examples |

## Contents

| File / dir | Role |
|------------|------|
| `SKILL.md` | Metadata and deliverables |
| `references/` | Templates and notes |

