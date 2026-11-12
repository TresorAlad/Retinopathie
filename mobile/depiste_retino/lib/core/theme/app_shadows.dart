import 'package:flutter/material.dart';
import 'app_colors.dart';

/// Définitions des ombres portées douces conformes à l'élévation Stitch.
abstract final class AppShadows {
  /// Ombre standard des cartes : 0 4 20 -2 rgba(61, 58, 56, 0.06)
  static const List<BoxShadow> card = [
    BoxShadow(
      offset: Offset(0, 4),
      blurRadius: 20.0,
      spreadRadius: -2.0,
      color: AppColors.cardShadow,
    ),
  ];

  /// Ombre de l'en-tête fixe : 0 1 8 0 rgba(0, 0, 0, 0.04)
  static const List<BoxShadow> header = [
    BoxShadow(
      offset: Offset(0, 1),
      blurRadius: 8.0,
      spreadRadius: 0.0,
      color: AppColors.headerShadow,
    ),
  ];

  /// Ombre Tailwind md : 0 4 6 -1 + 0 2 4 -2
  static const List<BoxShadow> md = [
    BoxShadow(
      offset: Offset(0, 4),
      blurRadius: 6.0,
      spreadRadius: -1.0,
      color: AppColors.shadowMd,
    ),
    BoxShadow(
      offset: Offset(0, 2),
      blurRadius: 4.0,
      spreadRadius: -2.0,
      color: AppColors.shadowMd,
    ),
  ];

  /// Ombre Tailwind sm : 0 1 2 0
  static const List<BoxShadow> sm = [
    BoxShadow(
      offset: Offset(0, 1),
      blurRadius: 2.0,
      spreadRadius: 0.0,
      color: AppColors.shadowSm,
    ),
  ];

  /// Ombre intense de l'obturateur : 0 8 24 0 rgba(244, 163, 140, 0.55)
  static const List<BoxShadow> shutter = [
    BoxShadow(
      offset: Offset(0, 8),
      blurRadius: 24.0,
      spreadRadius: 0.0,
      color: AppColors.shutterShadow,
    ),
  ];

  /// Ombre du bouton Analyser : 0 6 20 0 rgba(244, 163, 140, 0.40)
  static const List<BoxShadow> analyze = [
    BoxShadow(
      offset: Offset(0, 6),
      blurRadius: 20.0,
      spreadRadius: 0.0,
      color: AppColors.analyzeShadow,
    ),
  ];
}
