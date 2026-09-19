# KAT9I_OS Adapter (v1.0)

## Purpose

Bridge between KAT9I_OS execution layer and CKS knowledge layer without responsibility bleed.

## Detailed Contract Specification

See canonical contract document: [docs/CKS_KAT9I_OS_ADAPTER_CONTRACT_v1.md](file:///c:/GIT/CKS/docs/CKS_KAT9I_OS_ADAPTER_CONTRACT_v1.md)

## Rules

- KAT9I_OS owns runtime, workers and workflows.
- CKS owns validated knowledge, decisions and evidence.
- Adapter transfers structured artifacts only.
- Raw runtime memory and process telemetry are not imported into CKS.

## Flow

KAT9I_OS -> Adapter -> CKS -> Validated Knowledge

