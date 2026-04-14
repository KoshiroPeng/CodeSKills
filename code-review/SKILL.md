---
name: code-review
description: Review GitHub pull requests with a structured multi-pass workflow when the user asks for code review, PR review, pull request audit, review this PR, or automated GitHub review. Use this skill for deliberate review passes that should filter weak findings and produce only high-confidence actionable issues.
---

# Code Review

Use this skill to review a GitHub pull request with multiple independent passes, confidence scoring, and a brief final output.

## Requirements

- Use `gh` for GitHub data instead of web browsing when repository access is available.
- Make a todo list before the main review work.
- Keep the final review brief.
- Cite concrete files, lines, and URLs for every reported issue.
- Do not run build, lint, or typecheck steps just for this review.

## Eligibility Gate

Before deep review, confirm whether the pull request should be reviewed at all.

Check for these stop conditions:
- the pull request is closed
- the pull request is a draft
- the pull request is trivial, automated, or obviously does not need review
- a review from this workflow was already posted earlier

If any stop condition applies, stop and report why no review was posted.

## Review Workflow

1. Identify the target pull request and gather the basic metadata with `gh`.
2. Find the repository guidance files relevant to the touched paths. Include the root `CLAUDE.md` if present and any closer `CLAUDE.md` files under modified directories.
3. Summarize the pull request briefly before detailed review.
4. Run independent review passes in parallel when possible:
   - guidance compliance against relevant `CLAUDE.md` files
   - obvious bug scan limited mostly to changed code
   - git history or blame review for historical context
   - previous pull request comments on the same files when accessible
   - code comments in modified files that impose local constraints
5. Deduplicate the findings.
6. Re-check each finding and assign a confidence score from `0` to `100`.
7. Drop all findings below `80`.
8. Run the eligibility gate again before preparing a final comment.
9. If no findings remain, report that no issues were found.
10. If findings remain, produce a concise review comment draft with links.

## Confidence Rubric

Score each issue with exactly one of these levels:

- `0`: false positive or not credible after light scrutiny
- `25`: possible issue but unverified or mostly stylistic
- `50`: real but relatively minor or low-impact
- `75`: very likely real and important, but not fully certain
- `100`: directly confirmed and clearly actionable

Only keep issues scored `80` or above.

## False Positive Filter

Do not report these unless repository guidance explicitly requires them:

- pre-existing issues outside the change
- cosmetic nits or pedantic style complaints
- problems that CI, compilers, typecheckers, or linters will catch
- vague code quality complaints without a concrete defect
- likely intentional behavior changes tied to the PR goal
- issues on lines not modified by the pull request

## Output Rules

When reporting issues:

- Keep the output brief.
- Avoid emojis.
- For each issue, include:
  - a one-line description
  - why it matters
  - a concrete file link with full SHA and line range when possible
  - the applicable guidance source when the issue comes from `CLAUDE.md`

When no issues remain after filtering, state:

```markdown
### Code review

No issues found. Checked for bugs and CLAUDE.md compliance.
```

When issues remain, use this shape:

```markdown
### Code review

Found N issues:

1. Brief issue description

https://github.com/owner/repo/blob/fullsha/path/to/file#L10-L15
```
