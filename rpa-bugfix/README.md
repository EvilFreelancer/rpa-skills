# Bugfix with regression tests

## Purpose

Fix a bug: **reproduction test** first, then **fix**, then **full test suite**, then a **short report**.

**You must describe the bug** (expected vs actual, how to reproduce, issue text). **`/rpa-bugfix` alone is not enough.**

## When to use

- User runs **`/rpa-bugfix`** and provides **bug details**.

## Workflow (summary)

1. Write failing test that reproduces the bug.
2. Fix code; confirm test passes.
3. Run all tests; run linter or pre-commit when configured.
4. Short factual report.

## Contents

| File       | Role                    |
|------------|-------------------------|
| `SKILL.md` | Metadata and full steps |
