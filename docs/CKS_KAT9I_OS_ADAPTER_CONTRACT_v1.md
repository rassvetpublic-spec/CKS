# CKS <-> KAT9I_OS Execution Adapter Contract v1.0

## 1. Overview & Purpose

This contract defines the formal interface boundary between **KAT9I_OS** (the execution, subagent orchestration, and runtime environment) and **CKS** (Canonical Knowledge System, responsible for validated knowledge, decision records, and audit evidence).

The objective is to enable seamless artifact exchange while maintaining strict separation of concerns without responsibility bleed.

---

## 2. Separation of Responsibility

| Dimension | KAT9I_OS (Execution Layer) | CKS (Knowledge Layer) |
| :--- | :--- | :--- |
| **Primary Focus** | Workflow execution, subagent pool, telemetry DBs, CLI/IDE profiles | Validated knowledge, decision records, evidence, auditability |
| **State Nature** | Ephemeral, dynamic, process-bound | Immutable, audited, provenance-tracked |
| **Ownership** | Owns runtime execution & task completion | Owns Canon state & verified knowledge objects |
| **Storage Boundary** | Local state (`.kat9i`), active task locks | Repository knowledge structures (`schemas/`, `docs/`, `records/`) |

---

## 3. Boundary Rules & Constraints

1. **Zero Execution Leak:** CKS does NOT store runtime execution details, subagent thread states, or raw process logs from KAT9I_OS.
2. **Zero Direct Canon Mutation:** KAT9I_OS cannot directly mutate CKS Canon files. All knowledge ingestion must pass through normalized adapter artifacts and validation gates.
3. **Artifact-Based Exchange:** All data transfers between KAT9I_OS and CKS must be formatted as structured, self-contained artifacts with full provenance.
4. **Fail-Closed Rejection:** Any artifact containing unvalidated runtime memory, raw telemetry, or missing provenance metadata is rejected by the adapter.

---

## 4. Artifact Mapping Rules

| KAT9I_OS Source Artifact | CKS Target Object | Required Provenance Metadata | Validation Rule |
| :--- | :--- | :--- | :--- |
| `context_package` | `candidate_object` | `source_execution_id`, `timestamp` | Must conform to `schemas/context_package_kat9i_v1.yaml` |
| `decision_artifact` | `decision_record` | `decision_id`, `sha_hash`, `author` | Must reference exact SHA boundary |
| `evidence_artifact` | `evidence_record` | `test_run_id`, `ci_gate_link`, `sha` | Must include verifiable verification output |

---

## 5. Lifecycle Flow

```
[ KAT9I_OS Runtime ]
        │ (Emits Execution Artifact)
        ▼
[ Adapter Ingestion ]
        │ (Schema Validation & Provenance Check)
        ▼
[ CKS Normalization ]
        │ (Convert to Candidate / Decision Record)
        ▼
[ CKS Decision Gate ]
        │ (Verification & Evidence Audit)
        ▼
[ CKS Canon / History ]
```

---

## 6. Verification & Compliance

* **Automated Validation:** The adapter contract is backed by schema validators (`schemas/context_package_kat9i_v1.yaml`) and mapping rules (`adapters/kat9i_mapping_rules.yaml`).
* **Audit Trail:** Every imported object preserves `source_system: KAT9I_OS` and `execution_id` to guarantee traceability.
