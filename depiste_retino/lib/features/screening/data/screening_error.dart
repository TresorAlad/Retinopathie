import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';

import '../../../core/constants/app_strings.dart';

/// Typologie des erreurs d'analyse et de capture.
enum ScreeningError {
  /// Aucune connexion Internet disponible sur le terminal.
  noConnection,

  /// Serveur inaccessible, hors service, code HTTP != 2xx ou réponse invalide.
  serverUnavailable,

  /// Délai maximal d'attente de 60 secondes dépassé.
  timeout,

  /// La prise de vue ou sa conversion en PNG a échoué.
  captureFailed;

  /// Libellé textuel officiel en français à afficher dans la bannière.
  String get message {
    switch (this) {
      case ScreeningError.noConnection:
        return AppStrings.errNoConnection;
      case ScreeningError.serverUnavailable:
        return AppStrings.errServer;
      case ScreeningError.timeout:
        return AppStrings.errTimeout;
      case ScreeningError.captureFailed:
        return AppStrings.errCapture;
    }
  }

  /// Icône Material Symbols Outlined correspondante.
  IconData get icon {
    switch (this) {
      case ScreeningError.noConnection:
        return Symbols.wifi_off;
      case ScreeningError.serverUnavailable:
        return Symbols.cloud_off;
      case ScreeningError.timeout:
        return Symbols.schedule;
      case ScreeningError.captureFailed:
        return Symbols.no_photography;
    }
  }
}
