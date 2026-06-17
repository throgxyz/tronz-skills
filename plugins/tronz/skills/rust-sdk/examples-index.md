# Examples index

Every capability has a focused, compiling example in the separate
[`tronz-examples`](https://github.com/throgxyz/tronz-examples) repo, laid out as
`examples/<category>/examples/<name>.rs`. Map the task to a file and read it
before guessing an API. Run with `cargo run -p examples-<category> --example <name>`
(e.g. `cargo run -p examples-queries --example query`); most read-only ones need
no key, writes need `TRON_PRIVATE_KEY` (use Nile testnet).

| Task | Example file |
|---|---|
| Load a LocalSigner, sign a hash | `signer_local` |
| BIP-39 mnemonic / HD derivation | `signer_mnemonic` |
| Generate a fresh wallet | `signer_generate` |
| Encrypt/decrypt a keystore | `signer_keystore` |
| Send TRX, wait for receipt | `transfer_trx` |
| TRC20 read + transfer (typed) | `trc20` |
| Decode TRC20 Transfer events | `trc20_decode_transfer_event` |
| Read back a full receipt | `decode_receipt` |
| Arbitrary contract write (raw calldata) | `contract_send` |
| Dynamic ABI (runtime JSON ABI) | `contract_dynamic_abi` |
| Estimate energy / fee | `contract_estimate_energy` |
| Deploy a contract | `contract_deploy` |
| Handle a contract revert | `contract_revert` |
| Stake 1.0 freeze/unfreeze | `stake_v1` |
| Unfreeze | `unfreeze` |
| Withdraw expired unfreeze | `withdraw_unfreeze` |
| Claim SR rewards | `claim_rewards` |
| Delegate / undelegate resource | `undelegate` (+ delegate path) |
| Vote / list SRs | `governance_list` |
| Create an account | `account_create` |
| Update account name | `account_update` |
| TRC10 query / balance / by-name | `trc10_query`, `trc10_balance`, `trc10_by_name` |
| Amount (Trx/sun) math | `amount_math` |
| Read-only multi-query | `query` |

If a file name here drifts from the repo, `ls examples/*/examples/` and match by
topic — the names are descriptive.
