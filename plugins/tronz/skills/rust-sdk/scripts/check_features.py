#!/usr/bin/env python3
"""Check a Cargo.toml for the tronz features a task needs.

Usage:
    python check_features.py [path/to/Cargo.toml] [--need contract,signer-mnemonic]

Exits non-zero and prints what's missing. Best-effort text scan (no TOML lib
required); for tasks involving contracts/keystores/mnemonics it nudges you to
enable the right flags or just use `features = ["full"]`.
"""
import sys, re, pathlib

KNOWN = {"contract", "signer-mnemonic", "signer-keystore", "full"}

def main():
    args = sys.argv[1:]
    need = set()
    path = "Cargo.toml"
    i = 0
    while i < len(args):
        if args[i] == "--need" and i + 1 < len(args):
            need |= {x.strip() for x in args[i + 1].split(",") if x.strip()}
            i += 2
        else:
            path = args[i]; i += 1

    p = pathlib.Path(path)
    if not p.exists():
        print(f"! {path} not found"); sys.exit(2)
    text = p.read_text(encoding="utf-8", errors="replace")

    m = re.search(r'tronz\s*=\s*\{[^}]*\}', text) or re.search(r'^tronz\s*=.*$', text, re.M)
    if not m:
        print("! tronz dependency not found in", path); sys.exit(2)
    dep = m.group(0)

    feats = set(re.findall(r'"([a-z0-9\-]+)"', dep)) & KNOWN
    has_full = "full" in feats
    print(f"tronz features detected: {sorted(feats) or '[]'}")

    missing = set()
    if not has_full:
        for n in need:
            if n not in feats:
                missing.add(n)

    if missing:
        print(f"! missing features for this task: {sorted(missing)}")
        print('  fix: add them, or simplest -> features = ["full"]')
        sys.exit(1)
    print("ok: features satisfy the requested task" if need else "ok")

if __name__ == "__main__":
    main()
