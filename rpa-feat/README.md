# New feature (BDD)

## Purpose

Add a feature **by BDD**: **plan**, tests (**red**), code (**green**), **full test run**, **docs and examples**, **linter / pre-commit** at the end when the repo uses them.

**You must pass what to build** (for example issue text, acceptance criteria). **`/rpa-feat` alone is not enough.**

## When to use

- User runs **`/rpa-feat`** and supplies a **feature description** in the same turn or right after.

## Workflow (summary)

1. Study code, docs, tests.
2. Plan (components, contracts, edge cases).
3. Add failing tests, then implementation.
4. Run all tests; update docs and examples.
5. Run linter or `pre-commit` when configured.

## Contents

| File       | Role                    |
|------------|-------------------------|
| `SKILL.md` | Metadata and full steps |

