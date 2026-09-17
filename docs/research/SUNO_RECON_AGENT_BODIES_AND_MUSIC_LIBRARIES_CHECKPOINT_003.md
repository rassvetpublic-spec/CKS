# SUNO/KAT9I Recon — Checkpoint 003

Date: 2026-09-17
Status: DATA / RECON — not Canon

## Scope

This checkpoint narrows the reconnaissance to actual agent bodies and their libraries/data, not only agent names or architecture. Search targets: SKILL.md bodies, registries/manifests, referenced reference files, voice/vocal descriptors, delivery/cadence, adlibs/SFX, genre/subgenre, BPM, key, swing/pulse, rhythm, bass, drums, synths, instruments, effects, mix, STYLE/NEGATIV vocabulary, and research/trend inputs.

## Verified findings

### 1. Runtime registry is a library index

At `NewDeep67/KAT9I_IIIJIIOXA@073c497e1bdb64e8341990204d7587a980cc55e0`, `.agent/skills_manifest.json` reports 75 runtime skills. The registry stores lightweight metadata including category, manifest path, status, SHA-256 and tier origin. This confirms a hot-index/cold-body model: discoverable metadata can stay small while the full skill body is loaded on demand.

### 2. SUIGETSU body exposes the ten-agent production graph

`skills-catalog/creative/suigetsu-engine/SKILL.md` explicitly names: LUNA, Sui, KRONOS, VANDAL, Axiom, ZERO, Kodama, VOX, NEO, Mirage. It describes them as a coordinated production methodology and references historical local data files including `18_АНТИСЛОП_ДВИЖОК.txt` and `21_STYLE_WINDOW_AND_NEGATIV_V3.md`.

These referenced files are leads only. They are not considered recovered until exact source content/commit/hash is obtained.

### 3. LUNA body is a real music research database/protocol, not just a genre agent

`skills-catalog/creative/luna-researcher/SKILL.md` requires extraction of:
- track metadata and credits;
- scene/geography/subculture;
- four-level genre hierarchy;
- BPM, key, swing and pulse character;
- vocal timbre, effects, flow and speech defects;
- bass, drums, synths, live/sample instruments and mix;
- production descriptor string;
- idea bank: what to take / what to reject;
- current trend radar using live web research.

The production descriptor explicitly combines genre/subgenre, vocal flow/delivery, bass/distortion, drums/kick/hats, acoustic/sample switch, mastering/mix and vibe.

### 4. VOX body is a reusable voice-parameter library

`skills-catalog/creative/vox-voice-engine/SKILL.md` defines six independent voice dimensions:
1. origin/archetype;
2. pitch/spectrum;
3. timbral texture;
4. cavity resonance;
5. delivery/cadence;
6. signal chain.

Delivery includes aggressive punch, laid-back, machine-gun flow and sustained singing. Signal-chain vocabulary includes dry/upfront, zero reverb, FET warmth and de-essing. The body explicitly uses Voice Decoupling: voice character is treated independently from genre.

The exact polar-negative filter remains donor data only; do not promote its blacklist automatically.

### 5. Artist Mimicry body contains a behavioral vocal library

`skills-catalog/creative/artist-mimicry/SKILL.md` contains 13 phonetic/delivery archetypes and explicitly couples phonetic behavior with adlibs/SFX and STYLE descriptors. Examples include drunken/mumble/slurred flow, fast off-beat flow, whispered thriller, robotic/vocoder delivery and stuttering/glitch behavior.

Reusable donor candidate: behavior-first vocal archetypes + adlib/SFX behavior. Do not treat named-artist imitation as an active rule.

### 6. ZERO body contains a diagnostic/surgery library

`skills-catalog/creative/anti-slop-checker/SKILL.md` has 14 radar patterns, rhyme/assonance procedures and a three-option surgery protocol. Its numeric Slop-Score and universal bans are preserved as historical donor material only.

### 7. AXIOM body contains a section/event-chain library

`skills-catalog/creative/axiom-dramaturgy/SKILL.md` audits physical event chains, dramatic function, continuity, escalation, climax and line-level logical conflicts. This is a separate dramaturgical diagnostic library, not a replacement for Lyrics canon.

## Search correction / negative evidence

Guessed paths such as `neo-instrument-engine` and `kronos` were not found at those exact locations. This is NOT evidence that NEO/KRONOS bodies do not exist. Exact directory names must be recovered from the registry/tree rather than guessed. Future search must use registry metadata or verified tree entries.

Public web search was not used as a substitute for the private donor repository. Repository-native evidence remains authoritative for donor recovery.

## Regression against checkpoints 001–002

- R001–R018 remain unchanged.
- R018 (LUNA) is now strengthened from commit-level evidence to actual body-level evidence.
- R011 (JIT/on-demand) is strengthened by the 75-skill registry with body paths/hashes.
- R007–R009 remain valid: manifest-first delegation, tail dedup and transactional harvesting.
- No old universal vocal negative, fixed 4-line structure, fixed Style length, or other legacy heuristic is promoted.
- The reconnaissance target is now explicitly `agent body + referenced library/data + musical parameter vocabulary`, not agent-name collection.

## Candidate extraction schema for future ABC/XYZ

Each future finding should be recorded as:

`R-ID | agent | body/path | library/data referenced | parameter family | exact evidence | historical outcome | current DirectSUNO coverage | uniqueness | ABC | XYZ | disposition`

ABC and XYZ remain `UNASSESSED` until the evidence set is sufficiently complete.

## Next pass

Recover exact bodies for KRONOS, NEO, VANDAL, Kodama, Mirage and Sui from the verified registry/tree; then inspect their referenced libraries and data files. Search specifically for voice, genre, BPM, key, rhythm, arrangement, instrument, effects, adlib, STYLE and NEGATIV catalogs. Compare each finding against DirectSUNO only after extraction, not before.
