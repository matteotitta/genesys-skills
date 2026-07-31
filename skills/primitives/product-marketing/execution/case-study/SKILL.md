---
name: case-study
version: '1.0'
last_updated: 2026-01-17
author: genesys-growth
description: Writes customer case studies with a challenge-solution-results structure. Extracts verbatim quotes, verified
  metrics, and quantified outcomes into a persuasive narrative ready for web or PDF. Triggers on "case study", "customer story",
  "success story", "customer proof point", or "write up this win". Consumes win-loss-analysis as upstream input for win patterns.
  Feeds into sales-enablement and landing-page-copy as social proof assets.
goal: Writes customer case studies with a challenge-solution-results structure.
outcome: Writes customer case studies with a challenge-solution-results structure. Extracts verbatim quotes, verified metrics,
  and quantified outcomes into a persuasive narrative ready for web or PDF. Triggers on "case study", "customer story", "success
  story", "customer proof point", or "write up this...
primitive: product-marketing
sub_primitive: execution
ontology_type: case-study
review_gate: 2
inputs:
  required:
  - win-loss-analysis
  - product-messaging
  recommended: []
- type: case-study
  feeds_into: []
depends_on:
- win-loss-analysis
- product-messaging
owned_by_agent: growth
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /case-study
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# Case study

Generate compelling B2B SaaS case studies that transform customer success data into persuasive proof points. Output structured narratives with quantified results, authentic quotes, and visual sections ready for web pages or PDF downloads.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`marketing-psychology.md`](../../../../../rules/marketing-psychology.md) — JTBD framing, loss-aversion default
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in case-study |
|---|---|---|
| **R1** | Source placement (three layers) | Published case study is **end-customer-facing** (website / PDF). **No sources block.** Customer quotes appear inline with named attribution (job title + company), but no `[VERIFIED:...]` tags. Source dataset (interviews, transcripts, metrics) lives in working doc for QA only. |
| **R3** | Product-update tone | Capability framing — "Customer ships X with Y" not "Customer is thrilled to announce." Even when the metric is huge. |
| **R6** | CTA hierarchy | Closing CTA names sign-up or trial as primary; "talk to sales" as fallback for enterprise. Never "read more on our blog" — case study IS the blog. |
| **R8** | Entity-name headings | Section headings repeat the customer name — "How [Customer] used [Product]," "Why [Customer] chose [Product]" — not pronoun headings ("How they used it"). |
| **R9** | Action-oriented section names | "How [Customer] solved X" beats "About [Customer]." Outcome-led, not status-led. |

---

## Claude Code triggers

**Invoke when user says:**
- "Write a case study"
- "Create a customer story"
- "Case study for [customer]"
- "Customer success story"
- "Turn this into a case study"
- "Customer story from [data]"
- "Case study from interview"
- "Win story for [customer]"
- "Success story for [company]"
- "Reference customer content"

**Do NOT invoke when:**
- User wants testimonial quotes only → extract directly
- User wants sales deck slides → use `sales-enablement`
- User wants full campaign → use `storytelling`
- User wants video script → use `demo-script`

---

## Input requirements

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Customer name** | Company being featured | User provides |
| **Challenge/problem** | What they struggled with before | Interview, win-loss, user provides |
| **Solution** | How they used the product | Interview, user provides |
| **Results** | Quantified outcomes | Customer data, interview |

### Optional (improve quality)

| Input | How it helps |
|-------|--------------|
| Customer interview transcript | Authentic quotes, story details |
| Win-loss analysis | Context on decision drivers |
| Usage data | Specific feature adoption metrics |
| Customer logo | Visual asset for header |
| Contact info (name, title) | Attribution for quotes |
| Industry/vertical | Vertical-specific framing |
| Timeline | Duration context (implemented in X weeks) |

### Validation

Before proceeding: customer name + industry known; ≥1 quantified result available; challenge clearly articulated; solution approach understood.

If inputs are missing: ask for customer name, primary challenge, and at least one measurable outcome. Offer to structure interview questions if no transcript — see the premium reference.

---

## Process

The case study runs in 3 phases. Read the premium reference for the full step-by-step (4 extraction steps, 4 structure steps, 3 output steps, plus per-phase checkpoints and the process flowchart).

Phase summary:

1. **Story extraction** — transformation arc, quote library (3-5), metrics table, signature moment
2. **Structure development** — hero statement, section drafts, metrics callouts, pull quotes
3. **Output generation** — pick format (web / PDF / slide), apply template, generate derivatives

---

## Case study structure

### Standard sections

| Section | Purpose | Length |
|---------|---------|--------|
| **Hero statement** | Capture attention, summarize transformation | 1 sentence |
| **Metrics bar** | Immediate proof of results | 3 numbers |
| **Company overview** | Context on customer | 2-3 sentences |
| **The challenge** | Problem + pain articulation | 2-3 paragraphs |
| **The solution** | How they use the product | 2-3 paragraphs |
| **The results** | Quantified outcomes + quotes | 2-3 paragraphs |
| **Closing CTA** | Next step for reader | 1 sentence |

### Metrics bar format

```
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ 3-5x │ │ 40-60 │ │ 20-40% │
│ More creator │ │ Hours saved │ │ Stronger │
│ content/month │ │ per month │ │ performance │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Quote format

```
"When we got Archive, I didn't have to do those screenshots anymore."

— Kristen Klochko, Project Manager, Brand Relations & Ecommerce, POPFLEX
```

---

## What good looks like — Archive + POPFLEX

**Input:**
```
Customer: POPFLEX
Industry: Retail/Activewear
Challenge: Manual UGC capture, spreadsheet tracking
Solution: Archive for automatic content capture
Results: 3-5x more content, 40-60 hours saved, Taylor Swift discovery
```

**Expected hero statement:**
```
POPFLEX was trapped in IG notifications and manual spreadsheets.
When they got Archive, they made it into a Taylor Swift song (just saying).
```

**Why this works:** specific pain (IG notifications, spreadsheets); memorable hook (Taylor Swift reference); conversational tone (parenthetical "just saying"); implies transformation without stating it.

Full worked example: `examples/archive-popflex.md`.

---

## Anti-hallucination guardrails

1. **Metrics from source only.** Never invent numbers. Mark as `[METRIC NEEDED]` if not provided.
2. **Quotes verbatim.** Use exact customer words. Don't paraphrase into "better" quotes.
3. **Mark unconfirmed details.** Use `[CONFIRM: detail]` for anything requiring verification.
4. **No invented story beats.** The "signature moment" must come from customer data.
5. **Attribution required.** Every quote needs name, title, company.

---

## Quality checklist (pre-delivery)

### Content
- [ ] Hero statement under 25 words
- [ ] At least 3 quantified metrics
- [ ] At least 3 attributed quotes
- [ ] Challenge clearly articulated
- [ ] Solution tied to specific features
- [ ] Results include before/after comparison

### Format
- [ ] All sections complete
- [ ] Metrics bar formatted
- [ ] Quotes properly attributed
- [ ] CTA included
- [ ] Derivatives generated (if requested)

---

## Gotchas

- **Invented metrics.** Creates "3x improvement" or "50% reduction" without sourced data → every metric must come from the customer or be marked `[UNAVAILABLE]`. Never fabricate results.
- **Generic challenge section.** Opens with "Company X was struggling with..." instead of specific, named pain → the challenge must reference the actual problem as the customer described it, not a generic industry pain.
- **Missing customer voice.** Writes the entire case study in third person without direct quotes → at least 3-5 verbatim customer quotes are needed. These are the most credible parts.
- **No clear "before" snapshot.** Jumps straight to the solution without establishing the baseline state → the "before" picture makes the "after" results meaningful. Include specific metrics or processes that existed before.

---

## Integration with other skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **win-loss-analysis** | Provides input | Customer insights for story |
| **sales-enablement** | Uses output | Case study slides for sales deck |
| **landing-page-copy** | Uses output | Social proof snippets |
| **storytelling** | Uses output | Customer videos in campaigns |

---

## MCP data integration

**Level:** 2 — PM Execution (customer-specific pulls)

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Granola** | Customer-specific call transcripts | `search_meetings` | Always (per-customer story) |
| **Slack** | Customer success threads | `slack_search_public` | Always (per-customer data) |

### Fallback (no MCP)

- User-provided customer interview transcripts
- Manual success metrics from customer
- Email threads or shared docs with customer quotes

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

