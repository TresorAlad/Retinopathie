# Cahier de recette et tests manuels — Dépiste Retino

> **À quoi sert ce document :** Fournir le plan de validation manuelle exhaustif à exécuter sur un smartphone Android physique pour garantir la conformité complète de l'application avec le cahier des charges.  
> **Pour qui :** Les testeurs QA, les développeurs lors des tests d'intégration et les évaluateurs du projet.

---

## Scénarios d'intégration API

Exécuter l'application avec l'URL HTTPS ngrok et la clé fournie en privé.
Vérifier que ni les données patient, ni la photo, ni la clé ne sont écrites
dans les journaux de l'application.

| Scénario | Étapes | Résultat attendu |
|---|---|---|
| Configuration multipart valide | Envoyer une photo PNG avec nom, prénom, âge et sexe ; inspecter l'appel côté serveur. | `POST /api/v1/mobile/scan`, champs `patient_code`, `first_name`, `last_name`, `age`, `sexe`, fichier `image` nommé `photo.png` avec `image/png`; en-tête `X-Mobile-Api-Key` si configuré ; pas de `Content-Type` défini manuellement. |
| Code patient stable pendant la session | Envoyer deux scans en gardant les mêmes nom, prénom, âge et sexe normalisés. | Les deux envois réutilisent le même code `M-` + 8 caractères `A-Z0-9`. |
| Résultat œil reconnu | Envoyer une image d'œil lorsque le service IA est disponible. | Réponse `200`; `patient_message` non vide affiché. Les autres champs de réponse ne modifient pas l'interface. |
| Image non reconnue comme un œil | Envoyer une image rejetée par le service IA. | Le backend répond `200` avec `is_eye: false` et un `patient_message`; le client affiche ce message comme résultat. |
| Authentification invalide | Utiliser une clé incorrecte ou absente sur un serveur qui en exige une. | Réponse hors 2xx traitée comme « Serveur indisponible » ; photo conservée. |
| Service IA indisponible | Arrêter ou rendre inaccessible le service IA, puis envoyer une image. | Backend en `503`; l'application affiche « Serveur indisponible » et conserve la photo. |
| Réponse invalide | Faire renvoyer un JSON invalide, un JSON sans `patient_message`, ou un message vide. | « Serveur indisponible » ; photo conservée. |
| Expiration globale | Laisser la vérification réseau ou l'appel/lecture HTTP dépasser 60 secondes. | Erreur de délai ; photo effacée et reprise imposée. |
| Erreur caméra puis réessai | Simuler un échec d'initialisation caméra puis appuyer sur « Réessayer ». | Le contrôleur est réinitialisé et le processus normal de permission et d'initialisation caméra est relancé ; aucune caméra disponible n'affiche toujours aucun bouton. |
| Échec de capture | Simuler un échec de prise de vue ou de conversion PNG. | La bannière indique « La photo n'a pas pu être prise. Veuillez réessayer. » ; une photo précédente reste inchangée. |
| Animations désactivées | Activer le réglage système qui désactive les animations et afficher le viseur, l'obturateur et un indicateur animé. | Aucun contrôleur d'animation répétée ne tourne ; l'apparence statique habituelle est conservée. |
| Changement d'un champ | Modifier chacun des champs du patient entre deux envois, un champ à la fois. | Un `patient_code` nouveau est généré dès qu'un champ normalisé change. |

## Tableau exhaustif des 33 scénarios de tests manuels

| N° | Scénario testé | Étapes à réaliser | Résultat attendu |
|---|---|---|---|
| **1** | Permission caméra accordée au démarrage | Installer et lancer l'application pour la première fois. Accepter la demande d'autorisation caméra. | Le flux vidéo de la caméra s'affiche immédiatement dans le viseur ; l'obturateur est actif. |
| **2** | Permission caméra refusée | Réinitialiser les autorisations et relancer. Refuser la boîte de dialogue de permission. | La vue d'état s'affiche dans le viseur avec le texte *« L'accès à la caméra est nécessaire… »* et le bouton *« Autoriser la caméra »*. L'obturateur est inactif. |
| **3** | Permission refusée définitivement | Refuser deux fois l'accès ou cocher « Ne plus demander ». | Le bouton d'action devient automatiquement *« Ouvrir les réglages »*. |
| **4** | Retour depuis les réglages système | Cliquer sur *« Ouvrir les réglages »*, activer la caméra dans les paramètres Android, puis revenir sur l'application. | Au retour (`resumed`), l'application détecte automatiquement l'accord et initialise la caméra sans redémarrage. |
| **5** | Caméra frontale par défaut | Démarrer l'application avec les permissions accordées. | Le capteur sélectionné par défaut est la caméra frontale pour faciliter le centrage des deux yeux. |
| **6** | Bascule vers la caméra arrière | Cliquer sur le bouton circulaire de rotation en haut à droite du viseur. | Le flux bascule de façon fluide vers la caméra arrière ; le bouton flash apparaît en haut à gauche. |
| **7** | Bascule vers la caméra avant | Cliquer à nouveau sur le bouton de rotation. | Le flux redevient la caméra avant ; le bouton flash disparaît automatiquement. |
| **8** | Activation du flash (mode torche) | Sur caméra arrière, cliquer sur l'icône éclair en haut à gauche. | La torche physique du téléphone s'allume en continu ; l'icône passe en mode `flash_on`. |
| **9** | Extinction du flash | Cliquer à nouveau sur l'icône éclair. | La torche physique s'éteint ; l'icône redevient `flash_off`. |
| **10** | Prise de vue oculaire | Positionner ses yeux dans l'ovale guidé et appuyer sur le gros bouton obturateur circulaire. | Micro-animation d'échelle au toucher, déclenchement instantané, l'écran défile de façon fluide vers la carte « Cliché instantané ». |
| **11** | Effacement immédiat du fichier temporaire | Vérifier le stockage de l'appareil après la capture. | Aucun fichier photo n'est créé ni conservé dans le dossier DCIM ou les dossiers temporaires du terminal. L'image n'existe qu'en mémoire vive (RAM). |
| **12** | Action « Reprendre » | Sur la carte d'aperçu, cliquer sur le bouton *« Reprendre »*. | La carte d'aperçu disparaît, la mémoire de la photo est libérée (`null`), et l'écran remonte vers le viseur prêt pour une nouvelle prise. |
| **13** | Validation : Nom manquant | Laisser le champ Nom vide et cliquer sur *« Analyser »*. | Bordure rouge de 1.5px autour du champ Nom ; message *« Ce champ est obligatoire »* en dessous ; défilement vers le champ Nom. |
| **14** | Validation : Nom avec espaces uniquement | Saisir uniquement des espaces `"   "` dans le champ Nom et cliquer sur *« Analyser »*. | Erreur déclenchée : la fonction `trim()` détecte l'absence de texte réel. |
| **15** | Validation : Nom > 60 caractères | Saisir un nom de 61 caractères. | Message d'erreur *« 60 caractères maximum »* sous le champ. |
| **16** | Validation : Prénom manquant | Laisser le champ Prénom vide et cliquer sur *« Analyser »*. | Bordure rouge ; message *« Ce champ est obligatoire »* sous le Prénom ; aucun envoi émis. |
| **17** | Validation : Âge manquant | Laisser le champ Âge vide et cliquer sur *« Analyser »*. | Message *« Ce champ est obligatoire »* sous le champ Âge. |
| **18** | Validation : Âge égal à 0 ou négatif | Saisir `0` dans le champ Âge et cliquer sur *« Analyser »*. | Message d'erreur *« Entrez un âge valide (de 1 à 120) »*. |
| **19** | Validation : Âge supérieur à 120 | Saisir `125` dans le champ Âge et tenter d'analyser. | Message d'erreur *« Entrez un âge valide (de 1 à 120) »*. |
| **20** | Validation : Sexe non sélectionné | Conserver la valeur par défaut vide de la liste déroulante et analyser. | Message *« Veuillez sélectionner une option »* sous la liste déroulante. |
| **21** | Effacement de l'erreur à la saisie | Un champ est en erreur rouge. Taper un caractère dans ce champ. | La bordure rouge et le message d'erreur disparaissent instantanément. |
| **22** | Défilement vers le 1er champ invalide | Laisser Nom, Âge et Sexe vides, puis cliquer sur *« Analyser »*. | Les 3 erreurs s'affichent simultanément et l'écran défile précisément vers le champ Nom (le premier). |
| **23** | Envoi en cours et désactivation | Valider tous les champs et cliquer sur *« Analyser »*. | Le bouton Analyser passe à *« Analyse... »* avec roue tournante ; Reprendre devient grisé à 50% d'opacité et insensible aux touches. |
| **24** | Défilement vers la carte de chargement | Dès le clic sur *« Analyser »*. | La carte « Analyse en cours… » apparaît et l'écran défile pour la rendre parfaitement visible. |
| **25** | Réception avec succès (200 OK) | L'API distante renvoie une réponse JSON avec du texte explicatif. | La section « Résultats de l'analyse » apparaît au sommet de la vue avec le texte intégral et l'heure courante (ex: *« Aujourd'hui à 14:32 »*). |
| **26** | Mode avion (« Pas de connexion ») | Activer le mode avion sur le téléphone et cliquer sur *« Analyser »*. | La bannière rouge *« Pas de connexion »* s'affiche immédiatement avec l'icône `wifi_off`. La photo est conservée. |
| **27** | Panne serveur (« Serveur indisponible ») | Désactiver le mode avion mais pointer vers une URL invalide (`https://api.example.invalid`). | La bannière rouge *« Serveur indisponible »* s'affiche avec l'icône `cloud_off`. La photo est conservée. |
| **28** | Dépassement du délai (Timeout 60s) | Simuler un serveur qui ne répond pas pendant 60 secondes. | La bannière *« Le délai d'attente est dépassé. Veuillez reprendre la photo. »* s'affiche ; **la photo est effacée** et l'écran remonte au viseur. |
| **29** | Remplacement d'un ancien résultat | Après un bilan reçu, modifier le nom du patient et reprendre une photo puis renvoyer. | L'ancien résultat est effacé de l'écran dès le nouvel envoi ; le nouveau résultat le remplace à l'arrivée. |
| **30** | Verrouillage strict en orientation portrait | Tourner physiquement le smartphone Android en mode paysage (rotation automatique activée). | L'application reste strictement verrouillée en mode portrait sans aucune rotation d'écran. |
| **31** | Accessibilité de la taille de texte | Régler la taille de police système Android au maximum (ex: 150%). | Le texte reste borné à un facteur maximal de 1.3 dans l'application ; aucun bouton ne déborde et aucune superposition n'a lieu. |
| **32** | Respect de la réduction des animations | Activer « Supprimer les animations » dans les options d'accessibilité Android. | Les animations en boucle (`pulse`, `ping`, `spin`) sont automatiquement figées et ne consomment aucun cycle CPU. |
| **33** | Conformité graphique pixel-perfect | Comparer visuellement l'application sur le téléphone avec la capture `screen.png`. | Alignements, arrondis 32px, marges de 20px, ombres douces et couleurs conformes à la maquette Stitch. |
