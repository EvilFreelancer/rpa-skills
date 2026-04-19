---
paths:
  - "**/*.py"
---

# Python code style

Loads when editing any Python file. Align with `ruff.toml`, `pyproject.toml`, or team standards.

## General

1. Code comments only in English unless the project says otherwise.
2. Type hints on public functions and methods when the codebase uses them.
3. End new files with a newline.

## Imports

Order: standard library, third party, local. One import style per project (follow `ruff` / `isort` config).

## References

Point `@` imports in `CLAUDE.md` at `@ruff.toml` or `@pyproject.toml` so tools stay authoritative.
