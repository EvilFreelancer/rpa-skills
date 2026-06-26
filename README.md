# RPA Skills

A catalog of [Pavel Rykov](https://t.me/evilfreelancer)'s **agent skills** — reusable instructions and
reference material for AI agents in Cursor, Kimi Code CLI, Claude Code, OpenAI Codex, and so on.

Motivation: [notes on vibe coding](https://t.me/evilfreelancer/1485) and the prompt collection
[cursor-vibe-prompts](https://github.com/EvilFreelancer/cursor-vibe-prompts) are packaged as **skills** so you do not
paste the same long instructions into chat every time.

> **This repository is now an aggregator (a marketplace catalog).** Each skill has been split into its own
> repository so it can be versioned, installed, and depended on independently. This repo keeps the catalog
> ([`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)), the authoring guide
> ([`AGENTS.md`](AGENTS.md)), and the links below.

## Skills

| Skill | Purpose |
|-------|---------|
| [/rpa-init](https://github.com/EvilFreelancer/rpa-init) | Warm up context on the repo: study code, docs and test code, set up the **dev environment**, run tests, write a **short project report**. No extra brief. |
| [/rpa-gen-rules](https://github.com/EvilFreelancer/rpa-gen-rules) | Create or refresh **agent rules** for **Cursor** (`.cursor/rules/*.mdc`) and **Claude Code** (`.claude/`). **Layered-cake** architecture + **BDD**, with a mandatory **Rules Sync** step across agent trees. |
| [/rpa-feat](https://github.com/EvilFreelancer/rpa-feat) | Add a feature strictly **by BDD**: plan, tests (**red**), implementation (**green**), full run, docs and examples, **linter** at the end. **Requires** a clear task. |
| [/rpa-bugfix](https://github.com/EvilFreelancer/rpa-bugfix) | **Reproduction test** first, then fix, full test run, **short report**. **Requires** a clear bug description. |
| [/logika](https://github.com/EvilFreelancer/logika) | Classical formal logic from G. Chelpanov's textbook (concepts, judgments, syllogisms, induction, fallacies). |
| [/token-cost](https://github.com/EvilFreelancer/token-cost) | Estimate the **floor cost** of a self-hosted LLM token (electricity + hardware amortization), not the market price. |

**Input for `/rpa-*`** — `/rpa-init` and `/rpa-gen-rules` need no extra briefing. `/rpa-feat` and `/rpa-bugfix`
need you to pass **what** to do (for example issue text), otherwise they will not work correctly.

Each skill repository has its own **README.md** with usage, install, and attribution.

## Install

### The whole catalog (Claude Code)

Add this repo as a plugin marketplace, then install any skill from it:

```text
/plugin marketplace add EvilFreelancer/rpa-skills
/plugin install rpa-init@rpa-skills
/plugin install logika@rpa-skills
# ...and so on
```

> The catalog points at the per-skill repositories listed above. Make sure those repositories exist and are
> pushed (they are split out from this one), then the marketplace entries resolve.

### A single skill

Install just one skill from the same catalog — add the catalog once, then install only what you need:

```text
/plugin marketplace add EvilFreelancer/rpa-skills
/plugin install <name>@rpa-skills
```

Or copy/symlink a skill's repository into a skill root (`~/.claude/skills/`, `~/.cursor/skills/`,
`~/.codex/skills/`, `~/.kimi/skills/`). Each skill repo keeps its `SKILL.md` at the repo root, so copy the
repository as `<name>/`. The directory name must match the `name` field in `SKILL.md`.

## Typical skill layout

```
<skill>/
├─ .claude-plugin/
│  └─ plugin.json        # plugin manifest (name, version, description) — no skills field
├─ SKILL.md              # YAML frontmatter + agent instructions (canonical, loaded from the repo root)
├─ references/ | scripts/   # optional bundled assets, referenced relative to SKILL.md
├─ README.md             # human overview
└─ LICENSE
```

A plugin with `SKILL.md` at the repo root, no `skills/` directory, and no `skills` field in `plugin.json`
is loaded by Claude Code (v2.1.142+) as a single-skill plugin; the invocation name comes from the `name`
field in `SKILL.md`. That name should match the slash command — the `rpa-*` skills use hyphenated names
such as `/rpa-init`.

## Making the agent use a skill

1. **Slash command** — type `/` in agent chat and pick the skill by its **`name`**, or type it directly,
   e.g. `/logika` or `/rpa-init`.
2. **`@` context** — type `@` and attach the skill (or its folder / `SKILL.md`) to ground the message.
3. **Automatic selection** — the agent may load a skill on its own when your request matches the
   **`description`** in `SKILL.md`, so clear trigger wording in that field helps.

## Authoring new skills

See [`AGENTS.md`](AGENTS.md) for the standard process (directory structure, mandatory `SKILL.md` frontmatter,
documentation, testing, commit guidelines).

## License

MIT — see [LICENSE](LICENSE). Each split-out skill repository carries its own copy of the same license.
