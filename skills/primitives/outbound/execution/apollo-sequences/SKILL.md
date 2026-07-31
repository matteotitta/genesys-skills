---
name: apollo-sequences
version: '1.0'
last_updated: 2026-04-08
author: genesys-growth
description: 'Searches, audits, and manages Apollo email sequences. Find sequences by name, add enriched contacts to existing
  sequences, remove contacts, check connected mailboxes, and audit sequence performance. Free — does not consume Apollo credits.
  Triggered by "add to sequence", "manage sequences", "sequence audit", "Apollo sequences", "enroll in sequence", or "remove
  from sequence". Upstream: outreach-emails for sequence content, deepline-enrich for validated contacts. NOT for creating
  new sequences or editing sequence steps (not supported by Apollo MCP yet).'
goal: Searches, audits, and manages Apollo email sequences.
outcome: Searches, audits, and manages Apollo email sequences. Find sequences by name, add enriched contacts to existing sequences,
  remove contacts, check connected mailboxes, and audit sequence performance. Free — does not consume Apollo credits. Triggered
  by "add to sequence", "manage sequences",...
primitive: outbound
sub_primitive: execution
ontology_type: outreach-sequence
review_gate: 1
inputs:
  required:
  - lead-scoring
  recommended:
  - outreach-emails
  - deepline-enrich
- type: sequence-audit
  feeds_into:
  - outreach-emails
depends_on:
- lead-scoring
- outreach-emails
owned_by_agent: operator
mcps_used:
- apollo-io
- deepline
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
context: fork
effort: low
---

# /apollo-sequences -- Manage Apollo email sequences

Search, audit, and manage Apollo email sequences. Add enriched contacts, remove contacts, check mailboxes, and review performance. All sequence management actions are free.

**Imported via:** `/steal` analysis of workflows.io Apollo x Claude Playbook (2026-04-08)

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`outbound-research-hygiene.md`](../../../../../rules/outbound-research-hygiene.md) — dated signals, no stale references, no prior-job hooks
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in apollo-sequences |
|---|---|---|
| **R1** | Source placement (three layers) | The skill manages sequences (orchestration), not body copy. When it reports performance, summary lives in working-doc form for internal review — no end-customer-facing surface. |
| **R3** | Product-update tone | When sequence-level reports surface "we shipped X" framing, it stays product-update, not "thrilled-to-announce." Carries forward into sequences generated downstream by `/outreach-emails`. |
| **R6** | CTA hierarchy | Sequence design respects per-stage CTA hierarchy — cold sequences end with discovery-call/sign-up primary; warm follow-ups end with product-action. Surfaced when adding contacts to the right sequence type. |
| **R9** | Action-oriented section names | "When to use / Pre-flight checks / Common operations" — verb-led. Preserve. |

---

## When to use

- Quick pulse check on all active sequences and their performance
- Finding the right sequence for a specific prospect or ICP
- Adding an enriched contact to an existing sequence
- Removing a contact from a sequence (replied, unsubscribed, wrong fit)
- Auditing a sequence before adding new contacts (duplicate check)

## When NOT to use

- Creating new sequences or editing steps (not supported by Apollo MCP yet)
- Writing outreach email copy -> `/outreach-emails`
- Enriching contacts before enrollment -> `/deepline-enrich`

---

## Credit usage

**FREE.** All sequence management actions are free.

---

## Limitations

- You can **search and manage** existing sequences.
- You **cannot create new sequences** or edit sequence steps/content via MCP (coming soon from Apollo).
- You **must use the exact sequence name** as it appears in Apollo. Search first to confirm.

---

## Pre-requisites for adding contacts

Before adding contacts to a sequence:
1. Contact must already exist in Apollo CRM (use Apollo MCP `apollo_enrich_person` or search saved contacts first)
2. You need a connected mailbox in Apollo
3. If unsure about mailbox, run "Show me my connected email accounts" first

---

## Framework

### Action 1: Search sequences

Use the Apollo MCP sequence search tool.

**Parameters:**
- `q_name`: keyword to search sequence names (optional — leave empty to list all)
- `per_page`: number of results (default 10)
- `page`: page number for pagination

**Present results as a table:**

| Sequence Name | Status | Contacts | Open Rate | Reply Rate | Last Activity |
|---|---|---|---|---|---|

### Action 2: Find the right sequence for a prospect

When the user describes a prospect profile:
1. Search all sequences
2. Review sequence names and stats
3. Recommend the best match based on the prospect's title, industry, and seniority
4. If no strong match, say so and suggest the closest option

### Action 3: Add a contact to a sequence

**Required info from user:**
1. **Sequence name** (exact match)
2. **Contact's Apollo ID or email** (must already exist in Apollo CRM)
3. **Sending mailbox email** (the connected email account to send from)

**Before adding, confirm:**
> "I'll add **[Name]** to the **[Sequence Name]** sequence, sending from **[mailbox]**. Proceed?"

**After adding, confirm success and note:**
- Contact is now active in the sequence
- First email will send according to the sequence's schedule

### Action 4: Remove a contact from a sequence

**Required info from user:**
1. **Sequence name** (exact match)
2. **Contact's Apollo ID or email**

**Before removing, confirm:**
> "I'll remove **[Name]** from the **[Sequence Name]** sequence. This cancels all pending emails but preserves engagement history. Proceed?"

### Action 5: Check connected mailboxes

Returns all linked email accounts with their IDs. Needed before adding contacts to sequences.

---

## Tips

- Always run a sequence search FIRST to confirm the exact name before adding or removing contacts.
- Before adding contacts to a sequence, check if they're already in it to avoid duplicate outreach.
- When removing contacts, engagement history (opens, clicks, replies) is preserved.
- If the user wants to add multiple contacts to the same sequence, batch the requests.
- Sequence search by name uses keyword matching. "Q1" will match "Q1 Outbound" and "Q1 ABM Campaign".
- For campaign-scale enrollment, run `/deepline-enrich` first to validate emails.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
