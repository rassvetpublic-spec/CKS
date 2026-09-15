# CKS Bootstrap 1.0 Storage Model

## Goal

Provide minimal storage lifecycle for Knowledge Objects.

## Storage layout

```
knowledge/
 └── objects/
      └── <id>.yaml
```

## Supported operations

- create object
- read object
- update version
- archive object

## Bootstrap rule

Storage contains knowledge objects only.
Raw context, agent memory and execution state are not stored here.
