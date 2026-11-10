/// Configuration de l'API d'analyse. Toutes les valeurs à ajuster sont ici.
abstract final class ApiConfig {
  // TODO(API): URL de base fournie plus tard. Surchargeable avec --dart-define=API_BASE_URL=...
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'https://api.example.invalid', // domaine réservé : ne se résout jamais
  );

  // TODO(API): chemin de l'endpoint d'analyse.
  static const String analyzePath = '/analyze';

  // TODO(API): clé d'accès (méthode d'authentification inconnue). Vide = aucun en-tête d'authentification.
  static const String apiKey = String.fromEnvironment('API_KEY', defaultValue: '');
  static const String authHeaderName = 'Authorization'; // TODO(API)
  static const String authHeaderPrefix = 'Bearer ';     // TODO(API)

  // TODO(API): nom du champ JSON contenant le texte de la réponse.
  static const String responseTextKey = 'resultat';

  /// Délai maximal pour l'ensemble de la requête (imposé par le cahier des charges).
  static const Duration timeout = Duration(seconds: 60);

  /// URI complète vers le point de terminaison d'analyse.
  static Uri get analyzeUri => Uri.parse('$baseUrl$analyzePath');

  /// En-têtes HTTP de la requête JSON.
  static Map<String, String> get headers {
    final headersMap = <String, String>{
      'Content-Type': 'application/json; charset=utf-8',
      'Accept': 'application/json',
    };
    if (apiKey.isNotEmpty) {
      headersMap[authHeaderName] = '$authHeaderPrefix$apiKey';
    }
    return headersMap;
  }
}
