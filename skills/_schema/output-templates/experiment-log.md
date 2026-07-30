---
knowledge_type: experiment-log
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Meta"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Experiment Log — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Hypothesis + variants + method + results + learnings — one experiment per file. Locks when sprint closes (after Results land). Aggregate view (Sheet) tracks all experiments per client per sprint cycle.

## Required frontmatter fields

```yaml
client: {slug}                       # or "genesys" for internal experiments
skill: experiment
version: 1
status: active | completed | abandoned
generated: {YYYY-MM-DD}
ontology_type: experiment-log
hypothesis: {falsifiable statement}
domain: content | messaging | workflow | outreach | pricing | growth
variants:                            # ≥2 entries
  - name: {variant name}
    description: {what's being tested}
control: {the baseline or null variant}
controlled_dimensions:               # held constant across variants
  - {dimension}
uncontrolled_dimensions:             # known confounds
  - {dimension}
success_metric: {metric}
baseline: {n + unit}
target: {n + unit}
linked_cycle: {path to goals/MMYY-NN-cycle.md}   # required for client-scoped experiments
linked_skill: {skill name}           # which skill this experiment tests
results: null                        # populated only when status=completed
learnings: null                      # populated only when status=completed
winner: null                         # variant_name or "inconclusive" when status=completed
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

**Locking gate:** `status: locked` requires `status: completed` first; `results` and `learnings` populated; sprint closed.

## Required body sections (in order)

1. **Hypothesis** — falsifiable statement with predicted direction + magnitude
2. **Setup** — what was changed, when, on what subset
3. **Variants** — variant-by-variant description + sample size targets
4. **Method** — how the experiment was run (tooling, instrumentation, gates)
5. **Predicted signal** — what we expected to see if hypothesis is true vs false
6. **Baseline + target** — pre-experiment baseline + target for this experiment
7. **Results** (only when `status: completed`) — measured outcomes per variant
8. **Learnings** (only when `status: completed`) — what we now believe; what to test next

## Optional body sections

- **Confounders observed** — uncontrolled dimensions that may have biased results
- **External events** — market / seasonal / news events during the experiment window
- **Next test** — proposed follow-up experiment

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Meta-tier requires ≥40% verified — but experiment-log baseline + results have higher bar (≥60%) when feeding client deliverables.

Sections requiring tags:
- Baseline (every baseline number: source — own data, prior period; method)
- Results (every measured outcome: instrumentation source + measurement window)
- Confounders observed (every named confounder: evidence)

Hypothesis + Predicted signal + Learnings are interpretive; tags inherit from cited evidence.

## Render rules per target

### gdrive (Doc — canonical for individual experiments)

- Inter, black, plain header, page-numbered footer, native TOC
- Variants table as Drive native table (rows: variants; columns: name, description, sample size, key metric)
- Results table as Drive native table (rows: variants; columns: outcome, lift vs control, confidence)

### gdrive (Slides) — N/A
### gdrive (Sheet — for series aggregate view)

Sheet variant: experiment series aggregate (one row per experiment, columns: ID, domain, hypothesis, status, baseline, target, winner, success_metric, learning, applies_to, promote, linked_cycle).

### notion (Page render)

- Overview = hypothesis + status + winner (when complete)
- H1 = "{Client} — {hypothesis short form}"
- Each H2 = toggle block; **Results toggle stays empty until status:completed** (intentional signal)

## Validation rules

1. All required frontmatter fields present
2. `domain` enum check
3. `variants` ≥2 entries
4. **`results` and `learnings` MUST be null while `status: active`** — validation fails if populated
5. **When `status: completed`:** `results`, `learnings`, `winner` all populated
6. `winner` is one of variant names OR literal "inconclusive"
7. `linked_cycle` resolves to existing cycle file (for client-scoped experiments)
8. **Hypothesis and Results are SEPARATE sections** — never combined
9. **Locking gate:** `status: locked` requires `status: completed` AND sprint cycle closed
10. `controlled_dimensions` + `uncontrolled_dimensions` documented (no silent confounders)

## Examples in the wild

- `.claude/skills/meta/learning/experiment/SKILL.md` is the runner for these
- Per-client experiments: `projects/consulting/active/{client}/goals/MMYY-NN-cycle.md` (cycle file references experiments)
- Phase 4 will produce conforming examples during rollout
