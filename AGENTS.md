# How to Create Agent Skills

This document describes the **standard process** for adding a new agent skill to the repository. Follow the steps
carefully so that the skill can be discovered, loaded, and used by the OpenCode platform.

## Agent Skills references (read before authoring)

Use these sources so you do not rely on memory alone when designing skills, progressive disclosure, and security:

- [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) (Anthropic Engineering, progressive disclosure, metadata, bundled scripts)
- [anthropics/skills](https://github.com/anthropics/skills) (examples, `template/`, `spec/`, document skills patterns)
- [agentskills.io specification](https://agentskills.io/) and [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) (scope, tokens, defaults, gotchas, when to split reference files)

### RPA workflow skills in this repo

| Skill directory | Purpose |
|-----------------|--------|
| `rpa-init` | Context warm-up: code, docs, test code, dev env setup, run tests, short report (no extra user brief) |
| `rpa-gen-rules` | Agent rules (Cursor `.mdc`, Claude Code `.claude/`); layered-cake + BDD; examples under `references/cursor-examples/.cursor/`, `references/claude-examples/.claude/` |
| `rpa-feat` | New feature by BDD; requires task text; plan, red/green, full suite, docs, linter at end |
| `rpa-bugfix` | Bugfix with repro test first; requires bug description; full suite, short report |

---

## 1. Directory Structure

Create a dedicated directory for each skill under the repository root. The directory name should be the **skill’s name
** (lower‑case, hyphen‑free), unless the skill is part of the `rpa-*` workflow set where hyphenated names match the
invocation (`rpa-init`, `rpa-gen-rules`, `rpa-feat`, `rpa-bugfix`).

```
<repo-root>/my-skill/
    ├─ SKILL.md       # Mandatory metadata and loading instructions
    ├─ README.md      # Human‑readable documentation (optional but recommended)
    └─ <implementation files>
```

## 2. Mandatory `SKILL.md`

Every skill must contain a `SKILL.md` file with the following **YAML front‑matter** (enclosed between `---` lines):

```yaml
---
name: <skill‑name>
version: <semantic‑version>   # e.g. 1.0.0
description: >
  <Brief, human‑readable summary of what the skill does and when to use it>
---
```

- **`name`** – Unique identifier used by the loader (`name: logika`).
- **`version`** – Semantic version (`major.minor.patch`). Allows the system to manage updates and compatibility.
- **`description`** – One or two sentences that explain the skill’s purpose and typical triggers.

### Example

```yaml
---
name: skill-name
version: 1.0.0
description: >
  Provides a classical formal‑logic framework for reasoning, syllogism checking,
  fallacy detection, and inductive methods.
---
Body of skill with all details.
```

## 3. Optional Metadata

You may add additional keys after the mandatory block, such as:

- `author`
- `tags`
- `dependencies`
  These are ignored by the loader but can be useful for documentation.

## 4. Human‑Readable Documentation (`README.md`)

Create a `README.md` inside the skill directory that explains:

- The problem domain the skill addresses.
- How the skill is structured (reference files, helper scripts, etc.).
- Usage examples and typical triggers.
- Any required external resources.

## 5. Implementation Files

Place the actual code, reference data, or assets the skill needs in the same directory or sub‑folders. Keep the layout
logical; for example, a `references/` folder for markdown reference material, or a `src/` folder for Python/JS modules.

## 6. Testing (recommended)

If the skill includes executable logic, add tests under a `tests/` folder and ensure they pass before committing.

## 7. Commit Guidelines

When adding a new skill:

1. Stage the new directory (`git add <skill‑name>/`).
2. Commit with a clear message, e.g., `feat: add logika skill – formal logic reasoning`.
3. Push to the appropriate branch and open a PR for review.

---

## Quick Checklist

- [ ] Directory created with skill name.
- [ ] `SKILL.md` present with **name**, **version**, **description**.
- [ ] Human‑readable `README.md` added.
- [ ] Implementation files placed.
- [ ] (Optional) tests added and passing.
- [ ] Commit follows conventional commit style.

Following this template ensures all agent skills are discoverable, versioned, and maintainable across the project.
