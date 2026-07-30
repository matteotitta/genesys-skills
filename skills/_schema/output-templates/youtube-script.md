---
knowledge_type: youtube-script
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 3 Content"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: local
---

# YouTube Script — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Retention-optimized script for a YouTube video — long-form (8-15 min) or short (≤60s). The video is the artifact; the script is the production input. Channel-native canonical render (`local`) — no auto-publish.

## Required frontmatter fields

```yaml
client: {slug}                       # or "genesys" / "creator" for Matteo's content
skill: youtube-scripts
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: youtube-script
target_runtime_seconds: {n}          # 480-900 typical for long-form; ≤60 for shorts
format: long-form | short
hook_options:                        # 3-5 hook variants scored before recording
  - {hook 1}
retention_beats:                     # timestamps where audience retention typically dips
  - {MM:SS — beat description}
title_options:                       # 3-5 thumbnail-ready titles
  - {title}
thumbnail_concepts:                  # 2-3 concept descriptions
  - {concept}
description: {YouTube video description with timestamps}
pinned_comment: {first comment we post}
upstream_youtube_strategy: {path}    # which video idea from the strategy this is
evidence_anchored_by:
  - {path}
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order)

1. **Strategic context** — which video idea from youtube-strategy, target audience, expected retention shape
2. **Hook options** — 3-5 hooks (first 15 sec) scored against retention tenets
3. **Script** — full script with retention beats called out, b-roll cues, on-screen text cues
4. **Title + thumbnail concepts** — 3-5 title options + 2-3 thumbnail concept descriptions
5. **Description + pinned comment** — YouTube description (with timestamps), first pinned comment to seed engagement
6. **Repurposing plan** — long-form → shorts cuts, → LinkedIn post, → newsletter feature

## Optional body sections

- **Sponsorship notes** — when video has sponsor read-in
- **Guest brief** — when interview format
- **Production notes** — gear, location, B-roll list

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Content tier requires ≥40% verified.

**No inline tags in script body** — breaks recording flow.

Strategic context section can use inline tags for market/ICP claims. Substantive claims trace to `evidence_anchored_by`.

For shorts (≤60s): every claim must be defensible and one-line — no padding.

## Render rules per target

### gdrive (Doc — for review + recording)

- Inter, black, plain header, page-numbered footer
- Script as the body content (paste-ready for teleprompter when recording)
- Hook options + title concepts as bulleted list with scoring rubric notes

### gdrive (Slides) — N/A
### gdrive (Sheet) — for video pipeline tracking

Sheet variant: video pipeline (rows: videos; columns: idea, script_status, recording_date, edit_status, publish_date, retention_target).

### notion (Page render — for collaboration with editor / co-creator)

- Overview = strategic context summary
- H1 = "{Channel} — {video title}"
- Script as toggle (collapsed for review), retention beats highlighted

### Channel-native (canonical)

The video is the artifact. Script is consumed during recording (often via teleprompter from the Doc).

## Validation rules

1. All required frontmatter fields present
2. `format` enum check
3. For shorts: `target_runtime_seconds` ≤60; for long-form: ≥300
4. Hook options: 3-5 variants
5. Title options: 3-5 (test before publish)
6. Thumbnail concepts: 2-3
7. Description has timestamps (chapter markers for long-form)
8. Pinned comment present (seeds first engagement)
9. Retention beats called out at minimum: 0:15 (post-hook), 1:00, midpoint, 2-min-from-end

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
