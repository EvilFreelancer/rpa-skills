# RPA Skills

This repository holds [Pavel Zloi](https://t.me/evilfreelancer)'s agent skills - instructions and
reference material for AI agents in Cursor, Kimi Code CLI, Claude Code, OpenAI Codex, and so on.

Motivation: [notes on vibe coding](https://t.me/evilfreelancer/1485) and the prompt collection
[cursor-vibe-prompts](https://github.com/EvilFreelancer/cursor-vibe-prompts) are packaged here as **skills** so you do not paste the same long instructions into chat every time.

**Repository:** [github.com/EvilFreelancer/rpa-skills](https://github.com/EvilFreelancer/rpa-skills)

## Skills in this repository

| Folder | `name` in `SKILL.md` | Purpose |
|--------|----------------------|---------|
| [rpa-init/](rpa-init/) | `rpa-init` | **`/rpa-init`** - Warm up context on the repo. The agent studies application code, reads docs and test code, sets up the **dev environment** (install tooling the project expects, for example a venv), runs tests, writes a **short project report**. Runs without an extra user brief. |
| [rpa-gen-rules/](rpa-gen-rules/) | `rpa-gen-rules` | **`/rpa-gen-rules`** - Create or refresh **agent rules**. Bundled examples for **Cursor** (`.cursor/rules/*.mdc`) and **Claude Code** (`.claude/`). Rules encode a **layered approach** (layer 1 with no inward dependencies, then layer 2, and so on) and **BDD-style** development. Runs without an extra user brief. |
| [rpa-feat/](rpa-feat/) | `rpa-feat` | **`/rpa-feat`** - Add a feature strictly **by BDD**: plan, tests (**red**), implementation (**green**), full test run, update docs and examples, **linter / pre-commit** at the end when the repo uses them. **Requires** a clear task (for example issue text). |
| [rpa-bugfix/](rpa-bugfix/) | `rpa-bugfix` | **`/rpa-bugfix`** - **Reproduction test** first, then fix, full test run, **short report**. **Requires** a clear bug description. |
| [logika/](logika/) | `logika` | **`/logika`** - Classical formal logic from G. Chelpanov's textbook (concepts, judgments, syllogisms, induction, fallacies). |

**Input for `/rpa-*`** - **`/rpa-init`** and **`/rpa-gen-rules`** need no extra briefing. **`/rpa-feat`** and **`/rpa-bugfix`** need you to pass **what** to do (for example issue text), otherwise they will not work correctly.

Each skill folder has its own **README.md** with details.

## Typical skill layout

- `SKILL.md` - YAML frontmatter (`name`, `version`, `description`) and main agent instructions.
- `README.md` - Human overview (recommended).
- Optional `references/`, `scripts/`, or other assets.

The skill directory name should match the `name` field in `SKILL.md`. The `rpa-*` skills use hyphenated directory names to match slash commands such as `/rpa-init`.

## Making the agent use a skill

In **Agent** chat (not only Inline Edit), you can pull a skill into the run in several ways.

1. **Slash command** - type `/` in the chat input. Cursor shows available commands; pick the skill by its **`name`**
   from `SKILL.md`, or type it directly, e.g. **`/logika`** or **`/rpa-init`**.
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

## License

This project is licensed under the MIT License, see the [LICENSE](LICENSE) file in the repository root for details.

