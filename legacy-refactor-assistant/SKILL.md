---
name: legacy-refactor-assistant
description: helps plan and execute safe ai-assisted refactoring or architecture replacement for unfamiliar legacy codebases that contain important business logic which must not be deleted. use when the user wants to understand old source code, map business flows, add tests, wrap legacy logic with adapters or facades, design a new modular architecture, migrate features incrementally, compare old and new behavior, or produce refactoring plans, checklists, prompts, and review reports.
---

# Legacy Refactor Assistant

## Goal

Guide safe, incremental refactoring of unfamiliar legacy systems. Prioritize preserving behavior and business logic over producing a clean rewrite. Use AI as an analysis, documentation, verification, and small-step implementation assistant, not as an uncontrolled whole-project rewrite tool.

## Core Rules

- Never recommend deleting legacy code only because it is unclear.
- Do not rewrite an entire project in one step.
- Separate behavior preservation from architecture improvement.
- Ask for or infer the smallest useful code slice: one function, class, endpoint, module, or workflow.
- Treat unknown logic as business-critical until proven otherwise.
- Require verification before replacement: tests, logs, data checks, or old/new behavior comparison.
- Prefer modular monolith or strangler-style migration before microservices unless scale and team constraints justify otherwise.

## Default Workflow

Use this sequence unless the user asks for a narrower task.

1. **Inventory the legacy code**
   - Identify entry points, routes, jobs, commands, scheduled tasks, and external callbacks.
   - List major modules, dependencies, database tables, external APIs, queues, cache usage, and config.
   - Produce a risk map: core business logic, side effects, magic values, hidden coupling, unclear branches.

2. **Explain before changing**
   - For each submitted code slice, explain in plain language what it does.
   - Extract business rules, state transitions, side effects, dependencies, and failure paths.
   - Mark unclear assumptions explicitly.

3. **Build a protection net**
   - Recommend API regression tests, golden-master tests, core use-case tests, database read/write checks, logging, and feature flags.
   - If tests are hard, suggest characterization tests around observed behavior.

4. **Design the target architecture**
   - Prefer business-domain boundaries over purely technical layers.
   - Recommend layers such as controller/handler, application use case, domain service, repository, adapter, and infrastructure.
   - Keep database changes minimal at first unless the user explicitly targets data migration.

5. **Wrap legacy logic first**
   - Design facade/adapter interfaces around old modules.
   - Let the new architecture call old logic through stable interfaces.
   - Keep old implementation available as rollback until behavior is proven equivalent.

6. **Migrate incrementally**
   - Choose a low-risk or high-change module first.
   - Replace one endpoint/use case at a time.
   - Compare old and new outputs, side effects, logs, and database changes.
   - Use gray release, feature flags, or route-level switching where possible.

7. **Review and document**
   - Produce before/after comparison.
   - Document decisions, remaining risks, TODOs, and rollback steps.

## User Input Patterns

When the user provides code, analyze it using this structure:

```markdown
## What this code does

## Business rules found

## Inputs and outputs

## Side effects

## Dependencies

## Risk points

## Refactoring boundary

## Suggested tests

## Safe next step
```

When the user asks for a plan, produce:

```markdown
## Current assumptions

## Recommended strategy

## Migration phases

## Target architecture

## Module priority

## Risk controls

## AI prompts to use

## Immediate next actions
```

When the user asks to rewrite a module, first produce an understanding summary and ask the user to verify only if the logic is ambiguous or high risk. Otherwise provide a behavior-preserving refactor and include a checklist for equivalence validation.

## Prompt Templates

Use these templates when the user wants prompts they can paste into another AI tool.

### Understand a module

```text
Analyze this legacy module. Explain what it does in plain language. Extract business rules, inputs, outputs, database writes, external API calls, state changes, edge cases, and risky assumptions. Do not rewrite yet. Mark anything unclear.
```

### Create a flow map

```text
Based on this code, map the request flow from entry point to final side effects. Include function calls, important conditions, database tables touched, external services, emitted events, and possible failure paths.
```

### Design an adapter

```text
Design a facade/adapter that lets a new architecture call this legacy logic without changing the old code. Keep the interface business-oriented. Include method names, input/output DTOs, error handling, and rollback considerations.
```

### Behavior-preserving refactor

```text
Refactor this code for readability and layering while preserving behavior exactly. First summarize the current behavior, then show the new structure. Do not remove branches, magic values, validations, side effects, or compatibility behavior unless explicitly justified.
```

### Compare old and new logic

```text
Compare the old and new implementations. Check whether behavior, edge cases, side effects, errors, database writes, and external calls remain equivalent. List possible regressions and tests needed before release.
```

## Output Quality Checklist

Every substantial answer should include:

- What is known versus assumed.
- The safest next step, not just the ideal final architecture.
- A preservation strategy for existing business logic.
- A validation strategy before production rollout.
- Rollback or fallback guidance when changing runtime behavior.

## Architecture Guidance

Default target architecture:

```text
api/controller
  -> application use case
  -> domain service/model
  -> repository interface
  -> infrastructure repository/adapter
  -> database/external services
```

For legacy migration, use:

```text
new api or application layer
  -> legacy facade/adapter
  -> unchanged legacy business logic
```

Only recommend microservices when the user has clear independent domains, team ownership, deployment needs, observability, service contracts, and operational maturity.

## Safety Boundaries

If the user asks to remove unknown logic, respond with a safer alternative: quarantine, wrap, mark deprecated, add tests, log usage, and remove only after evidence shows it is unused and safe.
