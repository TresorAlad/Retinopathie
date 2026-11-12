import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';
import 'package:depiste_retino/core/constants/app_dimens.dart';
import 'package:depiste_retino/core/constants/app_strings.dart';
import 'package:depiste_retino/core/theme/app_colors.dart';
import 'package:depiste_retino/core/theme/app_text_styles.dart';

import '../../logic/screening_controller.dart';
import 'common/app_card.dart';
import 'common/status_badge.dart';
import 'pill_text_field.dart';

class PatientInfoCard extends StatelessWidget {
  final ScreeningController controller;
  final GlobalKey? nomKey;
  final GlobalKey? prenomKey;
  final GlobalKey? ageKey;
  final GlobalKey? sexeKey;

  const PatientInfoCard({
    super.key,
    required this.controller,
    this.nomKey,
    this.prenomKey,
    this.ageKey,
    this.sexeKey,
  });

  @override
  Widget build(BuildContext context) {
    final errors = controller.fieldErrors;

    return AppCard(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
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
                  Symbols.badge,
                  size: 18.0,
                  color: AppColors.primary,
                ),
              ),
              const SizedBox(width: 10.0),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      AppStrings.infoTitle,
                      style: AppTextStyles.labelLg.copyWith(
                        fontWeight: FontWeight.w700,
                        color: AppColors.onSurface,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    Text(
                      AppStrings.infoSubtitle,
                      style: AppTextStyles.bodySm.copyWith(
                        color: AppColors.onSurfaceVariant,
                      ),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 8.0),
              const StatusBadge(
                label: AppStrings.confidential,
                backgroundColor: AppColors.surfaceContainer,
                foregroundColor: AppColors.onSurfaceVariant,
                padding: EdgeInsets.symmetric(horizontal: 10.0, vertical: 4.0),
                icon: Icon(
                  Symbols.lock,
                  size: 14.0,
                  color: AppColors.secondary,
                ),
              ),
            ],
          ),
          const SizedBox(height: AppDimens.cardSpacing),
          Column(
            children: [
              Container(
                key: nomKey,
                child: PillTextField(
                  label: AppStrings.labelNom,
                  hintText: AppStrings.hintNom,
                  controller: controller.nomController,
                  errorMessage: errors['nom'],
                  textCapitalization: TextCapitalization.words,
                  textInputAction: TextInputAction.next,
                  maxLength: 60,
                ),
              ),
              const SizedBox(height: AppDimens.fieldSpacing),
              Container(
                key: prenomKey,
                child: PillTextField(
                  label: AppStrings.labelPrenom,
                  hintText: AppStrings.hintPrenom,
                  controller: controller.prenomController,
                  errorMessage: errors['prenom'],
                  textCapitalization: TextCapitalization.words,
                  textInputAction: TextInputAction.next,
                  maxLength: 60,
                ),
              ),
              const SizedBox(height: AppDimens.fieldSpacing),
              Container(
                key: ageKey,
                child: PillTextField(
                  label: AppStrings.labelAge,
                  hintText: AppStrings.hintAge,
                  controller: controller.ageController,
                  errorMessage: errors['age'],
                  keyboardType: TextInputType.number,
                  textInputAction: TextInputAction.next,
                  maxLength: 3,
                ),
              ),
              const SizedBox(height: AppDimens.fieldSpacing),
              Container(
                key: sexeKey,
                child: PillDropdownField(
                  label: AppStrings.labelSexe,
                  hintText: AppStrings.hintSexe,
                  value: controller.sexe,
                  errorMessage: errors['sexe'],
                  items: const [
                    DropdownMenuItem(
                      value: 'femme',
                      child: Text(AppStrings.sexeFemme),
                    ),
                    DropdownMenuItem(
                      value: 'homme',
                      child: Text(AppStrings.sexeHomme),
                    ),
                    DropdownMenuItem(
                      value: 'autre',
                      child: Text(AppStrings.sexeAutre),
                    ),
                  ],
                  onChanged: controller.setSexe,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
