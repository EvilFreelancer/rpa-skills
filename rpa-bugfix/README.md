# Bugfix with regression tests

## Purpose

Fix a bug using a **regression test first**: reproduce the failure, fix the code, run the full suite, then give a short factual report.

## When to use

- User runs **`/rpa-bugfix`** and describes the bug (expected vs actual, how to reproduce).
- Ask a clarifying question only when reproduction is impossible without it.

## Workflow (summary)

1. Add a test that fails on the current code and captures the bug.
2. Fix the implementation with minimal scope.
3. Confirm the new test passes; run **all** tests.
4. Optional `pre-commit run -a` if the project relies on it.

## Contents

| File       | Role                    |
|------------|-------------------------|
| `SKILL.md` | Metadata and full steps |
