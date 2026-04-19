---
name: rpa-feat
version: 1.0.0
description: >
  Run when the user invokes /rpa-feat and then describes a new feature. Uses TDD: failing tests first,
  implementation, full pytest run, then documentation updates. Expects feature text in the same message or follow-up.
---

# RPA feature work (TDD)

## When this skill applies

The user message should include `/rpa-feat` (or equivalent) and a **feature description** (what to build, acceptance criteria, edge cases). If the description is only "add X", ask one short clarifying question only when blocking.

## Principles

Tests are the project long-term memory. Add behavior by first writing tests that encode the contract, then code that satisfies them, then run **all** tests to guard regressions.

## Workflow

1. **Understand** existing code, docs, and tests. Virtualenv: `.venv` when present. Align with `.cursor/rules/` if it exists.
2. **Plan** briefly: touched modules, scenarios, edge cases, public API or config changes.
3. **Write tests** that describe the new behavior. Names and structure should match project conventions (see `tests/` and any `testing.mdc` rule).
4. **Run new tests** and confirm they **fail** for the right reason (feature absent or incorrect).
5. **Implement** the smallest change that makes the new tests pass. Follow architecture boundaries and style rules.
6. **Run the full test suite** (for example `pytest`). Fix any regressions.
7. **Update documentation** where behavior, configuration, or public API changed (README, `docs/`, examples). Keep examples consistent with code (for example paired `examples.md` and `.http` if the project uses that pattern).
8. **Optional quality gate** if the repo uses it: `pre-commit run -a` and fix reported issues.

## Report

Close with a compact summary: what was implemented, which tests were added or changed, full suite result, docs touched.
