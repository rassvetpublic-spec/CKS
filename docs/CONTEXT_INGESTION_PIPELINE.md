# CKS Context Ingestion Pipeline v1

## Goal

Convert large external contexts into validated CKS objects.

## Pipeline

1. Receive context package
2. Split context into candidates
3. Classify candidates
4. Validate source and evidence
5. Promote accepted objects

## Output Types

- Knowledge Object
- Decision Record
- Evidence Record
- Graveyard Item

## Principle

CKS stores validated meaning, not raw history.
