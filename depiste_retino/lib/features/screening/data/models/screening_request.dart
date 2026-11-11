import 'dart:math';
import 'dart:typed_data';

/// Modèle de requête HTTP envoyé à l'API d'analyse.
/// Contient les champs du formulaire et l'image PNG à envoyer en multipart.
final class ScreeningRequest {
  final String nom;
  final String prenom;
  final int age;
  final String sexe;
  final Uint8List imagePng;
  final String patientCode;

  ScreeningRequest({
    required this.nom,
    required this.prenom,
    required this.age,
    required this.sexe,
    required this.imagePng,
    required this.patientCode,
  });

  /// Construit les champs multipart attendus par l'API.
  Map<String, String> toMultipartFields() {
    return {
      'patient_code': patientCode,
      'first_name': prenom.trim(),
      'last_name': nom.trim(),
      'age': age.toString(),
      'sexe': sexe,
    };
  }

  static String generatePatientCode() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    final random = Random.secure();
    return 'M-${List.generate(8, (_) => characters[random.nextInt(characters.length)]).join()}';
  }
}
