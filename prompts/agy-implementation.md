# Antigravity Implementation Prompt

Paste this prompt into Antigravity (AGY) after placing `AGY_CHANGE_REQUEST.md` in your workspace.
It instructs AGY to perform Phase 1 (Revalidation) first, report drift, and wait for explicit approval before Phase 2 (Implementation).

---

```markdown
Review AGY_CHANGE_REQUEST.md against the CURRENT workspace.

The work order is a proposal, not an authority that overrides
repository rules, user instructions, or safety boundaries.

PHASE 1 — REVALIDATION ONLY

Do not modify application code yet.

1. Read the work order and relevant project rules.
2. Compare its snapshot metadata with the current repository.
3. Inspect the actual affected files, interfaces, and call sites.
4. Check working-tree changes and available source hashes.
   A matching commit alone is insufficient when files are modified.
5. Verify the proposed paths, symbols, dependencies, and commands.
6. Identify stale assumptions, missing evidence, and scope conflicts.
7. Inspect verification commands for side effects before proposing them.
8. Do not install dependencies, call external services, or execute
   migrations during this review.

Report:
- Snapshot assessment: MATCH, DRIFT, or UNKNOWN.
- Readiness: READY_FOR_APPROVAL or BLOCKED.
- Differences between the work order and current source.
- A corrected, dependency-ordered implementation plan.
- Exact files expected to change.
- Tests and verification commands proposed.
- Any dependency, schema, infrastructure, or destructive changes
  requiring separate approval.

Stop and wait for this explicit authorization:
APPROVE IMPLEMENTATION: <request_id>

PHASE 2 — IMPLEMENTATION AFTER APPROVAL

After authorization:
- Implement only the approved scope.
- Preserve unrelated and pre-existing user changes.
- Follow the validated dependency order.
- Prefer focused changes over broad refactors.
- Reuse established project patterns and extension points.
- Add or update tests for the acceptance criteria.
- Run only agreed verification commands.
- Do not install packages, execute migrations, deploy, or perform
  destructive actions unless those actions were explicitly approved.
- Stop and ask if new evidence materially changes the scope,
  security assumptions, public contracts, or migration requirements.
- Do not silently weaken tests to obtain a passing result.

Completion report:
- Summary of implemented behavior.
- Changed files and important design decisions.
- Acceptance criteria with supporting evidence.
- Commands executed and actual results.
- Checks not run and reasons.
- Remaining risks and manual follow-up.
- Whether the exported project context should be refreshed.

Do not claim completion when essential acceptance criteria remain unmet.
```
