# Governance & account management

## Vote for super representatives
Votes use TRON Power (gained by staking). Voting replaces your previous vote set.
```rust
// single SR
provider.vote_witness().vote(sr_addr, 1_000).send().await?;

// multiple at once
provider.vote_witness()
    .votes([(sr_a, 600i64), (sr_b, 400)])
    .send().await?;
```

## Witness / SR info
`get_brokerage`, `get_reward_info`, and `update_witness` live on the `WitnessApi`
extension trait — import it first (`list_witnesses` is on `TronProvider`):
```rust
use tronz::providers::ext::WitnessApi as _;

provider.list_witnesses().await?;                          // Vec<WitnessInfo>
provider.get_brokerage(sr_addr).await?;                    // u64, % the SR keeps
provider.get_reward_info(addr).await?;                     // u64
provider.update_witness().url("https://my-sr").send().await?; // if you operate an SR; .url() required
```

## Accounts
```rust
// activate a new on-chain account (costs a small fee/bandwidth)
provider.create_account()
    .account_address(new_addr)
    .memo("activation")     // optional
    .send().await?;

// set the account name (one-time on most networks)
provider.update_account_name()
    .name("dennis")
    .send().await?;
```

All of these return a `PendingTransaction`; call `.get_receipt().await?` and check
`info.status` to confirm. The owner defaults to the signer; override with
`.from(addr)` where the builder exposes it.
