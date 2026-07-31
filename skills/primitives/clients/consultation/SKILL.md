---
name: consultation
version: "1.0"
last_updated: 2026-07-13
author: genesys-growth
description: |
  Interactive consultation-elicitation loop that turns a vague client or internal
  ask into a sharp, reviewed spec plus a copy-paste handoff prompt. Interrogates
  the ask one question at a time, maps gaps on a four-quadrant Known/Unknown board
  (living consultation doc), drafts a planning-doctrine spec, routes the adversarial
  review through /premortem, and emits a delimited handoff for a fresh execution
  session. Triggers: "scope this", "help me think through", "turn this into a spec",
  "consultation", "what do we actually need for X". Feeds into client-proposals and
  execution skills. Do NOT use for discovery-CALL prep (use client-discovery), for
  producing the proposal doc itself (use client-proposals), or for validating a
  business idea (use business-brainstorm).
goal: Turn a vague ask into a sharp, adversarially-reviewed spec plus a clean handoff prompt.
outcome: A scoped spec in planning-doctrine shape, a maintained four-quadrant gap board, and a delimited copy-paste handoff prompt an execution session can run without re-litigating decisions.
primitive: clients
sub_primitive: null
ontology_type: client-engagement
review_gate: 2
inputs:
  required: []
  recommended:
    - company-context
depends_on: []
owned_by_agent: b2b-consultant
mcps_used: []
triggers:
  slash_commands:
    - /consultation
  natural_language:
    - "scope this"
    - "help me think through"
    - "turn this into a spec"
    - "consultation"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
disable-model-invocation: true
---

# Consultation

Turn a vague ask — "ClientCo needs a new landing page", "we should refresh ClientCo's competitor set", "build me a skill that does X" — into a sharp, reviewed spec and a clean handoff, by interrogating the ask one question at a time and mapping what's known vs unknown.

This is the **elicitation front-end** our intake surface was missing. `/discovery` preps a human's prospect call; `/proposal` produces a doc from discovery notes; this skill is the interactive loop *between* a vague ask and a sharp spec.

---

## When to run

**Invoke when:**
- "Scope this" / "turn this into a spec" / "help me think through [X]"
- A client or internal ask is genuinely vague or high-stakes and would otherwise surface gaps halfway through execution.
- You're about to enter plan mode on something underspecified.

**Do NOT invoke when:**
- The ask is already sharp — a one-line clarification does the job. Skip the loop.
- You need discovery-**call** prep (question bank for a human to ask a prospect) → `client-discovery`.
- You need the proposal document itself → `client-proposals`.
- You're pressure-testing a *business idea* for viability → `business-brainstorm`.

---

## How it composes (do not reinvent these)

This skill is deliberately thin — it wires four existing Genesys systems into an elicitation loop:

| Stage | Delegates to | Why |
|-------|-------------|-----|
| Question shape | **`AskUserQuestion`** | Already the "2–4 options, one Recommended, one 'other'" convention |
| Inspect-before-asking preflight | **`brain-first-lookup`** | recall → grep client folder → path read, before pinging the user |
| Adversarial review of the spec | **`/premortem --plan`** (+ `scope-guardian-reviewer` for client-facing scopes) | Our review discipline is already hook-enforced — do NOT ship a competing 5-round reviewer |
| Spec format | **`planning-doctrine`** | The spec is a plan; use the canonical structure, not a bespoke one |

If you find yourself writing a bespoke reviewer or a new plan format, stop — that's the anti-pattern this skill exists to avoid.

---

## Inputs

| Input | Required? | Source |
|-------|-----------|--------|
| The vague ask | required | User provides (client request or internal build idea) |
| Client / target | recommended | Names the folder + brand voice to inspect |
| `company-context` output | recommended | Skips re-research for client scoping |

If the ask is missing, ask for it in one line. If it's already fully specified, say so and skip to the handoff.

---

## The loop

```
resolve working doc → questioning loop (gap-map) → draft spec → review (premortem) → handoff
```

1. **Resolve the working doc.** Client ask → `projects/consulting/active/{client}/docs/MMYY-{topic}-consultation.md`. Internal ask → a session scratchpad (or `~/.claude/plans/` if it's heading to plan mode). If a matching doc exists, ask continue-or-new. Seed it with the four-quadrant board below.
2. **Run the questioning loop** (details below) until no material unknown remains except client-accepted assumptions.
3. **Draft the spec** in `planning-doctrine` shape (Context → Goals → Outcome → Audience → Strategy → Use cases → Steps → Premortem → Resources).
4. **Review** — route the spec through `/premortem --plan` (and `scope-guardian-reviewer` if it's a client-facing scope). On BLOCKERS, never revise silently: bring each gap back as a numbered `AskUserQuestion`, update the board, redraft, re-review. Cap at 3 rounds, then present what remains and let the user decide.
5. **Print the handoff** — the delimited block below, with the real absolute spec path.

---

## The four-quadrant gap board (the working doc)

The consultation doc maintains these named sections, updated **before** each next question:

- **Brief** — the ask in one paragraph, as currently understood.
- **Known knowns** — stated facts and constraints.
- **Unknown knowns** — implicit taste and preferences, surfaced by *showing options* (this is the move — when taste is hard to verbalize, show 2–4 concrete references and let the choice reveal the preference; lean on the taste-library / a1-gallery / brand-kit for real artifacts).
- **Known unknowns** — named open questions.
- **Unknown unknowns** — blind spots you surface through expertise, `brain-first-lookup`, or inspecting the target territory (the client folder, the live site, the existing skill).
- **Decisions** — what's been settled, dated.
- **Next step** — a copy-paste next action, so any sitting can resume.

**Pre-seed the gap board.** When the ask targets a *known deliverable type*, seed Known-unknowns with that deliverable's required inputs from the ontology — e.g. scoping a landing page pre-seeds "positioning locked? messaging locked? brand-kit present? primary CTA? proof points?"; scoping a competitor refresh pre-seeds "which competitors? which dimensions? aggregate or per-competitor?". The gap board then partly drains as a checklist.

---

## The questioning loop

Repeat until no material unknown remains except client-accepted assumptions:

1. **Pick the highest-leverage gap** on the board.
2. **Inspect before asking** — run `brain-first-lookup` (recall → grep the client folder → read the path) to see if a fact or the territory already answers it. Don't ask the user what the workspace already knows.
3. **Ask one question** via `AskUserQuestion` — a single numbered question with 2–4 options, one clearly marked **(Recommended)**, plus the implicit "Other". Lead with options and your recommendation; the client owns taste and the final call.
4. **Update the board** — quadrants, Decisions, Next step — before the next question.

Rules: one question at a time (never batch a wall of questions); stop at the handoff, never start building; end every sitting with the doc current and a copy-paste next step.

---

## The spec (draft output)

The spec follows `planning-doctrine` canonical structure — **not** a bespoke format. Map the consultation into: Context (SQCA) · Goals · Outcome · Audience · Strategy · **Use cases** (named engagement + present-tense pain, per the use-cases doctrine) · Steps · **Premortem** (≥2 failure modes) · Resources. Client-facing scope docs additionally obey `doc-output-structure.md`.

---

## The handoff prompt

After review passes, print this verbatim (replace the placeholder with the real absolute path):

```text
---HANDOFF PROMPT START---
You are the execution session for the approved spec at `<absolute path to spec>`.

Read the spec and every reference it names. Implement it while preserving its
outcome, decisions, constraints, out-of-scope items, and open assumptions.
Inspect the target territory (client folder, live site, existing skill) before
changing it via brain-first-lookup; ask only if the spec leaves a true blocker.
Follow the relevant Genesys voice + doc rules, run /premortem --output before
ship, then report what changed, what passed, and any remaining risks.
---HANDOFF PROMPT END---
```

For an internal build that heads straight to plan mode, the "handoff" is simply: enter plan mode with this spec as the plan file.

---

## Self-roast (run before handoff)

- Anti-hallucination: mark unknowns `[PLACEHOLDER: …]`; never invent a client constraint, metric, or preference the consultation didn't surface.
- Composition check: review ran through `/premortem`, not a bespoke reviewer; the spec is in planning-doctrine shape, not a home-grown format; questions used `AskUserQuestion`.
- Quality pass: the four quadrants are current; every Decision is dated; the Next step is copy-paste; the seven-tenet gate (`output-tenets.md`) passed.
- Skip check: if the ask was already sharp, did I avoid adding ceremony?

---

## Integration with other skills

| Skill | Relationship |
|-------|--------------|
| **company-context** | Inspect-before-asking source for client scoping |
| **client-proposals** | A locked client scope feeds the proposal |
| **premortem** | Owns the adversarial-review stage (composed, not reinvented) |
| **business-brainstorm** | Sibling for *idea* validation (this skill scopes an *already-decided* ask) |

---

## Attribution

The consultation-elicitation loop — the four-quadrant Known/Unknown gap board, one-question-at-a-time questioning, "surface implicit taste by showing options," "inspect before asking," "lead with options + a recommendation," "never revise silently," and the delimited handoff block — is adapted from the `consultant` skill in [`eliasstravik/skills`](https://github.com/eliasstravik/skills) (MIT, © Elias Stravik, accessed 2026-07-13). Concepts re-voiced; the review + plan-format stages are Genesys-native. See `.claude/discovery/0726-eliasstravik-skills-steal-analysis.md`.

---

