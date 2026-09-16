# CKS Architecture Guard

## Purpose

Защита границ CKS v1.2.

## Frozen Core Rules

```yaml
core:
  status: frozen

rules:
  no_core_expansion_without_gap: true
  no_proposal_as_decision: true
  no_experiment_as_canon: true
```

## Forbidden automatic changes

Запрещено без отдельного Decision:

- добавление новых обязательных Core слоёв;
- перенос экспериментальных моделей в канон;
- изменение границы CKS / KAT9I_OS;
- превращение исследования в архитектурный стандарт.

## Allowed evolution

Только через:

```text
GAP → Evidence → Proposal → Decision
```
