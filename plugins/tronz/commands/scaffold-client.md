---
name: scaffold-client
description: Scaffold a minimal compiling tronz 0.3.x read-only client.
---

# `/tronz:scaffold-client`

Create a new read-only tronz client from
`${CLAUDE_PLUGIN_ROOT}/skills/rust-sdk/assets/scaffold-client/`.

1. Ask for the destination only when it cannot be inferred. Do not overwrite
   existing files without confirmation.
2. Copy that template directory to the destination. Resolve it from
   `${CLAUDE_PLUGIN_ROOT}`; do not look for it relative to the user's project.
3. Keep mainnet unless the user requests Nile; then replace
   `TRONGRID_MAINNET` with `TRONGRID_NILE`.
4. Run `cargo check` in the generated project.
5. Tell the user to set `TRON_ADDRESS` before running it.
6. Do not add a signer or private key to this read-only scaffold. For sends,
   explain that recommended fillers and a signer are both required.
