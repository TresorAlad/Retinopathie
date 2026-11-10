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

## 3. Points d'attention produit essentiels

L'équipe projet doit garder à l'esprit les spécificités suivantes :
1. **Caractère statique des mentions de sécurité :**  
   Les mentions *« Confidentiel »*, *« IA Santé v2.4 »*, *« Résultat enregistré en toute sécurité. Données médicales chiffrées de bout en bout sur votre appareil »* et l'icône verte `verified` sont issues de la maquette et affichées de manière statique. L'application mobile n'effectue **aucun chiffrement asymétrique local** (la sécurité repose sur le canal HTTPS) et n'évalue pas médicalement la gravité du diagnostic.
2. **Texte médical direct :**  
   L'application affiche mot pour mot le contenu renvoyé par l'API sans chercher à l'interpréter, à le résumer ou à lui attribuer une couleur de gravité.
