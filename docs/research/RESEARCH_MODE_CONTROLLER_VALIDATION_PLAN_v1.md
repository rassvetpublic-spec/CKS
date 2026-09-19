# RESEARCH_MODE_CONTROLLER_VALIDATION_PLAN_v1

## Status

PROVISIONAL / VALIDATION PLAN

Not Canon.

## Purpose

Define how H-MODE-001 can be tested without using the same discovery material as the sole evaluation dataset.

## Hypothesis Under Test

H-MODE-001:

Explicit separation of Discovery, Validation, and Synthesis modes improves methodological separation between exploration and verification.

## Dependencies

- docs/research/RESEARCH_MODE_CONTROLLER_v1.md
- Issue #380
- Issue #382
- docs/research/CKS_BOOTSTRAP_SNAPSHOT_RULE_REPLAY_v1.md
- docs/research/RULE_REPLAY_AB_C_PROTOCOL_v1.md
- AGENTS.md

## Evaluation Design

Use a frozen evaluation task set that was not used to create H-MODE-001.

Compare:

1. Control workflow — one undifferentiated research mode.
2. Mode-separated workflow — Discovery -> Validation -> Synthesis with explicit transition gates.

## Required Frozen Inputs

- evaluation_dataset_ref;
- task_set_ref;
- control_rules_ref;
- mode_rules_ref;
- runtime/model configuration;
- scoring procedure;
- task order.

Execution remains BLOCKED while any required input is UNKNOWN.

## Transition Gates

### Discovery -> Validation

Required:

- hypothesis explicitly stated;
- discovery evidence separated from evaluation dataset;
- unknowns recorded;
- evaluation criteria frozen.

### Validation -> Synthesis

Required:

- validation evidence persisted;
- metric calculation complete;
- critical errors resolved or explicitly BLOCKED;
- rejected hypotheses preserved.

### Synthesis -> Decision Candidate

Required:

- only validated results are promoted into synthesis claims;
- limitations are preserved;
- conflicting evidence is recorded;
- no Canon change occurs automatically.

## Metrics

Use the same calculation method for control and mode-separated runs.

Required dimensions:

1. hypothesis preservation;
2. evidence traceability;
3. false blocking;
4. validation leakage;
5. critical-error detection;
6. unsupported-claim count;
7. completion cost.

## Failure Conditions

H-MODE-001 is not supported if mode separation:

- does not improve methodological separation;
- materially increases false blocking without compensating validation benefit;
- introduces uncontrolled transition ambiguity;
- cannot be reproduced on an independent evaluation dataset.

## Boundary Review

The controller is a research operating model, not an execution owner.

It must not:

- replace CKS architecture;
- promote Canon automatically;
- treat automation as Decision;
- treat Synthesis as Evidence.

## Current State

BLOCKED pending independent frozen evaluation inputs and execution results.

This file defines validation criteria only. It does not claim H-MODE-001 is validated.
