# Retinopathie

Monorepo de dépistage de la rétinopathie diabétique : **backend**, **IA** et **blockchain**.

Le client **mobile (Flutter)** est sous [`mobile/`](mobile/README.md). Le **dashboard médecin (React)** n’est pas encore dans ce dépôt ; l’API backend sert les deux parcours.

## Modules

| Dossier | Rôle |
|---------|------|
| [backend/](backend/README.md) | API FastAPI : auth médecin, patients, dépistages, **parcours mobile** (`POST /api/v1/mobile/scan`), explorateur blockchain JWT |
| [ia/](ia/README.md) | Flask `POST /predict` via **Rodium AI** (vision + agent) |
| [blockchain/](blockchain/README.md) | Chaîne locale chiffrée, types de blocs dont `mobile_scan` |
| [mobile/](mobile/README.md) | Application Flutter **Dépiste Retino** (scan + ML Kit on-device) |

## Flux mobile (côté serveur)

1. Client envoie identité patient + image avec `X-Mobile-Api-Key`.
2. L'IA rejette ou classifie ; l'agent enrichit constantes simulées et recommandations.
3. Si œil valide : création du dépistage + **un** bloc `mobile_scan`.
4. Réponse JSON : `refer_to_doctor`, `patient_message`, `blockchain_block_index`, etc.

## Démarrer

```bash
cd backend
docker compose up -d --build
```

- API : http://localhost:8000/docs
- IA : http://localhost:8001/health

## Tests

À la racine :

```bash
pip install -r backend/requirements-dev.txt
python -m pytest -q
```

## Intégration futures équipes

- **Mobile** : app dans [mobile/depiste_retino](mobile/depiste_retino) ; API `POST /api/v1/mobile/scan`, voir [mobile/depiste_retino/docs/API_INTEGRATION.md](mobile/depiste_retino/docs/API_INTEGRATION.md).
- **React médecin** : JWT + `GET/POST/PATCH` screenings, `GET /api/v1/blockchain/blocks` pour l'historique des blocs.

Architecture détaillée IA : [ia/Arch_Gen_.md](ia/Arch_Gen_.md).
