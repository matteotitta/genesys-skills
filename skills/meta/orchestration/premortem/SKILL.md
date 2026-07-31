---
name: premortem
version: '1.0'
last_updated: 2026-05-25
author: genesys-growth
description: 'Imagine failure first to surface guardrails before plan execution or deliverable ship. Two modes: --plan (5 strategic domains for plan files in ~/.claude/plans/) and --output (5 execution domains for shippable deliverables like LinkedIn posts, AEO articles, landing-page-copy, proposals, positioning). Produces a ## Premortem section pasted into the plan or output draft. Plan mode is hook-enforced (block on missing section at ExitPlanMode); output mode is soft-warn-enforced (validate-frontmatter.py warns when output skills lack the reference). Triggers: "/premortem", "premortem this", "what could go wrong", "imagine failure first", "what could undermine this", "pre-mortem". Downstream: every output skill in primitives/ chains to /premortem --output before ship. NOT for post-draft review (use voice-reviewer, design-reviewer, product-lens-reviewer, scope-guardian-reviewer for that).'
goal: Surface failure modes upstream of plan execution and deliverable ship, so strategic blind spots get caught at draft-time not review-time.
outcome: "A Premortem section pasted into the plan (--plan mode) or appended to the output draft (--output mode), naming 2-3 failure modes across the relevant 5-domain taxonomy with mitigations and confidence rating."
primitive: meta
sub_primitive: orchestration
ontology_type: runbook
review_gate: 1
inputs:
  required: []
  recommended: []
- type: runbook
  feeds_into: []
depends_on: []
owned_by_agent: operator
mcps_used: []
triggers:
  slash_commands:
  - /premortem
  natural_language:
  - "premortem this"
  - "what could go wrong"
  - "imagine failure first"
  - "what could undermine this"
  - "pre-mortem"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fresh
effort: low
---

# `/premortem` — Imagine failure first, surface guardrails before commit

Two modes share one cognitive frame: write the obituary of the work, then reverse-engineer the avoidable failure. The mode flag picks the domain taxonomy.

| Mode | Use when | Domain taxonomy | Enforced how |
|---|---|---|---|
| `--plan` | Authoring a plan file in `~/.claude/plans/` | 5 strategic domains (positioning-messaging / channel-distribution / stakeholder-alignment / execution-velocity / market-regulatory) | **BLOCK** via `.claude/hooks/exit-plan-premortem-check.sh` at ExitPlanMode |
| `--output` | Producing a client-facing or external-facing deliverable (LinkedIn post, AEO article, landing-page-copy, proposal, positioning lock, messaging library, etc.) | 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) | **SOFT-WARN** via `_schema/validate-frontmatter.py` `check_output_premortem_contract()` |

If invoked without a flag, ask the user which mode applies. Don't generate a generic premortem — the value is in the mode-specific domains.

---

## When to use --plan

You're writing a plan file (most often in `~/.claude/plans/` during plan mode, or a delivery plan in `docs/`). The Auto-Challenge Protocol "For Plans" check + the planning-doctrine pre-ExitPlanMode 8-gate already cover completeness and clarity. Premortem covers what those miss: **strategic blind spots the author can't see because they just convinced themselves the approach works.**

The hook enforces presence: ExitPlanMode will exit non-zero with `Plan missing required ## Premortem section` if you skip it.

## When to use --output

You're producing a shippable deliverable. The output is going in front of a client, a prospect, an external audience, or a public surface. Examples:
- LinkedIn post, AEO article, newsletter issue
- Landing page copy, sales deck, proposal
- Positioning lock, messaging library, ICP synthesis ready for client review
- Pricing strategy doc, content strategy doc

The convention is enforced by validate-frontmatter.py soft-warning when an output skill's body lacks `/premortem --output` reference. The retrofit pass added this reference to ~60-70 existing output skills in `primitives/`.

## Trivial-case escape

For genuinely trivial work (typo fix, single-line rename, one-character config change), the Premortem section can be a single line:

```
## Premortem
No failure modes — trivial change.
```

This satisfies both the hook (plan mode) and the convention (output mode). Use sparingly — most work has failure modes worth naming.

---

## Process (both modes share the same 5 steps)

1. **Define the success state.** One sentence on what "this worked" looks like at the relevant horizon (90 days for plans, immediate for outputs).
2. **Imagine the failure.** Write the obituary: "This shipped, and it didn't work because…" — one paragraph.
3. **Enumerate failure modes per domain.** Walk the 5-domain taxonomy for your mode (see reference files). Name 2-3 specific failure modes with likelihood (L/M/H).
4. **Propose mitigations or accept the risk.** Per failure mode: either a mitigation (with effort S/M/L and owner) or an explicit accept-risk statement.
5. **Carry-forward opportunities.** Pull 1-3 mitigations that double as new product / content / process ideas. Adapted from Cortex's Step 4.

---

## Domain taxonomies (mode-dependent)

### `--plan` mode — 5 Genesys strategic domains

| Domain | What it covers |
|---|---|
| **Positioning-messaging** | Message-market misfit, positioning drift, brand misalignment, "we look like X" risk |
| **Channel-distribution** | Wrong channel, wrong cadence, audience-channel mismatch, channel saturation |
| **Stakeholder-alignment** | Founder availability gap, internal politics, partner pushback, signing-authority drift |
| **Execution-velocity** | Timeline slip, capacity gap, dependency miss, integration risk |
| **Market-regulatory** | Regulatory change (e.g., FCA), competitor move, ICP shift, macro shift |

Full worked examples in the premium reference.

### `--output` mode — 5 Genesys execution domains

| Domain | What it covers |
|---|---|
| **Will-it-resonate** | Hook strength, audience-state fit, novelty vs. familiarity, attention budget |
| **Will-it-convert** | CTA clarity, friction map, trust signals, decision-readiness fit |
| **Will-it-stay-on-brand** | Voice drift, claims integrity, tone match, anti-AI tell exposure |
| **Will-stakeholder-push-back** | Predicted objections, sensitive-claim flagging, internal-politics exposure |
| **Will-it-degrade-over-time** | Time-bound claims, link rot, stale stats, dated references |

If 3 of 5 domains don't apply to a specific output type, explicitly note "Not applicable — [reason]" and proceed with the relevant 2. Forcing weak coverage on misfitting domains produces noise, not signal.

Full worked examples in the premium reference. Output template (both modes) in the premium reference.

---

## Premortem

### Success state ({horizon})
{One sentence.}

### Failure modes (across {mode-specific domains})
- **{Domain}:** {failure mode} — *Likelihood: {L|M|H}.*
-...

### Mitigations (effort, owner)
- **{Failure mode}:** {mitigation OR explicit accept-risk}. (Effort {S|M|L}, owner: {who})
-...

### Carried-forward opportunities (mitigations that double as new ideas)
- {Opportunity 1}
-...

### Premortem confidence
**{L|M|H}.** {One-sentence rationale.}
```

Full template with both --plan and --output worked examples in the premium reference.

---

## Pairings

- **Upstream:** This is upstream of almost everything. /premortem --plan fires during plan mode; /premortem --output fires as the final step in every output skill body.
- **Downstream:** Plan mode feeds the ExitPlanMode hook. Output mode feeds whichever lens-reviewer applies (voice-reviewer for content; design-reviewer for visual; product-lens-reviewer for strategy; scope-guardian-reviewer for proposals).
- **Sister skills:** [`/steal`](../../learning/steal/SKILL.md) imports patterns including this one; [`/workflow-design`](../workflow-design/SKILL.md) designs multi-step prompts where premortem fits as a stage.

---

## Anti-patterns

- ❌ Invoking `/premortem` without a mode flag and getting a generic output. The skill should prompt for disambiguation, not synthesize.
- ❌ Stubbing the Premortem section as "No failure modes — trivial change" when the work isn't trivial. Defeats the gate.
- ❌ Forcing coverage on misfitting domains. If 3 of 5 don't apply, note it explicitly — better than weak coverage.
- ❌ Treating mitigations as work-creation. Mitigation can be "accept the risk" — that's a valid first-class outcome.
- ❌ Running /premortem on every typo fix. The trivial escape exists for a reason.
- ❌ Using /premortem as a post-draft review tool. That's what voice-reviewer, design-reviewer, product-lens-reviewer, scope-guardian-reviewer are for.

---

## Attribution

The "imagine failure first" cognitive frame is adapted from Nick Crew's [`Claude-Cortex/skills/collaboration/pre_mortem`](https://github.com/NickCrew/Claude-Cortex/tree/main/skills/collaboration/pre_mortem) (MIT license). The 5-domain taxonomies and mode split are Genesys-adapted per the /steal analysis at [`.claude/discovery/0526-cortex-premortem-steal-analysis.md`](../../../../discovery/0526-cortex-premortem-steal-analysis.md).

---

