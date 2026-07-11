# tronz Skills

[![CI](https://github.com/throgxyz/tronz-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/throgxyz/tronz-skills/actions/workflows/ci.yml)
[![tronz 0.3.x](https://img.shields.io/badge/tronz-0.3.x-4c1)](https://github.com/throgxyz/tronz/releases/tag/v0.3.0)
[![plugin 0.2.0](https://img.shields.io/badge/plugin-0.2.0-blue)](https://github.com/throgxyz/tronz-skills)
[![license](https://img.shields.io/badge/license-MIT%20OR%20Apache--2.0-blue)](https://github.com/throgxyz/tronz-skills#license)

Official Agent Skill and Claude Code plugin for the
[tronz](https://github.com/throgxyz/tronz) Rust SDK for TRON.

The `rust-sdk` skill helps agents choose verified tronz 0.3.x APIs, avoid
TRON-specific integration mistakes, and route to the official
[documentation](https://throgxyz.github.io/docs/) and
[runnable examples](https://github.com/throgxyz/examples).

## Install

### Claude Code plugin

```text
/plugin marketplace add throgxyz/tronz-skills
/plugin install tronz@tronz
```

This installs the `tronz:rust-sdk` skill and the
`/tronz:scaffold-client` command.

### Agent Skill

Copy `plugins/tronz/skills/rust-sdk/` into the skill directory used by your
agent host. Common locations include:

```text
.claude/skills/rust-sdk/   # Claude Code, project-local
~/.claude/skills/rust-sdk/ # Claude Code, user-local
~/.codex/skills/rust-sdk/  # Codex, user-local
```

Consult the host's current documentation when its discovery path differs.

## Contents

```text
plugins/tronz/
├── commands/scaffold-client.md
└── skills/rust-sdk/
    ├── SKILL.md
    ├── agents/openai.yaml
    ├── assets/scaffold-client/
    └── references/
        ├── api-map.md
        └── pitfalls.md
```

The skill is intentionally thin: detailed tutorials live in the docs and full
programs live in the examples repository.

## Validate

Run the local checks:

```sh
./scripts/validate.sh
```

The scaffold build requires `protoc` (`protobuf-compiler` on Debian/Ubuntu).

The validation rejects known pre-0.3 APIs, validates `SKILL.md`, parses plugin
JSON, and compiles the scaffold client.

When tronz publishes a new minor release, update the version-sensitive rules,
API map, and scaffold in the same change, then run validation.

## License

MIT OR Apache-2.0.
