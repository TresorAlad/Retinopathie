import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';

import '../../../../core/constants/app_strings.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';
import 'common/pill_button.dart';

/// Vue d'état affichée dans le viseur lorsque l'accès à la caméra est refusé ou indisponible.
class CameraPermissionView extends StatelessWidget {
  final bool isPermanentlyDenied;
  final bool hasCameraError;
  final bool hasNoCamera;
  final VoidCallback onAction;

  const CameraPermissionView({
    super.key,
    required this.isPermanentlyDenied,
    required this.hasCameraError,
    required this.hasNoCamera,
    required this.onAction,
  });

  @override
  Widget build(BuildContext context) {
    final String message;
    if (hasNoCamera) {
      message = AppStrings.noCamera;
    } else if (hasCameraError) {
      message = AppStrings.cameraError;
    } else {
      message = AppStrings.permDenied;
    }

    final String buttonLabel = isPermanentlyDenied
        ? AppStrings.permSettings
        : AppStrings.permAllow;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 24.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(
            Symbols.no_photography,
            size: 32.0,
            color: AppColors.onSurfaceVariant,
          ),
          const SizedBox(height: 8.0),
          Text(
            message,
            textAlign: TextAlign.center,
            style: AppTextStyles.bodySm.copyWith(
              color: AppColors.onSurfaceVariant,
            ),
          ),
          if (!hasCameraError && !hasNoCamera) ...[
            const SizedBox(height: 12.0),
            PillButton(
              label: buttonLabel,
              onTap: onAction,
              fontWeight: FontWeight.w700,
            ),
          ] else if (hasCameraError) ...[
            const SizedBox(height: 12.0),
            Semantics(
              label: AppStrings.semCameraRetry,
              button: true,
              child: PillButton(
                label: AppStrings.cameraRetry,
                onTap: onAction,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ],
      ),
    );
  }
}
