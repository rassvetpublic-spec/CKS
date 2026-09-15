# Generic Agent Adapter v1

## Role

Adapter converts external agent messages into CKS exchange objects.

## Boundary

```
External Agent
      |
      v
Adapter
      |
      v
CKS
```

## Forbidden

- raw memory import
- hidden agent state import
- unverified canon changes
