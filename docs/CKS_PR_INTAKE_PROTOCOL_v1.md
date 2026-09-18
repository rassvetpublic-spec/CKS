# CKS PR Intake Protocol v1

## Purpose

Define the handling path for pull requests that are created without a linked Issue.

PR-first work must enter the same lifecycle as Issue-first work.

## Flows

### Issue-first

Issue → HANDOFF → Worker → PR → Decision → Merge

### PR-first

PR → PR Intake → linked Issue → HANDOFF → Worker → Decision → Merge

## PR without Issue

When a PR has no source Issue:

1. Create PR Intake Issue.
2. Link PR and Issue.
3. Add HANDOFF metadata.
4. Classify the task.
5. Continue through normal review lifecycle.

## PR Intake Template

```md
# PR Intake

SOURCE:
Pull Request #

REPOSITORY:
https://github.com/rassvetpublic-spec/CKS

TYPE:
PR-first

PURPOSE:
-

CLASSIFICATION:

ABC:
-

XYZ:
-

COMPLEXITY:
-

RISK:
-

CHANNEL:
GitHub Issue conversation

REPORT FORMAT:
STATUS:
EVIDENCE:
BLOCKERS:
NEXT:
```

## Metrics

Required:

- complexity
- risk
- ABC/XYZ
- evidence coverage
- traceability
- protocol compliance

## Model Policy

Model selection remains optional.

Any Worker may take any task.

Future Model Recommendation is a separate v2 capability.
