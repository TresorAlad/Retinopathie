# Guide de contribution et qualité de code — Dépiste Retino

> **À quoi sert ce document :** Définir les normes de collaboration Git, le style de code Dart, les processus de revue de code et la liste des interdictions strictes.  
> **Pour qui :** Tout développeur contribuant au code source de Dépiste Retino.

---

## 1. Organisation Git

### 1.1. Branches
- `main` : Branche principale de production (toujours stable et analysable sans avertissement).
- `feature/<nom-fonctionnalite>` : Développement d'une nouvelle capacité (ex: `feature/ajustement-viseur`).
- `fix/<nom-anomalie>` : Correction d'un bogue (ex: `fix/timeout-reprise`).

### 1.2. Messages de commit
Rédigés en **français** à l'impératif présent, concis et explicites :
- `Ajouter la gestion du flash torche sur caméra arrière`
- `Corriger le défilement vers le premier champ invalide`
- `Ajuster la couleur de la bannière d'erreur`

---

## 2. Règles de qualité et vérifications obligatoires

Avant chaque commit ou proposition de pull request, vous devez impérativement exécuter sur votre machine :

```bash
# Formatage automatique selon les normes officielles de Dart
dart format .

# Analyse statique rigoureuse (doit retourner 0 problème)
flutter analyze
```

---

## 3. Conventions de style et de nommage

- **Langues du projet :**
  - Textes d'interface visibles : **Français exclusivement** (centralisés dans `AppStrings`).
  - Identifiants de code (classes, variables, méthodes, fichiers) : **Anglais technique** standard.
  - Commentaires de code et documentation : **Français**.
- **Constructeurs `const` :** Doivent être utilisés systématiquement partout où le widget ou la valeur est immutable.
- **Gestion de la mémoire :** Tout contrôleur (`TextEditingController`, `FocusNode`, `AnimationController`, `StreamSubscription`, `CameraController`, `http.Client`) doit être obligatoirement libéré dans la méthode `dispose()`.
- **Contexte asynchrone :** Ne jamais utiliser `BuildContext` après un `await` sans avoir préalablement vérifié `if (!mounted) return;`.
- **Aucune journalisation sauvage :** Ne jamais utiliser `print()` ou `debugPrint()` pour logger des données de santé ou des photos de patients.

---

## 4. Comment ajouter de nouveaux éléments ?

### Ajouter un nouveau texte dans l'application :
1. Ouvrir `lib/core/constants/app_strings.dart`.
2. Déclarer une nouvelle constante `static const String maCle = 'Mon texte en français';`.
3. Utiliser `AppStrings.maCle` dans le widget concerné.

### Ajouter un nouveau composant d'interface :
1. Créer un fichier dédié sous `lib/features/screening/ui/widgets/` (un seul widget public par fichier).
2. Déclarer un constructeur `const`.
3. Référencer exclusivement les tokens de `AppColors`, `AppDimens` et `AppTextStyles`.

---

## 5. Les interdits stricts (Sanctions de revue de code)

- ❌ **Interdit d'ajouter un nouveau package** dans `pubspec.yaml` sans accord formel préalable (la liste de la section 4 du cahier des charges est limitative).
- ❌ **Interdit d'implémenter un stockage local** (`shared_preferences`, SQLite, Realm, fichiers locaux conservés).
- ❌ **Interdit de coder une couleur ou une chaîne en dur** dans un composant d'interface.
- ❌ **Interdit de conserver un fichier image temporaire sur le disque** (le fichier doit être supprimé immédiatement après lecture).
