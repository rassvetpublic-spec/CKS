# CKS 1.2 Decision Memory Requirements

Status: discovery draft

## Goal

Remember decisions without turning all history into active knowledge.

## Required record

A decision memory object should contain:

- proposal reference
- decision status
- evidence references
- rationale
- rejected alternatives when applicable
- revisit conditions

## Forbidden fields

Do not include:

- Owner as knowledge metadata
- execution status
- runtime state
- approval chains as knowledge content

## Acceptance path

Proposal -> Review -> Evidence -> Decision -> Human Gate -> Accepted Memory

Rejected decisions remain historical records, not active knowledge.
