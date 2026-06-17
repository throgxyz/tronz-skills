# Signers — keys, mnemonics, keystores

All signers implement the `TronSigner` trait: `.address() -> Address` and
`async sign_hash(B256) -> RecoverableSignature`. Attach one with
`.with_signer(signer)` on the provider builder.

## LocalSigner (in-memory secp256k1)

```rust
use tronz::{LocalSigner, TronSigner};

let signer = LocalSigner::from_hex(&key_hex)?;   // 64 hex chars, no 0x prefix
let me = signer.address();                        // tronz::Address (base58 "T...")
let hex_form = me.to_hex();                        // 0x41-prefixed hex form

// Sign an arbitrary 32-byte hash (real txs hash the protobuf raw tx to B256)
use tronz::primitives::B256;
let sig = signer.sign_hash(B256::repeat_byte(0xab)).await?; // RecoverableSignature
let bytes = sig.to_bytes();                        // r[32] + s[32] + v[1] = 65 bytes
let (r, s, v) = (sig.r(), sig.s(), sig.v());
```
Signing is RFC-6979 deterministic: same key + same hash → same signature.

## Mnemonic (feature `signer-mnemonic`)

BIP-39 phrase + BIP-44 derivation. TRON coin type is **195**; default path
`m/44'/195'/0'/0/{index}`.

```rust
use tronz::{MnemonicBuilder, TronSigner, coins_bip39::English};

let signer = MnemonicBuilder::<English>::default()
    .phrase(phrase)
    .index(0)?
    .build()?;

// optional BIP-39 passphrase
let signer = MnemonicBuilder::<English>::default()
    .phrase(phrase).password("pass").index(0)?.build()?;

// generate a fresh wallet
let (signer, phrase) = MnemonicBuilder::<English>::default()
    .word_count(24)
    .build_random()?;

// efficient multi-account: derive the parent once, then cheap children
let parent = MnemonicBuilder::<English>::default().phrase(phrase).build_parent_key()?;
let acct_3 = parent.child(3)?.signer()?;
```

## Keystore (feature `signer-keystore`)

Web3 Secret Storage V3 JSON, compatible with TronLink / go-ethereum / gotron-sdk.
The address is stored in base58check form.

```rust
use tronz::{LocalSigner, KeystoreFile};

let path = signer.encrypt_keystore(dir, password)?;            // -> PathBuf
let signer = LocalSigner::decrypt_keystore(&path, password)?;  // wrong password -> clear Err

// inspect the JSON if needed
let ks: KeystoreFile = serde_json::from_str(&std::fs::read_to_string(&path)?)?;
// ks.version, ks.id, ks.address, ks.crypto.{kdf, cipher}, ks.crypto.kdfparams.n
```

## Notes
- `LocalSigner`'s `Debug` hides the private key.
- Never print real private keys / phrases; the examples that do are testnet-only.
- The signer only signs hashes — the provider's fillers handle building and
  hashing the raw transaction, so you rarely call `sign_hash` directly.
