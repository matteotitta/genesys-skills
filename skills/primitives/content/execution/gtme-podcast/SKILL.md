---
name: gtme-podcast
version: '1.2'
last_updated: 2026-05-25
author: genesys-growth
description: 'Turns a GTM Engineer School podcast transcript into four artifacts bundled into one branded Notion page for review
  and copy-paste: (1) a Substack post matching the S{S}E{E}-episode format (intro, guest bio, takeaways, 4 pull quotes, tools,
  chapters, CTA), (2) a LinkedIn expert post for Matteo via linkedin-expert-posts, (3) a LinkedIn post in the guest''s own
  voice for them to publish from their profile (with a soft Cohort 4 referral CTA if the guest has a promo code), and (4)
  an outreach email from Matteo to the guest bundling all assets, links, and partnership details. Last mile is always a single
  Notion page created under the GTME School podcast parent page via mcp__notion__notion-create-pages, with a Notion sync-back
  manifest line appended to the local bundle.md per.claude/rules/notion-protocol.md. (Changed 2026-05-25 from GDoc to Notion per
  Matteo''s standing preference; see MEMORY.md feedback_gtme_podcast_notion_default.) Triggers: "podcast episode post", "GTME
  podcast Substack", "write up episode S#E#", "/gtme-podcast". NOT for the Pulse newsletter — use gtme-pulse. NOT for generic
  transcript insights — use transcript-analysis alone.'
goal: 'Turns a GTM Engineer School podcast transcript into four artifacts bundled into one Notion page: Substack post, host
  LinkedIn (Matteo + Jared), guest LinkedIn draft, and outreach email.'
outcome: 'Turns a GTM Engineer School podcast transcript into four artifacts bundled into one branded Notion page for review
  and copy-paste: (1) a Substack post matching the S{S}E{E}-episode format (intro, guest bio, takeaways, 4 pull quotes, tools,
  chapters, CTA), (2) a LinkedIn expert post for Matteo...'
primitive: content
sub_primitive: execution
ontology_type: content-strategy
review_gate: 2
inputs:
  required: []
  recommended:
  - transcript-analysis
  - linkedin-expert-posts
  - voice-reviewer
- type: newsletter
  feeds_into: []
- type: linkedin-post
  feeds_into: []
- type: linkedin-post
  feeds_into: []
- type: outreach-email
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used:
- exa
- notion
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

## Research source (Exa)

**Default:** Exa, per `.claude/rules/exa-protocol.md` (auto-loaded for research, audit, competitor, ICP, AEO, content sourcing, sales prospecting work).

**Primary Exa tools for this skill:** `web_search_exa, company_research_exa`. **Use case:** pre-podcast guest + company research.

**Citation:** every Exa-derived claim uses `[VERIFIED: exa_search, {url}, accessed {YYYY-MM-DD}]` per `.claude/rules/ontology.md`. **Quality gate:** ≥3 sources per major claim, ≥50% `[VERIFIED]` confidence, date filter for any "recent / latest" claim, no fallback to `WebSearch` without flagging.

---

# GTM Engineer School podcast

Turn a single podcast transcript into a complete amplification kit: the Substack post, Matteo's LinkedIn expert post, a guest-voice LinkedIn post (with a soft Cohort 4 CTA), and an outreach email bundling it all for the guest. Every quote traces verbatim to the transcript — no fabrication, no invented promo codes, no generic filler.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md) — the 12 patterns LinkedIn voice can't carry
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in gtme-podcast |
|---|---|---|
| **R1** | Source placement (three layers) | Substack post + LinkedIn posts + guest email are **end-customer-facing**. **No sources block.** Transcript quotes appear inline with attribution to the guest — but no `[VERIFIED:...]` tags. Source transcript lives in working doc for QA only. |
| **R3** | Product-update tone | When the episode features GTME School cohort framing, frame as "Cohort 5 opens [date]" not "we are thrilled to announce Cohort 5." Per [[feedback_gtme_pulse_conventions]] cohort-naming rule. |
| **R6** | CTA hierarchy | Substack + LinkedIn posts → soft cohort enrollment as primary CTA, podcast subscribe as fallback. Guest email → reply-to-share primary, social-share as fallback. Cohort naming pulled from current cohort in [[feedback_gtme_pulse_conventions]]. |
| **R9** | Action-oriented section names | "Why this episode matters / What [Guest] shipped / How to take [Guest's] approach further" — verb-led + entity-named. |

---

## Claude Code triggers

**Invoke when user says:**

- "Write up episode S{N}E{M}" (e.g., "S2E1")
- "GTME podcast Substack post"
- "Podcast episode post"
- "Create the episode kit"
- "/gtme-podcast"
- User pastes a podcast transcript and mentions GTM Engineer School

**Do NOT invoke when:**

- User wants Pulse newsletter → use `gtme-pulse`
- User wants raw transcript insights only → use `transcript-analysis`
- User wants Matteo's expert post without the full episode kit → use `linkedin-expert-posts` directly
- User wants a personal/story-style post → use `linkedin-personal-posts`

---

## Input requirements

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Transcript** | Full episode transcript text, file path, or YouTube URL | User provides |
| **Season number** | Integer (default `2` for current season) | User provides or defaults |
| **Episode number** | Integer — episode-within-season, NOT cumulative | User provides |
| **Guest full name** | e.g., "Yash Tekriwal" | User provides |
| **Guest role + company** | e.g., "Head of Education, Clay" | User provides |
| **Guest LinkedIn URL** | Used in Substack footer + email | User provides |

**Episode numbering convention:**
- Season 1 used `E{N}` format on Substack (E1–E10, legacy).
- Season 2+ uses `S{S}E{E}` format (S2E1, S2E2, …).
- File naming ALWAYS uses `s{S}e{E}` (lowercase), e.g., `s2e1`.

### Optional but strongly encouraged

| Input | How it helps |
|-------|--------------|
| `episode_title` | Main topic. If missing, derived from transcript themes. |
| `guest_company_url` | For Substack footer "Where to find {guest}" |
| `guest_email` | Required if user wants Gmail draft staged. Skip if email delivered as file only. |
| `guest_promo_code` | **Unlocks secondary CTA in guest LinkedIn post AND partnership section in email.** If missing → both omitted, skill flags omission. |
| `spotify_url`, `youtube_url`, `apple_podcasts_url` | Populate email link block. If missing → `_placeholder` retained. |
| Release date | For context line in email |

### Cohort-level config (auto-loaded)

The skill reads the premium reference for: `cohort_name`, `cohort_url`, `student_discount`, `guest_commission`, `referral_dashboard_url`. Update once per cohort — never pass per-episode.

### Validation

Before proceeding: transcript provided (fetch via youtube-transcript MCP if URL); episode number provided; guest name + role + company + LinkedIn URL provided; cohort config loaded.

If `guest_promo_code` missing → ask: "No promo code passed — proceed without the Cohort 4 CTA? (yes / provide code / cancel)". Default to proceed without if user confirms.

If any required input missing → ask, don't invent.

---

## Process flowchart

```
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ INPUT │─▶│ PHASE 1│─▶│ PHASE │─▶│ PHASE 4│─▶│ PHASE 5│─▶│ PHASE 6│
│ VALID. │ │ INSIGHT│ │ 2–3 │ │ BUNDLE │ │ NOTION │ │ SUMMARY│
│ │ │ ANALYS.│ │ 4 ASSTS│ │ ASSEMB.│ │ PUSH │ │ TO USER│
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
                                                     │
                                                     ▼
                                              Notion page URL
                                              (last mile — mandatory)
```

---

## Process

The episode kit runs in 6 phases. Read the premium reference for the full step-by-step.

Phase summary:

1. **Phase 1 — Transcript analysis.** Delegate to `transcript-analysis`; save SCQA insights with verbatim quotes + timestamps to `insights.md` (audit trail).
2. **Phase 2 — Substack post.** 11-section structure following `substack-template.md`. 4 takeaways, 4 verbatim blockquotes, 15–20 timestamps, both co-hosts in footer.
3. **Phase 3a — Host LinkedIn post.** Chain into `linkedin-expert-posts` with the most opinion-worthy POV from the episode + 2–3 verbatim quotes as proof.
4. **Phase 3b — Guest LinkedIn post (inline).** Match the guest's voice (NOT Matteo's). Always marked `[DRAFT — edit freely]`. Conditional Cohort 4 P.S. iff `guest_promo_code` provided.
5. **Phase 3c — Guest outreach email.** Specific-takeaway opener; 🎧 listen / 🧵 host posts / ✏️ embedded guest draft / 💸 conditional partnership block / closing.
6. **Phase 4 — Bundle assembly.** Concatenate all 4 artifacts with `═══ SECTION N ═══` dividers into one bundle.md.
7. **Phase 5 — Notion push (mandatory).** Resolve the GTME School podcast parent page via `notion-search`, then `notion-create-pages` with the bundle as body. Append the Notion sync-back manifest line (`<!-- notion: pageId=... url=... published=... last_pulled=... -->`) to the local `bundle.md` per `.claude/rules/notion-protocol.md`.
8. **Phase 6 — Delivery summary.** Notion page URL + local file paths + promo-code status + unfilled placeholder warnings + next actions.

---

## The Iron Law (inherited from transcript-analysis + extended)

1. **Every quote traces to transcript.** Substack blockquotes, guest LinkedIn paraphrases, email takeaway line — all traceable.
2. **Core Takeaways reference specific SCQA insights** from Phase 1. No invented takeaways.
3. **Guest bio facts marked inferred** if sourced from WebSearch, not user input.
4. **Tools list contains only tools named in transcript.** No "probably mentioned".
5. **Chapter descriptions correspond to transcript ranges.** Rewritten for scannability, not fabricated.
6. **Guest LinkedIn post must not put words in their mouth.** Always marked `[DRAFT — edit freely before publishing]`.
7. **Guest email's specific-takeaway line references a real transcript moment.** No generic filler.
8. **Never invent a promo code, discount, commission, or cohort URL.** If `guest_promo_code` missing → omit both CTA blocks cleanly and flag in delivery summary. Routing real student signups to a fabricated code is a revenue-integrity failure.

---

## Red flags (stop and verify)

🚩 About to write a Substack quote without a transcript match → STOP. Pull from insights.md verbatim.

🚩 About to render `{guest_promo_code}` as a literal string → STOP. Either a real code was passed, or the CTA block is absent entirely.

🚩 About to send / auto-stage email without URL placeholders filled → STOP. Always save as draft / file; Matteo fills URLs before sending.

🚩 About to omit Jared from the Substack "Where to Connect" footer → STOP. Template requires both co-hosts.

🚩 About to write the guest LinkedIn post with arrows, em-dash section setups, or Matteo's catchphrases → STOP. Voice must be the guest's, not Matteo's.

---

## Anti-hallucination guardrails

1. No invented promo codes, discounts, or commission rates.
2. No invented URLs — placeholders stay as `_placeholder` strings until filled.
3. No invented guest bio details — if guest input is thin, use WebSearch but mark inferred fields.
4. No paraphrased "quotes" — if a blockquote appears, it's verbatim from transcript.
5. No fabricated tool mentions — category rows skipped if no tools in that category were named.
6. No attributing specific statements to the guest in the guest LinkedIn post unless they said it on the pod.

---

## Quality

Per-artifact pre-delivery checklist (Substack / host LI / guest LI / guest email / all artifacts / bundle+GDoc): the premium reference.

---

## Gotchas

- **Both hosts in the footer.** The Substack template lists Jared Waxman AND Matteo Tittarelli as co-founders. Missing Jared is an obvious error — always verify against `e8-reference.md`.
- **Quotes have no attribution.** E8/E10 both show clean blockquotes with no `— Guest, [MM:SS]` suffix. Attribution lives in `insights.md`, not the published Substack post.
- **Promo code is conditional, not defaulted.** Missing code → both CTAs omitted cleanly. Do NOT fall back to a house code.
- **Cohort 4 has no referral dashboard yet.** The `Track signups:` line in the email is omitted until `cohort-config.md` gets that URL.
- **Guest LinkedIn post uses guest voice, not Matteo.** Single most common failure mode — read aloud and verify.
- **URL placeholders stay as placeholders.** The Substack post isn't published when the email is drafted. Matteo swaps URLs after publishing.
- **Notion push is not optional.** The delivery is the Notion page (changed from GDoc 2026-05-25). If push fails, surface the error — don't silently fall back to "here are the local files". The local bundle.md must carry a `<!-- notion: pageId=... -->` manifest line after a successful push so the ambient sync-back engine can pull edits back.
- **File naming is `s{S}e{E}`, not `e{N}`.** Legacy `e{N}` was Season 1 only. Current and future episodes use `s2e1`, `s2e2`, etc. Mismatches break sort order.

---

## Integration with other skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **transcript-analysis** | `depends_on` (Phase 1) | Extract SCQA insights + verbatim quotes |
| **linkedin-expert-posts** | `depends_on` (Phase 3a) | Generate Matteo's LinkedIn post |
| **gtme-pulse** | Sibling | Both publish to GTM Engineer School Substack. Share voice + footer conventions |
| **voice-reviewer** | `validates` | Optional gate before delivery — run on Substack + host LI |
| **notion (MCP)** | `feeds_into` | Mandatory Phase 5 — push bundle to branded Notion page under the GTME School podcast parent (changed from create-gdrive 2026-05-25; see `.claude/rules/notion-protocol.md`) |

---

## File locations (reference)

| File | Purpose |
|------|---------|
| the premium reference | Full 6-phase step-by-step |
| the premium reference | Per-artifact pre-delivery checklist |
| the premium reference | Current cohort values — update per cohort |
| the premium reference | Substack post template with placeholders |
| the premium reference | Guest-voice post template + voice calibration |
| the premium reference | Outreach email template + conditional rendering |
| the premium reference | Gold-standard filled example (E8 — Nico Druelle, Season 1 legacy format) |
| the premium reference | One-doc-all-assets layout for the Notion push (Phase 4 + 5) |

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

