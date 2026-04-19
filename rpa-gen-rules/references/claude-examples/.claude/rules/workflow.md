# Workflow (global rule)

This file has **no** `paths` frontmatter, so it loads at session start like `.claude/CLAUDE.md`. See [modular rules](https://code.claude.com/docs/en/memory#organize-rules-with-claude-rules).

## Documentation and examples (optional convention)

If the project uses paired API docs:

- Narrative examples in `docs/examples.md`
- Runnable HTTP in `docs/examples.http`

Keep them in sync when you add or change an example.

## New features (TDD)

When the user asks for a new feature (including words like "feature", "add", "implement", "фича", "добавить"), use this order. Do not skip steps.

1. Write a test that describes the new behavior in `tests/test_*.py`. The test must **fail** (red) for the right reason.
2. Run only that test and confirm it fails.
3. Implement the smallest change that makes the test pass (green).
4. Run the full test suite. All tests must pass.
5. Run `pre-commit run -a` if the project uses pre-commit. Fix reported issues.
6. Update docs where public behavior, config, or API changed.

## Bug fixes (TDD)

1. Write a regression test that reproduces the bug. It must **fail** on the broken code.
2. Fix the implementation.
3. Confirm the new test passes, then run the full suite.
4. Run `pre-commit run -a` if configured.

## Before the final answer

- Full test run is green.
- Optional linter or pre-commit is clean when the repo expects it.
- Report what changed, which tests were added, and results.

## Relationship to `implementation-order.md`

That file describes **layers and dependencies**. For **new behavior**, this file wins on order (test first, then code). Use `implementation-order.md` to choose where code belongs in the stack.
