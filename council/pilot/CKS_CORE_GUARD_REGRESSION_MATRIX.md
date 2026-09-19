# CKS CORE Guard Regression Matrix

Status: DISCOVERY TEST SPECIFICATION

| Test | Expected |
|---|---|
| Add Owner to knowledge object | Reject |
| Add Task ID to knowledge object | Reject |
| Add Runtime state to knowledge object | Reject |
| Treat chat PASS as approval | Reject |
| Treat Discovery as Canon | Reject |
| Modify CORE from Discovery flow | Reject |
| Merge without Human Gate | Reject |
| Preserve rejected history with rationale | Required |

## Invariants

CORE remains frozen.
Knowledge remains separate from execution.
Decision acceptance requires evidence and approval path.
Discovery artifacts cannot silently become canon.
