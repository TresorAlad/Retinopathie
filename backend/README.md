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
- Service IA dans `ia/` : si `AI_SERVICE_URL` est défini, appel Rodium AI ; sinon `ai_status` = `pending`.
- Parcours **mobile** (sans app Flutter) : `POST /api/v1/mobile/scan` avec clé `X-Mobile-Api-Key` ; un bloc `mobile_scan` par scan valide.
- Explorateur blockchain (JWT médecin) : `GET /api/v1/blockchain/blocks` et `GET /api/v1/blockchain/blocks/{index}`.

## Démarrage avec Docker (recommandé)

Exécute les commandes depuis le dossier **`Retinopathie/backend`** (pas l'ancien nom `diabetic-retinopathy-backend`).

Créer **`backend/.env`** (obligatoire pour Docker : `FERNET_KEY` et `JWT_SECRET_KEY` ne doivent jamais être versionnés) :

```bash
chmod +x scripts/prepare-env.sh
./scripts/prepare-env.sh
```

Si une clé Fernet a été exposée (ex. alerte GitGuardian), générez-en une nouvelle, mettez à jour `.env`, puis supprimez ou rechiffrez le dossier `storage/` en local (les anciennes images ne seront plus lisibles).

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
| POST | `/api/v1/mobile/scan` (clé mobile) |
| GET | `/api/v1/blockchain/blocks` (médecin) |
| GET | `/api/v1/blockchain/blocks/{index}` (médecin) |

Upload dépistage médecin : `multipart/form-data` avec `patient_id` et fichier `image` (JPEG ou PNG).

### Exemple scan mobile (curl)

```bash
export MOBILE_API_KEY=dev-mobile-api-key-change-me
curl -sS -X POST http://localhost:8000/api/v1/mobile/scan \
  -H "X-Mobile-Api-Key: $MOBILE_API_KEY" \
  -F patient_code=M-DEMO-01 \
  -F first_name=Marie \
  -F last_name=Demo \
  -F birth_date=1990-01-15 \
  -F image=@/chemin/vers/retine.jpg
```

## Intégration équipes externes

| Client | Auth | Endpoints utiles |
|--------|------|------------------|
| Flutter mobile | `X-Mobile-Api-Key` | `POST /api/v1/mobile/scan` |
| Dashboard React | JWT Bearer | patients, screenings, diagnosis, `GET /api/v1/blockchain/blocks` |

Variables : `MOBILE_API_KEY`, `AI_SERVICE_URL`, `RODIUMAI_API_KEY` (service `ia`, voir [ia/.env.example](../ia/.env.example)).

## Variables blockchain

| Variable | Rôle |
|----------|------|
| `BLOCKCHAIN_ENABLED` | `true` par défaut ; `false` pour désactiver l'ancrage |
| `BLOCKCHAIN_DATA_DIR` | Répertoire `blockchain.json` et clé AES |
| `BLOCKCHAIN_POW_DIFFICULTY` | Difficulté PoW (2 recommandé en dev) |
| `MOBILE_API_KEY` | Clé partagée pour `POST /api/v1/mobile/scan` |

## Sécurité

- Ne jamais versionner `.env`, les clés ni le dossier `storage/`.
- Les images ne sont pas stockées sur la blockchain ; identité patient (code, nom, prénom) oui, chiffrée dans les blocs.
- Prévoir Alembic, audit et stockage objet avant la production.

Stades API : `no_dr`, `mild`, `moderate`, `severe`, `proliferative`.
