---
name: ad-creative
version: "1.0"
last_updated: 2026-05-11
author: genesys-growth
description: |
  Runs the full Higgsfield + GPT Image 2 + Seedance 2.0 chain end-to-end from a brand URL to produce a multi-format ad pack: LinkedIn 1.91:1 + 1:1 and Meta 1:1 + 4:5 + 9:16 (Reels/UGC), each in static, animated, and UGC variants. Stages: Firecrawl brand brief → GPT Image 2 hero static → platform-tuned text overlay → Seedance 2.0 animated hero → GPT Image 2 UGC persona → Seedance 2.0 UGC clips. Outputs a run-id folder with brief.md, static/, video/, ugc/, and a cost+model manifest. Brand-bound via DESIGN.md (no hardcoded colors/fonts). Triggers: "AI ad creative", "make ads for this brand", "LinkedIn + Meta ad pack", "AI UGC video", "Higgsfield ads", "generate ad creative from URL". Requires Higgsfield MCP. NOT for writing the underlying brief for a human designer — use /ad-creative-brief first if a human is in the loop.
goal: Produce a brand-bound multi-format AI ad pack (statics + animated + UGC) for LinkedIn and Meta from a single brand URL invocation.
outcome: A run-id folder containing brief.md, per-platform aspect-ratio crops (static PNG + animated MP4 + UGC MP4), copy variants, and a manifest.yaml capturing prompts, model versions, asset hashes, and cost — ready for /design-reviewer and direct upload to LinkedIn Campaign Manager + Meta Ads Manager.

primitive: paid-marketing
sub_primitive: execution
ontology_type: ad-creative-asset
review_gate: 3

inputs:
  required: []
  recommended:
    - brand-kit
    - ad-creative-brief
    - product-messaging
depends_on: []

owned_by_agent: paid
mcps_used:
  - higgsfield
  - firecrawl
triggers:
  slash_commands:
    - /ad-creative
  natural_language:
    - "make ads for this brand"
    - "generate AI ad creative"
    - "LinkedIn + Meta ad pack from URL"
    - "AI UGC video for this brand"
    - "Higgsfield ad pipeline"

status: draft
locked_by: null
locked_date: null
lock_version: null
sources_count: 0
effort: high
---

# Ad Creative — AI ad agency in Claude Code

Generate a full multi-format ad pack (static + animated + UGC, LinkedIn + Meta) from one brand URL. Chains Firecrawl → GPT Image 2 → Seedance 2.0 via the Higgsfield MCP. Brand-bound to DESIGN.md tokens; outputs ready to upload to LinkedIn Campaign Manager and Meta Ads Manager.

---

## Doctrine inherited (Step 7 — 0626 rollout)

Output complies with:

- [`output-tenets.md`](../../../../rules/output-tenets.md) — the seven tenets
- [`output-simplicity.md`](../../../../rules/output-simplicity.md) — length caps, three-layer source placement, robot-tells ban
- [`design-production.md`](../../../../rules/design-production.md) — DESIGN.md contract + banned visual patterns (composes with The Iron Law below)
- Step 6 calibration: see [[feedback_execution_doctrine_refinements_step6]]

**Refinements applied to this skill:**

| Code | Refinement | How it lands in ad-creative |
|---|---|---|
| **R1** | Source placement (three layers) | Ads are **end-customer-facing**. **No sources block in the ad copy or on the creative.** Run manifest captures prompts + sources for QA; not surfaced in the deliverable. |
| **R2** | Single-doc-with-toggles | Multi-format ad pack ships as **one run-folder + one summary doc with per-platform toggles** (LinkedIn 1.91:1 / 1:1 / Meta 1:1 / 4:5 / 9:16). Not 8 separate sub-docs. |
| **R3** | Product-update tone | Ad copy frames as "[Product] now does X" not "we're thrilled to announce." Even hero-launch ads default to even-keeled product framing. |
| **R5** | Blog as voice anchor | When the campaign has an anchor blog, the blog's opening line becomes the hero headline across LinkedIn + Meta + variants. Verbatim. Cross-platform voice consistency is what makes the pack read as one campaign. |
| **R6** | CTA hierarchy | Market-facing ads → sign-up or trial primary. Blog/whitepaper as fallback for cold awareness. Never both. Retargeting / warm-base ad sets → product-action CTA. |
| **R9** | Action-oriented section names | Brief sections + asset captions verb-led. "How to start with [Product]" beats "Get started." |

---

## Triggers

Run this skill when:

- A campaign needs creative for both LinkedIn and Meta simultaneously and a human design queue is too slow.
- A new launch needs a same-day asset pack to A/B test angles before committing to bigger spend.
- A client wants UGC-style video without booking a creator shoot.
- The operator already has a brand-kit DESIGN.md and wants on-brand AI generation, not a generic stock-photo look.

Do NOT run when:

- The output is going to a human designer for production — use `/ad-creative-brief` instead.
- There's no DESIGN.md and no brand URL — the skill needs at least one to bind brand identity.
- The campaign needs a single hero shot with art-directed humans (still a creator-shoot job; AI UGC is not photoreal humans).
- The Higgsfield MCP isn't installed (see Prerequisites).

---

## The Iron Law — voice-locked

**ASSETS ARE BRAND ARTIFACTS, NOT AI OUTPUTS.**

Every asset the skill produces must read as if it were made for *this brand specifically* — not as a generic AI render. The DESIGN.md token contract is the floor, not the ceiling.

**No exceptions:**

- Off-palette colors → reject the render, re-prompt with explicit hex tokens.
- Fabricated stats, testimonials, or customer logos in overlays → strip them. Mark `[NOT AVAILABLE]` if the brief implies a number we can't source.
- Generic UGC personas with no ICP grounding → re-roll with the brand-kit's audience description.
- Em dashes in ClientCo overlays (or any client with a no-em-dash rule) → re-prompt without them.
- Mixing rounded + sharp corners in the same asset → reject; pick one per `design-production.md` Do's/Don'ts.

---

## Prerequisites — Higgsfield MCP

This skill depends on the Higgsfield MCP for GPT Image 2 + Seedance 2.0 calls (Higgsfield also exposes Soul V2, Veo 3.1, Kling 3.0, Flux 2 from the same server), plus the already-installed Firecrawl MCP for the brand-brief stage.

Higgsfield uses an HTTP MCP server with **OAuth-based authentication** — no API keys to manage. Auth happens once per machine, on first tool use, via a browser sign-in to your Higgsfield account.

**One-time setup (run before first invocation):**

```bash
# 1. Install the Higgsfield MCP at user scope (persists across all worktrees):
claude mcp add --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp

# 2. Verify it registered:
claude mcp list | grep higgsfield
# higgsfield: https://mcp.higgsfield.ai/mcp (HTTP) - ! Needs authentication

# 3. Authenticate via OAuth:
# Open a Claude Code session and run the /mcp slash command.
# Higgsfield will print an auth URL — open it in a browser, sign in to your
# Higgsfield account, copy the returned code, and paste it back in Claude.
# Alternatively, authentication is triggered automatically the first time
# any mcp__higgsfield__* tool is called.

# 4. Confirm tools are surfaced:
# In a fresh Claude Code session, look for tools named
# mcp__higgsfield__* in the deferred-tool list.
```

**Startup check (the skill runs this on every invocation):**

The skill calls a no-op Higgsfield tool (e.g., `mcp__higgsfield__list_models` or equivalent) before stage 1. If the call returns "tool not found" or "needs authentication," the skill aborts with:

> "Higgsfield MCP not detected or not authenticated. Run `claude mcp add --transport http --scope user higgsfield https://mcp.higgsfield.ai/mcp` then `/mcp` to authenticate. See SKILL.md."

No partial runs — if the MCP is missing or unauthenticated, no Firecrawl credits get spent either.

**Cost gate:** Higgsfield credit spend is non-trivial. The skill estimates total run cost before stage 2 (image generation) and asks the user to confirm if estimated cost > $5 USD-equivalent. See the premium reference."

---

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **Brand URL** | The brand's website root (e.g., `https://ClientCo.com`) — Firecrawl scrapes for hero copy + visual hints | Required |
| **`--client {slug}`** | Routes output to `projects/consulting/active/{slug}/paid/execution/`. Triggers brand-kit lookup at `brand/{MMYY}-brand-kit.md` | Recommended |
| **DESIGN.md (brand-kit)** | Token frontmatter (colors, typography, components) — the brand contract | Recommended; falls back to transient brief if absent |
| **`--brief {path}`** | Path to a pre-existing `/ad-creative-brief` output to consume — overrides Firecrawl extraction for angles + copy | Optional |
| **`--copy {path}`** | Path to a `/linkedin-ads-copy` or `/google-ads-copy` output to use as text overlays + UGC scripts | Optional |
| **`--mode`** | `full` (default), `statics-only`, `ugc-only`, `animate-only` | Optional |
| **`--platforms`** | Comma-separated subset of `linkedin,meta` (default both) | Optional |

---

## Process

Seven-stage deterministic chain (Stage 7 is an optional pre-ship gate). Each stage has explicit MCP tool, model pick, prompt template, expected output, and failure mode. Full reference in the premium reference.

| # | Stage | MCP / Model | Output |
|---|-------|-------------|--------|
| 1 | Brand brief | Firecrawl scrape + DESIGN.md merge | `brief.md` |
| 2 | Hero static | `mcp__higgsfield__generate_image` → **`marketing_studio_image`** (default; ads-tagged Higgsfield model) or `gpt_image_2` (text-heavy variants) | per-aspect static PNGs |
| 3 | Text overlay | Sharp/Jimp local OR `flux_kontext` for context-aware edit | static-with-overlay PNGs |
| 4 | Animated hero | `mcp__higgsfield__generate_video` → **`seedance_2_0`** (default; identity-consistent) | 6s MP4 per aspect ratio |
| 5 | UGC persona | `mcp__higgsfield__generate_image` → **`soul_2`** (UGC + portrait specialty; supports `soul_id` for identity persistence) | persona portrait PNG |
| 6 | UGC clips | `mcp__higgsfield__generate_video` → `seedance_2_0` or `wan2_7` (lip-sync) | 9:16 + 1:1 MP4s |
| 7 | Virality predict | `mcp__higgsfield__virality_predictor` (optional gate) | scores written to manifest; ranks A/B variants |

Mode flags skip stages: `--statics-only` runs 1→3; `--ugc-only` runs 1+5+6; `--animate-only` runs 1+2+4. `--no-virality` skips Stage 7.

**Aspect-ratio honesty:** LinkedIn 1.91:1 renders as native 16:9 (no model supports 1.91:1 directly; LinkedIn auto-crops 16:9 cleanly). Meta 4:5 static is native to `marketing_studio_image` but NOT `gpt_image_2`. Meta 4:5 **video** is not native to any model; spec ships 1:1 + 9:16 for video, not 4:5.

---

## DESIGN.md token contract — voice-locked

Every prompt to GPT Image 2 + Seedance 2.0 cites brand tokens explicitly. Same contract as the rest of the marketing surface.

| Required in every prompt | Forbidden |
|--------------------------|-----------|
| Token-cited colors (e.g., `colors.primary: #1A1C1E`) | Free-form color names ("a warm blue") |
| Token-cited typography (`typography.headline-lg.fontFamily: Inter`) | Off-brand font names from the model's defaults |
| Brand-kit's `signature_elements` (logo treatments, photographic style) | Generic stock-photo aesthetics |
| Voice overrides (e.g., ClientCo no-em-dash) on every overlay | Em dashes / banned tokens leaking through |

**Authority:** Full integration contract in `.claude/rules/design-production.md` (auto-loaded). If DESIGN.md doesn't exist, the skill builds a *transient* brief from Firecrawl and flags the gap — it does NOT invent token values.

---

## Design cycle (post-authoring phases)

After producing the happy-path output, walk these phases before ship. Each references the shared design-quality library at `../../../meta/catalog/design-reviewer/the premium reference. Run `/design-reviewer` as the final ship-ready gate.

- **Layout** — `layout-tenets.md` (rhythm, alignment, density across aspect ratios)
- **Distill** — `distill-principles.md` (strip generative noise; one message per asset)
- **Typeset** — `typeset-principles.md` (overlay measure, leading, scale — esp. on 9:16 mobile)
- **Polish** — `polish-principles.md` (16 details; verify caption legibility on muted video)
- **Cognitive load** — `cognitive-load-tenets.md` (when overlay copy is dense)
- **Delight** — `delight-patterns.md` (1–3 motion moments per video; nothing more)
- **Final review** — run `/design-reviewer` (5 dimensions × 0–4, P0–P3 severity)

Skip Harden + Onboarding — they apply to code/app output, not ad creative.

---

## Anti-Hallucination Guardrails

1. **Never invent customer stats.** "2,000 advisers trust us" needs a verified brand-kit source. Otherwise strip from overlays.
2. **Never invent token values.** If DESIGN.md doesn't define a needed color, pause — do not guess.
3. **Never approximate platform specs.** Use the table in `process.md`.
4. **Never let the model improvise voice.** Pass brand-kit voice overrides into every prompt (ClientCo: no em dashes; ClientCo brand-name = single word).
5. **Never strip captions from video.** 85% of LinkedIn + Meta video is watched muted; auto-generate caption tracks.
6. **Never ship without /design-reviewer pass.** Review-gate 3 is the floor for external publication.

---

## Quality

Self-evaluation checklist (token coverage, aspect-ratio compliance, overlay character limits, caption presence, voice override compliance), worked examples (ClientCo + ClientCo), failure-mode triage, and the rerun-loop pattern in the premium reference.

---

## Integration with Other Skills

### Upstream (consumes)

| Skill | What it provides | Required? |
|-------|-----------------|-----------|
| `brand-kit` | DESIGN.md tokens | Recommended (falls back to transient brief) |
| `ad-creative-brief` | Angles + visual concepts | Optional (overrides Firecrawl extraction) |
| `product-messaging` | Value props, taglines | Optional (used in overlays) |
| `linkedin-ads-copy` / `google-ads-copy` | Headlines for overlays | Optional |

### Downstream

Terminal deliverable — assets upload directly to LinkedIn Campaign Manager / Meta Ads Manager. Run through `/design-reviewer` as the final gate. Track results via `/paid-audit` after spend begins.

---

## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.

---

## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md](../../../../../rules/persuasion-and-stickiness.md) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.

---

