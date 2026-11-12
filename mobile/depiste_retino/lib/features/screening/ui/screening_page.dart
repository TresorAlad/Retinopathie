import 'dart:async';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../core/constants/app_dimens.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/utils/scroll_utils.dart';
import '../logic/screening_controller.dart';
import 'widgets/app_header.dart';
import 'widgets/capture_card.dart';
import 'widgets/disclaimer_card.dart';
import 'widgets/error_banner.dart';
import 'widgets/intro_section.dart';
import 'widgets/loading_card.dart';
import 'widgets/patient_info_card.dart';
import 'widgets/preview_card.dart';
import 'widgets/results_section.dart';

/// Page principale unique de l'application Dépiste Retino.
/// Organise le défilement fluide, gère les clés d'ancrage et les requêtes de défilement automatique.
class ScreeningPage extends StatefulWidget {
  const ScreeningPage({super.key});

  @override
  State<ScreeningPage> createState() => _ScreeningPageState();
}

class _ScreeningPageState extends State<ScreeningPage> {
  final ScrollController _scrollController = ScrollController();
  StreamSubscription<ScrollTarget>? _scrollSubscription;

  // Clés globales pour les cibles de défilement automatique
  final GlobalKey _captureKey = GlobalKey();
  final GlobalKey _previewKey = GlobalKey();
  final GlobalKey _loadingKey = GlobalKey();
  final GlobalKey _resultsKey = GlobalKey();
  final GlobalKey _nomKey = GlobalKey();
  final GlobalKey _prenomKey = GlobalKey();
  final GlobalKey _ageKey = GlobalKey();
  final GlobalKey _sexeKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final controller = context.read<ScreeningController>();
      _scrollSubscription = controller.scrollRequests.listen(_handleScrollRequest);
    });
  }

  void _handleScrollRequest(ScrollTarget target) {
    if (!mounted) return;

    GlobalKey targetKey;
    bool alignCenter = false;

    switch (target) {
      case ScrollTarget.capture:
        targetKey = _captureKey;
        break;
      case ScrollTarget.preview:
        targetKey = _previewKey;
        alignCenter = true;
        break;
      case ScrollTarget.loading:
        targetKey = _loadingKey;
        break;
      case ScrollTarget.results:
        targetKey = _resultsKey;
        break;
      case ScrollTarget.firstInvalidField:
        final controller = context.read<ScreeningController>();
        final errors = controller.fieldErrors;
        if (errors.containsKey('nom')) {
          targetKey = _nomKey;
        } else if (errors.containsKey('prenom')) {
          targetKey = _prenomKey;
        } else if (errors.containsKey('age')) {
          targetKey = _ageKey;
        } else {
          targetKey = _sexeKey;
        }
        break;
    }

    // Temporisation minimale pour laisser le temps au framework de construire le widget
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ScrollUtils.scrollToTarget(
        scrollController: _scrollController,
        targetKey: targetKey,
        context: context,
        alignCenter: alignCenter,
      );
    });
  }

  @override
  void dispose() {
    _scrollSubscription?.cancel();
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final statusBarHeight = MediaQuery.of(context).padding.top;
    final bottomSafeArea = MediaQuery.of(context).padding.bottom;

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: Stack(
        children: [
          // 1. Contenu défilant fluide
          Consumer<ScreeningController>(
            builder: (context, controller, _) {
              return SingleChildScrollView(
                controller: _scrollController,
                padding: EdgeInsets.only(
                  top: AppDimens.headerHeight + statusBarHeight + 16.0,
                  left: AppDimens.screenMargin,
                  right: AppDimens.screenMargin,
                  bottom: 32.0 + bottomSafeArea,
                ),
                child: Center(
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(
                      maxWidth: AppDimens.maxContentWidth,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Section d'introduction bienveillante
                        const IntroSection(),
                        const SizedBox(height: AppDimens.blockSpacing),

                        // Carte formulaire patient
                        PatientInfoCard(
                          controller: controller,
                          nomKey: _nomKey,
                          prenomKey: _prenomKey,
                          ageKey: _ageKey,
                          sexeKey: _sexeKey,
                        ),
                        const SizedBox(height: AppDimens.blockSpacing),

                        // Carte de capture avec viseur guidé
                        Container(
                          key: _captureKey,
                          child: CaptureCard(controller: controller),
                        ),

                        // Carte d'aperçu du cliché instantané (si photo prise)
                        if (controller.photoBytes != null) ...[
                          const SizedBox(height: AppDimens.blockSpacing),
                          Container(
                            key: _previewKey,
                            child: PreviewCard(controller: controller),
                          ),
                        ],

                        // Carte d'analyse en cours ou bannière d'erreur
                        if (controller.isSending) ...[
                          const SizedBox(height: AppDimens.blockSpacing),
                          Container(
                            key: _loadingKey,
                            child: const LoadingCard(),
                          ),
                        ] else if (controller.error != null) ...[
                          const SizedBox(height: AppDimens.blockSpacing),
                          ErrorBanner(error: controller.error!),
                        ],

                        // Section des résultats reçus de l'API
                        if (controller.result != null) ...[
                          const SizedBox(height: AppDimens.blockSpacing),
                          Container(
                            key: _resultsKey,
                            child: ResultsSection(result: controller.result!),
                          ),
                        ],

                        // Bloc d'avertissement médical (toujours visible)
                        const SizedBox(height: AppDimens.blockSpacing),
                        const DisclaimerCard(),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),

          // 2. En-tête supérieur fixe avec flou d'arrière-plan
          const Positioned(
            top: 0,
            left: 0,
            right: 0,
            child: AppHeader(),
          ),
        ],
      ),
    );
  }
}
