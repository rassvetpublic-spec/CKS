# SUNO RECON — Checkpoint 004: prompt, orchestration and music-agent bodies

Date: 2026-09-17
Status: DATA-ONLY / forensic research

## R032 — Historical Suno prompt-engineer data body
Evidence: ZIP snapshot `KAT9I_IIIJIIOXA_7b376c8e1ad2_20260902_023751.zip`, `skills-catalog/suno-prompt-engineer/suno-prompt-engineer.md`.

Recovered concrete knowledge:
- Style was decomposed into microgenre, mood, BPM, key instrument and vocal style in the historical engine.
- Lyrics used section metadata such as Intro/Verse/Pre-Chorus/Chorus/Bridge/Drop/Outro and special instrumental tags.
- Historical vocal tags included raspy, whispered, falsetto, powerful belting, spoken word, harmonies, call-and-response and ad-lib.
- Historical energy tags included high/low/building/explosive.
- A named-artist replacement table translated artist names into sound descriptors.
- Historical body explicitly described itself as Lead Music Producer & Audio Prompt Architect.

Caution: its 120–130 character Style rule and some platform assumptions are obsolete donor material. Do not promote them.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

## R033 — Executable Suno request schema is richer than the old visible prompt template
Evidence: ZIP `src/models/suno_prompt.py`.

Recovered request dimensions:
`idea`, `genre`, `subgenre`, `mood`, `tempo_bpm`, `vocal_type`, `instruments`, `language`, `is_instrumental`.

Recovered result dimensions:
`title`, `style_prompt`, `lyrics`, `is_instrumental`, `bpm`, `tags_used`.

Recovered structure vocabulary includes Hook, Synth Solo and Breakdown in addition to the usual Intro/Verse/Pre-Chorus/Chorus/Bridge/Outro.

Potential reusable insight: treat prompt generation as a typed parameter object, not only free text. The parameter vocabulary itself is valuable donor data even if the historical implementation is obsolete.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

## R034 — Descriptor library couples genre → subgenre → BPM → instruments → voice
Evidence: ZIP `src/core/descriptors.py`.

The historical executable catalog stores each genre as a compound record containing:
- subgenres;
- default BPM;
- instrument set;
- vocal-style set.

This means the old engine had an explicit **descriptor lattice** rather than an unstructured word list. Example records exist for rock, electronic, hip-hop, pop, metal and ambient.

Potential reusable insight: a future DirectSUNO music knowledge layer could keep these dimensions independently queryable and compose them conditionally, instead of storing giant monolithic Style strings.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

## R035 — Auto-orchestrator rule contains a concrete dynamic-routing and delegation policy
Evidence: ZIP `.agent/rules/auto_orchestrator.md`.

Recovered behavior:
- obvious engineering decisions should be made autonomously;
- irreversible operations and critical equal alternatives require user involvement;
- non-trivial tasks are internally classified and profile skills are activated by domain;
- 1-agent mode is used for simple/linear tasks, 2–3 agents for independent heavy modules;
- research/audit agents are explicitly routed to cheaper model tiers;
- critical logic changes trigger additional audit;
- every code change requires a syntax/test check;
- changes are recorded in a changelog;
- knowledge harvesting has a tail-based exclusion gate to avoid re-harvesting sessions already ending in knowledge synchronization.

Important distinction: this is an operational rule body, not merely a high-level architecture diagram.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

## R036 — Prompt-engineer body + library provide a reusable technique catalog
Evidence: ZIP:
- `.agent/skills/prompt-engineer/SKILL.md`
- `skills-catalog/prompt-engineer/prompt-engineer.md`
- `skills-catalog/prompt-engineer/references/techniques.md`
- `skills-catalog/prompt-engineer/templates/*.md`

Recovered library:
- diagnostic pre-pass: target model, task class, output format, context/tool availability;
- technique selection: ReAct, Few-Shot, Output Schema, Meta-Prompt, Self-Consistency, Tree-of-Thoughts;
- dedicated templates for system/agent/meta prompts and chain-of-thought;
- mandatory post-generation verification of role, output format, negatives and contradictions;
- anti-bloat rule: every sentence should carry meaning; avoid vague wording and duplicate instructions.

Potential reusable insight: the machine that creates prompts can itself have a **technique selector + template library + post-generation validator**, rather than one universal prompt template.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

## R037 — Agent body vs registry distinction confirmed
Evidence: `skills-catalog/skills_registry.json` and the fetched creative bodies.

The registry is not the knowledge itself. It carries discovery metadata: name, aliases, description, manifest path, SHA256, skill ID, status, tags and tier options. The actual body lives at the manifest path. Therefore future reconnaissance must inventory both:
1. registry metadata;
2. manifest/body;
3. referenced files;
4. scripts/data/templates used by the body.

Potential reusable insight: build the forensic inventory at the **registry → body → dependencies** level.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

## Regression check
- R001–R031 remain valid and are not overwritten.
- R019–R030 are strengthened by actual body/library inspection.
- Earlier negative evidence for missing `voice encyclopedia`, `microdosing`, and `studio.py` remains scoped to the inspected repository/history only.
- No historical Style-length rule, fixed syllable law, universal vocal prohibition, or scoring scheme is promoted.

## Next target
Continue body/dependency recovery for the named production agents: LUNA, KRONOS, VANDAL, KODAMA, NEO, MIRAGE and Sui. Search by exact manifest paths where available, then inspect all referenced files. If a named agent has no body in the accessible snapshot, record exact negative evidence rather than reconstructing it.
