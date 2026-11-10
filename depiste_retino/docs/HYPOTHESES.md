# Journal des hypothèses techniques — Dépiste Retino

> **À quoi sert ce document :** Consigner les décisions techniques d'exécution prises pour les éventuels cas non explicitement tranchés par les spécifications initiales.  
> **Pour qui :** L'équipe de développement et les auditeurs du code source.

---

## 1. Hypothèses et arbitrages techniques

Conformément à la règle 3 du cahier des charges, toutes les règles et comportements requis ont été rigoureusement spécifiés dans les sections 1 à 15, les annexes A et B et le document de design Stitch.

- **Hypothèse 1 (Format des images capturées) :** La caméra capture initialement un fichier JPEG sur le disque temporaire de l'appareil (format natif universel d'Android et iOS). Ce fichier est immédiatement lu en mémoire puis supprimé du disque avec `File.delete()`. La conversion au format PNG demandée par le cahier des charges est ensuite réalisée intégralement en mémoire dans un isolate d'arrière-plan avec la bibliothèque `image`.
- **Hypothèse 2 (Version SDK Flutter & Dart) :** Le code est rédigé et vérifié pour l'environnement **Flutter 3.47.9 / Dart 3.13.7**. Les API utilisées (`WidgetsBindingObserver`, `SystemChrome`, `CameraController`, `TextScaler.clamp`) sont stables et pleinement compatibles.

En dehors de ces précisions de mise en œuvre, **aucune hypothèse supplémentaire n'a été nécessaire**.
