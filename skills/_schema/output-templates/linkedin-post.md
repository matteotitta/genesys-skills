---
knowledge_type: linkedin-post
ontology_source: .claude/rules/ontology.md
ontology_section: "Knowledge types — Level 3 Content"
schema_version: 1
render_targets: [gdrive, notion]
canonical_render: local
---

# LinkedIn Post — Canonical Output Schema

> Canonical schema. Edit only via MCP companion plan.
> Source: `.claude/rules/ontology.md`

## Purpose

LinkedIn feed post — hook + body + CTA, paste-ready for the LinkedIn UI. Channel-native canonical render (`local`) — no auto-publish; the post is copy-pasted by Matteo or the client.

## Required frontmatter fields

```yaml
client: {slug}                       # or "genesys" for Matteo's own posts
skill: linkedin-content              # or specific variant: linkedin-expert-posts, linkedin-sales-posts, etc.
version: 1
status: draft
generated: {YYYY-MM-DD}
ontology_type: linkedin-post
post_type: expert | personal | sales | story | hot-take
pillar: {pillar from content-strategy}
target_icp: {ICP segment}
character_count: {n}
hook_variant_chosen: {n}             # which hook (1-5) was selected from variants
evidence_anchored_by:                # upstream skill outputs
  - {path}
locked_by: null
locked_date: null
review_gate_passed: null
```

## Required body sections (in order)

1. **Strategic context** — pillar, target ICP, intended action, why this post now
2. **Hook variants** — 3-5 hook options scored against tenets (the chosen one is `hook_variant_chosen`)
3. **Final post** — code-block with paste-ready post body (hook + body + CTA)
4. **Quality checklist** — voice check, 100 Posts Test, no banned hooks (no X-not-Y per `feedback_no_x_not_y_hooks.md`), banned buzzwords absent
5. **Repurposing notes** — how this post repurposes upstream content + what it could spawn (carousel, comment thread)

## Optional body sections

- **A/B variants** — when posting two versions to test
- **Cross-channel echo** — when the same idea ships to newsletter / blog
- **Founder personalization notes** — when post is in someone else's voice

## Confidence-tag conventions

Per `.claude/rules/exa-protocol.md`. Content tier requires ≥40% verified.

**No inline tags in the post body** — breaks reading flow + 100 Posts Test. Substantive claims trace to `evidence_anchored_by` paths instead.

The Strategic context section can use inline tags if claims about ICP / market are made (rare).

LinkedIn coach tenets per `feedback_linkedin_coach_tenets.md` apply: 15 general + 7 Matteo-specific.

## Render rules per target

### gdrive (Doc — for stakeholder review when needed)

- Inter, black, plain header, page-numbered footer
- Final post in code-block (paste fidelity)
- Strategic context + hook variants + quality checklist as standard markdown sections

### gdrive (Slides) — N/A
### gdrive (Sheet) — for editorial calendar tracking

When part of a content calendar, post metadata goes to Sheet (rows: posts; columns: pillar, post_type, character_count, scheduled_date, status, actuals).

### notion (Page render — rare, only for stakeholder review)

- Overview = strategic context summary
- H1 = "{Client} — LinkedIn post: {first 60 chars of hook}"
- Final post in code block at top; metadata in toggles below

### Channel-native (canonical)

The artifact is the final post copy-pasted into LinkedIn. Manifest line not applicable for direct LinkedIn publish; only the Doc/Notion review surfaces carry manifests.

## Validation rules

1. All required frontmatter fields present
2. `post_type` is one of the 5 enum values
3. `character_count` ≤3000 (LinkedIn limit; 1300 = sweet spot)
4. `hook_variant_chosen` resolves to one of the variants in body
5. Final post passes 100 Posts Test (would feel authentic for 100 posts in a row)
6. No X-not-Y hook patterns in hook OR body (per `feedback_no_x_not_y_hooks.md`)
7. Banned buzzwords absent ("innovative", "leverage", "synergy", "solutions")
8. CTA present (low-friction — comment / DM / link)
9. `evidence_anchored_by` populated when post makes substantive claims

## Examples in the wild

- Phase 4 will produce conforming examples during rollout
