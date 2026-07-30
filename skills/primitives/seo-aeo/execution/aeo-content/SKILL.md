---
name: aeo-content
version: '2.1'
last_updated: 2026-01-21
author: genesys-growth
description: Writes content optimized for AI citation by ChatGPT, Claude, and Perplexity using the CITABLE framework. Produces
  AEO-optimized articles with structured data, entity optimization, and citation-ready formatting. Triggered by "AEO", "AI
  SEO", "get cited by AI", "answer engine optimization", or "AI search content". Consumes aeo-strategy, landing-page-copy,
  product-messaging, and icp-behavioural as upstream context. Feeds into lifecycle-marketing for distribution. NOT for content
  strategy or keyword planning — use /aeo-strategy instead.
goal: Writes content optimized for AI citation by ChatGPT, Claude, and Perplexity using the CITABLE framework.
outcome: Writes content optimized for AI citation by ChatGPT, Claude, and Perplexity using the CITABLE framework. Produces
  AEO-optimized articles with structured data, entity optimization, and citation-ready formatting. Triggered by "AEO", "AI
  SEO", "get cited by AI", "answer engine optimization", or...
primitive: seo-aeo
sub_primitive: execution
ontology_type: aeo-content
review_gate: 3
inputs:
  required: []
  recommended:
  - aeo-strategy
  - website-copy
  - product-messaging
  - icp-behavioural
outputs:
- type: aeo-content
  feeds_into:
  - lifecycle-marketing
depends_on: []
feeds_into:
- lifecycle-marketing
owned_by_agent: content
mcps_used:
- ahrefs
- exa
- gdrive
push_targets:
- gdrive
- notion
- framer
triggers:
  slash_commands:
  - /aeo-content
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# AEO Content

Produce articles citation-worthy by ChatGPT, Claude, Perplexity, and Google AI Overviews using the CITABLE framework + retrieval-citation-trust pipeline. Two output modes: CITABLE block (800-1,500 words) for definition/FAQ/short BOFU pages, and authority long-form (2,000-4,000 words) for competitor comparisons, listicles, how-to guides, and industry guides. Review gate is Level 3 because output publishes externally under client domain.

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`doc-output-structure.md`](../../../../rules/doc-output-structure.md) — GDoc/Notion structural defaults (when published to either before site)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in aeo-content |
|---|---|---|
| **R1** | Source placement (three layers) | Published articles are **end-customer-facing**. **No "Sources" block on the rendered page** — citations live in working draft for QA only, then convert to inline links inside the prose at publish-time. The page itself never carries a sources block; that's an AI-citation tell. |
| **R3** | Product-update tone | Any product / feature mention frames as "[Product] does X" not "we are thrilled to announce [Product]." Even hero comparison pages stay even-keeled. |
| **R6** | CTA hierarchy | TOFU/MOFU articles (definition, FAQ, how-to, industry guide) → blog-CTA + sign-up secondary. BOFU articles (competitor comparison, listicle ending in vendor pick) → sign-up or trial primary. |
| **R7** | FAQ titles + no sources block | FAQ articles use canonical FAQ titles ("What is [X]?", "How does [X] work?", "How to [task]"). Never marketing-flavored variants ("X in 60 seconds," "The ultimate guide to X"). No sources block, two-types pattern (educational longer / how-to ≤4 bullets). |
| **R8** | Entity-name headings | Section headings repeat the entity name — "What [Product] does," "How [Product] is different" — not pronoun headings ("What it does"). Customers scan for the entity. |
| **R9** | Action-oriented section names | "How to set up [X]" beats "Setup." "Why [X] matters" beats "Importance." "How [X] compares to [Y]" beats "Comparison." |

## When to run

- After `aeo-strategy` produces an article queue (Mode B — title, keywords, cluster, funnel stage, mode supplied).
- Standalone for a single article (Mode A — user provides topic + 3+ target queries).
- After `landing-page-copy` finishes (auto-suggest: AEO content can extend a landing page into a citable hub).
- When user mentions: "AEO content", "answer engine optimization", "get cited by AI", "ChatGPT citations", "Perplexity visibility", "comparison/definition/how-to/FAQ page AEO", "refresh content for AI", "CITABLE framework". Full trigger and don't-invoke list: `references/auto-update-protocol.md`.

## Inputs

**Required:** topic/concept; 3+ target queries (primary + adjacent); company context (capabilities, differentiators).
**Mode B from `aeo-strategy` queue:** article title, target keywords, cluster, funnel stage, content mode — skip Phase 1.
**Optional (improve quality):** ICP research, competitor content, existing proof points, current page (for refresh), competitor research deep dives.
**Client context:** auto-loaded from client CLAUDE.md — apply Voice & Messaging rules, vocabulary, anchors automatically.
**Validation:** topic specific enough; ≥3 queries; company context available; mode determined. Full input matrix + validation checklist: `references/process.md`.

## Steps

1. **Validate inputs.** Confirm topic, queries, company context. If missing, ask user or offer Exa research per `.claude/rules/exa-protocol.md`.
2. **Phase 1.1 — Map queries to content type.** Use query pattern table in `references/output-modes.md` ("[X] vs [Y]" → comparison; "What is [X]" → definition; "How to [X]" → problem-solution; "FAQ" or multi-question → FAQ).
3. **Phase 1.2 — Identify 5-7 adjacent intents.** Patterns: What/How/Why/vs/best/examples. These become H2 sections.
4. **Phase 1.3 — Load template.** From `references/{type}.md` (`comparison-page.md`, `definition-page.md`, `problem-solution-guide.md`, `faq-page.md`, `authority-long-form.md`, `bofu-comparison.md`, `mofu-listicle.md`, `mofu-how-to.md`, `content-refresh.md`). Confirm structure with user.
5. **Phase 2 — Apply CITABLE (7 letters).** C: BLUF (40-80w) + key facts box (3-5 sourced); I: answer primary in first 100w + H2s for adjacent; T: 3+ third-party sources, G2/Capterra if relevant; A: 1-2 quotable facts/section, inline `[Source, Year]`; B: 200-400w sections, TL;DR, comparison tables (<10 rows), jump links if >1,500w; L: visible "Last updated: YYYY-MM-DD" + refresh schedule; E: relationship statements + schema plan. Per-letter deliverables: `references/frameworks.md`.
6. **Phase 3.1 — Add structural elements.** TL;DR box, ≥1 table, FAQ (5-10 questions), hub-and-spoke internal links, schema markup plan.
7. **Phase 3.2 — Apply citation-boost stack.** FAQ +40%, comparison table +30-40%, numbered list +25%, TL;DR +20%, key facts box +20%. Verify each present.
8. **Phase 3.3 — Generate schema.** JSON-LD for FAQPage/HowTo/Product. Validate schema matches visible content exactly (anti-hallucination rule 3).
9. **Self-evaluation gate.** All facts sourced? Citations real (URLs verified)? Schema matches visible? No invented stats/quotes/G2 ratings? If fail: use `[PLACEHOLDER]` or `[NEED TO VERIFY]`.
10. **Format output.** CITABLE block uses template in `references/output-format.md`; authority long-form uses templates directly. Inter font, sentence-case headers, [Source, Year] citations, max 10 row tables.
11. **Run pre-delivery checklist.** CITABLE audit + format quality + completeness — see `references/quality-gates.md`.
12. **Present at Review Gate 3** (deep review, external publication). Actions: [Approve] [Add sources] [Expand].
13. **Post-output: offer iteration prompts** (refinement, expansion, quality) — see `references/auto-update-protocol.md`.
14. **Capture learnings.** Log feedback signals; on user approval, save to `examples/[date]-[content-type].md` per the reference-capture format.
15. **Suggest chain.** → `lifecycle-marketing` (content feeds nurture), `landing-page-copy` (AEO enhances LPs), `competitor-research` (deeper comparison content).

Full phase-by-phase walkthrough with checkpoints + flowchart: `references/process.md`. Mode + content-type mapping (BOFU/MOFU/TOFU): `references/output-modes.md`.

## What good looks like

### References
- `references/frameworks.md` — CITABLE per-letter deliverables, retrieval-citation-trust pipeline, citation-impact stats (FAQ +40%, comparison table +30-40%, etc.).
- `references/output-modes.md` — CITABLE block vs authority long-form, mode comparison table, content-type → mode mapping, query-pattern → type table.
- `references/output-format.md` — CITABLE block markdown template (header, TL;DR, key facts, BLUF, H2s, FAQ, schema, metadata, iteration prompts), formatting rules.
- `references/process.md` — full Phase 1/2/3 flowchart, per-step deliverables, phase checkpoints, input modes (A standalone vs B from `aeo-strategy` queue).
- `references/quality-gates.md` — anti-hallucination guardrails (6 rules), pre-delivery checklist (CITABLE audit + format + completeness), gotchas, anti-examples.
- `references/auto-update-protocol.md` — feedback signal table, reference-capture format, pattern detection (3+ same feedback → update), iteration prompts, Claude Code triggers, Ahrefs MCP integration, MCP data inheritance, changelog.
- `references/examples.md` — worked examples (RevOps definition BLUF, HubSpot vs Salesforce TL;DR) + example index pointing to `examples/`.
- Template library (`references/`): `comparison-page.md`, `definition-page.md`, `problem-solution-guide.md`, `faq-page.md`, `content-refresh.md`, `authority-long-form.md`, `bofu-comparison.md`, `mofu-listicle.md`, `mofu-how-to.md`.
- Research substrate: Exa per `.claude/rules/exa-protocol.md` — `web_search_exa` + `find_similar_links_exa` for citation gap research per article. Citation: `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]`.

### Examples
- `examples/example-comparison-page.md` — full worked output (Complete).
- Pending captures: example-definition-page, example-how-to-guide, example-bofu-comparison, example-mofu-listicle. Promote on user approval per `auto-update-protocol.md`.

### Evaluations
- BLUF ≤100 words and answers primary query directly?
- Key facts box has 3-5 data points each with `[Source, Year]`?
- H2s cover 5-7 adjacent intents (not just primary)?
- Every section has 1-2 quotable facts with inline citations?
- ≥1 comparison table AND ≥1 numbered list present?
- FAQ has 5+ self-contained answers (40-60w direct + 100-200w expanded)?
- "Last updated: YYYY-MM-DD" timestamp visible at top?
- Schema JSON-LD matches visible content exactly (no hidden info)?
- Hub-and-spoke internal links identified?
- Zero invented stats/quotes/G2 ratings (all sources verifiable or marked `[PLACEHOLDER]`/`[NEED TO VERIFY]`)?
- Output header includes skill name, date, font (Inter), version, content type?
- Citations use inline `[Source, Year]` format consistently?
- TL;DR matches mode (bullet list for CITABLE block, blockquote paragraph for authority long-form)?
- Refresh schedule defined and content-type-appropriate?

## Push

- Save output to `client_folder/execution/aeo-content/` (Google Docs export per `.claude/rules/gdrive-protocol.md` — `create-doc-unified.mjs --client {slug}`).
- Optional pushes: Framer draft page; Notion Content Database.
- Append entry to client `history.md` ("ran /aeo-content for {topic} — gate 3 approved YYYY-MM-DD").
- Update client `latest.md` with current article in queue + next.
- On user approval, save to `examples/[date]-[content-type].md` and update reference index.
- Suggest chain: → `lifecycle-marketing` (distribution), → `landing-page-copy` (AEO enhances LP), → `competitor-research` (deeper BOFU comparisons).

---

## Sourced patterns — comparison page architecture

<!-- Sourced from coreyhaines31/marketingskills/competitors/SKILL.md (MIT) — accessed 2026-05-17. Imported via /steal I11. -->

For comparison / alternative / "vs." pages (alt page format, plural alternatives format, you-vs-competitor format, competitor-vs-competitor format):

- **"Honesty Builds Trust" pattern.** Acknowledge competitor strengths and your own limitations explicitly. Reads as referee, not biased advocate. Trust-as-conversion.
- **"Who it's for" sections per option.** On a plural alternatives page (e.g., "Best alternatives to X"), each listed alternative gets a "Who it's for" block — explicit ICP fit per option. Helps evaluators self-select; converts at higher rate than positioning-against-all.
- **4–7 genuine alternatives on plural pages.** Fewer reads as biased; more reads as overwhelming. The 4–7 range optimizes for "this is helpful" perception.
- **TL;DR-then-depth hierarchy.** Lead each option with a 1-sentence summary; follow with paragraph-level depth. Scanners take the TL;DR; deep readers go further.
- **Modular centralized competitor data.** Don't hardcode competitor facts per page — maintain a `references/competitors.json` (or equivalent) so refreshes update one source. The alt / vs / plural pages all read from it.
- **Conversion benchmark per source:** comparison / alternative pages convert at 5–15% vs. 0.5–2% for generic content. The format earns its place when the cluster exists.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Then run `/voice-reviewer` — the content ship gate: voice + brand quality (pm-loop.md § lens-reviewer).

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
