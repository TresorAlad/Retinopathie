import 'package:flutter/material.dart';
import '../../../../core/constants/app_dimens.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_shadows.dart';

/// Conteneur carte blanc standard de l'application (rayon 32px, ombre douce).
class AppCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry padding;
  final Clip clipBehavior;

  const AppCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(20.0),
    this.clipBehavior = Clip.none,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      clipBehavior: clipBehavior,
      decoration: BoxDecoration(
        color: AppColors.surfaceContainerLowest,
        borderRadius: BorderRadius.circular(AppDimens.cardRadius),
        boxShadow: AppShadows.card,
      ),
      padding: padding,
      child: child,
    );
  }
}
