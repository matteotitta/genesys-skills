#!/usr/bin/env python3
"""Seed `name` + `ontology_type` for the 14 Phase 4 orphan skills.

These skills currently have no `name` or `ontology_type` in frontmatter.
This script adds them so the main migrator can pick them up in subsequent batches.
Idempotent: re-runs are no-ops.
"""
import re, sys
from pathlib import Path

# Mapping per Phase 4 plan
ORPHAN_MAP = {
    ".claude/skills/meta/infra/create-gdrive/SKILL.md":
        ("create-gdrive", "runbook"),
    ".claude/skills/meta/learning/steal/SKILL.md":
        ("steal", "runbook"),
    ".claude/skills/primitives/outbound/execution/apollo-sequences/SKILL.md":
        ("apollo-sequences", "outreach-sequence"),
    ".claude/skills/primitives/outbound/execution/enrichment/deepline-enrich/SKILL.md":
        ("deepline-enrich", "runbook"),
    ".claude/skills/primitives/outbound/execution/linkedin-engagement/SKILL.md":
        ("linkedin-engagement", "outreach-sequence"),
    ".claude/skills/primitives/outbound/research/list-building/apollo-find/SKILL.md":
        ("apollo-find", "lead-assessment"),
    ".claude/skills/primitives/outbound/research/list-building/niche-signal/SKILL.md":
        ("niche-signal", "lead-assessment"),
    ".claude/skills/primitives/outbound/strategy/abm/SKILL.md":
        ("abm", "outreach-sequence"),
    ".claude/skills/primitives/seo-aeo/execution/gbp-suite/SKILL.md":
        ("gbp-suite", "runbook"),
    ".claude/skills/primitives/seo-aeo/strategy/aeo-strategy/SKILL.md":
        ("aeo-strategy", "content-strategy"),
    ".claude/skills/primitives/social/linkedin/linkedin-content-audit/SKILL.md":
        ("linkedin-content-audit", "content-audit"),
    ".claude/skills/primitives/social/linkedin/linkedin-profile/SKILL.md":
        ("linkedin-profile", "content-audit"),
    ".claude/skills/research/brand-kit/SKILL.md":
        ("brand-kit", "brand-kit"),
    ".claude/skills/research/funnel-strategy/SKILL.md":
        ("funnel-strategy", "funnel-strategy"),
}


def seed_one(path, name, ontology_type):
    p = Path(path)
    if not p.exists():
        return f"MISS {path}"
    text = p.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return f"NO-FM {path}"
    fm_text = m.group(1)

    changes = []
    new_fm = fm_text

    # Inject name if absent
    if not re.search(r"^name:\s*\S", new_fm, re.MULTILINE):
        new_fm = f"name: {name}\n" + new_fm
        changes.append(f"name={name}")

    # Inject ontology_type if absent
    if not re.search(r"^ontology_type:\s*\S", new_fm, re.MULTILINE):
        new_fm = f"ontology_type: {ontology_type}\n" + new_fm
        changes.append(f"ontology_type={ontology_type}")

    if not changes:
        return f"NOOP {path}"

    new_text = "---\n" + new_fm + "\n---" + text[m.end():]
    p.write_text(new_text, encoding="utf-8")
    return f"OK {path}  ({', '.join(changes)})"


def main():
    n_ok, n_noop, n_miss = 0, 0, 0
    for path, (name, otype) in ORPHAN_MAP.items():
        result = seed_one(path, name, otype)
        print(result)
        if result.startswith("OK"):
            n_ok += 1
        elif result.startswith("NOOP"):
            n_noop += 1
        else:
            n_miss += 1
    print(f"\n=== Seeded: {n_ok}, NoOp: {n_noop}, Missing: {n_miss} ===")
    return 0 if n_miss == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
