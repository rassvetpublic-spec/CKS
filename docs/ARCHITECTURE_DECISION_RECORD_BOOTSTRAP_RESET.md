# ADR: Bootstrap 1.0 Reset Decision

## Status
Accepted

## Context
CKS development moved faster than the minimal bootstrap scope required. Several future platform concepts were designed before the core knowledge storage model was stabilized.

## Decision
Restore Bootstrap 1.0 as the current implementation target.

Bootstrap 1.0 includes:

- repository structure;
- minimal knowledge object;
- versioning;
- lifecycle states;
- basic read/write/update flow;
- documentation and validation.

## Deferred
The following are moved to later versions:

- Context Passport;
- Worker Manifest;
- Agent runtime;
- advanced adapters;
- knowledge graph;
- automated promotion engine;
- advanced scoring.

## Architectural Principles

KAT9I_OS remains execution layer.

CKS remains knowledge source of truth.

GitHub remains collaboration and history layer.
