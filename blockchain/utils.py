"""
Utilitaires pour la blockchain.

Fonctions :
- Sérialisation JSON déterministe (clés triées, sans espaces)
- Calcul de hash SHA-256
- Formatage de l'affichage terminal
"""

import hashlib
import json
from typing import Any, Dict
from datetime import datetime

from config import JSON_ENCODING


def deterministic_json(obj: Any) -> str:
    """
    Sérialise un objet en JSON déterministe.

    Garantit que deux objets identiques produisent la même chaîne JSON :
    - Clés triées alphabétiquement
    - Pas d'espaces superflus
    - Encodage UTF-8

    Args:
        obj: Objet à sérialiser (dict, list, str, int, float, bool, None)

    Returns:
        str: JSON déterministe
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_sha256(data: str) -> str:
    """
    Calcule le hash SHA-256 d'une chaîne de caractères.

    Args:
        data: Données à hasher

    Returns:
        str: Hash hexadécimal (64 caractères)
    """
    return hashlib.sha256(data.encode(JSON_ENCODING)).hexdigest()


def compute_block_hash(index: int, timestamp: str, data: Dict[str, Any],
                       previous_hash: str, nonce: int) -> str:
    """
    Calcule le hash SHA-256 d'un bloc.

    La sérialisation inclut tous les champs du bloc dans un ordre fixe
    pour garantir la reproductibilité.

    Args:
        index: Index du bloc
        timestamp: Horodatage ISO 8601
        data: Données du bloc (déjà chiffrées)
        previous_hash: Hash du bloc précédent
        nonce: Valeur du Proof of Work

    Returns:
        str: Hash hexadécimal du bloc
    """
    block_data = {
        "index": index,
        "timestamp": timestamp,
        "data": data,
        "previous_hash": previous_hash,
        "nonce": nonce,
    }
    serialized = deterministic_json(block_data)
    return compute_sha256(serialized)


def current_timestamp() -> str:
    """
    Retourne l'horodatage actuel au format ISO 8601.

    Returns:
        str: Timestamp ISO 8601 (ex: 2024-01-15T14:30:45.123456)
    """
    return datetime.now().isoformat()


def format_block_display(block: Dict[str, Any]) -> str:
    """
    Formate un bloc pour l'affichage dans le terminal.

    Args:
        block: Dictionnaire représentant un bloc

    Returns:
        str: Représentation formatée
    """
    lines = [
        f"  Index        : {block.get('index', 'N/A')}",
        f"  Timestamp    : {block.get('timestamp', 'N/A')}",
        f"  Previous Hash: {block.get('previous_hash', 'N/A')[:64]}",
        f"  Hash         : {block.get('hash', 'N/A')[:64]}",
        f"  Nonce        : {block.get('nonce', 'N/A')}",
        f"  Data (enc.)  : {str(block.get('data', 'N/A'))[:80]}...",
    ]
    return "\n".join(lines)


def print_header(title: str) -> None:
    """Affiche un en-tête standardisé."""
    print(f"\n=== {title} ===")


def print_info(message: str) -> None:
    """Affiche un message d'information."""
    print(f"[INFO] {message}")


def print_success(message: str) -> None:
    """Affiche un message de succès."""
    print(f"[SUCCESS] {message}")


def print_warning(message: str) -> None:
    """Affiche un avertissement."""
    print(f"[WARNING] {message}")


def print_error(message: str) -> None:
    """Affiche une erreur."""
    print(f"[ERROR] {message}")