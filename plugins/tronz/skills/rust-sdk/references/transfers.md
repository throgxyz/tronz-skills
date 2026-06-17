# Transfers — TRX, TRC10, TRC20

## Amounts
```rust
use tronz::Trx;
let a = Trx::from_sun(1_000_000)?;  // 1 TRX (i64 sun in, fallible)
a.as_sun();                          // i64
a.as_trx();                          // human TRX
```
`1 TRX = 1_000_000 sun`. **TRC20 token** amounts are raw `U256` integers with no
implicit decimals — scale by `10^decimals` only for display.

## TRX

```rust
let pending = provider.send_trx().to(to).amount(Trx::from_sun(n)?).send().await?;
let info = pending.get_receipt().await?;
// info.block_number, info.status, info.net_usage, info.net_fee.as_sun()
```
The sender defaults to the attached signer. Override with `.from(addr)` for
multisig/permission scenarios.

## TRC10 (native assets)

TRC10 lives on the `Trc10Api` extension trait — import it to unlock these methods:
```rust
use tronz::providers::ext::Trc10Api as _;
```

Reads:
```rust
provider.get_asset_info(token_id).await?;                 // AssetInfo (token_id is &str, the numeric id)
provider.trc10_balance(addr, token_id).await?;            // i64
provider.get_asset_issue_by_account(addr).await?;         // Vec<AssetInfo>
provider.get_asset_issue_by_name(name).await?;            // AssetInfo
provider.get_asset_issue_list(offset, limit).await?;      // Vec<AssetInfo>
```
Transfer:
```rust
let pending = provider.transfer_trc10()
    .to(to)
    .token_id("1000001")   // numeric asset id as string
    .amount(100)           // i64, raw units
    .memo("hi")            // optional
    .send().await?;
```
Other TRC10 builders: `issue_trc10()`, `participate_trc10()`, `unfreeze_trc10()`,
`update_trc10()`.

## TRC20 — typed (preferred for standard tokens)

```rust
use tronz::contract::Trc20Ext;   // adds .trc20() to the provider
let token = provider.trc20(contract);   // contract: tronz::Address

// reads
token.name().await?;           // String
token.symbol().await?;         // String
token.decimals().await?;       // u8
token.total_supply().await?;   // U256
token.balance_of(holder).await?;            // U256 (raw units)
token.allowance(owner, spender).await?;     // U256

// writes (need signer + fillers) -> PendingTransaction
token.transfer(to, amount).await?.get_receipt().await?;
token.approve(spender, amount).await?;
token.transfer_from(from, to, amount).await?;
```
`amount` here is `U256` raw units. Display:
```rust
let raw = token.balance_of(holder).await?;
let dec = token.decimals().await?;
// raw / 10u128.pow(dec as u32)
```

For non-standard tokens or arbitrary functions, drop to the contract layer —
see `references/contracts.md`.
