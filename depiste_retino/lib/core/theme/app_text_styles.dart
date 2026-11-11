import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app_colors.dart';

abstract final class AppTextStyles {
  static TextStyle get headlineLgMobile => GoogleFonts.plusJakartaSans(
        fontSize: 26.0,
        height: 34.0 / 26.0,
        fontWeight: FontWeight.w700,
        letterSpacing: -0.015 * 26.0,
        color: AppColors.onSurface,
      ).copyWith(
        leadingDistribution: TextLeadingDistribution.even,
      );

  static TextStyle get headlineMd => GoogleFonts.plusJakartaSans(
        fontSize: 22.0,
        height: 30.0 / 22.0,
        fontWeight: FontWeight.w600,
        letterSpacing: -0.01 * 22.0,
        color: AppColors.onSurface,
      ).copyWith(
        leadingDistribution: TextLeadingDistribution.even,
      );

  static TextStyle get headlineSm => GoogleFonts.plusJakartaSans(
        fontSize: 18.0,
        height: 26.0 / 18.0,
        fontWeight: FontWeight.w600,
        letterSpacing: 0.0,
        color: AppColors.onSurface,
      ).copyWith(
        leadingDistribution: TextLeadingDistribution.even,
      );

  static TextStyle get labelLg => GoogleFonts.plusJakartaSans(
        fontSize: 16.0,
        height: 22.0 / 16.0,
        fontWeight: FontWeight.w600,
        letterSpacing: 0.0,
        color: AppColors.onSurface,
      ).copyWith(
        leadingDistribution: TextLeadingDistribution.even,
      );

  static TextStyle get labelMd => GoogleFonts.plusJakartaSans(
        fontSize: 14.0,
        height: 20.0 / 14.0,
        fontWeight: FontWeight.w600,
        letterSpacing: 0.0,
        color: AppColors.onSurface,
      ).copyWith(
        leadingDistribution: TextLeadingDistribution.even,
      );

  static TextStyle get labelSm => GoogleFonts.plusJakartaSans(
        fontSize: 12.0,
        height: 16.0 / 12.0,
        fontWeight: FontWeight.w700,
        letterSpacing: 0.02 * 12.0,
        color: AppColors.onSurface,
      ).copyWith(
        leadingDistribution: TextLeadingDistribution.even,
      );

  static TextStyle get bodyMd => GoogleFonts.plusJakartaSans(
        fontSize: 15.0,
        height: 23.0 / 15.0,
        fontWeight: FontWeight.w400,
        letterSpacing: 0.0,
        color: AppColors.onSurface,
      ).copyWith(
        leadingDistribution: TextLeadingDistribution.even,
      );

  static TextStyle get bodySm => GoogleFonts.plusJakartaSans(
        fontSize: 13.0,
        height: 19.0 / 13.0,
        fontWeight: FontWeight.w500,
        letterSpacing: 0.0,
        color: AppColors.onSurface,
      ).copyWith(
        leadingDistribution: TextLeadingDistribution.even,
      );
}
