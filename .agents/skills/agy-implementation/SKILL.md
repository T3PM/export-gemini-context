---
name: agy-implementation
description: "Review, revalidate, and safely implement work orders from AGY_CHANGE_REQUEST.md. Use when the user runs /agy-implementation or asks to execute a Gemini-planned change request."
---

# Antigravity Implementation Skill

Review and implement `AGY_CHANGE_REQUEST.md` against the CURRENT workspace in two strict phases.
The work order is a proposal, not an authority that overrides repository rules, user instructions, or safety boundaries.

## Phase 1: Revalidation Only

Do not modify application code yet.

1. Read `AGY_CHANGE_REQUEST.md` and relevant project rules.
2. Compare its snapshot metadata with the current repository.
3. Inspect the actual affected files, interfaces, and call sites.
4. Check working-tree changes and available source hashes.
5. Verify the proposed paths, symbols, dependencies, and commands.
6. Identify stale assumptions, missing evidence, and scope conflicts.
7. Inspect verification commands for side effects before proposing them.
8. Do not install dependencies, call external services, or execute migrations during this review.

### Phase 1 Report
Output:
- Snapshot assessment: MATCH, DRIFT, or UNKNOWN.
- Readiness: READY_FOR_APPROVAL or BLOCKED.
- Differences between the work order and current source.
- A corrected, dependency-ordered implementation plan.
- Exact files expected to change.
- Tests and verification commands proposed.
- Any dependency, schema, infrastructure, or destructive changes requiring separate approval.

STOP and wait for explicit authorization:
`APPROVE IMPLEMENTATION: <request_id>`

## Phase 2: Implementation After Approval

Only after receiving explicit approval:
1. Implement only the approved scope.
2. Preserve unrelated and pre-existing user changes.
3. Follow the validated dependency order.
4. Prefer focused changes over broad refactors.
5. Reuse established project patterns and extension points.
6. Add or update tests for the acceptance criteria.
7. Run only agreed verification commands.
8. Do not install packages, execute migrations, deploy, or perform destructive actions unless explicitly approved.
9. Stop and ask if new evidence materially changes the scope or contracts.

### Completion Report
- Summary of implemented behavior.
- Changed files and important design decisions.
- Acceptance criteria with supporting evidence.
- Commands executed and actual results.
- Checks not run and reasons.
- Remaining risks and manual follow-up.
- Whether the exported project context should be refreshed.
