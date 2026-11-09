# Backend - rétinopathie diabétique

API FastAPI pour l'application de dépistage de la rétinopathie diabétique.

## Fonctionnalités

- Authentification médecin (JWT, Argon2).
- Patients : liste et détail.
- Dépistages : JPEG/PNG, chiffrement Fernet, SHA-256, consultation, validation médecin.
- PostgreSQL via SQLAlchemy.
- Adaptateurs IA et blockchain en attente de contrat technique (résultat `pending`, blockchain `not_configured`).

## Démarrage avec Docker (recommandé)

À la racine du dossier `backend` :

```bash
cp .env.example .env
```

Génère les secrets et renseigne `JWT_SECRET_KEY` et `FERNET_KEY` dans `.env` :

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Construire l'image et lancer l'API avec PostgreSQL :

```bash
docker compose build
docker compose up -d
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
