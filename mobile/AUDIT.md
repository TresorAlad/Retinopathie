# Audit mobile (Flutter) vs backend

Date de référence : intégration sur `main` du monorepo Retinopathie.

## Aligné

- Route `POST /api/v1/mobile/scan`, en-tête `X-Mobile-Api-Key`, champs `patient_code`, `first_name`, `last_name`, fichier `image` (PNG).
- Réponse : lecture de `patient_message`, `is_eye`, `stage_label`, `refer_to_doctor`, `recommendations`, identifiants optionnels.
- Rejet œil : HTTP 200 avec `is_eye: false`, message patient affiché.
- Timeout client 60 s ; HTTP 503 (IA indisponible) mappé sur « Serveur indisponible ».

## Écarts / limites

| Sujet | App | Backend |
|-------|-----|---------|
| Âge / sexe | Collectés dans le formulaire, envoyés en champs extra | Non persistés ; ignorés par la route |
| Date de naissance | Non envoyée (seul l’âge est saisi) | Champ optionnel `birth_date` (ISO) |
| Code patient | `M-` + 8 caractères, réutilisé en session | Unique en base, max 50 car. côté modèle |
| Clé API | Injectée via `--dart-define=API_KEY` | Secret partagé ; extractible d’un APK release sans obfuscation dédiée |
| Cadrage | Heuristique ML Kit locale (visage / luminosité), pas de validation côté serveur | L’IA valide uniquement « image œil » sur la photo capturée |
| Blockchain | Affichage optionnel via `blockchain_block_index` dans le modèle | Médecin : JWT + liste des blocs |

## Recommandations (hors scope actuel)

1. Ne pas stocker la clé API en dur ; prévoir un canal de distribution sécurisé ou un proxy.
2. Traduire l’âge en `birth_date` approximatif si le produit exige la conformité dossier patient.
3. Tests instrumentés sur appareil réel pour le flux YUV Android et la capture auto.
