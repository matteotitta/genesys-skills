---
name: help-center
version: "1.0"
last_updated: 2026-05-06
author: genesys-growth
description: |
  Generates Intercom-bound help-center / knowledge-base articles for tech products
  organized by researched canonical collection taxonomy (getting-started, account,
  integrations, settings, advanced, troubleshooting, etc.). Produces a persona ×
  collection × article matrix per product, with markdown bodies + screenshot
  placeholders, plus a one-shot Intercom Articles API JSON export. Triggers on
  "help center", "knowledge base", "user documentation", "Intercom articles",
  "product docs", "FAQ articles". NOT for marketing/SEO content (use aeo-content
  or website-copy) and NOT for onboarding emails (use email-nurture or
  lifecycle-marketing — but help-center articles are the link target those emails
  point to).
goal: Produce a complete persona × collection × article matrix of Intercom-ready help-center articles for one product, scoped per persona, exported as both markdown and JSON.
outcome: A locked artifact tree per product (collections/, intercom-import.json) the client's CX team imports into Intercom. Closes the activation lifecycle by giving onboarding emails their canonical link target.
primitive: lifecycle
sub_primitive: null
ontology_type: help-center-article
review_gate: 3
inputs:
  required:
    - product-messaging
  recommended:
    - positioning
    - tov-guidelines
    - icp-behavioural
    - transcript-analysis
    - brand-kit
depends_on:
  - product-messaging
owned_by_agent: growth
mcps_used:
  - exa
  - firecrawl
triggers:
  slash_commands:
    - /help-center
  natural_language:
    - "help center"
    - "knowledge base"
    - "Intercom articles"
    - "user documentation"
    - "product docs"
    - "FAQ articles"
    - "support center"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# Help Center

Produce Intercom-ready help-center / knowledge-base articles for one product, organized by a researched canonical collection taxonomy and scoped per user persona. The output is the canonical link target that onboarding emails, in-product tooltips, and Intercom Fin AI agents reference.

The taxonomy (which collections to include) is **researched and codified** — see the premium reference. The skill picks from a 12-module library based on product shape; it does not invent collections at runtime.

For the full template library by collection → the premium reference. For Intercom-native voice + structure rules → the premium reference. For persona scoping → the premium reference. For the JSON export schema + script → the premium reference.

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`doc-output-structure.md`](../../../../rules/doc-output-structure.md) — GDoc/Notion structural defaults
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]] (canonical R7 + R8 implementation)

**Refinements applied to this skill (the R7 + R8 canonical implementation):**

| Code | Refinement | How it lands in help-center |
|---|---|---|
| **R1** | Source placement (three layers) | KB articles are **end-customer-facing**. **No sources block.** Source dataset (product PRDs, transcripts, win-loss) lives in working doc only. The article IS the surface. |
| **R3** | Product-update tone | Capability framing — "[Product] does X" not "we are thrilled to introduce X." Even on launch-day articles. |
| **R6** | CTA hierarchy | Educational overviews → sign-up at the close for prospects; product-action CTA for existing users. How-to articles → product-action only (user is in-product). |
| **R7** | FAQ titles + two types + no sources block | **Two article types only.** Educational overviews (~500-800 words, FAQ titles: "What is [Product]?" / "What does [Product] do?"). Quick how-tos (≤4 bullets max, FAQ titles: "How to [task]"). Pattern: "How to issue virtual card" (right) vs "Issue your first virtual card in two minutes" (wrong). Sequential steps use numbered lists (1. 2. 3.), not dash-bullets. No sources block ever. |
| **R8** | Entity-name headings | Section headings repeat the product name — "What [Product] does," "Who [Product] is for," "How [Product] is different." Pronoun headings ("What it does") disappear in skim-reading; entity headings surface. |
| **R9** | Action-oriented section names | "How to start with [Product]" beats "Getting Started." "How to set up [Feature]" beats "Setup guide." |

---

## Claude Code triggers

**Invoke this skill when user says:**

- "Build a help center for {product}"
- "Generate KB articles"
- "Create Intercom articles for {product}"
- "Write product documentation for {persona}"
- "Build the FAQ library for {product}"

**Do NOT use this skill for:**

- Marketing blog content → use `/aeo-content`
- Landing-page or website copy → use `/website-copy`
- Onboarding emails → use `/email-nurture` (KB articles are the link targets, not the emails themselves)
- Internal SOPs / runbooks → use `/runbook`

---

## Inputs

**Required:**

- `product-messaging` output for this product (capabilities → article 01 in getting-started, value-props → article 02, status-quo alternatives → benefit framing). If absent, the skill blocks.

**Recommended (degraded but functional without):**

- `positioning` — anchors article voice + the "why this product exists" framing
- `tov-guidelines` — applies house writing rules; for ClientCo this means "no em dashes" etc.
- `transcript-analysis` — surfaces real user language for opening hooks AND surfaces recurring issues that warrant a `troubleshooting` collection.
- `brand-kit` — DESIGN tokens for any custom callout styling on the Intercom side (post-v1.0).

**Per-run runtime inputs (the user provides at invocation):**

- `product` slug — e.g. `report-generator`
- `screenshots/` folder path (recommended) — UI screenshots referenced by `{{screenshot:filename.png}}` placeholders in article bodies
- `additional_transcripts/` path (optional) — raw Granola/Zoom transcripts of customer calls or product walkthroughs to mine for language and screen-by-screen flow

---

## Process

The skill executes in 5 phases. Phases 1–3 run with you in the loop (taxonomy + matrix approval); phase 4 fans out via the approval-loop pattern; phase 5 exports.

### Phase 1 — Taxonomy selection (which collections to include)

Read inputs. Run the 6-question product-shape interview from the premium reference → derives which Tier-2 and Tier-3 modules to include. `getting-started` is always present.

Produce `00-taxonomy.md` listing selected collections, the trigger-justification per collection, and any modules explicitly excluded with reasoning. **You review and approve before phase 2.**

### Phase 2 — Persona scoping

Read `icp-behavioural` (or run mini-interview per the premium reference). Decompose buyer personas into **user personas** (admin / end-user / integrator are the canonical three; the persona scoping doc shows when to add more).

Map each user persona to which collections they need:
- Admin persona → `account-and-profile`, `settings-and-configuration`, `admin-sso-user-management`, `billing-and-plans`, `integrations` (admin views)
- End-user persona → `getting-started`, `advanced-workflows`, `troubleshooting`
- Integrator/developer persona → `developer-api`, `integrations` (technical views)

Produce `00-article-matrix.md` listing every (persona, collection, article) cell to be generated. **You review and approve before phase 3.**

### Phase 3 — Per-cell article tuning (approval-loop pattern)

Per [`.claude/rules/approval-loop-pattern.md`](../../../../rules/approval-loop-pattern.md): pick one representative cell from the matrix (highest-stakes; usually the `getting-started` × end-user × `setup` article). Generate it using the matching template from the premium reference. Show you the result. Edit prompt; regenerate. Two consecutive zero-correction rounds = locked tuning prompt.

### Phase 4 — Fan-out generation

Apply the locked prompt across the remaining cells in the matrix via parallel sub-agents (Agent tool, multiple invocations in one message). Batch size: 5 cells per Agent call. Each cell produces one markdown file at `collections/{collection}/personas/{persona-slug}/{NN}-{article-type}.md`.

**Each per-cell generation must explicitly pull from FOUR client sources** (not optional — these are the inputs that adapt the article to the client's voice and substance):

| Source | What the article pulls | Where it lands in the article |
|---|---|---|
| `icp/{latest}-icp-research.md` | Persona-specific pain language, segment triggers, voice-of-customer phrases | Opening hook + benefits framing |
| `positioning/{latest}-positioning.md` | Primary anchor, replace-not-add framing, status-quo alternatives | Capabilities/benefits articles' "When to use vs not" sections |
| `messaging/{latest}-product-messaging.md` (unified) + per-product messaging files | Capabilities, value props, tagline, status-quo alternatives, proof points | Body claims, all capability/benefit assertions |
| `brand/{latest}-tov-analysis.md` | Sentence-length cap, vocabulary rules, third-vs-first-person rules, action-verb-first bullet rule, banned terms | Voice enforcement on EVERY sentence |

If any of these inputs are missing or stale (>90 days), the agent flags before generating instead of inventing. Per `.claude/rules/exa-protocol.md` confidence thresholds for execution outputs: ≥60% verified claims required.

Per [`.claude/rules/outbound-research-hygiene.md`](../../../../rules/outbound-research-hygiene.md) and the Genesys voice rules: each article must pass the **100 Posts Test for user-doc voice** — would this read authentically as one of 100 help articles, not as marketing copy? If "feels marketing-y," rewrite with second-person instructional voice and concrete UI references.

### Phase 5 — Intercom export

Run `python3 scripts/export-intercom.py` (per the premium reference) to walk `collections/` and emit `intercom-import.json` — one collections array, one articles array, parent-child references intact. Hand off to client CX team for Intercom Articles API import.

---

## Voice + brand binding

Before generating any article, read the client's `tov-guidelines` and `brand/` outputs. Apply:

- Per-client voice rules (e.g., ClientCo: no em dashes; ClientCo: brand name "ClientCo" one word; etc. — see client CLAUDE.md)
- Help-center voice baseline (instructional, second-person, scannable, scannable bullets, no jargon, link out to related articles in the same collection)
- Per [`.claude/rules/design-production.md`](../../../../rules/design-production.md), screenshots referenced by placeholder do NOT need design treatment in v1.0 — Intercom renders them as-is. Custom callout styling deferred to v1.1.

---

## Review gate

Gate 3 (deep review) — every article is external-facing user documentation. Your review checks:

1. **Voice fit** — passes 100 Posts Test for user-doc voice (not marketing-flavored)
2. **JTBD framing** — opening sentence answers "what task does this help me complete?"
3. **Persona-collection mapping** — admin content stays in admin collections; end-user content stays in user collections
4. **Screenshot placeholders** — every UI claim has a `{{screenshot:...}}` placeholder OR an explicit text walkthrough
5. **Internal linking** — each article links to ≥2 sibling articles in the same collection
6. **Meta description** — present, ≤140 chars, contains the article's primary keyword

If any check fails, push back to phase 4 for that cell.

---

## Integration with other skills

- **Upstream:** `product-messaging` (required). `positioning`, `tov-guidelines`, `icp-behavioural`, `transcript-analysis`, `brand-kit` (recommended).
- **Downstream:** `email-nurture` and `lifecycle` consume the published help-center URLs as link targets in onboarding sequences.
- **Pairs with:** `aeo-content` for SEO surface (different audience: prospects vs activated users).

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

