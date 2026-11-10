"""
Module de chiffrement AES-128-GCM pour la blockchain.

Fonctionnalités :
- Génération sécurisée de clé AES-128 (128 bits)
- Chiffrement avec nonce aléatoire de 12 octets
- Authentification intégrée (GCM)
- Gestion sécurisée des erreurs
"""

import os
import json
import base64
import binascii
from typing import Dict, Any, Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

from config import (
    AES_KEY_SIZE,
    AES_NONCE_SIZE,
    ENCRYPTION_KEY_FILE,
    JSON_ENCODING,
)


def generate_aes_key() -> bytes:
    """
    Génère une clé AES-128 cryptographiquement sécurisée.

    Returns:
        bytes: Clé de 16 octets (128 bits)
    """
    return os.urandom(AES_KEY_SIZE)


def save_key(key: bytes, filepath: str = None) -> None:
    """
    Sauvegarde la clé de chiffrement dans un fichier binaire.

    Args:
        key: Clé AES à sauvegarder
        filepath: Chemin du fichier (par défaut: config.ENCRYPTION_KEY_FILE)

    Raises:
        IOError: Si l'écriture échoue
    """
    path = filepath or ENCRYPTION_KEY_FILE
    try:
        with open(path, "wb") as f:
            f.write(key)
        # Restreindre les permissions (lecture/écriture propriétaire uniquement)
        os.chmod(path, 0o600)
    except OSError as e:
        raise IOError(f"Impossible de sauvegarder la clé: {e}")


def load_key(filepath: str = None) -> bytes:
    """
    Charge la clé de chiffrement depuis un fichier.

    Args:
        filepath: Chemin du fichier (par défaut: config.ENCRYPTION_KEY_FILE)

    Returns:
        bytes: Clé AES de 16 octets

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        ValueError: Si la clé a une taille incorrecte
        IOError: Si la lecture échoue
    """
    path = filepath or ENCRYPTION_KEY_FILE

    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier de clé introuvable: {path}")

    try:
        with open(path, "rb") as f:
            key = f.read()
    except OSError as e:
        raise IOError(f"Impossible de lire la clé: {e}")

    if len(key) != AES_KEY_SIZE:
        raise ValueError(
            f"Taille de clé invalide: {len(key)} octets (attendu: {AES_KEY_SIZE})"
        )

    return key


def get_or_create_key(filepath: str = None) -> bytes:
    """
    Récupère la clé existante ou en génère une nouvelle si le fichier n'existe pas.

    Ne remplace JAMAIS une clé existante.

    Args:
        filepath: Chemin du fichier (par défaut: config.ENCRYPTION_KEY_FILE)

    Returns:
        bytes: Clé AES de 16 octets
    """
    path = filepath or ENCRYPTION_KEY_FILE

    if os.path.exists(path):
        return load_key(path)

    # Générer et sauvegarder une nouvelle clé
    key = generate_aes_key()
    save_key(key, path)
    return key


def encrypt_data(data: Dict[str, Any], key: bytes) -> Dict[str, str]:
    """
    Chiffre un dictionnaire de données avec AES-128-GCM.

    Le nonce est généré aléatoirement pour chaque chiffrement.
    Les données sont sérialisées en JSON avant chiffrement.

    Args:
        data: Dictionnaire à chiffrer
        key: Clé AES de 16 octets

    Returns:
        dict: Dictionnaire contenant 'ciphertext', 'nonce', 'tag' (tous en base64)

    Raises:
        ValueError: Si la clé a une taille incorrecte
        Exception: Si le chiffrement échoue
    """
    if len(key) != AES_KEY_SIZE:
        raise ValueError(f"Clé invalide: {len(key)} octets (attendu: {AES_KEY_SIZE})")

    # Sérialisation JSON déterministe (clés triées, pas d'espaces)
    plaintext = json.dumps(data, sort_keys=True, separators=(",", ":")).encode(JSON_ENCODING)

    # Générer un nonce aléatoire de 12 octets
    nonce = os.urandom(AES_NONCE_SIZE)

    # Chiffrement AES-GCM
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    # AESGCM retourne ciphertext + tag concaténés (tag = 16 derniers octets)
    tag = ciphertext[-16:]
    ciphertext_only = ciphertext[:-16]

    return {
        "ciphertext": base64.b64encode(ciphertext_only).decode(JSON_ENCODING),
        "nonce": base64.b64encode(nonce).decode(JSON_ENCODING),
        "tag": base64.b64encode(tag).decode(JSON_ENCODING),
    }


def decrypt_data(encrypted_data: Dict[str, str], key: bytes) -> Dict[str, Any]:
    """
    Déchiffre des données chiffrées avec AES-128-GCM.

    Vérifie automatiquement l'authenticité (tag GCM).
    Lève une exception si les données ont été modifiées.

    Args:
        encrypted_data: Dict avec 'ciphertext', 'nonce', 'tag' (base64)
        key: Clé AES de 16 octets

    Returns:
        dict: Données déchiffrées (dictionnaire original)

    Raises:
        ValueError: Si la clé a une taille incorrecte ou données invalides
        InvalidTag: Si l'authentification échoue (données modifiées/clé incorrecte)
        Exception: Si le déchiffrement échoue
    """
    if len(key) != AES_KEY_SIZE:
        raise ValueError(f"Clé invalide: {len(key)} octets (attendu: {AES_KEY_SIZE})")

    try:
        # Décoder depuis base64
        ciphertext = base64.b64decode(encrypted_data["ciphertext"])
        nonce = base64.b64decode(encrypted_data["nonce"])
        tag = base64.b64decode(encrypted_data["tag"])
    except (KeyError, ValueError, binascii.Error) as e:
        # Toute erreur de décodage = données potentiellement modifiées
        raise InvalidTag("Échec de l'authentification: données modifiées ou clé incorrecte")

    # Reconstituer ciphertext + tag pour AESGCM
    ciphertext_with_tag = ciphertext + tag

    # Déchiffrement avec vérification d'authenticité
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext_with_tag, None)
    except InvalidTag:
        raise InvalidTag("Échec de l'authentification: données modifiées ou clé incorrecte")

    # Désérialisation JSON
    try:
        return json.loads(plaintext.decode(JSON_ENCODING))
    except json.JSONDecodeError as e:
        raise ValueError(f"Données déchiffrées invalides (JSON): {e}")