# Spécifications fonctionnelles — Dépiste Retino

> **À quoi sert ce document :** Décrire l'ensemble des fonctionnalités, du parcours utilisateur et des règles fonctionnelles dans un langage clair et compréhensible par tous (développeurs, testeurs, équipes médicales et parties prenantes).  
> **Pour qui :** Toute personne intervenant sur le produit ou évaluant sa conformité.

---

## 1. Présentation du produit

**Dépiste Retino** est une application mobile de dépistage oculaire conçue pour apporter une expérience rassurante, fluide et bienveillante. Elle permet à un utilisateur de renseigner son identité, de cadrer simultanément ses deux yeux dans un viseur guidé, puis de transmettre ces informations vers une API d'analyse spécialisée. L'application restitue ensuite le bilan explicatif global renvoyé par le serveur.

---

## 2. Parcours utilisateur détaillé

Le parcours se déroule intégralement sur un **écran unique défilant** :

```
[1. Informations patient] -> [2. Prise de vue oculaire] -> [3. Aperçu & Validation] -> [4. Analyse & Bilan]
```

1. **Étape 1 : Renseignement des informations patient**
   - L'utilisateur saisit son Nom, son Prénom et son Âge, puis sélectionne son Sexe dans une liste déroulante.
   - Ces 4 informations sont obligatoires pour calibrer l'analyse médicale.
2. **Étape 2 : Cadrage et prise de vue**
   - L'utilisateur positionne son visage face à l'objectif de son smartphone à environ 30 cm de distance, dans un endroit bien éclairé.
   - Le viseur affiche en direct le flux vidéo avec un masque sombre et un contour ovale pointillé matérialisant l'emplacement idéal des deux yeux et du nez.
   - L'utilisateur peut au besoin basculer entre la caméra avant et arrière ou activer la torche lumineuse sur la caméra arrière.
   - Il appuie sur l'obturateur circulaire tactile pour capturer le cliché.
3. **Étape 3 : Aperçu instantané**
   - L'écran fait défiler la vue vers la carte « Cliché instantané » qui affiche la photo prise.
   - Deux choix s'offrent à l'utilisateur :
     - **Reprendre :** La photo est immédiatement effacée et l'écran remonte vers le viseur pour reprendre un cliché.
     - **Analyser :** L'application vérifie la complétude des 4 champs, puis envoie la photo et les informations vers l'API.
4. **Étape 4 : Analyse en cours**
   - L'état de l'écran passe en mode chargement (« Analyse en cours… ») rappelant les deux axes d'analyse (clarté sclérale bilatérale et réseau micro-vasculaire).
   - Les boutons d'action sont désactivés pour empêcher tout double envoi.
5. **Étape 5 : Restitution du résultat**
   - Dès réception de la réponse du serveur, la section des résultats apparaît automatiquement avec l'heure exacte de réception.
   - Le diagnostic global est affiché sous forme d'un paragraphe textuel clair.
   - Une mention de sécurité rappelle le caractère chiffré et sécurisé de la transmission.
   - En bas d'écran, l'avertissement médical rappelle que ce dépistage ne remplace pas une consultation ophtalmologique.

---

## 3. Règles de validation des champs

La validation est déclenchée lors du clic sur le bouton **« Analyser »** :

| Champ | Obligatoire | Règles de validation | Message d'erreur affiché |
|---|---|---|---|
| **Nom** | Oui | Chaîne non vide après suppression des espaces ; longueur maximale 60 caractères. | *« Ce champ est obligatoire »* ou *« 60 caractères maximum »* |
| **Prénom** | Oui | Chaîne non vide après suppression des espaces ; longueur maximale 60 caractères. | *« Ce champ est obligatoire »* ou *« 60 caractères maximum »* |
| **Âge** | Oui | Nombre entier positif strictement compris entre 1 et 120 inclus. | *« Ce champ est obligatoire »* ou *« Entrez un âge valide (de 1 à 120) »* |
| **Sexe** | Oui | Une valeur doit être explicitement choisie parmi « Femme », « Homme », « Autre / Non précisé ». | *« Veuillez sélectionner une option »* |
| **Photo** | Oui | La photo doit avoir été prise (le bouton Analyser n'apparaît que si une photo existe). | N/A |

### Comportement en cas d'erreur de saisie :
- Si un ou plusieurs champs sont invalides, tous les champs en anomalie affichent leur bordure en rouge avec le message d'erreur correspondant sous le contrôle.
- Aucune requête n'est émise vers le serveur.
- L'écran défile automatiquement pour afficher le **premier champ invalide** au sommet de l'écran.
- Dès que l'utilisateur commence à corriger un champ, le message d'erreur de ce champ disparaît immédiatement.

---

## 4. États de l'écran et gestion des erreurs

L'application gère 4 états principaux :

### 4.1. État initial (Formulaire + Viseur)
- Les champs sont accessibles en saisie.
- Le flux caméra s'affiche en direct. L'obturateur est disponible.
- Si l'accès à la caméra est refusé par l'utilisateur, un message clair s'affiche dans le viseur avec un bouton « Autoriser la caméra » (ou « Ouvrir les réglages »).

### 4.2. État photo prête (Aperçu)
- La photo capturée apparaît dans un cadre arrondi 16/10.
- Les boutons « Reprendre » et « Analyser » sont actifs.

### 4.3. État analyse en cours
- Le bouton « Analyser » affiche une icône animée avec le libellé « Analyse... ».
- La carte « Analyse en cours… » s'affiche. Les touches sont ignorées.
- Le délai d'attente maximal est borné à 60 secondes.

### 4.4. État résultat ou erreur
- **En cas de succès :** Affichage de la carte « Bilan global unifié » avec le texte explicatif de l'API et l'horodatage.
- **En cas de perte réseau :** Bannière rouge *« Pas de connexion »*. La photo est conservée pour permettre de retenter l'analyse dès le rétablissement de la connexion.
- **En cas de panne serveur ou réponse invalide :** Bannière rouge *« Serveur indisponible »*. La photo est conservée.
- **En cas de délai de 60 secondes dépassé :** Bannière rouge *« Le délai d'attente est dépassé. Veuillez reprendre la photo. »*. La photo est automatiquement effacée et l'écran remonte au viseur pour imposer une nouvelle prise de vue fraîche.

---

## 5. Ce que l'application ne fait volontairement PAS

Afin de garantir une ergonomie simple, une étanchéité absolue des données et le respect du cahier des charges :
1. **Aucun stockage local :** Ni les noms, ni les photos, ni les résultats ne sont enregistrés sur le téléphone après la fermeture.
2. **Aucune importation depuis la galerie :** La prise de vue doit impérativement être faite en direct dans le viseur.
3. **Aucune gestion de compte :** Pas de login, pas de mot de passe, pas de profil utilisateur.
4. **Aucune blockchain côté mobile :** Toute interaction Web3 ou décentralisée relève exclusivement de la responsabilité de l'API distante.
5. **Aucun score chiffré généré localement :** L'application ne calcule aucun diagnostic par elle-même ; elle restitue fidèlement le texte de l'API.
6. **Aucune annulation d'envoi :** Dès que l'analyse est lancée, elle s'exécute jusqu'à son terme (succès, erreur ou expiration à 60s).
