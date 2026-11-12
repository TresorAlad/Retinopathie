import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../../../core/utils/scroll_utils.dart';
import '../../../core/utils/validators.dart';
import '../data/models/screening_request.dart';
import '../data/models/screening_result.dart';
import '../data/screening_api_service.dart';
import '../data/screening_error.dart';
import 'camera_manager.dart';

/// Contrôleur d'état unique de l'écran principal (ChangeNotifier).
/// Centralise l'état du formulaire, la capture photo, l'envoi vers l'API et les requêtes de défilement.
class ScreeningController extends ChangeNotifier {
  // Contrôleurs de formulaire
  final TextEditingController nomController = TextEditingController();
  final TextEditingController prenomController = TextEditingController();
  final TextEditingController ageController = TextEditingController();
  String? _sexe;
  bool _autoCaptureEnabled = false;

  // Erreurs de validation par champ
  final Map<String, String> _fieldErrors = {};

  // Photo et état de prise de vue
  Uint8List? _photoBytes;
  bool _isCapturing = false;

  // États d'envoi et de résultat
  bool _isSending = false;
  bool _isDone = false;
  ScreeningResult? _result;
  ScreeningError? _error;
  String? _lastPatientKey;
  String? _lastPatientCode;

  // Dépendances de logique
  late final CameraManager camera;
  final ScreeningApiService _apiService;

  // Flux de requêtes de défilement automatique
  final StreamController<ScrollTarget> _scrollController =
      StreamController<ScrollTarget>.broadcast();

  ScreeningController({ScreeningApiService? apiService})
    : _apiService = apiService ?? ScreeningApiService() {
    camera = CameraManager(onStateChanged: notifyListeners);
    camera.onAutoCaptureRequest = _onAutoCaptureRequest;

    // Écoute des champs de saisie pour effacer les erreurs au fur et à mesure de la frappe
    nomController.addListener(() => _onFieldChanged('nom'));
    prenomController.addListener(() => _onFieldChanged('prenom'));
    ageController.addListener(() => _onFieldChanged('age'));

    // Démarrage de la caméra
    camera.initialize();
  }

  // Getters publics
  String? get sexe => _sexe;
  Map<String, String> get fieldErrors => Map.unmodifiable(_fieldErrors);
  Uint8List? get photoBytes => _photoBytes;
  bool get isCapturing => _isCapturing;
  bool get isSending => _isSending;
  bool get isDone => _isDone;
  ScreeningResult? get result => _result;
  ScreeningError? get error => _error;
  Stream<ScrollTarget> get scrollRequests => _scrollController.stream;
  bool get autoCaptureEnabled => _autoCaptureEnabled;

  void toggleAutoCapture(bool enabled) {
    if (_autoCaptureEnabled == enabled) return;
    _autoCaptureEnabled = enabled;
    camera.autoCaptureEnabled = enabled;
    notifyListeners();
  }

  void _onAutoCaptureRequest() {
    if (_isCapturing || _isSending || _photoBytes != null) return;
    if (!camera.isFramingReady) return;
    unawaited(takePhoto());
  }

  /// Mise à jour de la sélection du sexe
  void setSexe(String? value) {
    if (_sexe == value) return;
    _sexe = value;
    _onFieldChanged('sexe');
  }

  /// Réinitialise l'erreur du champ modifié et remet l'état de validation à neuf
  void _onFieldChanged(String fieldKey) {
    if (_fieldErrors.containsKey(fieldKey)) {
      _fieldErrors.remove(fieldKey);
    }
    if (_isDone) {
      _isDone = false;
    }
    notifyListeners();
  }

  /// Déclenche la prise de vue et l'affichage de l'aperçu instantané
  Future<void> takePhoto() async {
    if (!camera.isInitialized || _isCapturing || _isSending) return;

    _isCapturing = true;
    _error = null;
    notifyListeners();

    try {
      final bytes = await camera.capturePhoto();
      if (bytes != null) {
        _photoBytes = bytes;
        _error = null;
        _isDone = false;
        _scrollController.add(ScrollTarget.preview);
      }
    } on CaptureFailedException {
      _error = ScreeningError.captureFailed;
    } finally {
      _isCapturing = false;
      notifyListeners();
    }
  }

  /// Supprime la photo courante et retourne au viseur de capture
  void retakePhoto() {
    if (_isSending) return;
    _photoBytes = null;
    _isDone = false;
    _error = null;
    _scrollController.add(ScrollTarget.capture);
    notifyListeners();
  }

  /// Valide les champs et lance la requête d'analyse vers l'API
  Future<void> analyze() async {
    if (_isSending || _isDone || _photoBytes == null) return;

    // 1. Validation stricte des 4 champs obligatoires
    final errors = <String, String>{};

    final nomError = Validators.validateNom(nomController.text);
    if (nomError != null) errors['nom'] = nomError;

    final prenomError = Validators.validatePrenom(prenomController.text);
    if (prenomError != null) errors['prenom'] = prenomError;

    final ageError = Validators.validateAge(ageController.text);
    if (ageError != null) errors['age'] = ageError;

    final sexeError = Validators.validateSexe(_sexe);
    if (sexeError != null) errors['sexe'] = sexeError;

    if (errors.isNotEmpty) {
      _fieldErrors
        ..clear()
        ..addAll(errors);
      _scrollController.add(ScrollTarget.firstInvalidField);
      notifyListeners();
      return;
    }

    _fieldErrors.clear();
    _result = null;
    _error = null;
    _isSending = true;
    _isDone = false;
    notifyListeners();

    // Défilement vers la carte de chargement
    _scrollController.add(ScrollTarget.loading);

    try {
      final age = int.parse(ageController.text.trim());
      final patientKey = jsonEncode([
        nomController.text.trim().toLowerCase(),
        prenomController.text.trim().toLowerCase(),
        age,
        _sexe!.trim().toLowerCase(),
      ]);
      if (patientKey != _lastPatientKey) {
        _lastPatientKey = patientKey;
        _lastPatientCode = ScreeningRequest.generatePatientCode();
      }

      final request = ScreeningRequest(
        nom: nomController.text,
        prenom: prenomController.text,
        age: age,
        sexe: _sexe!,
        imagePng: _photoBytes!,
        patientCode: _lastPatientCode!,
      );

      // 3. Appel de l'API avec délai maximal de 60s
      final apiResult = await _apiService.analyze(request);

      _result = apiResult;
      _isDone = true;
      _scrollController.add(ScrollTarget.results);
    } on ScreeningError catch (err) {
      _error = err;
      if (err == ScreeningError.timeout) {
        // En cas de délai dépassé, la photo doit être obligatoirement reprise
        _photoBytes = null;
        _scrollController.add(ScrollTarget.capture);
      }
      // Pour les erreurs de connexion ou serveur indisponible, la photo est conservée
    } catch (_) {
      _error = ScreeningError.serverUnavailable;
    } finally {
      _isSending = false;
      notifyListeners();
    }
  }

  @override
  void dispose() {
    nomController.dispose();
    prenomController.dispose();
    ageController.dispose();
    _scrollController.close();
    unawaited(camera.dispose());
    _apiService.dispose();
    super.dispose();
  }
}
