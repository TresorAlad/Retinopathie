import 'package:flutter/material.dart';

/// Décorateur d'ombre interne concave pour les conteneurs arrondis.
class InnerShadow extends StatelessWidget {
  final Widget child;
  final Color shadowColor;
  final double blurRadius;
  final Offset offset;
  final BorderRadius borderRadius;

  const InnerShadow({
    super.key,
    required this.child,
    this.shadowColor = const Color(0x0D000000),
    this.blurRadius = 4.0,
    this.offset = const Offset(0, 2),
    this.borderRadius = BorderRadius.zero,
  });

  @override
  Widget build(BuildContext context) {
    return ClipRRect(
      borderRadius: borderRadius,
      child: Stack(
        children: [
          child,
          Positioned.fill(
            child: CustomPaint(
              painter: _InnerShadowPainter(
                shadowColor: shadowColor,
                blurRadius: blurRadius,
                offset: offset,
                borderRadius: borderRadius,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _InnerShadowPainter extends CustomPainter {
  final Color shadowColor;
  final double blurRadius;
  final Offset offset;
  final BorderRadius borderRadius;

  _InnerShadowPainter({
    required this.shadowColor,
    required this.blurRadius,
    required this.offset,
    required this.borderRadius,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final rect = Offset.zero & size;
    final rrect = borderRadius.toRRect(rect);

    final outerRect = rect.inflate(blurRadius + offset.distance + 10.0);
    final outerRRect = BorderRadius.circular(100.0).toRRect(outerRect);

    final shadowPath = Path()
      ..addRRect(outerRRect)
      ..addRRect(rrect)
      ..fillType = PathFillType.evenOdd;

    final paint = Paint()
      ..color = shadowColor
      ..maskFilter = MaskFilter.blur(BlurStyle.normal, blurRadius);

    canvas.save();
    canvas.clipRRect(rrect);
    canvas.translate(offset.dx, offset.dy);
    canvas.drawPath(shadowPath, paint);
    canvas.restore();
  }

  @override
  bool shouldRepaint(covariant _InnerShadowPainter oldDelegate) {
    return oldDelegate.shadowColor != shadowColor ||
        oldDelegate.blurRadius != blurRadius ||
        oldDelegate.offset != offset ||
        oldDelegate.borderRadius != borderRadius;
  }
}
