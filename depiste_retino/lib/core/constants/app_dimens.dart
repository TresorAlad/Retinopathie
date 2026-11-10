/// Constantes géométriques : rayons, marges, espacements et dimensions d'ergonomie tactile.
abstract final class AppDimens {
  // Rayons imposés par le design system
  /// Rayon standard des cartes (rounded-lg = 32px)
  static const double cardRadius = 32.0;

  /// Rayon intermédiaire des conteneurs internes (rounded-2xl = 16px)
  static const double innerRadius = 16.0;

  /// Rayon arrondi pilule (haute courbure)
  static const double pillRadius = 9999.0;

  /// Rayon effectif des champs de saisie (hauteur 52px / 2 = 26px)
  static const double inputRadius = 26.0;

  // Espacements et marges
  /// Marge horizontale générale de l'écran (20px)
  static const double screenMargin = 20.0;

  /// Espacement vertical entre les blocs principaux (24px)
  static const double blockSpacing = 24.0;

  /// Espacement interne standard dans les cartes (16px)
  static const double cardSpacing = 16.0;

  /// Espacement entre les champs de formulaire (12px)
  static const double fieldSpacing = 12.0;

  /// Espacement standard entre libellé et champ (6px)
  static const double labelSpacing = 6.0;

  // Hauteurs et contraintes
  /// Hauteur fixe de l'en-tête supérieur hors zone de sécurité
  static const double headerHeight = 64.0;

  /// Hauteur tactile minimale recommandée pour les boutons et contrôles (56px)
  static const double minTouchTarget = 56.0;

  /// Hauteur minimale des champs de saisie (52px)
  static const double inputMinHeight = 52.0;

  /// Largeur maximale de la colonne de contenu centré sur écran large (480px)
  static const double maxContentWidth = 480.0;
}
