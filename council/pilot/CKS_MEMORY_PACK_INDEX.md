# CKS Memory Pack Index

## Purpose
Minimal set of documents required to continue CKS work after chat migration or deletion.

## Bootstrap layer

| Order | File | Purpose |
|---|---|---|
| 1 | `CKS_BOOTSTRAP_CONTEXT.md` | Initial orientation |
| 2 | `CKS_BOOTSTRAP_SNAPSHOT_2026-09-15.md` | Current state snapshot |
| 3 | `CHAT_DELETE_HANDOFF.md` | Chat migration handoff |

## Decision layer

| File | Purpose |
|---|---|
| `HUMAN_GATE_DECISION_BRIEF.md` | Decision boundary |
| `CKS_FINAL_STATUS_REPORT.md` | Current project state |

## Evidence layer

| File | Purpose |
|---|---|
| `CKS_FINAL_EVIDENCE_INDEX.md` | Evidence map |
| `CKS_FINAL_CONSISTENCY_CHECK.md` | Consistency validation |
| `PR3_FINAL_AUTOMATION_REVIEW.md` | PR technical review |

## Recovery rule

A new working session should load this index first, then read only the required documents.

## Invariants

- CORE remains frozen.
- Runtime remains external.
- Evidence is not a decision.
- Technical PASS is not owner approval.
