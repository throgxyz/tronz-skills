use tronz::{ProviderBuilder, TRONGRID_MAINNET, TronProvider};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let provider = ProviderBuilder::new().on_grpc(TRONGRID_MAINNET).await?;

    let address: tronz::Address = std::env::var("TRON_ADDRESS")?.parse()?;
    let account = provider.get_account(address).await?;

    println!("address: {address}");
    println!("balance: {} TRX", account.balance);
    Ok(())
}
