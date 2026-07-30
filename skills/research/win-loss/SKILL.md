---
name: win-loss-analysis
version: '2.1'
last_updated: 2026-07-14
author: genesys-growth
description: Analyzes sales call transcripts to extract win/loss patterns, objection themes, and competitive intelligence.
  Produces aggregate insights with verbatim quotes, pattern frequencies, and strategic recommendations. Triggers on "win/loss
  analysis", "lost deals", "why we lose", "why we win", "churn analysis", or "sales call patterns". Feeds into icp-behavioural,
  positioning, and battlecards as foundational customer evidence.
goal: Analyzes sales call transcripts to extract win/loss patterns, objection themes, and competitive intelligence.
outcome: Analyzes sales call transcripts to extract win/loss patterns, objection themes, and competitive intelligence. Produces
  aggregate insights with verbatim quotes, pattern frequencies, and strategic recommendations. Triggers on "win/loss analysis",
  "lost deals", "why we lose", "why we win", "churn...
primitive: research
ontology_type: win-loss-analysis
review_gate: 1
inputs:
  required: []
  recommended: []
outputs:
- type: win-loss-analysis
  feeds_into:
  - case-study
  - icp-behavioural
  - positioning
  - product-messaging
depends_on: []
feeds_into:
- case-study
- icp-behavioural
- positioning
- product-messaging
owned_by_agent: researcher
mcps_used: []
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
---

# Win/loss analysis

Analyze sales call transcripts to extract actionable insights on why deals are won, lost, retained, or churned. Cross-reference findings with ICP, firmographics, and competitive context to produce strategic recommendations.

---

## Claude Code triggers

**Invoke when user says:**
- "Win/loss analysis"
- "Analyze sales calls"
- "Why did we win/lose"
- "Churn analysis"
- "Retention analysis"
- "Sales call insights"
- "Deal outcome patterns"
- "Customer feedback synthesis"
- "Analyze these transcripts"
- "What patterns in our sales calls"

**Do NOT invoke when:**
- User wants general transcript analysis → use `transcript-analysis`
- User wants competitor research → use `competitor-research`
- User wants single customer interview analysis → use `transcript-analysis`
- User wants sales enablement assets → use `sales-enablement`

---

## Input requirements

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Transcripts** | Sales call transcripts with customer name and outcome | User provides |
| **Outcome** | Win/Loss/Retention/Churn for each call | User specifies or infer |

### Optional (improve quality)

| Input | How it helps |
|-------|--------------|
| Website URL per customer | Firmographics cross-reference |
| Product/ICP document | Define in-scope product capabilities |
| Market/GTM document | Positioning and competitive landscape |
| Sales notes column | Additional context (stage, deal size) |
| Competitor names | Pre-identify competitors to watch for |

### Validation

Before proceeding: at least one transcript provided; outcome known or inferable from transcript; customer name identifiable.

If inputs are missing: ask the user for transcripts. Clarify if outcome should be inferred from transcript signals.

### Transcript intake — normalize any recorder format

Transcripts arrive in many shapes: Gong, Fireflies, Otter, Grain exports, Zoom/Avoma VTT, SRT, recorder JSON, or plain pasted text. Before Phase 1, normalize whatever you're handed into one shape — speaker-attributed turns, timestamps where present. See `references/transcript-adapters.md` for the sniff-and-parse table per format and the normalized target shape. `/transcripts` inherits the same reference.

Two rules apply to every transcript before analysis:

- **Redact PII first** — `.claude/rules/pii-redaction.md`. Mask end-client names, emails, account numbers before processing; keep roles, company, deal context. (Load-bearing for ClientCo and any regulated client.)
- **Bind every claim to evidence** — `.claude/rules/evidence-bound-outputs.md`. Every extracted pattern cites a verbatim quote + speaker; normalized turns make speaker attribution reliable.

---

## Process

The analysis runs in 3 phases. Read `references/process.md` for the full step-by-step (4 transcript-processing steps, 4 aggregation steps, 4 synthesis steps, plus per-phase checkpoints and the process flowchart).

Phase summary:

1. **Transcript processing** — classify outcome, identify speakers, extract customer context, pull verbatim quotes for the 6 dimensions
2. **Pattern aggregation** — group by outcome, count frequency, rank patterns (3+ mentions), cross-reference by ICP/competitor/persona
3. **Insight synthesis** — state pattern, provide evidence with frequency + confidence, identify opportunity, generate executive summary
4. **Canonical-doc drift → propose diff** *(optional — active client, cadenced batch only)* — check recurring patterns against the client's current positioning/messaging docs and emit gated diff **proposals**. See `references/canonical-doc-propose.md`.

### Cadence

For an active client, run the batch analysis on a **monthly** cadence — the review cycle that keeps positioning/messaging current between quarterly refreshes. Phase 4 rides that same monthly run; it adds no separate schedule. Single-call and ad-hoc runs skip Phase 4.

### Phase 4 — when it runs

Phase 4 fires only on a **cadenced batch** for an **active client with canonical docs** (`projects/consulting/active/{client}/positioning/` or `messaging/`). It **proposes** diffs; it never applies them — the merge is a separate, two-layer human gate (Genesys PMM, then client signoff). Win-loss stays additive; positioning/messaging stay human-locked. Skip Phase 4 silently for single-call runs, comparison-only runs, prospects, or clients with no canonical docs. Full protocol, eligibility (recurrence gate), voice gate, and merge bridge: `references/canonical-doc-propose.md`.

---

## Core frameworks

### Analysis modes

| Mode | When to use | Output |
|------|-------------|--------|
| **Single call** | Deep analysis of one transcript | Full insight extraction per dimension |
| **Batch analysis** | Multiple transcripts (3-20 calls) | Aggregated patterns with frequency counts |
| **Comparison matrix** | Win vs. loss OR retention vs. churn | Side-by-side pattern comparison |

**Default to batch analysis mode** when multiple transcripts are provided.

### 6 analysis dimensions

| # | Dimension | Win signals | Loss signals |
|---|-----------|-------------|--------------|
| 1 | **Product** | "Exactly what we need," feature praised | "Missing [feature]," "Doesn't do [X]" |
| 2 | **Messaging** | "Now I understand why this matters" | "What does it actually do?" |
| 3 | **GTM/Sales** | "You really understand our problem" | "Demo didn't address our needs" |
| 4 | **Pricing** | "Fair price," "good value" | "Too expensive," "over budget" |
| 5 | **Competition** | "Chose you over [competitor]" | "Going with [competitor]" |
| 6 | **Customer context** | "Need this now," deadline-driven | "No rush," "maybe next year" |

### Confidence scoring

| Level | Definition | When to apply |
|-------|------------|---------------|
| **High** | 3+ calls with consistent pattern | Clear recurring theme |
| **Medium** | 2 calls or inferred from strong signals | Emerging pattern |
| **Low** | Single mention or indirect reference | Possible outlier |

### Outcome classification

| Outcome | Definition | Key signals |
|---------|------------|-------------|
| **Win** | Deal closed, contract signed | "We're moving forward," pricing confirmed |
| **Loss** | Deal lost to competitor or no-decision | "Going with [competitor]," "Not right now" |
| **Retention** | Existing customer renewing/expanding | Renewal discussion, expansion |
| **Churn** | Existing customer leaving/reducing | Cancellation, "not getting value" |

---

## Output

Produce a single win/loss report markdown file. Template + iteration prompts library: `references/output-format.md`.

Pre-delivery quality checklist + worked example + anti-examples: `references/quality.md`.

Auto-update protocol (feedback signals, pattern detection, skill-update template): `references/auto-update.md`.

---

## Anti-hallucination guardrails

1. **Quote verbatim.** All insights must trace to specific transcript quotes.
2. **Never invent patterns.** If a pattern appears in only one call, label it "Single mention — pattern unconfirmed."
3. **State frequency.** Always note how many calls support each finding (e.g., "4 of 7 calls").
4. **Acknowledge gaps.** If a dimension has no data, mark "Not discussed in transcripts."
5. **Distinguish roles.** Tag who said what — prospect vs. sales rep vs. champion.

---

## Gotchas

- **Correlation as causation.** Reports "deals with longer sales cycles were lost" as if cycle length caused the loss → always distinguish patterns from causes. Use "associated with" not "caused by".
- **Small sample bias.** Draws conclusions from 2-3 deals instead of waiting for sufficient data → flag sample size prominently. Minimum 5 wins and 5 losses for reliable patterns.
- **Missing verbatim quotes.** Summarizes what buyers said instead of extracting exact quotes → verbatim quotes are the primary deliverable. Summaries are secondary.
- **Single-dimension analysis.** Only looks at win/loss by competitor, missing dimensions like deal size, ICP segment, or sales cycle stage → cross-tabulate across at least 3 dimensions.
- **Conflates product feedback with sales insights.** Mixes "they wanted feature X" with "they didn't trust our team" → separate product gaps from sales execution issues. They feed into different downstream skills.

---

## Integration with other skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **transcript-analysis** | Related | Use for general transcripts, not sales calls |
| **sales-enablement** | Downstream | Feed insights into battlecards and objection handlers |
| **positioning / product-messaging** | Downstream | Phase 4 proposes gated diffs to the client's canonical positioning/messaging docs from recurring patterns (propose only, human-merged). See `references/canonical-doc-propose.md` |
| **competitor-research** | Related | Cross-reference competitor mentions |

---

## Reference files

| File | Purpose |
|------|---------|
| `references/process.md` | Full 3-phase step-by-step + flowchart |
| `references/output-format.md` | Win/loss report template + iteration prompts |
| `references/quality.md` | Pre-delivery checklist + worked example + anti-examples |
| `references/auto-update.md` | Feedback signal detection + pattern rules (self-improvement of THIS skill) |
| `references/canonical-doc-propose.md` | Phase 4 — propose gated diffs to client positioning/messaging docs |
| `references/extraction-patterns.md` | Signal patterns for each dimension |
| `references/output-template.md` | Legacy report template (kept for reference) |
| `references/example-analysis.md` | Worked example with 5 transcripts |

---

## MCP data integration

**Level:** 0 — Context (heavy pulls)

### Pulls fresh

| Source | What to pull | Tool | When |
|--------|-------------|------|------|
| **Granola** | Sales call transcripts and deal discussions | `search_meetings`, `get_meeting_content` | Always |
| **Slack** | Deal discussion threads and competitive intel | `slack_search_public` | Always |

### Fallback (no MCP)

- User-provided call transcripts or recordings
- Manual deal review notes

---

