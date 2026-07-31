---
name: linkedin-personal-posts
version: '1.1'
last_updated: 2026-04-21
author: genesys-growth
description: 'Writes personal story LinkedIn posts for founders and SMEs using a 5-section storytelling format. Produces posts
  that build credibility and attract buyers through vulnerability and relatability. Triggers: "personal posts", "story posts",
  "personal LinkedIn series", "credibility posts", "founder story". Depends on linkedin-content-guide (ICP + offer) for audience
  targeting. NOT for educational or expert posts — use linkedin-expert-posts. NOT for case studies or promo — use linkedin-sales-posts.'
goal: Writes personal story LinkedIn posts for founders and SMEs using a 5-section storytelling format.
outcome: 'Writes personal story LinkedIn posts for founders and SMEs using a 5-section storytelling format. Produces posts
  that build credibility and attract buyers through vulnerability and relatability. Triggers: "personal posts", "story posts",
  "personal LinkedIn series", "credibility posts", "founder...'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 3
inputs:
  required: []
  recommended:
  - linkedin-content-guide
  - tov-guidelines
- type: linkedin-post
  feeds_into:
  - linkedin-comment
depends_on: []
- linkedin-comment
owned_by_agent: content
mcps_used: []
- notion
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

# LinkedIn Personal Posts

Generate a series of personal story posts that build credibility and attract buyers — using the 5-section storytelling template. Takes a LinkedIn content guide (ICP + offer + pains→goals) and hooks as context, then outputs 3-5 ready-to-post personal stories.

**Source:** Nick Broekema (Content Design) — "How I write personal stories to build credibility and attract" framework.

**Why personal stories?** They rank #1 in LinkedIn content effectiveness. The algorithm rewards them because they generate the highest engagement, longest dwell time, and most saves. They're also the hardest to fake — which is exactly why they work.

**How this differs from `linkedin-expert-posts`:** That skill handles educational/framework content. This skill is *exclusively* personal storytelling — a rigid 5-section template applied across a series of posts, each mapped to a specific ICP pain→goal pair.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (post body is end-customer-facing — no source tags), R3 (operator-direct first-person voice), R9 (5-section template steps verb-led).

---

## The 5-Section Personal Story Template

Every post follows this exact structure:

```
┌─────────────────────────────────────────┐
│ 1. PAINS ICP (OR PEERS) │
│ Hook with a mutual pain │
│ → Start with a shared struggle │
│ → Use words your audience uses │
│ → Use real examples so it resonates │
│ → Address real emotions/frustrations │
│ → Make the story relatable & sincere │
├─────────────────────────────────────────┤
│ 2. BREAK │
│ Let the post breathe │
│ → Breaks (re)gain attention │
│ → Breaks allow for "plot twists" │
│ → Breaks prevent boring writing │
│ → 1-3 short lines that shift energy │
├─────────────────────────────────────────┤
│ 3. SOLUTION │
│ Present the problem you solved │
│ → Describe the results of inaction │
│ → Show how tough it was for you │
│ → Show how you mastered this │
│ → Build credibility with evidence │
├─────────────────────────────────────────┤
│ 4. ICP'S IDEAL SITUATION │
│ Paint the outcome your ICP desires │
│ → Describe the solution's outcome │
│ → Paint a picture your ICP desires │
│ → Or: your peer's desire │
│ → Present the outcome as a solution │
│ → Make it exciting for your audience │
├─────────────────────────────────────────┤
│ 5. MOTIVATIONAL ENDING │
│ Close with purpose │
│ → Personal story = helping people │
│ → Personal story = attracting people │
│ → Personal story = encouraging people│
│ → Personal story = about what you do │
│ →...while building credibility + │
│ attracting simultaneously │
└─────────────────────────────────────────┘
```

---

## Claude Code Triggers

**Invoke this skill when user says:**
- "Write personal story posts for [client/person]"
- "Generate a personal post series"
- "LinkedIn credibility posts from my ICP"
- "Story posts from my content guide"
- "Personal posts that build authority"
- "Write a series of personal LinkedIn posts"

**Do NOT invoke when:**
- User wants educational/framework posts → Use `linkedin-expert-posts`
- User wants to build the ICP + offer first → Use `linkedin-content-guide`
- User wants LinkedIn comments → Use `linkedin-comment`
- User wants to optimize their profile → Use `linkedin-profile`
- User wants a single post (not a series) → Use `linkedin-expert-posts` or `linkedin-sales-posts`

---

## Inputs

### Required

| Input | Description | Source |
|-------|-------------|--------|
| **ICP context** | Pains→goals table, ICP description, offer statement | `linkedin-content-guide` output OR user provides manually |
| **Personal story seeds** | Real experiences, turning points, failures, lessons | User provides (prompted by story mining questions) |

### Optional (improve quality)

| Input | How It Helps |
|-------|--------------|
| **Voice profile / TOV guidelines** | Ensures posts match the author's actual voice |
| **Hooks library** | Provides proven hook formulas to draw from |
| **Proof points** | Real metrics, client names, outcomes to include |
| **Author's existing content** | Reference posts to match their style |

**If inputs are missing:** Ask for ICP context and personal stories. Use the story mining questions from the premium reference to extract story seeds from the author.

### Validation Checklist

- [ ] ICP pains are specific (not generic "they struggle with marketing")
- [ ] At least 3 personal story seeds provided (real experiences, not hypotheticals)
- [ ] Author identity is clear (who is posting)
- [ ] Goal is understood (build authority, attract buyers, grow audience)

---

## Process

3-phase flow: Story Mining → Series Generation → Quality & Variation Check. Each phase has explicit checkpoints and references the 5-section template above. Full step-by-step in the premium reference.

---

## AI-Speak Scan (Personal Story Edition)

Personal stories are WHERE AI writes worst. Scan every post for these tells:

| Pattern | Why it kills personal posts | Fix |
|---------|---------------------------|-----|
| **"X isn't Y. It's Z."** | THE #1 AI tell. Never use in personal stories. | Just state the point directly |
| **Wrapped bow ending** | Real stories don't resolve neatly | End on a question, open thought, or mid-realisation |
| **"Here's the thing:"** | AI transition tic, not how people tell stories | Cut entirely — just say the thing |
| **Uniform paragraph rhythm** | Stories meander, stall, speed up | Mix one-word lines with longer passages |
| **Progressive ClientCo** | "Each step taught me more" | Real growth meanders. Show the setbacks and dead ends directly. |
| **Wisdom narrator voice** | "Looking back, I realise..." as if writing memoir | Stay in the moment. "I didn't know it then." |
| **Humble-brag setup** | "I failed... but then I crushed it" | Sit in the failure longer. The lesson is the post, not the win. |
| **Generic motivation** | "Just start. Take the leap." | Specific > inspirational. What EXACTLY did you do? |
| **Story time.** as a break | Overused. Everyone does it. | Find your own break style. "Let me explain." / Just a line break. / A one-word reaction. |

---

## Nick's X-not-Y sweep (mandatory before delivery)

Added April 2026 in response to Nick Broekema's coaching feedback (see `feedback_no_x_not_y_hooks.md`). Before output, scan every line of the draft for false-contrast structures — the AI-Speak Scan above catches the most obvious forms, but the full sweep covers disguised variants.

Build a sweep table modelled on [0426-pmm-os-post.md](../../../../projects/genesys/content/execution/linkedin/linkedin-posts/0426-pmm-os-post.md) lines 79-96:

| Candidate sentence | Verdict |
|---|---|
| {exact line from draft} | {OK: positive declarative / OK: temporal transition / BANNED: rewrite} |

Check at minimum the hook, every reflection beat, every transition, and the closing line. Any line matching `"not X — Y"`, `"X. It's Y."`, `"isn't about X, it's about Y"`, `"Stop X. Start Y."`, or two-sentence parallels where the second sentence asserts the inverse of the first is **banned**. Rewrite to positive declarative + behavioural implication before output. Real dialogue quotes are exempt if the speaker actually said those words — but pick a different real quote when possible.

---

## Anti-Hallucination Guardrails

1. **Never invent the author's personal stories.** Every story must come from real experiences the author has shared. If no stories provided, ASK — don't make them up.
2. **Never fabricate metrics.** "My content generated $0" is powerful because it's TRUE. Don't invent numbers to make stories more compelling.
3. **Never add fake emotional details.** "Kid on the way" works because it happened. Don't add family/health/financial details the author hasn't shared.
4. **Mark placeholders clearly.** Use `[YOUR SPECIFIC EXPERIENCE HERE]` when a story detail needs the author's input.
5. **No composite stories.** Don't blend multiple experiences into one fictional narrative. Each post = one real story.

---

## Quality

Pre-delivery checklist covers template adherence, voice quality, format quality, series variety, coach's quality gates, and the 5-dimension refine rubric (hook strength, clarity, engagement potential, platform fit, authenticity — score per post; iterate any dimension ≤ 6). Gold standard worked example + full checklist in the premium reference.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

