---
# === Identity ===
name: skill-slug                      # MUST match parent folder name (lowercase, hyphens)
version: "1.0"                        # Semver. Bump on behavior changes.
last_updated: 2026-04-29               # ISO date YYYY-MM-DD
author: genesys-growth

# === Trigger surface (Claude Code uses `description` for auto-suggest) ===
description: |
  Single-paragraph description (≥80 chars) covering: what the skill does, what
  it produces, when it triggers ("Triggers: '...'"), what it depends on
  upstream, what it feeds downstream, and what NOT to use it for. Used by
  Claude Code's trigger matcher.
goal: One-sentence outcome — imperative voice, ≤200 chars.
outcome: What the locked artifact contains and what it unblocks downstream.

# === Taxonomy (drives folder placement + chain-lint + auto-sync catalog) ===
primitive: research                    # See enum in skill-frontmatter.schema.json
sub_primitive: null                    # null when primitive has no sub-grouping
ontology_type: company-context         # See enum (matches .claude/rules/ontology.md)
review_gate: 1                         # 0-4: 0=auto, 1=quick, 2=standard, 3=deep, 4=collaborative

# === Graph edges (chain-lint validates these resolve) ===
inputs:
  required: []                         # Skills whose output must exist first
  recommended: []                      # Skills whose output meaningfully helps
outputs:
  - type: company-context              # Usually mirrors ontology_type
    feeds_into:
      - competitor-research
      - icp-research
depends_on: []                         # Flat mirror of inputs.required
feeds_into:                            # Flat mirror of outputs[].feeds_into
  - competitor-research
  - icp-research

# === Operations (dispatch + MCP + push) ===
owned_by_agent: researcher             # role-agent: researcher|pmm|growth|content|sales|b2b-consultant|paid|operator
mcps_used:                             # MCP server names this skill calls
  - exa
  - apollo-io
  - firecrawl
push_targets:                          # Empty array if local-only
  - gdrive
triggers:
  slash_commands:
    - /skill-slug
  natural_language:
    - "natural phrase 1"
    - "natural phrase 2"

# === Lifecycle (locked-down state machine) ===
status: draft                          # draft | review | locked | superseded
locked_by: null                        # "Team" | "Genesys" | null while draft
locked_date: null                      # ISO date or null
lock_version: null                     # Integer, increments per unlock-relock
sources_count: 0                       # Updated on first run (not at rollout)

# === Legacy (preserved if previously set) ===
# context: fork                        # fork | inherit | fresh
# effort: medium                       # low | medium | high | max
# paths: "projects/consulting/**"
# disable-model-invocation: false
---

# Skill name

<!--
Phase 3 slim guarantee: ≤300 lines for SKILL.md; heavier reference material
goes to `references/` subfolder. Use `slim_exemption` field in frontmatter
only as last resort (Phase 4.5.0 protocol).

== Authoring checklist (read before writing this skill) ==

Single source of truth: `.claude/skills/_schema/AUTHORING.md` — the runbook
that consolidates Phase 4-5 + design + ontology rules. Read first.

Ontology + frontmatter:
- All required fields populated (validate via `_schema/validate-frontmatter.py`)
- ontology_type matches an enum in `.claude/rules/ontology.md`
- depends_on mirrors inputs.required (chain-lint enforces)
- feeds_into mirrors outputs[].feeds_into (chain-lint enforces)
- owned_by_agent resolves to a role-agent file (operator|researcher|pmm|growth|content|sales|b2b-consultant|paid)

Body discipline:
- ≤300 lines or documented `slim_exemption`
- Heavy material in `references/{topic}.md` siblings
- 90% content-preservation gate when slimming existing skills

If this is a DESIGN-OUTPUT skill (primitive: design / website / content+motion / etc.):
- Read `.claude/rules/design-production.md` § "Skill authorship contract" — the 6 requirements
- Declare `inputs.recommended: [brand-kit]` in frontmatter
- Uncomment the "Design cycle (post-authoring phases)" block below
- Add a row to design-production.md "Skill integration cheat sheet" table
- Include "Run /design-reviewer as the final ship-ready gate" in body
-->

## When to run

**Invoke when:**
- "[trigger phrase]"
- "[trigger phrase]"

**Do NOT invoke when:**
- [anti-trigger — a different skill fits better]

## Inputs

| Input | Required? | Source |
|-------|-----------|--------|
| [input] | required / recommended | [where it comes from] |

If a required input is missing, name it and offer to run the upstream skill first.

## Steps

1. **[Step / phase]** — [what happens]. Output: [what it produces].
2. **[Step / phase]** — [what happens]. Output: [what it produces].

## Output format

[Shape of the deliverable — headers, structure, any length/character limits. Client-facing docs follow `.claude/rules/doc-output-structure.md`.]

## Self-roast (run before ship)

- Anti-hallucination: mark unknowns `[PLACEHOLDER: …]`, cite sources (URL + date), never invent metrics or quotes.
- Quality pass: every required section present + substantive; claims traced to inputs; voice + seven-tenet gate (`.claude/rules/output-tenets.md`) passed.

## References

- `references/{topic}.md` — [heavy material extracted to keep the body ≤300 lines]

<!-- Uncomment for design-output skills:

## Design cycle (post-authoring phases)

After producing the happy-path output, walk these phases before ship. Each references the shared design-quality library at `../../meta/catalog/design-reviewer/references/` (adjust relative path depth to match this skill's location). Run `/design-reviewer` as the final ship-ready gate.

- **Layout** — `layout-tenets.md` (rhythm, alignment, density)
- **Distill** — `distill-principles.md` (strip-to-essence)
- **Typeset** — `typeset-principles.md` (measure, leading, scale)
- **Polish** — `polish-principles.md` (16 details + interaction states)
- **Harden** — `harden-checklist.md` (9-step production-readiness — code output only)
- **Cognitive load** — `cognitive-load-tenets.md` *(when output is data-dense)*
- **Delight** — `delight-patterns.md` (1–3 moments per screen)
- **Onboarding** — `onboarding-patterns.md` *(when output is app-shaped)*
- **Final review** — run `/design-reviewer` (5 dimensions × 0–4, P0–P3 severity)

Drop the phases marked with conditions if they don't apply to this skill's output type. See `design-production.md` § "Skill authorship contract" for guidance per output type.

-->

<!-- Uncomment for OUTPUT skills (per .claude/rules/premortem-production.md):

## Final ship gate

Run `/premortem --output` before ship. See `.claude/skills/meta/orchestration/premortem/SKILL.md` for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

For genuinely trivial outputs: a one-line stub `## Premortem\nNo failure modes — trivial change` satisfies the contract. Most shippable work has failure modes worth naming.

-->

<!-- Uncomment for MARKETING-COPY skills (per .claude/rules/persuasion-and-stickiness.md):

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Before ship: deploy the 1–2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), then run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate. Adjust the relative-path depth (`../`) to match this skill's folder — copy it from the skill's existing "Output complies with […]" line. The `check_copywriting_contract` validator soft-warns until the body references `persuasion-and-stickiness`.

-->

<!-- Uncomment for skills that consume MCPs that cost credits (Apollo, Clay, Apify, Exa):

## MCP credit gate

This skill calls [Apollo / Clay / Apify / Exa]. Per `.claude/rules/apollo-credits.md` (or equivalent), credit-spend operations require explicit user confirmation before execution. The companion hook `.claude/hooks/mcp-credit-gate.sh` enforces this at runtime; the SKILL.md body should also state which operations are credit-spending vs free.

-->

<!-- Uncomment for skills with output that lands in client folders:

## Output routing

Output lands at `projects/consulting/active/{client}/{lane}/{stage}/MMYY-{topic}.md` per `.claude/rules/consulting-clients.md` auto-routing rule. The companion hook `.claude/hooks/output-routing-check.sh` flags violations.

-->

