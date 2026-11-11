# Journal officiel des décisions d'arbitrage — Dépiste Retino

> **À quoi sert ce document :** Consigner l'historique exhaustif des décisions d'arbitrage prises par le client et l'équipe de rédaction, afin d'expliquer chaque divergence maîtrisée entre la maquette initiale et le cahier des charges exécutable.  
> **Pour qui :** L'équipe produit, la maîtrise d'ouvrage et les évaluateurs du projet.

---

## 1. Décisions issues des exigences client (Annexe A)

| N° | Sujet d'arbitrage | Décision retenue | Justification du client |
|---|---|---|---|
| **C1** | Nom de l'application | **Dépiste Retino** | Remplacement officiel de la dénomination commerciale fictive « ClarEye ». |
| **C2** | Périmètre technique | **Code Flutter pur** pour Android et iOS | Projet scolaire centré sur la prise de vue oculaire et la transmission vers l'API. |
| **C3** | Thème et orientation | **Clair uniquement**, **Portrait verrouillé** | Cohérence clinique et simplicité ergonomique sur téléphone mobile. |
| **C4** | Contrôle de qualité de la photo | **Aucun contrôle local** | L'application ne réalise aucune détection en temps réel ; l'évaluation est confiée à l'API. |
| **C5** | Galerie photo | **Supprimée** (aucun bouton de sélection) | La prise de vue oculaire doit être réalisée en direct dans le viseur sous éclairage naturel. |
| **C6** | Persistance de la photo | **Suppression immédiate du fichier** | La photo est convertie en PNG en mémoire (RAM) et n'est jamais conservée sur le stockage du téléphone. |
| **C7** | Nature du résultat d'analyse | **Un seul bloc de texte brut** | Aucun score chiffré, aucun pourcentage, aucune pastille : seul le texte explicatif renvoyé par l'API est affiché. |
| **C8** | Délai maximal d'expiration | **60 secondes** | Si aucune réponse n'est obtenue après 1 minute, la photo est effacée et l'utilisateur doit reprendre la pose. |
| **C9** | Blockchain | **Gérée par l'API** | L'application mobile ne contient aucun portefeuille, aucun smart-contract ni clé privée. |
| **C10** | Comptes et profils | **Aucun compte** | Pas de système d'inscription, pas de mot de passe, pas de persistance inter-sessions. |
| **C11** | Éléments retirés de la maquette | **Bouton « Consulter un professionnel » et bouton « info »** | Éléments non retenus pour la version scolaire. |
| **C12** | Avertissement médical | **Texte conservé tel quel** | Mention médico-légale obligatoire présente en bas de page sans bouton d'action. |

---

## 2. Décisions de rédaction technique (Annexe B)

| N° | Décision prise | Raison technique / ergonomique | Décideur |
|---|---|---|---|
| **R1** | Logo image supprimé de l'en-tête | Remplacé par le libellé textuel « Dépiste Retino » seul (pas d'icône d'application personnalisée). | Rédaction |
| **R2** | Badge « Position stable détectée » supprimé | Annonçait une détection temps réel non conforme au refus de tout contrôle de qualité local. | Rédaction |
| **R3** | Textes « Confidentiel », « IA Santé v2.4 », « Données médicales chiffrées… » et icône `verified` conservés | Règle C de la maquette ; intégrés sous forme statique. | Rédaction |
| **R4** | Bloc d'avertissement médical conservé sans bouton | Répond à l'obligation de réassurance légale sans créer de navigation superflue. | Rédaction |
| **R5** | Caméra frontale sélectionnée par défaut | Permet au patient de s'auto-cadrer immédiatement dans le viseur à double repère. | Rédaction |
| **R6** | Bouton flash limité au mode torche sur caméra arrière | Les caméras avant des smartphones ne disposent généralement pas d'un flash torche physique. | Rédaction |
| **R7** | Résolution `veryHigh` (1080p) | Équilibre parfait entre netteté sclérale et poids du fichier PNG envoyé en Base64. | Rédaction |
| **R8** | Traitement PNG et Base64 dans des isolates | Évite tout gel de l'interface ou saccade d'animation durant la compression de l'image. | Rédaction |
| **R9** | Distinction « Pas de connexion » / « Serveur indisponible » | Permet à l'utilisateur de comprendre immédiatement si le problème provient de son réseau ou du serveur. | Rédaction |
| **R10** | Validation : Nom/Prénom max 60, Âge entre 1 et 120 | Bornes sémantiques et physiologiques strictes issues des attributs de la maquette HTML. | Rédaction |
| **R11** | Gestion d'état avec `Provider` + `ChangeNotifier` | Architecture éprouvée, lisible et parfaitement accessible pour une équipe de développement. | Rédaction |
| **R12** | Polices Google Fonts et icônes Material Symbols | Restitution fidèle à 100% de la maquette Stitch sans obliger à livrer des polices binaires volumineuses. | Rédaction |
| **R13** | Défilement automatique compensé de 64px | Évite que l'élément focalisé ne soit masqué par l'en-tête fixe supérieur. | Rédaction |
| **R14** | Verrouillage de la taille de police système (1.0 à 1.3) | Empêche le débordement des boutons de 56px tout en respectant l'accessibilité malvoyante. | Rédaction |

---

## 3. Intégration au backend mobile

| N° | Décision retenue | Raison technique |
|---|---|---|
| **API1** | Envoi en `multipart/form-data` sur `/api/v1/mobile/scan` | La route backend attend les champs de formulaire et un fichier `image`, pas un JSON avec une photo Base64. |
| **API2** | Envoyer la photo PNG comme `image` / `photo.png` (`image/png`) | Conserver la conversion PNG existante tout en respectant le contrat du champ fichier. |
| **API3** | Créer un `patient_code` de forme `M-` + 8 caractères aléatoires `A-Z0-9` et le réutiliser pour les envois de la session ayant les mêmes champs normalisés | Le backend identifie un patient par code unique ; la réutilisation évite un nouveau dossier à chaque scan du même patient dans la session. |
| **API4** | Envoyer l'âge et le sexe comme champs multipart supplémentaires, ne pas envoyer `birth_date` | L'âge et le sexe sont connus du client et la route actuelle ignore les champs supplémentaires ; l'application ne connaît pas la date de naissance. |
| **API5** | Lire uniquement `patient_message` ; ne pas interpréter `is_eye`, le stade ou la blockchain | L'interface conserve son résultat textuel existant et laisse l'analyse métier au serveur. |
| **API6** | Injecter l'URL et la clé avec `--dart-define`; utiliser `X-Mobile-Api-Key` sans préfixe | L'URL ngrok change et les secrets ne doivent pas être enregistrés dans le dépôt. Une clé intégrée à une application mobile reste toutefois extractible. |
| **API7** | Ne pas définir manuellement `Content-Type` et ajouter `ngrok-skip-browser-warning: true` | `MultipartRequest` doit générer le type multipart avec sa frontière ; l'en-tête complémentaire permet les appels au tunnel ngrok. |
| **API8** | Appliquer 60 secondes à la chaîne réseau complète | La vérification de connectivité, l'envoi multipart et la lecture du corps forment une seule opération bornée. |
| **API9** | Garder le code patient uniquement en mémoire pour la durée de la session | Le code est renouvelé au redémarrage ; aucune donnée d'identité supplémentaire n'est persistée sur l'appareil. |
| **APP1** | Corriger l'action du bouton d'analyse pour appeler `analyze()` et garder le bouton désactivé pendant l'envoi | Le contrôleur expose `analyze()` et `isSending`; le nom d'action doit correspondre à l'API réelle du contrôleur. |
| **APP2** | Supprimer le test widget de compteur obsolète | Le test ne correspond plus à l'application et le cahier des charges interdit les tests automatisés. |
| **APP3** | Permettre de relancer l'initialisation caméra après une erreur, sans bouton si aucune caméra n'existe | Distinguer une panne réessayable de l'absence de matériel. |
| **APP4** | Représenter un échec réel de prise de vue/conversion par `CaptureFailedException` et `ScreeningError.captureFailed` | L'utilisateur voit l'échec sans perdre une éventuelle photo précédente. |
| **APP5** | Arrêter les animations répétées lorsque les animations sont désactivées et les relancer à leur réactivation | Respecter le réglage d'accessibilité sans modifier l'apparence statique. |

---

## 4. Points d'attention produit essentiels

L'équipe projet doit garder à l'esprit les spécificités suivantes :
1. **Caractère statique des mentions de sécurité :**  
   Les mentions *« Confidentiel »*, *« IA Santé v2.4 »*, *« Résultat enregistré en toute sécurité. Données médicales chiffrées de bout en bout sur votre appareil »* et l'icône verte `verified` sont issues de la maquette et affichées de manière statique. L'application mobile n'effectue **aucun chiffrement asymétrique local** (la sécurité repose sur le canal HTTPS) et n'évalue pas médicalement la gravité du diagnostic.
2. **Texte médical direct :**  
   L'application affiche mot pour mot le contenu renvoyé par l'API sans chercher à l'interpréter, à le résumer ou à lui attribuer une couleur de gravité.

### Limite connue — code patient

Après un redémarrage de l'application, le même patient reçoit un nouveau code
et peut donc créer un nouveau dossier côté backend. Une solution définitive
demande une décision produit avec l'équipe backend.
