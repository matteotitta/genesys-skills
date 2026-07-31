---
name: video-pipeline
version: '0.3'
last_updated: 2026-05-20
author: genesys-growth
description: 'Orchestrates raw video footage editing through a four-layer pipeline: AI plans the edit from transcript + intent → FFmpeg executes cuts → Remotion composes brand frames + captions → VideoDB indexes the source for findability. Produces brand-bound cliplets (LinkedIn vertical, YouTube short, podcast clip). Sibling to product-ui-frames (HTML→MP4) and onboarding-video (HTML→MP4) — this is the real-footage editing path. Triggers: "cut this podcast", "make a LinkedIn vertical from", "produce a cliplet of", "scrub this video for", "auto-edit this podcast episode". Pairs with gtme-podcast for cliplet production. STATUS: scaffold only — pending env setup (ffmpeg + Remotion + VideoDB key).'
goal: Orchestrate AI plan + FFmpeg + Remotion + VideoDB into one workflow that produces brand-bound cliplets from raw video footage.
outcome: 'A brand-bound MP4 cliplet (typically LinkedIn vertical 9:16, YouTube short 9:16, or LinkedIn square 1:1) cut from raw footage with brand overlay + captions + audio, plus a VideoDB index entry for source reusability.'
primitive: content
sub_primitive: motion
ontology_type: video-composition
review_gate: 3
inputs:
  required:
  - brand-kit
  recommended:
  - product-messaging
  - transcript-analysis
- type: video-composition
  feeds_into: []
depends_on:
- brand-kit
owned_by_agent: content
mcps_used: []
- gdrive
triggers:
  slash_commands: []
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
context: fork
effort: max
disable-model-invocation: true
---

# /video-pipeline — raw-footage editing through AI plan + FFmpeg + Remotion + VideoDB

**STATUS: scaffold only.** This skill ships as v0.1 with the workflow documented but NOT yet runnable. Activation is gated on:

1. `brew install ffmpeg` (the CLI dependency for cuts)
2. `npm install -g @remotion/cli` (the composition layer)
3. VideoDB API key registered in `.claude/apis/videodb-api-key.txt` (the indexing layer)
4. First proving run: produce a 60-second LinkedIn vertical from a recent GTM Engineer Pulse podcast episode

Sourced from 2026-05-17 MCP Market /steal Item D — consolidates the four upstream patterns `ai-video-production-pipeline`, `videodb-for-claude-code`, `ai-video-editing-workflow-1`, `video-editing-workflow-1` into one orchestrated Genesys skill.

---

## Why this skill exists

`product-ui-frames` and `onboarding-video` render HTML compositions to MP4 via Hyperframes — perfect for product UI animation, useless for editing actual filmed footage. Anything that involves real video sources (podcast cuts, webinar highlights, founder interview clips, customer testimonial videos) falls outside our current stack.

This skill closes the real-footage gap. It's the production pipeline that `gtme-podcast` was always missing.

---

## When to use

**Invoke when user says:**
- "Cut this podcast into a 60-second LinkedIn vertical"
- "Make a YouTube short from the [topic] section of [episode]"
- "Produce a cliplet of [guest] talking about [thing]"
- "Auto-edit this podcast episode for the punchiest segments"
- "Scrub this video for [keyword] and cut a 90-second clip"

**Do NOT invoke when:**
- The source is HTML/UI composition → use `/product-ui-frames` or `/onboarding-video`
- The source is just an audio file (no video) → use `/transcript-analysis` + downstream content skills
- The user wants a script for a video that doesn't exist yet → use `/youtube-scripts` or `/gtme-podcast`

---

## Input requirements

| Input | Required | Source |
|---|---|---|
| Source video file (mp4, mov) or URL | Required | User |
| Brand kit | Required | `brand-kit` output (the colors, fonts, overlay specs) |
| Intent: what segment, what platform | Required | User ("60-second LinkedIn vertical of the agent-dispatch section") |
| Transcript or transcript-search query | Recommended | `transcript-analysis` output or user query |
| Product messaging context | Recommended | `product-messaging` for hook framing |
| Target platform spec | Required | LinkedIn vertical (9:16, ≤60s), YouTube short (9:16, ≤60s), LinkedIn square (1:1, ≤90s), or custom |

---

## The four-layer pipeline

### Phase 1 — AI plans the edit (from transcript + intent)

1. Load the source's transcript (from `transcript-analysis` output or generate via VideoDB transcribe).
2. From the intent, identify the target segment (e.g., "the 60 seconds where the guest talks about why agents loop").
3. Use VideoDB semantic search to surface the timestamp range matching the intent.
4. Produce a structured edit plan:
   - Source in-point + out-point (HH:MM:SS.mmm)
   - Hook frame (the 1-2 second moment that opens the cut)
   - Caption track (verbatim from transcript, time-aligned)
   - Brand overlay specs (logo placement, color frame, end-card)
   - Aspect-ratio decision (9:16 vertical letterbox vs 1:1 square center-crop)

**Cost gate:** VideoDB transcribe + semantic search = `.claude/rules/videodb-credits.md` applies. Estimate before running.

### Phase 2 — FFmpeg executes the cut

5. From the AI edit plan, generate the FFmpeg command:
   - `ffmpeg -i source.mp4 -ss [in] -to [out] -vf "[aspect-ratio filter]" -c:a copy intermediate.mp4`
6. Run the cut (deterministic, no AI cost).
7. Verify output duration matches plan ±0.5 sec.

### Phase 3 — Remotion composes brand frames + captions

8. Load brand-kit tokens (colors, fonts, logo path, end-card template).
9. Generate Remotion composition that overlays:
   - Brand frame (color border, logo top-left)
   - Captions (time-aligned, burned-in for vertical platforms)
   - End-card (last 2 seconds: brand mark + CTA)
10. Render: `npx remotion render src/composition.tsx./out/final.mp4`.

### Phase 4 — VideoDB indexes the source for reuse

11. Upload the source video to VideoDB (if not already indexed).
12. Tag with metadata: source type (podcast / webinar / interview), date, guest, topics from transcript.
13. Store the index entry so future `/video-pipeline` runs can search "already indexed" before re-uploading.

**Cost gate:** Indexing has a per-minute fee. See `.claude/rules/videodb-credits.md`.

---

## Quality gate before ship

Per `design-production.md` skill authorship contract, every video-output skill must pass:

- [ ] Output duration ≤ target cap (60s for LinkedIn vertical / YouTube short, 90s for LinkedIn square)
- [ ] Aspect ratio matches platform spec (9:16 vertical, 1:1 square, etc.)
- [ ] Captions are time-aligned and verbatim from transcript
- [ ] Brand frame uses brand-kit tokens (no hardcoded colors)
- [ ] End-card includes CTA + brand mark
- [ ] No copyrighted music or audio in the cut (verify source rights)
- [ ] VideoDB index entry created with proper metadata tags
- [ ] Cost matches estimate within 20% (verify against `.claude/rules/videodb-credits.md` budget)

---

## Anti-patterns

- ❌ Skipping Phase 4 (indexing). Re-indexing the same source costs credits next time. Always index on first cut.
- ❌ Running auto-edit during exploration. Sketch the cut in transcript form (Phase 1) first; only then commit to the cut.
- ❌ Hardcoded brand colors in the Remotion composition. Always reference brand-kit tokens.
- ❌ Burning captions in for desktop platforms. Vertical (LinkedIn vertical, YouTube short, TikTok) = burned-in; desktop (YouTube long, LinkedIn newsfeed image) = subtitle file.
- ❌ Using VideoDB for sources you'll only cut once. If it's truly one-shot, transcribe via cheaper means and skip the index pass.

---

## Chain suggestions

After producing a cliplet:

- "Want me to draft the LinkedIn post that ships with this cliplet?" → `/linkedin-content-guide` + the cliplet path
- "Should I create the YouTube-short metadata (title, description, hashtags)?" → `/youtube-scripts` adaptation
- "Should I cascade this into other platform formats?" → `/content-operations` Platform-Native Adaptation Matrix

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

