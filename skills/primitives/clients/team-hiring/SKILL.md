---
name: team-hiring
version: '2.0'
last_updated: 2026-05-28
author: genesys-growth
description: |
  Generate the canonical Genesys hiring artefacts end-to-end. Mode A produces the sourcing 3-pack (JD + interview process + LinkedIn hiring post) plus an optional public careers page. Mode B produces per-batch operational artefacts (interview hub per role per sprint) and per-candidate Stage-1 outputs (scorecard from Granola transcript + advance email or decline note). Calibrated to a specific client (or Genesys-internal) context. Pulls voice, positioning, traction, ICP, team structure, and brand rules from the client's CLAUDE.md + locked PMM artefacts. Layers best-practice patterns from category-leading companies per role type (Nooks / Apollo / 11x / Clay for outbound; Linear / Vercel / Notion for PMM; Anthropic for technical roles). Produces markdown files in the client's team-hiring/ folder. Triggers Mode A: "create JD for", "hire a {role}", "hiring 3-pack", "team hiring sprint", "careers page", "SDR JD", "AE JD". Triggers Mode B: "build interview hub for {role}", "score this interview", "stage 1 scorecard for {candidate}", "draft advance email for {candidate}", "decline note for {candidate}", "interview debrief". Depends on client CLAUDE.md for voice rules and externally-safe proof points; recommends positioning, product-messaging, tov-guidelines, expert-pov, icp-research, brand-kit upstream. Gate 3 deep review for Mode A (public-facing). Gate 2 standard review for Mode B (internal stakeholder + candidate-facing).
goal: Ship full-funnel hiring artefacts in client voice. Mode A = JD + interview process + LinkedIn post (+ optional careers page). Mode B = interview hub + Stage-1 scorecard + candidate comms.
outcome: Markdown files in {client}/team-hiring/ passing voice-rule self-review. Mode A ships 3-4 sourcing files per role; Mode B ships hub per role + scorecard + comms per candidate. Push handoffs documented.
primitive: clients
ontology_type: client-engagement
review_gate: 3
inputs:
  required: []
  recommended:
    - positioning
    - product-messaging
    - tov-guidelines
    - expert-pov
    - icp-research
    - brand-kit
depends_on: []
owned_by_agent: b2b-consultant
mcps_used:
  - exa
  - firecrawl
  - gdrive
  - notion-api
  - granola
triggers:
  slash_commands:
    - /team-hiring
  natural_language:
    - "create JD for"
    - "hire a"
    - "hiring 3-pack"
    - "team hiring sprint"
    - "careers page"
    - "SDR JD"
    - "AE JD"
    - "PMM JD"
    - "engineer JD"
    - "build interview hub for"
    - "score this interview"
    - "stage 1 scorecard for"
    - "draft advance email for"
    - "decline note for"
    - "interview debrief"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 1
context: fork
effort: high
paths: projects/consulting/**, projects/genesys/**
---

# Team hiring

Full-funnel hiring skill. Mode A covers sourcing (JD + interview process + LinkedIn post + optional careers page). Mode B covers batch operations (interview hub per role per sprint) and per-candidate Stage-1 outputs (scorecard from Granola transcript + advance email or decline note). One skill, two operational halves, calibrated per client.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../rules/ai-speak-anti-patterns.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (JD + careers page → end-customer-facing → no sources; interview hub + scorecard → client-team review → cleaned cites in appendix), R2 (Mode A multi-asset pack ships as one doc with toggles per asset: JD + process + LinkedIn post + careers page), R3 (JD opener capability-led, never "we are thrilled to grow our team"), R6 (JD close → application primary CTA), R9 (verb-led role + section names).

## Modes

| Mode | Scope | Cadence | Output | Review gate |
|---|---|---|---|---|
| **A — Sourcing artefacts** | Per role per hiring sprint | Once per role | JD + interview process + LinkedIn post (+ optional careers page) | Gate 3 (public-facing) |
| **B — Batch operations** | Per batch + per candidate | Per interview cycle (~weekly) | Interview hub (per role) + Stage-1 scorecard (per candidate) + comms draft (per candidate) | Gate 2 (internal + candidate-facing) |

## When to run → which mode

| User says | Routes to |
|---|---|
| "create JD for {role}", "hire a {role}", "hiring 3-pack", "careers page" | Mode A |
| "build interview hub for {role}", "set up the {role} hiring batch" | Mode B Step 1 |
| "score this interview", "stage 1 scorecard for {candidate}", "interview debrief" | Mode B Step 2 |
| "draft advance email for {candidate}", "decline note for {candidate}" | Mode B Step 3 |

Don't run when the user wants: organisational design (headcount planning, org chart), updating an existing JD after feedback (edit directly), coaching session or interview-prep for the hiring panel, or a reference-check script or offer-letter template.

## Inputs

**Mode A required (no defaults):** org context (client folder), role title, artifact scope (3-pack vs 4-pack).

**Mode B required (no defaults):** org context, role (must already have an existing interview hub OR be creating one in Step 1), and per-step specifics:
- **Step 1 (hub):** role family (SDR / GM / PMM / engineer / etc.), candidate list for this batch (names + LinkedIn URLs + comp expectation + visa flag if relevant).
- **Step 2 (scorecard):** Granola meeting ID (or transcript) + the role's interview hub (for the canonical scorecard table) + user-stated pre-verdict (advance-clean / advance-with-caveat / reject).
- **Step 3 (comms):** the candidate's scorecard verdict + any caveats (office availability / comp recalibration / availability timing / format choice) for advance variants.

**Recommended for both modes (pulled from client artefacts):** voice rules (brand-name convention, em-dash policy, English variant, banned buzzwords, externally-safe vs internal-only proof), positioning + traction, ICP / buyer, team structure, mission + values. Source: client CLAUDE.md, `positioning/`, `messaging/`, `icp/`.

If any required input is missing, ask the user. Don't fabricate role specifics or candidate context.

## Steps

### Mode A — Sourcing artefacts (Steps A1-A8)

1. **Resolve context.** Read client CLAUDE.md, latest.md, canonical references. Pull voice rules, externally-safe proof points, team-member list, existing team-hiring/ precedents.
2. **Confirm scope.** Role title + reporting line + comp band (with role-family defaults). Artifact scope (3-pack or 4-pack).
3. **Route to role-family patterns.** Per the premium reference, identify 3-5 category-leading companies whose JDs and careers pages inform this hire.
4. **Draft the JD.** Use the 10-section template in the premium reference. Length 1,500-2,200 words.
5. **Draft the interview process.** Use the 3-stage template in the premium reference. Calibrate Stage 2 to role family. Length 1,200-1,500 words.
6. **Draft the LinkedIn hiring post.** Use one of the 4 hook archetypes from the premium reference (Challenge / Contrarian-Craft / Mission-Led / Story). Length 350-500 words.
7. **(If 4-pack) Draft the careers page.** WebFetch live About page first. Synthesise 5-7 operating principles from About + brand kit + voice + expert-pov. Length 1,200-1,800 words.
8. **Voice-rule self-review + Gate 3 pause + push handoff.** Per the premium reference voice-rule grep + push protocol.

### Mode B — Batch operations (Steps B1-B3)

1. **Build the interview hub** (per role per sprint). Per the premium reference: this-week's-candidates table + Stage-1 screening script (60-min outline with per-section timing) + live exercise template (per role family) + scorecard template (7 dims for SDR, 10 for GM, role-family adaptations for PMM / engineer / CS) + per-candidate prep appendices (snapshot + three-risks-to-verify + customised opening hook + two probe questions + comp framing + Stage-2 handoff template) + canonical 3-stage process reference. Output: `MMYY-{role}-interview-hub.md` in client's `team-hiring/` folder. Notion-publish as a child page; manifest line wired per `.claude/rules/notion-protocol.md`.

2. **Score the candidate** (per candidate per Stage-1 interview). Per the premium reference: pull Granola transcript via `mcp__granola__get_meeting_transcript`. Map transcript evidence to the role's canonical scorecard table (from the hub). Apply hiring bar ("no dimension below 3, at least 3 dimensions at 4+"). Verdict-up-top, verbatim transcript quotes per dimension, Stage-2 handoff template (or rejection rationale), "next move" footer. Three verdict shapes: advance-clean, advance-with-caveat (sub-variants per the premium reference), reject (rubric-anchored). Output: `MMYY-{firstname-lastname}-stage1-scorecard.md`. Notion-publish as child of the hub page (parent inheritance via the hub's `pageId`).

3. **Draft candidate-facing comms** (per candidate post-verdict). Per the premium reference: advance email (positive signal → next-stage framing → any-caveat-conversation framing → close) OR decline note (shape-of-role framing, not performance → named specific strength → genuine stay-in-touch close). Tone gate: "would I be comfortable if the candidate posted this on LinkedIn?" Output: `MMYY-{firstname-lastname}-stage1-{advance-email|decline-note}.md`. Local-only (operational draft, not stakeholder artefact). Voice rules per client CLAUDE.md.

## What good looks like

**Mode A quality bar (existing v1.0, unchanged):**

- Voice match: reads like the client's existing brand voice. 100-Posts Test.
- Specificity over generality: KPIs quantified, team members named, reporting line explicit, comp a real band.
- Externally-safe proof only: internal-only metrics never appear.
- Role-family pattern visible without copying.
- Application format consistent ("No CV. Three things." per Genesys convention).

**Mode B quality bar (new in v2.0):**

- **Hub:** scorecard dimensions match the role family (SDR 7-dim, GM 10-dim, etc.). Stage-1 script timed to 30 minutes. Per-candidate prep appendix grounded in real LinkedIn + JD context (no fabricated risks).
- **Scorecard:** verdict at line 1 (not buried). Every dimension score backed by a verbatim transcript quote or explicit "not assessed in Stage 1" marker. Hiring-bar logic applied correctly. Stage-2 handoff template populated. "Next move" footer specifies who-does-what.
- **Comms:** advance email frames any caveat (office / comp / availability) honestly without making the candidate feel they're on probation. Decline note frames on shape-of-role, not performance; names a specific strength; warm but unambiguous.
- **Voice rules per client:** no em dashes if banned (e.g., ClientCo), brand-name spelling correct, no affirmative use of internally-banned metrics.

**Self-evaluation (pre-delivery checklist):**

Mode A (unchanged): voice match, KPIs quantified, team members named, comp band specific, brand-name convention, em-dash policy, English variant, no banned buzzwords, no internal-only proof, application format, interview Stage 2 role-appropriate, (if 4-pack) careers page operating principles client-specific + works at openings = 0.

Mode B (new):
- [ ] **Hub:** scorecard dimensions match role family, Stage-1 script timed to 30 min, per-candidate appendices grounded in real profile data.
- [ ] **Scorecard:** verdict at line 1, every dimension backed by verbatim quote, hiring bar applied, Stage-2 handoff populated, "next move" footer specific.
- [ ] **Comms:** advance email caveat framed cleanly, decline note shape-of-role + named strength + warm close.
- [ ] **Voice rules:** pulled from active client's CLAUDE.md, applied per-output.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract.

---

