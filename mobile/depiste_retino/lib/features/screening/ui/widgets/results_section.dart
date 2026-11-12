import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';

import '../../../../core/constants/app_strings.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_shadows.dart';
import '../../../../core/theme/app_text_styles.dart';
import '../../../../core/utils/time_format.dart';
import '../../data/models/screening_result.dart';

/// Section des résultats affichant le texte explicatif renvoyé par l'API et la mention de sécurité.
class ResultsSection extends StatelessWidget {
  final ScreeningResult result;

  const ResultsSection({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Ligne de titre avec horodatage réel
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                const Icon(
                  Symbols.troubleshoot,
                  size: 24.0,
                  color: AppColors.primary,
                ),
                const SizedBox(width: 8.0),
                Text(
                  AppStrings.resultsTitle,
                  style: AppTextStyles.headlineMd.copyWith(
                    fontWeight: FontWeight.w700,
                    color: AppColors.onSurface,
                  ),
                ),
              ],
            ),
            Text(
              TimeFormat.formatReceiptTime(result.receivedAt),
              style: AppTextStyles.labelSm.copyWith(
                color: AppColors.onSurfaceVariant,
              ),
            ),
          ],
        ),
        const SizedBox(height: 16.0),

        // Carte principale de résultat
        Container(
          decoration: BoxDecoration(
            color: AppColors.surfaceContainerLowest,
            borderRadius: BorderRadius.circular(16.0),
            boxShadow: AppShadows.card,
          ),
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Badge de validation unifié
              Row(
                children: [
                  Container(
                    width: 44.0,
                    height: 44.0,
                    decoration: const BoxDecoration(
                      color: AppColors.secondaryContainer,
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(
                      Symbols.verified,
                      size: 26.0,
                      color: AppColors.secondary,
                      fill: 1.0,
                    ),
                  ),
                  const SizedBox(width: 12.0),
                  Text(
                    AppStrings.resultsLabel,
                    style: AppTextStyles.labelSm.copyWith(
                      fontWeight: FontWeight.w700,
                      letterSpacing: 0.025 * 12.0,
                      color: AppColors.secondary,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16.0),

              if (!result.isEye) ...[
                Row(
                  children: [
                    const Icon(
                      Symbols.warning,
                      size: 20.0,
                      color: AppColors.tertiary,
                    ),
                    const SizedBox(width: 8.0),
                    Expanded(
                      child: Text(
                        AppStrings.eyeNotDetected,
                        style: AppTextStyles.labelSm.copyWith(
                          fontWeight: FontWeight.w600,
                          color: AppColors.tertiary,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12.0),
              ],

              if (result.stageLabel != null &&
                  result.stageLabel!.isNotEmpty) ...[
                Text(
                  '${AppStrings.stagePrefix} : ${result.stageLabel}',
                  style: AppTextStyles.bodySm.copyWith(
                    fontWeight: FontWeight.w600,
                    color: AppColors.onSurface,
                  ),
                ),
                const SizedBox(height: 8.0),
              ],

              if (result.referToDoctor) ...[
                Row(
                  children: [
                    const Icon(
                      Symbols.local_hospital,
                      size: 20.0,
                      color: AppColors.error,
                    ),
                    const SizedBox(width: 8.0),
                    Text(
                      AppStrings.referDoctor,
                      style: AppTextStyles.bodySm.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AppColors.error,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 12.0),
              ],

              // Bloc de texte intégral de l'API
              Text(
                result.text,
                style: AppTextStyles.bodyMd.copyWith(
                  height: 24.375 / 15.0,
                  color: AppColors.onSurfaceVariant,
                ),
              ),

              if (result.recommendations.isNotEmpty) ...[
                const SizedBox(height: 16.0),
                Text(
                  'Recommandations',
                  style: AppTextStyles.bodySm.copyWith(
                    fontWeight: FontWeight.w700,
                    color: AppColors.onSurface,
                  ),
                ),
                const SizedBox(height: 8.0),
                ...result.recommendations.map(
                  (line) => Padding(
                    padding: const EdgeInsets.only(bottom: 6.0),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          '• ',
                          style: TextStyle(color: AppColors.onSurfaceVariant),
                        ),
                        Expanded(
                          child: Text(
                            line,
                            style: AppTextStyles.bodySm.copyWith(
                              color: AppColors.onSurfaceVariant,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
        const SizedBox(height: 16.0),

        // Ligne de réassurance et chiffrement
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Symbols.lock, size: 18.0, color: AppColors.secondary),
              const SizedBox(width: 8.0),
              Flexible(
                child: RichText(
                  textAlign: TextAlign.center,
                  text: TextSpan(
                    style: AppTextStyles.bodySm.copyWith(
                      color: AppColors.onSurfaceVariant,
                    ),
                    children: const [
                      TextSpan(
                        text: '${AppStrings.secureBold} ',
                        style: TextStyle(
                          fontWeight: FontWeight.w600,
                          color: AppColors.onSurface,
                        ),
                      ),
                      TextSpan(text: AppStrings.secureRest),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
