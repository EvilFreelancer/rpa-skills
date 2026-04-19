# RPA Skills

This repository holds **author agent skills** - instructions and reference material for AI agents in Cursor, Kimi Code
CLI, Claude Code, OpenAI Codex, and similar tools. Skills are installed as directories that contain a `SKILL.md` file
and optionally folders such as `references/`, `source/`, and others.

## Skills in this repository

| Folder    | `name` in `SKILL.md` | Purpose                                                                                                                   |
|-----------|----------------------|---------------------------------------------------------------------------------------------------------------------------|
| `logika/` | `logika`             | Classical formal logic (concepts, judgments, syllogisms, induction, fallacies). See [logika/README.md](logika/README.md). |

More rows will be added as new skills are published.

## Typical skill layout

- `SKILL.md` - YAML frontmatter and main agent instructions.
- `references/` - structured notes the agent can load on demand.

The skill directory name should match the `name` field in `SKILL.md` (here both are `logika`).

## Installation by environment

Put the **skill directory** (named `logika`, containing at least `SKILL.md` and any bundled `references/` or other
files) into one of the standard skill roots for your tool. Paths below are typical; check your CLI version if something
differs.

### Cursor

- **User-wide** - `~/.cursor/skills/logika/`.
- **Project-only** - `<repo-root>/.cursor/skills/logika/`.

You can copy this repository's `logika/` folder as-is, or symlink it. Skills are discovered from these locations
per [Agent Skills](https://cursor.com/docs/context/skills).

### Kimi Code CLI

Layered skill roots are supported. Common choices:

- User - `~/.kimi/skills/logika/` or `~/.config/agents/skills/logika/`.
- Project - `.kimi/skills/logika/` at the repository root.

You can also pass extra directories with `--skills-dir` (repeatable). See
the [Kimi Code CLI skills docs](https://moonshotai.github.io/kimi-cli/en/customization/skills.html).

### Claude Code

- User - `~/.claude/skills/logika/`.
- Project - `.claude/skills/logika/`.

Copy or symlink the `logika/` directory under one of these paths.

### OpenAI Codex (CLI / agent)

- User - `~/.codex/skills/logika/`.
- Project - `.codex/skills/logika/`.

The directory name must match the `name` field in `SKILL.md` (`logika`).
