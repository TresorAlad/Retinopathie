# Application mobile Flutter

Le client de dépistage **Dépiste Retino** vit dans [`depiste_retino/`](depiste_retino/). Il appelle le backend de ce monorepo via `POST /api/v1/mobile/scan`.

## Prérequis

- Flutter SDK (voir `depiste_retino/pubspec.yaml`)
- Android : `minSdk 23`, appareil ou émulateur avec caméra pour le cadrage ML Kit
- Backend et service IA démarrés (`backend/docker compose up`)

## Configuration au lancement

```bash
cd depiste_retino
flutter pub get
flutter run \
  --dart-define=API_BASE_URL=http://10.0.2.2:8000 \
  --dart-define=API_KEY=<MOBILE_API_KEY>
```

Sur un téléphone physique, remplacer `API_BASE_URL` par l’adresse LAN ou HTTPS (ngrok) du backend.

## Documentation

| Fichier | Contenu |
|---------|---------|
| [depiste_retino/README.md](depiste_retino/README.md) | Structure du projet Flutter |
| [depiste_retino/docs/API_INTEGRATION.md](depiste_retino/docs/API_INTEGRATION.md) | Contrat multipart + réponse JSON |
| [depiste_retino/docs/TESTS_MANUELS.md](depiste_retino/docs/TESTS_MANUELS.md) | Scénarios de test manuel |
| [AUDIT.md](AUDIT.md) | Écarts connus entre l’app et le backend |

## Import depuis `appliMobile`

Le dossier a été importé depuis la branche `origin/appliMobile` (sous-arbre `depiste_retino/` uniquement, sans la maquette React à la racine de cette branche).
