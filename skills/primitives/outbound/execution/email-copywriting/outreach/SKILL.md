---
name: outreach-emails
version: '2.0'
last_updated: 2026-01-16
author: genesys-growth
description: 'Writes personalized cold outreach and follow-up email sequences. Runs in three modes: single-email (one prospect,
  one-off), generator (build reusable campaign prompt template), and runner (batch-generate emails per CSV row using the campaign
  prompt). Produces multi-touch sequences with GTM gap analysis, value-first messaging, and clear CTAs. Consumes deepline-enrich
  for validated contact data and company-context for prospect intelligence. Triggered by "outreach email", "cold email", "follow-up
  sequence", "write a cold email", "prospect outreach", "build a campaign prompt", or "batch-generate emails from CSV". For
  campaign-scale outreach, run deepline-enrich first to validate emails before sending.'
goal: Writes personalized cold outreach and follow-up email sequences.
outcome: 'Writes personalized cold outreach and follow-up email sequences. Runs in three modes: single-email (one prospect,
  one-off), generator (build reusable campaign prompt template), and runner (batch-generate emails per CSV row using the campaign
  prompt). Produces multi-touch sequences with GTM gap...'
primitive: outbound
sub_primitive: email-copywriting
ontology_type: outreach-sequence
review_gate: 2
inputs:
  required:
  - lead-scoring
  - niche-signal-discovery
  recommended: []
- type: outreach-sequence
  feeds_into: []
depends_on:
- lead-scoring
- niche-signal-discovery
owned_by_agent: b2b-consultant
mcps_used:
- apollo-io
- deepline
- gdrive
- notion
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# Outreach Emails

Generate personalized outreach and follow-up emails for Genesys Growth that convert prospects into clients. Every email demonstrates operator expertise, references specific prospect context, and leads with value. Three modes: single-email (default), generator (build campaign prompt), runner (batch-generate from CSV).

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`outbound-research-hygiene.md`](../../../../../../rules/outbound-research-hygiene.md) — dated signals, no stale references, no prior-job hooks
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in outreach-emails |
|---|---|---|
| **R1** | Source placement (three layers) | Emails are **end-customer-facing**. **No sources block.** No `[VERIFIED:...]` tags in body, no footer "Sources:" list. Research citations live in the working draft for QA only; stripped before send. |
| **R3** | Product-update tone | When pitching a capability or update, frame as "we shipped X to address Y" — not "we are thrilled to announce." Applies to single-email and runner modes. |
| **R6** | CTA hierarchy | Cold/market-facing → sign-up or discovery-call primary. Blog as fallback for prospects not ready. Never both as primary. Warm follow-up to existing pipeline → product-action CTA. |
| **R9** | Action-oriented section names | Production-doc sections (Subject / Opener / Value / Proof / CTA / Sign-off) already verb-led. Preserve. Don't rename to status-oriented variants. |

## When to run

Trigger on: "write outreach email", "cold email", "follow-up email", "post-call follow-up", "outreach sequence", "warm intro", "referral email", "re-engagement email", "build a campaign prompt", "batch-generate emails from CSV". For campaign mode (5+ prospects against same ICP), see the premium reference.

Do NOT use for marketing/nurture emails (use `lifecycle-marketing`), LinkedIn content (use `linkedin-content`), client deliverable emails, or internal comms.

## Inputs

Required (at least one): prospect name/company, website URL, conversation notes, LinkedIn profile, or discovery call summary. Optional: referrer context, specific service interest, timeline/urgency. Auto-loaded: client CLAUDE.md voice section. Auto-fetched: Gmail threads, Drive proposals, Calendar history. Full input table + validation checklist in the premium reference.

**Recommended for cold mode (load-bearing for the connector-opener doctrine):**
- **Peer customer(s):** 1–2 named logos that Genesys (or the client) has worked with that are structurally similar to the prospect's company. Without this, the connector-opener falls back to generic "we work with similar firms" phrasing that tanks reply rates.
- **Wedge:** one sentence on why the engagement won — the workflow or capability that maps from peer customer to prospect.

If either is missing for cold mode, ask before drafting. Don't hand-wave.

For campaign-scale outreach, run `/deepline-enrich` first to validate emails (waterfall across 15+ providers). Single-prospect emails: Apollo MCP enrichment is sufficient.

## Steps

1. **Mode select.** Default single-email; switch to generator for campaigns (5+ prospects, same ICP); switch to runner when applying an existing prompt to a CSV. See the premium reference.
2. **Validate inputs** per the premium reference Input section. If missing, ask for prospect name/company; offer Gmail search.
3. **Phase 1 — Context gathering.** Gmail/Calendar/Drive search → relationship timeline → email type (cold/warm/post-discovery/proposal/re-engagement). Company research: site, pricing, about, funding, LinkedIn. Detail in the premium reference.
4. **Phase 2 — GTM gap analysis.** Assess against Genesys ICP fit (design test, PMM test, persona pages, launch test, founder LinkedIn). Find personalization hooks (funding, hiring, posts, launches, competitor moves). Apply recency rule: 0–4 weeks primary, 4–8 cautious, 8+ skip.
5. **Phase 3 — Drafting.** Select structure: **for cold-with-peer-customer apply the premium reference (6 structural beats + A/B Loom-vs-POC arm + locked voice rules)**; for post-discovery / re-engagement use templates in the premium reference. Lead with specific observation. First-person singular. Operator voice. No forbidden phrases (the premium reference). Apply `.claude/rules/outbound-research-hygiene.md` to every research-derived signal in the draft (no >12mo, no prior-job hooks, dated not "recently", current-company-state only, sourced numbers only). Verify word counts: cold 150 / post-discovery 250 / follow-up 100 / re-engagement 100. Generate 2–3 subject variants.
6. **Self-evaluate.** Specific opening? "I" not "we"? No forbidden phrases? Hook ≤4 weeks old? Mark gaps `[Need to verify: X]`.
7. **Quality gate** per the premium reference (content, evidence, format checklists + anti-hallucination guardrails).
8. **Format output** per the premium reference (relationship context, sources, subject options, email body, word count, personalization notes, "if they reply" thread, iteration prompts).
9. **Suggest chain.** Follow-up sequence (no response in N days), `/proposal` (positive response), `/company-context` (deeper research).
10. **If campaign mode:** generator outputs a prompt artifact to `{client}/sales/campaigns/{campaign-name}/`; runner takes prompt + CSV, validates per-row variables, applies quality gates per row, outputs batch with skip log. Full spec in the premium reference.

## What good looks like

### Evaluations

- Opens with specific observation (not generic intro)
- Under word limit for type (150 / 250 / 100 / 100)
- Single, clear, low-friction CTA
- First-person singular ("I" not "we") throughout
- No forbidden phrases ("hope this finds you", "touch base", "synergy", "circle back")
- Hook recent (≤4 weeks) — skip if stale
- Subject line specific, ≤50 characters
- All claims traceable to research or conversation; gaps marked `[Need to verify: X]`
- Relationship context accurate; personalization notes explain specificity

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
