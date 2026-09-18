# Research Mode Controller v1

## Type

Research Operating Model Hypothesis

## Status

PROVISIONAL

## Context

During BENCH-001 and RULE REPLAY validation it was identified that one universal rule set creates a conflict between exploration and verification.

Discovery requires branching and hypothesis generation.
Validation requires constraints, metrics and evidence.

## Hypothesis H-MODE-001

Research systems require explicit operating modes:

1. Discovery Mode
2. Validation Mode
3. Synthesis Mode

## Model

```text
GOAL
 |
MODE SELECTOR
 |
+----------------+
|                |
DISCOVERY   VALIDATION
 |                |
 +-------+--------+
         |
    SYNTHESIS
```

## Discovery Mode

Purpose:

Finding new hypotheses.

Allows:

- branching;
- exploration;
- unexpected ideas.

## Validation Mode

Purpose:

Checking hypotheses.

Requires:

- frozen dataset;
- defined metrics;
- evidence;
- comparison.

## Synthesis Mode

Purpose:

Combining validated results into a model or decision.

## Relation to BENCH-001

Extended model:

```text
Dataset
  ↓
Representation
  ↓
Mode
  ↓
Method
  ↓
Metrics
```

## Constraints

This artifact:

- is not Canon;
- does not replace CKS architecture;
- requires experimental validation.

## Related Research

- RULE REPLAY v1
- BENCH-001 Factor Model
- Exploration-Control Dynamic Research Model
