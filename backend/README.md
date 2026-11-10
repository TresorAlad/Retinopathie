# Backend - rétinopathie diabétique

API FastAPI pour l'application de dépistage de la rétinopathie diabétique.

## Fonctionnalités

- Authentification médecin (JWT, Argon2).
- Patients : liste et détail.
- Dépistages : JPEG/PNG, chiffrement Fernet, SHA-256, consultation, validation médecin.
- PostgreSQL via SQLAlchemy.
- Adaptateurs IA et blockchain en attente de contrat technique (résultat `pending`, blockchain `not_configured`).

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

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

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

Upload dépistage : `multipart/form-data` avec `patient_id` et fichier `image` (JPEG ou PNG).

## Sécurité

- Ne jamais versionner `.env`, les clés ni le dossier `storage/`.
- Les images ne sont pas stockées en base ni sur la blockchain.
- Prévoir Alembic, audit et stockage objet avant la production.

Stades API : `no_dr`, `mild`, `moderate`, `severe`, `proliferative`.
