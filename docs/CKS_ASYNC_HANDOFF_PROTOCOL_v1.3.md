# CKS ASYNC HANDOFF PROTOCOL v1.3

## Purpose

Protocol for asynchronous transfer of state between Worker, QA, and Review Controller, connecting the protocol to real asynchronous execution workflows.

## Target Model & Lifecycle

The task execution lifecycle is tracked via a single authoritative Task State Object:

```text
READY → IN_PROGRESS → HANDOFF → QA → REVIEW → VERDICT → MERGED
```

```text
TASK
  ↓
OWNER (Worker A/B)
  ↓
HANDOFF
  ↓
QA+REVIEW CONTROLLER
  ↓
VERDICT
  ↓
HISTORY
```

### Lifecycle States

1. **READY**: Task is specified, prerequisites identified, unassigned or awaiting execution start.
2. **IN_PROGRESS**: Claimed by Owner (Worker A / Worker B), active implementation on a dedicated branch.
3. **HANDOFF**: Owner completes changes, pushes branch, creates PR, and emits HANDOFF with exact SHA, BASE_SHA, and evidence links.
4. **QA**: Independent verification against exact SHA and tests/CI gates.
5. **REVIEW**: Architecture and contract review against SSOT and canon boundaries.
6. **VERDICT**: Decision recorded by Review Controller referencing exact SHA (`APPROVED` | `REQUEST_CHANGES` | `BLOCKED`).
7. **MERGED**: Task completed, PR merged into target branch, state recorded in history.

## Roles and Separation

Strict separation of roles is enforced to prevent role ambiguity:

- **OWNER (Worker A / Worker B)**: Implements changes, owns the execution lane, creates branch/PR, and emits HANDOFF. Does NOT issue self-verdicts or perform self-merging.
- **CHECKER (QA Controller)**: Validates tests, verifies evidence artifacts, and confirms exact SHA matches.
- **DECIDER (Review Controller / Repo Admin)**: Validates SSOT consistency, compliance with canon invariants, issues VERDICT, and approves merge.

No single agent or participant may combine conflicting roles for the same change boundary.

## Rules

- **Single Task State Tracking**: One task can be tracked from assignment to merge via its Task State Object (`schemas/cks-task-state.schema.json` and `templates/TASK_TEMPLATE.md`).
- **Exact Verification Boundary**: `SHA` + `BASE_SHA` define the immutable boundary of verified state.
- **HANDOFF vs Commits**: HANDOFF represents state transfer, not EVIDENCE. Keep HANDOFF separate from code commits. Do NOT create commits solely for state exchange.
- **VERDICT Integrity**: A VERDICT is valid only for the exact SHA referenced. Any new commit/SHA invalidates the previous verdict and resets the review gate.
- **Declared Return Channel**: Every TASK and HANDOFF must declare its repository and return channel (default: GitHub PR conversation). All worker feedback and review verdicts must return through the declared channel.

## Model Summary

```text
PR         = work object
TASK STATE = lifecycle object (`schemas/cks-task-state.schema.json`, `templates/TASK_TEMPLATE.md`)
HANDOFF    = state transfer
EVIDENCE   = verifiable proof (CI runs, test logs, artifact SHAs)
VERDICT    = authoritative decision
CHANNEL    = return path for execution feedback
HISTORY    = recorded repository knowledge
```
