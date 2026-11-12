import 'package:flutter/material.dart';
import '../../../../core/constants/app_dimens.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_shadows.dart';
import 'common/pressable_scale.dart';

/// Bouton tactile circulaire de contrôle caméra (flash et bascule d'objectif).
/// Zone visuelle de 44px centrée dans une zone tactile ergonomique de 56x56px.
class CameraControlButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback onTap;
  final String semanticsLabel;

  const CameraControlButton({
    super.key,
    required this.icon,
    required this.onTap,
    required this.semanticsLabel,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: semanticsLabel,
      button: true,
      child: PressableScale(
        onTap: onTap,
        child: SizedBox(
          width: AppDimens.minTouchTarget,
          height: AppDimens.minTouchTarget,
          child: Center(
            child: Container(
              width: 44.0,
              height: 44.0,
              decoration: const BoxDecoration(
                color: AppColors.controlBg,
                shape: BoxShape.circle,
                boxShadow: AppShadows.sm,
              ),
              child: Icon(
                icon,
                size: 22.0,
                color: AppColors.inverseOnSurface,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
