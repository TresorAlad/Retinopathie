import 'package:flutter/foundation.dart';
import 'package:image/image.dart' as img;

/// Utilitaires de traitement d'image exécutés en arrière-plan dans des isolates.
/// Garantit qu'aucun traitement lourd ne bloque le fil d'exécution de l'interface utilisateur.
abstract final class ImageUtils {
  /// Décode les octets bruts capturés par la caméra, corrige l'orientation EXIF
  /// et ré-encode l'image au format PNG en mémoire.
  static Future<Uint8List> convertToPng(Uint8List rawBytes) async {
    return compute(_processImageToPng, rawBytes);
  }

  /// Fonction isolée de conversion en PNG avec préservation d'orientation.
  static Uint8List _processImageToPng(Uint8List bytes) {
    // Décodage de l'image brute capturée
    final image = img.decodeImage(bytes);
    if (image == null) {
      throw Exception('Impossible de décoder l\'image capturée');
    }

    // Correction de l'orientation selon les métadonnées EXIF sans recadrage ni rotation superflue
    final orientedImage = img.bakeOrientation(image);

    // Encodage strict au format PNG
    final pngBytes = img.encodePng(orientedImage);
    return Uint8List.fromList(pngBytes);
  }
}
