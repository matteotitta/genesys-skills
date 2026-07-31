---
name: event-pipeline
version: '1.0'
last_updated: 2026-07-28
author: genesys-growth
description: Turns an in-person event into pipeline across three phases - pre-event (qualify, build a capacity-capped hit
  list from the participant list, per-firm artifacts, layered cadence), at-event (mode-specific day routing, capture protocol,
  end-of-day CRM batch), post-event (segmented follow-up anchored on real conversations, cost-per-qualified-meeting review).
  Branches on attendance mode - sponsor, exhibitor, or attendee-only. Produces a full event brief plus the hit list, cadence
  and day plan. Triggers on "conference", "trade show", "event plan", "we are sponsoring X", "exhibiting at X", "booth",
  "roundtable", "summit". Consumes icp-research and product-messaging; feeds outreach-emails, one-pager and email-nurture.
  NOT for virtual events (use webinar-brief) or for a general account-based campaign with no event anchor (use abm-campaign).
goal: Turn a specific in-person event into a ranked, capacity-capped set of conversations and a follow-up motion that converts
  them.
outcome: An event brief containing the go/no-go call, the attendance mode, a hit list cut to real meeting capacity, per-firm
  artifacts for the top tier, a T-minus cadence, a routed day plan, a capture schema, and a segmented follow-up plan with
  its measurement floor.
primitive: product-marketing
sub_primitive: execution
ontology_type: launch-plan
review_gate: 2
inputs:
  required:
  - icp-research
  - product-messaging
  recommended:
  - lead-scoring
  - positioning
  - company-context
- type: launch-plan
  feeds_into:
  - outreach-emails
  - one-pager
  - email-nurture
depends_on:
- icp-research
- product-messaging
- outreach-emails
- one-pager
- email-nurture
owned_by_agent: growth
mcps_used:
- exa
- firecrawl
- apify
- spider
- gdrive
- notion
triggers:
  slash_commands:
  - /event-pipeline
  natural_language:
  - "plan our conference"
  - "we are sponsoring"
  - "exhibiting at"
  - "trade show plan"
  - "event follow-up"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# Event Pipeline

An in-person event is a system with a hard capacity constraint. One person holds roughly 12–16 meetings in a five-hour day. Everything upstream — how long the target list is, how many artifacts get built, how many people you chase — is a function of that number. Skills that skip it produce 200-row target lists for days with fourteen slots.

This skill is the in-person sibling of `webinar-brief`. That one is virtual and owns the run-of-show; this one is physical and owns the pipeline.

## Doctrine inherited

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md) and [`doc-output-structure.md`](../../../../../rules/doc-output-structure.md).

Also binding: [`crawl-cost-discipline.md`](../../../../../rules/crawl-cost-discipline.md) (free discovery before metered extraction), [`quantitative-evidence-floors.md`](../../../../../rules/quantitative-evidence-floors.md) (no ROI verdict below the floor), [`pii-redaction.md`](../../../../../rules/pii-redaction.md) (delegate data), [`outbound-research-hygiene.md`](../../../../../rules/outbound-research-hygiene.md) (dated signals only).

## When to run

**Invoke when:**
- "we're sponsoring / exhibiting at / attending [event]"
- "plan our conference" / "trade show plan" / "what do we do at [event]"
- "event follow-up" / "we just got back from [event]"
- Any physical gathering with a delegate list: conference, trade show, summit, roundtable, awards dinner, self-hosted meetup

**Do NOT invoke when:**
- The event is virtual → `webinar-brief`
- There is no event anchor, just a named account list → `abm-campaign`
- The ask is only the follow-up email copy → `outreach-emails`
- The ask is only a booth handout → `one-pager`

## Inputs

| Input | Required? | Source |
|---|---|---|
| Event name, date, venue, format | required | User, plus the event site |
| Attendance mode (sponsor / exhibitor / attendee-only) | required | User — drives the whole day plan |
| Headcount attending, and who | required | User |
| ICP definition | required | `icp-research` |
| Messaging + value props | required | `product-messaging` |
| Account scores | recommended | `lead-scoring`, or the client CRM |
| Client CRM + sending stack | recommended | Client CLAUDE.md — never assume; see the premium reference |
| All-in event cost | recommended | User — needed for the economics model |

If mode or headcount is missing, ask before anything else. Both change the arithmetic in step 2, and every later step depends on it.

## Steps

### Phase A — Pre-event

1. **Qualify and set the mode.** Go/no-go against audience fit and cost. Confirm sponsor, exhibitor or attendee-only. Each yields a different day, so this is not a label — it is the branch. See the premium reference.
2. **Set capacity.** Hours on site × headcount, split by mode: an exhibitor loses hours to stand duty; a sponsor gains access to private zones; attendee-only is fully mobile. Output: **N**, the number of real meeting slots. Every later number derives from N.
3. **Build the raw list.** Participant, exhibitor and speaker lists. Free discovery first (`spider_links`, sitemap) before any metered crawl — per `crawl-cost-discipline`. Many events publish the delegate list; check before buying one.
4. **Enrich and resolve.** Firms to named contacts, 2–3 per target account. Phone numbers acquired here go through the screening gate in the premium reference before any call.
5. **Score and rank.** Join the list to CRM account scores. Sort descending. Each row carries its reason: adviser count, recent acquisition, headcount, whatever the ICP actually keys on.
6. **Cut to capacity.** Take the top N from step 2, plus a reserve of roughly 50% for no-shows and chance encounters. This is the hit list. Everything below the cut is a post-event email, not a meeting target.
7. **Build per-firm artifacts for the top tier.** A firm-specific number from public data beats a pitch. Emailed pre-event as the reason to meet, shown from an iPad in the conversation. See the premium reference.
8. **Run the layered cadence.** Email at T-3 weeks, LinkedIn at T-2, phone or a light nudge the week of. Each touch references the event and the artifact. Timings and copy shape in the premium reference.
9. **Prep the booked meetings.** One short prep per confirmed meeting. Chain to `client-discovery`.

### Phase B — At-event

10. **Route the day.** Map the hit list onto the venue's zones and agenda, in time order, with travel between them. Mode decides the shape: an exhibitor anchors to the stand and sends one person walking; a sponsor works sessions and private lounges; attendee-only is all floor and pre-booked slots.
11. **Approach and capture.** Pre-read before each approach. Record where permitted. Capture the schema in the premium reference — contact, next step, and the **anchor**: the specific thing said that follow-up will cite. No anchor, no usable follow-up.
12. **End-of-day batch.** Notes → CRM → tomorrow's re-prioritised list. This is the step teams skip and the reason conversations evaporate. Chain to `transcript-analysis`.

### Phase C — Post-event

13. **Segment.** Met and warm / met and cool / booked-but-no-show / target-not-reached / met-but-out-of-ICP. Different segments get different sends; the last gets none.
14. **Follow up.** Within 48 hours, each message citing its anchor. Sequences via `outreach-emails`, sent per the client's actual stack, replies triaged by `reply-scoring`. See the premium reference.
15. **Measure and present at Gate 2.** Cost per qualified meeting, meetings held against N, pipeline sourced — with the volume floor stated. Feed the numbers back into the model for the re-book decision.

## Self-roast (run before ship)

- **Capacity honoured?** Is the hit list actually cut to N, or is it a wish list with a cap written next to it?
- **Anchors specified?** Does the capture schema force a citable moment, not just a business card?
- **Stack real?** Does every tool named appear in the client's CLAUDE.md, or did one leak in from a template?
- **Modes distinct?** Do sponsor, exhibitor and attendee-only produce visibly different day plans?
- **No invented delegates.** Never fabricate an attendee name, a firm's size, or an adviser count. Public register fields carry a pull date; anything else is `[UNAVAILABLE]`.
- **Benchmarks attributed.** Any external ROI figure names whose figure it is. Ours are the client's own numbers or nothing.
- Seven-tenet gate per [`output-tenets.md`](../../../../../rules/output-tenets.md).

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem`](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

## Persuasion & stickiness pass

Output complies with [`persuasion-and-stickiness.md`](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 levers + Heath's SUCCESs. For event outreach the levers that usually fit are **Scarcity** (a real, dated event with finite slots) and **Unity** (the shared professional room). Both are true here by construction, which is exactly why they must not be inflated: do not manufacture a "limited places" claim the event does not have. Run the SUCCESs diagnostic over the near-final copy, then the rule's pre-ship gate.

## MCP credit gate

This skill can call Apify, Exa and Firecrawl. Per [`crawl-cost-discipline.md`](../../../../../rules/crawl-cost-discipline.md), enumerate the participant list with free discovery (`spider_links`, sitemap, or a plain fetch of a published list) before any metered crawl, and triage to the kept rows before extraction. Per [`apify-credits.md`](../../../../../rules/apify-credits.md) and [`apollo-credits.md`](../../../../../rules/apollo-credits.md), enrichment is credit-spending and needs an estimate and a confirmation first. Searching is free; enriching is not.

