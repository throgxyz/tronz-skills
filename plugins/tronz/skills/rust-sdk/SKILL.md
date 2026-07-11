---
name: rust-sdk
description: >-
  Build, review, or debug Rust applications using tronz 0.3.x, including gRPC
  providers, TRX/TRC10/TRC20/TRC721 transfers, account and resource queries,
  TVM contract calls and deployment, tron_sol! bindings, events, staking,
  governance, LocalSigner, mnemonics, keystores, and AWS KMS. Use whenever a
  task involves tronz, a tronz-* crate, or TRON development in Rust. Do not use
  for TronWeb, TronBox, Java, or Go SDKs.
---

# tronz Rust SDK

Target `tronz 0.3.x`. Treat exact API names as version-sensitive.

## Work from evidence

1. Inspect the project's installed `tronz` version and enabled features.
2. Prefer local crate source when available; otherwise use the official
   [documentation](https://throgxyz.github.io/docs/) and
   [runnable examples](https://github.com/throgxyz/examples).
3. Read [references/api-map.md](references/api-map.md) for the task's API and
   example route.
4. Read [references/pitfalls.md](references/pitfalls.md) before generating
   transaction, amount, address, contract, or event code.
5. Compile or test generated Rust when a project or toolchain is available.
6. Do not infer missing APIs from alloy, TronWeb, or older tronz releases.

## Minimal setup

The default feature set includes the TLS gRPC provider, contracts, and
`LocalSigner`:

```toml
[dependencies]
anyhow = "1"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
tronz = "0.3"
```

Enable optional features only when needed:

- `signer-mnemonic` — BIP-39/BIP-44 derivation.
- `signer-keystore` — Web3 Secret Storage V3.
- `signer-aws` — AWS KMS signer.
- `provider-grpc` — gRPC transport without TLS.

`full` is currently an alias for the default feature set; it does not enable
the optional signer features.

## Non-negotiable rules

- Use a bare provider for reads. For sends, attach both
  `.with_recommended_fillers()` and `.with_signer(...)`.
- Use `tronz::Address` in TRON APIs. Convert to/from alloy's 20-byte address at
  ABI boundaries with `.into()`.
- Parse TRX exactly with `"1.5".parse::<Trx>()` or `parse_trx`; never use
  floating point. Format with `Display` or `format_trx`.
- Use `Trx` only for native TRX/sun. Use raw `U256` plus token decimals for
  TRC20/TRC721 values.
- Inspect both receipt `status` and `contract_result` for contract writes.
- Treat `tron_sol!` as Alpha. Prefer built-in TRC20/TRC721 instances for
  standard tokens.
- Do not assume `eth_getLogs`; query and decode TRON transaction receipts.

## Choose the API

- Native TRX: `TronProvider::send_trx()`.
- TRC10: extension APIs under `tronz::providers::ext`.
- TRC20: `Trc20Ext::trc20(address)`.
- TRC721: `Trc721Ext::trc721(address)`.
- Compile-time custom ABI: `tron_sol!`.
- Runtime JSON ABI: `Interface` and `ContractInstance`.
- Raw calldata: `ContractInstance::call_raw`.
- Events: generated filters or `decode_log` / `decode_logs`.
- Stake 2.0: `freeze_balance`, `unfreeze_balance`, `delegate_resource`, and
  `undelegate_resource`.

For a new read-only client, copy the template in
[assets/scaffold-client](assets/scaffold-client). For an interactive Claude Code
workflow, use `/tronz:scaffold-client`.
