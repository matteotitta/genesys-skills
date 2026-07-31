---
name: call-coaching
version: '1.0'
last_updated: 2026-06-08
author: genesys-growth
description: Scores a single sales-rep call transcript against the qualification framework that fits the call type, and returns
  an evidence-bound coaching report — strengths, gaps, and concrete better-move examples per framework element, plus a calibrated
  score and a focus for the next call. Triggers on "coach this call", "score this rep's call", "call coaching", "rep coaching
  report", or "how did this call go". Pulls the sales-qualification framework library for rubrics and inherits the evidence-bound
  + PII-redaction rules. Distinct from win-loss (retrospective multi-call patterns) and sales-call-playbook (authoring a playbook).
  Recommended upstream context is product-messaging and sales-call-playbook.
goal: Score a rep's single call against the fitting methodology and return an evidence-bound coaching report.
outcome: A per-rep coaching report — call type, framework, per-element verdict with quoted evidence, strengths, gaps, better-move
  examples, calibrated score, and a focus for the next call.
primitive: sales-enablement
sub_primitive: null
ontology_type: call-coaching-report
review_gate: 2
inputs:
  required: []
  recommended:
  - product-messaging
  - sales-call-playbook
- type: call-coaching-report
  feeds_into:
  - sales-tracks
depends_on: []
- sales-tracks
owned_by_agent: sales
mcps_used: []
- gdrive
- notion
triggers:
  slash_commands:
  - /call-coaching
  natural_language:
  - coach this call
  - score this rep's call
  - rep coaching report
  - how did this call go
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fresh
effort: high
---

# Call coaching

Score a sales rep's single call against the qualification framework that fits the call type, and return an evidence-bound coaching report: what they did well, where they fell short, the specific better moves to make next time, and the one thing to focus on. Every verdict is backed by a verbatim quote. Coach the rep; judge the call.

Built for sales-team enablement — e.g. ClientCo's SDR ramp and QA. It reads one call and helps one rep get better.

---

## Claude Code triggers

**Invoke when the user says:**
- "Coach this call" / "score this rep's call"
- "Rep coaching report" / "how did this call go?"
- "Grade this discovery/demo/closing call"
- "Where did the rep miss on this call?"

**Do NOT invoke when:**
- User wants patterns across many won/lost deals → use `win-loss` (retrospective aggregate, not per-rep coaching)
- User wants to author a reusable sales playbook → use `sales-call-playbook`
- User wants general meeting summary/notes → use `transcripts`
- User wants competitive intel → use `competitor-research`

### How this differs from its siblings

| Skill | Job | Input → output |
|-------|-----|----------------|
| **call-coaching** (this) | Make one rep better on one call | One call → forward-looking per-rep coaching |
| `win-loss` | Find why deals are won/lost | Many calls → backward-looking aggregate patterns |
| `sales-call-playbook` | Author the client's playbook | No transcript → reusable reference |

---

## Input requirements

| Input | Required? | Notes |
|-------|:---------:|-------|
| One call transcript | Required | Any recorder format — see intake below |
| Call outcome / context | Optional | Helps calibrate (deal stage, amount, competitor) |
| Chosen framework | Optional | If omitted, inferred from the call type |
| product-messaging | Recommended | What we're selling — sharpens "better move" examples |
| sales-call-playbook | Recommended | The client's own playbook, if one exists |

If no transcript: ask for one. A coaching report needs a real call — never fabricate one to demonstrate the format.

### Intake — normalize, then redact

1. **Normalize any recorder format** (Gong / Fireflies / Otter / Grain / VTT / SRT / JSON / plaintext) to speaker-attributed turns. Reuse the adapter spec at `research/win-loss/the premium reference. (Transcripts may come from Granola via MCP, or pasted directly.)
2. **Redact PII first** — `.claude/rules/pii-redaction.md`. Mask end-client names, emails, account numbers; keep the rep's name+role, company, deal context, and the words. Load-bearing for ClientCo (FCA-regulated).
3. **Infer roles** — label each speaker rep / buyer / champion / economic-buyer. Roles drive both scoring and evidence attribution.

---

## Process

1. **Classify the call type.** Map the transcript to one of the 14 types in [`call-type-taxonomy.md`](../../../../projects/research/taste-library/resources/0626-sales-qualification-frameworks/call-type-taxonomy.md). The type picks the framework — discovery → SPICED or Sandler or Gap Selling; demo → Command of the Message; technical-validation / go-no-go / negotiation / closing → MEDDPICC + Next Steps; cold call → BANT. If the call is mixed or ambiguous, name the dominant type and say why; ask the user if it's a coin-flip.

2. **Score against the framework's elements.** Pull the chosen framework from [`qualification-frameworks.md`](../../../../projects/research/taste-library/resources/0626-sales-qualification-frameworks/qualification-frameworks.md). For each element: a verdict (covered / partial / missing) and a calibrated 0–100 sub-score, using the element's "covered when / missing when" signals as the rubric. **Every verdict cites a verbatim quote + speaker** per `.claude/rules/evidence-bound-outputs.md`. No quote → lower confidence or mark the element "not enough evidence," never invent.

3. **Flag deal-health movement (optional).** Note which deal-health dimensions the call advanced vs. left untouched, per [`health-rubrics.md`](../../../../projects/research/taste-library/resources/0626-sales-qualification-frameworks/health-rubrics.md). A single call rarely moves all ten — name the one or two it should have and didn't.

4. **Write the coaching report.** Follow the 8 principles below and the template at the premium reference. Lead with the headline signal, order improvements high → low impact, give concrete better-move examples in a human voice. Keep it skimmable — a manager reads it in two minutes.

---

## The 8 coaching principles

Adapted from the gtm-superintelligence coaching operating frame (Apache-2.0). These govern every coaching report.

1. **Evidence over opinion** — every score quotes the transcript with attribution. Lower confidence rather than invent evidence. (Enforced by `evidence-bound-outputs.md`.)
2. **Coach the rep, judge the call** — evaluate seller behavior only. Buyer responses are evidence of how the rep performed, not the thing being graded.
3. **Specific and actionable** — give concrete "better move" examples the rep can reuse on the next call. No vague "build more rapport."
4. **Calibrated scoring** — use the full 0–100 range. Excellent execution 80+, average 50–65, reserve 90+ for textbook moments.
5. **Respect the rubric** — score only against the chosen framework's elements. Don't import outside criteria the rep was never measured on.
6. **Honor methodology vocabulary** — name the elements: "no Critical Event surfaced (SPICED)", "Economic Buyer never engaged (MEDDPICC)". It teaches the framework while it coaches.
7. **Brevity with substance** — lead with signal, prioritize improvements high to low. Managers skim. One page.
8. **No fabrication of business facts** — don't assume deal size, competitors, or outcomes unsupported by the transcript or provided metadata.

**Tone:** direct, supportive, concrete — like a strong 1:1 manager. Praise genuine strengths; be honest about gaps.

**Better-move style:** sound human, not automated. No em-dashes, no corporate openings ("I hope this finds you well"), no hype words ("leverage", "synergy", "unlock"). Lead with the point and one clear ask. (Aligns with `.claude/rules/ai-speak-anti-patterns.md` — the better-move examples are model copy, so they pass the same bar as any shipped content.)

---

## Final ship gate

Run `/premortem --output` before ship. See `.claude/skills/meta/orchestration/premortem/SKILL.md` for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and the output template. For a coaching report the sharpest failure modes are: a verdict with no quote behind it (evidence-bound miss), unredacted client PII reaching a shared doc, and "better move" examples that read like AI slop — check all three.

---

## Attribution

The four-stage coaching approach (classify → score → coach), the 8 operating principles, and the call-type → framework mapping are adapted from [`attentiontech/gtm-superintelligence`](https://github.com/attentiontech/gtm-superintelligence) (Apache-2.0), accessed 2026-06-08. Imported via `/steal` — `.claude/discovery/0626-gtm-superintelligence-steal-analysis.md`.

---

