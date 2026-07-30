#!/usr/bin/env python3
"""migrate-add-copywriting-gate.py

One-shot retrofit: walk .claude/skills/primitives/, identify marketing-copy skills
per the persuasion-and-stickiness.md contract, and append a "## Persuasion &
stickiness pass" section to each SKILL.md body. Idempotent — skip if the body
already references `persuasion-and-stickiness`.

Discrimination logic mirrors is_copy_skill() / check_copywriting_contract() in
validate-frontmatter.py. Strategy, research, audit, data-ops (list-building /
enrichment / research sub-primitives), motion, and the named non-copy skills are
excluded.

Safety (per .claude/rules/skill-ops-safety.md): DRY-RUN IS THE DEFAULT. Pass
--apply to actually write. Bare invocation previews only.

Usage:
    python3 .claude/skills/_schema/migrate-add-copywriting-gate.py            # preview (dry-run)
    python3 .claude/skills/_schema/migrate-add-copywriting-gate.py --apply     # write
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


SKILLS_ROOT = Path(__file__).resolve().parent.parent
PRIMITIVES_ROOT = SKILLS_ROOT / "primitives"

# Mirrors validate-frontmatter.py COPY_PRIMITIVES / COPY_EXCLUDED_SUB_PRIMITIVES /
# COPY_EXCLUDED_SKILL_NAMES — keep the three in sync across both files.
COPY_PRIMITIVES = {
    "content",
    "social",
    "website",
    "lifecycle",
    "outbound",
    "paid-marketing",
    "seo-aeo",
    "product-marketing",
}
COPY_EXCLUDED_SUB_PRIMITIVES = {"strategy", "motion", "list-building", "enrichment", "research"}
COPY_EXCLUDED_SKILL_NAMES = {
    "outbound-send-orchestrator",  # send infrastructure / ops, not copy
    "extrovert-sync",              # MCP seed-sync ops, not copy
    "transcripts",                 # transcript extraction (data), not copy
    "schema-markup",               # JSON-LD technical markup, not prose
    "paid-ads-report",             # analytics report, not copy
    "youtube-strategy",            # strategy doc, not copy
    "website-build",               # design-build (design contract covers it; website-copy is the copy skill)
    "website-clone",               # design-build
    "website-wireframe",           # design-build
}


def parse_frontmatter(filepath: Path) -> Optional[dict]:
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except Exception:
        return None


def is_copy_skill(filepath: Path, frontmatter: dict) -> bool:
    """Same discrimination logic as validate-frontmatter.py is_copy_skill()."""
    path_str = str(filepath).lower()
    if "/skills/primitives/" not in path_str:
        return False
    if "/audit/" in path_str or "audit" in filepath.parent.name.lower():
        return False
    if "/research/" in path_str:
        return False
    if filepath.parent.name in COPY_EXCLUDED_SKILL_NAMES:
        return False
    if frontmatter.get("primitive") not in COPY_PRIMITIVES:
        return False
    if frontmatter.get("sub_primitive") in COPY_EXCLUDED_SUB_PRIMITIVES:
        return False
    return True


def has_copywriting_gate(filepath: Path) -> bool:
    """Idempotency check: body already references the rule?"""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return False
    body_match = re.match(r"^---\s*\n.*?\n---\s*\n(.*)$", text, re.DOTALL)
    body = body_match.group(1) if body_match else text
    return "persuasion-and-stickiness" in body


def insert_gate(filepath: Path, apply: bool = False) -> bool:
    """Insert the Persuasion & stickiness pass before the Changelog (or at end).

    Returns True if the file was (or would be) modified.
    """
    text = filepath.read_text(encoding="utf-8")

    # Relative path from this SKILL.md back up to .claude/rules/persuasion-and-stickiness.md.
    # rel_parts like ('primitives','{lane}','{stage}','{name}','SKILL.md'); depth = len - 1.
    # From SKILL.md's dir, `depth` ups reach .claude/skills/; one more reaches .claude/; then rules/.
    rel_parts = filepath.relative_to(SKILLS_ROOT).parts
    depth = len(rel_parts) - 1
    rel_rule = "../" * (depth + 1) + "rules/persuasion-and-stickiness.md"

    section = f"""
## Persuasion & stickiness pass

Output complies with [persuasion-and-stickiness.md]({rel_rule}) — Cialdini's 7 persuasion levers + Heath's SUCCESs. Deploy the 1-2 Cialdini levers that fit the reader's barrier (never all seven; every lever must be TRUE), run the SUCCESs diagnostic (Simple / Unexpected / Concrete / Credible / Emotional / Stories) over the near-final draft, then the rule's pre-ship gate.
"""

    changelog_match = re.search(r"^## Changelog", text, re.MULTILINE)
    if changelog_match:
        insert_pos = changelog_match.start()
        new_text = text[:insert_pos] + section.strip() + "\n\n---\n\n" + text[insert_pos:]
    else:
        sep = "" if text.endswith("\n") else "\n"
        new_text = text + sep + "\n---\n" + section

    if not apply:
        return True

    filepath.write_text(new_text, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Retrofit persuasion-and-stickiness.md reference into marketing-copy skills"
    )
    parser.add_argument("--apply", action="store_true", help="Write changes (default is dry-run preview)")
    args = parser.parse_args()
    apply = args.apply

    added = []
    skipped_already_present = []
    skipped_not_copy = []
    skipped_no_frontmatter = []

    skill_files = sorted(PRIMITIVES_ROOT.rglob("SKILL.md"))

    for sf in skill_files:
        fm = parse_frontmatter(sf)
        if fm is None:
            skipped_no_frontmatter.append(sf)
            continue
        if not is_copy_skill(sf, fm):
            skipped_not_copy.append(sf)
            continue
        if has_copywriting_gate(sf):
            skipped_already_present.append(sf)
            continue
        insert_gate(sf, apply=apply)
        added.append(sf)

    print(f"\n=== Migration report ({'APPLIED' if apply else 'DRY RUN — pass --apply to write'}) ===")
    print(f"Scanned: {len(skill_files)} SKILL.md files under primitives/")
    print(f"{'Added' if apply else 'Would add'} gate: {len(added)}")
    print(f"Skipped (already present): {len(skipped_already_present)}")
    print(f"Skipped (not a copy skill): {len(skipped_not_copy)}")
    print(f"Skipped (no frontmatter / parse error): {len(skipped_no_frontmatter)}")

    if added:
        print(f"\n--- {'ADDED' if apply else 'WOULD ADD'} gate to {len(added)} files ---")
        for f in added:
            print(f"  + {f.relative_to(SKILLS_ROOT.parent)}")

    if skipped_no_frontmatter:
        print(f"\n--- SKIPPED (no frontmatter) — investigate ---")
        for f in skipped_no_frontmatter:
            print(f"  ? {f.relative_to(SKILLS_ROOT.parent)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
