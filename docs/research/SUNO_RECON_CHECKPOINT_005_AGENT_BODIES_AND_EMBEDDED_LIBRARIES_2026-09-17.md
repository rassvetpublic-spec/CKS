# SUNO RECON — Checkpoint 005: agent bodies and embedded music libraries

Date: 2026-09-17  
Status: **DATA-ONLY / forensic research / NON-CANONICAL**  
Parent research stream: CKS #31  
Scoped work item: CKS #35

## 0. SSoT boundary

This checkpoint stores research Evidence only.

It does **not** define the current music-agent Canon and does not promote recovered donor material into CKS Canon.

Authority split for this work:
- `rassvetpublic-spec/AndreysSUNOBOT` #8/#9 — durable music-agent/music-engine archaeology lane and current music-agent canon lane;
- CKS #31 — parent SUNO/KAT9I reconstruction research stream;
- CKS #35 — bounded search scope for agent bodies and embedded libraries;
- KAT9I_OS #233/#239 — separate architecture-forensics program;
- `NewDeep67/KAT9I_IIIJIIOXA`, `NewDeep67/kat9i_skills`, fork `rassvetpublic-spec/kat9i_skills` — Evidence sources, not CKS Canon.

No recovered prompt, body, engine, vocabulary, lookup table, Style rule, vocal rule, BPM rule, or scoring rule is authoritative merely because it existed historically.

---

## 1. Mission correction

Previous search emphasis on `SUMA` / `VOX` was too narrow.

The actual recovery target is the **complete historical KAT9I/SUNO music knowledge layer**, including:

1. full agent bodies/prompts;
2. input/output contracts and handoffs;
3. numbered engines and predecessor files;
4. referenced scripts/data/templates;
5. embedded dictionaries, taxonomies and tables;
6. genre/subgenre/style vocabulary;
7. tempo/BPM/groove/rhythm vocabulary;
8. vocal/timbre/register/delivery knowledge;
9. structure, harmony, instrumentation and arrangement vocabularies;
10. FX/signal-chain/mix/master vocabularies;
11. lyrics/rhyme/phonetics/prosody/slang/wordplay knowledge;
12. hooks/virality/dramaturgy/anti-slop/negative-prompt rules;
13. SUNO-specific tags, Style/Lyrics/Negative grammar;
14. examples/few-shot/reference blocks;
15. aliases, versions, predecessors and descendants.

`SUMA` is now treated as one unresolved alias/lineage hypothesis inside the broader Voice lineage, not as the objective of the investigation.

---

## 2. Current adapted package: useful index, not historical proof

The current Agentic SUNO source package defines ten canonical agent names:

`LUNA, Sui, KRONOS, VANDAL, Axiom, ZERO, Kodama, VOX, NEO, Mirage`.

It also maps agents to memory-file names, including candidates such as:
- `07_СОВРЕМЕННЫЕ_ЖАНРЫ_2026.txt`;
- `08_ДВИЖОК_МИКРОДОЗИНГА_ЖАНРОВ.txt`;
- `12_ДВИЖОК_ФЛОУ_И_РИТМИКИ.txt`;
- `15_ДВИЖОК_РИФМ_И_АССОНАНСОВ.txt`;
- `16_ДВИЖОК_ИГРЫ_СЛОВ.txt`;
- `18_АНТИСЛОП_ДВИЖОК.txt`;
- `19_ДВИЖОК_БЭКОВ.txt`;
- `20_ДВИЖОК_ГОЛОСА_2026.txt`;
- `21_STYLE_WINDOW_AND_NEGATIV_V3.md`;
- `22_ТЕГИ_ИНСТРУМЕНТОВ_И_СИНТЕЗА.txt`.

Important limitation preserved from the source package itself: those memory files are registered by provided inventory, but their actual content/version has not yet been independently verified. Therefore **file name / allowlist membership is a search lead, not evidence of file content**.

This corrects a dangerous reconstruction shortcut: current role definitions must not be back-projected into historical agent bodies without exact historical provenance.

---

## 3. Historical evidence already confirmed before this checkpoint

### R038 — Mature music engines entered Git after pre-Git development

Evidence lineage already stored in AndreysSUNOBOT archaeology and earlier CKS checkpoints:
- import boundary around `NewDeep67/KAT9I_IIIJIIOXA` commit `4f939c17...`;
- the creative engine set appears in Git already in mature form;
- `VOX Generative Voice Engine` already identifies itself as v4.0 at first recovered Git appearance;
- old local path references point to an older numbered-engine corpus outside the normalized Git skill layout.

Interpretation: repository history is not necessarily the beginning of the agent/engine history. Search must include references to pre-import files and deleted predecessor artifacts.

Disposition: HISTORICAL EVIDENCE. No Canon promotion.

### R039 — Historical pipeline confirms the ten-name production team

Historical `suigetsu-engine` evidence names:

`LUNA, Sui, KRONOS, VANDAL, Axiom, ZERO, Kodama, VOX, NEO, Mirage`.

This supports continuity of the team names, but **does not prove that current adapted role descriptions are identical to the historical bodies**.

Disposition: HISTORICAL EVIDENCE.

### R040 — Numbered-engine lineage is real and broader than recovered Git bodies

Historical references include at least:
- `09_ДВИЖОК_ИДЕЙ.txt`;
- `18_АНТИСЛОП_ДВИЖОК.txt`;
- `21_STYLE_WINDOW_AND_NEGATIV_V3.md`;
- `26_ДВИЖОК_ПРОПОРЦИЙ_И_ИНЖЕНЕРИИ_ТЕКСТА.txt`.

The search target must therefore be the numbered corpus `01..26+`, including unknown adjacent versions/aliases, rather than only the normalized skill directories.

Disposition: HISTORICAL EVIDENCE / LOST-KNOWLEDGE SEARCH LEAD.

---

## 4. Descriptor-library evidence strengthened

### R041 — Historical Suno data model explicitly includes musical dimensions

Source: `NewDeep67/KAT9I_IIIJIIOXA` Issue #7.

The historical architecture task explicitly proposed a `SunoPrompt` whose Style dimensions included:
- genre;
- BPM;
- mood;
- instruments;
- vocals.

The same Issue explicitly requested a catalog of musical descriptors containing:
- genres;
- subgenres;
- mixing effects;
- vocal types.

This is important because it proves the search target is not speculative: the historical project explicitly intended a reusable music-descriptor knowledge layer.

Disposition: HISTORICAL DESIGN EVIDENCE. The planned catalog itself is not yet proven recovered from this Issue alone.

### R042 — Checkpoint 004 recovered executable descriptor lattice evidence

Existing CKS checkpoint 004 recovered a historical executable descriptor catalog where a genre record couples:
- subgenres;
- default BPM;
- instruments;
- vocal styles.

This strengthens R041 from design intent toward implementation evidence.

Important remaining question: determine whether this descriptor lattice was only a small prototype catalog or one projection of a larger pre-Git knowledge base.

Disposition: PRESERVE_AS_DONOR_REFERENCE / UNASSESSED for later classification.

---

## 5. Search taxonomy for embedded libraries

Every body/dependency pass must search semantically across the following dimensions, not only exact filenames.

### Voice / performance
`voice`, `vocal`, `singer`, `timbre`, `тембр`, `голос`, `register`, `range`, `pitch`, `formant`, `resonance`, `cavity`, `breath`, `rasp`, `falsetto`, `chest`, `head`, `mix`, `delivery`, `cadence`, `phrasing`, `articulation`, `diction`, `flow`, `recitative`, `spoken`, `sung`.

### Genre / style
`genre`, `subgenre`, `microgenre`, `style`, `mood`, `era`, `scene`, `fusion`, genre microdosing and cross-genre descriptors.

### Tempo / rhythm
`tempo`, `BPM`, `groove`, `swing`, `half-time`, `double-time`, `meter`, `subdivision`, `syncopation`, `pickup`, `stop-time`, rhythmic switches.

### Harmony / structure
`key`, `mode`, `tonal center`, `harmony`, `chord`, `Intro`, `Verse`, `Pre-Chorus`, `Chorus`, `Bridge`, `Drop`, `Breakdown`, `Solo`, `Outro`, `Hook`, section transitions.

### Instrument / production
instrument names, `arrangement`, `orchestration`, `drums`, `bass`, `808`, `guitar`, `piano`, `strings`, `synth`, `FX`, `signal chain`, `saturation`, `compression`, `reverb`, `delay`, `distortion`, `stereo`, `mix`, `master`.

### Lyrics / language
`lyrics`, `rhyme`, `assonance`, `phonetics`, `prosody`, `syllable`, `stress`, `slang`, `wordplay`, `double entendre`, diction rules, taboo/stop lists.

### Quality / routing
`hook`, `memorability`, `virality`, dramaturgy, anti-slop, cliché detection, negative prompts, forbidden moves, conflict gates, scoring and reason codes.

### SUNO grammar
Style vocabulary, Lyrics cues, section tags, Negative vocabulary, prompt grammar, output constraints and version-specific tags.

Any table or embedded block that effectively maps
`descriptor → genre/BPM/voice/instrument/FX/structure/role`
should be treated as a candidate library even if the source never calls it a library.

---

## 6. Agent-body forensic contract

A registry row is not the body.

For each historical agent or engine, recover the chain:

`registry/discovery metadata → manifest/body prompt → referenced files → scripts/data/templates → outputs/handoffs → downstream consumer`.

For every recovered unit record:
- stable finding ID;
- object type: `AGENT_BODY / LIBRARY / ENGINE / TEMPLATE / REGISTRY / RULE / EXAMPLE / ALIAS`;
- exact repository;
- exact ref/commit/blob;
- exact path;
- historical owner/consumer;
- version/epoch when known;
- summary of actual content;
- dependency links;
- relation to current AndreysSUNOBOT artifact;
- preservation status: `PRESERVED / PARTIAL / LOST / SUPERSEDED / UNKNOWN`;
- evidence class/confidence;
- donor disposition;
- `ABC / XYZ / Genome value = UNASSESSED` until the later classification gate.

---

## 7. Regression review of previous conclusions

### Corrected

1. **Old emphasis:** find SUMA and VOX lineage.  
   **Correction:** recover all bodies and embedded music knowledge; Voice lineage is one substream.

2. **Old shortcut risk:** current agent role can stand in for historical body.  
   **Correction:** current adapted role is only a present-day reference unless exact historical body provenance is found.

3. **Old shortcut risk:** memory allowlist proves memory content.  
   **Correction:** allowlist/file name is only a search pointer; content requires exact file/blob evidence.

4. **Old shortcut risk:** registry metadata equals agent implementation.  
   **Correction:** registry → body → dependencies must all be inspected.

### Retained

- `SUMA = VOX` remains NOT PROVEN.
- `SUMA = Suigetsu` remains unsupported by the recovered functional split.
- VOX v4.0 at first recovered Git appearance supports a pre-Git lineage hypothesis.
- historical 120/130-character Style constraints remain obsolete donor assumptions and are not promoted.
- donor material remains DATA until an explicit later Decision/Promotion path.

---

## 8. Next bounded passes

### PASS 2B — Agent Bodies Inventory
Recover exact historical body/manifest/dependency chain for each of the ten named roles. Negative evidence must be exact and scoped when a body is absent.

### PASS 2C — Embedded Libraries Inventory
Extract actual descriptor blocks/tables/dictionaries from recovered bodies and dependencies. Separate implementation from design-only references.

### PASS 2D — Numbered Engines Map
Build `01..26+ → function → historical consumer → recovered descendant → preservation status`.

### PASS 2E — Voice lineage
Search SUMA/VOX/aliases/predecessors only after broader body/library inventory prevents tunnel vision.

### PASS 2F — Lost Knowledge Registry
Consolidate recovered units into `PRESERVED / PARTIAL / LOST / SUPERSEDED / UNKNOWN` with exact evidence.

---

## 9. Classification gate

This checkpoint intentionally does **not** assign final ABC/XYZ or Genome value.

Current state:
- knowledge recovery: IN PROGRESS;
- provenance: partial;
- body inventory: incomplete;
- embedded-library inventory: incomplete;
- numbered-engine map: incomplete;
- lost-knowledge registry: incomplete;
- promotion to Canon: BLOCKED.

Only after inventory completeness should later work classify what is foundational, developmental, useful, archival, promotable, superseded, or rejected.
