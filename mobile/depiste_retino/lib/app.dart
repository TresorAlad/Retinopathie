import 'package:flutter/material.dart';
import 'core/constants/app_strings.dart';
import 'core/theme/app_theme.dart';
import 'features/screening/ui/screening_page.dart';

/// Configuration racine de l'application MaterialApp.
/// Enforce le thème clair et borne l'échelle de texte système entre 1.0 et 1.3 pour l'accessibilité.
class DepisteRetinoApp extends StatelessWidget {
  const DepisteRetinoApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppStrings.appName,
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      builder: (context, child) {
        // Bridage de la taille de texte système entre 1.0 et 1.3 pour préserver la mise en page
        final mediaQuery = MediaQuery.of(context);
        final clampedTextScaler = mediaQuery.textScaler.clamp(
          minScaleFactor: 1.0,
          maxScaleFactor: 1.3,
        );

        return MediaQuery(
          data: mediaQuery.copyWith(textScaler: clampedTextScaler),
          child: child ?? const SizedBox.shrink(),
        );
      },
      home: const ScreeningPage(),
    );
  }
}
