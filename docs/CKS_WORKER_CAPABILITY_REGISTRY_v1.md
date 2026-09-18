# CKS Worker Capability Registry v1.0

## 1. Overview

The **CKS Worker Capability Registry v1.0** defines a model-agnostic contract specification (`schemas/cks_worker_capability_registry_v1.yaml`) for Worker roles operating across CKS and KAT9I_OS execution layers.

This registry decouples agent roles and task capabilities from specific LLM models (e.g. Claude, Gemini, GPT), ensuring pure contract-driven task assignment.

---

## 2. Capability Contract Structure

Each Worker role definition requires:
1. **`role_name`**: Formal role identifier (`Implementation_Worker`, `Documentation_Architect`, `Harvester_Worker`, `QA_Controller`, `Spy_Worker`, `Executor_Worker`).
2. **`task_types`**: Supported operation classes (`code_mutation`, `schema_design`, `knowledge_harvesting`, `evidence_audit`).
3. **`input_requirements`**: Required inputs, context scopes, or trigger events.
4. **`expected_output`**: Defined deliverables (`PR`, `WORKER_REPORT`, `evidence_record`).
5. **`constraints`**: Hard operational boundaries (e.g. "Do not mutate Canon directly", "Do not choose specific model").

---

## 3. Standard Worker Role Capabilities

| Role Name | Supported Task Types | Input Requirements | Expected Deliverables | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| **`Implementation_Worker`** | `code_refactor`, `bug_fix`, `feature_dev` | Validated Issue, Scope definition | PR, SHA reference, Test evidence | Must pass 100% CI tests |
| **`Documentation_Architect`** | `schema_design`, `protocol_specification` | Issue specs, Architecture guidelines | `schemas/*.yaml`, `docs/*.md` | No direct Canon promotion |
| **`Harvester_Worker`** | `knowledge_discovery`, `orphan_rescue` | Repo history, Unstructured issues | Candidate Objects, Knowledge Index | Read-only analysis |
| **`QA_Controller`** | `evidence_verification`, `verdict_issuance` | PR SHA, Test reports, Evidence record | Verdict Record, Merge Recommendation | Independent review |

---

## 4. Model Agnosticism Guarantee

* Roles specify **required capabilities and constraints only**.
* Model routing and execution assignment are handled externally by the execution environment (KAT9I_OS / Router Policy) based on complexity and cost metrics.
