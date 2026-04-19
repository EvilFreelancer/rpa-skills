# Project onboarding

## Purpose

Onboard the agent onto a codebase: read code, documentation, and tests, run the test suite, and return a **short report**. Treats tests as the durable specification of behavior (BDD-oriented: learn expected behavior from executable tests and assertions first).

## When to use

- User runs **`/rpa-init`** or asks to understand a repo, warm up context, or produce an onboarding summary.
- No separate task description is required; the agent discovers `.venv`, pytest (or project-specific runners), and entrypoints.

## What the agent does

1. Scan layout, docs, and test configuration.
2. Run tests (for example `pytest` via `.venv` when present).
3. Summarize purpose, how tests map to behavior, gaps, and suggested next steps.

## Contents

| File       | Role                          |
|------------|-------------------------------|
| `SKILL.md` | Metadata and full workflow    |
