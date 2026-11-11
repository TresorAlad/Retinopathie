import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:depiste_retino/core/utils/image_utils.dart';

class CameraManager with WidgetsBindingObserver {
  CameraController? _controller;
  List<CameraDescription> _availableCameras = [];
  int _currentCameraIndex = 0;

  bool _isInitialized = false;
  bool _isSwitching = false;
  bool _isInitializing = false;
  bool _isTakingPicture = false;
  bool _isFlashOn = false;
  bool _hasFlashSupport = false;
  bool _isPermissionDenied = false;
  bool _isPermanentlyDenied = false;
  bool _hasCameraError = false;
  bool _hasNoCamera = false;

  final VoidCallback onStateChanged;

  CameraManager({required this.onStateChanged}) {
    WidgetsBinding.instance.addObserver(this);
  }

  CameraController? get controller => _controller;
  bool get isInitialized =>
      _isInitialized && _controller != null && _controller!.value.isInitialized;
  bool get isSwitching => _isSwitching;
  bool get isInitializing => _isInitializing;
  bool get isFlashOn => _isFlashOn;
  bool get hasFlashSupport => _hasFlashSupport && !isFrontCamera;
  bool get isPermissionDenied => _isPermissionDenied;
  bool get isPermanentlyDenied => _isPermanentlyDenied;
  bool get hasCameraError => _hasCameraError;
  bool get hasNoCamera => _hasNoCamera;

  CameraDescription? get primaryBackCamera {
    try {
      return _availableCameras.firstWhere(
        (cam) => cam.lensDirection == CameraLensDirection.back,
      );
    } catch (_) {
      return null;
    }
  }

  CameraDescription? get primaryFrontCamera {
    try {
      return _availableCameras.firstWhere(
        (cam) => cam.lensDirection == CameraLensDirection.front,
      );
    } catch (_) {
      return null;
    }
  }

  bool get canSwitchCamera {
    if (_isSwitching) return false;
    return (primaryBackCamera != null && primaryFrontCamera != null) ||
        _availableCameras.length > 1;
  }

  bool get isFrontCamera {
    if (_availableCameras.isEmpty ||
        _currentCameraIndex >= _availableCameras.length) {
      return false;
    }
    return _availableCameras[_currentCameraIndex].lensDirection ==
        CameraLensDirection.front;
  }

  Future<void> initialize() async {
    if (_isInitializing) return;
    _isInitializing = true;
    _hasCameraError = false;
    _hasNoCamera = false;
    onStateChanged();
    try {
      await _initializeWithPermission();
    } catch (error) {
      debugPrint('[CameraManager] Erreur d’initialisation caméra: $error');
      _isInitialized = false;
      _hasCameraError = true;
      onStateChanged();
    } finally {
      _isInitializing = false;
      onStateChanged();
    }
  }

  Future<void> _initializeWithPermission() async {
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

  Future<void> retryInitialization() async {
    if (_isInitializing) return;
    _isInitializing = true;
    _hasCameraError = false;
    _hasNoCamera = false;
    _isPermissionDenied = false;
    _isPermanentlyDenied = false;
    _isInitialized = false;
    final oldController = _controller;
    _controller = null;
    onStateChanged();
    try {
      await oldController?.dispose();
      await _initializeWithPermission();
    } catch (error) {
      debugPrint('[CameraManager] Erreur de nouvelle tentative caméra: $error');
      _isInitialized = false;
      _hasCameraError = true;
      onStateChanged();
    } finally {
      _isInitializing = false;
      onStateChanged();
    }
  }

  Future<void> _initCameras() async {
    try {
      _availableCameras = await availableCameras();
      if (_availableCameras.isEmpty) {
        _hasNoCamera = true;
        _isInitialized = false;
        onStateChanged();
        return;
      }

      final back = primaryBackCamera;
        if (back != null) {
          _currentCameraIndex = _availableCameras.indexOf(back);
        } else {
          final front = primaryFrontCamera;
            _currentCameraIndex = front != null
              ? _availableCameras.indexOf(front)
              : 0;
        }

      await _setupController(_availableCameras[_currentCameraIndex]);
    } catch (e) {
      debugPrint('[CameraManager] Erreur _initCameras: $e');
      _hasCameraError = true;
      _hasNoCamera = false;
      _isInitialized = false;
      onStateChanged();
    }
  }

  Future<void> _setupController(CameraDescription cameraDescription) async {
    final oldController = _controller;
    _controller = null;
    if (oldController != null) {
      try {
        await oldController.dispose();
      } catch (_) {}
    }

    CameraController newController = CameraController(
      cameraDescription,
      ResolutionPreset.high,
      enableAudio: false,
      imageFormatGroup: ImageFormatGroup.jpeg,
    );

    try {
      await newController.initialize();
    } catch (e) {
      try {
        await newController.dispose();
      } catch (_) {}
      newController = CameraController(
        cameraDescription,
        ResolutionPreset.medium,
        enableAudio: false,
      );
      try {
        await newController.initialize();
      } catch (_) {
        try {
          await newController.dispose();
        } catch (_) {}
        rethrow;
      }
    }

    try {
      await newController.lockCaptureOrientation(DeviceOrientation.portraitUp);
    } catch (_) {}

    _controller = newController;
    _isInitialized = true;
    _hasCameraError = false;
    _hasNoCamera = false;
    _isPermissionDenied = false;
    _isPermanentlyDenied = false;
    _isFlashOn = false;
    _hasFlashSupport =
        (cameraDescription.lensDirection == CameraLensDirection.back);

    onStateChanged();
  }

  Future<void> switchCamera() async {
    if (!canSwitchCamera) return;

    _isSwitching = true;
    _isFlashOn = false;
    onStateChanged();

    try {
      CameraDescription? targetCamera;

      if (isFrontCamera) {
        targetCamera = primaryBackCamera;
      } else {
        targetCamera = primaryFrontCamera;
      }

      if (targetCamera == null && _availableCameras.isNotEmpty) {
        final nextIdx = (_currentCameraIndex + 1) % _availableCameras.length;
        targetCamera = _availableCameras[nextIdx];
      }

      if (targetCamera != null) {
        _currentCameraIndex = _availableCameras.indexOf(targetCamera);
        await _setupController(targetCamera);
      }
    } catch (e) {
      debugPrint('[CameraManager] Erreur switchCamera: $e');
      _isInitialized = false;
      _hasCameraError = true;
      onStateChanged();
    } finally {
      _isSwitching = false;
      onStateChanged();
    }
  }

  Future<void> toggleFlash() async {
    if (_controller == null ||
        !_isInitialized ||
        isFrontCamera ||
        !_hasFlashSupport) {
      return;
    }

    try {
      final newMode = _isFlashOn ? FlashMode.off : FlashMode.torch;
      await _controller!.setFlashMode(newMode);
      _isFlashOn = (newMode == FlashMode.torch);
    } catch (_) {
      _isFlashOn = false;
      _hasFlashSupport = false;
    }
    onStateChanged();
  }

  Future<Uint8List?> capturePhoto() async {
    if (_controller == null || !_isInitialized || _isTakingPicture) return null;

    _isTakingPicture = true;
    File? tempFile;
    try {
      final xFile = await _controller!.takePicture();
      tempFile = File(xFile.path);
      final rawBytes = await tempFile.readAsBytes();

      try {
        if (await tempFile.exists()) {
          await tempFile.delete();
          tempFile = null;
        }
      } catch (_) {}

      final pngBytes = await ImageUtils.convertToPng(rawBytes);
      return pngBytes;
    } catch (_) {
      throw CaptureFailedException();
    } finally {
      if (tempFile != null) {
        try {
          if (await tempFile.exists()) {
            await tempFile.delete();
          }
        } catch (_) {}
      }
      _isTakingPicture = false;
    }
  }

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

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.inactive ||
        state == AppLifecycleState.paused) {
      _controller?.dispose();
      _controller = null;
      _isInitialized = false;
      onStateChanged();
    } else if (state == AppLifecycleState.resumed) {
      initialize();
    }
  }

  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _controller?.dispose();
    _controller = null;
  }
}

class CaptureFailedException implements Exception {}
