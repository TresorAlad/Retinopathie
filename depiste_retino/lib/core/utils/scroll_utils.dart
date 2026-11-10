import 'package:flutter/material.dart';
import '../constants/app_dimens.dart';

/// Cibles de défilement automatique vers les sections de l'écran principal.
enum ScrollTarget {
  capture,
  preview,
  loading,
  results,
  firstInvalidField,
}

/// Utilitaires de défilement animé compensant la hauteur de l'en-tête fixe.
abstract final class ScrollUtils {
  /// Défilement fluide vers une cible donnée en tenant compte de l'en-tête supérieur fixe
  static Future<void> scrollToTarget({
    required ScrollController scrollController,
    required GlobalKey targetKey,
    required BuildContext context,
    bool alignCenter = false,
  }) async {
    final targetContext = targetKey.currentContext;
    if (targetContext == null || !scrollController.hasClients) return;

    final renderBox = targetContext.findRenderObject() as RenderBox?;
    if (renderBox == null) return;

    // Calcul de la hauteur de l'en-tête fixe + barre système
    final statusBarHeight = MediaQuery.of(context).padding.top;
    final totalHeaderHeight = AppDimens.headerHeight + statusBarHeight;

    // Position verticale absolue de l'élément dans le défilement
    final position = renderBox.localToGlobal(Offset.zero);
    final currentOffset = scrollController.offset;
    final viewportHeight = MediaQuery.of(context).size.height;

    double targetOffset;
    if (alignCenter) {
      // Alignement centré dans la zone visible utile
      final itemHeight = renderBox.size.height;
      targetOffset = currentOffset +
          position.dy -
          totalHeaderHeight -
          (viewportHeight - totalHeaderHeight - itemHeight) / 2;
    } else {
      // Alignement en haut avec marge de dégagement de 8px
      targetOffset = currentOffset + position.dy - totalHeaderHeight - 8.0;
    }

    final clampedOffset = targetOffset.clamp(
      0.0,
      scrollController.position.maxScrollExtent,
    );

    await scrollController.animateTo(
      clampedOffset,
      duration: const Duration(milliseconds: 400),
      curve: Curves.easeInOut,
    );
  }
}
