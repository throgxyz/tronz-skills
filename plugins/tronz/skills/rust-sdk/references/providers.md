# Providers — connect, configure, read state

## Build a provider

```rust
use tronz::{ProviderBuilder, TronProvider, TRONGRID_MAINNET, TRONGRID_NILE};

// Read-only
let provider = ProviderBuilder::new().on_grpc(TRONGRID_MAINNET).await?;

// Signing-capable
let provider = ProviderBuilder::new()
    .with_recommended_fillers()   // fills ref-block (TAPOS) + fee_limit, then signs
    .with_signer(signer)          // any TronSigner
    .maybe_api_key(api_key)       // Option<String>; TronGrid API key
    .on_grpc(TRONGRID_NILE)
    .await?;
```

`with_recommended_fillers()` is the alloy `JoinFill` analogue. Without it a write
has no reference block / expiration / fee limit and the node rejects it. Reads
never need fillers or a signer.

### Endpoints
| Network | Const | Address |
|---|---|---|
| Mainnet (TLS) | `TRONGRID_MAINNET` | `grpc.trongrid.io:443` |
| Nile testnet | `TRONGRID_NILE` | `grpc.nile.trongrid.io:50051` |

`TRONGRID_MAINNET` is TLS; Nile is plaintext. Both are re-exported from the crate
root. For a custom node, pass its endpoint to `.on_grpc(...)`. Import the
low-level transport from `tronz::transports` only if you need it directly.

## Read methods (on `TronProvider`)

```rust
let block = provider.get_now_block().await?;            // BlockInfo: .number, .timestamp
let acct  = provider.get_account(addr).await?;          // AccountInfo: .balance (Trx)
let res   = provider.get_account_resource(addr).await?; // AccountResource: energy/bandwidth used/limit
let reward = provider.get_reward(addr).await?;          // Trx: claimable SR reward
let params = provider.chain_parameters().await?;        // HashMap<String, i64> e.g. params.get("getEnergyFee")
let srs    = provider.list_witnesses().await?;          // Vec<WitnessInfo>

// By transaction id (TxId == B256)
let signed = provider.get_transaction(tx_id).await?;       // SignedTransaction: .signatures, .raw.{expiration,timestamp}
let info   = provider.get_transaction_info(tx_id).await?;  // TransactionInfo (the receipt)
```

Build a `TxId` from hex:
```rust
use tronz::primitives::B256;
let tx_id = B256::from_slice(&hex::decode(tx_hex.trim_start_matches("0x"))?);
```

### `TransactionInfo` (the receipt)
Fields you'll use: `block_number`, `block_timestamp`, `status`, `contract_result`,
`energy_usage`, `energy_fee` (Trx), `net_usage`, `net_fee` (Trx), `logs`,
`revert_reason` (`Option<String>`).

### `AccountResource`
`energy_used` / `energy_limit`, `bandwidth_used` / `bandwidth_limit`. Compare
before/after a freeze to confirm resources landed.

## Sending: the `PendingTransaction` lifecycle

Every write (`send_trx`, contract calls, staking, TRC10/20 writes) returns a
`PendingTransaction`:
```rust
let pending = provider.send_trx().to(to).amount(amount).send().await?;
let tx_id = pending.tx_id();                    // available immediately
let info  = pending.get_receipt().await?;       // polls until confirmed -> TransactionInfo
```
Grab `tx_id()` right away (for logging / idempotency), then `get_receipt()` to
wait for on-chain confirmation. Always check `info.status` and, for contract
calls, `info.revert_reason` before treating a tx as successful.
