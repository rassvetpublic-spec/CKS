# SUNOBOT forensic checkpoint — donor evidence

Date: 2026-09-17  
Status: `INTERMEDIATE / DONOR / NON-SSOT`

This document indexes the current forensic reconstruction of the historical SUNOBOT / SUIGETSU system. It does **not** promote donor material into CKS canon.

Primary preservation location:
- repository: `rassvetpublic-spec/AndreysSUNOBOT`
- branch: `forensics/2026-09-17-all-artifacts`

## Search contract

Search is broader than the word `SUNO`. Candidate evidence includes agent/system-prompt bodies; role aliases; memory/files-in-memory; inputs/outputs; prohibitions; gates; scores; loops; vocals/voice/timbre; genre/microgenre; BPM/tempo/beat/flow; lyrics/rhyme/hook; structure/dramaturgy; Style/Negative; instruments/synthesis/FX; mix/master; backing/adlibs/SFX; formatting and limits.

A file may be a high-value library without containing an agent name. Agent ownership requires direct provenance and is not inferred from substrings such as `neo-soul` or `suite`.

## Recovered role set

Ten roles are directly evidenced across old cores, live execution and later orchestration material:
`LUNA, Sui/SUI, KRONOS, VANDAL, Axiom, ZERO, Kodama, VOX, NEO, Mirage`.

Earlier naming evidence also preserves `LIMA`, `SUIT`, and `Aktion`.

## Recovered bodies

### `5.txt`
Status: COMPLETE in 7 lossless parts.  
SHA-256: `f8e2556a7893849f8cf001880abb0d1a4e5331c6dce60fa43aee74da23773a2e`

Direct evidence:
- ten agents;
- `Файлы в памяти` assignments;
- tasks/handoffs;
- feedback-loop behavior.

### `ЯДРО_2.0.txt`
Status: COMPLETE in 4 parts.  
SHA-256: `759f031b73098b185d6e421288b014669ac6b06ffcc7d49abb59bbaa6c714f7b`

Direct evidence:
- `SUIGETSU 10-AGENT SUNO PRODUCTION ENGINE v2.0`;
- statement that each file is the “brain” of a specific agent and agents use scoped instructions;
- full bodies for all ten roles;
- pipeline ordering;
- genre adaptation;
- Style/Negative contract;
- historical limits;
- Mirage release checklist;
- historical output contract and knowledge inventory.

### `ядро v2.txt`
Status: COMPLETE in 4 parts.  
SHA-256: `b8fac14abeb177a36aa83a4bf83022dc2309e468dac4c96d6245b3e4e94caeb1`

Direct evidence:
- internal historical conflict: heading says `9 АГЕНТОВ`, body enumerates ten;
- NEO explicitly appears as `[НОВЫЙ АГЕНТ]`;
- direct memory assignments;
- older Mirage Style limit and output-generation rules.

### `промпт 15.txt`
Raw SHA-256: `0243f0067c9986edca977490bd97bea98dade2646e0577c8be1a0a0bc08cc8de`

GitHub copy is a sanitized forensic replica because the raw historical source contains credential-like literal values. Music/agent content is retained.

Direct evidence:
- self-audit dialogue of all ten roles;
- `LUNA Engine v4.0`, `AXIOM Engine v3.0`, `Slop-Score 2.0`, `SUIGETSU ENGINE v3.5`;
- NEO High-Density Prompt Compression;
- VOX+Kodama multi-voice isolation;
- Sui cross-language assonance;
- VANDAL+KRONOS micro-drop retention;
- W1–W8 weighted scoring and historical TPW admission gate;
- reference to `26_ДВИЖОК_ПРОПОРЦИЙ_И_ИНЖЕНЕРИИ_ТЕКСТА.txt`.

## Live execution evidence

Six screenshots are preserved/transcribed as primary operational evidence. They show ZERO, NEO, KRONOS, VANDAL, Kodama, Axiom, LUNA, VOX and Mirage actively handing work across a production task; SUI appears in the hidden weighted matrix as phonetic integration. The trace contains a formal weighted evaluator and `СТАТУС: ДОПУСК` gate.

## Libraries

Already preserved in the forensic branch: Mirage checklist, tag conflicts, idea engine, backs, genre sources, VOX/vocal material, ONE_SHOT, new functions, ZERO anti-slop, Style/Negative, text engine, line-delivery engine, Axiom dramaturgy, and runtime/conversation sources.

`12_ДВИЖОК_ФЛОУ_И_РИТМИКИ.txt` is COMPLETE 4/4 and classified `SHARED_LIBRARY`: vocal personas, vocal processing, flow, cadence, pauses, CIS flows, SoundCloud/Trap, 2025–2026 microgenres, Style prompts and lyric meta-tags.

`22_ТЕГИ_ИНСТРУМЕНТОВ_И_СИНТЕЗА.txt` is classified `NEO LIBRARY` because `5.txt` directly assigns file 22 to NEO. Current preservation status: parts 01–02 committed; parts 03–06 next.

## Authoritative corrections

- Semantic scan V3 supersedes V1/V2 for ambiguous short agent names.
- `NEO` inside `neo-soul` etc. is not agent evidence.
- Historical limits, pipeline order and output format are versioned facts; conflicts remain visible.
- Donor evidence stays non-canonical until explicit CKS review/promotion.

## Exact continuation point

Do not restart.

1. `22_ТЕГИ_ИНСТРУМЕНТОВ_И_СИНТЕЗА.txt` parts 03–06
2. `FIX SUNOOOOo (1).txt`
3. `raw_genres (2).txt`
4. `помощник .txt`
5. cross-dump source ledger + lineage
6. final matrix: `BODY / LIBRARY / SHARED_LIBRARY / ORCHESTRATION / EVALUATOR / OUTPUT_TEMPLATE`
7. update the four main forensic documents after primary evidence coverage.

Latest preservation commits in `AndreysSUNOBOT`:
- `96a6f584279906dfe31a9fbb965b46c8bc04ff97` checkpoint
- `b4d4d81aba287a3fbbf0fce4d8558c42a334f1b1` completes `5.txt`
- `e8f8f7862fc978c3d7637ac58a8026b1ec533fe8` completes `ЯДРО_2.0`
- `4283df31a46476231cd33c94382ce77208e0012f` completes `ядро v2`
- `66539997905fca521672d51444a02bf6ade8d886` completes sanitized `промпт 15`
- `0d1850cc1155fd869ac130df4725e1c5caa581e7` progress checkpoint
- `fdff4452c4b65d65c8dbfb906e31c12eacaef668` completes flow/rhythm library
- `4ebdb2a435e2a6885f2478dd7f3eb291450d2b7c` NEO tag library part01
- `94dc8546dcd588ff505269867d0593e1b41520fa` NEO tag library part02

Preservation policy: keep old generations, provenance and conflicts. Distinguish `SOURCE_FACT`, `INFERENCE`, `RECOMMENDATION`, `UNVERIFIED_DERIVED`.
