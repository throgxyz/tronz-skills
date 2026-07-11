#!/usr/bin/env python3
"""Validate the required Agent Skill frontmatter."""

import re
import sys
from pathlib import Path

def main() -> int:
    skill_dir = Path(sys.argv[1])
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise SystemExit("invalid or missing SKILL.md frontmatter")

    frontmatter = match.group(1)
    keys = re.findall(r"^([a-zA-Z0-9_-]+):", frontmatter, re.MULTILINE)
    if keys != ["name", "description"]:
        raise SystemExit("SKILL.md frontmatter must contain only name and description")
    name_match = re.search(r"^name:\s*(\S+)\s*$", frontmatter, re.MULTILINE)
    if not name_match or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name_match.group(1)):
        raise SystemExit("skill name must use lowercase hyphen-case")
    if not re.search(r"^description:\s*(?:>-)?.+$", frontmatter, re.MULTILINE):
        raise SystemExit("skill description must be a non-empty string")

    print("Skill is valid!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
