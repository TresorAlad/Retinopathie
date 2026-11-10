import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';
import '../../../../core/constants/app_strings.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';
import 'common/status_badge.dart';

/// Section d'introduction bienveillante avec badges de certification et description du dépistage.
class IntroSection extends StatelessWidget {
  const IntroSection({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 8.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Ligne de badges contextuels
          Row(
            children: [
              StatusBadge(
                label: AppStrings.badgeKind,
                backgroundColor: AppColors.secondaryContainer,
                foregroundColor: AppColors.onSecondaryContainer,
                padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 4.0),
                icon: const Icon(
                  Symbols.spa,
                  size: 15.0,
                  color: AppColors.onSecondaryContainer,
                  fill: 1.0,
                ),
              ),
              const SizedBox(width: 8.0),
              StatusBadge(
                label: AppStrings.badgeVersion,
                backgroundColor: AppColors.surfaceContainerHigh,
                foregroundColor: AppColors.onSurfaceVariant,
                padding: const EdgeInsets.symmetric(horizontal: 10.0, vertical: 4.0),
                icon: Container(
                  width: 6.0,
                  height: 6.0,
                  decoration: const BoxDecoration(
                    color: AppColors.secondary,
                    shape: BoxShape.circle,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8.0),

          // Titre principal
          Text(
            AppStrings.introTitle,
            style: AppTextStyles.headlineLgMobile.copyWith(
              fontWeight: FontWeight.w700,
              letterSpacing: -0.025 * 26.0,
              color: AppColors.onSurface,
            ),
          ),
          const SizedBox(height: 8.0),

          // Paragraphe d'accompagnement
          Text(
            AppStrings.introText,
            style: AppTextStyles.bodyMd.copyWith(
              color: AppColors.onSurfaceVariant,
            ),
          ),
        ],
      ),
    );
  }
}
