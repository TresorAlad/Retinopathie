import os
import sys
from pathlib import Path
from threading import Lock

_lock = Lock()
_chain = None


def _ensure_blockchain_path() -> None:
    root = str(_repo_root())
    if root not in sys.path:
        sys.path.insert(0, root)


def _blockchain_enabled() -> bool:
    return os.getenv("BLOCKCHAIN_ENABLED", "true").lower() in ("1", "true", "yes")


def _data_dir() -> Path:
    raw = os.getenv("BLOCKCHAIN_DATA_DIR")
    path = Path(raw) if raw else _repo_root() / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _repo_root() -> Path:
    base = Path(__file__).resolve().parents[2]
    if base.name == "backend":
        return base.parent
    return base


def _get_chain():
    global _chain
    if _chain is None:
        _ensure_blockchain_path()
        data_dir = _data_dir()
        os.environ.setdefault("BLOCKCHAIN_DATA_DIR", str(data_dir))
        from blockchain import Blockchain

        filepath = data_dir / "blockchain.json"
        _chain = Blockchain(filepath=filepath)
    return _chain


def register_screening(screening_id: int, image_sha256: str) -> str:
    '''
    Enregistre sur la blockchain uniquement l'identifiant du dépistage et le hash image.
    Aucune donnée patient ni image n'est stockée dans les blocs.
    '''
    if not _blockchain_enabled():
        return "not_configured"

    try:
        _ensure_blockchain_path()
        from blockchain.encryption import encrypt_data, get_or_create_key

        payload = {
            "type": "screening_anchor",
            "screening_id": screening_id,
            "image_sha256": image_sha256,
        }
        encrypted = encrypt_data(payload, get_or_create_key())
        with _lock:
            block = _get_chain().add_block(encrypted)
        return f"registered:{block.index}"
    except Exception:
        return "error"
