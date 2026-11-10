# ============================================================
# PACKAGE "core"
# Ce fichier transforme le dossier "core/" en package Python.
# Sans lui : "from core.eye_checker import EyeChecker" ne marche pas.
#
# Il expose aussi les classes principales pour des imports plus courts :
#   from core import EyeChecker        (au lieu de core.eye_checker)
# ============================================================

# --- Imports des classes principales ---
from .eye_checker import EyeChecker
# EyeChecker : étape 1 (est-ce un œil ?)

from .stage_classifier import StageClassifier
# StageClassifier : étape 2 (quel stade ?)

# --- Imports des utilitaires ---
from .image_utils import load_image, to_tensor, IMG_SIZE
# load_image : bytes → image PIL
# to_tensor  : image PIL → tenseur PyTorch
# IMG_SIZE   : 224 (taille d'entrée des modèles)

# --- Imports du mock (accessible même en prod, utile pour tests) ---
from .mock import MockEyeChecker, MockStageClassifier, STAGE_LABELS
# MockEyeChecker    : version simulée de EyeChecker
# MockStageClassifier : version simulée de StageClassifier
# STAGE_LABELS      : dict {0: "...", ..., 4: "..."}


# ============================================================
# LISTE PUBLIQUE DU PACKAGE
# ============================================================
__all__ = [
    # Modèles réels
    "EyeChecker",
    "StageClassifier",

    # Utilitaires images
    "load_image",
    "to_tensor",
    "IMG_SIZE",

    # Mock (pour les tests et le mode mock)
    "MockEyeChecker",
    "MockStageClassifier",

    # Constantes
    "STAGE_LABELS",
]
# __all__ : définit ce que "from core import *" exporte
# Bonne pratique pour éviter les imports accidentels