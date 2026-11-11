import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';
import 'package:depiste_retino/core/constants/app_dimens.dart';
import 'package:depiste_retino/core/constants/app_strings.dart';
import 'package:depiste_retino/core/theme/app_colors.dart';
import 'package:depiste_retino/core/theme/app_text_styles.dart';

import '../../logic/screening_controller.dart';
import 'common/app_card.dart';
import 'common/status_badge.dart';
import 'shutter_button.dart';
import 'viewfinder.dart';

class CaptureCard extends StatelessWidget {
  final ScreeningController controller;

  const CaptureCard({super.key, required this.controller});

  @override
  Widget build(BuildContext context) {
    return AppCard(
      clipBehavior: Clip.antiAlias,
      child: Column(
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Container(
                width: 32.0,
                height: 32.0,
                decoration: const BoxDecoration(
                  color: AppColors.primaryFixed,
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Symbols.photo_camera,
                  size: 18.0,
                  color: AppColors.primary,
                ),
              ),
              const SizedBox(width: 8.0),
              Expanded(
                child: Text(
                  AppStrings.captureTitle,
                  style: AppTextStyles.labelMd.copyWith(
                    fontWeight: FontWeight.w600,
                    color: AppColors.onSurface,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: 8.0),
              const StatusBadge(
                label: AppStrings.lightBadge,
                backgroundColor: AppColors.surfaceContainer,
                foregroundColor: AppColors.onSurfaceVariant,
                padding: EdgeInsets.symmetric(horizontal: 10.0, vertical: 4.0),
                icon: Icon(
                  Symbols.wb_sunny,
                  size: 15.0,
                  color: AppColors.tertiary,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12.0),
          Viewfinder(camera: controller.camera),
          const SizedBox(height: 14.0),
          Container(
            decoration: BoxDecoration(
              color: AppColors.surfaceContainerLow,
              borderRadius: BorderRadius.circular(AppDimens.pillRadius),
            ),
            padding: const EdgeInsets.symmetric(
              horizontal: 12.0,
              vertical: 8.0,
            ),
            child: Row(
              children: [
                Container(
                  width: 28.0,
                  height: 28.0,
                  decoration: const BoxDecoration(
                    color: AppColors.tertiaryFixed,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Symbols.light_mode,
                    size: 16.0,
                    color: AppColors.onTertiaryFixed,
                  ),
                ),
                const SizedBox(width: 10.0),
                Expanded(
                  child: Text(
                    AppStrings.instruction,
                    style: AppTextStyles.bodySm.copyWith(
                      color: AppColors.onSurfaceVariant,
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20.0),
          Padding(
            padding: const EdgeInsets.only(bottom: 8.0),
            child: ShutterButton(
              onTap: controller.takePhoto,
              isCapturing: controller.isCapturing,
              isEnabled:
                  controller.camera.isInitialized && !controller.isSending,
            ),
          ),
        ],
      ),
    );
  }
}
