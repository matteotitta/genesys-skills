# Goals cadence template — `goals/MMYY-cadence.md`

Used by `/new-client` to seed the cadence file for new active clients. Materializes a Mon/Wed/Fri + biweekly + monthly + quarterly skeleton with placeholders for client-specific events.

Source: stolen from `growthenginenowoslawski/coldoutboundskills/skills/cold-email-weekly-rhythm/SKILL.md` via /steal Phase 5–6 ADAPT #2. Their original is outbound-specific; this template generalizes to any client engagement (PMM, content, lifecycle, paid).

---

## Doctrine — read this first

**The cadence is the schedule, not the reminder system.** This file is a markdown skeleton — it's not an automated reminder. The discipline comes from the user's own calendar.

What separates a client engagement that compounds from one that drifts is consistency: every Monday someone reviews metrics, every Wednesday someone sweeps positive replies, every Friday someone runs retros on completed work. Without a stated rhythm, every week is improvised, and the engagement decays.

**Step 1 (mandatory before this file is "active"):** put each cadence below into the user's actual calendar (Google Calendar, Outlook, Apple Reminders — whatever they look at every day). Recurring events. The calendar is the accountability system.

---

## Template (materialize this into `{client}/goals/MMYY-cadence.md`)

```markdown
# {Client name} — engagement cadence

**Engagement start:** {MMYY}
**Sprint length:** {1 or 2 weeks}
**Stakeholder review cadence:** {weekly / biweekly / monthly}

## Step 1 (required before this cadence is active)

Open the user's calendar. Create these as recurring events. Copy the titles and cadences exactly:

| Event title | Cadence |
|---|---|
| {Client}: Monday metrics review | Every Monday, 9:00 am |
| {Client}: Wednesday positive-signal sweep | Every Wednesday, 10:00 am |
| {Client}: Friday cycle retrospective | Every Friday, 3:00 pm |
| {Client}: Biweekly stakeholder check-in | Every other {day}, {time} |
| {Client}: Monthly performance review | 1st of each month, {time} |
| {Client}: Quarterly strategy review | First Monday of each quarter, {time} |

**The calendar is non-negotiable.** Without it, the cadence below is just a document; with it, it's an operating system.

---

## Monday — Metrics review (15 min)

**What to do:**

- Read {client}/`latest.md` for delta since last Monday
- Pull current-cycle KPIs from {client}/`goals/MMYY-NN-cycle.md`
- Check upstream skill outputs for new dated files (icp/, positioning/, messaging/, competitors/, etc.)

**Surface:**

- Any KPI tracking ≥10% off-target → flag to stakeholder
- Any locked-down output that's drifted from current data → flag for refresh
- Any new artifact since last week → annotate in latest.md

**Action:**

- If KPIs are off-target → run the relevant audit skill (`/website-audit`, `/content-audit`, `/paid-ads-audit`) to diagnose
- If everything's on-track → log a one-line entry in `history.md` and move on
- If a stakeholder needs a heads-up → draft a Slack/email; do not batch — same-day is the right cadence

---

## Wednesday — Positive-signal sweep (30-60 min depending on volume)

**What to do (engagement-dependent):**

- **Outbound engagement** → run `/reply-scoring` on active campaigns; surface positive_interested + positive_referral replies
- **Content engagement** → review LinkedIn DMs, AEO citation deltas, newsletter replies
- **Lifecycle engagement** → review new sign-ups, trial-to-paid conversions, churn signals
- **Sales-enablement engagement** → review CRM activity, deals advanced/lost since Monday

**Surface:**

- High-positive signals needing 30-second human response (replies, intros, hot leads)
- Hostile / negative signals (unsub spikes, hostile replies, churn) — risk flags
- Trends vs prior week (improving / flat / degrading)

**Action:**

- Respond to every high-positive signal within 30 seconds of seeing this. Speed > batch.
- For hostile/negative spike → run incident-response triage (per `audit-triage-pairing.md`)
- Append summary to current cycle's `goals/MMYY-NN-cycle.md` metrics section

---

## Friday — Cycle retrospective (20-60 min depending on cycle close)

**What to do:**

- For each campaign / artifact / experiment hitting its measurement window this week:
  1. Pull final metrics (positive_reply_rate via `/reply-scoring`, content engagement via dashboard, etc.)
  2. Compare to baseline + target from `goals/MMYY-scope.md`
  3. Decide: WINNER (scale) / MIDDLING (iterate) / LOSER (kill) per `references/grade-mapping.md`-style verdict
- Log retrospective to `goals/MMYY-NN-cycle.md` (NN = sprint number within month)

**Surface:**

- Wins worth scaling (clone the pattern to the next campaign)
- Losers to kill (free up budget / inbox / attention)
- Hypotheses for next sprint (what to test next per `experiment` skill)

**Action:**

- Use Friday's outputs as the input to Monday's planning
- If a stakeholder review is scheduled (biweekly / monthly), prepare the cycle summary now (Friday > Monday is the right slack window)

---

## Biweekly — Stakeholder check-in (45-60 min, prep + meeting)

**What to do:**

- Compile cycle summary from the last 2 weeks (winners / middlings / losers)
- Pull KPI trend chart from `goals/measurement.md` data sources
- Update `latest.md` with the talking points
- Run the meeting; capture decisions/asks in `history.md`

**Surface:**

- Did we move the KPI? (trend, not point-in-time)
- What's blocking us this sprint? (people, data, decisions)
- What does the stakeholder want to ramp / cut?

**Action:**

- Update `goals/MMYY-scope.md` if priorities shifted
- Capture any new dated artifacts requested (e.g., new `competitors/MMYY-newcompetitor.md`)
- Add follow-up tasks to next sprint's `goals/MMYY-NN+1-cycle.md`

---

## Monthly — Performance review (60-90 min)

**What to do:**

- Aggregate metrics across all sprints in the month
- Compare to monthly target from `goals/MMYY-scope.md`
- Identify month's top 3 wins + bottom 3 misses
- Write 1-page monthly retro: `goals/MMYY-monthly-retro.md`

**Action:**

- Update `latest.md` with month's headline result
- If quarterly cadence is approaching, queue the quarterly review prep
- If a recurring artifact is overdue (icp/, competitors/, brand/), schedule its refresh

---

## Quarterly — Strategy review (90 min, first Monday of each quarter)

**What to do:**

- Read all `goals/MMYY-monthly-retro.md` files from the last quarter
- Identify pattern wins (which campaigns / channels / messages compounded) and pattern misses (what kept failing)
- Re-validate ICP, positioning, messaging against the quarter's data — flag any locked-down output that should unlock + refresh
- Write quarterly retro: `goals/MMYY-Q{N}-retro.md`

**Output:**

- Top 3 things to scale next quarter
- Top 3 things to cut
- 3-5 hypotheses for next quarter's experiments (feeds `/experiment` skill, outreach domain → see `experiment/references/outbound-experiments.md`)
- Updated `goals/MMYY-scope.md` for the new quarter

**Action:**

- Schedule unlock + refresh of any locked-down upstream artifact (ICP, messaging, brand-kit, etc.)
- Reset sprint cadence in `goals/cadence.md` if the quarter's rhythm needs to shift (e.g., from 1-week to 2-week sprints)

---

## What to skip

You do NOT need to:

- Check metrics every day (Monday review catches the important stuff)
- Read every Slack ping in real time (Wednesday sweep is the system)
- Micromanage active campaigns — let the 21-day window settle before reacting
- Run quarterly retros early — wait for the quarter's data to be complete

Daily pokes at any single metric are a procrastination pattern, not a performance pattern.

---

## When this cadence breaks

If the cadence stops getting honored (calendar events declined for 2+ weeks running), do NOT just abandon it. Investigate:

- Is the cadence too aggressive for the engagement size? → reduce to weekly + monthly only
- Is the cadence falling on the wrong day? → ask the stakeholder for their preferred review day
- Is the engagement winding down (offboarding)? → trigger the handoff playbook instead

Update `goals/cadence.md` (this file) when the cadence shifts. The file is the source of truth for how the engagement is actually run.
```

---

## Customization notes for the AI

When materializing this template into `{client}/goals/MMYY-cadence.md`:

1. **Replace `{client name}`** with actual kebab-case client slug
2. **Set `sprint length`** based on engagement type:
   - 1 week for fast-moving content/outbound
   - 2 weeks for PMM strategy or ABM
   - 4 weeks (override) only for advisory/long-cycle engagements
3. **Set `stakeholder review cadence`** — usually biweekly for active engagements
4. **Customize the Wednesday block** based on engagement type:
   - Outbound → reply-scoring focus
   - Content → engagement metrics + AEO citation tracking
   - Lifecycle → conversion + churn focus
   - Sales-enablement → CRM activity focus
5. **Inline the actual calendar event titles** — these go directly into the user's calendar app, so name them well

The `goals/cadence.md` is a living document — expect it to evolve as the engagement shape becomes clearer.
