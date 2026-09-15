# CKS Integration Test Report v1

## Scenarios

- valid KAT9I_OS context package import
- raw context rejection

## Expected results

PASS:
- validated context package accepted
- artifacts created only after validation

FAIL:
- raw memory dumps rejected
- unverified context not promoted

## Architecture check

KAT9I_OS remains execution system.
CKS remains knowledge and decision system.
