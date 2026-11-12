import '../constants/app_strings.dart';

/// Utilitaires de validation pour les 4 champs obligatoires du formulaire patient.
abstract final class Validators {
  /// Valide le champ Nom : obligatoire, non vide après trim, max 60 caractères.
  static String? validateNom(String? value) {
    if (value == null || value.trim().isEmpty) {
      return AppStrings.errRequired;
    }
    if (value.trim().length > 60) {
      return '60 caractères maximum';
    }
    return null;
  }

  /// Valide le champ Prénom : obligatoire, non vide après trim, max 60 caractères.
  static String? validatePrenom(String? value) {
    if (value == null || value.trim().isEmpty) {
      return AppStrings.errRequired;
    }
    if (value.trim().length > 60) {
      return '60 caractères maximum';
    }
    return null;
  }

  /// Valide le champ Âge : obligatoire, entier valide entre 1 et 120.
  static String? validateAge(String? value) {
    if (value == null || value.trim().isEmpty) {
      return AppStrings.errRequired;
    }
    final age = int.tryParse(value.trim());
    if (age == null || age < 1 || age > 120) {
      return AppStrings.errAge;
    }
    return null;
  }

  /// Valide le champ Sexe : obligatoire, doit être sélectionné.
  static String? validateSexe(String? value) {
    if (value == null || value.trim().isEmpty) {
      return AppStrings.errSexe;
    }
    return null;
  }
}
