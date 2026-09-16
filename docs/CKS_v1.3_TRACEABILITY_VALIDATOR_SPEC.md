# CKS v1.3 Traceability Validator Specification

## Purpose

Validate the chain:

GAP -> Evidence -> Proposal -> Decision -> Review Gate -> Change -> History

## Required checks

- Every Change requires Decision.
- Every Decision requires Evidence.
- Every Canon entry requires Owner, Evidence, Decision, History.
- Relations must use registered relation types.

## Result

PASS or FAIL with machine-readable findings.
