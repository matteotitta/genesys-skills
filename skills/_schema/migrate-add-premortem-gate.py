#!/usr/bin/env python3
"""migrate-add-premortem-gate.py

One-shot retrofit: walk .claude/skills/primitives/, identify output skills per
the premortem-production.md contract, and append a "## Final ship gate" section
to each SKILL.md body. Idempotent — skip if the section is already present.

Discrimination logic mirrors check_output_premortem_contract() in
validate-frontmatter.py. Pure-research, meta, and audit skills are excluded.

Output: per-file report (added / skipped-already-present / skipped-not-output)
plus a summary at end. Designed to be safe to re-run.

Usage:
    python3 .claude/skills/_schema/migrate-add-premortem-gate.py
    python3 .claude/skills/_schema/migrate-add-premortem-gate.py --dry-run
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

OUTPUT_PRIMITIVES = {
    "content",
    "sales-enablement",
    "outbound",
    "lifecycle",
    "social",
    "paid-marketing",
    "website",
    "design",
    "product-marketing",
    "seo-aeo",
    "clients",
}

SHIP_GATE_SECTION = """
## Final ship gate

Run `/premortem --output` before ship. See [`.claude/skills/meta/orchestration/premortem/SKILL.md`](../../../../meta/orchestration/premortem/SKILL.md) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
"""


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


def is_output_skill(filepath: Path, frontmatter: dict) -> bool:
    """Same discrimination logic as validate-frontmatter.py."""
    path_str = str(filepath).lower()
    # Must be under primitives/ — excludes _archive/, _flagged/, research/, meta/
    if "/skills/primitives/" not in path_str:
        return False
    primitive = frontmatter.get("primitive")
    if primitive not in OUTPUT_PRIMITIVES:
        return False
    if "/audit/" in path_str:
        return False
    if "audit" in filepath.parent.name.lower():
        return False
    return True


def has_premortem_gate(filepath: Path) -> bool:
    """Idempotency check: already has the reference?"""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return False
    body_match = re.match(r"^---\s*\n.*?\n---\s*\n(.*)$", text, re.DOTALL)
    body = body_match.group(1) if body_match else text
    return "/premortem --output" in body


def insert_ship_gate(filepath: Path, dry_run: bool = False) -> bool:
    """Insert the Final ship gate section before the Changelog (or at end if no Changelog).

    Returns True if the file was modified (or would be in dry-run mode).
    """
    text = filepath.read_text(encoding="utf-8")

    # Build relative path back to premortem skill — compute from this file's location
    # .claude/skills/primitives/{lane}/{stage}/{skill}/SKILL.md → up 4 levels to .claude/skills/
    # then meta/orchestration/premortem/SKILL.md
    rel_parts = filepath.relative_to(SKILLS_ROOT).parts
    # rel_parts is like ('primitives', 'content', 'execution', 'aeo-content', 'SKILL.md')
    # depth = len(rel_parts) - 1 (subtract SKILL.md itself)
    depth = len(rel_parts) - 1
    up = "../" * depth
    rel_premortem = f"{up}meta/orchestration/premortem/SKILL.md"

    section = f"""
## Final ship gate

Run `/premortem --output` before ship. See [`/premortem` skill]({rel_premortem}) for the 5 execution domains (will-it-resonate / will-it-convert / will-it-stay-on-brand / will-stakeholder-push-back / will-it-degrade-over-time) and output template.

Trivial-case escape: `## Premortem\\nNo failure modes — trivial change` satisfies the contract for genuinely trivial outputs.
"""

    # Try to insert before "## Changelog" heading
    changelog_match = re.search(r"^## Changelog", text, re.MULTILINE)
    if changelog_match:
        insert_pos = changelog_match.start()
        new_text = text[:insert_pos] + section.strip() + "\n\n---\n\n" + text[insert_pos:]
    else:
        # Append at end with separator
        sep = "" if text.endswith("\n") else "\n"
        new_text = text + sep + "\n---\n" + section

    if dry_run:
        return True

    filepath.write_text(new_text, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Retrofit /premortem --output reference into output skills")
    parser.add_argument("--dry-run", action="store_true", help="Report what would change without writing")
    args = parser.parse_args()

    added = []
    skipped_already_present = []
    skipped_not_output = []
    skipped_no_frontmatter = []

    skill_files = sorted(PRIMITIVES_ROOT.rglob("SKILL.md"))

    for sf in skill_files:
        fm = parse_frontmatter(sf)
        if fm is None:
            skipped_no_frontmatter.append(sf)
            continue
        if not is_output_skill(sf, fm):
            skipped_not_output.append(sf)
            continue
        if has_premortem_gate(sf):
            skipped_already_present.append(sf)
            continue
        # This skill needs the gate
        insert_ship_gate(sf, dry_run=args.dry_run)
        added.append(sf)

    # Report
    print(f"\n=== Migration report ({'DRY RUN' if args.dry_run else 'APPLIED'}) ===")
    print(f"Scanned: {len(skill_files)} SKILL.md files under primitives/")
    print(f"Added gate: {len(added)}")
    print(f"Skipped (already present): {len(skipped_already_present)}")
    print(f"Skipped (not output skill): {len(skipped_not_output)}")
    print(f"Skipped (no frontmatter / parse error): {len(skipped_no_frontmatter)}")

    if added:
        print(f"\n--- ADDED gate to {len(added)} files ---")
        for f in added:
            print(f"  + {f.relative_to(SKILLS_ROOT.parent)}")

    if skipped_no_frontmatter:
        print(f"\n--- SKIPPED (no frontmatter) — investigate ---")
        for f in skipped_no_frontmatter:
            print(f"  ? {f.relative_to(SKILLS_ROOT.parent)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
