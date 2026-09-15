# Task Dispatch Protocol

## Purpose

Define how agents receive work from CKS.

Flow:

CKS -> task artifact -> Agent -> result artifact -> CKS

Rules:

- task must have objective
- task must define expected artifacts
- agent does not create canon directly
- execution state remains outside CKS
