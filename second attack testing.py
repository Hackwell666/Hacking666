#!/usr/bin/env python3
"""
sim_recover.py — Safe detector & recovery for the ransomware simulator.
- Scans the target directory for the simulator metadata file (.ransomware_sim_meta.json)
  and encrypted files (*.encsim).
- Prompts for password and attempts to decrypt matching files according to metadata.
- Runs inside a safe test folder only (same LAB_ROOTS rule as the simulator).
"""

import argparse
import json
import base64
from pathlib import Path
from getpass import getpass
from typing import Dict
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend

# Match the simulator's values
LAB_ROOTS = [Path.home() / "ransomware_lab"]
METADATA_FILENAME = ".ransomware_sim_meta.json"

def derive_key_from_password(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=390000, backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))

def is_path_within_allowed(path: Path) -> bool:
    try:
        path = path.resolve()
    except Exception:
        return False
    for root in LAB_ROOTS:
        try:
            if root.resolve() in path.parents or root.resolve() == path:
                return Truecc
        except Exception:
            continue
    return False

def load_meta(target_dir: Path) -> Dict:
    meta_file = target_dir / METADATA_FILENAME
    if not meta_file.exists():
        print("No metadata file found in target directory.")
        return {}
    with open(meta_file, "r") as fh:
        return json.load(fh)

def recover(target_dir: Path, password: str, dry_run: bool):
    meta = load_meta(target_dir)
    if not meta:
        return
    salt_b64 = meta.get("salt")
    if not salt_b64:
        print("Metadata missing salt — cannot derive key.")
        return
    salt = base64.b64decode(salt_b64)
    key = derive_key_from_password(password, salt)
    fernet = Fernet(key)
    files_map = meta.get("files", {})
    if not files_map:
        print("No files listed in metadata.")
        return

    for rel_path, enc_name in list(files_map.items()):
        enc_path = target_dir / enc_name
        orig_path = target_dir / rel_path
        if not enc_path.exists():
            print(f"[MISSING] Encrypted: {enc_path} (skipping)")
            continue
        print(f"[FOUND] {enc_path} -> {orig_path}")
        if dry_run:
            continue
        try:
            token = enc_path.read_bytes()
            plain = fernet.decrypt(token)
            orig_path.parent.mkdir(parents=True, exist_ok=True)
            orig_path.write_bytes(plain)
            enc_path.unlink()
            print(f"[RECOVERED] {orig_path}")
            del files_map[rel_path]
        except Exception as e:
            print(f"[FAILED] Could not decrypt {enc_path}: {e}")

    # Save updated metadata
    new_payload = {"salt": salt_b64, "files": files_map}
    with open(target_dir / METADATA_FILENAME, "w") as fh:
        json.dump(new_payload, fh, indent=2)
    print("Recovery attempt finished.")

def parse_args():
    p = argparse.ArgumentParser(description="Simulator recovery tool: detect and decrypt .encsim files.")
    p.add_argument("-t", "--target-dir", required=True, help="Target directory (must be inside lab).")
    p.add_argument("--dry-run", action="store_true", help="List actions but do not modify files.")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    target = Path(args.target_dir).resolve()
    if not target.exists() or not target.is_dir():
        print("Target directory must exist and be a directory.")
        raise SystemExit(1)
    if not is_path_within_allowed(target):
        print("Target directory not inside allowed lab roots. Abort.")
        raise SystemExit(1)

    meta = load_meta(target)
    if not meta:
        raise SystemExit(1)

    pwd = getpass("Enter simulator password to attempt recovery (blank to abort): ").strip()
    if not pwd:
        print("No password entered — aborting.")
        raise SystemExit(1)

    recover(target, pwd, args.dry_run)
