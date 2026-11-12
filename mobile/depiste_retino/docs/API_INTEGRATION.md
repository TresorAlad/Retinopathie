# Intégration de l'API mobile — Dépiste Retino

L'application Flutter transmet la photo et les informations du formulaire à
l'API backend de dépistage. L'URL ngrok changeante est fournie au lancement
avec `API_BASE_URL` ; elle n'est pas enregistrée dans le code.

## Contrat

- **Méthode et route :** `POST {API_BASE_URL}/api/v1/mobile/scan`
- **Format :** `multipart/form-data`
- **Délai maximal :** 60 secondes pour la vérification réseau et l'échange HTTP
- **Authentification :** en-tête `X-Mobile-Api-Key`, uniquement si `API_KEY`
  n'est pas vide
- **Réponse :** JSON structuré ; champs principaux utilisés par l'app :
  `patient_message` (obligatoire, non vide), `is_eye`, `stage_label`,
  `refer_to_doctor`, `recommendations`, et optionnellement `screening_id`,
  `blockchain_block_index`.

| Champ multipart | Valeur |
|---|---|
| `patient_code` | Obligatoire ; `M-` suivi de 8 caractères aléatoires `A-Z0-9`, réutilisé pour le même patient pendant la session |
| `first_name` | Prénom saisi, espaces de début et de fin supprimés |
| `last_name` | Nom saisi, espaces de début et de fin supprimés |
| `age` | Âge entier (champ supplémentaire ignoré par le backend) |
| `sexe` | `femme`, `homme` ou `autre` (champ supplémentaire ignoré par le backend) |
| `image` | PNG, nom de fichier `photo.png`, type MIME `image/png` |

`birth_date` n'est pas envoyé : l'application ne connaît que l'âge. Le backend
accepte JPEG ou PNG, mais l'application transmet la photo convertie en PNG.
Les champs multipart supplémentaires `age` et `sexe` sont ignorés par la route
actuelle. Le code patient fait 10 caractères, reste inférieur à la limite de
50 caractères de la colonne backend et celle-ci est unique.

La réponse peut aussi contenir `stage`, `risk_score`, `ai_constants` et des
champs `blockchain_*` non affichés dans l'UI actuelle. Pour une image rejetée
comme n'étant pas un œil, le backend répond tout de même `200` avec
`is_eye: false` et un `patient_message` ; ce message est celui affiché.
Une indisponibilité du service IA donne notamment un statut `503`, traité
comme « Serveur indisponible ».

## Exemple `curl`

La clé ci-dessous est fictive et ne doit pas être utilisée comme secret réel.
Le type multipart et sa frontière sont générés par `curl`.

```bash
curl -X POST "https://<lien-ngrok>/api/v1/mobile/scan" \
  -H "X-Mobile-Api-Key: fake-mobile-key-not-a-secret" \
  -H "Accept: application/json" \
  -H "ngrok-skip-browser-warning: true" \
  -F "patient_code=M-A1B2C3D4" \
  -F "first_name=Camille" \
  -F "last_name=Dupont" \
  -F "age=34" \
  -F "sexe=femme" \
  -F "image=@retine.png;type=image/png;filename=photo.png"
```

Exemple de réponse (les identifiants, valeurs et résultats varient) :

```json
{
  "screening_id": 1,
  "patient_id": 1,
  "is_eye": true,
  "patient_message": "Signes légers.",
  "stage": "mild",
  "risk_score": 0.42,
  "blockchain_block_index": 1,
  "blockchain_status": "mobile:1"
}
```

## Lancement de l'application

Depuis `depiste_retino/`, après `flutter pub get` :

```bash
flutter run --dart-define=API_BASE_URL=https://<lien-ngrok> --dart-define=API_KEY=<clé>
```

Remplacer les deux valeurs par celles transmises en privé. L'URL et la clé ne
doivent pas être ajoutées aux fichiers du projet. Une clé d'API embarquée dans
une application mobile est extractible : `--dart-define` évite de la versionner,
mais ne la protège pas contre l'extraction depuis l'application compilée.

### Limite connue — code patient

Après un redémarrage de l'application, un même patient reçoit un nouveau code,
donc un nouveau dossier côté backend. Une solution définitive demande une
décision produit avec l'équipe backend.

## Checklist d'intégration

- [ ] Le tunnel ngrok du coéquipier est actif et son URL HTTPS est fournie.
- [ ] La clé du serveur est transmise en privé et injectée uniquement par
  `--dart-define=API_KEY=...`.
- [ ] L'API répond sur `POST /api/v1/mobile/scan`.
- [ ] Un scan valide avec une image d'œil produit un `patient_message` non vide.
- [ ] Une image qui n'est pas un œil donne une réponse `200` avec
  `is_eye: false` et un message utilisateur.
- [ ] Un service IA indisponible (`503`) est affiché comme « Serveur
  indisponible ».
- [ ] Vérifier qu'aucun nom, aucune photo, aucune clé et aucun corps de requête
  ne sont écrits dans les journaux côté application.

## Gestion des erreurs côté application

| Situation | Erreur interne | Comportement |
|---|---|---|
| Terminal sans connexion | `ScreeningError.noConnection` | Photo conservée |
| Statut HTTP hors 2xx, JSON invalide ou `patient_message` absent/vide | `ScreeningError.serverUnavailable` | Photo conservée |
| Serveur inaccessible ou erreur réseau | `ScreeningError.serverUnavailable` (ou `noConnection` si le réseau est coupé) | Photo conservée |
| Échange dépassant 60 secondes | `ScreeningError.timeout` | Photo effacée, nouvelle prise demandée |

La blockchain et le stockage des images restent gérés par le backend ; aucune
clé ou logique blockchain n'est intégrée à l'application mobile.
