# CKS Bootstrap 1.0 Scope

## Goal

CKS Bootstrap 1.0 creates a minimal working foundation for storing and managing knowledge objects.

The objective is not to build the final knowledge platform, but to establish a stable source of truth.

## Included in Bootstrap 1.0

- independent repository;
- basic documentation;
- minimal knowledge object format;
- versioning rules;
- create/read/update lifecycle;
- basic validation.

## Minimal Knowledge Object

```yaml
id:
type:
title:
content:
source:
version:
status:
```

## Lifecycle

```
create
  ↓
store
  ↓
read
  ↓
update version
```

## Explicitly excluded

The following belong to later versions:

- knowledge graph;
- agent layer;
- worker manifests;
- context passports;
- complex adapters;
- autonomous promotion engines.

## Architecture rule

CKS stores validated knowledge objects.
External systems reference and exchange objects but do not become the knowledge source of truth.
