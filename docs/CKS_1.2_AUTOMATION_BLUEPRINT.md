# CKS 1.2 Automation Blueprint

Status: Discovery Draft

## Purpose

CKS 1.2 does not introduce duplicate knowledge layers. It formalizes automation and validation around existing layers:

- Knowledge
- Evidence
- Decisions
- Graveyard

## Goals

- validate lifecycle transitions;
- preserve provenance;
- prevent unverified canon changes;
- automate checks without bypassing Human Gate.

## Non-goals

- changing CORE;
- automatic approval;
- storing runtime state in knowledge.

## Target flow

Result
-> Validation
-> Evidence Check
-> Review
-> Decision candidate
-> Accepted knowledge OR Rejected history

## Required automation

1. lifecycle validation tests
2. evidence linkage checks
3. rejected history preservation checks
4. boundary checks
