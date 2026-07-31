---
name: product-ui-frames
version: "1.0"
last_updated: 2026-05-01
author: genesys-growth
description: |
  Produce brand-bound HTML video compositions rendered to MP4 via the Hyperframes engine. Use when the brief asks for a video, motion clip, animated explainer, lower-third, b-roll, social cut, or website-to-video. Takes a brand-kit (Genesys, client, or course DESIGN.md) as required input and synthesizes a Hyperframes-compatible palette + typography + house-style at composition time, so the same template renders three visibly distinct videos for three brand-kits. Produces an `index.html` source + an MP4 output. Triggers: "create a video", "render a clip", "make an explainer", "animate this", "video version of", "turn this site into a video". Downstream: linkedin-content, newsletter, sales-enablement-asset, youtube-scripts. Not for: static images (use linkedin-infographics), web prototypes (use vibe-coding), or Figma motion (use figma-prototype).
goal: Render a brand-bound MP4 video composition from an HTML composition that consumes a DESIGN.md brand-kit.
outcome: A locked video-composition artifact — `index.html` source + MP4 output + sidecar metadata — bound to a specific brand-kit. The MP4 is the consumed asset; the HTML + metadata enable re-render when the brand-kit refreshes.
primitive: content
sub_primitive: motion
ontology_type: video-composition
review_gate: 3
inputs:
  required:
    - brand-kit
  recommended:
    - linkedin-weekly-content
    - youtube-scripts
    - thought-leadership
    - expert-pov
    - tov-guidelines
depends_on:
  - brand-kit
owned_by_agent: content
mcps_used: []
triggers:
  slash_commands:
    - /product-ui-frames
  natural_language:
    - "create a video"
    - "render a clip"
    - "make an explainer"
    - "animate this"
    - "video version of"
    - "turn this site into a video"
    - "make a 15s social ad"
    - "lower third"
    - "b-roll"
status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
---

# Product UI Frames

Generic brand-bound product-UI animation engine. Renders HTML video compositions to MP4 via the Hyperframes engine. The skill consumes a DESIGN.md brand-kit, synthesizes a Hyperframes-compatible palette, composes an `index.html`, and renders to MP4 via `npx hyperframes render`.

For the *onboarding-specific* variant with required stills intake + cursor/caption discipline, see [`/onboarding-video`](../onboarding-video/SKILL.md) — it inherits this engine and adds craft rules for app/product feature demos.

The architectural spine: **brand-kit input is required, not optional.** Same composition template, three brand-kits, three visibly distinct outputs.

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`design-production.md`](../../../../rules/design-production.md) — DESIGN.md contract, banned visual patterns
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in product-ui-frames |
|---|---|---|
| **R1** | Source placement (three layers) | Engine itself is **internal-reference** (generic renderer). Consuming skills (`/onboarding-video`, future video wrappers) inherit source-placement rules per their own audience. Engine docs keep inline brand-kit + DESIGN.md cites for QA. |
| **R3** | Product-update tone | Captions and on-screen text in rendered output frame as "[Product] does X" — engine enforces no "thrilled to announce" defaults in template caption library. |
| **R9** | Action-oriented section names | Composition section names verb-led ("Connect / Render / Stitch"). Preserve. |

Note: this skill is the generic engine — most archetype-specific refinements (R2/R5/R6/R7/R8) apply at the consuming-skill layer (e.g., `/onboarding-video` for end-customer videos, future skills for market-facing variants). The engine inherits R1+R3+R9 as the universal floor.

## When to use

Use when the brief asks for video, motion content, an animated explainer, a lower-third, social b-roll, or "turn this site into a video." Use when a downstream content artifact (LinkedIn post, newsletter, sales deck, YouTube script) needs a motion variant.

Do NOT use for static images ([`linkedin-infographics`](../../social/linkedin-infographics/SKILL.md), [`linkedin-carousels`](../../social/linkedin-carousels/SKILL.md)), web prototypes ([`vibe-coding`](../../website/vibe-coding/SKILL.md)), or Figma-anchored motion ([`figma-prototype`](../../design/figma-prototype/SKILL.md)).

## Prerequisites

- **Node.js ≥ 22 + FFmpeg** installed locally. Verify with `npx hyperframes doctor`.
- **A brand-kit DESIGN.md** for the consumer (Genesys, client, or course). If missing, run [`/brand-kit`](../../../research/brand-kit/SKILL.md) first.

## Inputs

| Input | Required | Source | Notes |
|-------|----------|--------|-------|
| `brand_kit_path` | Yes | DESIGN.md path | Genesys / client / course / adhoc |
| `aspect_ratio` | Recommended | brief | `9:16` / `16:9` / `1:1` / `4:5`. Default by platform: LinkedIn vertical → `9:16`, YouTube → `16:9`, Instagram square → `1:1` |
| `duration_seconds` | Recommended | brief | Default 15s for social, 8s for lower-thirds |
| `narration_text` | Optional | upstream skill output (linkedin-content, thought-leadership, etc.) | Auto-generates TTS if provided |
| `blocks_to_use` | Optional | brief | Registry blocks to install via `npx hyperframes add` |
| `source_url` | Optional | brief | If set, route through the website-to-video sub-workflow |

## Workflow

### Step 1 — Discovery (exploratory briefs only)

For open-ended briefs ("make me an explainer for the AI advice gap"), ask the four-question intake before touching tools:

- **Audience** — who watches this?
- **Platform** — where does it play? (drives aspect_ratio)
- **Priority** — motion quality vs content accuracy vs brand fidelity vs speed?
- **Variations** — single best shot or 2-3 options?

For specific briefs ("add a yt-lower-third with the guest name"), skip discovery.

### Step 2 — Bind brand-kit

1. Resolve `brand_kit_path`. Auto-detect by working directory if not supplied:
   - `projects/genesys/...` → Genesys brand-kit
   - `projects/consulting/active/{client}/...` → that client's brand-kit
   - `projects/courses/gtme-school/...` → GTM-E brand-kit
2. Read DESIGN.md tokens (colors, typography, rounded, spacing, components).
3. Read the "Do's and Don'ts" prose section to derive house-style constraints (e.g., ClientCo → no em-dashes anywhere — including TTS narration).
4. Synthesize a Hyperframes palette per the premium reference.

### Step 3 — Scaffold

```bash
npx hyperframes init {composition-id}
cd {composition-id}
```

Pick the aspect-ratio template from [`templates/`](templates/):
- `composition-9-16.html` for vertical (LinkedIn vertical, TikTok)
- `composition-16-9.html` for landscape (YouTube, web)
- `composition-1-1.html` for square (LinkedIn square, Instagram)
- `composition-base.html` for arbitrary dimensions

The template includes brand-kit token slots — fill them from Step 2's synthesized palette.

### Step 4 — Install registry blocks

```bash
npx hyperframes add {block-name}
```

See the premium reference for the block taxonomy. The 5 priority blocks documented in Phase 5a:

- `data-chart` — animated bar + line chart (data-viz category)
- `instagram-follow` — social-platform overlay (social-overlay category)
- `flash-through-white` — shader transition (transition category)
- `cinematic-zoom` — slow zoom effect (cinematic category)
- `yt-lower-third` — YouTube-style lower-third (utility category)

The remaining 38 catalog blocks are deferred to Phase 5b. They're available via `npx hyperframes add` even without our docs — see the premium reference for discovery commands.

### Step 5 — Author

Edit `index.html`. The composition root is a `<div id="stage" data-composition-id="{id}" data-width data-height>` containing:
- `<video>`, `<img>`, `<audio>` clips with `data-start`, `data-duration`, `data-track-index`
- Block sub-compositions via `<div data-composition-src="compositions/{block}.html">`
- CSS variables bound to the synthesized palette (NEVER hardcoded hex)

Heavy authoring guidance lives in the premium reference.

### Step 6 — Lint, inspect, preview

```bash
npx hyperframes lint # missing data-composition-id, overlapping tracks, unregistered timelines
npx hyperframes inspect # text overflow, off-canvas elements
npx hyperframes preview # browser preview with live reload
```

Fix everything `lint` and `inspect` surface before rendering. Rendering is expensive; previewing is cheap.

### Step 7 — Render

```bash
npx hyperframes render --output {client_path}/content/execution/video/{MMYY}-{composition_id}.mp4
```

Output paths follow the routing rule: Genesys content → `projects/genesys/content/execution/video/`, client → `projects/consulting/active/{client}/content/execution/video/`, course → `projects/courses/gtme-school/content/execution/video/`.

### Step 8 — Sidecar + manifest

Write the metadata sidecar `{...}/{MMYY}-{composition_id}.metadata.json` per the [video-composition output template](../../../_schema/output-templates/video-composition.md). Records: brand_kit_path, palette_synthesized, render_specs, blocks_used.

If publishing to GDrive or Framer, write the manifest line per `.claude/rules/gdrive-protocol.md` so sync-back works on the source.

## Variations

When the brief asks for multi-aspect output (same content as 9:16 + 1:1 + 16:9), produce three composition_ids with shared brand-kit binding. Each renders independently; metadata sidecar lists siblings.

## Website-to-video sub-workflow

When `source_url` is set, follow the 7-step capture pipeline in the premium reference. The brand-kit binding still applies — the captured site is rendered through the consumer's brand-kit, not the source site's brand.

## Remotion translation (deferred)

If the user provides Remotion `.tsx` source, follow the premium reference. The translation skill ships an SSIM-graded test corpus; do not skip it — a translation that "looks right" but renders 0.05 SSIM lower than the validated baseline is silently wrong.

## House-style derivation per brand-kit

Per the premium reference, the brand-kit's "Do's and Don'ts" section maps to motion choices:

- "no em dashes" → applies to TTS narration script and any visible text in the composition
- "operator-first, no buzzwords" → applies to narration, captions, on-screen copy
- "one primary color per screen" → palette mapper assigns primary to the single most important on-screen action; other elements use secondary/tertiary
- "two font weights max" → typography map exposes only display + body weights; do not pull a third
- Client-specific overrides (e.g., ClientCo's "ClientCo is one word") are checked in narration text before TTS

## Quality gate

Before declaring the output locked:
- `npx hyperframes lint` clean
- `npx hyperframes inspect` no overflow warnings
- Narration text passes the brand-kit's "Don'ts" check
- Output MP4 plays cleanly; duration matches `duration_seconds` ± 1 frame

## What this skill does NOT do

- Generate brand-kits — that's [`/brand-kit`](../../../research/brand-kit/SKILL.md)
- Publish to social platforms — separate lifecycle/social-posting skills
- Distributed/cloud rendering — local single-machine only
- Image generation (stills) — use [`linkedin-infographics`](../../social/linkedin-infographics/SKILL.md) or [`canvas-design`](#) instead

## Animation craft

Video motion is structurally different from UI motion (different durations, triggers, rendering context). Two reference layers apply:

- **Video-specific patterns** — see animation-patterns.md for brand-bound easing, stagger reveals, the 6/15/30 duration rule, and Hyperframes engine compatibility constraints.

For brand-bound easing tokens specifically, consult the client's DESIGN.md.

## See also

- Composition authoring deep-dive
- Brand-kit mapper
- Hyperframes CLI
- Hyperframes registry + 5 priority blocks
- Animation (GSAP)
- Animation patterns (impeccable, video-specific)
- Universal motion tenets (design-reviewer)
- Website-to-video pipeline
- Remotion translation
- 9 palette QA references
- 3 example briefs

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
