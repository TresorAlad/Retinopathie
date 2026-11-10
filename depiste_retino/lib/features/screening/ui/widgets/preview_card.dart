import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';
import '../../../../core/constants/app_dimens.dart';
import '../../../../core/constants/app_strings.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_shadows.dart';
import '../../../../core/theme/app_text_styles.dart';
import '../../logic/screening_controller.dart';
import 'common/app_card.dart';
import 'common/pill_button.dart';
import 'common/pulse_animations.dart';
import 'common/status_badge.dart';

/// Carte affichant l'aperçu du cliché instantané capturé en mémoire et les actions Reprendre / Analyser.
class PreviewCard extends StatelessWidget {
  final ScreeningController controller;

  const PreviewCard({super.key, required this.controller});

  @override
  Widget build(BuildContext context) {
    final photoBytes = controller.photoBytes;
    if (photoBytes == null) return const SizedBox.shrink();

    final isSending = controller.isSending;
    final isDone = controller.isDone;

    // Configuration dynamique du bouton Analyser selon son état
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
          // En-tête de la carte
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
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
                  Text(
                    AppStrings.previewTitle,
                    style: AppTextStyles.headlineSm.copyWith(
                      fontWeight: FontWeight.w600,
                      color: AppColors.onSurface,
                    ),
                  ),
                ],
              ),
              StatusBadge(
                label: AppStrings.previewBadge,
                backgroundColor: AppColors.secondaryFixed,
                foregroundColor: AppColors.onSecondaryFixedVariant,
                padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 4.0),
                icon: const Icon(
                  Symbols.check_circle,
                  size: 14.0,
                  color: AppColors.onSecondaryFixedVariant,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppDimens.cardSpacing),

          // Cadre de la photo capturée
          Container(
            constraints: const BoxConstraints(maxHeight: 288.0),
            decoration: BoxDecoration(
              color: AppColors.surfaceContainer,
              borderRadius: BorderRadius.circular(AppDimens.innerRadius),
              boxShadow: AppShadows.md,
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(AppDimens.innerRadius),
              child: AspectRatio(
                aspectRatio: 16 / 10,
                child: Stack(
                  fit: StackFit.expand,
                  children: [
                    Image.memory(
                      photoBytes,
                      fit: BoxFit.cover,
                      gaplessPlayback: true,
                    ),
                    // Dégradé d'ambiance collé au bas du cliché
                    Positioned(
                      left: 0,
                      right: 0,
                      bottom: 0,
                      height: 24.0,
                      child: Container(
                        decoration: const BoxDecoration(
                          gradient: LinearGradient(
                            begin: Alignment.bottomCenter,
                            end: Alignment.topCenter,
                            colors: [
                              AppColors.photoGradBottom,
                              AppColors.photoGradMid,
                              Colors.transparent,
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          const SizedBox(height: 16.0),

          // Boutons d'action : Reprendre et Analyser
          Column(
            children: [
              PillButton(
                label: AppStrings.retake,
                onTap: controller.retakePhoto,
                variant: PillButtonVariant.secondary,
                isDisabled: isSending,
                leadingIcon: const Icon(
                  Symbols.replay,
                  size: 20.0,
                  color: AppColors.onSurface,
                ),
              ),
              const SizedBox(height: 12.0),
              PillButton(
                label: analyzeLabel,
                onTap: controller.analyze,
                variant: PillButtonVariant.primary,
                fontWeight: FontWeight.w700,
                isDisabled: isSending || isDone,
                leadingIcon: analyzeLeading,
                trailingIcon: analyzeTrailing,
              ),
            ],
          ),
        ],
      ),
    );
  }
}
