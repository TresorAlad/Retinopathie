import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';
import '../../data/screening_error.dart';

/// Bannière d'erreur non intrusive affichée en cas de défaillance réseau ou d'indisponibilité du serveur.
class ErrorBanner extends StatelessWidget {
  final ScreeningError error;

  const ErrorBanner({super.key, required this.error});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.errorContainer,
        borderRadius: BorderRadius.circular(16.0),
      ),
      padding: const EdgeInsets.all(16.0),
      child: Row(
        children: [
          Icon(
            error.icon,
            size: 24.0,
            color: AppColors.onErrorContainer,
          ),
          const SizedBox(width: 12.0),
          Expanded(
            child: Text(
              error.message,
              style: AppTextStyles.labelLg.copyWith(
                fontWeight: FontWeight.w700,
                color: AppColors.onErrorContainer,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
