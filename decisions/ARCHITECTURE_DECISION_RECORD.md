# ARCHITECTURE_DECISION_RECORD

## ADR-0001: CKS as independent knowledge system

Status: ACCEPTED

## Decision
CKS is maintained as a separate repository and independent system.

## Why CKS is a separate repository

- Knowledge lifecycle differs from execution lifecycle.
- CKS must be reusable by multiple execution systems.
- Changes to knowledge governance must not depend on runtime changes.

## Why KAT9I_OS is not a knowledge storage system

KAT9I_OS is an execution system:

- workflows;
- agents;
- runtime processes.

It consumes knowledge but does not own the long-term knowledge lifecycle.

## Why CKS has its own storage and protocols

CKS requires:

- knowledge objects;
- decisions;
- evidence;
- canon management;
- graveyard lifecycle;
- exchange protocols.

The separation prevents CKS from becoming a runtime memory dump.