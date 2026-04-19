# RPA Skills

This repository holds [Pavel Zloi](https://t.me/evilfreelancer)'s agent skills - instructions and
reference material for AI agents in Cursor, Kimi Code CLI, Claude Code, OpenAI Codex, and so on.

## Skills in this repository

| Folder             | `name` in `SKILL.md` | Purpose                                                                         |
|--------------------|----------------------|---------------------------------------------------------------------------------|
| [logika/](logika/) | `logika`             | Classical formal logic (concepts, judgments, syllogisms, induction, fallacies). |

More rows will be added as new skills are published.

## Typical skill layout

- `SKILL.md` - YAML frontmatter and main agent instructions.

The skill directory name should match the `name` field in `SKILL.md`.

## Making the agent use a skill

In **Agent** chat (not only Inline Edit), you can pull a skill into the run in several ways.

1. **Slash command** - type `/` in the chat input. Cursor shows available commands; pick the skill by its **`name`**
   from `SKILL.md`, or type it directly, e.g. **`/logika`** for the logic skill in this repository.
2. **`@` context** - type `@` and attach the skill (or the skill folder / `SKILL.md`) so that message is grounded in
   that skill's instructions.
3. **Automatic selection** - the agent may load a skill on its own when your request matches the **`description`** in
   `SKILL.md`, so clear trigger wording in that field helps.

## Installation by environment

Put the skill directory into one of the standard skill roots for your tool. Paths below are typical; check your CLI
version if something differs.

### Cursor

- **User-wide** - `~/.cursor/skills/<name>/`.
- **Project-only** - `<repo-root>/.cursor/skills/<name>/`.

You can copy this repository's `<name>/` folder as-is, or symlink it. Skills are discovered from these locations
per [Agent Skills](https://cursor.com/docs/context/skills).

### Kimi Code CLI

Layered skill roots are supported. Common choices:

- User - `~/.kimi/skills/<name>/` or `~/.config/agents/skills/<name>/`.
- Project - `.kimi/skills/<name>/` at the repository root.

You can also pass extra directories with `--skills-dir` (repeatable). See
the [Kimi Code CLI skills docs](https://moonshotai.github.io/kimi-cli/en/customization/skills.html).

### Claude Code

- User - `~/.claude/skills/<name>/`.
- Project - `.claude/skills/<name>/`.

Copy or symlink the `<name>/` directory under one of these paths.

### OpenAI Codex (CLI / agent)

- User - `~/.codex/skills/<name>/`.
- Project - `.codex/skills/<name>/`.

The directory name must match the `name` field in `SKILL.md`.
