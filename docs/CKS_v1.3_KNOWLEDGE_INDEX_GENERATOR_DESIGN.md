# CKS v1.3 Knowledge Index Generator

## Purpose
Automatic generation of knowledge indexes from validated metadata.

## Input
- Knowledge Objects
- Document metadata
- Relations registry

## Output
- INDEX.md
- machine-readable index
- relation map

## Flow

Objects
↓
Metadata validation
↓
Relations resolution
↓
Index generation

## Rules
- only validated objects are indexed;
- deprecated objects remain visible with status;
- relations are not inferred without evidence.
