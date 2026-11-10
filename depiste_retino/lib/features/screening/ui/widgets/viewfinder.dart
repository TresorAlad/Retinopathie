import 'dart:ui';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:material_symbols_icons/symbols.dart';
import '../../../../core/constants/app_dimens.dart';
import '../../../../core/constants/app_strings.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_shadows.dart';
import '../../../../core/theme/app_text_styles.dart';
import '../../logic/camera_manager.dart';
import 'camera_control_button.dart';
import 'camera_permission_view.dart';
import 'common/inner_shadow.dart';
import 'viewfinder_overlay_painter.dart';

/// Viseur de caméra oculaire avec aperçu direct, masque d'occultation et repères bilatéraux.
class Viewfinder extends StatefulWidget {
  final CameraManager camera;

  const Viewfinder({super.key, required this.camera});

  @override
  State<Viewfinder> createState() => _ViewfinderState();
}

class _ViewfinderState extends State<Viewfinder>
    with SingleTickerProviderStateMixin {
  late final AnimationController _pulseController;
  late final Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    );

    _pulseAnimation = TweenSequence<double>([
      TweenSequenceItem(
        tween: Tween<double>(begin: 1.0, end: 0.5)
            .chain(CurveTween(curve: const Cubic(0.4, 0.0, 0.6, 1.0))),
        weight: 50.0,
      ),
      TweenSequenceItem(
        tween: Tween<double>(begin: 0.5, end: 1.0)
            .chain(CurveTween(curve: const Cubic(0.4, 0.0, 0.6, 1.0))),
        weight: 50.0,
      ),
    ]).animate(_pulseController);

    _pulseController.repeat();
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final camera = widget.camera;

    return AspectRatio(
      aspectRatio: 4 / 3,
      child: InnerShadow(
        borderRadius: BorderRadius.circular(AppDimens.innerRadius),
        child: Container(
          decoration: BoxDecoration(
            color: AppColors.surfaceContainer,
            borderRadius: BorderRadius.circular(AppDimens.innerRadius),
          ),
          child: ClipRRect(
            borderRadius: BorderRadius.circular(AppDimens.innerRadius),
            child: Stack(
              fit: StackFit.expand,
              children: [
                // Couche 1 : Aperçu caméra réel (ou dégradé de secours)
                if (camera.isInitialized && camera.controller != null)
                  _buildCameraPreview(camera.controller!)
                else
                  _buildFallbackGradient(),

                // Si permission refusée ou erreur matérielle
                if (camera.isPermissionDenied || camera.hasCameraError)
                  CameraPermissionView(
                    isPermanentlyDenied: camera.isPermanentlyDenied,
                    hasCameraError: camera.hasCameraError,
                    onAction: camera.requestPermissionOrOpenSettings,
                  )
                else ...[
                  // Couche 2 : Masque sombre autour de la pilule centrale
                  LayoutBuilder(
                    builder: (context, constraints) {
                      return CustomPaint(
                        size: Size(constraints.maxWidth, constraints.maxHeight),
                        painter: _ViewfinderMaskPainter(),
                      );
                    },
                  ),

                  // Couche 3 : Pilule-guide vectorielle animée
                  LayoutBuilder(
                    builder: (context, constraints) {
                      final guideWidth = constraints.maxWidth * 0.88;
                      const guideHeight = 144.0;

                      return Center(
                        child: SizedBox(
                          width: guideWidth,
                          height: guideHeight,
                          child: AnimatedBuilder(
                            animation: _pulseAnimation,
                            builder: (context, _) {
                              final opacity = MediaQuery.disableAnimationsOf(context)
                                  ? 1.0
                                  : _pulseAnimation.value;
                              return CustomPaint(
                                painter: ViewfinderOverlayPainter(
                                  pulseOpacity: opacity,
                                ),
                              );
                            },
                          ),
                        ),
                      );
                    },
                  ),

                  // Couche 4 : Texte et icône au centre de la pilule
                  Center(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(AppDimens.innerRadius),
                      child: BackdropFilter(
                        filter: ImageFilter.blur(sigmaX: 2.0, sigmaY: 2.0),
                        child: Padding(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 16.0,
                            vertical: 8.0,
                          ),
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const Icon(
                                Symbols.visibility,
                                size: 26.0,
                                color: AppColors.surfaceBright,
                                shadows: [
                                  Shadow(
                                    offset: Offset(0, 4),
                                    blurRadius: 3.0,
                                    color: Color(0x12000000),
                                  ),
                                  Shadow(
                                    offset: Offset(0, 2),
                                    blurRadius: 2.0,
                                    color: Color(0x0F000000),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 2.0),
                              Text(
                                AppStrings.guideText,
                                textAlign: TextAlign.center,
                                style: AppTextStyles.labelSm.copyWith(
                                  fontWeight: FontWeight.w700,
                                  letterSpacing: 0.025 * 12.0,
                                  color: AppColors.surfaceBright,
                                  shadows: const [
                                    Shadow(
                                      offset: Offset(0, 1),
                                      blurRadius: 1.0,
                                      color: Color(0x0D000000),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),

                  // Boutons de contrôle dans le viseur
                  // Flash / Torche (en haut à gauche, caméra arrière uniquement)
                  if (camera.hasFlashSupport)
                    Positioned(
                      top: 12.0,
                      left: 12.0,
                      child: CameraControlButton(
                        icon: camera.isFlashOn ? Symbols.flash_on : Symbols.flash_off,
                        semanticsLabel: camera.isFlashOn
                            ? AppStrings.semFlashOff
                            : AppStrings.semFlashOn,
                        onTap: camera.toggleFlash,
                      ),
                    ),

                  // Bascule de caméra (en haut à droite, si >= 2 caméras)
                  if (camera.canSwitchCamera)
                    Positioned(
                      top: 12.0,
                      right: 12.0,
                      child: CameraControlButton(
                        icon: Symbols.cameraswitch,
                        semanticsLabel: AppStrings.semSwitchCamera,
                        onTap: camera.switchCamera,
                      ),
                    ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// Aperçu caméra recadré en "cover" sans déformation géométrique
  Widget _buildCameraPreview(CameraController controller) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final previewSize = controller.value.previewSize;
        if (previewSize == null) return _buildFallbackGradient();

        // En mode portrait, inverser largeur et hauteur de la résolution du capteur
        final double previewWidth = previewSize.height;
        final double previewHeight = previewSize.width;

        final double scaleX = constraints.maxWidth / previewWidth;
        final double scaleY = constraints.maxHeight / previewHeight;
        final double scale = (scaleX > scaleY) ? scaleX : scaleY;

        return Center(
          child: SizedBox(
            width: previewWidth * scale,
            height: previewHeight * scale,
            child: CameraPreview(controller),
          ),
        );
      },
    );
  }

  /// Dégradé vertical de secours si la caméra n'est pas encore prête
  Widget _buildFallbackGradient() {
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topCenter,
          end: Alignment.bottomCenter,
          colors: [
            AppColors.viewerGradTop,
            AppColors.viewerGradMid,
            AppColors.viewerGradBottom,
          ],
        ),
      ),
    );
  }
}

/// Peintre du masque sombre entourant la pilule de cadrage
class _ViewfinderMaskPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final guideWidth = size.width * 0.88;
    const guideHeight = 144.0;
    final guideLeft = (size.width - guideWidth) / 2;
    final guideTop = (size.height - guideHeight) / 2;

    final outerRect = Rect.fromLTWH(0, 0, size.width, size.height);
    final innerRRect = RRect.fromRectAndRadius(
      Rect.fromLTWH(guideLeft, guideTop, guideWidth, guideHeight),
      const Radius.circular(72.0),
    );

    final path = Path.combine(
      PathOperation.difference,
      Path()..addRect(outerRect),
      Path()..addRRect(innerRRect),
    );

    final paint = Paint()
      ..color = AppColors.viewerScrim
      ..style = PaintingStyle.fill;

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
