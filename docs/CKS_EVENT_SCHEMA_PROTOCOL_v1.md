# CKS Event Schema Protocol v1.0

## 1. Overview

The **CKS Event Schema Protocol v1.0** establishes a unified, standardized event payload specification (`schemas/cks_event_schema_v1.yaml`) for triggering Workers autonomously.

This protocol enables event-driven activation (via Webhooks, File Watchers, or System Triggers) to replace expensive, continuous LLM polling loops while maintaining deterministic tracking.

---

## 2. Core Event Fields

1. **`source`**: The origin system emitting the event (`github_webhook`, `filesystem_watcher`, `cron_trigger`, `worker_handoff`, `system_alert`).
2. **`event_type`**: The category of event (`issue_created`, `issue_updated`, `pr_opened`, `commit_pushed`, `schedule_tick`, `worker_ready`).
3. **`priority`**: Urgency classification (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).
4. **`target_worker`**: Designated target Worker role or lane (e.g. `Worker A`, `Worker B`, `Harvester`, `QA_Controller`).
5. **`event_evidence`**: Verifiable event payload containing `repository`, `resource_id`, `resource_url`, `payload_sha`, and `timestamp`.

---

## 3. Boundary & Non-Goal Principles

* **No Execution Logic in CKS:** CKS specifies event definitions and schema validation. Runtime execution and dispatching are managed by the execution layer (KAT9I_OS).
* **No Direct Canon Mutation:** Events are transient trigger signals and do not modify CKS Canon files directly.
* **Deterministic Activation:** Workers process only confirmed, schema-compliant events.

---

## 4. Lifecycle Flow

```
[ GitHub / Watcher / System Event ]
                 │
                 ▼
     [ Event Emission (JSON/YAML) ]
                 │
                 ▼
[ Schema Validation (cks_event_schema_v1) ]
                 │
                 ▼
   [ Dispatch to Target Worker ]
```
