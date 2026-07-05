# Authoring & maintaining the `rpa-skills` catalog

Agent guide for working **inside this aggregator repository**. Read it before editing either marketplace
manifest, the README Skills table, or the installer.

> Naming (Russian): the adjective for "agent / agentic" is **«агентный»**, never «агентский».

## What this repo is

This repo is the **catalog**, not the skills. Each skill lives in its **own repository**
(`EvilFreelancer/rpa-init`, `.../logika`, …) and that repo is the **single source of truth** for the skill's
text, `version`, `description`, and tags. This catalog only *points* at those repos and re-states some of
their metadata so agents can discover and install them.

The same catalog is exposed to different agents through three surfaces:

```
rpa-skills/
├─ .claude-plugin/
│  └─ marketplace.json      # Claude Code marketplace (per-plugin `version` + `description`)
├─ .agents/plugins/
│  └─ marketplace.json      # Codex marketplace (git-backed sources; version resolved from the skill repo)
├─ install.sh               # folder-based installer for Cursor & co. (ALL_SKILLS array of repo names)
├─ README.md                # human overview + the Skills table (one row per skill)
├─ AGENTS.md                # this file — the collection-wide process
├─ CLAUDE.md                # symlink → AGENTS.md (so Claude Code reads the same guide)
└─ LICENSE
```

## ⚠️ Golden rule: the catalog mirrors the skills — keep them in sync

When you change a skill **in its own repo** — bump its version, reword its description, change its
tags/category — this catalog keeps showing the **old** metadata until you update it here. The catalog
**follows, never leads**: release in the skill repo first, then mirror the change here in the same PR/commit.
Nothing is allowed to drift.

### The catalog surface — every place a skill's metadata is duplicated

| Changed in the skill repo | Update here |
|---------------------------|-------------|
| **version** bump | `.claude-plugin/marketplace.json` → the plugin's `version`. Codex manifest only if its entry pins a `ref`/`sha` (see below). Bump top-level `metadata.version` if this is a catalog release. |
| **description** | `description` in **both** manifests **and** the README Skills-table row. |
| **tags / category** | `category` in **both** manifests. |
| **new skill added** | add an entry to **both** manifests, a README table row, the `install.sh` `ALL_SKILLS` array, and bump `metadata.version`. |
| **skill removed / renamed** | remove or rename it in **all four** places above. |

### Version sync — the two manifests behave differently

- **`.claude-plugin/marketplace.json`** carries an explicit `version` per plugin. It is a **copy** of the
  skill's own version → bump it here every time the skill's `plugin.json` / `SKILL.md` version changes.
- **`.agents/plugins/marketplace.json`** (Codex) has **no** per-plugin `version`. Codex reads the version
  from the skill's own `.codex-plugin/plugin.json` at the git `ref` the entry points to:
  - entry pinned to a moving branch (`"ref": "main"`, the current default) → it auto-follows the skill repo,
    **nothing to bump**;
  - entry pinned to a **tag or `sha`** for reproducibility → update that `ref`/`sha` on every release.
- The top-level **`metadata.version`** (present in both manifests) is the **catalog** version. Bump it when
  the catalog changes shape (a skill is added/removed), independently of any single skill's version. Keep it
  identical in both manifests.

### Worked example — releasing `rpa-init` 1.1.0

1. **In the `rpa-init` repo:** bump to `1.1.0`, edit the description if it changed, commit, tag, push.
2. **Here in `rpa-skills`:**
   - `.claude-plugin/marketplace.json` — set `rpa-init` → `"version": "1.1.0"`; update `description` if changed.
   - `.agents/plugins/marketplace.json` — update `description` if changed. If the entry pins a tag/sha, point
     it at the new release; if it points at `main`, nothing to do.
   - `README.md` — update the `rpa-init` row only if its purpose/description changed.
   - `install.sh` — no change (it clones by repo name, not by version).
   - Bump `metadata.version` only if you also consider this a catalog release.
3. Validate and commit (below).

## Adding a new skill to the catalog

1. Publish the skill's **own repo** first (flat layout: `SKILL.md` at the repo root, its own
   `.claude-plugin/` + `.codex-plugin/` manifests). The catalog cannot resolve an entry whose repo is not
   pushed.
2. Add a plugin entry to **both** manifests. Claude entry: `source: {source:"github", repo:"EvilFreelancer/<name>"}`.
   Codex entry: `source: {source:"url", url:"https://github.com/EvilFreelancer/<name>.git", ref:"main"}` plus
   `policy` + `category`.
3. Add a row to the README **Skills** table and add `<name>` to `install.sh`'s `ALL_SKILLS`.
4. Bump `metadata.version` in both manifests.

## Validate before committing

```bash
python3 -m json.tool .claude-plugin/marketplace.json  >/dev/null && echo claude-ok
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null && echo codex-ok
bash -n install.sh && echo installer-ok

# the skill list must be identical across all three catalog surfaces:
python3 - <<'PY'
import json,re
claude=[p['name'] for p in json.load(open('.claude-plugin/marketplace.json'))['plugins']]
codex =[p['name'] for p in json.load(open('.agents/plugins/marketplace.json'))['plugins']]
m=re.search(r'ALL_SKILLS=\((.*?)\)', open('install.sh').read(), re.S)
sh=m.group(1).split() if m else []
print('claude   :', claude)
print('codex    :', codex)
print('install  :', sh)
print('IN SYNC  :', claude==codex and set(claude)==set(sh))
PY
```

## Commit checklist

- [ ] The skill's own repo already released the change (the catalog **follows**, never leads).
- [ ] Both manifests updated — `version` where applicable, `description`, `category`.
- [ ] README **Skills** table row updated.
- [ ] `install.sh` `ALL_SKILLS` updated if a skill was added / removed / renamed.
- [ ] `metadata.version` bumped (and identical in both manifests) if the catalog shape changed.
- [ ] JSON validates and the skill lists match across both manifests + `install.sh`.
- [ ] Conventional commit, e.g. `chore(catalog): sync rpa-init 1.1.0`.

---

Part of the **[rpa-skills](https://github.com/EvilFreelancer/rpa-skills)** collection. Each skill repo has its
own `AGENTS.md` for authoring **that** skill; this file governs the **catalog**. See also
[cursor-vibe-prompts](https://github.com/EvilFreelancer/cursor-vibe-prompts).
