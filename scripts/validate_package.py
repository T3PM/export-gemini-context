#!/usr/bin/env python3
"""Static smoke checks for the export-gemini-context plugin package.

This script intentionally uses only Python's standard library. It validates
package shape and regression markers; it does not prove Antigravity runtime
compatibility or that an export contains no secrets.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SCHEMA_URL = "https://antigravity.google/schemas/v1/plugin.json"
REQUIRED_FILES = (
    "plugin.json",
    "README.md",
    "LICENSE",
    "skills/export-gemini-context/SKILL.md",
    "skills/agy-implementation/SKILL.md",
    "prompts/gemini-planning.md",
    "prompts/agy-implementation.md",
)
LEGACY_MIRRORS = (
    ".agents/skills/export-gemini-context/SKILL.md",
    ".agents/skills/agy-implementation/SKILL.md",
)
SKILLS = {
    "skills/export-gemini-context/SKILL.md": "export-gemini-context",
    "skills/agy-implementation/SKILL.md": "agy-implementation",
}
REQUIRED_MARKERS = {
    "skills/export-gemini-context/SKILL.md": (
        "Security and privacy gate",
        "Tiered extraction algorithm",
        "Framework-aware discovery",
        "Final quality gate",
    ),
    "skills/agy-implementation/SKILL.md": (
        "Critical-file manifest comparison",
        "Contract and interface drift comparison",
        "Phase 2: implementation after approval",
    ),
    "prompts/gemini-planning.md": (
        "work_order_schema_version: agy-change-request/v2",
        "requires_phase1_revalidation: true",
        "direct_human_approval_required: true",
    ),
    "prompts/agy-implementation.md": (
        "snapshot_assessment",
        "drift_impact",
        "revalidation ID",
    ),
}


def read_text(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Cannot read {path}: {exc}")
        return ""


def check_frontmatter(path: Path, expected_name: str, errors: list[str]) -> None:
    text = read_text(path, errors)
    if not text:
        return
    match = re.match(r"\A---\r?\n(?P<body>.*?)\r?\n---\r?\n", text, re.DOTALL)
    if not match:
        errors.append(f"{path}: missing YAML frontmatter")
        return
    body = match.group("body")
    name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", body, re.MULTILINE)
    description = re.search(r'^description:\s*".+"\s*$', body, re.MULTILINE)
    if not name or name.group(1) != expected_name:
        errors.append(f"{path}: expected name {expected_name}")
    if not description:
        errors.append(f"{path}: missing quoted description")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate plugin package shape.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Plugin root. Defaults to this script's parent directory.",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing required file: {relative}")

    manifest_path = root / "plugin.json"
    manifest_text = read_text(manifest_path, errors)
    if manifest_text:
        try:
            manifest = json.loads(manifest_text)
        except json.JSONDecodeError as exc:
            errors.append(f"plugin.json is invalid JSON: {exc}")
        else:
            expected = {
                "$schema": SCHEMA_URL,
                "name": "export-gemini-context",
            }
            for key, value in expected.items():
                if manifest.get(key) != value:
                    errors.append(f"plugin.json: expected {key} to equal {value}")
            if not isinstance(manifest.get("description"), str) or not manifest["description"]:
                errors.append("plugin.json: description must be a non-empty string")
            unexpected = set(manifest) - {"$schema", "name", "description"}
            if unexpected:
                errors.append(
                    "plugin.json contains fields outside the documented schema: "
                    + ", ".join(sorted(unexpected))
                )

    for relative, expected_name in SKILLS.items():
        check_frontmatter(root / relative, expected_name, errors)

    for relative, markers in REQUIRED_MARKERS.items():
        content = read_text(root / relative, errors)
        for marker in markers:
            if marker not in content:
                errors.append(f"{relative}: missing production marker: {marker}")

    for relative in LEGACY_MIRRORS:
        if (root / relative).exists():
            errors.append(
                f"Legacy duplicate skill remains: {relative}. "
                "Keep skills/ as the single source of truth."
            )

    readme = read_text(root / "README.md", errors)
    if "python scripts/validate_package.py" not in readme:
        errors.append("README.md does not document the validator command")

    if errors:
        print("Package validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Package validation passed: {root}")
    print("Static checks only; perform a real Antigravity install smoke test before release.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
