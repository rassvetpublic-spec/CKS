# CKS ASYNC HANDOFF PROTOCOL v1.2

## Purpose

Protocol for asynchronous transfer of state between Worker and QA+Review Controller.

## Flow

WORKER
↓
HANDOFF
↓
QA+REVIEW CONTROLLER
↓
VERDICT
↓
HISTORY

## Rules

- SHA + BASE_SHA define the verified state boundary.
- HANDOFF is not EVIDENCE.
- VERDICT is valid only for the exact SHA.
- New SHA invalidates previous verdict.
- Commit is used only for repository changes, not state exchange.

## Model

PR = work object
HANDOFF = state transfer
EVIDENCE = proof
VERDICT = decision
HISTORY = recorded knowledge
