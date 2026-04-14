# CodeSKills

CodeSKills is a local skill collection for Codex/Cursor-style coding assistants.
This repository currently includes three engineering-focused skills:
- `code-review`
- `code-simplifier`
- `code-slim-refactor`

## Repository Layout

```text
CodeSKills/
|-- code-review/
|   `-- SKILL.md
|-- code-simplifier/
|   |-- SKILL.md
|   `-- agents/openai.yaml
|-- code-slim-refactor/
|   |-- SKILL.md
|   |-- agents/openai.yaml
|   `-- references/*.md
`-- README.md
```

## Skills Overview

### 1) `code-review`

Purpose:
- Review GitHub pull requests with a structured multi-pass workflow.

Highlights:
- Uses `gh` for PR data collection.
- Includes an eligibility gate (skip closed/draft/trivial/already-reviewed PRs).
- Uses confidence scoring and keeps only high-confidence findings.
- Requires concrete links and file/line references for reported issues.

Typical trigger phrases:
- `review this PR`
- `PR review`
- `pull request audit`

### 2) `code-simplifier`

Purpose:
- Simplify existing code for readability and maintainability while preserving exact behavior.

Highlights:
- Defaults to small, conservative scope.
- Preserves outputs, side effects, APIs, data formats, and error semantics.
- Reduces redundancy and avoidable complexity without changing functionality.
- Follows repository conventions and local constraints.

Typical trigger phrases:
- `simplify the code`
- `cleanup without changing behavior`
- `refactor for readability only`

### 3) `code-slim-refactor`

Purpose:
- Run convergence-oriented refactors that reduce structural complexity while protecting current contracts.

Modes:
- `quick`: lightweight scoped pass (default)
- `strict`: auditable flow with branch/artifact/review gates

Highlights:
- Explicit contract-mismatch gate:
- `backend_regression`
- `stale_tests`
- Never weaken backend contracts or assertion standards just to satisfy tests.
- Includes workflow templates and checklists under `references/`.

Typical trigger phrases:
- `code slim`
- `slim refactor`
- `structured simplification pass`

## Quick Usage

In a skill-enabled Codex environment, trigger skills by name:

```text
Use $code-review on PR #123
Use $code-simplifier for files changed in latest commit
Use $code-slim-refactor with mode=quick on module X
```

`code-simplifier` and `code-slim-refactor` include `agents/openai.yaml` for UI metadata and default prompts.

## Design Principles

- Engineering constraints and verifiability first.
- Structural improvement without behavior drift.
- Scoped execution to avoid unbounded refactor work.

## Maintenance Notes

When adding a new skill, provide at least:
- `SKILL.md` with purpose, trigger conditions, workflow, and output format
- optional `agents/openai.yaml` for UI metadata/default prompt
- optional `references/` templates for plans, reports, and checklists when workflow is complex

After updates, include runnable examples so users can trigger the skill quickly.
