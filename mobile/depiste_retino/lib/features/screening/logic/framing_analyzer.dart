import 'dart:io';
import 'dart:typed_data';
import 'dart:ui';

import 'package:camera/camera.dart';
import 'package:google_mlkit_face_detection/google_mlkit_face_detection.dart';

import 'framing_status.dart';

/// Détecte si le visage et les yeux sont correctement centrés dans le viseur.
class FramingAnalyzer {
  FramingAnalyzer()
      : _detector = FaceDetector(
          options: FaceDetectorOptions(
            enableLandmarks: true,
            performanceMode: FaceDetectorMode.fast,
            minFaceSize: 0.15,
          ),
        );

  final FaceDetector _detector;
  DateTime _lastRun = DateTime.fromMillisecondsSinceEpoch(0);
  static const _minInterval = Duration(milliseconds: 220);

  Future<FramingStatus> analyzeFrame(
    CameraImage image,
    int rotation,
  ) async {
    final now = DateTime.now();
    if (now.difference(_lastRun) < _minInterval) {
      return FramingStatus.searching;
    }
    _lastRun = now;

    final input = _toInputImage(image, rotation);
    if (input == null) {
      return FramingStatus.searching;
    }

    try {
      final faces = await _detector.processImage(input);
      if (faces.isEmpty) {
        return FramingStatus.searching;
      }
      if (faces.length > 1) {
        return FramingStatus.almost;
      }

      final face = faces.first;
      final box = face.boundingBox;
      final imageW = image.width.toDouble();
      final imageH = image.height.toDouble();

      final cx = (box.left + box.right) / 2 / imageW;
      final cy = (box.top + box.bottom) / 2 / imageH;
      final faceHeight = box.height / imageH;

      if (faceHeight < 0.18) {
        return FramingStatus.almost;
      }

      final leftEye = face.landmarks[FaceLandmarkType.leftEye];
      final rightEye = face.landmarks[FaceLandmarkType.rightEye];
      if (leftEye == null || rightEye == null) {
        return FramingStatus.almost;
      }

      final eyeDist = (leftEye.position.x - rightEye.position.x).abs() / imageW;
      if (eyeDist < 0.12) {
        return FramingStatus.almost;
      }

      final inOval = cx > 0.28 &&
          cx < 0.72 &&
          cy > 0.32 &&
          cy < 0.68 &&
          faceHeight > 0.22;

      if (inOval) {
        return FramingStatus.ready;
      }
      if (faceHeight < 0.12) {
        return FramingStatus.poorLighting;
      }
      return FramingStatus.almost;
    } catch (_) {
      return FramingStatus.searching;
    }
  }

  InputImage? _toInputImage(CameraImage image, int rotation) {
    if (!Platform.isAndroid && !Platform.isIOS) {
      return null;
    }
    final format = InputImageFormatValue.fromRawValue(image.format.raw);
    if (format == null) {
      return null;
    }

    Uint8List bytes;
    if (Platform.isAndroid && image.planes.length == 3) {
      bytes = _yuv420ToNv21(image);
    } else {
      bytes = image.planes.first.bytes;
    }

    final imageFormat =
        Platform.isAndroid ? InputImageFormat.nv21 : InputImageFormat.yuv420;

    return InputImage.fromBytes(
      bytes: bytes,
      metadata: InputImageMetadata(
        size: Size(image.width.toDouble(), image.height.toDouble()),
        rotation: _rotationToImageRotation(rotation),
        format: imageFormat,
        bytesPerRow: image.planes.first.bytesPerRow,
      ),
    );
  }

  InputImageRotation _rotationToImageRotation(int rotation) {
    switch (rotation) {
      case 90:
        return InputImageRotation.rotation90deg;
      case 180:
        return InputImageRotation.rotation180deg;
      case 270:
        return InputImageRotation.rotation270deg;
      default:
        return InputImageRotation.rotation0deg;
    }
  }

  Uint8List _yuv420ToNv21(CameraImage image) {
    final width = image.width;
    final height = image.height;
    final yPlane = image.planes[0];
    final uPlane = image.planes[1];
    final vPlane = image.planes[2];

    final nv21 = Uint8List(width * height + (width * height) ~/ 2);
    var offset = 0;

    if (yPlane.bytesPerRow == width) {
      nv21.setRange(0, width * height, yPlane.bytes);
      offset = width * height;
    } else {
      for (var row = 0; row < height; row++) {
        nv21.setRange(
          offset,
          offset + width,
          yPlane.bytes,
          row * yPlane.bytesPerRow,
        );
        offset += width;
      }
    }

    final uvRowStride = uPlane.bytesPerRow;
    final uvPixelStride = uPlane.bytesPerPixel ?? 1;

    for (var row = 0; row < height ~/ 2; row++) {
      for (var col = 0; col < width ~/ 2; col++) {
        final uvIndex = row * uvRowStride + col * uvPixelStride;
        nv21[offset++] = vPlane.bytes[uvIndex];
        nv21[offset++] = uPlane.bytes[uvIndex];
      }
    }
    return nv21;
  }

  Future<void> dispose() async {
    await _detector.close();
  }
}
