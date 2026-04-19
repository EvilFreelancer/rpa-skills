# New feature (TDD)

## Purpose

Implement a **new feature** using **TDD**: failing tests first, then implementation, full test run, then documentation updates where behavior or public API changes.

## When to use

- User runs **`/rpa-feat`** and provides a **feature description** (acceptance criteria, edge cases, scope).
- Ask one clarifying question only when the request is blocking.

## Workflow (summary)

1. Study existing code, docs, and tests (`.venv` when used).
2. Short plan (components, contracts, edge cases).
3. Add tests that fail until the feature exists.
4. Implement until new tests pass; run **all** tests.
5. Update docs and examples as needed; optional `pre-commit run -a` if the repo uses it.

## Contents

| File       | Role                    |
|------------|-------------------------|
| `SKILL.md` | Metadata and full steps |
