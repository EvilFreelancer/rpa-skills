---
name: rpa-init
version: 1.0.0
description: >
  Run when the user invokes /rpa-init or asks to onboard, warm up context, or understand a repository.
  Loads the codebase with a BDD mindset: behavior is captured in executable tests (pytest). Produces a short report.
  No extra user story is required; discover venv, test layout, and docs yourself.
---

# RPA project initialization (BDD-oriented context load)

## Intent

Treat automated tests as the project long-term memory. They repeat the same question on every run: does behavior still match what was specified? Initialization is not a tour of files only; it maps **documented intent**, **observed behavior in tests**, and **implementation**.

Behavior-Driven Development here means: derive understanding from **examples and assertions** in tests (and from Gherkin or `pytest-bdd` features **only if** the repo already uses them). Prefer reading `tests/` and any `features/` or step definitions before guessing from production code alone.

## Preconditions you must verify yourself

1. Locate the Python virtual environment. Default: `.venv` at the repository root. If missing, note it in the report instead of inventing commands that assume it exists.
2. Find how tests are run. Default runner: `pytest`. Respect `pytest.ini`, `pyproject.toml` `[tool.pytest]`, or `tox`/`nox` if present.
3. Identify entrypoints: `README`, `docs/`, package layout, `main` modules, CLI, services.

## Workflow

1. **Scan** repository structure (src layout, apps, packages in a monorepo).
2. **Read** user-facing documentation and any technical specs under `docs/` or project root.
3. **Study tests** before deep-diving into implementation: naming, fixtures, markers, integration vs unit split. This is the BDD-facing view of expected behavior.
4. **Run the test suite** using the project venv when available, for example:

   ```bash
   .venv/bin/pytest -q
   ```

   If tests fail, record failing areas and suspected ownership (do not fix unless the user asked).

5. **Summarize** in a concise report (see template below). Use English for code-related terms if the codebase uses English; respond to the user in their language.

## Report template

Use this structure (adapt sections if some are not applicable):

```markdown
## Project snapshot
- Purpose (one paragraph)
- Main packages and boundaries

## How to run tests
- venv path and pytest (or other) command actually used

## Behavior from tests
- What scenarios are locked in by tests (bullets)
- Gaps: important paths with weak or missing tests (if any)

## Risks and notes
- Flaky tests, slow suites, env secrets, external services

## Suggested next steps
- 1 to 3 concrete follow-ups for development or stabilization
```

## Constraints

- Comments in any new code: English only.
- Do not add secrets or keys.
- If the repository is not Python, still follow the same pattern: find the official test command and behavior specs, then report.
