import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:permission_handler/permission_handler.dart';
import '../../../core/utils/image_utils.dart';

/// Gestionnaire de la caméra physique, de ses permissions et de son cycle de vie.
/// Conforme à l'ensemble des règles de prise de vue et de sécurité du cahier des charges.
class CameraManager with WidgetsBindingObserver {
  CameraController? _controller;
  List<CameraDescription> _availableCameras = [];
  int _currentCameraIndex = 0;

  bool _isInitialized = false;
  bool _isSwitching = false;
  bool _isFlashOn = false;
  bool _hasFlashSupport = true;
  bool _isPermissionDenied = false;
  bool _isPermanentlyDenied = false;
  bool _hasCameraError = false;

  final VoidCallback onStateChanged;

  CameraManager({required this.onStateChanged}) {
    WidgetsBinding.instance.addObserver(this);
  }

  // Getters d'état
  CameraController? get controller => _controller;
  bool get isInitialized => _isInitialized && _controller != null && _controller!.value.isInitialized;
  bool get isSwitching => _isSwitching;
  bool get isFlashOn => _isFlashOn;
  bool get hasFlashSupport => _hasFlashSupport && !isFrontCamera;
  bool get isPermissionDenied => _isPermissionDenied;
  bool get isPermanentlyDenied => _isPermanentlyDenied;
  bool get hasCameraError => _hasCameraError;
  bool get canSwitchCamera => _availableCameras.length > 1 && !_isSwitching;

  /// Indique si la caméra active actuelle est la caméra avant
  bool get isFrontCamera {
    if (_availableCameras.isEmpty || _currentCameraIndex >= _availableCameras.length) {
      return false;
    }
    return _availableCameras[_currentCameraIndex].lensDirection == CameraLensDirection.front;
  }

  /// Initialise la caméra au démarrage de la page après vérification de la permission
  Future<void> initialize() async {
    final status = await Permission.camera.status;
    if (status.isGranted) {
      await _initCameras();
    } else if (status.isPermanentlyDenied) {
      _isPermanentlyDenied = true;
      _isPermissionDenied = true;
      onStateChanged();
    } else {
      final requestStatus = await Permission.camera.request();
      if (requestStatus.isGranted) {
        await _initCameras();
      } else {
        _isPermissionDenied = true;
        _isPermanentlyDenied = requestStatus.isPermanentlyDenied;
        onStateChanged();
      }
    }
  }

  /// Recherche les caméras disponibles et initialise la caméra avant par défaut
  Future<void> _initCameras() async {
    try {
      _availableCameras = await availableCameras();
      if (_availableCameras.isEmpty) {
        _hasCameraError = true;
        _isInitialized = false;
        onStateChanged();
        return;
      }

      // Sélection prioritaire de la caméra avant si elle existe
      final frontIndex = _availableCameras.indexWhere(
        (cam) => cam.lensDirection == CameraLensDirection.front,
      );
      _currentCameraIndex = frontIndex != -1 ? frontIndex : 0;

      await _setupController(_availableCameras[_currentCameraIndex]);
    } catch (_) {
      _hasCameraError = true;
      _isInitialized = false;
      onStateChanged();
    }
  }

  /// Configure et démarre le contrôleur de la caméra choisie
  Future<void> _setupController(CameraDescription cameraDescription) async {
    final oldController = _controller;
    if (oldController != null) {
      await oldController.dispose();
      _controller = null;
    }

    final newController = CameraController(
      cameraDescription,
      ResolutionPreset.veryHigh,
      enableAudio: false,
      imageFormatGroup: ImageFormatGroup.jpeg,
    );

    try {
      await newController.initialize();
      // Verrouillage de l'orientation de capture en mode portrait
      await newController.lockCaptureOrientation(DeviceOrientation.portraitUp);

      _controller = newController;
      _isInitialized = true;
      _hasCameraError = false;
      _isPermissionDenied = false;
      _isPermanentlyDenied = false;
      _isFlashOn = false;
      _hasFlashSupport = true;
    } catch (_) {
      _hasCameraError = true;
      _isInitialized = false;
    }

    onStateChanged();
  }

  /// Bascule entre la caméra avant et arrière
  Future<void> switchCamera() async {
    if (!canSwitchCamera || !isInitialized) return;

    _isSwitching = true;
    _isFlashOn = false;
    onStateChanged();

    try {
      _currentCameraIndex = (_currentCameraIndex + 1) % _availableCameras.length;
      await _setupController(_availableCameras[_currentCameraIndex]);
    } finally {
      _isSwitching = false;
      onStateChanged();
    }
  }

  /// Active ou désactive le flash (mode torche) sur la caméra arrière
  Future<void> toggleFlash() async {
    if (_controller == null || !_isInitialized || isFrontCamera || !_hasFlashSupport) {
      return;
    }

    try {
      final newMode = _isFlashOn ? FlashMode.off : FlashMode.torch;
      await _controller!.setFlashMode(newMode);
      _isFlashOn = (newMode == FlashMode.torch);
    } catch (_) {
      // Si le matériel ne supporte pas le mode torche, repli silencieux
      _isFlashOn = false;
      _hasFlashSupport = false;
    }
    onStateChanged();
  }

  /// Déclenche la prise de vue, lit les données brutes, supprime immédiatement
  /// le fichier temporaire du disque et convertit l'image en PNG en mémoire.
  Future<Uint8List?> capturePhoto() async {
    if (_controller == null || !_isInitialized) return null;

    try {
      final xFile = await _controller!.takePicture();
      final tempFile = File(xFile.path);

      // Lecture intégrale des octets en mémoire
      final rawBytes = await tempFile.readAsBytes();

      // Suppression immédiate et silencieuse du fichier temporaire du disque
      try {
        if (await tempFile.exists()) {
          await tempFile.delete();
        }
      } catch (_) {
        // Suppression silencieuse
      }

      // Conversion en PNG dans un isolate d'arrière-plan avec correction EXIF
      final pngBytes = await ImageUtils.convertToPng(rawBytes);
      return pngBytes;
    } catch (_) {
      return null;
    }
  }

  /// Demande la permission ou ouvre les réglages système
  Future<void> requestPermissionOrOpenSettings() async {
    if (_isPermanentlyDenied) {
      await openAppSettings();
    } else {
      final status = await Permission.camera.request();
      if (status.isGranted) {
        _isPermissionDenied = false;
        _isPermanentlyDenied = false;
        await _initCameras();
      } else {
        _isPermissionDenied = true;
        _isPermanentlyDenied = status.isPermanentlyDenied;
        onStateChanged();
      }
    }
  }

  /// Gestion des changements d'état du cycle de vie de l'application
  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.inactive || state == AppLifecycleState.paused) {
      // Libération des ressources de la caméra quand l'application passe en arrière-plan
      _controller?.dispose();
      _controller = null;
      _isInitialized = false;
      onStateChanged();
    } else if (state == AppLifecycleState.resumed) {
      // Réinitialisation au retour au premier plan (ex: retour des réglages système)
      initialize();
    }
  }

  /// Libération finale des ressources
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _controller?.dispose();
    _controller = null;
  }
}
