# SUNO/KAT9I Recon — Auxiliary Reconciliation: LUNA assets + VANDAL provenance

Status: **DATA / FORENSICS ONLY — NON-CANONICAL**  
Date: 2026-09-17  
Parent stream: CKS #31  
Scoped stream: CKS #35

## Why this auxiliary artifact exists

During bounded child passes, CKS `main` advanced concurrently with another SUNO/KAT9I reconstruction worker. The current main now contains a global numbered ledger through `R059`, including:

- `SUNO_KAT9I_RECON_CHECKPOINT_006_R048_R054_2026-09-17.md`
- `SUNO_KAT9I_RECON_CHECKPOINT_007_R055_R059_2026-09-17.md`

Therefore child-branch finding IDs that reused `R038–R052` would collide with the already-materialized global ledger.

**Correction:** this artifact uses `AUX-*` IDs only. Global `R###` numbers are owned by the parent #31 ledger and must be assigned only during controlled reconciliation into that ledger.

This file preserves only evidence that is useful and not safely represented by a new global R number yet.

## SSoT rule

- current CKS `main` research ledger = durable parent evidence stream;
- #31 = parent work state;
- #35 = scoped agent-body/library work item;
- this file = auxiliary Evidence, not Canon and not a second numbered ledger;
- AndreysSUNOBOT remains the music-agent/music-engine canon lane;
- donor repositories remain Evidence sources only.

No ABC/XYZ, Genome or Canon promotion is performed here.

---

## AUX-LUNA-001 — LUNA assets path is bounded in reachable historical main-line history

Historical repository: `NewDeep67/KAT9I_IIIJIIOXA`.

Target path:

`skills-catalog/creative/luna-researcher/assets/`

Path-scoped commit history returns two reachable main-line events:

1. `4f939c17b43ee978547bd644872dcea701dba0a9` — bulk skills-catalog import;
2. `d23d8f576da383b3a747de5ad9014fa0a8316a67` — cleanup deleting remaining Engine/runtime/product artifacts from the Knowledge repository.

Exact directory listing was checked at:

- initial import `4f939c17...`;
- final pre-delete parent `57ec9595a5153d33a5bf5a7021e5cf811ca92d9a`;
- later inspected ref `073c497e1bdb64e8341990204d7587a980cc55e0`.

All inspected states expose only:

`assets/README.md`

with blob:

`af298b70ff2139610c441e3ca5c62cf00c23051e`.

The README declares an intended asset boundary for research-card templates, search-query presets and LUNA databases, but concrete payload files are not recovered under this path in the inspected reachable lineage.

### Regression correction

Previously cached concrete filenames such as:

- `microdosing_examples.md`
- `vocal_tag_blocks.md`

must **not** be treated as historical Git facts for this lineage. They require another exact ref/blob before reuse.

Status: `SCOPED_NEGATIVE_EVIDENCE + LIBRARY_BOUNDARY_CONFIRMED`.

---

## AUX-LUNA-002 — Recovered LUNA libraries/contracts live outside `assets/`

At historical ref `073c497...`, concrete recovered LUNA dependencies include:

- `references/search_queries_and_sources.md`
- `scripts/format_luna_dossier.py`

The reference file provides source classes and query patterns for production, BPM/key/credits, vocal-chain analysis, microgenres, trends and URL deconstruction.

The formatter provides a structured dossier contract covering sound profile, vocal profile, tangible items/slang, microdosing fields, role-specific directives and source evidence.

Important scope guard: demo values inside the formatter are fixtures/examples, not universal music rules.

Status: `PHYSICALLY_RECOVERED` for these two dependencies.

---

## AUX-VANDAL-001 — VANDAL role is confirmed; standalone body is still unrecovered in inspected slice

Positive evidence:

- historical `suigetsu-engine` names VANDAL among the ten production roles;
- historical LUNA body includes VANDAL in downstream team directives;
- LUNA formatter has a dedicated `vandal` directive field.

Scoped negative evidence:

- no VANDAL-named path was recovered in the inspected mature-import tree `4f939c17...`;
- no exact VANDAL registry entry was recovered in the inspected `skills_registry.json@073c497...` slice.

Safe conclusion:

> VANDAL existed as a historically routed role, but a standalone VANDAL body remains unrecovered in the inspected tree/registry slice.

This is not proof that a body never existed.

Status: role `CONFIRMED`; standalone body `UNKNOWN`.

---

## AUX-VANDAL-002 — Do not duplicate global R057

Current CKS main already records global finding `R057`:

- `idea-generator/SKILL.md` materially implements concept/hook/viral functions;
- it explicitly points to historical source `09_ДВИЖОК_ИДЕЙ.txt`;
- it is a strong VANDAL function-equivalent/shared predecessor candidate;
- it is **not** proof of a standalone VANDAL body and does not prove source 11.

The child pass independently reached the same functional-overlap conclusion. That result is therefore **DUPLICATE_OF_GLOBAL_R057**, not a new R finding.

Do not create another global finding for the same fact.

---

## Concurrency correction for future bounded passes

Because multiple workers are writing CKS research concurrently:

1. every pass must fetch fresh `main` before search;
2. immediately before persistence, fetch `main` again;
3. inspect any new SUNO/KAT9I checkpoint added during the pass;
4. child work uses temporary `AUX-*` IDs unless the next global R number is reserved from the current parent ledger;
5. duplicate conclusions are marked `DUPLICATE_OF_GLOBAL_R###` rather than renumbered;
6. new evidence should be appended to the parent ledger only after provenance/dedup reconciliation.

This prevents parallel workers from producing competing R-number namespaces.

## Disposition of superseded child PRs

Earlier child PRs #40 and #50 were created before the concurrent global ledger advance was detected. Their evidence remains historically useful, but their local R-number namespaces are unsafe for merge as written.

They should be treated as **SUPERSEDED BY THIS RECONCILIATION** and not merged in their current form.

A separate un-PR'd child branch for VANDAL provenance is likewise not authoritative and should not be merged without dedup against global R057.

## Resume point

The parent global ledger currently states `next finding after R059 = R060` and names NEO as the first resume target.

Before any new child pass:

`fresh main → read latest global checkpoint → dedup → one narrow target → auxiliary checkpoint if number ownership is uncertain`.

Recommended next bounded target: **NEO only**, but only after confirming that another concurrent worker has not already materialized R060+.