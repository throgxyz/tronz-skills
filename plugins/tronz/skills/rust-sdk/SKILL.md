---
name: rust-sdk
description: >-
  Write, review, or debug Rust code that uses the **tronz** SDK — the idiomatic,
  async-first Rust SDK for the TRON blockchain, modeled on alloy. Use this skill
  whenever the task involves tronz or building a TRON client in Rust: connecting
  to a node over gRPC, sending TRX / TRC10 / TRC20 transfers, querying balances
  and account resources, calling or deploying TVM smart contracts, encoding
  calldata, decoding logs/events, estimating energy, staking (freeze / unfreeze /
  delegate / claim rewards), voting for super representatives, or managing keys
  (LocalSigner, mnemonic, keystore). Trigger this even when the user only says
  "TRON in Rust", "TRC20 in Rust", "decode a TRON event", or names a crate like
  tronz-provider, tronz-contract, tronz-signer, or tronz-primitives — even if
  they don't say "tronz" explicitly. Do NOT use for the TronWeb/TronBox JS stack
  or for gotron Go SDKs.
---

# tronz — Rust SDK for TRON

`tronz` is an async-first Rust SDK for TRON, deliberately mirroring
[alloy](https://github.com/alloy-rs/alloy)'s shapes (`ProviderBuilder`, filler
chain, `sol!` bindings). If you know alloy, the ergonomics transfer directly.
TVM is EVM-compatible at the contract layer, so TRC20 ABI encode/decode is
identical to ERC-20 — tronz reuses alloy's ABI machinery.

**Bias toward the repo, not memory.** API names below are verified against
tronz 0.1.x, but versions move. When unsure of an exact signature, read the
matching file in the `tronz-examples` repo (see `examples-index.md`) or the crate
source rather than guessing.

**MSRV: Rust 1.85 (2024 edition).** Everything is `async` and assumes tokio.

## Crate map

| Crate | What's in it |
|---|---|
| `tronz` | Meta-crate. Re-exports everything. Depend on this. |
| `tronz-primitives` | `Address`, `Trx`, `U256`/`B256`/`Bytes`, `ResourceCode`, `RecoverableSignature` |
| `tronz-signer` | `TronSigner` trait, `LocalSigner`, `MnemonicBuilder`, keystore |
| `tronz-provider` | gRPC transport, `ProviderBuilder`, `TronProvider`, fillers, native-tx builders, endpoint consts |
| `tronz-contract` | `ContractInstance`, `Interface`, TRC20 bindings (`ITRC20`), `decode_logs`, deploy/call builders |

## Setup

```toml
[dependencies]
tronz = { version = "0.1", features = ["full"] }
tokio = { version = "1", features = ["full"] }
anyhow = "1"
hex = "0.4"
```

Feature flags: `contract` (TRC20/Interface), `signer-mnemonic`, `signer-keystore`;
`full` turns them all on. Dynamic-ABI work also pulls `alloy-json-abi` + `alloy-dyn-abi`.

## Three things that cause most bugs — internalize these first

1. **Read-only vs signing provider.** A bare provider does every `get_*`/`call`
   read. To *send* anything you MUST attach a signer AND the recommended fillers,
   or the tx has no reference block / fee limit and gets rejected:
   ```rust
   let read = ProviderBuilder::new().on_grpc(TRONGRID_NILE).await?;          // reads only
   let send = ProviderBuilder::new()
       .with_recommended_fillers()   // auto TAPOS ref-block + fee_limit + signing (alloy JoinFill analogue)
       .with_signer(signer)
       .maybe_api_key(api_key)       // Option<String>, TronGrid key
       .on_grpc(TRONGRID_NILE).await?;
   ```

2. **Addresses have three forms — convert with `.into()`.**
   - `tronz::Address`: base58check (`T...`). Use everywhere in tronz APIs. `"T...".parse()?`
   - On the wire: 21 bytes with `0x41` prefix.
   - Inside **ABI** (calldata, `DynSolValue::Address`, decoded event fields): **20-byte EVM form**, prefix stripped.
   - `tronz::Address → alloy Address` for ABI args; decoded `alloy Address → tronz::Address` to print `T...`:
     ```rust
     let arg = addr.into();                      // tronz -> alloy (ABI)
     let shown: tronz::Address = evt.from.into(); // alloy -> tronz (display)
     ```

3. **Amounts.** `Trx::from_sun(i64)?` builds; `.as_sun()` / `.as_trx()` read.
   `1 TRX = 1_000_000 sun`. **Token** amounts are raw `U256` with NO implicit
   decimals — divide by `10^decimals` yourself for display.

## Decision trees

**Connecting**
```
need to send a tx?  ── no ──> ProviderBuilder::new().on_grpc(ep)
                    └─ yes ─> + .with_recommended_fillers().with_signer(s)
```

**Calling a contract**
```
ABI known at compile time? ── yes ──> sol! bindings (ITRC20 or your own sol!{})  → typed args/returns
                           └─ no  ──> Interface::new(JsonAbi)                     → DynSolValue
is it a standard TRC20?    ── yes ──> provider.trc20(addr)  (Trc20Ext, typed reads+writes)
                           └─ no  ──> provider.contract(addr, interface) + call / call_raw
```

**Staking**
```
account on Stake 2.0 (current)? ── yes ──> freeze_balance() / unfreeze_balance() / delegate_resource()
                                └─ no  ──> freeze_balance_v1() / unfreeze_balance_v1()   (legacy 1.0)
```

**Sending value**
```
native TRX        → provider.send_trx()
TRC10 asset       → provider.transfer_trc10()
TRC20 token       → provider.trc20(addr).transfer(...)   or   ITRC20::transferCall + call_raw
```

## Where to go next (load the reference for the task)

| Task | Read |
|---|---|
| Connect, read chain/account state, receipts, fillers, endpoints | `references/providers.md` |
| Keys: LocalSigner, mnemonic, keystore, signing | `references/signers.md` |
| Send TRX / TRC10 / TRC20, balances, amount math | `references/transfers.md` |
| Call/deploy contracts, static vs dynamic ABI, estimate energy | `references/contracts.md` |
| Decode logs/events, topic0, event types | `references/events.md` |
| Freeze/delegate/rewards, resources | `references/staking.md` |
| Vote for SRs, create/update accounts, witnesses | `references/governance.md` |
| Common errors → cause → fix; per-crate error types | `references/errors.md` |
| Map a task to a runnable example in the repo | `examples-index.md` |

Every capability has a focused, compiling example in the `tronz-examples` repo.
When in doubt, read the example before writing code.
