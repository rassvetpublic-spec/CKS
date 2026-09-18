# CKS ASYNC HANDOFF PROTOCOL v1.2

## Purpose

Protocol for transferring implementation state from Worker to QA+REVIEW without mixing execution and decision roles.

## Core principles

- HANDOFF is not a code change.
- SHA is the boundary of verified state.
- VERDICT stores the decision, not the discussion process.
- History stores completed decisions.

## Flow

CODE

commit

SHA STATE

↓

HANDOFF

↓

QA+REVIEW

↓

VERDICT

↓

HISTORY

## Handoff contract

```yaml
HANDOFF:
  version:
  pr:
  worker:
  sha:
  base_sha:
  changes:
  tests:
  evidence:
  blockers:
  next_action:
```

## Freeze rule

After HANDOFF, HEAD and BASE must remain unchanged until verdict completion.

If SHA changes, previous HANDOFF is invalid.
