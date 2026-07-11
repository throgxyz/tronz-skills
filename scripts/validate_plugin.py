#!/usr/bin/env python3
"""Validate marketplace/plugin identity, versions, and local source path."""

import json
import sys
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1]).resolve()
    marketplace_path = root / ".claude-plugin" / "marketplace.json"
    marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))

    if marketplace.get("$schema") != "https://json.schemastore.org/claude-code-marketplace.json":
        raise SystemExit("marketplace.json is missing the Claude Code schema")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        raise SystemExit("marketplace.json must contain exactly one plugin")

    entry = plugins[0]
    source = entry.get("source")
    if not isinstance(source, str) or not source.startswith("./"):
        raise SystemExit("plugin source must be a repository-relative ./ path")

    plugin_root = (root / source).resolve()
    try:
        plugin_root.relative_to(root)
    except ValueError as exc:
        raise SystemExit("plugin source escapes the repository") from exc

    manifest_path = plugin_root / ".claude-plugin" / "plugin.json"
    if not manifest_path.is_file():
        raise SystemExit(f"plugin manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if entry.get("name") != manifest.get("name"):
        raise SystemExit("marketplace and plugin names differ")
    if entry.get("version") != manifest.get("version"):
        raise SystemExit("marketplace and plugin versions differ")
    if marketplace.get("metadata", {}).get("version") != manifest.get("version"):
        raise SystemExit("marketplace metadata and plugin versions differ")

    print("Plugin marketplace is valid!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
