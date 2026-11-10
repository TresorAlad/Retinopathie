# Système de design (Design System) — Dépiste Retino

> **À quoi sert ce document :** Consigner l'ensemble des tokens visuels (couleurs, typographies, élévations, rayons, formes) issus de la maquette Stitch et formaliser les règles de conversion Tailwind CSS vers Flutter.  
> **Pour qui :** Les développeurs d'interface graphique et les designers.

---

## 1. Philosophie visuelle : Chaleur organique tactile

L'identité visuelle de **Dépiste Retino** rompt avec la froideur clinique des applications médicales traditionnelles pour privilégier une atmosphère bienveillante, apaisante et humaine :
- Surfaces douces couleur parchemin clair (`#FFF8F5`).
- Ombres amples, diffuses et légèrement teintées.
- Courbures généreuses (rayons de 32px et profils pilules 9999px).
- Typographie ronde et lisible : **Plus Jakarta Sans**.

---

## 2. Palette de couleurs (`AppColors`)

| Rôle sémantique | Constante Dart | Code hexadécimal | Usage |
|---|---|---|---|
| Fond principal / Toile | `AppColors.surface` | `#FFF8F5` | Fond du Scaffold et de l'écran |
| Cartes et conteneurs | `AppColors.surfaceContainerLowest` | `#FFFFFF` | Fond des cartes principales |
| Fond des champs de saisie | `AppColors.surfaceContainerLow` | `#F9F2EF` | Fond des inputs et des étapes |
| Fond du viseur | `AppColors.surfaceContainer` | `#F3EDE9` | Viseur et badges neutres |
| Séparateurs / Neutre haut | `AppColors.surfaceContainerHigh` | `#EDE7E4` | Fond bouton Reprendre |
| Texte principal | `AppColors.onSurface` | `#1D1B19` | Titres et libellés |
| Texte secondaire | `AppColors.onSurfaceVariant` | `#53433F` | Paragraphes et sous-titres |
| Teinte primaire d'action | `AppColors.primary` | `#8D4D3B` | Icônes actives, anneaux |
| Conteneur primaire (Pêche) | `AppColors.primaryContainer` | `#F4A38C` | Bouton Analyser, réticule viseur |
| Texte sur primaire | `AppColors.onPrimaryContainer` | `#713726` | Texte du bouton Analyser |
| Vert de validation | `AppColors.secondary` | `#406749` | Icônes vérifiées, pastille |
| Conteneur vert pâle | `AppColors.secondaryContainer` | `#BFEAC5` | Fond badge bienveillant |
| Texte sur vert | `AppColors.onSecondaryContainer` | `#446B4D` | Texte badge bienveillant |
| Ambre d'alerte douce | `AppColors.tertiary` | `#815508` | Icône soleil, indicateur |
| Conteneur ambre clair | `AppColors.tertiaryFixed` | `#FFDDB3` | Fond icône soleil |
| Erreur médicale | `AppColors.error` | `#BA1A1A` | Bordures de champ en erreur |
| Fond bannière d'erreur | `AppColors.errorContainer` | `#FFDAD6` | Fond de la bannière rouge |
| Texte sur bannière d'erreur | `AppColors.onErrorContainer` | `#93000A` | Texte et icône de la bannière |

### Constantes avec transparence précalculées :
- `headerBg` (`0xCCFFF8F5`) : Fond supérieur à 80% d'opacité avec flou 24.
- `cardShadow` (`0x0F3D3A38`) : Ombre douce des cartes à 6% d'opacité.
- `focusRing` (`0x4D8D4D3B`) : Anneau de focus de 2px autour des champs (30% d'opacité).
- `viewerScrim` (`0x381D1B19`) : Masque sombre autour du cadrage des yeux (22% d'opacité).

---

## 3. Typographie (`AppTextStyles`)

Police de caractères imposée : **Plus Jakarta Sans** (via `google_fonts`).

| Style | Taille (px) | Hauteur de ligne (px) | Ratio `height` | Graisse (`FontWeight`) | Espacement (`letterSpacing`) |
|---|---|---|---|---|---|
| `headlineLgMobile` | 26 | 34 | 1.308 | 700 (Bold) | −0.015 em (−0.39 px) |
| `headlineMd` | 22 | 30 | 1.364 | 600 (SemiBold) | −0.01 em (−0.22 px) |
| `headlineSm` | 18 | 26 | 1.444 | 600 (SemiBold) | 0.0 |
| `labelLg` | 16 | 22 | 1.375 | 600 (SemiBold) | 0.0 |
| `labelMd` | 14 | 20 | 1.428 | 600 (SemiBold) | 0.0 |
| `labelSm` | 12 | 16 | 1.333 | 700 (Bold) | +0.02 em (+0.24 px) |
| `bodyMd` | 15 | 23 | 1.533 | 400 (Regular) | 0.0 |
| `bodySm` | 13 | 19 | 1.461 | 500 (Medium) | 0.0 |

---

## 4. Rayons de courbure (`AppDimens`)

> **Attention :** La configuration Tailwind de la maquette a redéfini les classes de rayon standard. Les valeurs suivantes font foi :

- `rounded-lg` -> **32 px** (AppCard principale).
- `rounded-xl` -> **48 px** (Profil pilule effectif pour les éléments de moins de 96px de haut).
- `rounded-2xl` -> **16 px** (Conteneurs internes, viseur, cartes de résultat).
- `rounded-full` -> **9999 px** (Boutons, badges, pastilles circulaires).

---

## 5. Table de conversion Tailwind CSS -> Flutter

| Classe Tailwind maquette | Équivalent Flutter implémenté |
|---|---|
| `bg-surface` | `color: AppColors.surface` |
| `rounded-[32px]` / `rounded-lg` | `BorderRadius.circular(AppDimens.cardRadius)` (32px) |
| `min-h-[56px]` | `constraints: BoxConstraints(minHeight: 56.0)` |
| `px-margin` (20px) | `padding: EdgeInsets.symmetric(horizontal: AppDimens.screenMargin)` |
| `space-y-6` (24px) | `SizedBox(height: AppDimens.blockSpacing)` (24px) |
| `gap-3` (12px) | `SizedBox(height: 12.0)` ou `width: 12.0` |
| `backdrop-blur-xl` | `BackdropFilter(filter: ImageFilter.blur(sigmaX: 24.0, sigmaY: 24.0))` |
| `active:scale-[0.98]` | Composant `PressableScale(pressedScale: 0.98)` |
| `animate-pulse` | Composant `PulseAnimation` (opacité 1.0 -> 0.5 -> 1.0 en 2s) |
| `animate-ping` | Composant `PingAnimation` (échelle 1 -> 2, opacité 0.75 -> 0 en 1s) |
| `animate-spin` | Composant `SpinAnimation` (rotation 360° en 1s) |

---

## 6. Règle d'or de développement

**Aucune couleur, taille, espacement ou texte ne doit être codé en dur directement dans un widget.**
- Couleurs -> exclusivement depuis `AppColors`
- Textes -> exclusivement depuis `AppStrings`
- Rayons, marges et espacements -> exclusivement depuis `AppDimens`
- Styles de texte -> exclusivement depuis `AppTextStyles`
