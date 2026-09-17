# SUNO RECON — Checkpoint 002: agent bodies and libraries

Date: 2026-09-17
Status: DATA-ONLY / forensic research
Purpose: preserve intermediate intelligence before future ABC/XYZ classification.

## Scope correction
The reconnaissance target is not only system architecture. We must recover the actual bodies of agents/skills and their supporting libraries: prompt rules, genre catalogs, BPM/tempo data, vocal models, instruments, structure tags, negatives, references, templates, scripts, and evolution history.

No item below is promoted to CKS Canon or DirectSUNO active rules by this checkpoint.

## Sources inspected
- NewDeep67/KAT9I_IIIJIIOXA historical repository and ZIP snapshot.
- skills-catalog/skills_registry.json at commit 073c497e1bdb64e8341990204d7587a980cc55e0.
- historical creative skill bodies available at that commit.
- local ZIP snapshot KAT9I_IIIJIIOXA_7b376c8e1ad2_20260902_023751.zip.

## Findings

### R019 — SUIGETSU engine body
Evidence: skills-catalog/creative/suigetsu-engine/SKILL.md at 073c497e1bdb64e8341990204d7587a980cc55e0.
- Presents a 10-role production methodology: LUNA, Sui, KRONOS, VANDAL, Axiom, ZERO, Kodama, VOX, NEO, Mirage.
- Claims autonomous #STYLE and #NEGATIV synthesis.
- References historical Anti-Slop Engine and Style Window/Negative material.
- Important: the body itself is a compact facade over deeper referenced files; those referenced files must be searched separately.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

### R020 — VOX voice-engine body
Evidence: skills-catalog/creative/vox-voice-engine/SKILL.md at same commit.
- Voice Decoupling: voice is treated as an independent character/instrument rather than genre-bound.
- Six factors: origin/archetype; pitch/spectrum; timbral texture; cavity resonance; delivery/cadence; signal chain.
- Explicit examples include gravelly rasp, whisper release, nasal constriction, throat/chest/skull resonance, aggressive punch, laid-back delivery, machine-gun flow, sustained singing.
- Negative construction is described as antithesis of selected voice factors plus acoustic-artifact shielding.
- Body explicitly allows Scream as a vocabulary item; therefore old universal anti-shout assumptions must not be reintroduced from historical defaults.
- It also contains a historical taboo against affirmative words vocal/vocals/singer/singing in #STYLE; this is historical donor behavior, not automatically current DirectSUNO policy.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

### R021 — AXIOM dramaturgy body
Evidence: skills-catalog/creative/axiom-dramaturgy/SKILL.md at same commit.
- Text is treated as dynamic drama, not static rhyme fragments.
- Checks causal continuity, physical world markers, character/psychological spine, and internal cost of the outcome.
- Section audit uses physical events + dramaturgical function + diagnostic failure.
- Includes concrete failure modes: broken continuity, phantom title, zero escalation, skipped climax, contradictory logic.
- Provides a structured audit output rather than merely rewriting lyrics.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

### R022 — ACE-Step songwriting body as parameter library
Evidence: skills-catalog/creative/acestep-songwriting/SKILL.md at same commit.
- Explicit dimensions: style/genre, emotion/atmosphere, instruments, timbre texture, era reference, production style, vocal characteristics, speed/rhythm, structure hints.
- Separates Caption from Lyrics and dedicated parameters.
- Dedicated parameters include duration, BPM, key, time signature, language.
- Lyrics can carry structure, vocal, instrumental and energy tags.
- Contains specific examples for raspy, whispered, falsetto, powerful belting, spoken word, harmonies, call-and-response, ad-lib; and high/low/building/explosive energy.
- Gives a granularity principle: less detail increases model freedom; more detail increases control.
- Gives a conflict-to-evolution pattern: start with one state, evolve into another, rather than forcing static contradictory descriptors.
- Also contains historical/engine-specific heuristics such as 6–10 syllables and fixed duration estimates; these remain donor evidence only.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

### R023 — Historical Suno prompt-engineer library
Evidence: ZIP snapshot files:
- skills-catalog/suno-prompt-engineer/suno-prompt-engineer.md
- docs/knowledge/suno-ai-prompt-engineering-guide.md
- src/models/suno_prompt.py
- src/core/prompt_engine.py
- src/core/descriptors.py
- skills-catalog/prompt-engineer/references/techniques.md
- skills-catalog/prompt-engineer/templates/*

Recovered concrete data, not just architecture:
- request schema fields: idea, genre, subgenre, mood, tempo_bpm, vocal_type, instruments, language, is_instrumental;
- vocal enum: male, female, duet, choir, instrumental;
- structure-tag enum includes Intro, Verse, Pre-Chorus, Chorus, Hook, Bridge, Drop, Guitar Solo, Synth Solo, Breakdown, Outro, Fade Out;
- historical genre catalog includes rock/electronic/hip-hop/pop/metal/ambient with subgenres, default BPM, instruments and vocal styles;
- historical artist replacement dictionary maps named artists to acoustic/production descriptors;
- prompt engine selected genre/subgenre, default BPM, mood, vocal style and up to two instruments, then sanitized Style and generated structured Lyrics;
- prompt-engineering library contains ReAct, Few-Shot, Output Schema, Meta-Prompt, Self-Consistency, Tree-of-Thoughts.
Important: these are historical implementation/data artifacts and may contain obsolete Suno constraints. Preserve as donor evidence, not active rules.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

### R024 — Genre/voice/tempo/instrument data are embedded in executable descriptors
Evidence: ZIP src/core/descriptors.py.
Recovered concrete catalog:
- rock: alternative rock, grunge, indie rock, post-punk, hard rock, punk rock; default 120 BPM; distorted guitars/heavy bass/punchy live drums; raw gritty/emotional rasp/powerful belting.
- electronic: synthwave, cyberpunk edm, drum and bass, deep house, techno, ambient lo-fi; default 128 BPM; analog synths/808/crisp percussion/sidechain pads; airy/robotic/ethereal female.
- hip-hop: boom bap, trap, drill, lo-fi hip-hop, cloud rap, r&b soul; default 90 BPM; hard 808/vinyl/sample keys/tight hats; smooth flow/melodic rap/deep pitched.
- pop: dance pop, electropop, indie pop, synth-pop, acoustic pop; default 115 BPM; acoustic guitar/punchy bass/synth hook; polished female/crisp male/layered harmonies.
- metal: metalcore, heavy metal, nu-metal, doom metal, symphonic metal; default 140 BPM; down-tuned guitars/double bass/blast beats; screams/growls+clean chorus/operatic.
- ambient: cinematic ambient, meditation soundscape, dark ambient, space drone; default 70 BPM; warm pads/reverberant piano/lush cello/nature sounds; ethereal chanting/whispered.
This is precisely the kind of data the reconnaissance must recover rather than summarize away.
Disposition: PRESERVE_AS_DONOR_REFERENCE. ABC/XYZ/Genome: UNASSESSED.

## Regression against previous reconnaissance
- R001–R018 remain unchanged and are not superseded.
- R019–R024 deepen the earlier conclusion: the donor contains actual agent bodies and concrete music parameter libraries, not only routing architecture.
- The earlier statement that the creative registry was merely a list is now insufficient: several registry entries point to full methodology bodies.
- The earlier negative search for `voice encyclopedia`, `microdosing`, and `studio.py` remains negative for the inspected KAT9I_IIIJIIOXA history; it does not rule out other repositories, branches, archives, or renamed files.
- The old universal anti-shout rule remains rejected as an active DirectSUNO rule; VOX provides positive historical evidence for delivery states including scream.
- The historical 120/130-character Style constraints remain unpromoted.

## Next reconnaissance target
Do not start ABC/XYZ yet. Continue source recovery in smaller passes:
1. fetch remaining high-value creative agent bodies from the registry;
2. recover every referenced library/file behind those bodies;
3. search for agent-specific templates, examples, catalogs, and scripts;
4. search Git history around each agent's introduction/change;
5. record exact path + commit + SHA where available;
6. only after source exhaustion begin F1 lost-idea normalization and later ABC/XYZ.
