# Retinopathie

Dépôt du projet de dépistage de la rétinopathie diabétique (monorepo par dossiers).

## Branches

| Branche | Rôle |
|---------|------|
| `main` | Branche d'intégration : contient le dossier `backend/` (et plus tard le frontend). |
| `feature/backend` | Travail API FastAPI et intégration blockchain. |
| `feature/react` | Travail interface (équipe React). |
| `blockchain` | Historique du module blockchain (fusionné dans `feature/backend`). |

Le dossier `blockchain/` contient la chaîne locale (PoW + chiffrement AES) branchée via `backend/app/services/blockchain_service.py`.

## Démarrer le backend

Voir [backend/README.md](backend/README.md).
