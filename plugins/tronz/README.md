# tronz plugin

Claude Code plugin for the [tronz](https://github.com/throgxyz/tronz) Rust SDK for TRON.

## Contents

- `skills/rust-sdk/` — the `rust-sdk` skill: write, review, and debug Rust code
  that uses tronz (providers, TRX/TRC10/TRC20 transfers, smart-contract
  call/deploy, event decoding, staking, key management).
- `commands/scaffold-client.md` — `/tronz:scaffold-client`, scaffolds a minimal
  read-only tronz client.

## Install

```
/plugin marketplace add throgxyz/tronz-skills
/plugin install tronz@tronz
```

The skill folder also follows the open Agent Skills standard and can be copied
directly into any compatible host — see `skills/rust-sdk/INSTALL.md`.
