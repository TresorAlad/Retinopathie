import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'app.dart';
import 'features/screening/logic/screening_controller.dart';

/// Point d'entrée principal de l'application Flutter Dépiste Retino.
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // 1. Verrouillage strict de l'orientation en mode portrait
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
  ]);

  // 2. Configuration des barres système : transparence et icônes sombres
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.dark,
      statusBarBrightness: Brightness.light,
      systemNavigationBarColor: Colors.transparent,
      systemNavigationBarIconBrightness: Brightness.dark,
    ),
  );

  // 3. Injection du contrôleur d'état unique et démarrage de l'arbre de widgets
  runApp(
    ChangeNotifierProvider(
      create: (_) => ScreeningController(),
      child: const DepisteRetinoApp(),
    ),
  );
}
