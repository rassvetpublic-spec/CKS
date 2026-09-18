# CKS Spy Worker Protocol v1.0

## 1. Overview

The **CKS Spy Worker Protocol v1.0** establishes a lightweight event detection specification (`schemas/cks_spy_worker_protocol_v1.yaml`) for monitoring repository changes, new GitHub issues, and incoming tasks **without continuous LLM invocation**.

The Spy Worker operates as an automated, non-LLM or low-cost watcher that scans event sources and emits confirmed tasks to Executor Workers.

---

## 2. Event Sources & Monitoring Mechanisms

1. **`github_api_poller`**: Lightweight REST/CLI query (`gh issue list --json ...`) on configured interval (e.g. 5–15 min).
2. **`git_repo_watcher`**: Git ref watcher tracking new commits on target branches.
3. **`webhook_receiver`**: Passive HTTP webhook endpoint receiving instant push/issue events.
4. **`filesystem_monitor`**: Local NTFS watcher tracking file system events in workspace.

---

## 3. Change Detection & Filter Rules

Matching criteria for activating an Executor Worker:
* **Unassigned Worker Task Pattern:** Body contains `## Задание для Worker` or `WORKER HANDOFF` AND `assignees == []`.
* **State Check:** Issue state == `open`.
* **Deduplication:** Event ID hashing prevents duplicate activation for already claimed tasks.

---

## 4. Handoff to Executor Worker

When a change is detected:
1. Spy Worker packages the event into `cks_event_schema_v1` payload.
2. Event is dispatched to the designated `target_worker` (e.g. `Executor_Worker`, `Documentation_Architect`).
3. Executor Worker wakes up, claims ownership (`IN_PROGRESS`), and processes the task.

---

## 5. Hard Operational Constraints

1. **No Task Execution:** Spy Worker NEVER modifies code, runs tests, or executes implementation tasks.
2. **No Knowledge Storage:** Spy Worker NEVER writes knowledge objects or decision records to CKS Canon.
3. **Zero Token Waste:** Event filtering occurs purely in code before calling LLM execution pipelines.
