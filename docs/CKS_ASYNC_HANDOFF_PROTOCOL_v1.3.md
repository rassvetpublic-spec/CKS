# CKS ASYNC HANDOFF PROTOCOL v1.3

## Purpose

Protocol for asynchronous transfer of state between Worker and QA+Review Controller, bridging the gap to real execution flow.

## Flow / Task Lifecycle

The task execution follows a strict lifecycle tracked via a single Task State Object:
READY → IN_PROGRESS → HANDOFF → QA → REVIEW → VERDICT → MERGED

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

## Roles and Separation

- **OWNER (Worker)**: Implements the task, owns the execution lane, and emits HANDOFF.
- **QA+REVIEW CONTROLLER**: Verifies boundaries, audits evidence, and emits VERDICT.
- **DECISION**: The VERDICT acts as the final decision before merge.
There is strict separation between Owner, Checker (QA/Review), and Decision makers. No role ambiguity is permitted.

## Rules

- **State Tracking**: One task can be tracked via its Task State Object from assignment to merge.
- **Verification Boundary**: SHA + BASE_SHA define the verified state boundary.
- **HANDOFF vs Commits**: HANDOFF is a state transfer, not EVIDENCE. Keep HANDOFF separate from code commits. Do NOT create commits only for state exchange.
- **VERDICT Integrity**: VERDICT is valid only for the exact SHA. It must reference the exact SHA. New SHA invalidates previous verdict.
- **Execution Channel**: Every HANDOFF task must define the repository and return channel. Worker results must return through the declared GitHub PR/Issue conversation channel.

## Model

PR = work object
TASK STATE = lifecycle object
HANDOFF = state transfer
EVIDENCE = proof
VERDICT = decision
CHANNEL = return path for execution feedback
HISTORY = recorded knowledge
