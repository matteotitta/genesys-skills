---
name: skill-of-the-week
version: '1.2'
last_updated: 2026-06-08
author: genesys-growth
description: 'Writes weekly "Skill of the Week" newsletter editions for Genesys Growth (newsletter.genesysgrowth.com). Publishes
  the featured skill to the public genesys-skills repo FIRST (cleaned per the public-repo-publish protocol), then produces a
  deep-dive article, two ASCII charts (speed + concept), and a companion LinkedIn post. Bundle publishes to Notion (canonical
  review surface); a post-approval Substack draft closes the loop. Triggers: "skill of the week", "write newsletter for [skill]",
  "next newsletter", "Genesys newsletter". NOT for GTM Engineer Pulse — use gtme-pulse instead.'
goal: Writes weekly "Skill of the Week" newsletter editions for Genesys Growth (newsletter.genesysgrowth.com).
outcome: 'Weekly "Skill of the Week" edition: featured skill published to the public genesys-skills repo first, then a deep-dive
  article, two ASCII charts, and a companion LinkedIn post — bundled to Notion for Matteo''s review.'
primitive: social
sub_primitive: newsletter
ontology_type: newsletter
review_gate: 2
inputs:
  required: []
  recommended:
  - linkedin-expert-posts
  - linkedin-hooks
  - voice-reviewer
- type: newsletter-draft
  feeds_into:
  - gdrive-create
- type: concept-chart
  feeds_into:
  - gdrive-create
- type: ascii-chart
  feeds_into:
  - gdrive-create
- type: linkedin-post
  feeds_into:
  - linkedin-weekly-content
depends_on: []
- gdrive-create
- linkedin-weekly-content
owned_by_agent: operator
mcps_used:
- notion
- slack
- github
- notion
- github
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

# Skill of the Week Newsletter

Write and publish the weekly "Skill of the Week" newsletter for Genesys Growth. Each edition features one Claude Code skill with a deep-dive article explaining the methodology, a before/after ASCII chart for Carbon.now.sh formatting, and a companion LinkedIn post. The featured skill publishes to the public `genesys-skills` repo BEFORE drafting, so the CTA URL is live when the article needs it.

For the full process (selection / publish / draft / charts / LinkedIn / Notion / output / Substack draft) → the premium reference.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Output complies with [`output-tenets.md`](../../../../../rules/output-tenets.md), [`output-simplicity.md`](../../../../../rules/output-simplicity.md), [`ai-speak-anti-patterns.md`](../../../../../rules/ai-speak-anti-patterns.md). Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]].

**Refinements applied:** R1 (newsletter is end-customer-facing — sources convert to inline links), R2 (newsletter + LinkedIn post + ASCII chart ship as one multi-asset deliverable with toggles), R3 (skill-feature framing capability-led), R5 (newsletter article opener anchors the LinkedIn post verbatim), R6 (newsletter close → sign-up to Genesys mailing primary, GTM-E cohort as fallback), R9 (verb-led section headings).

---

## Process at a glance

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Phase 1 │───▶│ Phase 1b │───▶│ Phase 2 │───▶│ Phase 3 │
│ Skill │ │ Public │ │ Newsletter │ │ ASCII │
│ Selection │ │ Repo Pub. │ │ Draft │ │ Charts │
└─────────────┘ └─────────────┘ └─────────────┘ └──────┬──────┘
                                                                │
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────▼──────┐
│ Phase 7 │◀───│ Phase 6 │◀───│ Phase 5 │◀───│ Phase 4 │
│ Substack │ │ Output + │ │ Notion │ │ LinkedIn │
│ Draft ⌥ │ │ Tracker │ │ Publish │ │ Post │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
                    ⌥ = post-approval only — Matteo presses send
```

| Phase | Purpose | Output |
|-------|---------|--------|
| **1. Selection** | Pick skill from tracker, study its SKILL.md, identify manual process it replaces | Skill chosen, manual process mapped |
| **1b. Public repo publish** | Clean-copy the skill to `genesys-skills` per the premium reference and push — FIRST, so the CTA URL is live | Public skill URL + `SKILL_NUMBER` |
| **2. Draft** | Write the deep-dive article in Matteo's voice | `newsletter.md` |
| **3a. Speed chart** | Generate before/after chart for Carbon.now.sh | `ascii-chart.txt` (~85 chars wide) |
| **3b. Concept chart** | Generate inline argument-anchored chart embedded in `newsletter.md` body | `concept-chart.txt` + inline fenced block (~74 chars wide) |
| **4. LinkedIn post** | Chain to `linkedin-expert-posts` for the companion piece | `linkedin-post.md` (post + first comment + image note + self-check) |
| **5. Notion publish** | One child page under the Genesys Growth parent (newsletter + LinkedIn + chart); manifest line written back per `notion-protocol.md` | Notion page URL |
| **6. Output + tracker** | Save all to `CWW-skill-name/`, Slack DM Matteo, update tracker | Subfolder + Slack message |
| **7. Substack draft** ⌥ | POST-APPROVAL: produce `substack-ready.md` + browser-create the Substack DRAFT per the premium reference. Never send — Matteo presses send | Substack draft URL |

---

## Triggers

**Invoke when user says:**
- "skill of the week"
- "write newsletter for [skill]"
- "next newsletter"
- "Genesys newsletter"

**Do NOT invoke when:**
- User wants GTM Engineer Pulse → use `/gtme-pulse`
- User wants a generic newsletter on a topic → write directly
- User wants only a LinkedIn post about a skill → use `/linkedin-expert-posts`

---

## Voice & quality rules

| Rule | Detail |
|------|--------|
| Voice | Matteo's — operator-first, direct, warm but challenging |
| Headline | Action-oriented, NOT the skill name |
| Buzzwords | None — banned: "innovative", "solutions", "leverage", "synergy" |
| Newsletter length | ~1,400–1,800 words (C23/C24 shipped range) |
| LinkedIn post | 400–1,100 words (Matteo's empirical range per Broekema; supersedes the old 1,500-char cap — both shipped posts exceed it), no emojis, no "DM me" CTA |
| LinkedIn CTA | Newsletter link lives in the FIRST COMMENT, not inline (algo-friendly); body says "link in the first comment" |
| Skill count claim | "skill #N in the public library" = the row count of the public README Skills table after this run's append — never estimated |
| 100 Posts Test | Both newsletter and LinkedIn post must pass |

---

## Worked-example doctrine ("See it in action")

1. **First preference — self-applied.** If the skill can plausibly run on Genesys's own business or workspace (most can), write the example as "I ran this on my own X" — the audit-on-myself shape (C23 ran `/level` on the workspace; C24 ran `/win-loss` on Genesys's own client book). Source real patterns from the matching `projects/genesys/{folder}` locked outputs when they exist.
2. **Confidentiality gate.** Public content never names clients, prospects, people, or deal values, and never reproduces verbatim client quotes — generalize to role/stage shapes ("a client", "a funding cycle", "their first in-house hire"). The lesson and the process are shareable; identities and quotes are not.
3. **Fallback.** A fictional company clearly framed as illustrative, or a named public B2B SaaS company — but never present invented numbers as real results.

---

## Anti-Hallucination Guardrails

1. **Use real, named B2B SaaS examples** — concrete data points, specific findings. No generic "a typical company" framing.
2. **Time estimates must be realistic** — don't inflate manual-process times to make the skill look better.
3. **GitHub URLs must resolve** — verify the SKILL.md path in `.claude/skills/[category]/[skill-name]/SKILL.md`.
4. **No invented Slack messages** — the actual Slack notification is sent via the Slack MCP, not transcribed.

---

## Integration with Other Skills

| Skill | Relationship | Usage |
|-------|--------------|-------|
| **linkedin-expert-posts** | Downstream | Generate the LinkedIn companion post |
| **linkedin-hooks** | Downstream | Pull hooks for the LinkedIn post |
| **voice-reviewer** | Quality gate | Run before publishing |
| **Notion publish** | Downstream | One child page under the Genesys Growth parent per `notion-protocol.md` (canonical review surface — replaced the GDrive export June 2026) |

---

## Cloud routine

The weekly cadence runs via a cloud Routine — see [`.claude/automation/skill-newsletter/`](../../../../automation/skill-newsletter/). The routine's prompt body is at `prompt.md` in that folder; manual-registration handoff at `REGISTER-IN-CLOUD-UI.md`.

The routine (v2, June 2026) runs the same pipeline as this SKILL.md — publish-first, both charts, Notion publish — under one framing rule: **autonomous production, human-gated publication.** Matteo is the final reviewer and judge; the routine ships review-ready drafts to Notion with run-linked Slack + email notifications, and the newsletter send + LinkedIn post wait for his approval (the GitHub skill publish stays autonomous behind the public-repo-publish cleaning gates). Phase 7 (Substack draft) is manual-session only — the cloud routine has no browser. Edit `prompt.md` first when tuning the routine, then re-paste into the cloud UI — the disk edit alone changes nothing live.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

