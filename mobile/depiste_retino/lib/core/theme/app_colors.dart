import 'package:flutter/painting.dart';

/// Définition exhaustive des tokens de couleur de l'application Dépiste Retino.
/// Toutes les constantes sont déclarées en `const` pour éviter les recalculs.
abstract final class AppColors {
  // 6.1 Couleurs de base de la maquette Stitch
  static const Color surface = Color(0xFFFFF8F5);
  static const Color background = Color(0xFFFFF8F5);
  static const Color surfaceBright = Color(0xFFFFF8F5);
  static const Color surfaceDim = Color(0xFFDFD9D6);
  static const Color surfaceContainerLowest = Color(0xFFFFFFFF);
  static const Color surfaceContainerLow = Color(0xFFF9F2EF);
  static const Color surfaceContainer = Color(0xFFF3EDE9);
  static const Color surfaceContainerHigh = Color(0xFFEDE7E4);
  static const Color surfaceContainerHighest = Color(0xFFE8E1DE);
  static const Color surfaceVariant = Color(0xFFE8E1DE);

  static const Color onSurface = Color(0xFF1D1B19);
  static const Color onBackground = Color(0xFF1D1B19);
  static const Color onSurfaceVariant = Color(0xFF53433F);

  static const Color outline = Color(0xFF86736E);
  static const Color outlineVariant = Color(0xFFD8C2BC);
  static const Color inverseSurface = Color(0xFF33302E);
  static const Color inverseOnSurface = Color(0xFFF6EFEC);

  static const Color primary = Color(0xFF8D4D3B);
  static const Color surfaceTint = Color(0xFF8D4D3B);
  static const Color onPrimary = Color(0xFFFFFFFF);
  static const Color primaryContainer = Color(0xFFF4A38C);
  static const Color onPrimaryContainer = Color(0xFF713726);
  static const Color primaryFixed = Color(0xFFFFDBD1);
  static const Color primaryFixedDim = Color(0xFFFFB5A0);
  static const Color onPrimaryFixed = Color(0xFF380C02);
  static const Color onPrimaryFixedVariant = Color(0xFF703625);
  static const Color inversePrimary = Color(0xFFFFB5A0);

  static const Color secondary = Color(0xFF406749);
  static const Color onSecondary = Color(0xFFFFFFFF);
  static const Color secondaryContainer = Color(0xFFBFEAC5);
  static const Color onSecondaryContainer = Color(0xFF446B4D);
  static const Color secondaryFixed = Color(0xFFC1EDC8);
  static const Color secondaryFixedDim = Color(0xFFA6D1AD);
  static const Color onSecondaryFixed = Color(0xFF00210C);
  static const Color onSecondaryFixedVariant = Color(0xFF284F33);

  static const Color tertiary = Color(0xFF815508);
  static const Color onTertiary = Color(0xFFFFFFFF);
  static const Color tertiaryContainer = Color(0xFFE5AD5C);
  static const Color onTertiaryContainer = Color(0xFF644100);
  static const Color tertiaryFixed = Color(0xFFFFDDB3);
  static const Color tertiaryFixedDim = Color(0xFFF6BC6A);
  static const Color onTertiaryFixed = Color(0xFF291800);
  static const Color onTertiaryFixedVariant = Color(0xFF633F00);

  static const Color error = Color(0xFFBA1A1A);
  static const Color onError = Color(0xFFFFFFFF);
  static const Color errorContainer = Color(0xFFFFDAD6);
  static const Color onErrorContainer = Color(0xFF93000A);

  // 6.2 Couleurs avec transparence (ARGB précalculés)
  static const Color headerBg = Color(0xCCFFF8F5);
  static const Color headerShadow = Color(0x0A000000);
  static const Color cardShadow = Color(0x0F3D3A38);
  static const Color inputBorder = Color(0x99EDE7E4);
  static const Color inputHint = Color(0x9953433F);
  static const Color focusRing = Color(0x4D8D4D3B);
  static const Color viewerScrim = Color(0x381D1B19);

  static const Color viewerGradTop = Color(0x66DFD9D6);
  static const Color viewerGradMid = Color(0x33F3EDE9);
  static const Color viewerGradBottom = Color(0x80DFD9D6);

  static const Color whiteStrokeDashed = Color(0xD9FFFFFF);
  static const Color whiteStrokeSolid = Color(0xE6FFFFFF);
  static const Color whiteStrokeSoft = Color(0x99FFFFFF);

  static const Color controlBg = Color(0xD933302E);
  static const Color ringPing = Color(0x66F4A38C);
  static const Color shutterShadow = Color(0x8CF4A38C);
  static const Color analyzeShadow = Color(0x66F4A38C);

  static const Color photoGradBottom = Color(0xCC33302E);
  static const Color photoGradMid = Color(0x4D33302E);

  static const Color shadowMd = Color(0x1A000000);
  static const Color shadowSm = Color(0x0D000000);
  static const Color shadowInner = Color(0x0D000000);
}
