# ============================================================
# TESTS UNITAIRES DES MODULES "core/"
# Objectif : tester chaque brique SANS passer par Flask.
# Plus rapide que test_api.py (pas de requête HTTP).
# ============================================================

# --- Imports images ---
import io
from PIL import Image
# Image : pour créer des images de test

# --- Imports internes ---
from core.image_utils import load_image, to_tensor, IMG_SIZE
# load_image : bytes → PIL.Image
# to_tensor  : PIL.Image → Tensor
# IMG_SIZE   : 224

from core.mock import MockEyeChecker, MockStageClassifier, STAGE_LABELS
# Les classes mock à tester

import torch
# torch : pour vérifier la forme des tenseurs


# ============================================================
# HELPERS : générer des images de test
# ============================================================
def make_image_bytes(width=300, height=300, color=(128, 60, 60)):
    """Crée une image JPEG en bytes (comme si elle venait du mobile)."""
    img = Image.new("RGB", (width, height), color)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.read()


# ============================================================
# TESTS DE core/image_utils.py
# ============================================================
def test_load_image_returns_pil_rgb():
    """load_image doit renvoyer une image PIL en mode RGB."""
    raw = make_image_bytes(300, 300)
    img = load_image(raw)

    assert isinstance(img, Image.Image)
    # Type correct

    assert img.mode == "RGB"
    # Mode forcé en RGB (même si l'original était L ou RGBA)

    assert img.size == (300, 300)
    # Les dimensions sont conservées (le resize se fait dans to_tensor)


def test_load_image_handles_rgba():
    """Une image RGBA (avec transparence) doit être convertie en RGB."""
    # Crée une image RGBA (4 canaux)
    img = Image.new("RGBA", (100, 100), (255, 0, 0, 128))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    result = load_image(buffer.read())
    # Doit être converti en RGB

    assert result.mode == "RGB"


def test_load_image_raises_on_invalid_bytes():
    """Des bytes non-image doivent lever une exception."""
    import pytest
    with pytest.raises(Exception):
        load_image(b"ceci n'est pas une image")
    # Pillow va lever UnidentifiedImageError ou similaire


def test_to_tensor_shape():
    """to_tensor doit produire un tenseur (1, 3, 224, 224)."""
    img = Image.new("RGB", (300, 300), (128, 60, 60))
    tensor = to_tensor(img)

    assert isinstance(tensor, torch.Tensor)
    # Type correct

    assert tensor.shape == (1, 3, IMG_SIZE, IMG_SIZE)
    # Forme : (batch=1, canaux=3, hauteur=224, largeur=224)

    # Vérifier que les valeurs sont normalisées (peuvent être négatives)
    assert tensor.min() < 0.0
    # Après normalisation ImageNet, certaines valeurs sont négatives
    assert tensor.max() > 0.0


def test_to_tensor_accepts_any_input_size():
    """to_tensor doit redimensionner n'importe quelle taille."""
    for size in [(100, 100), (512, 384), (1024, 1024)]:
        img = Image.new("RGB", size, (100, 100, 100))
        tensor = to_tensor(img)
        assert tensor.shape == (1, 3, IMG_SIZE, IMG_SIZE)
        # Toujours 224x224 en sortie


# ============================================================
# TESTS DE core/mock.py → MockEyeChecker
# ============================================================
def test_mock_eye_checker_accepts_normal_image():
    """Une image ≥ 50px doit être acceptée comme œil."""
    img = Image.new("RGB", (300, 300), (128, 60, 60))
    checker = MockEyeChecker()

    ok_eye, prob_eye = checker.is_eye(img)

    assert ok_eye is True
    assert 0.0 <= prob_eye <= 1.0
    # Probabilité dans les bornes


def test_mock_eye_checker_rejects_small_image():
    """Une image < 50px doit être rejetée (pas un œil)."""
    img = Image.new("RGB", (30, 30), (0, 0, 0))
    checker = MockEyeChecker()

    ok_eye, prob_eye = checker.is_eye(img)

    assert ok_eye is False
    assert prob_eye < 0.5
    # Probabilité faible


def test_mock_eye_checker_returns_tuple():
    """is_eye doit renvoyer un tuple (bool, float)."""
    img = Image.new("RGB", (300, 300))
    checker = MockEyeChecker()
    result = checker.is_eye(img)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], bool)
    assert isinstance(result[1], float)


# ============================================================
# TESTS DE core/mock.py → MockStageClassifier
# ============================================================
def test_mock_classifier_returns_valid_dict():
    """predict doit renvoyer un dict avec tous les champs du contrat."""
    img = Image.new("RGB", (300, 300), (128, 60, 60))
    classifier = MockStageClassifier()

    result = classifier.predict(img)

    # --- Champs présents ---
    assert "stage" in result
    assert "stage_label" in result
    assert "risk_score" in result
    assert "refer_to_doctor" in result

    # --- Types ---
    assert isinstance(result["stage"], int)
    assert isinstance(result["stage_label"], str)
    assert isinstance(result["risk_score"], float)
    assert isinstance(result["refer_to_doctor"], bool)


def test_mock_classifier_stage_in_range():
    """Le stade doit toujours être entre 0 et 4."""
    classifier = MockStageClassifier()
    for _ in range(50):
        # On teste sur 50 images différentes
        img = Image.new("RGB", (300, 300), (random_color()))
        result = classifier.predict(img)
        assert 0 <= result["stage"] <= 4


def test_mock_classifier_label_matches_stage():
    """Le stage_label doit correspondre au stage selon STAGE_LABELS."""
    classifier = MockStageClassifier()
    for _ in range(20):
        img = Image.new("RGB", (300, 300), (random_color()))
        result = classifier.predict(img)
        assert result["stage_label"] == STAGE_LABELS[result["stage"]]


def test_mock_classifier_refer_rule():
    """refer_to_doctor doit être True si et seulement si stage >= 2."""
    classifier = MockStageClassifier()
    for _ in range(50):
        img = Image.new("RGB", (300, 300), (random_color()))
        result = classifier.predict(img)

        if result["stage"] >= 2:
            assert result["refer_to_doctor"] is True
        else:
            assert result["refer_to_doctor"] is False


def test_mock_classifier_is_deterministic():
    """La même image doit donner exactement le même résultat."""
    img = Image.new("RGB", (300, 300), (42, 42, 42))
    # Couleur fixe → hash stable

    classifier = MockStageClassifier()
    result1 = classifier.predict(img)
    result2 = classifier.predict(img)

    assert result1["stage"] == result2["stage"]
    assert result1["risk_score"] == result2["risk_score"]
    assert result1["refer_to_doctor"] == result2["refer_to_doctor"]


def test_mock_classifier_risk_score_in_range():
    """risk_score doit toujours être entre 0.0 et 1.0."""
    classifier = MockStageClassifier()
    for _ in range(50):
        img = Image.new("RGB", (300, 300), (random_color()))
        result = classifier.predict(img)
        assert 0.0 <= result["risk_score"] <= 1.0


# ============================================================
# HELPER : couleur aléatoire pour varier les images de test
# ============================================================
def random_color():
    """Génère une couleur RGB aléatoire (pour varier les hash)."""
    import random
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
