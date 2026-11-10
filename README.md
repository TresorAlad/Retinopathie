# Retinopathie

Dépôt du projet de dépistage de la rétinopathie diabétique (monorepo par dossiers).

## Branches

| Branche | Rôle |
|---------|------|
| `main` | Branche d'intégration : `backend/`, `blockchain/`, `ia/`. |
| `feature/backend` | Travail API FastAPI et intégration blockchain. |
| `feature/react` | Travail interface (équipe React). |
| `blockchain` | Historique (fusionné). |
| `ia` | Service Flask de classification (`POST /predict`, port 8001). |

- **blockchain/** : ancrage chiffré (upload + validation médecin).
- **ia/** : module IA relié au backend via `AI_SERVICE_URL`.

## Démarrer

- Backend (+ db + ia en mock) : [backend/README.md](backend/README.md) (`docker compose up`).
- IA seule : [ia/README.md](ia/README.md).
