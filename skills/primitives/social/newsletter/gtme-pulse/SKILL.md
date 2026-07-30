---
name: gtme-pulse
version: '2.6'
last_updated: 2026-07-17
author: genesys-growth
description: 'Writes complete GTM Engineer Pulse newsletter editions from curated links. Produces Substack-ready content with
  intro synthesis, categorized link summaries (Recent News, Hot Takes, Jobs), and closing commentary matching the established
  Pulse voice. Triggers: "Pulse newsletter", "GTM Pulse", "newsletter edition", "write the Pulse", "here are the links for
  this week". NOT for the Genesys Growth newsletter — use skill-of-the-week for that. NOT for content strategy — use content-strategy
  instead.'
goal: Writes complete GTM Engineer Pulse newsletter editions from curated links.
outcome: 'Writes complete GTM Engineer Pulse newsletter editions from curated links. Produces Substack-ready content with
  intro synthesis, categorized link summaries (Recent News, Hot Takes, Jobs), and closing commentary matching the established
  Pulse voice. Triggers: "Pulse newsletter", "GTM Pulse",...'
primitive: social
sub_primitive: newsletter
ontology_type: newsletter
review_gate: 2
inputs:
  required: []
  recommended: []
outputs:
- type: newsletter
  feeds_into: []
depends_on: []
feeds_into: []
owned_by_agent: operator
mcps_used:
- exa
- gdrive
push_targets:
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
effort: high
---

# GTM Engineer Pulse

Generate complete editions of the GTM Engineer Pulse newsletter — the weekly briefing on go-to-market engineering, AI, and revenue systems. User provides categorized links; output is a polished, Substack-ready newsletter matching the established voice and structure.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]. Cohort framing per [[feedback_gtme_pulse_conventions]] (Cohort 5 current).

**Refinements applied:** R1 (newsletter is end-customer-facing — sources convert to inline links in prose; no appended sources block), R2 (multi-section newsletter ships as one doc with toggles per section type), R3 (commentary capability-led, never "thrilled"), R5 (Pulse's own thread-anchor opens every section), R6 (cohort enrollment primary CTA per cohort-conventions memory), R9 (verb-led section headings).

---

## When to invoke

**Yes:** "Create a new Pulse edition", "Write GTM Engineer Pulse #[X]", "Generate the Pulse newsletter", "Help me with the GTME Pulse", "/gtme-pulse"

**No:** general LinkedIn content → `linkedin-content`. Job board management only → handle directly. Edit existing edition → handle as direct edit task.

Full trigger detail + edge cases → `references/inputs.md`.

---

## Inputs (minimum)

User must provide:
- Edition number, publication date
- Recent News (4-5 URLs), LinkedIn Hot Takes (5-7 URLs), GTME Jobs (5-10 URLs), Top GTMEs (4-5 LinkedIn profiles), Recommended Resources (5-8 URLs)
- Optional: theme, cohort CTA status (`active` | `waitlist` | `none`), cohort number, cohort start month + enrollment deadline, cohort link, special announcement, spots remaining (only if Matteo gives a real current number — never inferred)

If counts are below minimum, ask for more before proceeding. Full table + format spec → `references/inputs.md`.

---

## Process — three phases

### Phase 1 — fetch
Parse input → categorize links → fetch LinkedIn posts via Apify (`supreme_coder~linkedin-post`) → fetch profiles via Apify (`harvestapi~linkedin-profile-scraper`) → fetch other URLs via WebFetch → supplement profiles with WebSearch for generalized bios.

API token: `api-keys/.env` → `APIFY_API_TOKEN`. Full curl commands + extraction-per-section spec → `references/steps/phase-1-fetch.md`.

### Phase 2 — generate
Write intro (multiple paragraphs, each 2-3 sentences, casual, reference highlights) → Recent News (bold linked headline + body inline, ONE paragraph of 2-3 sentences, NO line breaks within the bullet) → LinkedIn Hot Takes (link on headline NOT author, same one-paragraph 2-3 sentence rule) → GTME Jobs (`**[Role @ Company](url)** | salary | location — body of 2-3 sentences inline, NO line break between meta-line and body`) → Top GTMEs (`**[Name](url)** — Role @ Company. Bio sentence + last-30-days post activity sentence(s), 2-3 sentences total, ONE paragraph, NO "Follow for X" closer`) → Recommended Resources (`**[Title](url)** by Author (context). Body of 2-3 sentences inline, ONE paragraph`).

**Hard rules every section follows:**
- **Every bullet body is ONE paragraph of 2-3 sentences.** No line breaks within a bullet. No indented sub-paragraphs. If a topic needs more depth, condense or split into a separate bullet.
- **No `**` (bold) inside the body paragraph.** The bold-link headline at the start is fine; nothing else in the body gets bold for emphasis. Use italics with single `*` for quotes/titles only.
- **No "pairs with X" phrasing.** If the pairing is real, state the parallel directly without the meta-commentary. Most of the time, just say the thing.
- **Full conversational sentences, no abrupt sentence changes.** Connect clauses with commas, em-dashes, or semicolons so the paragraph flows as one thought. No fragment punchlines.
- **Strip AI-speak before shipping.** The "AI-speak phrases — never use" block in `references/voice-guidelines.md` is the canonical blocklist. Replace meta-commentary phrases ("the strategic read is", "the operator-canonical reading", "pairs directly with X — different angles on the same compound thesis") with the actual statement.
- **Sound like Matteo.** Direct, operator-first, contractions ("you're", "it's", "won't"), em-dashes with spaces, sentence case headers. The 100 Posts Test is the final check.

**Top GTMEs section — special rule:** instead of a generic "Follow for X" closer, mention something from the person's last 30 days of LinkedIn activity if active; if inactive, pull a freshness angle from their profile (latest role change, headline, current company traction). The bio should ground in their lineage; the closer should ground in what they're doing NOW.

Per-section instructions → `references/steps/phase-2-generate.md`. Templates with link rules → `references/section-elements.md`. Voice rules → `references/voice-guidelines.md`. Section-level templates → `references/section-templates.md`.

### Phase 3 — assemble + polish
GDrive manifest line (auto, line 1) → sections (NO editor-notes HTML comment block — strip if present from prior edits) → closing ("Keep shipping, Matteo") → image suggestions (2-3, single-line each, no headshot grids unless the bullet has a real reason) → format polish (em dashes with spaces, bullets `-`, sentence case, link spans full title) → 2 Cialdini-powered CTAs (mid + end).

Detailed steps → `references/steps/phase-3-assemble.md`. Cialdini CTA templates → `references/section-elements.md`. Output structure → `references/output-format.md`. Process flowchart → `references/process-flowchart.md`.

### Phase 4 — asset bundle (REQUIRED)
Download GTME Jobs company logos (logo.dev) + Top GTMEs LinkedIn headshots (Apify) for the edition. Output to `~/Downloads/pulse-{N}-assets/` with subfolders `logos/` and `headshots/`, plus a `manifest.md`. Run before Phase 5 follow-ups so assets are ready when the GDoc / Substack publish step fires.

**Coverage scope (narrow, deliberate):**
- **Logos:** the 5 hiring companies in GTME Jobs only. NOT Recent News, NOT MCP-of-the-week, NOT Hot Take authors' employers, NOT Top GTMEs' employers, NOT Resources publications. The Jobs companies anchor a section the reader scans for visual recognition; everything else carries on link + headline alone.
- **Headshots:** the 4 Top GTMEs to Follow only. NOT the 5 Hot Take authors. Top GTMEs is the only section where the person IS the subject and a face accelerates recognition.

**Hit rate from Pulse #30:** 5/5 logos via logo.dev + 4/4 headshots via Apify `apimaestro/linkedin-profile-batch-scraper-no-cookies-required` ($0.02 total spend, under the apify-credits no-gate threshold).

Full procedure → `references/steps/phase-4-assets.md`.

---

## Critical guardrails (do not violate)

1. **Link matching** — re-read original input, checklist every URL, match each to its section. Common miss: official blog links, podcast/Spotify, LinkedIn buried in long lists.
2. **Inline link formatting** — link MUST span the ENTIRE title text. `**[Title](url)**` not `**Tit[le](url)**`. Google Docs export breaks if partial.
3. **Profile research** — Apify alone is insufficient. Pair with WebSearch `"[Name]" [Company] background` for generalized bios. Never write "in their latest post about…".
4. **Job format** — `**[Role @ Company](url)**` | Salary | Location. Link spans full role-at-company text.
5. **CTA requirements** — exactly 2 Cialdini-powered CTAs (mid after Jobs header, end before "Keep shipping"). Each uses ≥2 of: social proof, authority, scarcity, concrete. **Every lever must be TRUE** — scarcity is the real deadline and cohort start date, never a spot count or percentage-filled nothing can source. A fabricated number is rule 7 + anti-hallucination #1, not persuasion.
6. **Hyphens `-` for body list items** — not `•`, not `→`. Applies to ALL body items including CTA action links and job board link. One carve-out: the LinkedIn promo block uses `•` (plain text, LinkedIn renders no markdown).
7. **News source verification** — never write a summary from fallback web search if the source URL failed to fetch. Flag the failed URL; never fabricate.

Plus 7 anti-hallucination rules: never invent metrics, fabricate quotes, guess salary, assume titles, invent expertise. Mark missing as `[Not available]`. Full guardrails + per-rule examples + pre-delivery quality checklist → `references/guardrails.md`.

---

## Output structure

```markdown
<!-- GTM Engineer Pulse #[X] · Generated: [date] · Author: Matteo Tittarelli · Font: Inter -->

# The GTM Engineer Pulse | #[X]

**SEO title:** [<60 chars]
**Meta description:** [<155 chars]

[Intro paragraph]

---

## Recent News        [4-5 items]
## LinkedIn Hot Takes [5-7 items]
## GTME Jobs          [Cohort CTA if active] [5-10 items] • Check our full job board: [gtm-engineer-jobs.com](...)
## Top GTMEs to Follow [4-5 profiles]
## Recommended Resources [5-8 items]

Keep shipping,
Matteo

## Recommended Images to Add [3-5 items]
```

Full structure with separators + formatting rules table → `references/output-format.md`. Section-level good/bad examples → `references/what-good-looks-like.md`. Full reference editions → `examples/pulse-14-example.md`, `examples/pulse-15-reference.md`.

---

## Required follow-ups

After approval:

1. **LinkedIn promo post** — REQUIRED. Template + 12 rules → `examples/linkedin-promo-template.md`. Real reference → `examples/pulse-20-linkedin-promo.md`.
2. **Publish — Notion + Substack draft (default since #32)** — create the Notion page (sibling of previous edition, manifest line added to local md) and stage the Substack draft via Claude in Chrome: title `The GTM Engineer Pulse | #N`, subtitle = meta description, body via synthetic HTML paste into the Tiptap editor, then the 4 CTA elements (2 blockquoted cohort CTAs + 2 native `subscribeWidget` nodes). Full procedure → `references/substack-publish.md`. Legacy GDoc path: `create-pulse.mjs` (NOT `create-doc-unified.mjs`) → `references/google-docs-export.md`.
3. **Self-improvement loop** — REQUIRED. Ask user the 4 capture questions (what worked, what to fix, new guardrails, new examples). Full prompt + auto-capture triggers + pattern detection → `references/self-improvement-loop.md`.

Iteration prompts (refine / expand / quality) → `references/iteration-prompts.md`.

---

## Research substrate (Exa)

**Default:** Exa, per `.claude/rules/exa-protocol.md`. **Primary tools:** `web_search_exa` (date-filtered for "recent" claims) and the plugin `/search` slash command for parallel topic deep-dives. **Fallback:** WebSearch with data-gap flag.

Use case: weekly news sweep with date filter; profile background supplementation; resource fact-check. Plugin namespace `mcp__plugin_exa_exa__*` preferred; legacy `mcp__exa__*` still mounted. Citation: `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]`. Quality gate: ≥3 sources per major claim, ≥50% `[VERIFIED]`, no silent WebSearch fallback.

Worked examples + full tool catalog → `.claude/skills/meta-skills/exa/`.

---

## MCP integration

| Source | What | Tool | When |
|--------|------|------|------|
| **Exa** | Newsletter topic research, profile background | `web_search_exa` | Always |
| **Apify** | LinkedIn posts + profiles | `atomus~linkedin-reactions-scraper-pro` (post-details mode), `harvestapi~linkedin-profile-posts` | When URLs are LinkedIn (`supreme_coder~linkedin-post` is BROKEN since ~June 2026) |
| **WebFetch** | Job boards, blogs, Substack, YouTube | built-in | Non-LinkedIn URLs |

**Fallback (no MCP):** WebSearch for GTM topics; user-provided topic list.

---

## Skill chain

| Skill | Relationship | Usage |
| ----- | ------------ | ----- |
| `linkedin-content` | Related | Standalone LinkedIn posts (not newsletter hot takes) |
| `outreach-emails` | Complementary | GTM Engineer School promotion emails |
| `aeo-content` | Complementary | Newsletter archive SEO optimization |

---

## References

| File | Purpose |
| ---- | ------- |
| `references/process-flowchart.md` | Full pipeline visualization |
| `references/inputs.md` | Required + optional inputs, validation, triggers |
| `references/steps/phase-1-fetch.md` | Phase 1 detailed steps + Apify curl |
| `references/steps/phase-2-generate.md` | Phase 2 detailed steps |
| `references/steps/phase-3-assemble.md` | Phase 3 detailed steps |
| `references/steps/phase-4-assets.md` | Phase 4 detailed steps + Clearbit curl loop + Exa LinkedIn headshot extraction |
| `references/section-templates.md` | Per-section templates (legacy depth) |
| `references/section-elements.md` | Section templates with link rules + Cialdini CTAs |
| `references/voice-guidelines.md` | Voice attributes, formatting, anti-patterns, 100 Posts Test |
| `references/output-format.md` | Full output structure + formatting rules |
| `references/guardrails.md` | 7 critical guardrails + 7 anti-hallucination rules + quality checklist |
| `references/what-good-looks-like.md` | Section-level good/bad examples |
| `references/iteration-prompts.md` | Refine / expand / quality prompts |
| `references/self-improvement-loop.md` | Capture questions, auto-triggers, pattern detection |
| `references/substack-publish.md` | Notion + Substack-via-Chrome publish pipeline + CTA widget insertion (default since #32) |
| `references/google-docs-export.md` | create-pulse.mjs procedure + format table (legacy path) |
| `references/changelog.md` | Version history (1.0 → 2.5) |
| `examples/pulse-14-example.md` | Reference edition #14 (voice/format) |
| `examples/pulse-15-reference.md` | Reference edition #15 (all v2.0 guardrails) |
| `examples/linkedin-promo-template.md` | LinkedIn promo template + 12 rules |
| `examples/pulse-20-linkedin-promo.md` | Pulse #20 LinkedIn promo (real reference) |
| `output/create-pulse-15.js` | docx-js template (local Word export) |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Then run `/voice-reviewer` — the content ship gate: voice + brand quality (pm-loop.md § lens-reviewer). The LinkedIn readability dimension is N/A for the Pulse body and fires on the promo post.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
