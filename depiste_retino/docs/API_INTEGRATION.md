# Intégration de l'API d'analyse — Dépiste Retino

> **À quoi sert ce document :** Documenter le contrat d'interface HTTP JSON, fournir des exemples concrets d'appels `curl`, récapituler le tableau de correspondance des erreurs et détailler la procédure pas à pas à suivre dès que la documentation officielle de l'API sera disponible.  
> **Pour qui :** Les développeurs de l'équipe mobile et les ingénieurs backend.

---

## 1. Contrat d'interface provisoire

L'API d'analyse existant déjà côté serveur mais n'ayant pas encore communiqué ses spécifications définitives, l'application est configurée avec une interface préparée et découplée.

### 1.1. Point de terminaison (Endpoint)
- **Méthode :** `POST`
- **URL :** `{baseUrl}{analyzePath}` (par défaut `https://api.example.invalid/analyze`)
- **Délai maximal (Timeout) :** 60 secondes
- **Protocole :** HTTPS obligatoire (HTTP possible en développement local avec ajustement du manifest Android)

### 1.2. En-têtes HTTP (Headers)
```http
Content-Type: application/json; charset=utf-8
Accept: application/json
Authorization: Bearer <API_KEY> (ajouté uniquement si API_KEY n'est pas vide)
```

### 1.3. Format du corps de la requête JSON
```json
{
  "nom": "Dupont",
  "prenom": "Camille",
  "age": 34,
  "sexe": "femme",
  "photo": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

#### Précisions sur les champs envoyés :
- `nom` *(string)* : Nom de famille du patient, sans espaces résiduels de début ou de fin.
- `prenom` *(string)* : Prénom du patient, sans espaces résiduels de début ou de fin.
- `age` *(integer)* : Âge numérique valide entre 1 et 120 (envoyé sous forme d'entier JSON, non de chaîne).
- `sexe` *(string)* : Valeur normalisée parmi `"femme"`, `"homme"` ou `"autre"`.
- `photo` *(string)* : Octets de la photo convertie au format PNG, encodés en Base64 standard sans en-tête data URI (pas de `data:image/png;base64,`).

### 1.4. Format de la réponse attendue du serveur
Le serveur doit renvoyer un statut HTTP 200 OK avec un corps JSON contenant au minimum le champ textuel de résultat :

```json
{
  "resultat": "L'analyse simultanée de vos deux yeux confirme une excellente homogénéité globale. La clarté sclérale, la coloration conjonctivale ainsi que les reflets micro-vasculaires se situent dans les normes physiologiques idéales, sans signe d'ictère, d'anémie ou de fatigue excessive détecté."
}
```

L'application lit et affiche intégralement le contenu de la clé `resultat` (ou le nom configuré dans `ApiConfig.responseTextKey`), en préservant les sauts de ligne.

---

## 2. Exemple d'appel en ligne de commande (`curl`)

Pour tester manuellement la réponse de votre serveur d'analyse depuis votre poste Linux :

```bash
curl -X POST https://api.votre-serveur-sante.fr/analyze \
  -H "Content-Type: application/json; charset=utf-8" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer votre_cle_secrete_provisoire" \
  -d '{
    "nom": "Dupont",
    "prenom": "Camille",
    "age": 34,
    "sexe": "femme",
    "photo": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
  }'
```

---

## 3. Checklist « Quand la documentation de l'API arrive »

Dès réception de la documentation officielle fournie par l'équipe backend, suivez cette liste de vérification point par point :

- [ ] **1. Vérifier l'URL de base et l'endpoint :**
  - Ouvrir `lib/core/config/api_config.dart`.
  - Mettre à jour `defaultValue` de `baseUrl` ou utiliser l'argument de compilation `--dart-define=API_BASE_URL=https://vrai-serveur.fr`.
  - Ajuster `analyzePath` si le point de terminaison est différent de `/analyze` (ex: `/api/v1/screening`).
- [ ] **2. Vérifier la méthode d'authentification :**
  - Dans `lib/core/config/api_config.dart`, ajuster `authHeaderName` (ex: `X-API-KEY` ou `Authorization`) et `authHeaderPrefix` (ex: `Bearer ` ou chaîne vide `""`).
- [ ] **3. Vérifier les noms des clés JSON envoyées :**
  - Ouvrir `lib/features/screening/data/models/screening_request.dart`.
  - Si le serveur attend par exemple `first_name` au lieu de `prenom`, adapter la méthode `toJson()`.
- [ ] **4. Vérifier le nom de la clé de réponse :**
  - Ouvrir `lib/core/config/api_config.dart`.
  - Si le texte se trouve dans une clé comme `"diagnostic"` ou `"summary"` au lieu de `"resultat"`, mettre à jour `responseTextKey`.
- [ ] **5. Vérifier la gestion des codes d'erreurs :**
  - Ouvrir `lib/features/screening/data/screening_api_service.dart`.
  - Vérifier si des codes d'erreur HTTP spécifiques (ex: 422 pour image floue) nécessitent un traitement particulier.

---

## 4. Correspondance des erreurs et bannières

| Cas rencontré | Erreur interne | Affichage dans l'application | Comportement sur la photo |
|---|---|---|---|
| Téléphone en mode avion ou sans réseau | `ScreeningError.noConnection` | Bannière *« Pas de connexion »* | Photo conservée (l'utilisateur peut réessayer) |
| Serveur inaccessible, échec DNS, timeout réseau | `ScreeningError.serverUnavailable` | Bannière *« Serveur indisponible »* | Photo conservée |
| Statut HTTP 4xx ou 5xx renvoyé par l'API | `ScreeningError.serverUnavailable` | Bannière *« Serveur indisponible »* | Photo conservée |
| Corps de réponse non JSON ou clé texte vide | `ScreeningError.serverUnavailable` | Bannière *« Serveur indisponible »* | Photo conservée |
| Requête non terminée après 60 secondes | `ScreeningError.timeout` | Bannière *« Le délai d'attente est dépassé. Veuillez reprendre la photo. »* | **Photo effacée** (l'utilisateur est redirigé vers le viseur) |

---

## 5. Rappel sur la blockchain et le stockage externe

Conformément au cahier des charges :
- **L'application mobile n'intègre aucun SDK blockchain, aucun portefeuille, ni aucun contrat intelligent.**
- Si les bilans de dépistage doivent être ancrés sur un registre décentralisé ou signés cryptographiquement, cette opération est **intégralement réalisée côté serveur par l'API**, en toute transparence pour le client mobile.
