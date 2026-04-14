---
name: code-simplifier
description: Simplify and refine existing source code for clarity, consistency, and maintainability while preserving exact behavior. Use when the user asks for code simplification, cleanup, readability improvements, redundancy removal, post-implementation polish, or a safe refactor of recently modified code without changing functionality.
---

# Code Simplifier

## Overview

Refine existing code conservatively. Preserve outputs, side effects, public behavior, and integration contracts.

Default to the smallest safe scope. Prefer recently modified files, the current diff, or the code explicitly named by the user.

## Workflow

1. Identify scope.
   Use the files named by the user first. If the user did not name files, inspect the current diff, recent edits, or the smallest local area that matches the request.
2. Discover project constraints.
   Read local guidance such as `CLAUDE.md`, `AGENTS.md`, lint config, formatter config, type config, and nearby code patterns before editing.
3. Simplify without changing behavior.
   Remove redundancy, flatten avoidable nesting, clarify naming, and make control flow easier to follow.
4. Preserve important structure.
   Keep abstractions that carry meaning, protect boundaries between concerns, and avoid "clever" compression that makes debugging harder.
5. Verify.
   Run focused tests, linters, or type checks when they exist and are relevant to the changed scope.

## Simplification Rules

- Preserve functionality exactly.
  Do not change inputs, outputs, observable side effects, data formats, error semantics, public APIs, or persistence behavior unless the user explicitly asks for that.
- Prefer explicit code over dense code.
  Do not collapse logic into terse one-liners when it hurts readability.
- Reduce unnecessary complexity.
  Remove dead branches, duplicated checks, redundant wrappers, needless indirection, and avoidable temporary state.
- Improve control flow.
  Reduce deep nesting where practical. For multi-branch logic, prefer readable `if` / `else` chains or `switch` over nested ternaries.
- Improve naming only when it is safe.
  Rename locals, helpers, or private members when it clearly improves comprehension and does not expand scope unnecessarily.
- Keep useful abstractions.
  Do not inline or merge code just to reduce line count when the existing structure helps organization, reuse, or testing.
- Remove low-value comments.
  Delete comments that restate obvious code. Keep comments that explain intent, invariants, or non-obvious decisions.
- Match project conventions.
  Follow the repository's established patterns for imports, typing, component structure, error handling, formatting, and module organization.

## Decision Rules

- If a change might alter behavior, stop and either narrow the edit or make the behavior change explicit.
- If the code is already clear, prefer no change over speculative cleanup.
- If a project rule conflicts with generic cleanup instincts, follow the project rule.
- If a simplification would broaden scope across many unrelated files, split it into smaller passes or keep the change local.

## Typical Requests

- "Simplify the code I just changed."
- "Clean up this function without changing behavior."
- "Reduce redundancy in this component."
- "Refactor this module for readability only."
- "Polish the latest diff and keep the same functionality."

## Output Expectations

When reporting results, summarize the meaningful simplifications, note any assumptions, and mention what verification was run. Keep the summary brief unless the user asks for a detailed review.
