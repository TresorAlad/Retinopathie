import hashlib
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any

logger = logging.getLogger(__name__)

_lock = Lock()
_chain = None


class BlockchainRegistrationError(RuntimeError):
    """Échec d'ancrage sur la blockchain alors que le module est activé."""


@dataclass(frozen=True)
class BlockchainHealth:
    enabled: bool
    configured: bool
    chain_valid: bool | None
    length: int | None
    last_block_index: int | None


def is_blockchain_enabled() -> bool:
    return os.getenv("BLOCKCHAIN_ENABLED", "true").lower() in ("1", "true", "yes")


def _repo_root() -> Path:
    base = Path(__file__).resolve().parents[2]
    if base.name == "backend":
        return base.parent
    return base


def _ensure_blockchain_path() -> None:
    root = str(_repo_root())
    if root not in sys.path:
        sys.path.insert(0, root)


def _data_dir() -> Path:
    raw = os.getenv("BLOCKCHAIN_DATA_DIR")
    path = Path(raw) if raw else _repo_root() / "data"
    path.mkdir(parents=True, exist_ok=True)
    return path


def reset_chain_for_tests() -> None:
    global _chain
    _chain = None


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


def patient_blockchain_fields(
    patient_id: int,
    patient_code: str,
    first_name: str,
    last_name: str,
    birth_date: str | None = None,
) -> dict[str, Any]:
    return {
        "patient_id": patient_id,
        "patient_code": patient_code,
        "first_name": first_name,
        "last_name": last_name,
        "birth_date": birth_date,
    }


def _add_encrypted_payload(payload: dict[str, Any]) -> int:
    _ensure_blockchain_path()
    from blockchain.encryption import encrypt_data, get_or_create_key

    encrypted = encrypt_data(payload, get_or_create_key())
    with _lock:
        block = _get_chain().add_block(encrypted)
    return block.index


def register_patient_record(
    patient_id: int,
    patient_code: str,
    first_name: str,
    last_name: str,
    birth_date: str | None = None,
) -> str:
    if not is_blockchain_enabled():
        return "not_configured"

    try:
        block_index = _add_encrypted_payload(
            {
                "type": "patient_record",
                **patient_blockchain_fields(
                    patient_id, patient_code, first_name, last_name, birth_date
                ),
            }
        )
        return f"patient:{block_index}"
    except Exception as exc:
        logger.exception("Échec ancrage patient patient_id=%s", patient_id)
        raise BlockchainRegistrationError(
            "Impossible d'enregistrer le patient sur la blockchain."
        ) from exc


def register_screening(
    screening_id: int,
    image_sha256: str,
    *,
    patient_id: int,
    patient_code: str,
    first_name: str,
    last_name: str,
    birth_date: str | None = None,
) -> str:
    '''
    Ancre dépistage, hash image et identité patient (chiffré). Lève si activé et échec.
    '''
    if not is_blockchain_enabled():
        return "not_configured"

    try:
        block_index = _add_encrypted_payload(
            {
                "type": "screening_anchor",
                "screening_id": screening_id,
                "image_sha256": image_sha256,
                **patient_blockchain_fields(
                    patient_id, patient_code, first_name, last_name, birth_date
                ),
            }
        )
        return f"registered:{block_index}"
    except Exception as exc:
        logger.exception("Échec ancrage dépistage screening_id=%s", screening_id)
        raise BlockchainRegistrationError("Impossible d'enregistrer le dépistage sur la blockchain.") from exc


def register_diagnosis_review(
    screening_id: int,
    image_sha256: str,
    diagnosis: str,
    reviewed_by_id: int,
    *,
    patient_id: int,
    patient_code: str,
    first_name: str,
    last_name: str,
    birth_date: str | None = None,
) -> str:
    if not is_blockchain_enabled():
        return "not_configured"

    digest = hashlib.sha256(
        f"{screening_id}:{diagnosis}:{reviewed_by_id}".encode()
    ).hexdigest()
    try:
        block_index = _add_encrypted_payload(
            {
                "type": "diagnosis_review",
                "screening_id": screening_id,
                "image_sha256": image_sha256,
                "diagnosis": diagnosis,
                "reviewed_by_id": reviewed_by_id,
                "review_digest": digest,
                **patient_blockchain_fields(
                    patient_id, patient_code, first_name, last_name, birth_date
                ),
            }
        )
        return f"review:{block_index}"
    except Exception as exc:
        logger.exception("Échec ancrage diagnostic screening_id=%s", screening_id)
        raise BlockchainRegistrationError(
            "Impossible d'enregistrer la validation sur la blockchain."
        ) from exc


def merge_blockchain_status(current: str, review_status: str) -> str:
    if current == "not_configured" or review_status == "not_configured":
        return current if review_status == "not_configured" else f"{current};{review_status}"
    return f"{current};{review_status}"


def get_blockchain_health() -> BlockchainHealth:
    if not is_blockchain_enabled():
        return BlockchainHealth(
            enabled=False,
            configured=False,
            chain_valid=None,
            length=None,
            last_block_index=None,
        )

    try:
        _ensure_blockchain_path()
        chain = _get_chain()
        length = chain.get_chain_length()
        last_index = chain.get_latest_block().index if length else None
        return BlockchainHealth(
            enabled=True,
            configured=True,
            chain_valid=chain.validate_chain(),
            length=length,
            last_block_index=last_index,
        )
    except Exception:
        logger.exception("Impossible de lire l'état de la blockchain")
        return BlockchainHealth(
            enabled=True,
            configured=False,
            chain_valid=False,
            length=None,
            last_block_index=None,
        )


def find_patient_record(patient_id: int) -> dict[str, Any] | None:
    _ensure_blockchain_path()
    from blockchain.encryption import decrypt_data, get_or_create_key

    key = get_or_create_key()
    chain = _get_chain()
    for block in reversed(chain.chain):
        if block.index == 0:
            continue
        try:
            data = decrypt_data(block.data, key)
        except Exception:
            continue
        if data.get("type") == "patient_record" and data.get("patient_id") == patient_id:
            return data
    return None


def find_anchor_block(screening_id: int, anchor_type: str = "screening_anchor") -> dict[str, Any] | None:
    '''Utilitaire de test : retrouve et déchiffre un ancrage par screening_id.'''
    _ensure_blockchain_path()
    from blockchain.encryption import decrypt_data, get_or_create_key

    key = get_or_create_key()
    chain = _get_chain()
    for block in reversed(chain.chain):
        if block.index == 0:
            continue
        try:
            data = decrypt_data(block.data, key)
        except Exception:
            continue
        if data.get("type") == anchor_type and data.get("screening_id") == screening_id:
            return data
    return None


def register_mobile_scan(
    *,
    request_id: str,
    screening_id: int,
    image_sha256: str,
    patient_id: int,
    patient_code: str,
    first_name: str,
    last_name: str,
    birth_date: str | None,
    ai_payload: dict[str, Any],
) -> str:
    if not is_blockchain_enabled():
        return "not_configured"

    from datetime import datetime, timezone

    try:
        block_index = _add_encrypted_payload(
            {
                "type": "mobile_scan",
                "request_id": request_id,
                "anchored_at": datetime.now(timezone.utc).isoformat(),
                "screening_id": screening_id,
                "image_sha256": image_sha256,
                **patient_blockchain_fields(
                    patient_id, patient_code, first_name, last_name, birth_date
                ),
                "ia": ai_payload,
            }
        )
        return f"mobile:{block_index}"
    except Exception as exc:
        logger.exception("Échec ancrage mobile_scan screening_id=%s", screening_id)
        raise BlockchainRegistrationError(
            "Impossible d'enregistrer le scan mobile sur la blockchain."
        ) from exc


def list_decrypted_blocks(skip: int = 0, limit: int = 50) -> list[dict[str, Any]]:
    _ensure_blockchain_path()
    from blockchain.encryption import decrypt_data, get_or_create_key

    chain = _get_chain()
    key = get_or_create_key()
    rows: list[dict[str, Any]] = []
    for block in chain.chain:
        if block.index == 0:
            continue
        try:
            data = decrypt_data(block.data, key)
        except Exception:
            data = {"type": "undecryptable"}
        rows.append(
            {
                "index": block.index,
                "hash": block.hash,
                "previous_hash": block.previous_hash,
                "timestamp": block.timestamp,
                "nonce": block.nonce,
                "type": data.get("type"),
                "summary": _block_summary(data),
            }
        )
    return rows[skip : skip + limit]


def get_decrypted_block(index: int) -> dict[str, Any] | None:
    _ensure_blockchain_path()
    from blockchain.encryption import decrypt_data, get_or_create_key

    block = _get_chain().get_block(index)
    if block is None or index == 0:
        return None
    data = decrypt_data(block.data, get_or_create_key())
    return {
        "index": block.index,
        "hash": block.hash,
        "previous_hash": block.previous_hash,
        "timestamp": block.timestamp,
        "nonce": block.nonce,
        "payload": data,
    }


def _block_summary(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "request_id": data.get("request_id"),
        "screening_id": data.get("screening_id"),
        "patient_code": data.get("patient_code"),
        "refer_to_doctor": (data.get("ia") or {}).get("refer_to_doctor"),
    }


def validate_chain_integrity() -> bool:
    if not is_blockchain_enabled():
        return True
    _ensure_blockchain_path()
    return _get_chain().validate_chain()
