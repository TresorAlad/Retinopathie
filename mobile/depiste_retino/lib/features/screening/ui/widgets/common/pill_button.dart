import 'package:flutter/material.dart';
import 'package:depiste_retino/core/constants/app_dimens.dart';
import 'package:depiste_retino/core/theme/app_colors.dart';
import 'package:depiste_retino/core/theme/app_shadows.dart';
import 'package:depiste_retino/core/theme/app_text_styles.dart';
import 'pressable_scale.dart';

enum PillButtonVariant {
  primary,
  secondary,
}

class PillButton extends StatelessWidget {
  final String label;
  final VoidCallback? onTap;
  final PillButtonVariant variant;
  final Widget? leadingIcon;
  final Widget? trailingIcon;
  final bool isLoading;
  final bool isDisabled;
  final FontWeight fontWeight;

  const PillButton({
    super.key,
    required this.label,
    required this.onTap,
    this.variant = PillButtonVariant.primary,
    this.leadingIcon,
    this.trailingIcon,
    this.isLoading = false,
    this.isDisabled = false,
    this.fontWeight = FontWeight.w600,
  });

  @override
  Widget build(BuildContext context) {
    final effectiveDisabled = isDisabled || isLoading || onTap == null;

    final Color backgroundColor;
    final Color foregroundColor;
    final List<BoxShadow> boxShadow;

    switch (variant) {
      case PillButtonVariant.primary:
        backgroundColor = AppColors.primaryContainer;
        foregroundColor = AppColors.onPrimaryContainer;
        boxShadow = effectiveDisabled ? const [] : AppShadows.analyze;
        break;
      case PillButtonVariant.secondary:
        backgroundColor = AppColors.surfaceContainerHigh;
        foregroundColor = AppColors.onSurface;
        boxShadow = const [];
        break;
    }

    final content = AnimatedOpacity(
      duration: const Duration(milliseconds: 150),
      opacity: effectiveDisabled ? 0.5 : 1.0,
      child: Container(
        constraints: const BoxConstraints(minHeight: AppDimens.minTouchTarget),
        decoration: BoxDecoration(
          color: backgroundColor,
          borderRadius: BorderRadius.circular(AppDimens.pillRadius),
          boxShadow: boxShadow,
        ),
        padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 14.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.max,
          children: [
            if (leadingIcon != null) ...[
              leadingIcon!,
              const SizedBox(width: 8.0),
            ],
            Text(
              label,
              style: AppTextStyles.labelLg.copyWith(
                color: foregroundColor,
                fontWeight: fontWeight,
              ),
            ),
            if (trailingIcon != null) ...[
              const SizedBox(width: 8.0),
              trailingIcon!,
            ],
          ],
        ),
      ),
    );

    if (effectiveDisabled) {
      return content;
    }

    return PressableScale(
      onTap: onTap,
      child: content,
    );
  }
}
