/// Configuration de l'API d'analyse. Toutes les valeurs à ajuster sont ici.
abstract final class ApiConfig {
  // URL ngrok fournie au lancement avec --dart-define=API_BASE_URL=...
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'https://api.example.invalid',
  );

  static const String analyzePath = '/api/v1/mobile/scan';

  // La clé est fournie au lancement ; une clé embarquée dans l'application reste extractible.
  static const String apiKey = String.fromEnvironment(
    'API_KEY',
    defaultValue: '',
  );
  static const String authHeaderName = 'X-Mobile-Api-Key';
  static const String authHeaderPrefix = '';

  static const String responseTextKey = 'patient_message';

  /// Délai maximal pour l'ensemble de la requête (imposé par le cahier des charges).
  static const Duration timeout = Duration(seconds: 60);

  /// URI complète vers le point de terminaison d'analyse.
  static Uri get analyzeUri => Uri.parse('$baseUrl$analyzePath');

  /// En-têtes HTTP ; MultipartRequest ajoute le Content-Type avec sa frontière.
  static Map<String, String> get headers {
    final headersMap = <String, String>{
      'Accept': 'application/json',
      'ngrok-skip-browser-warning': 'true',
    };
    if (apiKey.isNotEmpty) {
      headersMap[authHeaderName] = '$authHeaderPrefix$apiKey';
    }
    return headersMap;
  }
}
