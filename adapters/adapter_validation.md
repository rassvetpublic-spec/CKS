# Adapter Validation v1

Purpose: validate boundaries between KAT9I_OS and CKS.

Checks:

- source mapping exists
- artifact type is valid
- evidence requirements are preserved
- raw memory is rejected
- canon updates require decision records

Flow:

KAT9I_OS artifact -> Adapter -> Validation -> CKS object
