---
knowledge_type: video-composition
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 2 Execution"
schema_version: 1
render_targets: [local, gdrive, framer]
canonical_render: mp4-local
---

# Video Composition — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

Brand-bound HTML video composition rendered to MP4 via the Hyperframes engine. The composition consumes a DESIGN.md brand-kit as required input, synthesizes a Hyperframes-compatible palette + typography map at composition time, and produces a deterministic MP4 plus its source `index.html`. Distinct outputs per consumer brand-kit (Genesys, client, course) from the same template.

## Required frontmatter fields

```yaml
client: {slug | "genesys" | "gtme-school"}
skill: product-ui-frames
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: video-composition
composition_id: {kebab-case-id}            # matches data-composition-id on root <div>
brand_kit_source: genesys | client | course | adhoc
brand_kit_path: {absolute or workspace-relative path to DESIGN.md}
palette_synthesized:                        # emitted by brand-kit-mapper at composition time
  primary: "#hex"
  secondary: "#hex"
  tertiary: "#hex"
  surface: "#hex"
  on_surface: "#hex"
  font_display: "Inter"
  font_body: "Inter"
duration_seconds: {integer}
aspect_ratio: "9:16" | "16:9" | "1:1" | "4:5"
output_path: {workspace-relative path to .mp4}
locked_by: null
locked_date: null
review_gate_passed: null
```

## Optional frontmatter fields

```yaml
blocks_used: [data-chart, yt-lower-third, ...]   # registry blocks installed via npx hyperframes add
narration_text: {full TTS script}
narration_voice: {voice id from hyperframes tts}
audio_track: {workspace-relative path to background music}
captions_enabled: true | false
render_specs:
  width: 1080 | 1920 | 1080
  height: 1920 | 1080 | 1080
  fps: 30 | 60
  codec: h264
  bitrate: "8M"
  container: mp4
source_url: {URL — only when produced via website-to-video pipeline}
source_brief: {path to upstream brief — linkedin-content, youtube-scripts, thought-leadership, etc.}
```

## Required body sections (in order)

1. **Brief recap** — restate the input brief in 1-2 sentences (audience, platform, priority, variations requested)
2. **Brand-kit binding** — show the DESIGN.md tokens consumed and the synthesized palette emitted
3. **Composition manifest** — list of blocks/components installed, with `npx hyperframes add` commands
4. **`index.html` source** — the full HTML composition with `data-*` attributes and registered GSAP timeline
5. **Render command** — the exact `npx hyperframes render` invocation that produced the MP4
6. **Output artifact** — path to `.mp4` plus checksum
7. **Preview & QA** — `npx hyperframes preview` URL, lint output (`npx hyperframes lint`), visual inspect output (`npx hyperframes inspect`)

## Optional body sections

- **Variations** — when the brief requested multiple cuts (e.g., 9:16 + 1:1 + 16:9 of the same content), list each composition_id and output path
- **Source URL** — when produced via `website-to-video`, the captured URL + capture timestamp
- **Narration script + TTS specs** — when narration was generated, full script + voice + sync points
- **Caption track** — when captions are enabled, the SRT or timing data

## Confidence-tag conventions

Video output is non-textual; confidence tags do not apply to the MP4 itself. They DO apply to:
- Narration text (when sourced from upstream content with claims): inherits the upstream skill's confidence policy
- Data visualizations (when using `data-chart` or `flowchart` blocks with sourced data): tag each data point per `.claude/rules/exa-protocol.md`

## Render rules per target

### Local (canonical — mp4)

- Output to `{client_or_genesys_path}/content/execution/video/{MMYY}-{composition_id}.mp4`
- Source `index.html` co-located at `{...}/{MMYY}-{composition_id}.html`
- Metadata sidecar `{...}/{MMYY}-{composition_id}.metadata.json` with palette + brand_kit_path + render_specs

### gdrive (manifest pointer + embed link)

- Upload .mp4 to client's `PJ - {Client}` folder via gdrive MCP
- Embed link rendered into client's content tracker Doc with the manifest line for sync-back

### framer (when published as marketing collateral)

- Upload to Framer assets, embed via `<video>` element in target page
- Maintain manifest line in source for re-render when brand-kit refreshes

### notion — N/A by default
The MP4 is too large for Notion native; share as gdrive embed if Notion is the discussion surface.

## Validation rules

1. All required frontmatter fields present
2. `composition_id` matches `data-composition-id` on the composition root
3. `brand_kit_path` resolves to a valid DESIGN.md file with required token sections (colors, typography)
4. `palette_synthesized` is non-empty and consistent with brand-kit DESIGN.md tokens
5. `aspect_ratio` enum check; `duration_seconds` > 0
6. `output_path` exists post-render
7. `npx hyperframes lint` returns clean (no missing data-composition-id, overlapping tracks, unregistered timelines)
8. `npx hyperframes inspect` returns no overflow warnings
9. If `narration_text` set: TTS audio track exists and aligns to declared `duration_seconds`
10. If `blocks_used` non-empty: every block name is a valid Hyperframes registry name (validates via `npx hyperframes add --dry-run` or registry index)

## Examples in the wild

- Phase 6 will produce three smoke-test compositions during rollout (Genesys LinkedIn explainer, ClientCo sales-deck b-roll, GTM-E lesson intro)
