/// Modèle de requête HTTP envoyé à l'API d'analyse.
/// Contient les 4 champs obligatoires saisis et l'image PNG encodée en Base64.
final class ScreeningRequest {
  final String nom;
  final String prenom;
  final int age;
  final String sexe;
  final String photoBase64;

  const ScreeningRequest({
    required this.nom,
    required this.prenom,
    required this.age,
    required this.sexe,
    required this.photoBase64,
  });

  /// Convertit la requête au format JSON conforme au cahier des charges.
  /// Les espaces de début et fin sont préalablement supprimés pour le nom et prénom.
  Map<String, dynamic> toJson() {
    return {
      'nom': nom.trim(),
      'prenom': prenom.trim(),
      'age': age,
      'sexe': sexe,
      'photo': photoBase64,
    };
  }
}
