---
name: rpa-gen-rules
version: 1.1.0
description: >
  Run when the user invokes /rpa-gen-rules or asks to create or refresh agent project rules (Cursor .mdc,
  Claude Code CLAUDE.md and .claude/rules). Infers from specs, docs, and code. Rules use a layered-cake model
  (implement inner layers with no dependencies first, then the next layer) and BDD-style delivery. Generated
  rules include a mandatory Rules Sync step so changes to one agent's tree are mirrored to every other agent's
  tree (Cursor <-> Claude <-> AGENTS.md) in the same commit. No separate user brief required.
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
- **Rules sync is mandatory** (see next section): every workflow rule you generate must end with a "Rules Sync" step.
- Ask questions only when blocked. Comments in generated code snippets: English.

## Rules sync across agents (mandatory)

Projects in this workflow keep parallel rule trees - typically `.cursor/rules/*.mdc` and `.claude/rules/*.md`, plus a top-level `AGENTS.md` / `CLAUDE.md`. The two **must not drift**. Whenever the agent touches one tree, it must propagate the change to the others in the same task.

Bake this into every project you generate:

### 1. Top-level: one file, many symlinks

- Keep the canonical project brief in **`AGENTS.md`** at the repository root.
- Make **`CLAUDE.md`** a symlink to `AGENTS.md` (`ln -sf AGENTS.md CLAUDE.md`) so Claude Code, OpenCode, Cursor, Codex, and any other agent that reads either filename get the same text. Reference projects: `getconf`, `getconf-ui`, `sdm-client-proxy`.
- `.claude/CLAUDE.md` may exist as a short Claude-specific addendum; keep substantive content in the root `AGENTS.md`.

### 2. Per-topic modular rules: paired files, paired edits

For each topic (`workflow`, `testing`, `architecture`, `code-style`, `implementation-order`, `api-layer`, `core-modules`), generate **both** sides:

| Cursor | Claude Code |
|--------|-------------|
| `.cursor/rules/<topic>.mdc` | `.claude/rules/<topic>.md` |
| YAML: `description`, `globs`, `alwaysApply` | YAML: `description`, optional `paths:` |
| Inline links: `@architecture.mdc`, `@docs/foo.md` | Inline links: `.claude/rules/architecture.md`, `@docs/foo.md` |

Translation rules between the two formats:

- `paths: ["src/**/*.py"]` (Claude) ↔ `globs: src/**/*.py` + `alwaysApply: true` (Cursor); a Claude rule **without** `paths:` (loads every session) ↔ Cursor `alwaysApply: true`.
- `.claude/rules/architecture.md` references ↔ `@architecture.mdc` references.
- Body content stays the same; only frontmatter and inline link syntax change.

### 3. The "Rules Sync" section every workflow rule must carry

The generated `workflow.mdc` and `workflow.md` **must** end with a `## Rules Sync` section that makes propagation a mandatory step of every TDD/BDD pass. Use wording like this (adjust paths to the project's real layout):

```markdown
## Rules Sync

**MANDATORY** - if any rule file is added or changed in this task, mirror the change to every other agent's rule tree in the same PR:

1. Identify which trees exist in the repo: `.cursor/rules/`, `.claude/rules/`, root `AGENTS.md` / `CLAUDE.md`, plus any other agent roots (`.kimi/`, `.codex/`, `.github/copilot-instructions.md`).
2. For each edited file, locate or create its counterpart in every other tree (same topic name).
3. Copy the body verbatim, then adapt the frontmatter and inline link syntax:
   - Cursor `globs:` + `alwaysApply:` <-> Claude `paths:` (or omit `paths:` for always-on).
   - Cursor `@file.mdc` <-> Claude `.claude/rules/file.md`.
4. If `AGENTS.md` changed, verify `CLAUDE.md` resolves to the same content (symlink intact, or copy refreshed).
5. Include the synced files in the same commit. Do not leave one tree ahead of the other.

Skip only when the topic is genuinely tool-specific (e.g. a Cursor `@`-context trick with no Claude equivalent). When skipping, add a one-line comment in the file that diverges.
```

This section is non-optional. If the project uses only one agent today, still generate the sync block - it activates the moment the second agent's tree is added.

## Deliverables

1. Create or update rules (Cursor and Claude Code paired, plus any other agent roots the repo uses).
2. Ensure every `workflow` rule contains the **Rules Sync** section above.
3. Ensure top-level `AGENTS.md` exists and `CLAUDE.md` is a symlink to it (or note why not).
4. Summarize files added or changed, how `alwaysApply` / `paths` / `globs` are set, and confirm both trees were updated in lockstep.
