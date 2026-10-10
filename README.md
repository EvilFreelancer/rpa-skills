# RPA Skills

[Pavel Rykov](https://t.me/evilfreelancer)'s **agent-skills marketplace** — a plugin catalog for AI agents
in Claude Code, OpenAI Codex, Cursor, Kimi Code CLI, and so on. Connect the marketplace with one command
and install any skill from it, or install every skill on its own.

Motivation: [notes on vibe coding](https://t.me/evilfreelancer/1485) and the prompt collection
[cursor-vibe-prompts](https://github.com/EvilFreelancer/cursor-vibe-prompts) are packaged as **skills** so you do not
paste the same long instructions into chat every time.

> **This repository is the marketplace itself, not the skills.** Each skill lives in its own
> repository so it can be versioned, installed, and depended on independently. This repo keeps the catalog in
> two marketplace manifests — [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) for Claude
> Code and [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) for Codex — plus an
> [`install.sh`](install.sh) for folder-based agents like Cursor, the authoring guide
> ([`AGENTS.md`](AGENTS.md)), and the links below.

## Skills

| Skill | Purpose |
|-------|---------|
| [/rpa-init](https://github.com/EvilFreelancer/rpa-init) | Warm up context on the repo: optionally **git pull** first, then study code, docs and test code, set up the **dev environment**, run tests, write a **short project report**. No extra brief. |
| [/rpa-gen-rules](https://github.com/EvilFreelancer/rpa-gen-rules) | Create or refresh root `AGENTS.md`, native **Cursor** and **Claude Code** rules, and the **Codex** project hook that attaches Cursor rules without a separate manual index. Includes layered architecture, BDD/TDD, and mandatory Rules Sync for deliberate mirrors. |
| [/rpa-feat](https://github.com/EvilFreelancer/rpa-feat) | Add a feature strictly **by BDD**: plan, tests (**red**), implementation (**green**), full run, docs and examples, **linter** at the end. **Requires** a clear task. |
| [/rpa-bugfix](https://github.com/EvilFreelancer/rpa-bugfix) | **Reproduction test** first, then fix, full test run, **short report**. **Requires** a clear bug description. |
| [/logika](https://github.com/EvilFreelancer/logika) | Classical formal logic from G. Chelpanov's textbook (concepts, judgments, syllogisms, induction, fallacies). |
| [/token-cost](https://github.com/EvilFreelancer/token-cost) | Estimate the **floor cost** of a self-hosted LLM token (electricity + hardware amortization), not the market price. |
| [/mikrotik-config-gen](https://github.com/EvilFreelancer/mikrotik-config-gen) | Generate secure **MikroTik RouterOS v7** configs from plain language, or **review and harden** an existing `/export`. Hardening baseline, four presets, per-model device reference, offline validator. |
| [/screenshotting-gui](https://github.com/EvilFreelancer/screenshotting-gui) | Capture clean, repeatable screenshots of a **GUI desktop app** (IDEs, browsers, native apps) on an isolated **Xvfb** display, driven with **python-Xlib** (XTEST), annotated with **ImageMagick** (highlight box, crop, arrow). Never touches the operator's live desktop. |
| [/gpu-server-setup](https://github.com/EvilFreelancer/gpu-server-setup) | Prepare a **Linux server with NVIDIA GPUs** for LLM workloads: driver + CUDA from the **official repo**, Docker + **NVIDIA Container Toolkit** as the **mandatory base**, **staged verification gates**, optional compose presets for **vLLM**, Infinity, OpenWebUI, Ollama and llama.cpp, plus **GPU power-limit** setup persisted via systemd. |
| [/rdp-agent](https://github.com/EvilFreelancer/rdp-agent) | Drive a **remote Windows machine over RDP**: the RDP client runs on an isolated **Xvfb** display, the operator watches the same screen in a **VNC** window and can take over by hand, the **session survives between agent turns**, and a lock screen is recovered by an **NLA reconnect** instead of typing the password. |
| [/crossreview](https://github.com/EvilFreelancer/crossreview) | **Cross-review** with several console code agents at once: Claude Code, Codex, Coddy, Cursor Agent, Devin, OpenCode and others review the same brief **in parallel and blind to each other**, then the orchestrating agent **verifies every finding** against the code and decides what to fix. Linux, macOS and Windows; reviewers chosen once per agent, for one project or for all of them. Works best with [Coddy Agent](https://github.com/coddy-project/coddy-agent): there its built-in [`crossreview` coordinator subagent](https://coddy.dev/docs/features/subagents#built-ins) runs the review, and `coddy` is the reviewer CLI that reaches Codex, Devin and open models with one command. |
| [/nd-search](https://github.com/EvilFreelancer/nd-search) | **Web search**, clean **page text by URL** and **site crawling** (plus Telegram channel search) through the [NeuralDeep](https://neuraldeep.ru) Search API with an `sk-` key: search, then read the picked links, crawl only a whole section. A standard-library Python client takes the key from `--api-key` or `NEURALDEEP_API_KEY` and exits with codes per error class. |

**Input for `/rpa-*`** — `/rpa-init` and `/rpa-gen-rules` need no extra briefing. `/rpa-feat` and `/rpa-bugfix`
need you to pass **what** to do (for example issue text), otherwise they will not work correctly.

Each skill repository has its own **README.md** with usage, install, and attribution.

## Install

This catalog ships **two marketplace manifests** so it can be connected as a marketplace from more than one
agent, plus a plain installer script for agents that have no remote marketplace at all. Coddy needs
none of them, it has the catalog built in:

| File | Consumed by | How you connect it |
|------|-------------|--------------------|
| built into Coddy | **[Coddy](https://coddy.dev)** | nothing to connect: `coddy skills sync` |
| [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) | **Claude Code** (also read by Codex as a legacy fallback) | `/plugin marketplace add EvilFreelancer/rpa-skills` |
| [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) | **Codex** | `codex plugin marketplace add EvilFreelancer/rpa-skills` |
| [`install.sh`](install.sh) | **Cursor** and any folder-based agent | clones skills into `~/.agents/skills/` |

> All three point at the per-skill repositories listed above. Make sure those repositories exist and are
> pushed (they are split out from this one), then the entries resolve.

### Claude Code

Add this repo as a plugin marketplace, then install any skill from it:

```text
/plugin marketplace add EvilFreelancer/rpa-skills
/plugin install rpa-init@rpa-skills
/plugin install logika@rpa-skills
# ...and so on
```

### Codex

Codex has its own repo marketplace. Add this catalog, then browse/install from `/plugins`:

```bash
codex plugin marketplace add EvilFreelancer/rpa-skills
codex plugin marketplace list        # verify it resolved
# then in the CLI: run `codex`, open `/plugins`, pick the "RPA Skills" tab, install what you need
```

Codex reads [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json). It can also read the
Claude manifest above as a legacy-compatible source, so either entry point works.

### Coddy

[Coddy](https://coddy.dev) has this catalog built in as a system source: it is in effect on every machine
without being declared in any file, so there is nothing to connect. One command installs every skill of
the catalog into `~/.coddy/skills/` and keeps them up to date (**Sync all** in Settings → Skills does the
same):

```bash
coddy skills sync                 # install or update everything the catalog publishes
coddy plugin marketplace list     # shows EvilFreelancer/rpa-skills as built into Coddy
```

`/crossreview` and the `rpa-*` skills (`/rpa-init`, `/rpa-feat`, `/rpa-bugfix`, `/rpa-gen-rules`) ship
inside Coddy itself and are there on the first run, offline. To drop a skill, disable or delete it
(`coddy skills disable <name>`); the catalog itself cannot be removed from Coddy.

### Cursor (and other folder-based agents)

Cursor has **no remote plugin marketplace** — it discovers skills only from directories (`.agents/skills/`,
`.cursor/skills/`, and their `~/` globals). So instead of "connecting" the catalog, you install the skill
folders into a skills root the agent reads:

```bash
# install/update the whole catalog into ~/.agents/skills (read by Cursor and Codex)
curl -fsSL https://raw.githubusercontent.com/EvilFreelancer/rpa-skills/main/install.sh | bash

# or clone the repo and run it, optionally targeting a specific root / subset
git clone https://github.com/EvilFreelancer/rpa-skills && cd rpa-skills
./install.sh                       # -> ~/.agents/skills
./install.sh -d ~/.cursor/skills   # -> a Cursor-specific root
./install.sh logika rpa-init       # only the named skills
```

Then reload the Cursor window (`Cmd/Ctrl+Shift+P` → *Developer: Reload Window*).

### A single skill, by hand

Every skill repo keeps its `SKILL.md` at the repo root, so you can clone one straight into a skills root.
The directory name must match the `name` field in `SKILL.md`:

```bash
git clone https://github.com/EvilFreelancer/logika ~/.agents/skills/logika
```

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

## Maintaining the catalog

See [`AGENTS.md`](AGENTS.md) for the collection-wide process: how the two marketplace manifests, the Skills
table, and `install.sh` mirror each skill's metadata, and the **sync rule** to follow when a skill bumps its
version, description, or tags. For authoring an individual skill, see the `AGENTS.md` in that skill's own
repository.

## License

MIT — see [LICENSE](LICENSE). Each split-out skill repository carries its own copy of the same license.
