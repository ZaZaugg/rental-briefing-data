#!/usr/bin/env python3
"""Decrypt data.enc → stdout using AES-256-GCM + PBKDF2-SHA256."""

import json
import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PASSPHRASE = "KZP2018"
KEY_LEN = 32  # AES-256

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "data.enc")


def decrypt(passphrase: str, payload: dict) -> bytes:
    salt = base64.b64decode(payload["salt"])
    iv = base64.b64decode(payload["iv"])
    ct = base64.b64decode(payload["ct"])
    iters = int(payload["iters"])

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        iterations=iters,
    )
    key = kdf.derive(passphrase.encode())

    aesgcm = AESGCM(key)
    return aesgcm.decrypt(iv, ct, None)


if __name__ == "__main__":
    with open(INPUT_FILE) as f:
        payload = json.load(f)

    plaintext = decrypt(PASSPHRASE, payload)
    print(plaintext.decode())
