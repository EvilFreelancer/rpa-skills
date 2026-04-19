---
name: rpa-gen-rules
version: 1.0.0
description: >
  Run when the user invokes /rpa-gen-rules or asks to create or refresh agent project rules (Cursor .mdc,
  Claude Code CLAUDE.md and .claude/rules). Infers from specs, docs, and code. Rules use a layered-cake model
  (implement inner layers with no dependencies first, then the next layer) and BDD-style delivery. No separate user brief required.
---

# RPA generate project rules (layered + BDD, multi-agent)

## Goal

Produce or update **versioned** instructions so the agent stays inside architecture, style, and **BDD-style** discipline (behavior specified in tests, tests before new behavior, full suite before calling work done).

- **Layered cake** - rules must tell the agent to build **by layers**: first units that depend on nothing inside the project, then layers that depend only on lower layers, and so on. Mirror this in `architecture` and `implementation-order` style files.
- **Cursor** - `.cursor/rules/*.mdc` ([MDC](https://github.com/nuxt-content/mdc), `globs`, `alwaysApply`, `@` links).
- **Claude Code** - `CLAUDE.md` and `.claude/rules/*.md` with optional YAML `paths:` ([memory](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/)).

## Read these references from this skill (progressive disclosure)

1. **`references/bdd-and-agents.md`**  
   BDD-oriented rules, Cursor vs Claude vs others, avoiding duplicate drifting copies.

2. **`references/cursor-examples/.cursor/rules/workflow.mdc`**  
   Feature and bugfix flow (red, green, all tests, linter, report). Adapt globs and `@` links.

3. **`references/cursor-examples/.cursor/rules/testing.mdc`**  
   pytest naming, fixtures, commands.

4. **Other files in `references/cursor-examples/.cursor/rules/`**  
   `architecture.mdc`, `code-style.mdc`, `implementation-order.mdc`, `api-layer.mdc`, `core-modules.mdc` - templates from [cursor-vibe-prompts](https://github.com/EvilFreelancer/cursor-vibe-prompts/tree/main/cursor-rules). Replace placeholders with the real project.

5. **`references/claude-examples/.claude/`**  
   Example `CLAUDE.md` and modular `rules/*.md` with optional `paths:`.

## Discover first

Without asking for hand-written specs unless the repo has none:

1. Read `README`, `docs/`, `ARCHITECTURE*`, OpenAPI, `pyproject.toml` / `package.json`, CI.
2. Skim representative code.
3. Read `tests/` and linters (`ruff.toml`, `pre-commit-config.yaml`).
4. In monorepos, plan per-package `.cursor/rules/` or `.claude/rules/` when layouts split.

## Cursor (`.cursor/rules/*.mdc`)

YAML front matter example:

```markdown
---
description: Short label for this rule set
globs: path/glob/**/*.py
alwaysApply: true
---

# Title

Bullets and @references

@path/to/file.py
@docs/spec.md
```

Use `alwaysApply: true` for workflow and style that must always apply. Use `alwaysApply: false` or narrow `globs` for optional topics.

**Docs:** [Cursor Rules](https://cursor.com/docs/context/rules).

## Claude Code (`CLAUDE.md`, `.claude/rules/`)

Keep `CLAUDE.md` short. Put layered architecture and BDD workflow in topic files under `.claude/rules/`. Confirm `paths:` behavior against your Claude Code version. [CLAUDE.md overview](https://docs.anthropic.com/en/docs/claude-code/claude-md).

## Files to create or align in the target project

| Topic | Contents |
|-------|----------|
| `workflow` | BDD/TDD steps for features and bugs, final checks, `pre-commit` when used |
| `testing` | pytest layout, naming, fixtures |
| `architecture` | Layers, modules, allowed dependencies (supports layered cake) |
| `code-style` | Formatter, types, comments language |
| `implementation-order` | Explicit layer-by-layer order |
| `api-layer` | If HTTP or RPC exists |
| `core-modules` | Domain modules |

## Content rules

- **Layered cake** in rules: forbid jumping ahead to high-level code before lower layers exist and are tested.
- **BDD** in rules: new behavior starts with tests that describe observable outcomes.
- Ask questions only when blocked. Comments in generated code snippets: English.

## Deliverables

1. Create or update rules (Cursor and/or Claude Code as requested).
2. Summarize files added or changed and how `alwaysApply` / `paths` / `globs` are set.
