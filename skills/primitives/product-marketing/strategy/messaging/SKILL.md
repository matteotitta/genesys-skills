---
name: product-messaging
version: '2.1'
last_updated: 2026-01-21
author: genesys-growth
description: Builds a 10-component messaging library from website and product research. Produces value propositions, key differentiators,
  taglines, CTA variants, and proof points organized into a messaging hierarchy. Triggers on "product messaging", "messaging
  library", "capabilities and benefits", "value props", or "messaging framework". Requires positioning as upstream input.
  Feeds into landing-page-copy, outreach-emails, sales-enablement, and linkedin-content. NOT for positioning strategy — use
  positioning instead.
goal: Builds a 10-component messaging library from website and product research.
outcome: Builds a 10-component messaging library from website and product research. Produces value propositions, key differentiators,
  taglines, CTA variants, and proof points organized into a messaging hierarchy. Triggers on "product messaging", "messaging
  library", "capabilities and benefits", "value...
primitive: product-marketing
sub_primitive: strategy
ontology_type: messaging
review_gate: 2
inputs:
  required: []
  recommended:
  - positioning
  - icp-behavioural
  - competitor-research
- type: product-messaging-library
  feeds_into:
  - website-copy
  - sales-enablement
  - linkedin-weekly-content
  - outreach-emails
  - product-launch
depends_on: []
- website-copy
- linkedin-weekly-content
- outreach-emails
- product-launch
- sales-enablement
owned_by_agent: pmm
mcps_used:
- gdrive
- notion
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
context: fork
effort: high
---

# Product messaging

Builds a 10-component messaging library from website and product research. Output ships as the source of truth for all downstream marketing assets — landing pages, sales enablement, LinkedIn content, outreach. Knowledge type: `messaging` (per `.claude/rules/ontology.md`); maturity: emergent → validated after team review → canonical when locked. Visual phase map → the premium reference.

## When to run

Invoke when the user asks for: `product messaging for [URL/company]`, `messaging library for [product]`, `extract messaging from [website]`, `product messaging framework`, `capabilities and benefits for [company]`, `what are [product]'s differentiators?`, `pain points and capabilities for [URL]`. Do **NOT** invoke for: competitor analysis only (use `/competitor-research`), landing page copy directly (use `/landing-page-copy` — run this first), ICP research only (use `/icp-behavioural`), or single-feature questions (answer directly without full framework).

**The Iron Law:** no messaging output without source verification. Every claim cites URL + access date or is marked `[Not available]`. Every quote is verbatim. Every consequence chain traces 1st→2nd→3rd order. Full guardrails + red flags + anti-hallucination rules → the premium reference.

## Inputs

**Required:**

- `website URL` — primary product website (verify it loads).
- `product name` — exact product/company name (confirm if ambiguous, e.g., "Bolt" could be ride-share, fintech, or `bolt.new`).

**Recommended (improve quality):**

- `target ICP context` — focuses messaging on relevant segments.
- `competitor context` — sharpens differentiators (use `/competitor-research` output if available).
- `internal docs` — provides claims not on website.
- `customer quotes` — fills gaps in testimonial coverage.

**Upstream skill outputs (if available, read first):**

- `positioning` (primary) — frames Description and core messaging blocks.
- `icp-behavioural` — enriches pain points and benefits with VoC data.
- `competitor-research` — sharpens status quo and differentiators.
- `tov-guidelines` — applies tone to messaging.

If website URL is missing, ask. If product name is ambiguous, confirm before starting.

## Steps

1. **Validate inputs** → verify URL accessible, product name confirmed, ICP context confirmed if not obvious. Pull upstream skill outputs (positioning, icp-behavioural, competitor-research) into context if available.
2. **Phase 1 — Discovery research** → the premium reference. Fetch core pages (homepage, features, pricing, customers, about — 5+ pages with URLs + access dates). Search external data (G2, testimonials, vs-pages) per Exa protocol (`.claude/rules/exa-protocol.md`). Extract branded feature names verbatim before structured extraction begins. Detailed search/scraping patterns → the premium reference.
3. **Phase 2 — Structured extraction** → the premium reference. Extract all 10 components in order: Description → Status quo & alternatives → Pain points (with consequence chains) → Capabilities → Functional benefits → Emotional & social benefits → Features (branded names) → Cost of inaction → Common objections → Core messaging blocks. Frameworks + descriptor counts + link graph → the premium reference.
4. **Phase 3 — Verification & gaps** → the premium reference. Source-verify every claim (URL + access date), confirm verbatim quotes, assign confidence levels (High/Medium/Low → `[VERIFIED]/[INFERRED]/[ESTIMATED]`), document data gaps + recommendations as Component 10.
5. **Apply attribution standards** → per `.claude/rules/ontology.md`: `[VERIFIED: source_type, reference]`, `[INFERRED: from X + Y]`, `[ESTIMATED: reasoning]`, `[UNAVAILABLE]`. Quality threshold for client-deliverable strategy outputs: ≥60% verified, ≤10% estimated.
6. **Self-evaluate against quality gates** → the premium reference. Run completeness, evidence-quality, and guardrail checks. Answer self-roast questions honestly.
7. **Write to client folder** per output template → the premium reference. File path: `messaging/MMYY-messaging.md` (or per client CLAUDE.md folder map). Header includes skill name, generated date, font (Inter), version.
8. **Push** to Notion (Product Messaging Database) and Google Docs (`client_folder/strategy/`) per push targets in frontmatter. For refresh runs, UPDATE existing pages rather than duplicating.
9. **Offer iteration prompts** post-delivery → the premium reference. If user signals approval ("great messaging" / quick approval), offer to save as a reference example under the premium reference.

## What good looks like

### Evaluations (binary pass/fail before declaring "done")

- All 10 components present in correct order (or explicit `[Not available]` per component with reason).
- Status quo includes Manual/DIY + at least one named competitive alternative.
- Every pain point has a complete 1st→2nd→3rd order consequence chain (not cut short).
- Every pain point links forward to a capability; every capability links to a branded feature name.
- Every functional benefit includes a verbatim customer quote or explicit "Not available" with reason.
- Emotional + social benefits section complete: 2 emotional + 2 social.
- Cost of inaction section quantified (daily/weekly/monthly cost stated, not abstract).
- Common objections section complete (3-5 objections with root cause + Acknowledge/Reframe/Evidence response).
- Core messaging blocks complete: tagline ≤7 words, elevator pitch (1 sentence), 3-bullet value prop, proof point, audience-segmented messages.
- Every claim has source URL + access date; every quote verbatim; confidence level assigned (High/Medium/Low → `[VERIFIED]/[INFERRED]/[ESTIMATED]`).
- ≥60% `[VERIFIED]` confidence; ≤10% `[ESTIMATED]` (per ontology threshold for client deliverables).
- Data gaps section non-empty if any component is incomplete or low-confidence; recommendations provided for filling each gap.
- Source appendix lists ALL referenced URLs with access dates.
- Output title is `# Product messaging library: [Product Name]` exactly — no aliases.

## Pre-slim original

Pre-slim SKILL.md (1,048 lines, v2.1) archived at `.claude/skills/_archive/messaging/SKILL-pre-slim-20260429.md`. See the premium reference ("Changelog") for the v2.2 entry documenting the slim.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
