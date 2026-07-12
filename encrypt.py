#!/usr/bin/env python3
"""Encrypt data.json → data.enc using AES-256-GCM + PBKDF2-SHA256."""

import json
import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PASSPHRASE = "KZP2018"
ITERS = 250000
KEY_LEN = 32  # AES-256

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "data.json")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "data.enc")


def encrypt(passphrase: str, plaintext: bytes) -> dict:
    salt = os.urandom(16)
    iv = os.urandom(12)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        iterations=ITERS,
    )
    key = kdf.derive(passphrase.encode())

    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(iv, plaintext, None)

    return {
        "salt": base64.b64encode(salt).decode(),
        "iv": base64.b64encode(iv).decode(),
        "ct": base64.b64encode(ct).decode(),
        "iters": ITERS,
    }


if __name__ == "__main__":
    with open(INPUT_FILE, "rb") as f:
        plaintext = f.read()

    payload = encrypt(PASSPHRASE, plaintext)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(payload, f)

    print(f"Encrypted {INPUT_FILE} → {OUTPUT_FILE}")
