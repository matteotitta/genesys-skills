---
name: reply-scoring
version: '1.0'
last_updated: 2026-05-04
author: genesys-growth
description: 'Classifies inbound email replies into 11 mutually-exclusive buckets (positive_interested, positive_soft, positive_referral, neutral_question, negative_notnow, negative_notfit, negative_hostile, unsubscribe, ooo, bounce, other) and computes positive_reply_rate = (interested + soft + referral) / total_sent. Pulls reply threads via Gmail MCP, batch-classifies via the Agent tool, aggregates per campaign, and writes results to the client''s goals/MMYY-NN-cycle.md so positive reply rate becomes a tracked sprint metric. Triggers: "score replies", "positive reply rate", "how is [campaign] doing", "classify these replies", "post-send measurement". Upstream: outreach-emails or lifecycle-marketing produces the campaign whose replies get scored. Downstream: feeds lead-scoring (high-positive replies become high-priority follow-ups) and outreach-emails (negative-hostile patterns inform copy revision). NOT for pre-send list grading (use /list-quality) or pre-send account fit (use /lead-scoring).'
goal: Classify campaign replies into 11 buckets and compute positive_reply_rate as the north-star post-send metric.
outcome: A per-campaign reply scorecard with bucket counts, positive_reply_rate, hostile/unsub risk flags, and a ranked action list of high-positive replies needing a human, most-recent first.
primitive: outbound
sub_primitive: strategy
ontology_type: reply-classification
review_gate: 1
inputs:
  required: []
  recommended:
  - outreach-emails
  - lead-scoring
- type: reply-classification
  feeds_into:
  - outreach-emails
  - lead-scoring
depends_on: []
- outreach-emails
- lead-scoring
owned_by_agent: operator
mcps_used:
- google-workspace
- gdrive
triggers:
  slash_commands:
  - /reply-scoring
  natural_language:
  - score my replies
  - positive reply rate
  - how is the campaign doing
  - classify these replies
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# Reply scoring

Reply rate tells you if people are paying attention. Positive reply rate tells you if they want what you're selling. This skill computes the second by classifying every reply into one of 11 buckets, then surfaces the high-positive replies that need a human — ranked most-recent first, because this runs as a batch and the freshest reply is the one still worth answering.

**This is a measurement loop, not a speed-to-lead alert.** Speed-to-lead is real (the sales-floor rule of thumb is minutes, not days), but nothing here delivers it: the skill fires at the 14-day mark on a Gmail *pull*, so a reply from day 2 is already twelve days cold when it's scored. Don't read the action list as an SLA. Honouring speed-to-lead needs an arrival trigger this skill doesn't have — the Gmail MCP is pull-only, so the pragmatic version is a scheduled poll, not a webhook. Deferred: no live campaign is feeling this today. See [`.claude/discovery/0726-agentmail-steal-analysis.md`](../../../../../discovery/0726-agentmail-steal-analysis.md) (A2).

## Claude Code triggers

**Invoke when user says:**
- "Score my replies"
- "Positive reply rate"
- "How is [campaign name] doing"
- "Classify these replies"
- "What did our last campaign actually produce"
- "Pull replies from Gmail and bucket them"

**Do NOT invoke when:**
- User wants pre-send list QA → `/list-quality`
- User wants per-account fit before sending → `/lead-scoring`
- User wants the email content itself → `/outreach`
- User wants a content-strategy reply analysis (e.g., LinkedIn comments) → `/transcripts` or a content skill

**Auto-suggest after:** any campaign hits its 14-day mark (sample large enough to read), or user mentions "how did the campaign go" / "are we getting good replies."

## Input requirements

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Campaign identifier** | Gmail thread query, label, sequence ID, or date range that scopes which replies to pull | User provides |
| **Total sent** | The denominator for positive_reply_rate. Pulled from outreach skill's send log, Apollo sequence, or user-provided | User or upstream skill |

### Optional (improves quality)

| Input | Purpose |
|-------|---------|
| Client `goals/MMYY-scope.md` | Provides target positive_reply_rate baseline so we can flag winners vs losers |
| Prior `goals/MMYY-NN-cycle.md` files | Trend history — is positive reply rate improving across cycles? |
| ICP profile (`icp/MMYY-icp-research.md`) | Helps identify whether negative_notfit replies indicate targeting drift |

**Validation:** Skill cannot run without (a) a way to identify the replies to score and (b) a total_sent denominator. If denominator is missing, ask the user before estimating — never invent.

## Process

Three phases — full step detail in the premium reference.

1. **Phase 1 — Fetch.** Use Gmail MCP (`mcp__google-workspace__search_gmail_messages` + `get_gmail_threads_content_batch`) to pull the campaign's reply threads. Filter to the FIRST reply per lead only (later messages are conversation, not signal).
2. **Phase 2 — Classify.** For batches of 20-30 replies, dispatch the locked classification prompt (see the premium reference) via the Agent tool (subagent_type: general-purpose). Each reply returns `{lead_id, label, confidence, one_line_reason}`. Confidence < 0.7 → label as `other`.
3. **Phase 3 — Aggregate.** Compute bucket counts, exclude `ooo` + `bounce` from net replies, derive `positive_reply_rate = (interested + soft + referral) / total_sent`. Compare to baseline (target from `goals/MMYY-scope.md` if available). Flag hostile rate >0.3% and unsub rate >2% as deliverability risks.

## MCP data integration

**Pulls fresh:** Gmail thread content via `mcp__google-workspace__get_gmail_threads_content_batch` (max 100 threads per call; paginate). Uses `matteo@genesysgrowth.com` per `.claude/rules/google-workspace` MCP convention.

**Fallback (no MCP):** if Gmail MCP is unavailable, accept a CSV export from Apollo / Smartlead / Instantly with columns `lead_id, email, reply_subject, reply_body, reply_time`. Process the CSV inline.

**Validation:** every reply that lacks a body gets labeled `other` (cannot classify empty content). Auto-replies (Gmail header `Auto-Submitted: auto-replied`) auto-label as `ooo` without LLM call.

## Quality

Pre-delivery checklist: the premium reference.

Headline rules:
- Confidence threshold: 0.7. Below that → `other`, surface for manual review.
- OOO + bounce excluded from denominators (they're not real replies).
- Sample minimum: 200 sent before computing positive_reply_rate; below 200 the rate is too noisy to interpret.
- Classify only the FIRST reply per lead; later messages are conversation.

## Anti-hallucination guardrails

1. **Never label without reading the reply body.** Empty body → `other`, not guessed.
2. **Never invent total_sent.** If the user can't provide it, ask; do not estimate.
3. **Mark confidence per row.** The aggregate inherits per-row confidence.
4. **Cite the Gmail thread ID** for every classified reply in the output appendix.
5. **Acknowledge gaps.** If 12% of replies returned `other`, surface that as a coverage gap and offer to re-run with a refined prompt (per `.claude/rules/approval-loop-pattern.md`).

## Approval loop (when classifying for the first time per campaign)

Apply `.claude/rules/approval-loop-pattern.md` (auto-loaded for this skill). For the first batch of 10 replies in a new campaign, show the user the classifications and collect corrections. Lock the prompt after 2 zero-correction rounds. Subsequent batches use the locked prompt directly.

For routine cycle scoring on already-tuned campaigns, skip the loop — apply the locked prompt straight to the batch.

**Composes with the scoring-validity gate.** The 2-zero-correction lock proves the classifier *labels* correctly on the tuning batch; it does not prove classification *accuracy generalizes*. If you ever claim an accuracy number for the classifier (not just the ≥200-send `positive_reply_rate` floor already in), hold out a labeled slice per [`.claude/rules/scoring-validity.md`](../../../../../rules/scoring-validity.md) and report the tuning-vs-holdout gap. For routine bucket classification, the approval loop + sample floor are enough — this fires only when a generalization claim is made.

## Integration with other skills

**Upstream (recommended, not required):**
- `outreach` produces the campaigns whose replies this skill scores
- `lifecycle-marketing` produces nurture sequences with measurable replies
- `lead-scoring` provides per-account context (positive replies from STRONG_FIT accounts get extra priority)

**Downstream:**
- High-positive replies feed back into `outreach` (these become next-touch warm follow-ups)
- Per-cycle metrics land in `goals/MMYY-NN-cycle.md` (read by `/weekly-plan`)
- Hostile-reply patterns inform `outreach` copy revisions (the negative_hostile bucket is a copy-quality signal)

**Sideways:**
- Pairs with `/list-quality` (pre-send) to close the measurement loop: list-quality before send, reply-scoring after
- Pairs with `experiment` skill — positive_reply_rate is the success metric for outbound A/B tests

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

