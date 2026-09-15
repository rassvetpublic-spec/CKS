# CKS Human Gate Packet

Status: READY FOR HUMAN REVIEW

This packet prepares, but does not perform, owner decisions.

## Gate A — Council v0.1 / PR #3

Required decisions:
1. Confirm CKS 1.1 release status: retain Release Candidate, or authorize a separate Stable decision process.
2. Decide the current Council draft Decision Candidate: accept after review, return for revision, or reject.
3. Decide whether Council v0.1 may leave draft state and proceed toward integration.

Technical context:
- Council validation and CI were previously reported successful.
- PR #3 remains subject to Human Gate.
- Technical PASS is not owner approval.

## Gate B — CKS 1.2 Discovery

Requested acknowledgement only:
1. Recognize Decision Memory, Experience, Evolution, and rejected-history lifecycle as Discovery scope.
2. Keep all CKS 1.2 artifacts non-canon and non-Stable.
3. Permit implementation/testing work only after the relevant Council decision path is satisfied.

## Explicit non-actions

- No automatic merge.
- No automatic Stable promotion.
- No automatic Canon promotion.
- No CORE mutation.

## Current blockers

- Issue #4: Council Human Gate.
- Issue #5: rejected-history lifecycle is not yet verifiably implemented.

## Suggested owner decision form

- CKS 1.1 status: `RELEASE_CANDIDATE` or `START_STABLE_DECISION`
- Council v0.1: `ACCEPT_FOR_INTEGRATION`, `RETURN_FOR_REVISION`, or `REJECT`
- CKS 1.2 Discovery: `ACKNOWLEDGE_SCOPE`, `RETURN_FOR_REVISION`, or `REJECT_SCOPE`

Any acceptance must be recorded explicitly; silence is not approval.
