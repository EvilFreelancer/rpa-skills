---
name: rpa-gen-rules
version: 1.0.0
description: >
  Run when the user invokes /rpa-gen-rules or asks to create or refresh agent project rules (Cursor .mdc,
  Claude Code CLAUDE.md and .claude/rules, or aligned copies). Infers structure from specs, docs, and code.
  Bundled reference examples show BDD-style TDD workflow and testing rules. No separate task description required.
---

# RPA generate project rules (BDD-oriented, multi-agent)

## Goal

Produce or update **versioned** instructions so the agent stays inside architecture, style, and **TDD/BDD discipline** (tests first, regression tests for bugs, full suite before reporting). Cursor stores these as `.cursor/rules/*.mdc`. Claude Code uses `CLAUDE.md` and often `.claude/rules/*.md`. Other tools may use Copilot instructions or docs. Same ideas, different filenames.

## Read these references from this skill (progressive disclosure)

1. **`references/bdd-and-agents.md`**  
   What BDD-style rules mean in this workflow, how **Cursor** vs **Claude Code** vs other agents map, and how to avoid duplicated drifting copies.

2. **`references/cursor-examples/.cursor/rules/workflow.mdc`**  
   Primary template for **feature and bugfix workflows** (red → green → all tests → linter → report). Copy patterns and adapt globs, paths, and `@` links to the target repo.

3. **`references/cursor-examples/.cursor/rules/testing.mdc`**  
   Template for **pytest** naming, structure, fixtures, and commands.

4. **Other files in `references/cursor-examples/.cursor/rules/`**  
   `architecture.mdc`, `code-style.mdc`, `implementation-order.mdc`, `api-layer.mdc`, `core-modules.mdc` are **worked examples** (some placeholders like `search_project/`). Replace globs, package names, and bullets with the real project. These files originated from the [cursor-vibe-prompts cursor-rules](https://github.com/EvilFreelancer/cursor-vibe-prompts/tree/main/cursor-rules) collection.

5. **`references/claude-examples/.claude/`**  
   Claude Code **modular rules** example per [How Claude remembers your project](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/): `CLAUDE.md` plus `rules/*.md` using plain Markdown and optional YAML `paths:` for path-scoped rules. Copy into a project root and adjust globs (`src/`, `main.py`, etc.).

Load additional reference files only when you need detail for the current generation task.

## Discover first

Without asking the user for hand-written specs unless nothing exists:

1. Read `README`, `docs/`, `ARCHITECTURE*`, `TECH*`, OpenAPI, `pyproject.toml` / `package.json`, CI configs.
2. Skim representative code for stack (FastAPI, Django, CLI, front-end).
3. Read `tests/` and linters (`ruff.toml`, `pre-commit-config.yaml`) to encode real commands and conventions.
4. For monorepos, plan **per-package** rules under `backend/.cursor/rules/`, `frontend/.cursor/rules/`, or equivalent `.claude/rules/` subtrees when layouts clearly split.

## Cursor (`.cursor/rules/*.mdc`)

Each rule file is Markdown with YAML front matter ([MDC](https://github.com/nuxt-content/mdc)):

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

- `alwaysApply: true` for global constraints (style, testing discipline, workflow).
- Set `alwaysApply: false` for optional topics (for example implementation order) so the agent loads them when editing matching `globs` or when the user `@` mentions the file.

**Docs:** [Cursor Rules](https://cursor.com/docs/context/rules).

## Claude Code (`CLAUDE.md`, `.claude/rules/`)

- Keep **`CLAUDE.md`** short (stack, how to run tests, link or summarize non-negotiable workflow).
- Split detail into **`.claude/rules/*.md`** mirroring the same topics as Cursor (`workflow`, `testing`, `architecture`, `code-style`).
- Confirm path scoping and `@` imports against **your** Claude Code version. Overview: [CLAUDE.md in Claude Code docs](https://docs.anthropic.com/en/docs/claude-code/claude-md).
- **Agent Skills** (portable) complement repo rules; see [agentskills.io](https://agentskills.io/) and [anthropics/skills](https://github.com/anthropics/skills).

## Files to create or align in the target project

Typical set (rename globs and paths to match the project):

| File | Contents |
|------|----------|
| `workflow` | TDD for features and bugs, documentation sync, final verification, optional `pre-commit run -a` |
| `testing` | pytest layout, naming, fixtures, coverage, commands |
| `architecture` | Layers, modules, boundaries, `@README` or architecture doc |
| `code-style` | Formatter, line length, types, comments language, file layout |
| `implementation-order` | One class or unit at a time, bottom-up dependency order (often optional apply) |
| `api-layer` | Only if there is an HTTP or RPC surface |
| `core-modules` | Domain modules and invariants |

Use `@` (Cursor) or equivalent file links (Claude Code) to canonical docs and config so rules stay short.

## Content rules from RPA practice

- Extract terminology, constraints, NFRs, and open questions from specs; list open questions in `workflow` or `docs/` when appropriate.
- **Class-at-a-time**: layer 1 has no internal dependencies, layer 2 depends only on layer 1, and so on. Each new class gets minimal tests.
- **Task loop**: state understanding and plan; tests red; minimal implementation; tests green; full suite; short checklist for what is next.
- Minimize chat to steps, files, tests. Ask questions only when blocked.
- Code comments in rules stay in English. No emoji in rules unless the user project already uses them.

## Deliverables

1. Create or update rules in the target repo (Cursor `.mdc` and/or Claude Code markdown as requested).
2. If `docs/` should hold `ARCHITECTURE.md` or rule indexes and they are missing, add only what is needed to reference from rules (avoid large unsolicited docs).
3. End with a short summary of which files were added or changed, which tool they target, and how `alwaysApply` or scoping is set.
