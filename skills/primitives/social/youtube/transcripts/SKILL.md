---
name: transcript-analysis
version: '2.0'
last_updated: 2026-01-16
author: genesys-growth
description: 'Analyzes call, podcast, video, interview, or webinar transcripts to extract structured insights with anti-hallucination
  guardrails. Produces verbatim quotes with timestamps, speaker attribution, key themes (SCQA structure), and prioritized
  action items. Triggers: "analyze transcript", "summarize call", "extract quotes", "what did they say about X", "pull insights
  from this recording". Feeds into linkedin-content, storytelling, and expert-pov as source material. NOT for generating new
  content from scratch — use thought-leadership or linkedin-content instead.'
goal: Analyzes call, podcast, video, interview, or webinar transcripts to extract structured insights with anti-hallucination
  guardrails.
outcome: 'Analyzes call, podcast, video, interview, or webinar transcripts to extract structured insights with anti-hallucination
  guardrails. Produces verbatim quotes with timestamps, speaker attribution, key themes (SCQA structure), and prioritized
  action items. Triggers: "analyze transcript",...'
primitive: social
sub_primitive: youtube
ontology_type: transcript-insights
review_gate: 2
inputs:
  required: []
  recommended: []
- type: transcript-insights
  feeds_into:
  - icp-behavioural
  - tov-guidelines
depends_on: []
- icp-behavioural
- tov-guidelines
owned_by_agent: researcher
mcps_used: []
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
effort: high
---

# Transcript analysis

Extract structured, verifiable insights from long-form transcripts with strict anti-hallucination guardrails — every insight follows the Pyramid Principle (SCQA structure) and traces to a timestamped, speaker-attributed verbatim quote. The Iron Law: NO INSIGHT WITHOUT VERBATIM QUOTE. Pulls transcripts from Granola (meetings) and YouTube (videos) when MCPs are available; otherwise uses user-pasted text.

## Doctrine inherited (Step 7 — 0626 rollout, locked 2026-06-04)

Internal-reference skill — feeds insights to other skills. Applies [[feedback_execution_doctrine_refinements_step6]] R1 (inline verbatim quotes + timestamps stay — auditability is the Iron Law), R3 (insight framing operator-direct), R9 (verb-led section headings). R2/R5/R6/R7/R8 not applicable (no customer-facing surface).

## When to run

Invoke when the user says: "Analyze this transcript", "Extract takeaways from [transcript]", "Summarize this call", "Podcast summary", "Video transcript analysis", "Interview insights", "Webinar notes", "Extract key points from [content]", "What did they say about [topic]", "Meeting notes from transcript", "Conference talk summary", "Extract quotes from [transcript]".

Do NOT invoke for:
- Sales call win/loss analysis → `win-loss-analysis`
- Competitor research → `competitor-research`
- Quick 2-3 sentence summary → answer directly
- Creating new content from transcript → clarify (analysis vs. content creation); content goes to `linkedin-content` / `thought-leadership`

## Inputs

**Required:** Full transcript text (pasted, file, or pulled via Granola / YouTube MCP).

**Optional (improve quality):** speaker metadata (names, roles, companies); context (purpose, topic area, date recorded); focus areas (specific topics or questions to prioritize); output format (specific structure needed); analysis mode (full / quick takeaways / topic extraction / quote mining / speaker analysis — default: full).

**Validation gate before proceeding:**
- [ ] Transcript text provided
- [ ] Analysis mode confirmed (or defaulting to full)

If transcript missing, ask user to paste it or specify Granola meeting / YouTube URL to pull via MCP.

## Steps

1. **Identify transcript format.** Check for timestamps (HH:MM:SS / MM:SS / approximate / none), speaker labels, structure (continuous, segmented, Q&A). Output: format assessment. Cite per the premium reference Timestamp handling table.
2. **Map speakers.** Extract names from metadata if provided; identify from transcript cues ("Hi, I'm John..."); assign consistent identifiers (Speaker 1, Speaker 2 if unnamed). Output: speaker map. Apply Speaker identification rules in the premium reference.
3. **Segment content.** Break into logical sections; note topic transitions; map timestamp ranges to topics. Output: content segments.
4. **Extract verbatim quotes.** Pull key insights / data / metrics / specific claims / recommendations / opinions / predictions / memorable phrases. Output: raw quote library. Apply Iron Law — verbatim only, no paraphrasing.
5. **Tag each quote.** Timestamp (exact or approximate), speaker attribution, topic category, quote type (insight / data / advice / opinion / story). Output: tagged quote library.
6. **Synthesize SCQA insights.** Group related quotes; identify patterns; structure each insight using Situation → Complication → Question → Answer per the premium reference SCQA framework. Output: SCQA-structured insights with evidence quotes.
7. **Build topic hierarchy.** Cluster quotes by theme; create topic → subtopic structure; order by timestamp or importance. Output: topic tree.
8. **Prioritize insights.** Rank by importance and clarity; lead with most valuable; apply full SCQA to top 10-30 (transcript-length dependent).
9. **Extract proof points & metrics.** Pull specific numbers, claims, dates, milestones into a structured table (Metric | Value | Speaker | Timestamp).
10. **Self-evaluate.** All valuable quotes extracted? No invented content or paraphrasing? Speaker attribution on every quote? SCQA applied consistently? Apply Red flags table from the premium reference — STOP if any trigger fires. Mark inferences as "Implied:" or "Inferred:" never as quotes.
11. **Apply quality check.** Verify verbatim accuracy; confirm attribution; check no invented content; preserve quote context. Use the pre-delivery checklist in the premium reference.
12. **Format + present.** Use the premium reference exactly: header comment block → metadata → executive summary (3-5 sentences) → key insights (full SCQA per insight) → proof points & metrics table → topic hierarchy → analysis metadata. Review gate level 1 (quick review) — actions: [Approve] [Extract more] [Refine].
13. **Offer iteration prompts.** After delivery, surface refinement / expansion / quality prompts from the premium reference.

## What good looks like

### Evaluations

Pre-delivery checklist (full version in the premium reference):

**Evidence quality** — every insight follows SCQA; all quotes verbatim (no paraphrasing); all quotes have speaker attribution; timestamps included where source provides them.

**Analysis quality** — no invented content or quotes; proof points and metrics extracted as priority; executive summary captures essence accurately; quote context preserved (not misleadingly excerpted).

**Format quality** — speaker names/identifiers used consistently throughout; output header comment block present; topic hierarchy complete (when 5+ topics); proof points & metrics table populated.

**Iron Law check** — for every insight, point to the supporting quote with timestamp + speaker. If you cannot, the insight is not ready to ship.

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
