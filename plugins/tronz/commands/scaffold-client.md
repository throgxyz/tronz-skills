---
name: scaffold-client
description: Scaffold a minimal tronz read-only client (connect + query balance) the user can run immediately.
---

# /tronz:scaffold-client

Generate a minimal, compiling tronz program that connects to a network and reads
an address balance. Ask only for what you can't infer; default to mainnet + USDT.

Steps:
1. Confirm network (mainnet vs Nile) and the address to query. Default mainnet.
2. Emit a `Cargo.toml` with `tronz = { version = "0.1", features = ["full"] }`,
   `tokio`, `anyhow`, `hex`.
3. Emit `src/main.rs`:

```rust
use tronz::{ProviderBuilder, TronProvider, TRONGRID_MAINNET, contract::Trc20Ext};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let provider = ProviderBuilder::new().on_grpc(TRONGRID_MAINNET).await?;

    // native TRX
    let addr: tronz::Address = "T...".parse()?;
    let acct = provider.get_account(addr).await?;
    println!("TRX: {}", acct.balance.as_trx());

    // a TRC20 token (USDT mainnet shown)
    let usdt: tronz::Address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t".parse()?;
    let token = provider.trc20(usdt);
    let raw = token.balance_of(addr).await?;
    let dec = token.decimals().await?;
    println!("{}: {} (raw {})", token.symbol().await?, raw, dec);
    Ok(())
}
```

4. Remind: this is read-only (no signer/fillers). To send, add
   `.with_recommended_fillers().with_signer(LocalSigner::from_hex(..)?)` — point
   the user to the `rust-sdk` skill's `references/providers.md` and
   `references/transfers.md`.
