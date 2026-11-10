import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';
import '../../../../core/constants/app_strings.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';

/// Bloc d'avertissement médical réglementaire toujours visible au bas de l'écran.
class DisclaimerCard extends StatelessWidget {
  const DisclaimerCard({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLow,
        borderRadius: BorderRadius.circular(16.0),
      ),
      padding: const EdgeInsets.all(20.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            margin: const EdgeInsets.only(top: 2.0),
            width: 24.0,
            height: 24.0,
            decoration: const BoxDecoration(
              color: AppColors.surfaceContainerHigh,
              shape: BoxShape.circle,
            ),
            child: const Icon(
              Symbols.info,
              size: 16.0,
              color: AppColors.onSurfaceVariant,
            ),
          ),
          const SizedBox(width: 12.0),
          Expanded(
            child: Text(
              AppStrings.disclaimer,
              style: AppTextStyles.bodySm.copyWith(
                height: 21.125 / 13.0,
                color: AppColors.onSurfaceVariant,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
