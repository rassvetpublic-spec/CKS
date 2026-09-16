# CHAT_CONTEXT_EXPORT_001

## Purpose

Migration record of the CKS architecture discussion before chat deletion.

This document preserves decisions, not raw conversation.

## Origin

CKS was created as an independent research project for context, knowledge and decision lifecycle management.

## Core decisions

### CKS independence

CKS is a separate project.

CKS is not SSOT for KAT9I_OS.

### KAT9I_OS boundary

KAT9I_OS remains an execution system:

- runtime;
- workflows;
- workers;
- operational processes.

CKS remains a knowledge and decision system.

### Donor principle

External projects may provide ideas and research patterns, but cannot directly modify another system's canon.

Flow:

idea -> research -> audit -> ABC/XYZ -> decision -> possible adoption

## Preserved architecture topics

- Context Split Modes
- Knowledge Objects
- Decision System
- Evidence Layer
- Decision Graveyard
- Canon Registry
- Storage separation
- Protocol contracts

## Deletion safety

After storing this migration artifact, future work can continue from GitHub without requiring the original chat history.
