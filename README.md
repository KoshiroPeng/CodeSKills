# CodeSKills

CodeSKills is a local skill collection for Codex/Cursor-style coding assistants.
This repository currently includes five engineering-focused skills:
- `code-review`
- `code-simplifier`
- `code-slim-refactor`
- `iterative-module-refactor-docs`
- `worklog-skill`

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
|-- iterative-module-refactor-docs/
|   |-- SKILL.md
|   |-- agents/openai.yaml
|   |-- scripts/update_refactor_index.py
|   `-- references/*.md
|-- worklog-skill/
|   |-- SKILL.md
|   `-- agents/openai.yaml
`-- README.md
```

## Skills Overview

### 1) `worklog-skill`

Purpose:
- Fill work logs and daily reports in internal Zentao and daily-report systems.

Systems:
- Zentao: `http://172.16.3.197/max` - Task work hours logging
- Daily Report: `http://172.16.4.152/login` - Daily report confirmation

Workflow:
1. Open Zentao first, log in and record work hours
2. Validate the Zentao operation
3. Only then open daily-report system
4. Fill the daily report

Quick Commands:
```powershell
# Zentao login
playwright-cli.cmd -s=maxlogin fill e17 "pengkang"
playwright-cli.cmd -s=maxlogin fill e21 "Netinfo2025"
playwright-cli.cmd -s=maxlogin click e29

# Daily report login
playwright-cli.cmd -s=report152 fill e18 "pengkang"
playwright-cli.cmd -s=report152 fill e25 "888888"
playwright-cli.cmd -s=report152 click e31
```

Typical trigger phrases:
- `填写日报`
- `填日报`
- `fill daily report`

### 3) `code-review`

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

### 4) `code-simplifier`

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

### 5) `code-slim-refactor`

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

### 6) `iterative-module-refactor-docs`

Purpose:
- Run multi-round refactors one service boundary at a time with persistent documentation and per-round commits.

Highlights:
- Uses `docs/refactor/refactor-index.md` as the source of truth for service queue and status.
- Requires four maintained artifacts:
- `refactor-index.md`
- `technical.md`
- `task-brief.md`
- `rationale.md`
- Includes `scripts/update_refactor_index.py` to auto-scan service boundaries and sync index.
- Enforces one-service-per-round execution and one commit per round.

Typical trigger phrases:
- `iterative refactor by service`
- `multi-round refactor with docs`
- `incremental module refactor`

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
