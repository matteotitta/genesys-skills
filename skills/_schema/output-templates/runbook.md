---
knowledge_type: runbook
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Meta"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: gdrive-doc
---

# Runbook — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Step-by-step procedure with troubleshooting — the "how to do X" doc that makes operations repeatable. Internal-facing working document. Rarely locks (runbooks evolve as procedures evolve).

## Required frontmatter fields

```yaml
client: {slug}                       # or "genesys" for internal runbooks
skill: runbook
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: runbook
runbook_type: procedure | troubleshooting | onboarding | recovery
audience: developer | operator | client-stakeholder
triggers:                            # when to run this runbook
  - {trigger condition}
prerequisites:
  - {required state}
expected_outcomes:
  - {observable outcome}
troubleshooting_section_present: true   # MUST be true (validation rule)
related_skills:                      # cross-refs to skills this runbook supports
  - {skill name}
related_mcps:                        # MCPs invoked by this runbook
  - {mcp name}
last_field_test: null | {YYYY-MM-DD}  # when last validated by running it
sources_count: { verified, inferred, estimated, unavailable }
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order)

1. **Header block** — runbook_type, audience, triggers, prerequisites, expected_outcomes
2. **Prerequisites** — what must be in place (tool installed, credential configured, prior step done)
3. **Procedure** — numbered steps; each step has expected output + verification
4. **Verification** — how to know the runbook completed successfully
5. **Troubleshooting** — common failures + fixes (REQUIRED — this is what makes a runbook useful)
6. **Common gotchas** — non-obvious traps + mitigations
7. **Quick reference** — one-screen summary for experienced runners
8. **Related** — links to related runbooks, skills, MCPs

## Optional body sections

- **Field test log** — when team has tested the runbook, what failed
- **Versioning notes** — what changed between versions
- **Rollback procedure** — for procedures that have side effects

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Meta-tier requires ≥40% verified — but most runbook content is procedural, not evidentiary.

Sections that require tags:
- Any external API behavior claim (version-specific, MCP tool behavior)
- Any tool/version behavior (e.g., "this works on Node 18+; fails on 16") — evidence from documentation or tested

Procedure steps themselves don't need tags — they're imperative actions, not factual claims.

## Render rules per target

### gdrive (Doc — canonical)

- Inter, black, plain header, page-numbered footer, native TOC
- Steps as numbered list with expected-output called out via blockquote or callout
- Troubleshooting as 2-column Drive native table (left: symptom; right: fix)

### gdrive (Slides) — N/A
### gdrive (Sheet) — N/A

### notion (Page render — for collaborative procedure)

- Overview = runbook_type + triggers + prerequisites in 2 sentences
- H1 = runbook title
- Each H2 = toggle block; **Troubleshooting toggle is collapsed by default** (happy path reads cleanly without expansion)

## Validation rules

1. All required frontmatter fields present
2. `runbook_type` enum check
3. `audience` enum check
4. **`troubleshooting_section_present: true`** — validation fails otherwise (the section MUST exist)
5. `triggers` array: ≥1 entry
6. Procedure: ≥1 step
7. Each step has expected output + verification method
8. Body length: ≤200 lines (split into multiple runbooks if longer)
9. `prerequisites` MAY be empty but section MUST exist

## Examples in the wild

- `.claude/skills/meta/learning/runbook/SKILL.md` is the runbook for runbooks
- Phase 4 will produce conforming examples during rollout
