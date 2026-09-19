# CHAT_ORIGIN_DATASET_PROTOCOL_v1

## Status

PROVISIONAL / RESEARCH

Not Canon.

## Purpose

Define a protocol for treating a long AI research conversation as an origin dataset for studying knowledge evolution, rule influence, and research process behavior.

## Core Hypothesis

A long research chat is not only a communication log.

It can become part of the experimental environment and influence the result of later validation.

Therefore:

```
Historical Record

↓

Bootstrap Snapshot

↓

Clean Experiment Environment

↓

Replay
```

## Problem

A research conversation contains hidden variables:

- order of ideas;
- previous decisions;
- corrections of mistakes;
- accumulated context;
- branching history;
- terminology evolution.

If these variables are not separated, an experiment may validate the context instead of the tested rules.

## Chat as Dataset

The dataset unit is not only a message.

Primary unit:

```
message

↓

idea event

↓

branch

↓

hypothesis

↓

validation

↓

decision
```

## Required Layers

### Historical Layer

Preserves the original evolution path.

### Bootstrap Layer

Creates a reproducible recovery package:

- goal;
- checkpoint;
- known hypotheses;
- unknowns;
- next action.

### Experiment Layer

Provides clean conditions for replay.

## A/B/C Validation Model

A:

Old rules + full historical context

B:

New rules + full historical context

C:

New rules + clean bootstrap context

## Metrics

Compare:

- idea preservation;
- trajectory stability;
- rule influence;
- context influence;
- noise resistance.

## Constraints

This protocol does not claim that chat datasets are universally superior.

It defines a method for studying the influence of context on research systems.
