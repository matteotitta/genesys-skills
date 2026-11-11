---
name: battlecards
description: Builds a sales battlecard against one competitor: when you win and lose, how to position, objection handling, landmines and proof points, kept to what a rep can use on a call. Use when asked for a battlecard, competitive sales sheet or how to sell against X.
---

# Battlecards

Quick-reference competitive intelligence battlecards for live sales conversations. Designed to be scanned in 30 seconds during a call. Supports batch generation for multiple competitors with confidence-level sourcing on every claim.

The body of this file holds decision-grade context (when to invoke, inputs, structure, anti-hallucination guardrails, gotchas). Step-by-step process, output template, quality gates, and feedback loops live in the premium reference.

---

## Claude Code triggers

**Invoke this skill when user says:**
- "Create battlecard for [competitor]"
- "Competitive battlecard"
- "How to win against [competitor]"
- "Competitive intel for sales"
- "Battlecards for [product]"
- "Sales battlecard"
- "Counter-positioning against [competitor]"
- "Competitive one-pager" (if focus is on win/lose scenarios)

**Do NOT invoke when** the user wants deep competitor research, a sales deck, a demo script, or a feature comparison only.

---

## Input requirements

### Required inputs

| Input | Description | Source |
|-------|-------------|--------|
| **Competitor name(s)** | Which competitor(s) to create battlecards for | User specifies |
| **Your product context** | What you sell, key capabilities | User, product-messaging, or URL |

### Optional inputs (improve quality)

| Input | How it helps |
|-------|--------------|
| Competitor notes or a prior dossier | Pre-researched intel (funding, features, positioning) |
| Win/loss notes | When we win/lose patterns with evidence |
| Product messaging | Counter-positioning based on your value props |
| Positioning context | Strategic anchors for competitive framing |
| Competitor URLs | For live research if no prior research exists |
| Sales call transcripts | Real objections and competitive mentions |

### Input validation checklist

Before proceeding, verify:
- [ ] Competitor(s) confirmed
- [ ] Your product's key differentiators known
- [ ] At least one intel source available (research, URL, or docs)

**If inputs are missing:** Ask which competitor(s). If no intel is available, research the competitor's website, pricing page and reviews first.

---

## Process at a glance

| Phase | Purpose | Output |
|-------|---------|--------|
| 1. Competitor selection | Confirm scope (single vs batch) | Confirmed competitor list |
| 2. Intel gathering | Pull from your notes + call transcripts + web research | Intel dossier per competitor |
| 3. Battlecard generation | Fill template, add confidence levels, write talk tracks + landmines | Draft battlecard(s) |
| 4. Validation & delivery | Verify sources, format for delivery | Final battlecard(s) |

Full step-by-step (with checkpoints, confidence framework, workflow sequences, GDrive export commands) in the premium reference.

---

## Battlecard structure (decision-grade)

Every battlecard contains these sections — in this order, no exceptions:

1. **Quick facts** — Founded, funding, employees, target market, pricing model, starting price (side-by-side table)
2. **When we win** — 3 specific scenarios + verbatim customer proof point
3. **When we lose** — 2+ honest losing scenarios + mitigation actions
4. **Their pitch** — Verbatim competitor language + key claims
5. **Counter-positioning** — Scripted "when they say X, we say Y" responses
6. **Feature comparison** — Honest table with winner-per-row
7. **Landmines to plant** — 3+ discovery questions that expose competitor weaknesses
8. **Objection handling** — Common objections with proof-pointed responses
9. **Red flags** — When to walk away (qualification-out criteria)
10. **Sources** — Every claim with URL + access date + confidence

Full template with field-level guidance in the premium reference. Output wrapper format and iteration prompts in the premium reference.

---

## Anti-hallucination guardrails

**Critical for sales credibility:**

1. **Never invent competitor claims.** Only use verified data with sources.
2. **Never fabricate customer quotes.** Verbatim only or mark "[PLACEHOLDER: need customer quote]".
3. **Never guess competitor pricing.** Use verified data or mark "[CONFIRM: pricing]".
4. **Mark confidence levels** on all competitive intel (High/Medium/Low/UNVERIFIED).
5. **Cite sources** for all factual claims with access dates.
6. **Acknowledge gaps** rather than fill with plausible content.
7. **Be honest about weaknesses.** "When we lose" builds credibility with sales team.

---

## Gotchas

- **Fabricated competitor pricing**: Invents pricing tiers when pricing page is gated or not found → Mark pricing as [UNAVAILABLE] and note where to find it (sales call, demo request). Never guess.
- **Generic objection handlers**: Produces "we're more reliable" instead of specific counter-arguments → Every objection handler must reference a concrete differentiator or proof point.
- **Missing landmines**: Only covers strengths, forgets to include questions that expose competitor weaknesses → Landmines are the most valuable section for sales reps. 3-5 questions per competitor minimum.
- **Stale competitive data**: Uses old competitor positioning without checking current website → Always scrape competitor website at time of battlecard creation. Note access date.

---

## MCP data integration

**Pulls fresh:** the competitor's website, pricing page and review sites at the time you build the card.

**Fallback (no live research):** use whatever competitor and win/loss notes the user provides, and mark gaps as `[UNAVAILABLE]`.
