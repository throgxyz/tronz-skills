#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL="$ROOT/plugins/tronz/skills/rust-sdk"
python3 "$ROOT/scripts/validate_skill.py" "$SKILL"
python3 "$ROOT/scripts/validate_plugin.py" "$ROOT"

python3 -m json.tool "$ROOT/.claude-plugin/marketplace.json" >/dev/null
python3 -m json.tool "$ROOT/plugins/tronz/.claude-plugin/plugin.json" >/dev/null

if rg -n \
  'tronz[[:space:]]*=[[:space:]]*"0\.1|full turns them all on|features[[:space:]]*=[[:space:]]*\["full"\]' \
  "$ROOT/plugins" "$ROOT/README.md"; then
  echo "error: found a known pre-0.3 API or feature claim"
  exit 1
fi

if rg -n 'from_trx|as_trx' "$ROOT/plugins" --glob '!pitfalls.md'; then
  echo "error: found a removed amount API outside the pitfalls reference"
  exit 1
fi

CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-/tmp/tronz-skills-target}" \
  cargo check --manifest-path "$SKILL/assets/scaffold-client/Cargo.toml"

echo "all tronz skill checks passed"
