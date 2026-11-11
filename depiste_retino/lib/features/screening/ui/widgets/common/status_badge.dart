import 'package:flutter/material.dart';
import 'package:depiste_retino/core/constants/app_dimens.dart';
import 'package:depiste_retino/core/theme/app_text_styles.dart';

class StatusBadge extends StatelessWidget {
  final String label;
  final Color backgroundColor;
  final Color foregroundColor;
  final Widget? icon;
  final EdgeInsetsGeometry padding;

  const StatusBadge({
    super.key,
    required this.label,
    required this.backgroundColor,
    required this.foregroundColor,
    this.icon,
    this.padding = const EdgeInsets.symmetric(horizontal: 12.0, vertical: 4.0),
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: backgroundColor,
        borderRadius: BorderRadius.circular(AppDimens.pillRadius),
      ),
      padding: padding,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (icon != null) ...[
            icon!,
            const SizedBox(width: 4.0),
          ],
          Text(
            label,
            style: AppTextStyles.labelSm.copyWith(
              color: foregroundColor,
            ),
          ),
        ],
      ),
    );
  }
}
