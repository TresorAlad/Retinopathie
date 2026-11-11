import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

import '../../../core/config/api_config.dart';
import 'models/screening_request.dart';
import 'models/screening_result.dart';
import 'screening_error.dart';

/// Service gérant la transmission de la requête d'analyse vers l'API externe et le traitement des erreurs.
class ScreeningApiService {
  final http.Client _client;
  final Connectivity _connectivity;

  ScreeningApiService({http.Client? client, Connectivity? connectivity})
    : _client = client ?? http.Client(),
      _connectivity = connectivity ?? Connectivity();

  /// Envoie la requête multipart avec un délai d'expiration strict de 60 secondes.
  /// En cas d'échec, lance une exception contenant l'erreur [ScreeningError] appropriée.
  Future<ScreeningResult> analyze(ScreeningRequest request) async {
    try {
      return await _sendWithErrorMapping(request).timeout(ApiConfig.timeout);
    } on TimeoutException {
      // Dépassement du délai maximal de 60 secondes
      throw ScreeningError.timeout;
    }
  }

  Future<ScreeningResult> _sendWithErrorMapping(
    ScreeningRequest request,
  ) async {
    try {
      return await _sendMultipart(request);
    } on SocketException {
      // Vérification si la perte de connectivité s'est produite pendant l'appel
      final checkAgain = await _connectivity.checkConnectivity();
      if (checkAgain.contains(ConnectivityResult.none) &&
          checkAgain.length == 1) {
        throw ScreeningError.noConnection;
      }
      throw ScreeningError.serverUnavailable;
    } on http.ClientException {
      final checkAgain = await _connectivity.checkConnectivity();
      if (checkAgain.contains(ConnectivityResult.none) &&
          checkAgain.length == 1) {
        throw ScreeningError.noConnection;
      }
      throw ScreeningError.serverUnavailable;
    } on HttpException {
      throw ScreeningError.serverUnavailable;
    } on FormatException {
      // Réponse non conforme au format JSON
      throw ScreeningError.serverUnavailable;
    } catch (e) {
      if (e is ScreeningError) rethrow;
      throw ScreeningError.serverUnavailable;
    }
  }

  Future<ScreeningResult> _sendMultipart(ScreeningRequest request) async {
    // La vérification réseau fait partie de la chaîne soumise au délai global.
    final connectivityResults = await _connectivity.checkConnectivity();
    if (connectivityResults.contains(ConnectivityResult.none) &&
        connectivityResults.length == 1) {
      throw ScreeningError.noConnection;
    }

    final multipartRequest = http.MultipartRequest('POST', ApiConfig.analyzeUri)
      ..headers.addAll(ApiConfig.headers)
      ..fields.addAll(request.toMultipartFields())
      ..files.add(
        http.MultipartFile.fromBytes(
          'image',
          request.imagePng,
          filename: 'photo.png',
          contentType: MediaType('image', 'png'),
        ),
      );

    final streamedResponse = await _client.send(multipartRequest);
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw ScreeningError.serverUnavailable;
    }

    final dynamic decodedJson = jsonDecode(utf8.decode(response.bodyBytes));
    if (decodedJson is! Map<String, dynamic>) {
      throw ScreeningError.serverUnavailable;
    }

    final dynamic rawText = decodedJson[ApiConfig.responseTextKey];
    if (rawText is! String || rawText.trim().isEmpty) {
      throw ScreeningError.serverUnavailable;
    }

    return ScreeningResult(text: rawText, receivedAt: DateTime.now());
  }

  /// Ferme proprement le client HTTP lors de la destruction du service.
  void dispose() {
    _client.close();
  }
}
