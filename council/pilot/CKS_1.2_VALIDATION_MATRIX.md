# CKS 1.2 Discovery Validation Matrix

Status: DISCOVERY DRAFT

| Area | Current result | Evidence / next gate |
|---|---|---|
| CKS 1.1 ingestion boundary | PASS | Production test result packet |
| Evidence separation | PASS | Existing protocols + result packet |
| Human Gate protection | PASS | Council pilot / Issue #4 |
| Merge protection | PASS | PR #3 remains draft and unmerged |
| CORE isolation | PASS | No intended CORE changes in discovery artifacts |
| Knowledge/runtime separation | PASS | Draft schema constraints |
| Owner/task leakage | PASS | Draft schema constraints |
| Decision Memory model | DRAFT | Needs executable schema validation + lifecycle implementation |
| Rejected-history lifecycle | GAP | Issue #5 |
| Experience model | DRAFT | Needs executable schema validation + lifecycle implementation |
| Evolution model | DRAFT | Needs review and Human Gate before promotion |
| Cross-reference integrity | PARTIAL | Index created; repository-level automated reference checker not yet established |
| CKS 1.2 candidate promotion | BLOCKED | Human Gate required |

## Exit criteria for Discovery

1. Draft schemas validate through repository tooling.
2. Decision Memory rejected-history lifecycle is executable and tested.
3. Experience lifecycle is executable and tested.
4. Evolution proposals cannot mutate CORE automatically.
5. Reference integrity is checked automatically or independently verified.
6. Council review completes with evidence.
7. Human Gate explicitly authorizes Candidate promotion.

Discovery PASS does not imply Candidate, Accepted, Stable, or Canon status.
