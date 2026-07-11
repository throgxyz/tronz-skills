# tronz 0.3.x pitfalls

## Provider cannot send

A provider created only with `.on_grpc(...)` is for reads. Sending requires:

```rust
let provider = ProviderBuilder::new()
    .with_recommended_fillers()
    .with_signer(signer)
    .on_grpc(endpoint)
    .await?;
```

Recommended fillers add TAPOS and a default contract fee limit. A signer alone
is insufficient.

## Wrong address representation

- TRON APIs: `tronz::Address`, 21 bytes on the wire, displayed as `T...`.
- Solidity ABI: alloy's 20-byte address.
- Convert only at the ABI boundary with `.into()`.

Never prepend `0x41` inside Solidity calldata.

## Floating-point or old amount APIs

Do not generate `Trx::from_trx` or `Trx::as_trx`; they do not exist in 0.3.x.

```rust
let amount: Trx = "1.5".parse()?;
println!("{amount}");       // 1.500000
println!("{}", amount.as_sun());
```

Parsing truncates beyond 6 fractional digits and rejects negative or
out-of-range values. Use `U256` for token values.

## Misunderstanding `full`

`full` aliases the default features. It does not enable `signer-mnemonic`,
`signer-keystore`, or `signer-aws`; request those explicitly.

## Contract transaction appears successful but reverted

Network inclusion and TVM execution are different. Inspect both:

```rust
let info = pending.get_receipt().await?;
println!("network: {:?}, contract: {:?}", info.status, info.contract_result);
```

Also inspect `revert_reason` and energy usage.

## Ethereum assumptions

- Do not call Ethereum JSON-RPC methods on the TRON gRPC provider.
- Do not assume `eth_getLogs`. Decode logs from transaction receipts or use a
  generated filter's `query_tx` / `query_block`.
- Do not use `alloy::ProviderBuilder`, wallet, or transaction types unless the
  tronz API explicitly accepts them.

## `tron_sol!` stability

Treat generated provider bindings as Alpha. Pin `tronz`, review the changelog,
and prefer built-in `Trc20Instance` / `Trc721Instance` for standard tokens.
