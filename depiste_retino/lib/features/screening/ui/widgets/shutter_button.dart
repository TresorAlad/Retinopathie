import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';
import '../../../../core/constants/app_strings.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_shadows.dart';
import '../../../../core/theme/app_text_styles.dart';
import 'common/inner_shadow.dart';
import 'common/pulse_animations.dart';

/// Bouton d'obturation circulaire tactile avec anneau de pulsation et retour haptique visuel.
class ShutterButton extends StatefulWidget {
  final VoidCallback onTap;
  final bool isCapturing;
  final bool isEnabled;

  const ShutterButton({
    super.key,
    required this.onTap,
    this.isCapturing = false,
    this.isEnabled = true,
  });

  @override
  State<ShutterButton> createState() => _ShutterButtonState();
}

class _ShutterButtonState extends State<ShutterButton> {
  bool _isPressed = false;

  void _handleTapDown(TapDownDetails _) {
    if (widget.isEnabled && !widget.isCapturing) {
      setState(() => _isPressed = true);
    }
  }

  void _handleTapUp(TapUpDetails _) {
    if (_isPressed) {
      setState(() => _isPressed = false);
    }
  }

  void _handleTapCancel() {
    if (_isPressed) {
      setState(() => _isPressed = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final effectiveEnabled = widget.isEnabled && !widget.isCapturing;

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Semantics(
          label: AppStrings.semShutter,
          button: true,
          enabled: effectiveEnabled,
          child: Stack(
            alignment: Alignment.center,
            clipBehavior: Clip.none,
            children: [
              // Anneau pulsant décoratif (affiché uniquement quand le bouton est actif)
              if (effectiveEnabled)
                const Positioned(
                  child: PingAnimation(
                    child: SizedBox(
                      width: 96.0,
                      height: 96.0,
                      child: DecoratedBox(
                        decoration: BoxDecoration(
                          color: AppColors.ringPing,
                          shape: BoxShape.circle,
                        ),
                      ),
                    ),
                  ),
                ),

              // Bouton d'obturation tactile
              GestureDetector(
                behavior: HitTestBehavior.opaque,
                onTap: effectiveEnabled ? widget.onTap : null,
                onTapDown: _handleTapDown,
                onTapUp: _handleTapUp,
                onTapCancel: _handleTapCancel,
                child: AnimatedScale(
                  scale: _isPressed ? 0.95 : 1.0,
                  duration: const Duration(milliseconds: 150),
                  curve: Curves.easeOutCubic,
                  child: Opacity(
                    opacity: effectiveEnabled ? 1.0 : 0.5,
                    child: Container(
                      width: 80.0,
                      height: 80.0,
                      decoration: const BoxDecoration(
                        color: AppColors.primaryContainer,
                        shape: BoxShape.circle,
                        boxShadow: AppShadows.shutter,
                      ),
                      child: Center(
                        child: InnerShadow(
                          borderRadius: BorderRadius.circular(32.0),
                          child: AnimatedContainer(
                            duration: const Duration(milliseconds: 150),
                            width: 64.0,
                            height: 64.0,
                            decoration: BoxDecoration(
                              color: _isPressed
                                  ? AppColors.primaryFixed
                                  : AppColors.surfaceContainerLowest,
                              shape: BoxShape.circle,
                            ),
                            child: Center(
                              child: widget.isCapturing
                                  ? const SizedBox(
                                      width: 28.0,
                                      height: 28.0,
                                      child: CircularProgressIndicator(
                                        strokeWidth: 3.0,
                                        valueColor: AlwaysStoppedAnimation<Color>(
                                          AppColors.primary,
                                        ),
                                      ),
                                    )
                                  : const Icon(
                                      Symbols.photo_camera,
                                      size: 32.0,
                                      color: AppColors.primary,
                                    ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 8.0),

        // Libellé sous le bouton
        Text(
          AppStrings.shutterLabel,
          style: AppTextStyles.labelSm.copyWith(
            fontWeight: FontWeight.w500,
            color: AppColors.onSurfaceVariant,
          ),
        ),
      ],
    );
  }
}
