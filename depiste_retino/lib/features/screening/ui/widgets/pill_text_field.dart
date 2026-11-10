import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';
import '../../../../core/constants/app_dimens.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_text_styles.dart';

/// Champ textuel au profil pilule avec prise en charge de l'anneau de focus et des erreurs de validation.
class PillTextField extends StatefulWidget {
  final String label;
  final String hintText;
  final TextEditingController? controller;
  final TextInputType keyboardType;
  final TextCapitalization textCapitalization;
  final TextInputAction textInputAction;
  final String? errorMessage;
  final ValueChanged<String>? onChanged;
  final int? maxLength;

  const PillTextField({
    super.key,
    required this.label,
    required this.hintText,
    this.controller,
    this.keyboardType = TextInputType.text,
    this.textCapitalization = TextCapitalization.words,
    this.textInputAction = TextInputAction.next,
    this.errorMessage,
    this.onChanged,
    this.maxLength,
  });

  @override
  State<PillTextField> createState() => _PillTextFieldState();
}

class _PillTextFieldState extends State<PillTextField> {
  final FocusNode _focusNode = FocusNode();
  bool _isFocused = false;

  @override
  void initState() {
    super.initState();
    _focusNode.addListener(() {
      setState(() {
        _isFocused = _focusNode.hasFocus;
      });
    });
  }

  @override
  void dispose() {
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final hasError = widget.errorMessage != null && widget.errorMessage!.isNotEmpty;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        // Libellé supérieur
        Text(
          widget.label,
          style: AppTextStyles.labelSm.copyWith(
            fontWeight: FontWeight.w600,
            color: AppColors.onSurface,
          ),
        ),
        const SizedBox(height: AppDimens.labelSpacing),

        // Boîtier de saisie
        AnimatedContainer(
          duration: const Duration(milliseconds: 150),
          constraints: const BoxConstraints(minHeight: AppDimens.inputMinHeight),
          decoration: BoxDecoration(
            color: AppColors.surfaceContainerLow,
            borderRadius: BorderRadius.circular(AppDimens.inputRadius),
            border: Border.all(
              color: hasError ? AppColors.error : AppColors.inputBorder,
              width: hasError ? 1.5 : 1.0,
            ),
            boxShadow: (_isFocused && !hasError)
                ? const [
                    BoxShadow(
                      color: AppColors.focusRing,
                      spreadRadius: 2.0,
                      blurRadius: 0.0,
                    ),
                  ]
                : const [],
          ),
          padding: const EdgeInsets.symmetric(horizontal: 16.0),
          alignment: Alignment.centerLeft,
          child: TextField(
            controller: widget.controller,
            focusNode: _focusNode,
            keyboardType: widget.keyboardType,
            textCapitalization: widget.textCapitalization,
            textInputAction: widget.textInputAction,
            maxLength: widget.maxLength,
            cursorColor: AppColors.onSurface,
            style: AppTextStyles.bodyMd.copyWith(color: AppColors.onSurface),
            decoration: InputDecoration(
              isDense: true,
              border: InputBorder.none,
              counterText: '',
              hintText: widget.hintText,
              hintStyle: AppTextStyles.bodyMd.copyWith(color: AppColors.inputHint),
              contentPadding: const EdgeInsets.symmetric(vertical: 14.0),
            ),
            onChanged: widget.onChanged,
          ),
        ),

        // Message d'erreur
        if (hasError) ...[
          const SizedBox(height: 6.0),
          Padding(
            padding: const EdgeInsets.only(left: 8.0),
            child: Text(
              widget.errorMessage!,
              style: AppTextStyles.bodySm.copyWith(
                color: AppColors.error,
              ),
            ),
          ),
        ],
      ],
    );
  }
}

/// Variante liste déroulante pilule pour la sélection du sexe.
class PillDropdownField extends StatelessWidget {
  final String label;
  final String hintText;
  final String? value;
  final List<DropdownMenuItem<String>> items;
  final ValueChanged<String?>? onChanged;
  final String? errorMessage;

  const PillDropdownField({
    super.key,
    required this.label,
    required this.hintText,
    required this.value,
    required this.items,
    required this.onChanged,
    this.errorMessage,
  });

  @override
  Widget build(BuildContext context) {
    final hasError = errorMessage != null && errorMessage!.isNotEmpty;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        // Libellé
        Text(
          label,
          style: AppTextStyles.labelSm.copyWith(
            fontWeight: FontWeight.w600,
            color: AppColors.onSurface,
          ),
        ),
        const SizedBox(height: AppDimens.labelSpacing),

        // Conteneur sélecteur
        Container(
          constraints: const BoxConstraints(minHeight: AppDimens.inputMinHeight),
          decoration: BoxDecoration(
            color: AppColors.surfaceContainerLow,
            borderRadius: BorderRadius.circular(AppDimens.inputRadius),
            border: Border.all(
              color: hasError ? AppColors.error : AppColors.inputBorder,
              width: hasError ? 1.5 : 1.0,
            ),
          ),
          padding: const EdgeInsets.only(left: 16.0, right: 12.0),
          alignment: Alignment.centerLeft,
          child: DropdownButtonHideUnderline(
            child: DropdownButton<String>(
              value: value,
              isExpanded: true,
              hint: Text(
                hintText,
                style: AppTextStyles.bodyMd.copyWith(color: AppColors.inputHint),
              ),
              icon: const Icon(
                Symbols.expand_more,
                size: 20.0,
                color: AppColors.onSurfaceVariant,
              ),
              dropdownColor: AppColors.surfaceContainerLowest,
              borderRadius: BorderRadius.circular(AppDimens.innerRadius),
              style: AppTextStyles.bodyMd.copyWith(color: AppColors.onSurface),
              items: items,
              onChanged: onChanged,
            ),
          ),
        ),

        // Erreur
        if (hasError) ...[
          const SizedBox(height: 6.0),
          Padding(
            padding: const EdgeInsets.only(left: 8.0),
            child: Text(
              errorMessage!,
              style: AppTextStyles.bodySm.copyWith(
                color: AppColors.error,
              ),
            ),
          ),
        ],
      ],
    );
  }
}
