import os
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

def _fernet() -> Fernet:
    key = os.getenv("FERNET_KEY")
    if not key:
        raise RuntimeError("FERNET_KEY absente du fichier .env.")
    return Fernet(key.encode() if isinstance(key, str) else key)

def store_encrypted_image(filename: str, content: bytes) -> Path:
    storage = Path(os.getenv("STORAGE_DIR", "storage")).resolve()
    storage.mkdir(parents=True, exist_ok=True)
    # filename est généré par le backend (UUID), jamais fourni par le client.
    destination = storage / f"{filename}.enc"
    destination.write_bytes(_fernet().encrypt(content))
    return destination

def read_encrypted_image(filename: str) -> bytes:
    storage = Path(os.getenv("STORAGE_DIR", "storage")).resolve()
    path = (storage / f"{filename}.enc").resolve()
    if path.parent != storage:
        raise ValueError("Chemin de fichier invalide.")
    try:
        return _fernet().decrypt(path.read_bytes())
    except InvalidToken as exc:
        raise ValueError("Impossible de déchiffrer l'image.") from exc

def delete_encrypted_image(filename: str) -> None:
    storage = Path(os.getenv("STORAGE_DIR", "storage")).resolve()
    path = storage / f"{filename}.enc"
    if path.exists():
        path.unlink()
