# CKS v1.3 Architecture Contract

Status: Proposal
Type: Architecture Rule

## Layers

- Core: stable canonical rules
- Knowledge: knowledge objects, clusters, tags, metrics
- Evidence: proofs and sources
- Decisions: accepted decisions and rationale
- Research: exploration only
- Automation: validation and reporting only

## Forbidden transitions

Research -> Core
Proposal -> Canon without Decision
Automation -> Decision

## Required lifecycle

GAP -> Evidence -> Proposal -> Decision -> Change -> History
