# CKS Evidence Schema Protocol v1.0

## 1. Overview

The **CKS Evidence Schema Protocol v1.0** defines a structured format (`schemas/cks_evidence_schema_v1.yaml`) for recording empirical proof of actions executed by Workers.

Evidence artifacts serve as audit trails for automated CI gates, QA controllers, and human reviewers.

---

## 2. Evidence Structure Requirements

1. **`action`**: Clear description of the operation executed.
2. **`inputs`**: Context parameters, task definitions, or source files provided.
3. **`output`**: Summary of deliverables produced.
4. **`affected_files`**: List of added (`NEW`), edited (`MODIFY`), or removed (`DELETE`) repository files.
5. **`changes_summary`**: Concise narrative explaining rationale and scope.
6. **`verifications`**: Automated command outputs (e.g. `pytest`, `mypy`, `git diff`) and outcome status (`PASS`/`FAIL`).
7. **`confidence_level`**: Self-assessed execution confidence level (`HIGH`/`MEDIUM`/`LOW`).

---

## 3. Boundary & Authority Rule

* **Evidence is Not Decision Authority:** Evidence records provide verifiable proof of execution. They do NOT replace or override canonical CKS Decision Records or Frozen Core rules.
* **Traceability:** Every evidence object must link to an exact SHA commit boundary and task identifier.

---

## 4. Lifecycle Integration

```
[ Worker Action Execution ]
           │
           ▼
[ Verification Test Suite ]
           │
           ▼
[ Generate Evidence Record (cks_evidence_schema_v1) ]
           │
           ▼
[ Submit to QA / Review Controller Gate ]
```
