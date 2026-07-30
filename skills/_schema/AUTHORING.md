# Skill authoring runbook — the single source of truth

**Read this before authoring any new skill.** This runbook consolidates Phase 4–5 schema rules + design authorship contract + brand-context conventions + ontology rules into one document. Updates propagate when the underlying rules update — this file references them rather than duplicating.

If you (or me on your behalf) are creating a new skill — whether it's a Hyperframes derivative, a new wireframe variant, a dashboard tool, a content engine, anything — this is the SOP.

---

## Why this exists

Skills in this catalog must comply with multiple overlapping rule sets:

- **Phase 4 schema** — `_schema/skill-frontmatter.schema.json` (15 required frontmatter fields, enum constraints, validators)
- **Phase 4.5 + 5 body discipline** — ≤300-line body cap, `references/` slim pattern, 90% content-preservation gate, `slim_exemption` only as last resort
- **Companion (hooks) Phase F** — runtime gates: `mcp-credit-gate.sh`, `stale-context-warning.py`, `output-routing-check.sh`, `subagent-telemetry.sh`
- **Companion (agents)** — role-agent reciprocity: `owned_by_agent` resolves to a role-agent file
- **Auto-sync hooks** — `pre-commit.sh` runs `validate-frontmatter.py` + `chain-lint.py` + `regenerate-catalog.py` + `regenerate-role-agents.py` on every commit
- **Ontology** — `.claude/rules/ontology.md` constrains `ontology_type` enum
- **Design authorship contract** (for design-output skills) — `.claude/rules/design-production.md` § "Skill authorship contract" — 6 requirements
- **Apollo / MCP credit rules** — `.claude/rules/apollo-credits.md` for skills that call paid MCPs
- **Output routing** — `.claude/rules/consulting-clients.md` auto-routing rule for client-folder outputs

Authoring a skill correctly requires touching all of these. This runbook is the linearized walkthrough.

---

## The walkthrough

### Step 1 — Decide if a new skill is justified

Before authoring, check:
- Does an existing skill cover this? (Search the catalog at `meta/catalog/skill-catalog/SKILL.md` — auto-regenerated body lists every skill.)
- Could this be a `references/` file inside an existing skill instead?
- Could this be a new section in `design-production.md` or another rule?

**Default: don't add a new skill.** New skills cost frontmatter + chain-lint + role-agent reciprocity overhead. Add a reference file or rule update first; promote to a skill only when the workflow is clearly distinct.

### Step 2 — Copy the template

```bash
cp .claude/skills/_schema/SKILL.template.md \
   .claude/skills/{primitives|meta}/{primitive}/{name}/SKILL.md
```

The template includes commented-out scaffolds for design-cycle, MCP credit gate, and output routing. Uncomment whichever apply.

### Step 3 — Fill the frontmatter

Reference: `_schema/skill-frontmatter.schema.json`. The 15 required fields, in order:

1. `name` — lowercase-hyphens, MUST equal parent folder name
2. `version` — string semver, e.g. `"1.0"`
3. `last_updated` — ISO `YYYY-MM-DD` (today's date for new skills)
4. `description` — ≥80 chars; covers what produces / triggers / upstream / downstream / anti-triggers
5. `goal` — 20–200 chars, imperative voice, one sentence
6. `outcome` — 20–300 chars, what the locked artifact contains + what it unblocks
7. `primitive` — enum: `research | product-marketing | content | website | social | lifecycle | seo-aeo | paid-marketing | outbound | sales-enablement | design | clients | meta`
8. `sub_primitive` — enum: `audit | strategy | execution | research | linkedin | youtube | newsletter | list-building | enrichment | email-copywriting | catalog | orchestration | session | learning | infra | motion | null`
9. `ontology_type` — enum from `.claude/rules/ontology.md` (use `runbook` for review/lint/process skills)
10. `review_gate` — integer 0–4
11. `inputs` — object with `required: []` + `recommended: []` arrays
12. `outputs` — non-empty array of `{type, feeds_into}` objects
13. `depends_on` — flat mirror of `inputs.required`
14. `feeds_into` — flat mirror of `outputs[].feeds_into`
15. `owned_by_agent` — enum: `researcher | pmm | growth | content | sales | b2b-consultant | paid | operator`
16. `status` — enum: `draft` for new skills

**Description craft (triggering).** The `description` is load-bearing for skill selection across 150+ skills — write it to carry judgment, not just a label. Bake the workflow hint ("start here when…"), the anti-trigger ("NOT for Y — use Z"), and any terminology the reader needs *inside* the description string. A description that reads like a decision ("use this when you need the WoW story, not a raw metrics dump") triggers more accurately than one that reads like a title. Stolen from `stan-default/liam` (MIT) — its tool descriptions carry the judgment, not just the params.

### Step 4 — Author the body

- Body ≤300 lines. Heavy material extracts to `references/{topic}.md` siblings.
- Standard sections: title + intro / Triggers / Inputs / Process / Output Format / Self-roast / References.
- Cite reference files via relative path links from the body.

### Step 5 — Apply applicable contracts

**If this is a DESIGN-OUTPUT skill** (primitive: `design` / `website` / `content`+motion / anything that produces visual deliverables):

Read `.claude/rules/design-production.md` § "Skill authorship contract" — the 6 requirements. Specifically:

1. `inputs.recommended` includes `brand-kit`
2. Body includes "Design cycle (post-authoring phases)" section pointing to `meta/catalog/design-reviewer/references/`
3. Body explicitly says "Run `/design-reviewer` as the final ship-ready gate"
4. Add a row to `design-production.md` § "Skill integration cheat sheet"
5. Apache-2.0 attribution if importing impeccable-sourced reference content

**If this is an OUTPUT skill** (primitive in `content` / `sales-enablement` / `outbound` / `lifecycle` / `social` / `paid-marketing` / `website` / `design` / `product-marketing` / `seo-aeo` / `clients`, OR any skill producing client-facing / external-facing deliverables):

Read `.claude/rules/premortem-production.md` — the 4-requirement contract. Specifically:

1. Body includes a `## Final ship gate` section (H2 heading, near end-of-body before Changelog)
2. Section contains the line: *"Run `/premortem --output` before ship. See `.claude/skills/meta/orchestration/premortem/SKILL.md` for the 5 execution domains and output template."*
3. Don't customize the 5 execution domains — single source of truth lives in `domains-output.md`
4. Validator (`validate-frontmatter.py` `check_output_premortem_contract`) soft-warns on missing reference

For skills that are BOTH design-output AND output (most landing-page / deck / carousel skills): include BOTH gate sections. /premortem --output runs BEFORE /design-reviewer.

**If this is a MARKETING-COPY skill** (primitive in `content` / `social` / `website` / `lifecycle` / `outbound` / `paid-marketing` / `seo-aeo` / `product-marketing`, execution-stage, producing persuasive copy — NOT strategy / research / audit / data-ops):

Read `.claude/rules/persuasion-and-stickiness.md` — Cialdini's 7 persuasion levers + Heath's SUCCESs stickiness framework. Specifically:

1. Body references `persuasion-and-stickiness.md` — add it to the "Output complies with […]" line, or a `## Persuasion & stickiness pass` section (uncomment the scaffold in `SKILL.template.md`)
2. Deploy 1–2 Cialdini levers that fit the reader's barrier; never all seven; every lever must be TRUE
3. Run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) + the rule's pre-ship gate before ship
4. Validator (`validate-frontmatter.py` `check_copywriting_contract`) soft-warns on missing reference

**If this is an ANALYTICAL / DATA-VERDICT skill** (audit, scoring, ranking, or reporting that renders a verdict / ranking / "winner" from counts — paid-audit, paid-ads-report, paid-ads-experiment-log, lead-scoring, reply-scoring, website-score, content-audit, pricing-research, product-pulse, ab-testing):

Read `.claude/rules/quantitative-evidence-floors.md`. Specifically:

1. **Bind the floor rule.** State the volume floor behind any verdict; below it, give a directional read + "too early" caveat, never a crown. Add it to the "Doctrine inherited" / guardrails line.
2. **Declare a Report-format contract.** Ship a named Output Format section, and — where the deliverable recurs (weekly/monthly report, quarterly audit) — a **literal fill-in template**, so runs are directly comparable at a glance. A comparable format is what turns a series of one-off reports into a trend. (Reuse a skeleton from `_schema/output-templates/` where one fits; don't duplicate it.)
3. **Synthesize, don't dump.** The output is the judgment + the 2–3 numbers that drive it, not raw report rows (floor rule §3).

Stolen from `stan-default/liam` (MIT) — every Liam analytical skill refuses a verdict below a volume floor, ships a fixed report format, and synthesizes rather than dumping rows. See [`.claude/discovery/0726-liam-steal-analysis.md`](../../discovery/0726-liam-steal-analysis.md).

**If this skill calls Apollo / Clay / Apify / Exa MCPs:**

Document credit-spending vs. free operations in body. Confirm with the user before any credit-spending call. The runtime hook `.claude/hooks/mcp-credit-gate.sh` enforces this; the SKILL.md states the policy.

**If this skill produces output landing in client folders:**

Document the output path per `.claude/rules/consulting-clients.md` auto-routing rule. The runtime hook `output-routing-check.sh` enforces.

**If this skill is a MULTI-PHASE SKILL CHAIN (3+ phases run sequentially):**

Adopt the **per-phase handoff convention**. /steal'd from `Andytoizer/agentoperator-outbound-engine` (2026-05-05; cite-only) — see [`.claude/discovery/0526-agentoperator-outbound-engine-steal-analysis.md`](../../discovery/0526-agentoperator-outbound-engine-steal-analysis.md) (P2).

Each phase writes a handoff file with 7 fields: Status / Inputs read / Outputs written / Gates passed / Notable decisions / Blockers / Next step. Predecessor handoff is the next phase's contract.

- Naming: `handoffs/PHASE_{N}.md` at the campaign / engagement / chain root (NOT in the skill folder — handoffs live with the work, not the spec).
- Required when the chain has 3+ phases AND can plausibly split across sessions (research-cycle, AEO loop, sales pipeline, outbound campaign). NOT required for single-skill or 2-phase chains.
- Handoff files are **operational state**, distinct from `WORKING.md` (per-role queue), `latest.md` (≤500-word delta cache), and `history.md` (append-only ops record). The four mechanisms compose; handoffs cover the per-phase-of-a-chain gap that the others don't fill.
- Skill body should reference the convention and link the template:

```markdown
## Handoff

This skill is Phase {N} of {chain-name}. On exit, write `handoffs/PHASE_{N}.md` with: Status / Inputs read / Outputs written / Gates passed / Notable decisions / Blockers / Next step. Phase {N+1} reads this on entry.
```

A reusable template lives at the chain root once the convention is adopted (don't pre-create empty handoff folders for skills that don't need them).

**If this skill is a HIGH-STAKES SKILL** (`review_gate: 3` or `4`, OR client-deliverable, OR strategic/locked-down output):

Adopt the **worked-example convention**. /steal'd from `Andytoizer/agentoperator-outbound-engine` (2026-05-05; cite-only) — see [`.claude/discovery/0526-agentoperator-outbound-engine-steal-analysis.md`](../../discovery/0526-agentoperator-outbound-engine-steal-analysis.md) (P3).

Ship at least one anonymised real prior run as `references/examples/{MMYY}-{anonymised-context}.md` alongside the SKILL.md. Distinct from `_schema/output-templates/` (which are skeletal): a worked example is a real artifact with real shape, anonymised for client confidentiality.

- **Required for new high-stakes skills**: positioning / messaging / win-loss / client-discovery / content-strategy / outreach-emails / proposal / pricing-strategy / brand-kit / icp-research / icp-behavioural / battlecards / sales-deck.
- **Not retroactive**: existing skills aren't required to backfill, but doing so is high-leverage when a new client onboards to a skill they've never used (see Roxanne onboarding to /positioning case in the steal analysis).
- **Anonymisation rule**: replace client name + verbatim brand language with a structurally similar substitute. Don't anonymise so heavily that the example loses its shape — the point is to show what good output looks like in the wild, not to teach via abstract template.

Worked examples live in `references/examples/` so they ship with the skill and don't pollute client folders. The example file should carry a one-line provenance note ("Derived from {client} engagement {MMYY}; anonymised; original retained at `{client-folder-path}` for retrieval").

### Step 6 — Validate before commit

Run locally before `git add`:

```bash
# Schema validation
python3 .claude/skills/_schema/validate-frontmatter.py path/to/new/SKILL.md

# Chain integrity (run for the whole tree, not just one file)
bash .claude/skills/meta/catalog/skill-catalog/scripts/chain-lint.sh

# Body cap
wc -l path/to/new/SKILL.md  # Should be ≤300
```

The validator's "WARN (design-contract)" output is informational — it does not block commits but flags drift early. Fix warnings before merge.

### Step 7 — Commit (auto-sync handles the rest)

`git commit` triggers `.claude/hooks/pre-commit.sh`, which:

1. Runs `validate-frontmatter.py` on changed SKILL.md files
2. Runs `chain-lint.py`
3. Runs `regenerate-catalog.py` (auto-syncs the catalog body)
4. Runs `regenerate-role-agents.py` (auto-syncs role-agent owned-skills bodies)

If any step fails, fix the underlying issue and re-commit. **Do not bypass the hook with `--no-verify`** — the hook is the integrity gate.

---

## Phase 4 standards — quick checklist

Pin this somewhere visible while authoring:

- [ ] Frontmatter passes `validate-frontmatter.py` (all 15 required fields)
- [ ] `name` equals parent folder name
- [ ] `description` ≥80 chars and includes triggers + upstream + downstream + anti-triggers
- [ ] `primitive` and `sub_primitive` from the enum
- [ ] `ontology_type` from `.claude/rules/ontology.md`
- [ ] `inputs.required` mirrors `depends_on`; `outputs[].feeds_into` mirrors `feeds_into`
- [ ] `owned_by_agent` resolves to a `.claude/agents/{role}.md` file
- [ ] Body ≤300 lines (heavy material in `references/{topic}.md`)
- [ ] `slim_exemption` not set (default — only set as last resort)
- [ ] Chain-lint passes (no broken edges, no orphans, no role-agent reciprocity violations)
- [ ] Pre-commit hook runs cleanly

## Design-output skill checklist (additional)

If `primitive: design` / `website` / `content`+motion:

- [ ] `inputs.recommended` includes `brand-kit`
- [ ] Body includes "Design cycle (post-authoring phases)" section
- [ ] Body explicitly references `/design-reviewer` as the final ship gate
- [ ] Cheat-sheet row added to `.claude/rules/design-production.md`
- [ ] Token-cite discipline documented (no hardcoded hex / fonts / radii in produced output)
- [ ] Apache-2.0 attribution if importing from `design-reviewer/references/`
- [ ] Validator's "WARN (design-contract)" output clean

## Analytical / data-verdict skill checklist (additional)

If the skill scores / ranks / declares a winner from counts:

- [ ] Body binds `quantitative-evidence-floors.md` — verdicts carry the volume floor + "too early" caveat below it
- [ ] Output Format section is explicit; recurring deliverables ship a literal comparable template
- [ ] Output synthesizes (judgment + the 2–3 driving numbers), never dumps raw rows

---

## When the runbook itself updates

This file is the single source of truth for authoring discipline. Updates land here when:

- A new Phase ships (Phase 6+ rules → add to this runbook)
- A new Companion hook ships (link to it from Step 5)
- A new rule file is added under `.claude/rules/` (link to it from Step 5)
- A new authorship contract emerges (e.g., the copywriting contract — `check_copywriting_contract` per `.claude/rules/persuasion-and-stickiness.md`, a content-quality contract analogous to the design-quality contract)

**Propagation discipline:** when authoring future skills, this file is *always* the starting reference. Skill-creator (Anthropic-shipped or Genesys-equivalent) should be invoked with the prompt: *"Author this skill per `.claude/skills/_schema/AUTHORING.md`."* That single sentence pulls in every current rule.

---

## Source files (kept up-to-date by their owners; this runbook references)

- Schema: `.claude/skills/_schema/skill-frontmatter.schema.json`
- Template: `.claude/skills/_schema/SKILL.template.md`
- Validator: `.claude/skills/_schema/validate-frontmatter.py`
- Chain-lint: `.claude/skills/meta/catalog/skill-catalog/scripts/chain-lint.py`
- Catalog regenerator: `.claude/skills/meta/catalog/skill-catalog/scripts/regenerate-catalog.py`
- Role-agent regenerator: `.claude/skills/meta/catalog/skill-catalog/scripts/regenerate-role-agents.py`
- Pre-commit hook: `.claude/hooks/pre-commit.sh`
- Companion hooks: `.claude/hooks/{mcp-credit-gate.sh,stale-context-warning.py,output-routing-check.sh,subagent-telemetry.sh}`
- Ontology: `.claude/rules/ontology.md`
- Design contract: `.claude/rules/design-production.md` § "Skill authorship contract"
- Design-quality library: `.claude/skills/meta/catalog/design-reviewer/references/`
- MCP credit rules: `.claude/rules/apollo-credits.md`
- Client folder routing: `.claude/rules/consulting-clients.md`

If any of these change, the change propagates here automatically (via reference). Re-read this file at the start of every new skill authoring session.
