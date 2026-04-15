# Documentation Templates

## `docs/refactor/refactor-index.md`

```markdown
# Refactor Index

## Service Status
| Service | Status (`pending`/`in-progress`/`done`) | Owner | Last Updated | Commit |
|---|---|---|---|---|
| services/user-service | pending | - | - | - |

## Round Timeline
| Round | Service | Result | Commit | Date |
|---|---|---|---|---|
| 1 | services/user-service | done | abc1234 | 2026-04-15 |
```

## `docs/refactor/technical.md`

```markdown
# Technical Notes

## Architecture Snapshot
- Current service boundaries:
- Key interfaces and contracts:
- Data flow:

## Round {{N}} - {{service}}
- Refactor scope:
- Design changes:
- Public API impact:
- Compatibility risks:
- Test impact:
```

## `docs/refactor/task-brief.md`

```markdown
# Task Brief

## Current Round
- Round: {{N}}
- Service: {{service}}
- Goal:
- Non-goals:

## Changes
- Files changed:
- Tests/checks run:
- Results:

## Next
- Next service candidate:
- Known blockers:
```

## `docs/refactor/rationale.md`

```markdown
# Refactor Rationale

## Why Refactor
- Pain points:
- Maintenance cost:
- Defect or complexity indicators:

## Round {{N}} - {{service}}
- Why this service now:
- Options considered:
- Chosen approach:
- Why rejected alternatives are weaker:
- Expected long-term gains:
```

## Commit Message Template

```text
重构({{service}}): {{根据本次修改的中文总结}}
```
