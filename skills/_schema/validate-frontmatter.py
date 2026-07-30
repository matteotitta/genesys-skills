#!/usr/bin/env python3
"""
Validate SKILL.md frontmatter against skill-frontmatter.schema.json.

Adopted from Gooseworks via /steal 2026-04-21 to replace regex-based grep
validation in .github/workflows/validate-skills.yml.

Usage:
    python validate-frontmatter.py [--all | --changed | <file_path> ...]

Exit codes:
    0 = all validated SKILL.md files conform to the schema
    1 = one or more validation errors
    2 = script error (missing dependency, schema not found, etc.)
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import ValidationError
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(2)


SCHEMA_PATH = Path(__file__).parent / "skill-frontmatter.schema.json"
SKILLS_ROOT = Path(".claude/skills")


def load_schema() -> dict:
    if not SCHEMA_PATH.exists():
        print(f"ERROR: schema not found at {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(2)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _stringify_dates(value):
    """Recursively convert datetime.date / datetime.datetime to ISO strings.

    PyYAML auto-coerces YAML dates like `2026-03-31` to datetime.date objects,
    but JSON Schema validates against the string type. This normalises before
    validation without changing the source files.
    """
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _stringify_dates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_stringify_dates(v) for v in value]
    return value


def parse_frontmatter(filepath: Path) -> dict | None:
    """Extract YAML frontmatter from a SKILL.md file. Returns None if missing."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    try:
        parsed = yaml.safe_load(match.group(1)) or {}
        return _stringify_dates(parsed)
    except yaml.YAMLError as e:
        print(f"  YAML parse error: {e}", file=sys.stderr)
        return None


def validate_file(filepath: Path, validator: Draft202012Validator) -> list[str]:
    """Validate one SKILL.md. Returns list of error messages (empty = pass)."""
    frontmatter = parse_frontmatter(filepath)
    if frontmatter is None:
        return ["missing or unparseable YAML frontmatter"]

    errors = []
    for err in validator.iter_errors(frontmatter):
        path = ".".join(str(p) for p in err.absolute_path) or "(root)"
        errors.append(f"{path}: {err.message}")
    return errors


# Primitives that produce visual/design output and therefore should follow the
# design-production.md authorship contract (Layer 1 of the propagation system).
DESIGN_PRIMITIVES = {"design", "website"}
# content+motion is the product-ui-frames pattern (HTML→MP4); same contract applies.
DESIGN_SUB_PRIMITIVES_FOR_CONTENT = {"motion"}


def is_design_output_skill(frontmatter: dict) -> bool:
    """Heuristic: should this skill follow the design-production.md authorship contract?"""
    primitive = frontmatter.get("primitive")
    if primitive in DESIGN_PRIMITIVES:
        return True
    if primitive == "content" and frontmatter.get("sub_primitive") in DESIGN_SUB_PRIMITIVES_FOR_CONTENT:
        return True
    return False


def check_design_authorship_contract(filepath: Path, frontmatter: dict) -> list[str]:
    """Soft-warn checks for design-output skills against design-production.md § Skill authorship contract.

    Returns a list of warning strings (empty = pass). These are warnings, not errors —
    the validator's exit code is not affected. The intent is to surface drift early
    so authors can self-correct.

    Skipped for non-design-output skills.
    """
    if not is_design_output_skill(frontmatter):
        return []

    warnings = []

    # Requirement 1: brand-kit in inputs.recommended (or inputs.required)
    inputs = frontmatter.get("inputs", {}) or {}
    recommended = inputs.get("recommended", []) or []
    required = inputs.get("required", []) or []
    if "brand-kit" not in recommended and "brand-kit" not in required:
        warnings.append(
            "design-contract: missing 'brand-kit' in inputs.recommended (or inputs.required). "
            "Per design-production.md authorship contract requirement 1."
        )

    # Read the body to check for the design-cycle section
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return warnings

    # Strip frontmatter
    body_match = re.match(r"^---\s*\n.*?\n---\s*\n(.*)$", content, re.DOTALL)
    body = body_match.group(1) if body_match else content

    # Requirement 3: "Design cycle" section in body (case-insensitive heading match)
    if not re.search(r"^##+\s*Design cycle", body, re.MULTILINE | re.IGNORECASE):
        warnings.append(
            "design-contract: missing 'Design cycle (post-authoring phases)' section in body. "
            "Per design-production.md authorship contract requirement 3. "
            "Uncomment the scaffold in _schema/SKILL.template.md."
        )

    # Requirement 5: explicit /design-reviewer final-gate mention
    if "/design-reviewer" not in body:
        warnings.append(
            "design-contract: body does not reference '/design-reviewer' as the final ship-ready gate. "
            "Per design-production.md authorship contract requirement 5."
        )

    return warnings


# Primitives whose skills are "output skills" per .claude/rules/premortem-production.md —
# their bodies must reference /premortem --output as the final ship gate.
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


def is_output_skill(filepath: Path, frontmatter: dict) -> bool:
    """Heuristic: should this skill follow the premortem-production.md output contract?

    IN scope: skills under .claude/skills/primitives/ whose primitive is in OUTPUT_PRIMITIVES,
    EXCEPT audit skills (which produce internal scores for triage, not shippable deliverables).

    OUT: all research/, meta/, _archive/, _flagged/, and audit skills.
    Path-based check (must be in primitives/) prevents meta-skills with output-flavored primitive
    (e.g., sales-enablement-index in meta/orchestration/) from being flagged.
    """
    path_str = str(filepath).lower()
    # Must be under primitives/ — excludes _archive/, _flagged/, research/, meta/
    if "/skills/primitives/" not in path_str:
        return False
    primitive = frontmatter.get("primitive")
    if primitive not in OUTPUT_PRIMITIVES:
        return False
    # Exclude *-audit skills (their output is an internal score, not a shippable artifact)
    if "/audit/" in path_str or "audit" in filepath.parent.name.lower():
        return False
    return True


def check_output_premortem_contract(filepath: Path, frontmatter: dict) -> list[str]:
    """Soft-warn checks for output skills against premortem-production.md.

    Returns a list of warning strings (empty = pass). These are warnings, not errors —
    validator exit code is not affected. Surface drift early so authors can self-correct.

    Skipped for non-output skills (research, meta, audit).
    """
    if not is_output_skill(filepath, frontmatter):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    # Strip frontmatter
    body_match = re.match(r"^---\s*\n.*?\n---\s*\n(.*)$", content, re.DOTALL)
    body = body_match.group(1) if body_match else content

    warnings = []

    # Requirement: explicit /premortem --output reference in body
    if "/premortem --output" not in body:
        warnings.append(
            "premortem-contract: body does not reference '/premortem --output' as the final ship gate. "
            "Per .claude/rules/premortem-production.md. "
            "Add a '## Final ship gate' section near end-of-body — see scaffold in _schema/SKILL.template.md."
        )

    return warnings


# Primitives whose skills publish prose in a brand voice and therefore should
# declare a /voice-reviewer ship gate (pm-loop.md § lens-reviewer). Content-tier.
VOICE_PRIMITIVES = {"social", "content"}
# sub_primitives within those that are NOT voice-published content:
#   motion    → design-output (covered by the design-authorship contract)
#   strategy  → internal strategy docs, not published copy
VOICE_EXCLUDED_SUB_PRIMITIVES = {"motion", "strategy"}


def is_content_tier_skill(filepath: Path, frontmatter: dict) -> bool:
    """Heuristic: should this skill declare a /voice-reviewer ship gate?

    IN scope: primitives/ skills whose primitive is social or content that publish
    prose in a brand voice.
    OUT: audit skills (internal scores), motion (design contract covers them),
    strategy sub-primitives (internal strategy docs, not published copy), and
    anything outside primitives/.
    """
    path_str = str(filepath).lower()
    if "/skills/primitives/" not in path_str:
        return False
    if "/audit/" in path_str or "audit" in filepath.parent.name.lower():
        return False
    if frontmatter.get("primitive") not in VOICE_PRIMITIVES:
        return False
    if frontmatter.get("sub_primitive") in VOICE_EXCLUDED_SUB_PRIMITIVES:
        return False
    return True


def check_voice_reviewer_contract(filepath: Path, frontmatter: dict) -> list[str]:
    """Soft-warn checks for content-tier skills against the lens-reviewer contract.

    Returns a list of warning strings (empty = pass). These are warnings, not errors —
    the validator's exit code is unaffected. Surface drift early so authors self-correct.

    Skipped for non-content-tier skills.
    """
    if not is_content_tier_skill(filepath, frontmatter):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    # Strip frontmatter
    body_match = re.match(r"^---\s*\n.*?\n---\s*\n(.*)$", content, re.DOTALL)
    body = body_match.group(1) if body_match else content

    warnings = []

    # Requirement: explicit /voice-reviewer reference in body (the content ship gate)
    if "/voice-reviewer" not in body:
        warnings.append(
            "voice-contract: body does not reference '/voice-reviewer' as the final content ship gate. "
            "Per pm-loop.md § lens-reviewer (voice-reviewer validates content quality). "
            "Add a '## Final ship gate' section near end-of-body naming /voice-reviewer."
        )

    return warnings


# Primitive whose skills produce client-facing deliverables (proposals, decks,
# battlecards) and therefore should declare a /scope-guardian-reviewer ship gate.
SCOPE_GUARDIAN_PRIMITIVES = {"sales-enablement"}


def is_client_deliverable_skill(filepath: Path, frontmatter: dict) -> bool:
    """Heuristic: should this skill declare a /scope-guardian-reviewer ship gate?

    IN scope: primitives/ sales-enablement skills (client-facing decks, battlecards,
    proposals). OUT: audit skills and anything outside primitives/.
    """
    path_str = str(filepath).lower()
    if "/skills/primitives/" not in path_str:
        return False
    if "/audit/" in path_str or "audit" in filepath.parent.name.lower():
        return False
    return frontmatter.get("primitive") in SCOPE_GUARDIAN_PRIMITIVES


def check_scope_guardian_contract(filepath: Path, frontmatter: dict) -> list[str]:
    """Soft-warn checks for client-deliverable skills against the lens-reviewer contract.

    Returns a list of warning strings (empty = pass). These are warnings, not errors —
    the validator's exit code is unaffected. Skipped for non-client-deliverable skills.
    """
    if not is_client_deliverable_skill(filepath, frontmatter):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    # Strip frontmatter
    body_match = re.match(r"^---\s*\n.*?\n---\s*\n(.*)$", content, re.DOTALL)
    body = body_match.group(1) if body_match else content

    warnings = []

    # Requirement: explicit /scope-guardian-reviewer reference in body
    if "/scope-guardian-reviewer" not in body:
        warnings.append(
            "scope-guardian-contract: body does not reference '/scope-guardian-reviewer' as the client-deliverable ship gate. "
            "Per pm-loop.md § lens-reviewer (scope-guardian checks proposals/SOWs for scope creep). "
            "Add a '## Final ship gate' section near end-of-body naming /scope-guardian-reviewer."
        )

    return warnings


# Primitives whose skills produce persuasive marketing copy and therefore should
# reference .claude/rules/persuasion-and-stickiness.md (Cialdini's 7 persuasion
# levers + Heath's SUCCESs stickiness framework). Marketing-copy execution lanes only.
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
# sub_primitives within those lanes that are NOT persuasive copy:
#   strategy       → upstream strategy docs (positioning/messaging/pricing) — excluded per scope
#   motion         → design/video output (the design contract covers it)
#   list-building  → data-ops (TAM / list construction), not copy
#   enrichment     → data-ops (contact enrichment), not copy
#   research       → research sub-lanes, not copy
COPY_EXCLUDED_SUB_PRIMITIVES = {"strategy", "motion", "list-building", "enrichment", "research"}
# Skills that live in a copy lane but whose OUTPUT is not persuasive prose — their
# primitive/sub_primitive matches a copy lane, but the deliverable is data-ops,
# technical markup, an analytics report, a strategy doc, or a design-build. Excluded
# by folder name because no single frontmatter field cleanly separates them.
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


def is_copy_skill(filepath: Path, frontmatter: dict) -> bool:
    """Heuristic: should this skill reference persuasion-and-stickiness.md?

    IN scope: primitives/ skills in a marketing-copy lane (COPY_PRIMITIVES) whose
    output is persuasive copy.
    OUT: audit skills (internal scores), research/ sub-lanes, the list-building /
    enrichment / research / strategy / motion sub-primitives (data-ops, upstream
    strategy, design-video), the named non-copy skills above, and anything outside
    primitives/.
    """
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


def check_copywriting_contract(filepath: Path, frontmatter: dict) -> list[str]:
    """Soft-warn checks for marketing-copy skills against persuasion-and-stickiness.md.

    Returns a list of warning strings (empty = pass). These are warnings, not errors —
    the validator's exit code is unaffected. Surface drift early so authors self-correct.

    Skipped for non-copy skills (strategy, research, audit, data-ops, motion).
    """
    if not is_copy_skill(filepath, frontmatter):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    # Strip frontmatter
    body_match = re.match(r"^---\s*\n.*?\n---\s*\n(.*)$", content, re.DOTALL)
    body = body_match.group(1) if body_match else content

    warnings = []

    # Requirement: body references the persuasion-and-stickiness rule (Cialdini + Heath).
    if "persuasion-and-stickiness" not in body:
        warnings.append(
            "copywriting-contract: body does not reference .claude/rules/persuasion-and-stickiness.md "
            "(Cialdini's 7 persuasion levers + Heath's SUCCESs stickiness framework). "
            "Add it to the 'Output complies with […]' line, or add a '## Persuasion & stickiness pass' section."
        )

    return warnings


def collect_files(args: argparse.Namespace) -> list[Path]:
    if args.files:
        return [Path(f) for f in args.files]
    if args.all:
        return sorted(SKILLS_ROOT.rglob("SKILL.md"))
    if args.changed:
        # Read newline-separated paths from stdin
        return [Path(line.strip()) for line in sys.stdin if line.strip().endswith("SKILL.md")]
    print("ERROR: specify --all, --changed, or one or more file paths", file=sys.stderr)
    sys.exit(2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="validate every SKILL.md under .claude/skills/")
    parser.add_argument("--changed", action="store_true", help="read changed file paths from stdin")
    parser.add_argument("files", nargs="*", help="explicit SKILL.md paths to validate")
    args = parser.parse_args()

    schema = load_schema()
    validator = Draft202012Validator(schema)

    files = collect_files(args)
    if not files:
        print("No SKILL.md files to validate.")
        return 0

    total_errors = 0
    failed_files = 0
    total_warnings = 0
    warned_files = 0

    for filepath in files:
        if not filepath.exists():
            print(f"SKIP (not found): {filepath}")
            continue
        errors = validate_file(filepath, validator)
        if errors:
            failed_files += 1
            total_errors += len(errors)
            print(f"\nFAIL: {filepath}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"PASS: {filepath}")

        # Soft-warn checks (do not affect exit code)
        # Re-parse frontmatter for the warning checks (cheap; same file already in cache)
        frontmatter = parse_frontmatter(filepath)
        if frontmatter is not None:
            warnings = check_design_authorship_contract(filepath, frontmatter)
            if warnings:
                warned_files += 1
                total_warnings += len(warnings)
                print(f"  WARN (design-contract): {filepath}")
                for w in warnings:
                    print(f"    - {w}")

            premortem_warnings = check_output_premortem_contract(filepath, frontmatter)
            if premortem_warnings:
                # Only count this file once in warned_files even if both checks warn
                if not warnings:
                    warned_files += 1
                total_warnings += len(premortem_warnings)
                print(f"  WARN (premortem-contract): {filepath}")
                for w in premortem_warnings:
                    print(f"    - {w}")

            voice_warnings = check_voice_reviewer_contract(filepath, frontmatter)
            if voice_warnings:
                # Count this file once even if earlier contracts already warned
                if not warnings and not premortem_warnings:
                    warned_files += 1
                total_warnings += len(voice_warnings)
                print(f"  WARN (voice-contract): {filepath}")
                for w in voice_warnings:
                    print(f"    - {w}")

            scope_warnings = check_scope_guardian_contract(filepath, frontmatter)
            if scope_warnings:
                if not warnings and not premortem_warnings and not voice_warnings:
                    warned_files += 1
                total_warnings += len(scope_warnings)
                print(f"  WARN (scope-guardian-contract): {filepath}")
                for w in scope_warnings:
                    print(f"    - {w}")

            copywriting_warnings = check_copywriting_contract(filepath, frontmatter)
            if copywriting_warnings:
                if not warnings and not premortem_warnings and not voice_warnings and not scope_warnings:
                    warned_files += 1
                total_warnings += len(copywriting_warnings)
                print(f"  WARN (copywriting-contract): {filepath}")
                for w in copywriting_warnings:
                    print(f"    - {w}")

    print("")
    print(f"=== Summary: {len(files)} validated, {failed_files} failed, {total_errors} errors, {warned_files} with warnings, {total_warnings} warnings total ===")
    return 1 if failed_files else 0


if __name__ == "__main__":
    sys.exit(main())
