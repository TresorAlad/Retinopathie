# ============================================================
# TESTS DE L'API FLASK (/health et /predict)
# Objectif : prouver que le service respecte le contrat du Master.
# Lancement : pytest tests/ -v
# ============================================================

# --- Imports de test ---
import io
# io : pour créer des fausses images en mémoire (BytesIO)

from PIL import Image
# Image : pour générer des images de test programmatiquement

import pytest
# pytest : framework de test (fixtures, assert, etc.)

# --- Import de l'application Flask ---
from app import app
# app = l'instance Flask créée dans app.py
# Grâce à tests/__init__.py, IA_MODE=mock est forcé
# → aucun modèle PyTorch ne sera chargé


# ============================================================
# FIXTURE : client de test
# ============================================================
@pytest.fixture
def client():
    """
    Crée un client HTTP de test pour Flask.
    Équivalent de curl, mais en Python, sans lancer le serveur.
    """
    app.config["TESTING"] = True
    # TESTING=True : Flask renvoie les erreurs détaillées au lieu de
    # pages HTML génériques → plus facile à déboguer en cas d'échec

    with app.test_client() as c:
        yield c
    # yield : le client est disponible pour chaque test, puis fermé


# ============================================================
# FONCTION UTILITAIRE : générer une image de test
# ============================================================
def make_image(width=300, height=300, color=(128, 60, 60)):
    """
    Crée une image JPEG en mémoire (bytes) pour l'envoyer à /predict.

    Args:
        width, height : dimensions (pour tester le rejet <50px)
        color         : couleur RGB (peu importe pour le mock)

    Returns:
        tuple (nom_fichier, bytes, content_type) prêt pour multipart
    """
    img = Image.new("RGB", (width, height), color)
    # Image.new : crée une image unie (pas de fichier à lire)

    buffer = io.BytesIO()
    # BytesIO : "faux fichier" en mémoire pour stocker le JPEG

    img.save(buffer, format="JPEG")
    # Enregistre l'image au format JPEG dans le buffer

    buffer.seek(0)
    # Remet le curseur au début pour la lecture

    return "test.jpg", buffer.read(), "image/jpeg"
    # Format attendu par flask.test_client : (nom, bytes, content_type)


# ============================================================
# TEST 1 : /health doit répondre 200 et "ok"
# ============================================================
def test_health(client):
    """Le service doit être vivant et se déclarer en mode mock."""
    response = client.get("/health")
    # Simule : curl http://localhost:8001/health

    assert response.status_code == 200
    # On attend un succès HTTP

    data = response.get_json()
    # .get_json() : parse la réponse JSON en dict Python

    assert data["status"] == "ok"
    # Le contrat impose "status": "ok"

    assert data["service"] == "ia"
    # Le service doit s'identifier

    assert data["mode"] == "mock"
    # On tourne en mode mock dans les tests (forcé par __init__.py)


# ============================================================
# TEST 2 : /predict avec une image valide → contrat complet
# ============================================================
def test_predict_valid_image_returns_all_contract_fields(client):
    """Une image valide doit renvoyer TOUS les champs du contrat."""
    name, data, ct = make_image(300, 300)
    # Image 300x300 → pas rejetée par le mock (seuil à 50px)

    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
        # content_type obligatoire avec un envoi de fichier Flask
    )

    assert response.status_code == 200
    # Pas d'erreur

    body = response.get_json()

    # --- Vérifier que tous les champs du contrat sont présents ---
    required_fields = {
        "is_eye",
        "stage",
        "stage_label",
        "risk_score",
        "refer_to_doctor",
        "model_version",
    }
    for field in required_fields:
        assert field in body, f"Champ manquant : {field}"
    # f-string : message d'erreur clair si un champ manque

    # --- Vérifier les types et les bornes ---
    assert body["is_eye"] is True
    # Le mock renvoie True pour une image ≥ 50px

    assert isinstance(body["stage"], int)
    # stage doit être un int (pas un float, pas un str)

    assert 0 <= body["stage"] <= 4
    # stade valide 0..4

    assert body["stage_label"] in (
        "Pas de rétinopathie", "Légère", "Modérée", "Sévère", "Proliférative"
    )
    # Libellé dans la liste officielle

    assert isinstance(body["risk_score"], float)
    assert 0.0 <= body["risk_score"] <= 1.0
    # risk_score : float entre 0 et 1

    assert isinstance(body["refer_to_doctor"], bool)
    # booléen strict (pas 0/1)

    assert body["model_version"] == "1.0.0"
    # traçabilité


# ============================================================
# TEST 3 : /predict avec une image NON-œil → rejet propre
# ============================================================
def test_predict_non_eye_returns_rejection(client):
    """Une image trop petite déclenche le rejet (is_eye=false)."""
    # Le mock rejette les images < 50px (voir core/mock.py)
    name, data, ct = make_image(30, 30)

    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    # Le rejet est une réponse VALIDE (pas une erreur HTTP)

    body = response.get_json()

    assert body["is_eye"] is False
    # Confirme le rejet

    assert body["stage"] == -1
    # -1 = "non applicable" (convention du contrat)

    assert body["stage_label"] == "Image non reconnue"
    # Libellé spécifique au rejet

    assert body["risk_score"] == 0.0
    # Pas de risque calculé

    assert body["refer_to_doctor"] is False
    # Pas de référence pour un non-œil


# ============================================================
# TEST 4 : /predict sans champ "image" → 400
# ============================================================
def test_predict_missing_image_returns_400(client):
    """Sans fichier 'image', on doit renvoyer 400."""
    response = client.post(
        "/predict",
        data={},
        # Aucun fichier
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    # Bad Request

    body = response.get_json()
    assert "error" in body
    # On veut un message d'erreur clair


# ============================================================
# TEST 5 : /predict avec un mauvais content-type → 400
# ============================================================
def test_predict_bad_content_type_returns_400(client):
    """Un fichier .txt ne doit pas être accepté."""
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(b"pas une image"), "f.txt", "text/plain")},
        # content_type="text/plain" → refusé par app.py
        content_type="multipart/form-data",
    )

    assert response.status_code == 400

    body = response.get_json()
    assert "error" in body


# ============================================================
# TEST 6 : /predict avec des bytes corrompus → 400
# ============================================================
def test_predict_corrupt_image_returns_400(client):
    """Des bytes aléatoires renommés .jpg doivent échouer proprement."""
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(b"\x00\x01\x02 fake bytes"), "fake.jpg", "image/jpeg")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    # Pillow va échouer à ouvrir → app.py renvoie 400

    body = response.get_json()
    assert "error" in body


# ============================================================
# TEST 7 : cohérence stage >= 2 ⇒ refer_to_doctor = True
# ============================================================
def test_refer_to_doctor_rule_consistency(client):
    """
    Règle clinique : dès que stage >= 2, refer_to_doctor doit être True.
    C'est le Master qui va exiger ce test (règle ETDRS).
    """
    # On teste sur plusieurs images pour avoir différents stades
    for size in [100, 200, 300, 400, 500]:
        name, data, ct = make_image(size, size)
        response = client.post(
            "/predict",
            data={"image": (io.BytesIO(data), name, ct)},
            content_type="multipart/form-data",
        )
        body = response.get_json()

        # Si c'est un œil ET que le stade >= 2
        if body["is_eye"] and body["stage"] >= 2:
            assert body["refer_to_doctor"] is True, (
                f"Violation : stage={body['stage']} "
                f"mais refer_to_doctor={body['refer_to_doctor']}"
            )


# ============================================================
# TEST 8 : /predict est déterministe (même image = même réponse)
# ============================================================
def test_predict_is_deterministic(client):
    """
    Le mock est basé sur un hash de l'image.
    La même image doit TOUJOURS donner la même réponse.
    C'est vital pour la démo : pas de résultat qui change tout seul.
    """
    name, data, ct = make_image(300, 300, color=(50, 100, 150))
    # Image avec une couleur spécifique → hash stable

    # Envoi 1
    r1 = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
    )
    body1 = r1.get_json()

    # Envoi 2 (même image)
    r2 = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
    )
    body2 = r2.get_json()

    # Les deux réponses doivent être identiques
    assert body1["stage"] == body2["stage"]
    assert body1["risk_score"] == body2["risk_score"]
    assert body1["refer_to_doctor"] == body2["refer_to_doctor"]