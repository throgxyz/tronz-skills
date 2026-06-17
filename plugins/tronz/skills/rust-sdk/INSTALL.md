# Installing the tronz skill

This skill follows the open Agent Skills standard (a folder with `SKILL.md` +
`references/`). It works with any host that reads skills: Claude Code, Cursor,
OpenAI Codex, Gemini CLI, and others.

## Option A — manual copy (works everywhere)
Copy the `rust-sdk/` skill folder into your agent's skills directory:

```bash
# Claude Code, project-local (recommended; commit it with the repo)
mkdir -p .claude/skills && cp -r plugins/tronz/skills/rust-sdk .claude/skills/

# Claude Code, global (available in every project)
mkdir -p ~/.claude/skills && cp -r plugins/tronz/skills/rust-sdk ~/.claude/skills/
```

For Cursor: add via **Settings → Rules → Add Rule → Remote Rule (GitHub)** pointing
at this repo, or copy `rust-sdk/` into the project's rules/skills directory.

For Codex / other AGENTS.md-based tools: place `rust-sdk/` where the tool discovers
skills (often `.agent/skills/` or `.codex/skills/`).

## Option B — Claude Code plugin marketplace
This repo ships a `.claude-plugin/marketplace.json` so it can be registered as a
plugin marketplace:

```
/plugin marketplace add throgxyz/tronz-skills
/plugin install tronz@tronz
```

(Exact plugin/marketplace manifest fields evolve — if install fails, check the
current Claude Code plugin docs and adjust `.claude-plugin/marketplace.json`.)

## Verifying it loaded
Ask the agent something tronz-specific, e.g. *"using tronz, write a read-only
script that prints the USDT balance of an address on mainnet."* It should pull in
this skill, use `ProviderBuilder` + `Trc20Ext`, and not invent API names.

## Keeping it current
The skill is versioned with the SDK. When the public API changes, update the
matching `references/*.md` and the `examples-index.md` mapping in the same PR that
changes the code, so the skill never drifts from the crate.
