# RULE_REPLAY_AB_C_PROTOCOL_v1

## Status

PROVISIONAL / RESEARCH

Not Canon.

## Purpose

Define a reproducible A/B/C experiment for measuring rule influence separately from historical-context influence.

## Hypotheses

### H-CONTEXT-001

Historical conversational context can influence rule-validation outcomes.

### H-MODE-001

Explicit Discovery / Validation / Synthesis modes may improve separation between exploration and verification.

## Experimental Arms

### A — Baseline Context

Old rules + full historical context.

### B — Rule Change

New rules + the same full historical context.

### C — Context Isolation

New rules + clean bootstrap context from CKS_BOOTSTRAP_SNAPSHOT_RULE_REPLAY_v1.

## Independence Rule

Discovery data MUST NOT be reused as the sole Evaluation dataset.

The evaluation task set must be frozen before scoring.

## Frozen Inputs Required Before Run

- old_rules_ref;
- new_rules_ref;
- historical_context_ref;
- clean_bootstrap_ref;
- evaluation_dataset_ref;
- task_order;
- model/runtime configuration;
- metric definitions.

If any required input is UNKNOWN, execution status remains BLOCKED.

## Metrics

Metrics must be computed by one documented method across A/B/C.

Required dimensions:

1. Idea preservation.
2. Trajectory stability.
3. Rule influence.
4. Context influence.
5. Noise resistance.

Optional operational dimensions:

- false blocking;
- critical-error detection;
- rule-growth overhead;
- completion cost.

## Comparisons

### Rule Effect

B - A

Measures change associated with new rules while historical context is held constant.

### Context Effect

C - B

Measures change associated with replacing historical context with clean bootstrap while new rules are held constant.

### Combined Difference

C - A

Descriptive only. Must not be attributed to a single cause.

## Anti-Contamination Controls

- no hidden historical chat in C;
- no assistant memory as evaluation evidence;
- identical task order unless task-order randomization is explicitly part of the protocol;
- identical scoring method across arms;
- record all deviations.

## Result Classification

Each result must be classified as one of:

FACT / CALC / ESTIMATE / UNKNOWN / HYPOTHESIS.

No UNKNOWN may be converted to zero.

## Critical Error Gate

If input drift, SSOT break, scoring inconsistency, or context leakage is detected:

1. stop the affected run;
2. preserve evidence;
3. record the defect;
4. version the fix;
5. restart only the affected stage.

## Acceptance Conditions

The experiment can move from PROVISIONAL to VALIDATED only when:

- all frozen input refs are preserved;
- A/B/C runs are reproducible;
- metrics are calculated using the same method;
- context leakage check passes;
- results and limitations are stored as evidence;
- independent review confirms the comparison.

## Current Execution State

BLOCKED pending frozen experiment inputs and persisted evaluation dataset.

This protocol defines the experiment; it does not claim an experimental result.
