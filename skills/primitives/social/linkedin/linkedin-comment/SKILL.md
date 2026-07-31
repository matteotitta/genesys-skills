---
name: linkedin-comment
version: '2.1'
last_updated: 2026-01-20
author: genesys-growth
description: 'Writes strategic LinkedIn comments for Matteo on target accounts'' posts. Produces relationship-building comments
  using audience merging and engagement reciprocity strategies. Triggers: "comment on this post", "LinkedIn comment", "write
  a comment", "engage with this post", "audience merging". Accepts post URL or pasted post content as input. Feeds into linkedin-social-selling
  for signal-based outreach conversion.'
goal: Writes strategic LinkedIn comments for Matteo on target accounts' posts.
outcome: 'Writes strategic LinkedIn comments for Matteo on target accounts'' posts. Produces relationship-building comments
  using audience merging and engagement reciprocity strategies. Triggers: "comment on this post", "LinkedIn comment", "write
  a comment", "engage with this post", "audience merging"....'
primitive: social
sub_primitive: linkedin
ontology_type: linkedin-post
review_gate: 2
inputs:
  required:
  - linkedin-content-guide
  recommended: []
- type: linkedin-post
  feeds_into: []
depends_on:
- linkedin-content-guide
owned_by_agent: content
mcps_used: []
triggers:
  slash_commands:
  - /linkedin-comment
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: low
---

# LinkedIn Comment

Generates strategic LinkedIn comments that build relationships through audience merging — high-value engagement that drives reciprocity and positions Matteo as a B2B SaaS GTM expert. Uses a 3-Sentence Framework (VALIDATE → EXPAND → HOOK) and the 100 Posts Test to filter generic AI-flavoured comments.

How it differs from `/linkedin-content`: that skill writes *posts*; this skill writes *comments on other people's posts* — relationship building, not broadcast. Comments shape your member embedding (algorithm-side) and trigger 5.2x amplification when discussion threads form between commenters.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md) (all 12 banned patterns enforced — generic praise openers, parallel-3 rhythm, X-not-Y, engagement-farming closers all banned). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (comment body is end-customer-facing — no source tags), R3 (operator-direct comment voice), R9 (3-sentence VALIDATE→EXPAND→HOOK structure verb-led).

## Reply style — lead with the move (locked 2026-06-16)

Calibrated on the GTME Cohort 4 thread-feedback batch. Four rules that override the validate-first habit when writing thread replies (and sharpen ordinary comments too):

1. **Lead with the constructive suggestion, not validation.** No name-opener, no opening acknowledgement or "you nailed X" stroke — those are the scripted-flattery tells. Just read, acknowledge briefly (woven in mid-reply, never fronted), and lead with something they can implement.
2. **First-person operator POV.** "this is what I'd do", "I'd rather focus on", "I'd build X first" — not "X is the right call" / "great instinct" / "you nailed it". You're sharing your own move, not awarding marks from the front of the room.
3. **Different structure per reply across a batch.** When a run produces more than one reply, every one takes a distinct shape — reframe-led, imperative-led, question-led, risk-led, scope-led, peer-amplify, sequencing-led. Same skeleton across a batch is itself an AI fingerprint the 100 Posts Test can't catch (it tests one comment in isolation, blind to cross-batch repetition).
4. **Still anchored.** Open on a specific phrase from their post, name one real bottleneck (not the obvious one), reference real peer replies by name where they exist, close on one concrete move. Voice anchors for cohort feedback: `projects/courses/gtme-school/course/0626-c4-exercise-1-feedback.md` + `0626-c4-week3-wip-feedback.md`.

## When to run

- "comment on this post" / "write a LinkedIn comment" / "engage with this post"
- "respond to LinkedIn post" / "reply to this post" / "help me comment"
- "comment ideas for [post]" / "comment strategy" / "LinkedIn engagement"

Also runs for thread-style replies on non-LinkedIn surfaces — LMS / cohort feedback, Slack threads, community replies — where the same human, anti-AI-speak discipline applies (per the standing memory rule on using this skill for thread replies). Apply the "Reply style — lead with the move" doctrine below for those.

Do NOT run when: user wants a LinkedIn post (`/linkedin-content`), a LinkedIn DM (`/outreach-emails` adapted), or general broadcast social content.

Full trigger list and input checklist: the premium reference.

## Inputs

**Required**

| Input | Description | Source |
|-------|-------------|--------|
| Post content | Full text of the LinkedIn post to comment on | User-provided (text or screenshot) |

**Optional (improves quality)**

| Input | How it helps |
|-------|--------------|
| Poster's profile/role | Calibrates tone and expertise level |
| Relationship context | Existing relationship affects warmth |
| Specific angle requested | Focuses the comment direction |
| Prior engagement history | Avoids repetition |

If only partial post content provided (e.g., screenshot truncation), ask for full text before generating. Verify post is appropriate for engagement (not controversial/risky).

## Steps

1. **Phase 1 — Post analysis.** Extract thesis (1-sentence), identify 2-3 quotable elements, select value-add angle (support / extend / answer / nuanced agreement / parallel story). → the premium reference Phase 1.
2. **Phase 2 — 3-Sentence Framework draft.** Sentence 1 VALIDATE (reference specific phrase from their post), Sentence 2 EXPAND (operator-perspective experience/data/insight), Sentence 3 HOOK (question or bold take). → the premium reference for framework, the premium reference for templates per type.
3. **Select comment type.** Value-add / Contrarian / Story drop / Bridge / Question-first / Insight drop. Pick by what genuinely fits the post and your expertise. → the premium reference.
4. **Apply voice rules.** Operator-first ("I've tested..." not "One could argue..."), direct (no throat-clearing), warm (first-person, genuine), proof-backed (numbers, results, specific examples). Skip corporate speak, hedging, passive voice.
5. **Phase 3 — Quality gates.** Run 100 Posts Test (could this apply to 100 other posts? → if yes, rewrite); verify no AI-detection phrases ("Great insights!", "This resonated"); confirm no pitching ("DM me", "I can help", "Book a call"); check word count 50-150 (max 200). → the premium reference for full list.
6. **Self-evaluation.** Comment references specific element from their post? Includes first-person operator experience? Stands out vs "Great post!"? No invented experiences/numbers/credentials? → the premium reference.
7. **Generate alternative version** (different angle/type) so user can compare and pick.
8. **Suggest thread continuation** (2-3 reply options if the poster responds) and DM follow-up plan after 3-4 exchanges. → the premium reference for signal prioritization, micro-commitment CTAs, voice notes.
9. **Format output** per canonical template (post analysis → comment → quality checks → alternative → reply suggestions). → the premium reference.
10. **Review gate Level 1 (Quick Review).** Present comment + word count + quality checks + alternative. Actions: [Approve] / [Different angle] / [Shorter]. On approval with positive engagement signal ("they replied!", "got a DM"), offer to save as reference example. → the premium reference.
11. **Suggest chains:** post-publish engagement routine for poster's content, `linkedin-social-selling` for signal-based outreach conversion, `outreach-emails` for thread → DM → email sequences.

Visual flowchart of the full process: the premium reference. Algorithm rationale (why strategic commenting compounds, GPU-RAR + 5.2x amplification + member embedding): the premium reference. 60-min post-publish engagement routine and weekly cadence: the premium reference.

## What good looks like

### Evaluations

The output passes when: comment references a specific phrase or data point from the post (not "great post"); includes first-person operator experience ("I've found...", "I tested...", with concrete numbers or timeframes); ends with a hook (question that invites response, or bold take that sparks discussion); passes the 100 Posts Test (could not be copy-pasted to 100 other posts); contains no forbidden AI phrases ("Great insights!", "This resonated", "Thanks for sharing"); contains no pitching ("DM me", "I can help", "Book a call"); word count is 50-150 (max 200); no invented experiences, fabricated numbers, or fake credentials. Full pre-delivery checklist: the premium reference.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
