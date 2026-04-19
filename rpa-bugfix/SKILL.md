---
name: rpa-bugfix
version: 1.0.0
description: >
  Run when the user invokes /rpa-bugfix and describes a bug. Writes a failing reproduction test first, fixes the code, runs all tests, and returns a short report. Expects bug description from the user.
---

# RPA bugfix (test-first)

## When this skill applies

The user message should include `/rpa-bugfix` (or equivalent) and a **bug description** (expected vs actual, how to reproduce, environment if relevant). Ask a clarifying question only when reproduction is impossible without it.

## Principles

A bug is a mismatch between intended behavior and current behavior. Encode the intention in a **regression test** so the bug cannot return unnoticed.

## Workflow

1. **Understand** the area of code from the report and from existing tests. Use `.venv` and project test commands as usual.
2. **Write a test** that fails on the current code and demonstrates the bug. Place it with related tests following project layout.
3. **Run** that test and confirm it fails for the expected reason.
4. **Fix** the implementation with the smallest reasonable change. Respect architecture and `.cursor/rules/` if present.
5. **Run** the new test until it passes.
6. **Run the full test suite** to catch side effects.
7. **Optional** `pre-commit run -a` if the project relies on it.

## Report

Short and factual: cause, fix, test added or changed, full suite outcome, files touched.
