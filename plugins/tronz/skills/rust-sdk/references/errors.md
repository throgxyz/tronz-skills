# Errors & troubleshooting

## Symptom → cause → fix

| Symptom | Cause | Fix |
|---|---|---|
| Tx rejected / "no reference block" / expired | Missing fillers on a signing provider | Add `.with_recommended_fillers()` (and `.with_signer()`) before `.on_grpc()` |
| ABI arg type mismatch / wrong calldata | Passed `tronz::Address` straight into a `*Call` field or `DynSolValue::Address` | Convert first: `addr.into()` (20-byte alloy form) |
| Decoded `from`/`to` print as hex, not `T...` | Decoded fields are `alloy_primitives::Address` | `let a: tronz::Address = evt.from.into();` |
| Token balance looks 10^n too big | Treated raw `U256` as already-scaled | Divide by `10^decimals` for display only; keep raw for math |
| Staking call fails with state error | Mixed Stake 1.0 (`*_v1`) and 2.0 (no suffix) on the same account | Use the mechanism the account is actually on |
| `decode_logs` returns fewer events than expected | It silently skips logs whose topic0 ≠ the event type | Expected behavior; use the right event type, or `SIGNATURE_HASH` to inspect |
| Connection/TLS error on mainnet | Used a plaintext endpoint, or Nile settings against mainnet | Mainnet is TLS (`grpc.trongrid.io:443` via `TRONGRID_MAINNET`); Nile is plaintext |
| `429` / rate limited | No TronGrid API key | `.maybe_api_key(Some(key))` |
| Method/type not found at compile time | Feature flag off | Enable `contract` / `signer-mnemonic` / `signer-keystore` (or `full`) |
| Edition / syntax errors building tronz | Toolchain below MSRV | Use Rust ≥ 1.85 (2024 edition) |
| `tx_id` type mismatch | `TxId`/`B256` expected, passed a string | `B256::from_slice(&hex::decode(s.trim_start_matches("0x"))?)` |

## Error types
Each crate exposes its own `Error` enum; calls return `Result<_, ThatError>`:
- `tronz_primitives::Error` — address parsing, amount/conversion.
- `tronz_signer::Error` — key/keystore/mnemonic failures (e.g. wrong password).
- `tronz_provider` error — transport/gRPC, request, and node-side failures.
- `tronz_contract` errors — `Trc20Error`, ABI encode/decode, call/deploy.

For app code, `anyhow::Result` over `?` is the common pattern (the examples do
this). Surface `info.revert_reason` and `info.status` from receipts — a tx can be
broadcast successfully yet revert on-chain.

## Confirming success
A successful broadcast is not a successful execution. After `get_receipt()`:
- check `info.status` is the success variant,
- for contract calls check `info.revert_reason.is_none()` and inspect
  `info.contract_result`,
- optionally re-read state (`get_account`, `trc20().balance_of`, resources) to verify.
