# Dépiste Retino — application Flutter

## Lancer l'application connectée au backend

Depuis le dossier `depiste_retino/` :

```bash
flutter pub get
flutter run --dart-define=API_BASE_URL=https://<lien-ngrok> --dart-define=API_KEY=<clé>
```

Remplacer les valeurs entre chevrons par l'URL HTTPS ngrok active et la clé
transmise en privé. La clé peut être omise uniquement si le backend autorise
explicitement l'accès sans clé. Aucune valeur réelle ne doit être inscrite dans
le dépôt.

L'API cible `POST /api/v1/mobile/scan` et attend du `multipart/form-data`.
Voir [la documentation d'intégration](docs/API_INTEGRATION.md) pour le contrat,
l'exemple `curl` et la checklist de validation.

**Sécurité :** une clé d'API embarquée dans une application mobile est
extractible. `--dart-define` évite de versionner la clé, mais ne la rend pas
secrète dans l'application compilée.
