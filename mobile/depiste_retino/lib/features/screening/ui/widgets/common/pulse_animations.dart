import 'dart:math' as math;

import 'package:flutter/material.dart';

/// Animation de pulsation d'opacité en boucle (animate-pulse Tailwind).
/// Durée 2s, opacité 1.0 -> 0.5 -> 1.0, courbe Cubic(0.4, 0, 0.6, 1).
class PulseAnimation extends StatefulWidget {
  final Widget child;

  const PulseAnimation({super.key, required this.child});

  @override
  State<PulseAnimation> createState() => _PulseAnimationState();
}

class _PulseAnimationState extends State<PulseAnimation>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    );

    _animation = TweenSequence<double>([
      TweenSequenceItem(
        tween: Tween<double>(
          begin: 1.0,
          end: 0.5,
        ).chain(CurveTween(curve: const Cubic(0.4, 0.0, 0.6, 1.0))),
        weight: 50.0,
      ),
      TweenSequenceItem(
        tween: Tween<double>(
          begin: 0.5,
          end: 1.0,
        ).chain(CurveTween(curve: const Cubic(0.4, 0.0, 0.6, 1.0))),
        weight: 50.0,
      ),
    ]).animate(_controller);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _syncAnimation();
  }

  void _syncAnimation() {
    if (MediaQuery.disableAnimationsOf(context)) {
      if (_controller.isAnimating) _controller.stop();
      if (_controller.value != 0.0) _controller.value = 0.0;
    } else if (!_controller.isAnimating) {
      _controller.repeat();
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (MediaQuery.disableAnimationsOf(context)) {
      return widget.child;
    }

    return FadeTransition(opacity: _animation, child: widget.child);
  }
}

/// Animation de propagation en cercle (animate-ping Tailwind pour l'obturateur).
/// Cycle de 1s : de 0% à 75%, échelle 1 -> 2 et opacité 0.75 -> 0. De 75% à 100%, invisible.
class PingAnimation extends StatefulWidget {
  final Widget child;

  const PingAnimation({super.key, required this.child});

  @override
  State<PingAnimation> createState() => _PingAnimationState();
}

class _PingAnimationState extends State<PingAnimation>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final Animation<double> _scaleAnimation;
  late final Animation<double> _opacityAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1000),
    );

    _scaleAnimation = TweenSequence<double>([
      TweenSequenceItem(
        tween: Tween<double>(
          begin: 1.0,
          end: 2.0,
        ).chain(CurveTween(curve: const Cubic(0.0, 0.0, 0.2, 1.0))),
        weight: 75.0,
      ),
      TweenSequenceItem(tween: ConstantTween<double>(2.0), weight: 25.0),
    ]).animate(_controller);

    _opacityAnimation = TweenSequence<double>([
      TweenSequenceItem(
        tween: Tween<double>(
          begin: 0.75,
          end: 0.0,
        ).chain(CurveTween(curve: const Cubic(0.0, 0.0, 0.2, 1.0))),
        weight: 75.0,
      ),
      TweenSequenceItem(tween: ConstantTween<double>(0.0), weight: 25.0),
    ]).animate(_controller);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _syncAnimation();
  }

  void _syncAnimation() {
    if (MediaQuery.disableAnimationsOf(context)) {
      if (_controller.isAnimating) _controller.stop();
      if (_controller.value != 0.0) _controller.value = 0.0;
    } else if (!_controller.isAnimating) {
      _controller.repeat();
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (MediaQuery.disableAnimationsOf(context)) {
      return const SizedBox.shrink();
    }

    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Transform.scale(
          scale: _scaleAnimation.value,
          child: Opacity(opacity: _opacityAnimation.value, child: widget.child),
        );
      },
    );
  }
}

/// Animation de rotation continue (animate-spin Tailwind).
class SpinAnimation extends StatefulWidget {
  final Widget child;

  const SpinAnimation({super.key, required this.child});

  @override
  State<SpinAnimation> createState() => _SpinAnimationState();
}

class _SpinAnimationState extends State<SpinAnimation>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 1),
    );
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _syncAnimation();
  }

  void _syncAnimation() {
    if (MediaQuery.disableAnimationsOf(context)) {
      if (_controller.isAnimating) _controller.stop();
      if (_controller.value != 0.0) _controller.value = 0.0;
    } else if (!_controller.isAnimating) {
      _controller.repeat();
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (MediaQuery.disableAnimationsOf(context)) {
      return widget.child;
    }

    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Transform.rotate(
          angle: _controller.value * 2 * math.pi,
          child: widget.child,
        );
      },
    );
  }
}
