/// Centralisation exhaustive de tous les textes en français de l'application.
/// Aucun texte ne doit être codé en dur dans les composants d'interface.
abstract final class AppStrings {
  static const String appName = 'Dépiste Retino';
  static const String badgeKind = 'Dépistage bienveillant';
  static const String badgeVersion = 'IA Santé v2.4';
  static const String introTitle =
      'Un petit contrôle de vos yeux, en quelques secondes.';
  static const String introText =
      'Positionnez confortablement votre regard. Nous veillons sur la clarté et la vitalité de vos yeux en une seule prise bienveillante.';
  static const String infoTitle = 'Vos informations';
  static const String infoSubtitle = 'Nécessaire pour calibrer l\'analyse';
  static const String confidential = 'Confidentiel';
  static const String labelNom = 'Nom';
  static const String hintNom = 'Votre nom';
  static const String labelPrenom = 'Prénom';
  static const String hintPrenom = 'Votre prénom';
  static const String labelAge = 'Âge';
  static const String hintAge = 'Ex. 45';
  static const String labelSexe = 'Sexe';
  static const String hintSexe = 'Sélectionner...';
  static const String sexeFemme = 'Femme';
  static const String sexeHomme = 'Homme';
  static const String sexeAutre = 'Autre / Non précisé';
  static const String errRequired = 'Ce champ est obligatoire';
  static const String errAge = 'Entrez un âge valide (de 1 à 120)';
  static const String errSexe = 'Veuillez sélectionner une option';
  static const String captureTitle = 'Viseur guidé simultané';
  static const String lightBadge = 'Lumière naturelle';
  static const String guideText = 'Positionnez vos deux yeux dans le cadre';
  static const String instruction =
      'Placez vos yeux face à l\'objectif, à environ 30 cm, dans un endroit bien éclairé.';
  static const String shutterLabel = 'Appuyer pour capturer';
  static const String framingReady = 'Bien cadré';
  static const String autoCaptureLabel = 'Capture automatique';
  static const String autoCaptureHint =
      'Photo prise seule quand le cadrage reste vert 1,5 s';
  static const String referDoctor = 'Consultez un médecin';
  static const String stagePrefix = 'Stade estimé';
  static const String eyeNotDetected = 'Œil non détecté sur l\'image';
  static const String semShutter = 'Prendre la photo';
  static const String semFlashOn = 'Activer le flash';
  static const String semFlashOff = 'Désactiver le flash';
  static const String semSwitchCamera = 'Changer de caméra';
  static const String permDenied =
      'L\'accès à la caméra est nécessaire pour photographier vos yeux.';
  static const String permAllow = 'Autoriser la caméra';
  static const String permSettings = 'Ouvrir les réglages';
  static const String noCamera =
      'Aucune caméra n\'est disponible sur cet appareil.';
  static const String cameraError = 'La caméra n\'a pas pu démarrer.';
  static const String cameraRetry = 'Réessayer';
  static const String semCameraRetry =
      'Réessayer l\'initialisation de la caméra';
  static const String errCapture =
      'La photo n\'a pas pu être prise. Veuillez réessayer.';
  static const String previewTitle = 'Cliché instantané';
  static const String previewBadge = 'Prêt pour l\'analyse';
  static const String retake = 'Reprendre';
  static const String analyze = 'Analyser';
  static const String analyzing = 'Analyse...';
  static const String analyzed = 'Analyse terminée';
  static const String loadingTitle = 'Analyse en cours…';
  static const String step1Title = 'Clarté sclérale bilatérale';
  static const String step1Sub =
      'Recherche d\'indices pigmentaires ou jaunâtres sur les deux yeux.';
  static const String step2Title = 'Reflets et réseau vasculaire';
  static const String step2Sub =
      'Évaluation simultanée de la pâleur et de la fatigue conjonctivale.';
  static const String loadingNote =
      'Synthèse et unification des marqueurs bilatéraux… Élaboration de votre bilan global.';
  static const String resultsTitle = 'Résultats de l\'analyse';
  static const String resultsLabel = 'BILAN GLOBAL UNIFIÉ';
  static const String today = 'Aujourd\'hui à';
  static const String secureBold = 'Résultat enregistré en toute sécurité.';
  static const String secureRest =
      'Données médicales chiffrées de bout en bout sur votre appareil.';
  static const String disclaimer =
      'Ce résultat est une aide au dépistage et ne remplace pas un avis médical. En cas de doute, d\'irritation persistante ou de gêne visuelle, parlez-en à votre ophtalmologue ou médecin traitant.';
  static const String errNoConnection = 'Pas de connexion';
  static const String errServer = 'Serveur indisponible';
  static const String errTimeout =
      'Le délai d\'attente est dépassé. Veuillez reprendre la photo.';
}
