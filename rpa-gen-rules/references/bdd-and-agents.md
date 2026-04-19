# BDD-style agent rules and multiple IDEs

This file explains how to encode **behavior** (examples, acceptance checks, regression discipline) in project rules, and how **Cursor**, **Claude Code**, and other tools differ while serving the same goal.

## What "BDD rules" means here

Classic BDD often uses Gherkin (`Given` / `When` / `Then`) and tools like `pytest-bdd`. In this RPA workflow, **BDD-oriented rules** mean:

1. **Executable behavior** lives in tests. Rules tell the agent to treat tests as the long-term memory of the project (red-green-refactor, full suite before done).
2. **`workflow.mdc` (in this skill)** is the main rail: trigger phrases for features and bugs, mandatory order (failing test → fix or implement → green → all tests → optional `pre-commit run -a` → short report).
3. **`testing.mdc`** defines how tests read: naming, Arrange-Act-Assert, fixtures, integration vs unit, commands (`pytest`, coverage).

If the repo already uses Gherkin or `pytest-bdd`, extend `testing.mdc` and `workflow.mdc` with paths to `features/`, step definitions, and how to run those tests. Otherwise, plain pytest examples are enough.

**Important:** In `implementation-order.mdc`, steps sometimes show a class before tests for illustration of **layers**. For **new behavior**, always follow **`workflow.mdc`**: write or extend the failing test first, then minimal code (TDD). Layering still applies when choosing *where* code lives.

## Cursor

- **Location:** `.cursor/rules/` with `.mdc` files.
- **Format:** YAML front matter ([MDC](https://github.com/nuxt-content/mdc)) with `description`, optional `globs`, optional `alwaysApply`.
- **Context:** Use `@path/to/file` inside a rule to pull files into context when the rule applies.
- **Docs:** [Cursor Rules](https://cursor.com/docs/context/rules).

**Mapping**

| Concern | Typical file |
|---------|----------------|
| TDD and bugfix workflow | `workflow.mdc` |
| pytest structure and examples | `testing.mdc` |
| Layers and modules | `architecture.mdc` |
| Style and tooling | `code-style.mdc` |
| Dependency order | `implementation-order.mdc` (often `alwaysApply: false`) |

## Claude Code

Official reference: [How Claude remembers your project](https://code.claude.com/docs/en/memory), including [modular rules with `.claude/rules/`](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/).

Claude Code uses a **similar** idea (persistent instructions + optional modular files) but **different paths and discovery**.

- **`CLAUDE.md`:** Project instructions loaded for sessions. Prefer under 200 lines; split using `@imports` or `.claude/rules/`. See the same memory page for load order and `CLAUDE.local.md`.
- **`.claude/rules/`:** Markdown files, one topic per file (`testing.md`, `workflow.md`, …). Discovered recursively; you can nest `frontend/`, `backend/`. Rules **without** YAML frontmatter load at launch (same priority as `.claude/CLAUDE.md`). Rules **with** `paths:` in frontmatter load when Claude works on matching files (see [path-specific rules](https://code.claude.com/docs/en/memory#path-specific-rules)). Use glob patterns like `src/**/*.py`, `tests/**/*.py`, `**/*.{ts,tsx}`.
- **Imports in `CLAUDE.md`:** `@README.md`, `@docs/guide.md`, up to five hops deep. First-time imports may require user approval in the IDE.
- **`AGENTS.md`:** Claude Code reads `CLAUDE.md`, not `AGENTS.md` by default. You can `import` with `@AGENTS.md` at the top of `CLAUDE.md` to share one text with other agents (documented on the memory page).
- **Skills (Agent Skills):** Portable folders with `SKILL.md` and optional `scripts/`. For heavy procedures that should not sit in every session context, prefer skills over huge rules. [agentskills.io](https://agentskills.io/), [anthropics/skills](https://github.com/anthropics/skills).

### Bundled example in this skill

Copy or adapt `references/claude-examples/.claude/` into a real project root. It demonstrates:

- Short `.claude/CLAUDE.md` with imports and pointers to modular rules.
- Global `rules/workflow.md` (no `paths`, TDD for features and bugs).
- Path-scoped `rules/testing.md`, `code-style.md`, `architecture.md`, `implementation-order.md`, `api-layer.md` with YAML `paths:` per the official docs.

**Practical alignment**

- Port the **same substance** as Cursor rules: one file for **workflow** (TDD, bug reproduction, full suite), one for **testing** conventions, one for **architecture**.
- Use Markdown in `.claude/rules/` without assuming MDC-only features; link `@` to repo files if your Claude Code build supports it.
- **Plugins vs repo rules:** Skills are portable packages; `CLAUDE.md` and `.claude/rules/` are project-local. Use both when skills encode reusable procedure and repo rules encode **this** codebase.

## Other agents and editors

| Tool | Where rules usually live | Notes |
|------|---------------------------|--------|
| **OpenCode / skills repos** | `SKILL.md`, `AGENTS.md` | Same progressive disclosure idea as Agent Skills standard. |
| **GitHub Copilot** | `.github/copilot-instructions.md` (or policy UI) | Keep instructions short; mirror key bullets from `workflow` and `testing`. |
| **Generic** | `CONTRIBUTING.md`, `docs/dev-guide.md` | Humans and any agent can read these; duplicate critical agent constraints here if your team does not use Cursor or Claude.

## Single source of truth

1. Prefer **one canonical place** for TDD workflow text (either `workflow.mdc` for Cursor or `workflow.md` under `.claude/rules/` for Claude Code).
2. When maintaining **both** Cursor and Claude Code, keep sections aligned by topic; avoid drifting copies.
3. Point all rules at the **same** test commands (`pytest`, `uv run`, etc.) and config files (`ruff.toml`, `pytest.ini`).

## Bundled examples in this skill

- **`references/cursor-examples/.cursor/rules/`** — full **reference copies** of [cursor-vibe-prompts](https://github.com/EvilFreelancer/cursor-vibe-prompts/tree/main/cursor-rules) (`.mdc` templates), laid out like a real Cursor project (same path as production `.cursor/rules/`).
- **`references/claude-examples/.claude/`** — parallel **Claude Code** layout (`CLAUDE.md` + `rules/*.md` with and without `paths`), aligned with [code.claude.com memory docs](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/).

Read these when generating or updating project rules so structure and BDD/TDD wording stay consistent across tools.
