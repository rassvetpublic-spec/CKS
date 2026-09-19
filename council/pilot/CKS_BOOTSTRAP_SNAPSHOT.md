# CKS Bootstrap Snapshot

## Purpose

Стартовый пакет для продолжения работы CKS после закрытия текущего чата.

## Repository

- Repository: `rassvetpublic-spec/CKS`
- Branch: `council-v0.1`
- Current focus: CKS 1.2 Discovery → preparation for Human Gate

## Canonical operating rules

- CORE не изменять без отдельного процесса.
- Discovery не считать Canon.
- Evidence обязателен для принятия решений.
- PASS проверки агента не равен APPROVE владельца.
- Runtime и исполнение не хранить в Knowledge.
- Историю отказов сохранять.

## Completed CKS 1.2 work

Completed artifacts:

- Architecture audit.
- Confirmation that new base layers are not required.
- Semantic Validation direction.
- Decision Validator specification.
- Evidence Trace Validator specification.
- Graveyard Lifecycle Validator specification.
- Validation Coverage Matrix.
- Gap Report.
- Gap to Validation Mapping.
- Implementation Proposal.
- Implementation Checklist.
- Execution Roadmap.

## Current architecture model

```
Knowledge
    |
Evidence
    |
Decisions ---- Review
    |
Graveyard
    |
Automation / Validation
```

## Current state

Status:

`Discovery complete enough for final audit preparation`

Not completed:

- final self review;
- validation contract finalization;
- Human Gate package;
- implementation of validators.

## Next session startup procedure

1. Read:
   - `CKS Bootstrap Context`.
   - `CKS_1.2_EXECUTION_ROADMAP.md`.
   - this snapshot.
2. Verify current Git SHA and branch.
3. Run final audit freeze.
4. Prepare Human Gate package.

## Forbidden actions

Do not:

- create duplicate architecture layers;
- modify CORE automatically;
- promote Discovery documents to Canon;
- replace evidence with chat memory.
