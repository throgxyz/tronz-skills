# tronz 0.3.x API map

Use this file to choose an API and then inspect the linked runnable example or
local crate source for the exact signature.

| Task | API | Documentation | Runnable example |
| --- | --- | --- | --- |
| Connect to gRPC | `ProviderBuilder::on_grpc` | [Provider builder](https://throgxyz.github.io/docs/providers/provider-builder) | [`connect_custom`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/queries/examples/connect_custom.rs) |
| Query block/account | `get_now_block`, `get_account` | [Reading chain state](https://throgxyz.github.io/docs/providers/queries) | [`query`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/queries/examples/query.rs) |
| Parse/format TRX | `FromStr<Trx>`, `parse_trx`, `format_trx` | [TRX and sun](https://throgxyz.github.io/docs/primitives/trx-and-sun) | [`amount_math`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/queries/examples/amount_math.rs) |
| Send TRX | `send_trx` | [Transferring TRX](https://throgxyz.github.io/docs/transactions/transfer-trx) | [`transfer_trx`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/transfers/examples/transfer_trx.rs) |
| TRC10 | traits in `providers::ext` | [TRC10 examples](https://throgxyz.github.io/docs/examples/trc10/README) | [`trc10_transfer`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/trc10/examples/trc10_transfer.rs) |
| TRC20 | `Trc20Ext::trc20` | [TRC20 tokens](https://throgxyz.github.io/docs/contracts/trc20) | [`trc20`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/trc20/examples/trc20.rs) |
| TRC721 | `Trc721Ext::trc721` | [TRC721 tokens](https://throgxyz.github.io/docs/contracts/trc721) | [`trc721_query`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/trc721/examples/trc721_query.rs) |
| Typed custom contract | `tron_sol!` | [Solidity bindings](https://throgxyz.github.io/docs/contracts/tron-sol) | [`tron_sol_bindings`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/sol-macro/examples/tron_sol_bindings.rs) |
| Runtime JSON ABI | `Interface`, `ContractExt` | [Contracts](https://throgxyz.github.io/docs/contracts/introduction) | [`contract_dynamic_abi`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/contracts/examples/contract_dynamic_abi.rs) |
| Deploy contract | `DeployBuilder` | [Contracts](https://throgxyz.github.io/docs/contracts/introduction) | [`contract_deploy`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/contracts/examples/contract_deploy.rs) |
| Estimate energy | `estimate_energy` | [Fillers](https://throgxyz.github.io/docs/providers/fillers) | [`contract_estimate_energy`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/contracts/examples/contract_estimate_energy.rs) |
| Decode logs | `decode_log`, `decode_logs`, generated filters | [Solidity bindings](https://throgxyz.github.io/docs/contracts/tron-sol) | [`decode_log`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/contracts/examples/decode_log.rs) |
| Stake/delegate | Stake 2.0 builders | [Staking](https://throgxyz.github.io/docs/transactions/staking) | [`stake`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/staking/examples/stake.rs) |
| Local signer | `LocalSigner`, `TronSigner` | [Local signer](https://throgxyz.github.io/docs/signers/local-signer) | [`signer_local`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/signers/examples/signer_local.rs) |
| Mnemonic/keystore/AWS | optional signer features | [Signer examples](https://throgxyz.github.io/docs/examples/signers/README) | [`signer_mnemonic`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/signers/examples/signer_mnemonic.rs) |
| Account/multisig | account builders | [Account examples](https://throgxyz.github.io/docs/examples/accounts/README) | [`account_permissions`](https://github.com/throgxyz/examples/blob/64958117b73f0ccfeafd884afd4f6e4666bc32e6/examples/accounts/examples/account_permissions.rs) |

Endpoint constants are `TRONGRID_MAINNET` and `TRONGRID_NILE`. Import extension
traits with `as _` when their name is not otherwise needed.
