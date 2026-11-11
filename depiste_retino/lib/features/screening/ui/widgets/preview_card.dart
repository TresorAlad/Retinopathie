import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';
import 'package:depiste_retino/core/constants/app_dimens.dart';
import 'package:depiste_retino/core/constants/app_strings.dart';
import 'package:depiste_retino/core/theme/app_colors.dart';
import 'package:depiste_retino/core/theme/app_shadows.dart';
import 'package:depiste_retino/core/theme/app_text_styles.dart';

import '../../logic/screening_controller.dart';
import 'common/app_card.dart';
import 'common/pill_button.dart';
import 'common/pulse_animations.dart';
import 'common/status_badge.dart';

class PreviewCard extends StatelessWidget {
  final ScreeningController controller;

  const PreviewCard({super.key, required this.controller});

  @override
  Widget build(BuildContext context) {
    final photoBytes = controller.photoBytes;
    if (photoBytes == null) return const SizedBox.shrink();

    final isSending = controller.isSending;
    final isDone = controller.isDone;

    final String analyzeLabel;
    final Widget? analyzeLeading;
    final Widget? analyzeTrailing;

    if (isSending) {
      analyzeLabel = AppStrings.analyzing;
      analyzeLeading = const SpinAnimation(
        child: Icon(
          Symbols.sync,
          size: 20.0,
          color: AppColors.onPrimaryContainer,
        ),
      );
      analyzeTrailing = null;
    } else if (isDone) {
      analyzeLabel = AppStrings.analyzed;
      analyzeLeading = null;
      analyzeTrailing = const Icon(
        Symbols.done,
        size: 20.0,
        color: AppColors.onPrimaryContainer,
      );
    } else {
      analyzeLabel = AppStrings.analyze;
      analyzeLeading = null;
      analyzeTrailing = const Icon(
        Symbols.arrow_forward,
        size: 20.0,
        color: AppColors.onPrimaryContainer,
      );
    }

    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Container(
                width: 10.0,
                height: 10.0,
                decoration: const BoxDecoration(
                  color: AppColors.secondary,
                  shape: BoxShape.circle,
                ),
              ),
              const SizedBox(width: 8.0),
              Expanded(
                child: Text(
                  AppStrings.previewTitle,
                  style: AppTextStyles.headlineSm.copyWith(
                    fontWeight: FontWeight.w600,
                    color: AppColors.onSurface,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: 8.0),
              const StatusBadge(
                label: AppStrings.previewBadge,
                backgroundColor: AppColors.secondaryFixed,
                foregroundColor: AppColors.onSecondaryFixedVariant,
                padding: EdgeInsets.symmetric(horizontal: 10.0, vertical: 4.0),
                icon: Icon(
                  Symbols.check_circle,
                  size: 14.0,
                  color: AppColors.onSecondaryFixedVariant,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppDimens.cardSpacing),
          Container(
            constraints: const BoxConstraints(maxHeight: 288.0),
            decoration: BoxDecoration(
              color: AppColors.surfaceContainer,
              borderRadius: BorderRadius.circular(AppDimens.innerRadius),
              boxShadow: AppShadows.md,
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(AppDimens.innerRadius),
              child: Image.memory(
                photoBytes,
                fit: BoxFit.cover,
                width: double.infinity,
              ),
            ),
          ),
          const SizedBox(height: AppDimens.cardSpacing),
          Row(
            children: [
              Expanded(
                flex: 2,
                child: PillButton(
                  label: AppStrings.retake,
                  onTap: isSending ? null : controller.retakePhoto,
                  variant: PillButtonVariant.secondary,
                  leadingIcon: const Icon(
                    Symbols.refresh,
                    size: 20.0,
                    color: AppColors.onSurface,
                  ),
                  isDisabled: isSending,
                ),
              ),
              const SizedBox(width: 12.0),
              Expanded(
                flex: 3,
                child: PillButton(
                  label: analyzeLabel,
                  onTap: (isSending || isDone) ? null : controller.analyze,
                  variant: PillButtonVariant.primary,
                  leadingIcon: analyzeLeading,
                  trailingIcon: analyzeTrailing,
                  isLoading: isSending,
                  isDisabled: isSending || isDone,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
