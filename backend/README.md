# Backend - rétinopathie diabétique

API FastAPI pour l'application de dépistage de la rétinopathie diabétique.

## Fonctionnalités

- Authentification médecin (JWT, Argon2).
- Patients : liste et détail.
- Dépistages : JPEG/PNG, chiffrement Fernet, SHA-256, consultation, validation médecin.
- PostgreSQL via SQLAlchemy.
- Blockchain locale : ancrage à l'upload (`registered:<index>`) et à la validation médecin (`review:<index>`).
- Politique stricte : si la blockchain est activée et échoue, l'opération est annulée (503).
- Les lectures GET ne créent pas de bloc.
- Adaptateur IA encore en attente de contrat technique (`ai_status` = `pending`).

## Démarrage avec Docker (recommandé)

Exécute les commandes depuis le dossier **`Retinopathie/backend`** (pas l'ancien nom `diabetic-retinopathy-backend`).

Créer `.env` (optionnel mais recommandé en prod) :

```bash
chmod +x scripts/prepare-env.sh
./scripts/prepare-env.sh
```

Sans `.env`, Docker Compose utilise des secrets de **développement** intégrés (uniquement pour tester en local).

Construire et lancer (le premier build prend quelques minutes, beaucoup moins qu'avec l'ancienne image) :

```bash
docker compose up -d --build
```

- API : http://localhost:8000
- Santé : http://localhost:8000/api/v1/health
- Documentation interactive : http://localhost:8000/docs

`DATABASE_URL` pour Docker est fourni par `docker-compose.yml` (service `db`). Les autres variables viennent de `.env`.

Créer un médecin ou un patient dans le conteneur :

```bash
docker compose exec api python -m scripts.create_doctor
docker compose exec api python -m scripts.create_patient
```

Arrêt :

```bash
docker compose down
```

## Installation locale (sans Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt
cp .env.example .env
```

Configure `.env` (PostgreSQL local, secrets). Puis :

```bash
python -m scripts.create_doctor
python -m scripts.create_patient
uvicorn app.main:app --reload
```

## Tests

À la racine du dépôt (`Retinopathie/`) :

```bash
pip install -r backend/requirements-dev.txt
python -m pytest -q
```

Exécute les tests API (`backend/tests`) et blockchain (`blockchain/tests`).

## Routes principales

| Méthode | Route |
|---------|-------|
| POST | `/api/v1/auth/login` |
| GET | `/api/v1/auth/me` |
| GET | `/api/v1/patients` |
| GET | `/api/v1/patients/{id}` |
| POST | `/api/v1/screenings` |
| GET | `/api/v1/screenings` |
| GET | `/api/v1/screenings/{id}` |
| GET | `/api/v1/screenings/{id}/image` |
| PATCH | `/api/v1/screenings/{id}/diagnosis` |
| GET | `/api/v1/health` |
| GET | `/api/v1/health/blockchain` (médecin) |

Upload dépistage : `multipart/form-data` avec `patient_id` et fichier `image` (JPEG ou PNG).

## Variables blockchain

| Variable | Rôle |
|----------|------|
| `BLOCKCHAIN_ENABLED` | `true` par défaut ; `false` pour désactiver l'ancrage |
| `BLOCKCHAIN_DATA_DIR` | Répertoire `blockchain.json` et clé AES |
| `BLOCKCHAIN_POW_DIFFICULTY` | Difficulté PoW (2 recommandé en dev) |

## Sécurité

- Ne jamais versionner `.env`, les clés ni le dossier `storage/`.
- Les images ne sont pas stockées sur la blockchain ; identité patient (code, nom, prénom) oui, chiffrée dans les blocs.
- Prévoir Alembic, audit et stockage objet avant la production.

Stades API : `no_dr`, `mild`, `moderate`, `severe`, `proliferative`.
