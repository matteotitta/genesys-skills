---
name: linkedin-expert-posts
version: '1.3'
last_updated: 2026-06-17
author: genesys-growth
description: 'Writes authority/MOFU LinkedIn posts — contrarian takes, expert frameworks, industry analysis, and opinionated
  POVs. Produces posts optimised for saves and credibility rather than direct conversions. Triggers: "thought leadership post",
  "expert post", "hot take", "framework post", "industry take", "contrarian take". Optionally consumes linkedin-content-guide
  and linkedin-hooks for ICP alignment. Feeds into linkedin-algo-audit for quality gating. NOT for personal stories — use
  linkedin-personal-posts. NOT for case studies or selling — use linkedin-sales-posts.'
goal: Writes authority/MOFU LinkedIn posts — contrarian takes, expert frameworks, industry analysis, and opinionated POVs.
outcome: 'Writes authority/MOFU LinkedIn posts — contrarian takes, expert frameworks, industry analysis, and opinionated POVs.
  Produces posts optimised for saves and credibility rather than direct conversions. Triggers: "thought leadership post",
  "expert post", "hot take", "framework post", "industry...'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 2
inputs:
  required: []
  recommended:
  - linkedin-content-guide
  - linkedin-hooks
  - voice-reviewer
- type: linkedin-post
  feeds_into:
  - linkedin-algo-audit
depends_on: []
- linkedin-algo-audit
owned_by_agent: content
mcps_used: []
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: medium
---

# LinkedIn Expert Posts

Write authority-tier LinkedIn posts that build topical credibility and trust with your ICP. This skill covers the MOFU layer — between broad personal stories (TOFU) and sales-conversion posts (BOFU). These are the posts that make people save, share with their team, and think "this person gets it."

---

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md) (banned X-not-Y hooks, no engagement-farming closers). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (post body is end-customer-facing — no source tags), R3 (capability-led framing), R6 (MOFU close = read more / blog as fallback; never engagement-farming question), R9 (claim-led hooks per Step 6).

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "contrarian take"
- "hot take on [topic]"
- "expert framework post"
- "industry analysis"
- "opinionated post"
- "thought leadership"
- "breakdown of [topic]"
- "prediction post"
- "what most [role]s get wrong"

**Do NOT invoke when:**
- User wants personal story posts → use `linkedin-personal-posts`
- User wants case study / client proof → use `linkedin-sales-posts`
- User wants a post about their product/offer → use `linkedin-sales-posts`
- User wants hook variations only → use `linkedin-hooks`

---

## Inputs

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **Topic/angle** | The expert view or framework to present | User provides |
| **Pillar** | Which content pillar this serves (Authority/MOFU) | Inferred or user confirms |

### Optional (improve quality)

| Input | How it helps |
|-------|--------------|
| Supporting proof | Data points, research, personal observations, named examples |
| Audience context | Who the ICP is — helps calibrate the contrarian angle |
| Preferred post type | One of the 5 post types below |

**Validation:**
- [ ] There is a genuine expert POV to express (not just summarizing the obvious)
- [ ] The user has standing to make this claim (from experience, data, or reasoning)
- [ ] If using statistics or research — source is real and citable

---

## Post Type Selector

Choose the format that best matches the topic and angle:

| Post Type | When to use | Characteristic |
|-----------|-------------|----------------|
| **Contrarian take** | Challenging accepted wisdom | "Everyone says X. Here's why they're wrong." |
| **Framework post** | Explaining a system or model | "The 3 things [role] get wrong about [topic]" |
| **Industry analysis** | Interpreting data or market signals | "LinkedIn's algorithm changed. Here's what the data says." |
| **Expert breakdown** | Deconstructing complexity for the ICP | Step-by-step explanation of something hard |
| **Prediction / hot take** | Forward-looking, opinion-driven | "This GTM tactic is dying. Here's what replaces it." |

Detailed structures + common mistakes per type in the premium reference.

---

## Base Structure (all 5 types)

Voice-locked structure — this stays in body.

```
Hook (1-2 lines)
→ Stop the scroll. Contrarian or specific. No "Here's the thing:" openers.

Contrarian thesis (1-3 lines)
→ State your actual position. Don't hedge. Don't use "X isn't Y. It's Z." — just state the point.

3 supporting points (with proof)
→ Each point anchors the thesis with evidence, observation, or named example.
→ At least one point should be counterintuitive.

Reframe (1-3 lines)
→ What does the reader now see differently? How does this shift their mental model?

Opinion-driven CTA
→ Ask a question that invites debate, not a pitch. "What's your take?" or "Am I wrong here?"
→ Never end with "DM me" or a product pitch.
```

---

## Voice and Format Rules

- Short sentences. One idea per line.
- Vertical format with line breaks.
- No bullet soup — use arrows (→) for lists, not hyphens.
- Contractions OK ("you're", "it's", "they're").
- First-person "I" for personal observations; avoid "we" unless citing a team.
- Run Dimension 7 (anti-AI-speak) check — no false contrast reframes, no "Here's the thing:", no wrapped bow endings.

### Nick's X-not-Y sweep (mandatory before delivery)

Before output, scan every line of the draft for the banned false-contrast patterns (per `feedback_no_x_not_y_hooks.md`). Build a sweep table as shown in [0426-pmm-os-post.md](../../../../projects/genesys/content/execution/linkedin/linkedin-posts/0426-pmm-os-post.md) lines 79-96:

| Candidate sentence | Verdict |
|---|---|
| {exact line from draft} | {OK: positive declarative / OK: temporal transition / BANNED: X-not-Y — rewrite} |

Check at minimum the hook, thesis line, each supporting-point transition, reframe line, and closing CTA. Any line matching `"not X — Y"`, `"X. It's Y."`, `"isn't about X, it's about Y"`, `"Stop X. Start Y."`, or two-sentence parallels where the second sentence asserts the inverse of the first is **banned**. Rewrite to positive declarative + behavioural implication before output.

---

## Process

3-phase flow: Select Post Type → Write the Post (using the base structure above) → Apply Voice and Format Rules (incl. X-not-Y sweep). Per-post-type formulas, structures, and common mistakes in the premium reference.

---

## Coach's Quality Gates (March + April 2026)

Voice-locked rules — these stay in body.

- [ ] **G1: Less is more** — zoom in on one thing, don't overview 5 steps
- [ ] **G3: Each step could be its own post** — flag if 4+ numbered steps
- [ ] **G6: Hook is not a question with a predictable answer** — "Should I make this public?" is friction-banned. If the hook is a question, confirm the answer isn't already obvious from the body.
- [ ] **G7: Never link to someone else's domain** — own your ecosystem
- [ ] **G8: Pipeline CTA, not engagement CTA** — "What's your take?" is fine; "What's your experience with X?" is not pipeline
- [ ] **G9: Stats formatted as scannable bullet lists**, not inline sentences
- [ ] **G10: Visual recommendation included** (1080 x 1350 portrait)

---

## Anti-Hallucination Guardrails

1. **No invented statistics.** If you need a data point, ask for one or mark as `[Data point needed]`.
2. **No fabricated case studies.** Use "a client I worked with" only if the user provided that context.
3. **No invented research citations.** If referencing a study, name the real source.
4. **Mark speculation clearly.** Use "In my experience..." or "What I'm seeing..." for personal observations.

---

## Gotchas

- **Generic hooks:** Opens with "Most people think X but actually Y" without ICP-specific language → Hooks must use the ICP's vocabulary and reference their specific pain points.
- **Framework without insight:** Presents a 4-step framework that's all structure, no unique perspective → The framework should contain at least one contrarian or non-obvious element that demonstrates real expertise.
- **Missing saves optimization:** Writes for engagement (likes/comments) when expert posts should optimize for saves/bookmarks → Include a takeaway dense enough that people want to reference it later.
- **Too salesy for MOFU:** Sneaks in product mentions or CTAs that break the authority-building intent → Expert posts build credibility. Sales happens in sales posts. Keep them separate.

---

## Quality

Pre-delivery checklist covers content quality, voice quality, format quality, and the 5-dim refine rubric (hook strength, clarity, engagement potential, platform fit, authenticity — score each, iterate any ≤ 6). Anti-examples in the premium reference.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

