# Contracts — static vs dynamic ABI, call, deploy, estimate

TVM contracts are EVM-compatible, so ABI encode/decode is exactly ERC-style and
tronz reuses alloy's machinery. There are two paths; pick by **when the ABI is
known**.

## Static — `sol!` bindings (ABI known at compile time → type-safe)

Use the built-in `ITRC20`, or write your own `sol! { ... }`. You get typed call
structs, typed returns, and `EVENT::SIGNATURE_HASH`.

```rust
use tronz::contract::{ContractExt, Interface, SolCall, trc20::ITRC20};

// encode calldata from a generated *Call struct
let calldata: tronz::primitives::Bytes = ITRC20::transferCall {
    to: to.into(),          // tronz::Address -> alloy Address (20-byte ABI form)
    amount,                  // U256
}.abi_encode().into();

// state-changing call
let instance = provider.contract(contract, Interface::empty());
let pending  = instance.call_raw(calldata).send().await?;
let info     = pending.get_receipt().await?;   // check info.status / info.revert_reason

// read-only estimate (no broadcast)
let energy = instance.call_raw(other_calldata).estimate_energy().await?;  // energy units
```
`Interface::empty()` is fine when you encode calldata yourself with `sol!` types.

## Dynamic — `Interface::new(JsonAbi)` (ABI known at runtime → flexible)

When the ABI comes from a file or block explorer, parse it and call by name.
Returns `Vec<DynSolValue>`.

```rust
use alloy_json_abi::JsonAbi;
use alloy_dyn_abi::DynSolValue;
use tronz::contract::{ContractExt, Interface};

let abi: JsonAbi = serde_json::from_str(abi_json)?;
let instance = provider.contract(contract, Interface::new(abi));

let out = instance.call("name", &[]).await?;
let out = instance.call("balanceOf", &[DynSolValue::Address(addr.into())]).await?;
// inspect interface.abi().functions.keys() / .events.keys()

// extract: match DynSolValue
let name = match out.into_iter().next() { Some(DynSolValue::String(s)) => s, _ => String::new() };
```
`DynSolValue::Address` expects the 20-byte alloy form — convert with `addr.into()`.

### Choosing
- Compile-time ABI, want type safety and event types → **static `sol!`**.
- Runtime ABI, arbitrary/unknown contracts, generic tooling → **dynamic `Interface`**.
Both encode through the same alloy backend; the difference is type-safety vs flexibility.

## Deploy

```rust
use tronz::contract::ContractExt;

let pending = provider.deploy(bytecode)          // impl Into<Bytes>
    .abi(abi_bytes)                               // optional, enables ABI-aware features
    .value(Trx::from_sun(0)?)                     // optional TRX to send to constructor
    .fee_limit(Trx::from_sun(1_000_000_000)?)     // optional cap
    .name("MyContract")                           // optional
    .consume_user_resource_percent(100)           // optional
    .origin_energy_limit(10_000_000)              // optional
    .send().await?;
let info = pending.get_receipt().await?;          // deployed address derived from the tx
```

## Energy / fee estimation
```rust
let energy = instance.call_raw(calldata).estimate_energy().await?;
let price  = provider.chain_parameters().await?.get("getEnergyFee").copied().unwrap_or(420);
let fee_sun = energy * price;   // approximate cost in sun
```
