# Workflow Checklist

## Round 0: Bootstrap (Run Once Per Repository)

1. Create `docs/refactor/` if missing.
2. Create:
   `refactor-index.md`, `technical.md`, `task-brief.md`, `rationale.md`.
3. Run
   `python3 <skill-path>/scripts/update_refactor_index.py --repo-root <repo-root>`
   to discover services by service boundary and seed `refactor-index.md` with `pending` status.
4. Record baseline branch, baseline commit SHA, and validation command set.

## Round N: Standard Refactor Cycle

1. Read all four docs under `docs/refactor/`.
2. Re-run index sync script to pick up new services.
3. Select one service:
   first `in-progress`, else first `pending`.
4. Mark service `in-progress` in `refactor-index.md`.
5. Refactor service only.
6. Execute validation for changed scope.
7. Update:
   `technical.md`, `task-brief.md`, `rationale.md`, `refactor-index.md`.
8. Mark service `done` with date and commit SHA.
9. Commit all related code and docs once using:
   `重构(<服务名>): <根据本次修改的总结>`

## Failure Handling

1. If validation fails, fix within same service scope.
2. If blocked, keep service as `in-progress`.
3. Write blocker and next action in `task-brief.md`.
4. Do not move to next service before resolving blocker.
