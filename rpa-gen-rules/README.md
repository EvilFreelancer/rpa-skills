# Agent project rules

## Purpose

Generate or refresh **project rules** so agents stay inside architecture, style, and **TDD discipline**. Supports:

- **Cursor** — `.cursor/rules/*.mdc` (MDC front matter, `globs`, `alwaysApply`, `@` references).
- **Claude Code** — `CLAUDE.md` and `.claude/rules/*.md` with optional YAML **`paths:`** for path-scoped rules ([memory docs](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)).
- Aligned copies for other tools (for example Copilot instructions) when requested.

The agent infers content from README, specs, code, and tests; no long manual brief is required unless the repo has no docs.

## When to use

- User runs **`/rpa-gen-rules`** or asks to create or update Cursor rules, Claude rules, or equivalent.

## Bundled references (progressive disclosure)

| Path | Contents |
|------|----------|
| `references/bdd-and-agents.md` | BDD-style rules meaning, Cursor vs Claude vs others, single source of truth |
| `references/cursor-examples/.cursor/rules/` | Example `.mdc` templates (workflow, testing, architecture, …) |
| `references/claude-examples/.claude/` | Example `CLAUDE.md` + modular `rules/*.md` with and without `paths` |

## Contents

| File / dir | Role |
|------------|------|
| `SKILL.md` | Metadata, load order, deliverables |
| `references/` | Templates and multi-agent notes (not loaded until read) |
