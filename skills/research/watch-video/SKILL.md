---
name: watch-video
version: '1.0'
last_updated: 2026-07-08
author: genesys-growth
description: 'Transcribes and analyzes any video from any source — YouTube, Loom, Vimeo, Riverside, Zoom recordings, webinars, competitor and ad videos — at a chosen depth, then produces a clean timestamped transcript, timestamped key moments, and a summary flagging action items, decisions, and quotable lines. v1 is transcript-first: YouTube captions via the youtube-transcript MCP, other-platform captions via Firecrawl or WebFetch; local-Whisper transcription and multimodal frame-plus-vision analysis are deferred. Every extracted claim quotes the source per evidence-bound-outputs. Triggers: watch video, transcribe video, analyze video, video notes, summarize this recording, key moments from this Loom, what happened in this video. NOT for deep YouTube-only transcript insight-extraction — use /transcripts. NOT for sales-call win/loss — use /win-loss.'
goal: Transcribe and analyze any video from any source into a clean transcript, timestamped key moments, and an action-item, decision, and quote summary.
outcome: A dated transcript-insights artifact — a cleaned timestamped transcript, a key-moments list, and a summary of action items, decisions, and quotes — ready to feed content-strategy and thought-leadership or be captured to the taste-library.
primitive: research
ontology_type: transcript-insights
review_gate: 1
inputs:
  required: []
  recommended: []
outputs:
- type: transcript-insights
  feeds_into:
  - content-strategy
  - thought-leadership
depends_on: []
feeds_into:
- content-strategy
- thought-leadership
owned_by_agent: researcher
mcps_used:
- youtube-transcript
- firecrawl
push_targets: []
triggers:
  slash_commands:
  - /watch-video
  natural_language: []
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# Watch video — transcribe and analyze any video, at the depth you choose

The general, any-source video tool. Point it at a YouTube link, a Loom, a Vimeo, a Riverside export, a Zoom recording, a webinar, or a competitor's ad — it pulls the transcript, marks the key moments with timestamps, and writes a summary that flags action items, decisions, and quotable lines. v1 is transcript-first; the frame-and-vision roadmap sits under Deferred capabilities.

## Relationship to /transcripts

`watch-video` is the general any-source acquisition-to-summary tool: it *fetches* a transcript from whatever platform the video lives on, then produces transcript + key moments + summary. `/transcripts` (`transcript-analysis`, at `primitives/social/youtube/transcripts`) stays the YouTube-specific deep insight-extraction pipeline — SCQA structure, the verbatim-quote Iron Law, feeding icp-behavioural + tov-guidelines. They compose, they don't compete: when a YouTube job needs deep structured insight extraction, hand the transcript `watch-video` pulls to `/transcripts`. Neither is deprecated.

## Triggers

Run when the user says: "watch this video", "transcribe this Loom", "analyze this video", "summarize this recording", "key moments from this", "what happened in this video", "video notes from [url]".

Do NOT run for:
- Deep insight extraction from a YouTube transcript → `/transcripts`
- Sales-call win/loss analysis → `/win-loss`
- A 2-3 sentence answer the user could get without artifacts → just answer

## Inputs

**Required:** a video URL (any supported source) or a pasted/linked transcript.

**Optional:** the video's purpose (client call, competitor ad, webinar, talk) — sharpens the summary framing and the capture routing.

## Process (v1 — transcript-first)

### 1. Parse the source

Detect the source from the URL pattern or file extension: YouTube (`youtube.com`, `youtu.be`, `/shorts/`, raw 11-char id), Loom (`loom.com/share|embed`), Vimeo, Riverside, a Zoom recording, or a local file. If ambiguous, ask.

### 2. Pull the transcript

Backend by source, in order:

| Source | Method |
|---|---|
| YouTube | `mcp__youtube-transcript__get_transcript` — returns timestamped segments directly |
| Loom / Vimeo / Riverside / other web video | `mcp__firecrawl__firecrawl_scrape` (or `WebFetch`) on the share page to pull platform-provided captions / transcript |
| No captions anywhere, or a local file | Ask the user to paste or link a transcript. Local-Whisper transcription is deferred (see below) |

Clean the pulled text: strip caption tags, de-duplicate rolling captions, paragraph-break on long pauses. Keep the segment timestamps — they carry the whole key-moments layer.

### 3. Produce the three artifacts

From the timestamped transcript alone — no frames needed:

1. **Transcript** — cleaned, timestamped, speaker-attributed where the source distinguishes speakers.
2. **Key moments** — a timestamped list: view or topic changes, the moment a claim lands, anything that reads as a decision, action, or notable event. Each entry cites the transcript.
3. **Summary** — TL;DR, key moments, action items, decisions, quotes worth keeping, open questions. Full template: `references/output-format.md`.

### 4. Optional — capture to the taste-library

Offer to save the summary for reuse. Routing:
- Competitor / ad / talk / webinar / marketing-reference video → `projects/research/taste-library/resources/{MMYY}-video-{slug}.md`
- Client call / meeting recording (carries PII) → the client folder, not the shared taste-library, and redact per [`pii-redaction.md`](../../../rules/pii-redaction.md) first.

## Evidence-bound discipline

This skill is bound by [`evidence-bound-outputs.md`](../../../rules/evidence-bound-outputs.md). Every extracted claim — a key moment, an action item, a decision, a flagged quote, a theme — cites a verbatim (or near-verbatim) quote from the transcript with a timestamp and, where the source distinguishes them, the speaker. No quote to back a claim → lower the confidence per `ontology.md` (`[INFERRED]` / `[ESTIMATED]`) or drop the claim. Never invent a quote, a speaker, or a business fact the transcript doesn't state. Clean a garbled auto-caption lightly if you must, flag it `(cleaned)`, but never paraphrase words into someone's mouth.

Citation shape:

> "verbatim line from the transcript"
> — Speaker (if known) [00:12:34]

## Deferred capabilities (future)

v1 ships transcript-first. Three capabilities from the source skill are deferred until there's a live use case; the full design is preserved in `references/depth-modes.md` so implementation is a wire-up, not a redesign:

- **Local transcription (Whisper).** For videos with no platform captions. Deferred — v1 asks for a transcript instead.
- **Visual mode (ffmpeg frame extraction + Claude vision).** Frames on a per-source cadence, paired with the transcript window, for demos and slide decks where the screen carries meaning the words don't.
- **Multimodal mode (Gemini native video / dense vision).** Whole-video ingestion for delivery, pacing, and brand / ad-audit reads.

When a capability lands it becomes a selectable depth mode; the user picks depth, and long videos always confirm before any paid frame or vision pass.

## Anti-hallucination guardrails

1. Never invent a quote, speaker, name, or number the transcript doesn't contain.
2. Quote verbatim; flag any light cleanup `(cleaned)`.
3. Keep timestamps on every moment and quote.
4. Mark confidence per `ontology.md` when a claim isn't directly supported.
5. Say "not available" when the transcript is thin — don't fill the gap.

## Output format

Full templates — transcript, key moments, summary, taste-library capture: `references/output-format.md`.

## Reference files

| File | Purpose |
|---|---|
| `references/output-format.md` | Transcript / key-moments / summary templates + taste-library capture format |
| `references/depth-modes.md` | The 3-mode depth design; deferred visual + multimodal tooling preserved for future |

## Attribution

Adapts [`coreyhaines31/makerskills/watch-video`](https://github.com/coreyhaines31/makerskills) (MIT, © 2026 Corey Haines), accessed 2026-07-08. Re-tooled onto our youtube-transcript MCP + Firecrawl; local-transcription/multimodal deferred.
