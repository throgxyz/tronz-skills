# tronz-skills

Agent Skills and a Claude Code plugin for the
[tronz](https://github.com/throgxyz/tronz) Rust SDK for TRON.

The `rust-sdk` skill teaches an AI agent to write, review, and debug Rust code
that uses tronz: building providers, sending TRX / TRC10 / TRC20, calling and
deploying TVM contracts, decoding events, staking, governance, and key
management — with verified API names instead of guesses.

## Layout

```
tronz-skills/
├── .claude-plugin/
│   └── marketplace.json          # Claude Code plugin marketplace
└── plugins/
    └── tronz/                    # the plugin
        ├── .claude-plugin/plugin.json
        ├── commands/
        │   └── scaffold-client.md   # /tronz:scaffold-client
        └── skills/
            └── rust-sdk/            # the skill (SKILL.md + references/)
```

## Install

### Claude Code (plugin marketplace)

```
/plugin marketplace add throgxyz/tronz-skills
/plugin install tronz@tronz
```

The skill loads as `tronz:rust-sdk`; the command is `/tronz:scaffold-client`.

### Any other host (manual copy)

`plugins/tronz/skills/rust-sdk/` follows the open Agent Skills standard and works
with Cursor, Codex, Gemini CLI, and others:

```bash
mkdir -p ~/.claude/skills && cp -r plugins/tronz/skills/rust-sdk ~/.claude/skills/
```

See `plugins/tronz/skills/rust-sdk/INSTALL.md` for per-host details.

## Keeping it current

The skill is versioned alongside the SDK. When the public tronz API changes,
update the matching `references/*.md` and `examples-index.md` in the same PR that
changes the crate, so the skill never drifts.

## License

MIT OR Apache-2.0.
