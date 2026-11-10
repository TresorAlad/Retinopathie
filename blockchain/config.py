"""
Configuration centralisée de la blockchain privée.

Ce module contient tous les paramètres configurables du projet :
- Difficulté du Proof of Work
- Chemins des fichiers de persistance
- Paramètres de chiffrement
"""

import os
from pathlib import Path

# Répertoire de base du projet
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Créer le répertoire de données s'il n'existe pas
DATA_DIR.mkdir(exist_ok=True)

# === Proof of Work ===
# Nombre de zéros initiaux requis dans le hash (difficulté)
# 4 = facile pour démonstration, augmenter pour plus de sécurité
POW_DIFFICULTY = 4

# === Fichiers de persistance ===
BLOCKCHAIN_FILE = DATA_DIR / "blockchain.json"
ENCRYPTION_KEY_FILE = DATA_DIR / "encryption_key.bin"

# === Chiffrement AES-128-GCM ===
# Taille de la clé en octets (128 bits = 16 octets)
AES_KEY_SIZE = 16

# Taille du nonce en octets (96 bits = 12 octets, recommandé pour GCM)
AES_NONCE_SIZE = 12

# === Sérialisation ===
# Encodage utilisé pour la sérialisation JSON
JSON_ENCODING = "utf-8"

# Indentation pour la lisibilité du fichier JSON (None = compact)
JSON_INDENT = 2