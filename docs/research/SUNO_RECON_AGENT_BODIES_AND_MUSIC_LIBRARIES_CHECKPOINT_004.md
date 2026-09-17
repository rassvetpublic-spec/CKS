# SUNO/KAT9I Recon — Checkpoint 004

Date: 2026-09-17
Status: DATA / RECON — not Canon

## New body-level evidence

### `.agent/skills_manifest.json`
Commit snapshot: `073c497e1bdb64e8341990204d7587a980cc55e0`.
Registry version 2.1.0, updated 2026-09-03, reports 75 runtime skills and 5 platform built-ins. Registry entries expose name/category/manifest_path/status/sha256/tier_origin. The first inspected entries confirm creative skills including `acestep`, `acestep-songwriting`, `ai-prompt-tuning`, `anti-slop-checker`, `artist-mimicry`, `axiom-dramaturgy`, `idea-generator` and others.

### `ai-prompt-tuning/SKILL.md`
Contains a music/text prompt-tuning skill, but its concrete body is tied to a Genre web application endpoint and Gemini JSON handling. Do NOT treat it as evidence of a general SUNO prompt compiler. Preserve as donor implementation evidence only.

### `idea-generator/SKILL.md`
IDEA Engine v3.3 has a three-stage pipeline: concept selection/filtering, text engineering/line selection, and deep audit. It explicitly checks physical detail, assonance, setup-flip, rhythm/breath and clip hooks. It contains old universal constraints such as numeric Slop-Score and `0%` verb rhyme targets; these are historical donor rules only.

## Stronger target model for remaining search

The reconnaissance must now enumerate, for every relevant creative skill:
1. SKILL.md body;
2. frontmatter metadata;
3. references/ subfiles;
4. data/catalog JSON/TXT/MD files;
5. examples/templates;
6. tests/benchmarks;
7. historical versions and deleted predecessors;
8. musical parameter vocabularies: genre/subgenre/microgenre, BPM, key, meter, swing, pulse, groove, rhythm, bass, drums, synths, acoustic/live/sample instruments, effects, mix/master;
9. vocal parameter vocabularies: archetype, pitch, spectrum, timbre, resonance, delivery/cadence, flow, articulation, speech defects, adlibs, SFX, signal chain;
10. STYLE and NEGATIV construction logic.

## Important correction to search method

Guessed directory names are not acceptable evidence. Exact specialist paths must be recovered from the verified registry or repository tree. A 404 for a guessed path means only that the guessed path is wrong.

## Previous-result regression

R007–R018 remain valid. R018/LUNA is strengthened by body-level evidence. R011/JIT is strengthened by the real 75-skill registry. No previous donor disposition is replaced. No ABC/XYZ/Genome classification is assigned yet.

## Next chunk

Inspect the exact remaining creative manifest paths from the registry in small batches. Prioritize agent bodies and their `references/`/data libraries before generic engineering/platform skills. For every body, extract concrete musical/vocal parameter libraries and references rather than only the skill description.
