"""Configuration centralisée de la blockchain privée."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def get_data_dir() -> Path:
    path = Path(os.getenv("BLOCKCHAIN_DATA_DIR", str(BASE_DIR / "data")))
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_blockchain_file() -> Path:
    return get_data_dir() / "blockchain.json"


def get_encryption_key_file() -> Path:
    return get_data_dir() / "encryption_key.bin"


def get_pow_difficulty() -> int:
    return int(os.getenv("BLOCKCHAIN_POW_DIFFICULTY", "4"))


AES_KEY_SIZE = 16
AES_NONCE_SIZE = 12
JSON_ENCODING = "utf-8"
JSON_INDENT = 2
