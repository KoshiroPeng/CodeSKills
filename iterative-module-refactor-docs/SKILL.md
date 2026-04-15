---
name: iterative-module-refactor-docs
description: Incrementally refactor a code repository one service boundary per round with persistent documentation and git commits. Use when the user requests multi-round refactoring, asks to refactor by service, requires three docs per round (technical doc, task brief, rationale doc), wants completed services skipped in future rounds, and expects every round to read prior docs first, update docs after changes, and commit results.
---

# Iterative Service Refactor

## Overview

Run a deterministic, service-by-service refactor loop that can continue across many sessions.
Persist progress in repo docs so future rounds resume from the next unfinished service instead of repeating completed work.

## Mandatory Repo Artifacts

Create and maintain these files under `docs/refactor/` in the target repository:

1. `docs/refactor/refactor-index.md`
2. `docs/refactor/technical.md`
3. `docs/refactor/task-brief.md`
4. `docs/refactor/rationale.md`

Read [workflow.md](references/workflow.md) before executing the loop.
Use [templates.md](references/templates.md) whenever creating or extending docs.
Use `scripts/update_refactor_index.py` to auto-scan service boundaries and sync index status.

## Execution Loop (One Service Per Round)

1. Read `docs/refactor/refactor-index.md`, `technical.md`, `task-brief.md`, and `rationale.md`.
2. Run `python3 <skill-path>/scripts/update_refactor_index.py --repo-root <repo-root>`.
3. Build a service queue from `refactor-index.md`.
4. Select the first service whose status is not `done` in `refactor-index.md`.
5. Refactor only that service in this round.
6. Run relevant tests/lint/type checks for changed scope.
7. Update all three docs and index immediately after code changes.
8. Commit code + docs in one git commit.
9. Mark selected service as `done` in `refactor-index.md` with commit SHA and date.

If no service remains, stop and report completion.

## Service Selection And Skip Rules

Treat `refactor-index.md` as the source of truth.
Never refactor a service already marked `done`.
If a service is `in-progress`, resume it before starting a new service.
When new services appear later, append them as `pending` to the index.

## Documentation Update Rules

Update all documents every round, even for small edits.

1. `technical.md`: architecture, interfaces, data flow, constraints, risk notes.
2. `task-brief.md`: what changed in this round, affected files, validation results, next service.
3. `rationale.md`: why this refactor was needed, alternatives considered, why chosen approach is preferable.
4. `refactor-index.md`: service status table and round timeline.

Use append-only round sections for history, but keep the index table current.

## Commit Rules

Commit after each round using this Chinese format:

`重构(<服务名>): <根据本次修改的总结>`

Include code and documentation updates in the same commit.
Do not batch multiple services into one commit.

## Safety And Quality Gates

Preserve behavior unless the round explicitly targets behavior change.
Prefer internal simplification first: decomposition, naming, dead-code removal, and boundary clarification.
If tests are missing, add focused tests for the refactored service.
Block commit when checks fail; fix or document blocker explicitly in `task-brief.md`.

## Output Contract Per Round

At round end, always produce:

1. Refactored code for exactly one service.
2. Updated `refactor-index.md`, `technical.md`, `task-brief.md`, `rationale.md`.
3. One git commit containing all changes.
4. A concise summary listing service name, key edits, checks run, and commit SHA.

If blocked, do not pick a different service in the same round.
Record blocker details and next unblocked action in `task-brief.md`.
