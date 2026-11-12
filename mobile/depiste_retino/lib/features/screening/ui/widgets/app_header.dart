import 'dart:ui';
import 'package:flutter/material.dart';
import '../../../../core/constants/app_dimens.dart';
import '../../../../core/constants/app_strings.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_shadows.dart';
import '../../../../core/theme/app_text_styles.dart';

/// En-tête supérieur fixe avec arrière-plan semi-transparent et flou gaussien.
/// Affiche uniquement le titre « Dépiste Retino » sans icône ni logo.
class AppHeader extends StatelessWidget {
  const AppHeader({super.key});

  @override
  Widget build(BuildContext context) {
    final statusBarHeight = MediaQuery.of(context).padding.top;
    final totalHeight = AppDimens.headerHeight + statusBarHeight;

    return Container(
      height: totalHeight,
      decoration: const BoxDecoration(
        boxShadow: AppShadows.header,
      ),
      child: ClipRect(
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 24.0, sigmaY: 24.0),
          child: Container(
            color: AppColors.headerBg,
            padding: EdgeInsets.only(
              top: statusBarHeight,
              left: AppDimens.screenMargin,
              right: AppDimens.screenMargin,
            ),
            alignment: Alignment.centerLeft,
            child: Text(
              AppStrings.appName,
              style: AppTextStyles.headlineSm.copyWith(
                fontWeight: FontWeight.w700,
                letterSpacing: -0.025 * 18.0,
                color: AppColors.onSurface,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
