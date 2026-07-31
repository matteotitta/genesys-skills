# The angle matrix — score angle × persona × awareness before you brief

Replaces "group into 3–5 distinct angles" (a vibe) with a scored grid that says **which angle, for which buyer, at which awareness stage, to test next — and the evidence behind the ranking.** It is a *prioritisation* artifact: it ranks the test queue. It does not predict winners — the A/B test (concept-first, per the test hierarchy) still decides that.

Adapted from the HeyOz "Fable 5 Ad Creative Sprint" scored angle matrix.

---

## The three axes

Two of the three come from upstream — do not invent them. Pull the persona set and the awareness tiers from `paid-campaign-strategy` (which reads `icp-behavioural`). Only the angle axis is authored here.

### Axis 1 — Angle (what the ad argues)

The five angle types, unchanged from the Creative Angle Framework in `process.md`:

| Angle | Argues |
|---|---|
| Pain point | the problem they live with |
| Outcome | the after-state |
| Social proof | others like them already chose this (verified metric/quote only) |
| Comparison | side-by-side vs the status quo or a competitor |
| Product demo | the thing working, in the UI |

### Axis 2 — Persona (who it argues to)

Pull the persona set `paid-campaign-strategy` named from `icp-behavioural` — champion vs economic buyer vs end-user, by job function / seniority. **Never invent a persona the strategy didn't name.** If the strategy names one persona, the matrix has one persona column; that is fine.

### Axis 3 — Awareness (how ready they are to act)

Bound to the funnel tiers the strategy already uses, mapped onto Schwartz's awareness ladder so the axis is portable across platforms:

| Ladder stage | LinkedIn tier | Google pillar |
|---|---|---|
| Unaware / Problem-aware | TOFU | Problem-aware |
| Solution-aware | MOFU | High-intent |
| Product-aware | BOFU | Brand / Competitor |
| Most-aware | Retargeting | Remarketing |

The awareness stage constrains the angle: a Product-demo angle wasted on a Problem-aware audience under-performs; a Pain-point angle on a Most-aware retargeting pool is redundant. The matrix surfaces those mismatches as low scores.

---

## The score (1–10 per cell)

Each candidate `angle × persona × awareness` cell gets a 1–10 composite from three evidence inputs — **and states the evidence next to the number.** A cell with an empty evidence column is not scored; it is a hypothesis.

| Input | Question | Raises the score when |
|---|---|---|
| **Resonance evidence** | Does this angle land for this persona at this awareness? | VoC, a competitor's winning ad, or account-audit history says yes |
| **Competition density** (inverse) | How crowded is this angle in the teardown? | White space — few or no competitors run it (the opening) |
| **Product fit** | Does the product actually deliver on this angle for this persona? | A real, provable capability backs it |

Bands:

| Score | Verdict |
|---|---|
| 8–10 | **Brief now** — evidence + white space + fit all present |
| 5–7 | **Test** — promising, one input weak; queue behind the 8–10s |
| 1–4 | **Park** — mismatch, saturated, or unprovable. Say why. |

Rank by score; the top cells become briefs (they feed Phase 3 of the brief as the angle set). Cap the brief set at what the budget can actually test — a floored account tests 2–3 concepts, not 30.

---

## Where the evidence comes from

- **Competition density** → [`linkedin-ad-teardown`](../../../strategy/linkedin-ad-teardown/SKILL.md) gap analysis — "the opening for {client}" is a white-space cell.
- **Resonance (account history)** → the weekly-run audit: [`paid-ads-report`](../../paid-ads-report/SKILL.md) fatigue + what's converting, and the change journal [`paid-ads-experiment-log`](../../paid-ads-experiment-log/SKILL.md).
- **Product fit + proof** → `product-messaging` value props + verified proof points (no invented stats).
- **Persona resonance** → `icp-behavioural` voice-of-customer.

---

## It ranks the test queue — it does not predict winners

Two guards keep the scores honest:

- **Volume floor** — per `quantitative-evidence-floors.md`: below the volume floor (≈1,000 impressions / 3 conversions per variant), a "resonance" score built on account history is *directional*, not a verdict. State the floor next to the score; a thin-data cell gets the "too early" caveat, not an 8.
- **Backwards-reasoning** — per `scoring-validity.md`: if the resonance evidence is a handful of past-winning ads, the matrix **describes past winners; it does not predict**. Score them, but label the ranking as hypothesis-generating, and let the concept-first A/B test (per `process.md` § A/B test hierarchy) be what actually crowns a winner. The matrix picks *what to test*; the test picks *what wins*.

---

## Banned-claim block runs first (client-scoped)

Inherit the client's banned-claim list **before** scoring. A blocked claim cannot be an angle no matter how high it would score.

- **Regulated clients** (those with advertising-claim rules): claims like transparent-pricing or performance guarantees may be blocked — and a copy library assembled before a rule change can still lead on exactly the now-banned claim. Inherit the client's banned-claim list, and park any angle that would resurrect a blocked claim with a `blocked` verdict, rather than scoring it.

---

## Output — the ranked matrix

Render the scored cells as one table, highest first, then hand the top band to the brief:

```markdown
## Angle matrix — {client} · {campaign} · {date}

| # | Angle | Persona | Awareness | Score | Evidence (resonance / density / fit) | Verdict |
|---|---|---|---|---|---|---|
| 1 | Comparison | Economic buyer | Product-aware (BOFU) | 9 | Rival white space (teardown §3) / 0 competitors run it / migration proof exists | Brief now |
| 2 | Outcome | Champion | Solution-aware (MOFU) | 7 | Converting angle last cycle (n=210, above floor) / medium density / strong fit | Test |
| 3 | Social proof | Champion | Problem-aware (TOFU) | 3 | No verified metric available | Park (unprovable) |
| — | {banned claim for this client} | any | any | — | — | Blocked (banned-claim list) |

Floor note: cells scored on <1,000 impressions/variant are directional. Winner decided by concept-first A/B test, not by this score.
```

The `Brief now` rows (and the strongest `Test` rows the budget allows) become the angle set the brief's Phase 3 writes visual direction for.

---

## Worked example

Personas from `icp-behavioural` (illustrative): a *principal* (economic buyer), a *compliance lead* (blocker-turned-champion). The teardown shows every competitor leading on Outcome ("save 3 hours"), nobody on Comparison-vs-status-quo. Matrix result: **Comparison × principal × Product-aware = 9** (white space + migration proof), **Outcome × compliance lead × Problem-aware = 4** (saturated + weak fit for a blocker persona). The brief writes the Comparison angle first; the Outcome angle is parked with the reason, not padded in to hit "≥3 distinct."

---

## Anti-patterns

- ❌ Inventing a persona or awareness tier the strategy didn't name — the axes come from upstream.
- ❌ An 8–10 score with no evidence in the row — the number without evidence is a guess.
- ❌ Treating the score as a predicted winner — it ranks the test queue; the A/B test decides.
- ❌ Crowning a cell on a handful of past winners (backwards-reasoning) — label it directional per `scoring-validity`.
- ❌ Scoring a blocked claim — the banned-claim list runs before scoring, not after.
- ❌ Briefing 30 cells because the matrix has 30 rows — cap at what the budget can test.
