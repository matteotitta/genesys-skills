---
name: outbound-send-orchestrator
version: '1.0'
last_updated: 2026-05-05
author: genesys-growth
description: 'Orchestrates the human-in-the-loop send phase of an outbound campaign. Parses a SEND_SHEET.md (from outreach-emails),
  creates Gmail drafts for every contact, then schedules per-contact Slack DMs to the operator at T+0 (email send reminder
  + LinkedIn URL + connect-task note) and T+24h next-weekday (LinkedIn 1/2 connect note + LI 2/2 followup copy inline). Enforces
  the load-bearing invariant that every Gmail draft must materialise BEFORE its matching Slack DM is scheduled, so the operator
  never gets a "send this now" ping without a draft to send. Built-in deliverability spacing (varied 11-18 min gaps, 9am-12pm
  send window, max 10/day, 24h email→LI delay, weekdays only). Triggered by "schedule sends", "fire the campaign", "send
  this batch", or "wire up the Slack reminders". NOT for autosend (use Apollo/HubSpot sequencers); NOT for marketing email
  blasts (use lifecycle-marketing).'
goal: Orchestrates the human-in-the-loop send phase of an outbound campaign.
outcome: N Gmail drafts + 2N Slack DMs (T+0 email reminder + T+24h-weekday LI followup with copy inline) wired to a SEND_SHEET.md,
  plus a SEND_SCHEDULE.md reference at campaign root. Operator clicks send when the ping fires.
primitive: outbound
sub_primitive: execution
ontology_type: outreach-sequence
review_gate: 2
inputs:
  required:
  - outreach-emails
  recommended:
  - deepline-enrich
- type: outreach-sequence
  feeds_into: []
depends_on:
- outreach-emails
owned_by_agent: operator
mcps_used:
- google-workspace
- slack
triggers:
  slash_commands:
  - /outbound-send-orchestrator
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 1
effort: medium
---

# /outbound-send-orchestrator — send sheet → Gmail drafts + Slack reminders

Closes the gap between "the email is drafted" and "the human actually sent it + did the LinkedIn followup 24h later." Reads a SEND_SHEET.md (the canonical output of `/outreach-emails` campaign mode), creates one Gmail draft per contact, then schedules two Slack DMs per contact: a T+0 reminder when it's time to click send, and a T+24h-weekday reminder with the LinkedIn 1/2 connect note + LI 2/2 followup copy inline.

**Imported via:** `/steal` analysis of [Andytoizer/agentoperator-outbound-engine](https://github.com/Andytoizer/agentoperator-outbound-engine) (2026-05-05). Cite-only — no LICENSE in source repo. Pattern attribution: Andy Toizer.

---

## When to run

Trigger on: "schedule sends", "fire this campaign", "wire up the Slack reminders", "send this batch", "hand off to me to send manually."

Do NOT use for:
- Autosend campaigns (use Apollo Sequences via `apollo:sequence-load`, HubSpot, Lemlist, Smartlead, Instantly — anything that fires emails without human review).
- Marketing email blasts to subscriber lists (use `/lifecycle-marketing`).
- LinkedIn-only campaigns with no email touch (the orchestrator pairs the two; LI-only doesn't need it).
- Single one-off emails (just create the Gmail draft directly).

---

## Prerequisites

- Validated emails (run `/deepline-enrich` first if any contact has a placeholder or unverified email).
- LinkedIn URLs for every contact (the T+24h DM includes the URL inline).
- Slack MCP (`mcp__087d4f9f-*__slack_schedule_message`) and Google Workspace MCP (`mcp__google-workspace__draft_gmail_message`) connected.
- Operator's own Slack user ID (for DM-to-self) — surface from `slack_read_user_profile` or the MCP tool description.

---

## The load-bearing invariant — read this once, then never violate

**Every Gmail draft must materialise BEFORE its matching Slack DM is scheduled.** Never the inverse.

If you schedule the Slack DM first and the Gmail draft creation fails, the operator gets a "send this now" Slack ping at 9:03 AM with nothing in their drafts folder. They scramble, can't find the draft, the moment passes, the email never goes. The invariant exists to prevent exactly this failure mode (documented in the source repo at `schedule-sends/SKILL.md` lines 65-69).

Enforcement in this skill: **for each contact, create the Gmail draft and confirm the draft ID came back, THEN schedule its two Slack DMs.** Do not batch all drafts then all DMs — pair them per contact.

A second invariant from the same source: **always pass an `htmlBody` to `draft_gmail_message`** (one `<p>` per paragraph in the plain body). Gmail auto-wraps plain-text bodies at ~76 chars, which makes emails look pre-formatted and pre-sent — exactly the AI-template tell we're trying to avoid.

---

## Steps

1. **Parse the send sheet.** Read SEND_SHEET.md and extract one entry per H2 (`## N. First Last — Title, Company`). Each entry must yield: contact name, title, company, email, subject, body paragraphs, LinkedIn URL, LI 1/2 copy, LI 2/2 copy. Format spec in the premium reference. **Count entries before fanning out** — if the count looks wrong, the markdown drifted; stop and reformat.

2. **Cross-check each entry has a LinkedIn URL.** The T+24h DM needs it. If missing, look it up from the campaign's `people/shortlist.json` or `/clay-search` output. If still missing, flag the contact with a ⚠️ and decide: skip the LI followup for that contact, or stop and source.

3. **Plan the timing grid.** Compute the send schedule per the premium reference:
   - First send: next weekday at 9:03 AM in the operator's local timezone (push to tomorrow if past today's 9 AM).
   - Per-day cap: 10 sends. Overflow rolls to next weekday.
   - Inter-send gap: random 11–18 min (non-uniform — avoids burst-send patterns).
   - LI followup: 24 hours after each email send, snapped to next weekday (Mon connects > Sat/Sun connects).
   - 9 AM – 12 PM send window only (cold email hit rates peak Tue-Thu mornings).

4. **For each contact (in order, NOT in parallel within a contact):**
   1. **Create the Gmail draft** via `mcp__google-workspace__draft_gmail_message` with `to`, `subject`, `body` (plain-text), and `htmlBody` (one `<p>` per paragraph in the plain body). Confirm a draft ID came back.
   2. **Only after draft confirmation** — schedule the T+0 Slack DM via `mcp__087d4f9f-*__slack_schedule_message` with the format from the premium reference (email send reminder + LinkedIn URL + connect-task note).
   3. **Then schedule the T+24h-weekday Slack DM** with the LinkedIn 1/2 connect note + LI 2/2 followup copy inline (per the premium reference).
   4. If any of (a)/(b)/(c) fails, stop the loop, surface the contact + error, and DO NOT proceed to the next contact. Partial completion is recoverable; out-of-order completion is not.

5. **Batch in parallel ACROSS contacts** (5–10 tool calls per message) for throughput. **Do not batch within a contact.** The invariant is per-contact ordering, not global ordering.

6. **Handle rate-limits gracefully.** Slack `slack_schedule_message` rate-limits ~4-5 per 15 seconds when fired in parallel. Retry individually. Gmail `draft_gmail_message` is more lenient but can also rate-limit on bulk batches. If a retry fails twice, stop the loop and surface.

7. **Write SEND_SCHEDULE.md** at the campaign root with a full timing table: contact / scheduled send time / scheduled LI followup time / subject / warnings. Include a Monday pager-map if the schedule spans a day where both email reminders + LI followups fire (Monday ends up dense after a Friday send).

8. **Confirm and gate.** Print summary: N contacts, N drafts created, 2N DMs scheduled, any rate-limit retries, any contacts skipped. Send sheet entries with placeholder emails (⚠️ flagged) carry the warning into their Slack DMs so the operator doesn't fire a LI followup on a contact whose email never went out.

---

## Deliverability built-ins (do not override without reason)

| Rule | Why |
|---|---|
| Varied 11–18 min gaps | Non-uniform timing avoids burst-send patterns on receive side |
| 9 AM – 12 PM send window | Cold email hit rates peak Tue-Thu mornings |
| Max 10/day | Well under Gmail reputation thresholds for manual-send accounts |
| 24h email → LI delay | Lets email engagement signal the LI accept; same-time is noisy |
| Weekdays only for LI delay | Mon connects get better accept rates than Sat/Sun |
| Human-click-to-send via drafts | Carries normal session signals vs bulk API send |

These constants are in the premium reference and can be tuned per campaign with explicit override.

---

## Common failure modes

- **Parse misses** — non-conforming H2 format silently drops contacts. Always count entries before fanning out (Step 1).
- **Slack rate limits** — `slack_schedule_message` rate-limits ~4-5/15s in parallel. Retry individually.
- **Weekend timestamp** — LI followup can land on Saturday if the next-weekday helper isn't applied. Audit timestamps in SEND_SCHEDULE.md.
- **Test gate skipped** — ALWAYS pilot with a 2-3 contact send before firing the full batch. Once Slack DMs are scheduled, editing them requires the Slack UI (and you have to click cancel on each).
- **Reminder without draft (DON'T SHIP)** — see "load-bearing invariant" above. Never fire a Slack DM for a contact whose Gmail draft failed.
- **Plain-text column wrap** — Gmail auto-wraps plain-text `body` at ~76 chars. Always pass `htmlBody`.

---

## Quality gate

Before reporting "done":

- [ ] N entries parsed = N entries in source SEND_SHEET.md
- [ ] N Gmail drafts created (one per parsed entry)
- [ ] 2N Slack DMs scheduled (one T+0 + one T+24h-weekday per parsed entry, minus any explicitly skipped)
- [ ] Per-contact ordering invariant respected (draft created BEFORE matching DMs scheduled)
- [ ] All `htmlBody` fields populated (no plain-text-only drafts)
- [ ] SEND_SCHEDULE.md written at campaign root with timing table + Monday pager-map (if applicable)
- [ ] Pilot mode used if this is the first campaign with this operator-Slack-channel pairing

---

## Handoff

| From | What flows in |
|---|---|
| `/outreach-emails` (campaign mode) | SEND_SHEET.md with approved drafts |
| `/deepline-enrich` | Validated emails (so no `⚠️` flags carry through) |
| `/clay-search` | LinkedIn URLs (so the T+24h DM has the URL) |

**Terminal step.** No downstream skill — the operator takes over from here, watching for the Slack DM at the scheduled time and clicking send in Gmail Drafts.

---

## Integration with the engagement workflow

Slots into the **sales pipeline** as the value-add follow-up cadence (the "negotiation & close" stage), and into an outbound campaign as the terminal phase after `/outreach-emails` produces the SEND_SHEET.md.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

