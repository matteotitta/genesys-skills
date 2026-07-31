---
name: eval-harness
version: '1.0'
last_updated: 2026-05-25
author: genesys-growth
description: 'Deterministic programmatic gate for Genesys skill outputs and client deliverables. Stdlib Python evaluator that scores markdown artifacts against weighted rubric.json files — section presence, sentence/word counts, regex patterns, keyword anti-pattern guards, frontmatter validation, citation tag presence. No LLM calls. Composes with the qualitative LLM reviewers (voice-reviewer / design-reviewer / skill-reviewer): this gate fires first on structure, LLM reviewers fire after on voice + taste. Triggers: "eval", "lint this skill output", "score this artifact", or as a pre-commit / CI gate on `.claude/skills/` PRs and client deliverable PRs.'
goal: Deterministic structural quality gate for skill outputs and client deliverables.
outcome: Per-artifact pass/fail report with weighted score (0-100), blocker count, warning count, and gate status (PASS/FAIL). Composes with LLM reviewers.
primitive: meta
sub_primitive: catalog
ontology_type: runbook
review_gate: 1
inputs:
  required: []
  recommended:
  - rubric.json (per skill being gated)
- type: eval-report
  feeds_into:
  - skill-catalog
depends_on: []
- skill-reviewer
- voice-reviewer
- design-reviewer
owned_by_agent: operator
mcps_used: []
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: medium
disable-model-invocation: true
---

# /eval-harness — Deterministic structural gate for skill outputs

Stdlib Python that scores a markdown artifact against a declarative `rubric.json`. Runs in <100ms per artifact. No LLM calls — pure regex / section extraction / count checks.

The gate is **complementary to LLM reviewers**, not replacement. Structural rules are deterministic and cheap; voice / brand / taste judgment stays in `voice-reviewer`, `design-reviewer`, `skill-reviewer`.

---

## When to use

- Pre-commit hook on `.claude/skills/` PRs — catch missing sections, malformed frontmatter, banned keywords before the LLM reviewer pass
- CI gate on client deliverable PRs (proposals, positioning docs, messaging libraries, landing-page copy, AEO articles)
- Local lint during authoring: `python run.py --skill positioning`
- Sanity-check before voice-reviewer runs (saves expensive LLM passes on structurally broken drafts)

## When NOT to use

- For qualitative judgment (tone, voice, brand fit) — that's `voice-reviewer`
- For visual / design output — that's `design-reviewer`
- For skill-internal SKILL.md quality — that's `skill-reviewer`
- For one-off outputs without a stable rubric — rubric authoring costs more than the gate saves below ~5 artifacts

---

## Anatomy

```
eval-harness/
├── SKILL.md ← this file
├── engine.py ← check evaluator (stdlib, no LLM)
├── run.py ← walker + report renderer
├── NOTICE.md ← attribution to source pattern
├── the premium reference
│ ├── check-types.md ← every check type with example
│ └── rubric-authoring.md ← how to write a rubric for a Genesys skill
└── rubrics/
    ├── client-proposals.json
    ├── positioning.json
    ├── messaging.json
    ├── landing-page-copy.json
    └── aeo-content.json
```

## Workflow at a glance

| Step | Action | Output |
|------|--------|--------|
| 1 | Author `rubrics/{skill}.json` per gated skill | Declarative criteria with weights + severity |
| 2 | Run `python run.py --skill {skill}` against latest artifact | Per-criterion pass/fail + weighted score |
| 3 | On PASS, advance to LLM reviewer pass | `voice-reviewer` / `design-reviewer` / `skill-reviewer` |
| 4 | On FAIL with blocker, fix structure first | Re-run step 2 |
| 5 | On FAIL with only warnings, surface but proceed | Warnings logged, not blocking |

---

## Rubric shape

```json
{
  "skill": "positioning",
  "version": "1.0",
  "description": "Gates Genesys positioning docs for structural completeness + voice blocklist.",
  "threshold": 70,
  "artifacts": [
    "projects/consulting/active/*/positioning/*.md"
  ],
  "criteria": [
    {
      "id": "position_section_present",
      "name": "Position section present (Section 1)",
      "weight": 8,
      "severity": "error",
      "check": {"type": "section_present", "heading": "Position"}
    },
    {
      "id": "differentiators_section",
      "name": "Differentiators section present",
      "weight": 6,
      "severity": "error",
      "check": {"type": "section_present", "heading": "Differentiators"}
    },
    {
      "id": "no_buzzwords",
      "name": "Buzzword blocklist clean",
      "weight": 4,
      "severity": "warning",
      "check": {"type": "keyword_none", "keywords": ["leverage", "robust", "seamless", "synergy", "innovative"]}
    }
  ]
}
```

## Severity tiers

| Severity | Counts toward score? | Blocks gate? | Use for |
|----------|---------------------|--------------|---------|
| `error` (default) | full weight | yes | Load-bearing structure (required sections, required frontmatter fields) |
| `warning` | half weight | no | Style / preference (buzzword blocklist, em-dash spacing) |
| `info` | no | no | Telemetry-only (link count, doc length) |

Start any new rubric with mostly `warning`. Upgrade to `error` only after seeing the criterion fail on PRs that should genuinely have been blocked.

## Check types

All check types live in [`engine.py`](engine.py) and are documented with examples in the premium reference:

- `regex` / `regex_absent` — pattern match / anti-match
- `section_present` — markdown heading exists
- `section_word_count` / `section_sentence_count` — body length bounds
- `keyword_any` / `keyword_all` / `keyword_none` — keyword presence checks
- `has_table` / `has_list` — structural markers
- `url_count` / `length_in_range` / `line_count_range` — quantitative bounds
- `frontmatter_field_present` — YAML frontmatter validation (Genesys addition)
- `max_heading_level` — enforce `doc-output-structure.md` H1/H2-only rule (Genesys addition)
- `citation_present` — assert `[VERIFIED:...]` / `[INFERRED:...]` tags per ontology (Genesys addition)

## Composition with LLM reviewers

```
PR opens / artifact saved
        │
        ▼
┌──────────────────────────┐
│ eval-harness (this) │ ← deterministic, <100ms, free
│ Structure + frontmatter │
│ + banned-keyword check │
└────────────┬─────────────┘
             │
        ┌────┴────┐
        ▼ ▼
       PASS FAIL (blocker)
        │ │
        ▼ └→ Fix structure, re-run
┌──────────────────────────┐
│ voice-reviewer │ ← LLM, ~2K tokens, qualitative
│ Voice + brand + 100 │
│ Posts Test │
└────────────┬─────────────┘
             │
        ┌────┴────┐
        ▼ ▼
       PASS FAIL
        │ │
        ▼ └→ Rewrite, re-run from top
   Ship-ready
```

## CI integration

Sample GitHub Action stub at the premium reference The runner emits markdown by default (PR comment friendly) or JSON (programmatic consumption).

```bash
# Local lint
python.claude/skills/meta/catalog/eval-harness/run.py --all

# Single skill
python.claude/skills/meta/catalog/eval-harness/run.py --skill positioning

# Override threshold
python.claude/skills/meta/catalog/eval-harness/run.py --all --threshold 80

# Strict mode (exit 1 on any blocker — CI-friendly)
python.claude/skills/meta/catalog/eval-harness/run.py --all --strict
```

## Anti-patterns

- ❌ Authoring rubrics with all-`error` severity. Almost everything starts `warning`; upgrade to `error` after seeing the criterion catch real PR pain.
- ❌ Rubrics that mirror voice-reviewer (subjective). If a check needs an LLM to judge, it's not for this gate.
- ❌ Aiming for full skill coverage. Author rubrics for skills that have caused real PR pain. Skills without rubrics are un-gated by this harness — fine.
- ❌ Treating the gate output as ship-ready signal. Score ≥ threshold + zero blockers means "structure is OK"; voice/brand quality still needs an LLM reviewer.

## Roadmap (uncommitted)

- Per-criterion auto-fix suggestions (`suggest:` field in rubric → `engine.py` prints fix hint on failure)
- Rubric inheritance (`extends: positioning.json` for skill variants)
- Web UI report (currently markdown / JSON only)

