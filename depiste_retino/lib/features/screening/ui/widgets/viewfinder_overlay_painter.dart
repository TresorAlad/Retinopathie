import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

/// Dessinateur vectoriel pour le schéma de centrage des deux yeux et les repères anatomiques.
/// Tracé défini dans une matrice de référence de 290x144 pixels mise à l'échelle proportionnelle.
class ViewfinderOverlayPainter extends CustomPainter {
  final double pulseOpacity;

  const ViewfinderOverlayPainter({required this.pulseOpacity});

  @override
  void paint(Canvas canvas, Size size) {
    // Calcul de l'échelle et du centrage dans l'espace disponible
    const refWidth = 290.0;
    const refHeight = 144.0;

    final scale = math.min(size.width / refWidth, size.height / refHeight);
    final dx = (size.width - refWidth * scale) / 2;
    final dy = (size.height - refHeight * scale) / 2;

    canvas.save();
    canvas.translate(dx, dy);
    canvas.scale(scale);

    // 1. Grand masque ovale englobant les deux yeux (pointillé 6/6, pulsant)
    final rectPath = Path()
      ..addRRect(
        RRect.fromRectAndRadius(
          const Rect.fromLTWH(6.0, 14.0, 278.0, 116.0),
          const Radius.circular(58.0),
        ),
      );

    final rectPaint = Paint()
      ..color = AppColors.primaryContainer.withValues(alpha: pulseOpacity)
      ..strokeWidth = 2.5
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    _drawDashedPath(
      canvas,
      rectPath,
      rectPaint,
      dashWidth: 6.0,
      dashSpace: 6.0,
    );

    // 2. Repères oeil gauche (centre : 82, 72)
    _drawEyeTarget(canvas, const Offset(82.0, 72.0));

    // 3. Repères oeil droit (centre : 208, 72)
    _drawEyeTarget(canvas, const Offset(208.0, 72.0));

    // 4. Repère pont de nez central
    final nosePaint = Paint()
      ..color = AppColors.whiteStrokeSoft
      ..strokeWidth = 1.5
      ..strokeCap = StrokeCap.round;

    // Ligne verticale
    canvas.drawLine(
      const Offset(145.0, 60.0),
      const Offset(145.0, 84.0),
      nosePaint,
    );

    // Ligne horizontale
    canvas.drawLine(
      const Offset(141.0, 72.0),
      const Offset(149.0, 72.0),
      nosePaint,
    );

    canvas.restore();
  }

  /// Trace les 3 cercles concentriques repérant un oeil
  void _drawEyeTarget(Canvas canvas, Offset center) {
    // Cercle extérieur pointillé rayon 32 (pointillé 4/4)
    final outerPath = Path()
      ..addOval(Rect.fromCircle(center: center, radius: 32.0));

    final outerPaint = Paint()
      ..color = AppColors.whiteStrokeDashed
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;

    _drawDashedPath(
      canvas,
      outerPath,
      outerPaint,
      dashWidth: 4.0,
      dashSpace: 4.0,
    );

    // Cercle intermédiaire plein rayon 12
    final midPaint = Paint()
      ..color = AppColors.whiteStrokeSolid
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;

    canvas.drawCircle(center, 12.0, midPaint);

    // Disque central plein rayon 2.5
    final dotPaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.fill;

    canvas.drawCircle(center, 2.5, dotPaint);
  }

  /// Découpe et trace un chemin pointillé avec PathMetrics
  void _drawDashedPath(
    Canvas canvas,
    Path path,
    Paint paint, {
    required double dashWidth,
    required double dashSpace,
  }) {
    for (final metric in path.computeMetrics()) {
      double distance = 0.0;
      while (distance < metric.length) {
        final length = math.min(dashWidth, metric.length - distance);
        final extract = metric.extractPath(distance, distance + length);
        canvas.drawPath(extract, paint);
        distance += dashWidth + dashSpace;
      }
    }
  }

  @override
  bool shouldRepaint(covariant ViewfinderOverlayPainter oldDelegate) {
    return oldDelegate.pulseOpacity != pulseOpacity;
  }
}
