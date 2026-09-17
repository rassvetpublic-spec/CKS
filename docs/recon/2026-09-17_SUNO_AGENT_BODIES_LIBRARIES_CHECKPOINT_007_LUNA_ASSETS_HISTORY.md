# SUNO/KAT9I Recon — Checkpoint 007: LUNA assets history

Status: **DATA / FORENSICS ONLY — NON-CANONICAL**  
Date: 2026-09-17  
Parent research stream: CKS #31  
Scoped work item: CKS #35

## SSoT boundary

This artifact is research Evidence only. It does not change CKS Canon or AndreysSUNOBOT music-agent Canon. ABC/XYZ and Genome value remain `UNASSESSED`.

## Freshness anchor

CKS base for this pass:

`1234d5d86e40b4b18a184d5f2d111f2183889e00`

Historical repository:

`NewDeep67/KAT9I_IIIJIIOXA`

Target path only:

`skills-catalog/creative/luna-researcher/assets/`

This pass is intentionally limited to the history of that one path.

## PREV-VERIFY

Checkpoint 006 conclusions were regression-checked before continuing.

Still valid:

- LUNA v3.5 is historically confirmed as a substantive standalone body.
- LUNA has a concrete query/source reference library and an executable dossier formatter.
- the inspected `assets/` directory at `073c497...` exposes only `README.md`.
- concrete cached filenames such as `microdosing_examples.md` and `vocal_tag_blocks.md` are not supported at that ref.
- demo content in `format_luna_dossier.py` is example data, not universal rules.

No prior finding is promoted.

---

## R044 — Reachable path history has only import and deletion events

**Object type:** `LIBRARY / PATH_HISTORY`  
**Evidence class:** HISTORICAL-CONFIRMED

Git commit history scoped to:

`skills-catalog/creative/luna-researcher/assets`

returns two reachable default-lineage events:

1. `4f939c17b43ee978547bd644872dcea701dba0a9` — bulk skills-catalog import;
2. `d23d8f576da383b3a747de5ad9014fa0a8316a67` — cleanup deleting remaining Engine/runtime/product artifacts from the Knowledge repository.

This creates a bounded lifecycle for the path in the inspected main-line history:

`bulk import → retained through pre-cleanup state → deleted by Knowledge cleanup`.

It does **not** prove that no older local/off-branch copy ever existed.

---

## R045 — At both import and final pre-delete state, the assets directory contains only README.md

**Object type:** `LIBRARY / NEGATIVE_EVIDENCE`  
**Evidence class:** HISTORICAL-CONFIRMED

Exact directory listings were checked at:

- import commit `4f939c17b43ee978547bd644872dcea701dba0a9`;
- parent immediately before cleanup `57ec9595a5153d33a5bf5a7021e5cf811ca92d9a`.

Both expose exactly one file:

`skills-catalog/creative/luna-researcher/assets/README.md`

with the same blob SHA:

`af298b70ff2139610c441e3ca5c62cf00c23051e`.

Therefore, in the inspected reachable default-lineage, there is no Evidence that concrete asset payload files were ever committed under this path.

This materially strengthens the Checkpoint 006 correction: cached concrete asset filenames must not be treated as historical Git facts.

**Preservation status:** `UNKNOWN` for the intended payload; the README metadata itself was historically preserved until cleanup.

---

## R046 — README confirms intended library classes, not actual recovered payload

**Object type:** `LIBRARY / REGISTRY_INTENT`  
**Evidence:** `assets/README.md`, blob `af298b70...`  
**Evidence class:** HISTORICAL-CONFIRMED

The README states that the LUNA assets area is for:

- research-card templates;
- search-query presets;
- databases for LUNA.

This is valuable because it confirms an intended internal library boundary.

But the correct inference is:

`declared library classes != recovered library payload`.

The query/source library that *is* recovered lives separately under `references/`, and the executable output formatter lives under `scripts/`.

---

## R047 — Cleanup commit explains disappearance of the whole path, not existence of missing files

**Object type:** `HISTORICAL_EVENT`  
**Evidence:** commit `d23d8f576da383b3a747de5ad9014fa0a8316a67`  
**Evidence class:** HISTORICAL-CONFIRMED

The cleanup commit explicitly removes Engine/runtime/product artifacts from the Knowledge repository while preserving the Knowledge side by whitelist.

This explains why the LUNA skill/runtime subtree disappears from the later Knowledge repository state.

It must **not** be used to infer that specific undeclared asset files existed before deletion. Exact pre-delete listing still shows only README under `assets/`.

---

## Regression result for Checkpoint 007

### Confirmed

- Checkpoint 006's correction was right: current exact Evidence does not support named concrete LUNA asset files beyond README in the inspected Git lineage.
- LUNA nevertheless has real reusable libraries/contracts elsewhere: `references/search_queries_and_sources.md` and `scripts/format_luna_dossier.py`.
- the repository cleanup is a real provenance boundary and should be considered when searching removed agent bodies.

### Rejected

- `microdosing_examples.md` as a confirmed historical file under this assets path — REJECTED for inspected reachable history.
- `vocal_tag_blocks.md` as a confirmed historical file under this assets path — REJECTED for inspected reachable history.

### Not proven / remains open

- whether these or equivalent payloads existed in pre-Git local directories;
- whether they existed on another branch/ref not represented by the inspected path history;
- whether import tooling intentionally created placeholder asset READMEs while omitting local data.

## Search-budget decision

Do not spend additional context repeatedly scanning the same reachable main-line `assets/` path. That path has now been bounded by import/pre-delete/deletion Evidence.

Further recovery of LUNA library payload should move to one of:

- older/off-branch refs;
- backup/import artifacts;
- local-path references;
- dependencies referenced by LUNA body;
- semantic search for the underlying content rather than guessed filenames.

## Classification gate

R044–R047:

- `ABC = UNASSESSED`
- `XYZ = UNASSESSED`
- `Genome value = UNASSESSED`

No Canon promotion.

## NEXT SMALL PASS — Checkpoint 008

Return to **Agent Bodies Inventory**, one agent only.

Target: `VANDAL` historical provenance/body. Search exact registry/tree/consumer references, distinguish standalone body vs orchestration role, regression-check R038–R047, and checkpoint immediately.