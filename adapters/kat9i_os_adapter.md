# KAT9I_OS Adapter

## Purpose

Bridge between KAT9I_OS execution layer and CKS knowledge layer.

## Rules

- KAT9I_OS owns runtime, workers and workflows.
- CKS owns validated knowledge, decisions and evidence.
- Adapter transfers structured artifacts only.
- Raw runtime memory is not imported.

## Flow

KAT9I_OS -> Adapter -> CKS -> Validated Knowledge
