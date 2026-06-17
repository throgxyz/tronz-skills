# Staking & resources

TRON has two stake mechanisms. **Stake 2.0** is current (per-resource freeze with
a delegation market and an unlock/withdraw step). **Stake 1.0** is legacy. Use the
one the account is on — mixing them fails.

## ResourceCode
```rust
use tronz::primitives::ResourceCode;   // Bandwidth = 0, Energy = 1, TronPower = 2
```
Freeze for `Energy` to run contracts, `Bandwidth` for transfers; `TronPower` is
voting weight from staking.

## Stake 2.0 (current)

```rust
// freeze TRX to gain a resource
provider.freeze_balance()
    .amount(Trx::from_sun(10_000_000)?)
    .resource(ResourceCode::Energy)
    .send().await?;

// start unfreeze (begins the lock-up countdown)
provider.unfreeze_balance()
    .amount(Trx::from_sun(10_000_000)?)
    .resource(ResourceCode::Energy)
    .send().await?;

// after the lock period, withdraw the now-unfrozen TRX back to balance
provider.withdraw_expire_unfreeze().send().await?;

// delegate / reclaim a resource to/from another address
provider.delegate_resource()
    .to(receiver).amount(Trx::from_sun(5_000_000)?)
    .resource(ResourceCode::Energy)
    .lock_period(3 * 24 * 3600)   // seconds, optional
    .send().await?;

provider.undelegate_resource()
    .receiver(receiver).amount(Trx::from_sun(5_000_000)?)
    .resource(ResourceCode::Energy)
    .send().await?;
```

## Stake 1.0 (legacy)

```rust
provider.freeze_balance_v1()
    .amount(Trx::from_sun(10_000_000)?)
    .resource(ResourceCode::Energy)
    .receiver(addr)              // optional: delegate to another account
    .send().await?;

provider.unfreeze_balance_v1()
    .resource(ResourceCode::Energy)
    .send().await?;
```

## SR rewards

```rust
let pending = provider.get_reward(me).await?;   // Trx, claimable
if pending.as_sun() > 0 {
    provider.claim_rewards().send().await?;     // moves reward into balance
}
```

## Verify resources changed
```rust
let r = provider.get_account_resource(me).await?;
// r.energy_used / r.energy_limit, r.bandwidth_used / r.bandwidth_limit
```
Compare before/after a freeze or delegate to confirm the operation took effect.
