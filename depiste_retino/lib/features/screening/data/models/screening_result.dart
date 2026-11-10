/// Modèle encapsulant la réponse explicative renvoyée par l'API et son horodatage de réception.
final class ScreeningResult {
  /// Bloc de texte explicatif médical complet renvoyé par l'API.
  final String text;

  /// Horodatage exact de la réception de la réponse pour affichage dynamique.
  final DateTime receivedAt;

  const ScreeningResult({
    required this.text,
    required this.receivedAt,
  });
}
