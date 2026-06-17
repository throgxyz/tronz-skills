# Events — decoding logs

TRC20/TVM events are EVM-compatible: topic0 is `keccak256` of the event
signature, same as ERC-20. Decode with the static `sol!` event types.

## Decode from a receipt

```rust
use tronz::contract::{SolEvent, decode_logs, trc20::ITRC20};

let info = provider.get_transaction_info(tx_id).await?;   // TransactionInfo, has .logs

// topic0 for Transfer(address,address,uint256)
let topic0 = ITRC20::Transfer::SIGNATURE_HASH;

// decode_logs::<E> skips logs whose topic0 != E, and yields Result<E,_> for matches
let transfers: Vec<ITRC20::Transfer> =
    decode_logs::<ITRC20::Transfer>(&info.logs).collect::<Result<_, _>>()?;

for t in &transfers {
    let from: tronz::Address = t.from.into();   // alloy Address (20-byte) -> tronz for display
    let to:   tronz::Address = t.to.into();
    let value = t.value;                         // U256
}
```

Key points:
- `decode_logs::<E>` is a filter+decode in one: unrelated logs are silently
  skipped, matching logs come back as `Result<E, _>`. So
  `.collect::<Result<Vec<_>, _>>()` gives only matching, decoded events.
- Decoded indexed `address` fields are `alloy_primitives::Address` (20 bytes).
  Convert to `tronz::Address` with `.into()` to print/compare in base58.
- `EVENT::SIGNATURE_HASH` gives the topic0 if you want to pre-filter or match
  against an explorer.

## Custom events

Define them with `sol!` and decode the same way:
```rust
use tronz::contract::SolEvent;
tronz::contract::sol! {
    event Swap(address indexed sender, uint256 amount0In, uint256 amount1Out, address indexed to);
}
let swaps: Vec<Swap> = decode_logs::<Swap>(&info.logs).collect::<Result<_, _>>()?;
```
(If `sol!` isn't re-exported under `tronz::contract`, import it from
`alloy_sol_types::sol` — both generate identical `SolEvent` impls.)

## Dynamic event decoding
If you only have a runtime `JsonAbi`, decode against
`Interface::new(abi).abi().events` using alloy's `DynSolEvent` rather than a typed
`sol!` struct. Prefer the static path whenever the event is known.
