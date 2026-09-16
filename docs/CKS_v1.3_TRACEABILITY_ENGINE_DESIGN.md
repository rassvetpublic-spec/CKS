# CKS v1.3 Traceability Engine Design

## Object chain

```text
GAP
 ↓
Issue
 ↓
Evidence
 ↓
Proposal
 ↓
Decision
 ↓
Change
 ↓
History
```

## Required relations

- every Proposal links to GAP;
- every Decision links to Evidence;
- every Core change links to Decision;
- every rejection preserves history.

## Goal

Prevent orphan decisions and undocumented knowledge changes.
