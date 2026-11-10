# Blockchain Privée - Dépistage Rétinopathie Diabétique

Blockchain Python locale, privée et fonctionnelle avec chiffrement AES-128-GCM pour la protection des données de dépistage de la rétinopathie diabétique.

## Fonctionnalités

- **Structure de bloc complète** : index, timestamp, données chiffrées, previous_hash, hash, nonce
- **Proof of Work configurable** : difficulté ajustable (défaut: 4 zéros initiaux)
- **Chiffrement AES-128-GCM** : confidentialité + authenticité des données
- **Gestion sécurisée des clés** : génération, stockage (fichier séparé, permissions 600), chargement
- **Persistance locale JSON** : sauvegarde/chargement automatique, vérification d'intégrité au démarrage
- **Validation complète** : hash de chaque bloc, liaisons inter-blocs, Proof of Work
- **Détection de fraude** : toute modification est détectée
- **Thread-safety** : verrou pour ajouts concurrents
- **API d'intégration** : fonctions prêtes pour FastAPI

## Architecture

```
blockchain/
├── config.py           # Configuration (difficulté, chemins, tailles)
├── encryption.py       # AES-128-GCM (clé, chiffrement, déchiffrement)
├── block.py            # Classe Block (structure, hash, vérification)
├── blockchain.py       # Classe Blockchain (chaîne, PoW, persistance)
├── utils.py            # Utilitaires (JSON déterministe, SHA-256, affichage)
├── main.py             # Démonstration complète
├── requirements.txt    # Dépendances
└── tests/              # Tests unitaires
    ├── test_encryption.py
    ├── test_block.py
    └── test_blockchain.py
```

## Installation

### Prérequis
- Python 3.8+
- Windows 10/11 (PowerShell ou CMD)

### Étapes

```powershell
# 1. Se placer dans le dossier du projet
cd C:\Users\pc\Desktop\Bloc\blockchain

# 2. Créer un environnement virtuel (recommandé)
python -m venv venv
venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

### Lancer la démonstration

```powershell
python main.py
```

### Exécuter les tests

```powershell
# Tous les tests
python -m pytest tests/ -v

# Un module spécifique
python -m pytest tests/test_encryption.py -v
python -m pytest tests/test_block.py -v
python -m pytest tests/test_blockchain.py -v
```

## Sortie attendue (démonstration)

```
=== DÉMONSTRATION BLOCKCHAIN - DÉPISTAGE RÉTINOPATHIE DIABÉTIQUE ===

[INFO] Initialisation de la blockchain...
[SUCCESS] Bloc Genesis créé.

=== Bloc Genesis ===
  Index        : 0
  Timestamp    : 2024-01-15T14:30:45.123456
  Previous Hash: 0000000000000000000000000000000000000000000000000000000000000000
  Hash         : a1b2c3d4e5f6...
  Nonce        : 0
  Data (enc.)  : {'message': 'Bloc Genesis - Initialisation de la blockchain'}...
  Intégrité    : OK
  Proof of Work: OK

=== Clé de chiffrement AES-128 ===
[INFO] Récupération ou génération de la clé AES-128...
[SUCCESS] Clé prête (16 octets = 128 bits)
[INFO] Clé stockée dans data/encryption_key.bin (ne jamais la partager)

=== Création des dépistages (données en clair) ===
[INFO] Dépistage #1: Patient PAT-2024-001 - Rétinopathie diabétique détectée (Stade 2 - Modérée)
[INFO] Dépistage #2: Patient PAT-2024-002 - Aucune rétinopathie détectée (Stade 0 - Aucune)
[INFO] Dépistage #3: Patient PAT-2024-003 - Rétinopathie diabétique détectée (Stade 3 - Sévère)

=== Chiffrement et ajout à la blockchain ===
[INFO] Chiffrement du dépistage #1...
[INFO]   Nonce: a1b2c3d4e5f6...
[INFO]   Tag:   1234567890ab...
[INFO] Ajout du bloc #1 (Proof of Work en cours)...
[SUCCESS] Bloc #1 ajouté (nonce: 12345).
[INFO] Chiffrement du dépistage #2...
...
[SUCCESS] Bloc #2 ajouté (nonce: 67890).
[INFO] Chiffrement du dépistage #3...
...
[SUCCESS] Bloc #3 ajouté (nonce: 54321).

=== Blockchain complète ===
=== Blockchain (4 blocs) ===

=== Bloc #0 ===
  Index        : 0
  Timestamp    : 2024-01-15T14:30:45.123456
  Previous Hash: 0000000000000000000000000000000000000000000000000000000000000000
  Hash         : a1b2c3d4e5f6...
  Nonce        : 0
  Data (enc.)  : {'message': 'Bloc Genesis - Initialisation de la blockchain'}...
  Intégrité    : OK
  Proof of Work: OK

=== Bloc #1 ===
  Index        : 1
  Timestamp    : 2024-01-15T14:30:47.234567
  Previous Hash: a1b2c3d4e5f6...
  Hash         : 0000f8e7d6c5...
  Nonce        : 12345
  Data (enc.)  : {'ciphertext': '...', 'nonce': '...', 'tag': '...'}...
  Intégrité    : OK
  Proof of Work: OK

...

=== Vérification d'intégrité ===
[INFO] Validation complète de la chaîne...
[SUCCESS] Chaîne VALIDE - Tous les blocs sont intacts et liés correctement.

=== Récupération et déchiffrement d'un dépistage ===
[INFO] Récupération du bloc #1 (index 1)...
[INFO] Déchiffrement des données...
[SUCCESS] Déchiffrement réussi !
[INFO] Données du dépistage :
  patient_id: PAT-2024-001
  screening_date: 2024-01-15
  ai_result: Rétinopathie diabétique détectée
  stage: Stade 2 - Modérée
  risk_score: 0.72
  validated_by_doctor: True

=== Simulation de fraude - Modification du bloc #1 ===
[WARNING] Modification directe des données chiffrées dans le bloc #1...
[WARNING] Données du bloc #1 modifiées (ciphertext corrompu).

=== Nouvelle vérification d'intégrité après fraude ===
[INFO] Validation de la chaîne...
[ERROR] Chaîne INVALIDE - Fraude détectée !
[SUCCESS] Le système a correctement détecté la modification frauduleuse.

=== FIN DE LA DÉMONSTRATION ===
[INFO] Blockchain fonctionnelle et sécurisée.
```

## Intégration FastAPI (exemple)

```python
# Dans votre backend FastAPI
from blockchain import Blockchain
from encryption import get_or_create_key, encrypt_data, decrypt_data

# Initialisation (au démarrage de l'app)
blockchain = Blockchain()
aes_key = get_or_create_key()

# Enregistrer un dépistage
def add_screening(screening_data: dict):
    encrypted = encrypt_data(screening_data, aes_key)
    block = blockchain.add_block(encrypted)
    return {"block_index": block.index, "block_hash": block.hash}

# Récupérer un dépistage (avec clé)
def get_screening(index: int):
    block = blockchain.get_block(index)
    if block:
        return decrypt_data(block.data, aes_key)
    return None

# Vérifier l'intégrité
def validate_chain():
    return blockchain.validate_chain()
```

## Sécurité

- **Clé AES** : Stockée dans `data/encryption_key.bin` (permissions 600), **jamais** dans la blockchain
- **Nonce** : 12 octets aléatoires uniques par chiffrement (GCM)
- **Authentification** : Tag GCM vérifié automatiquement au déchiffrement
- **Intégrité** : SHA-256 sur tous les champs du bloc + liaison previous_hash
- **Aucune donnée personnelle** : Seuls des identifiants pseudonymisés sont stockés

## Fichiers de données

```
data/
├── blockchain.json        # Chaîne complète (JSON)
└── encryption_key.bin     # Clé AES-128 (binaire, 600 permissions)
```

⚠️ **Ne jamais commiter** `data/encryption_key.bin` ni `data/blockchain.json` dans Git.

## Licence

Projet universitaire - Usage académique uniquement.