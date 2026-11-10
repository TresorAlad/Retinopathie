# ============================================================
# ETAPE 2 : CLASSIFIEUR DE STADE (vrai modèle)
# Rôle : prédire le stade de rétinopathie (0 à 4).
# Modèle : ResNet50 pré-entraîné, réentraîné sur 5 classes
#          0 = Pas de rétinopathie
#          1 = Légère
#          2 = Modérée
#          3 = Sévère
#          4 = Proliférative
# Chargé au démarrage de app.py
# ============================================================

# --- Imports PyTorch ---
import torch
# torch : tenseurs, chargement du modèle, opérations

import torch.nn as nn
# nn : couches de réseaux de neurones (Linear)

from torchvision import models
# models : architectures pré-entraînées (resnet50)

# --- Imports internes ---
from .image_utils import to_tensor
# to_tensor : convertit une image PIL en tenseur (1,3,224,224)

# --- Imports PIL ---
from PIL import Image
# Image : pour les annotations de type


# ============================================================
# LIBELLES DES STADES (rappel du contrat API)
# ============================================================
STAGE_LABELS = {
    0: "Pas de rétinopathie",
    1: "Légère",
    2: "Modérée",
    3: "Sévère",
    4: "Proliférative",
}
# ATTENTION : ces libellés doivent être EXACTEMENT les mêmes
# que le contrat API backend et mobile.
# Sinon le web docteur et le mobile afficheront des libellés différents.


# ============================================================
# CLASSE PRINCIPALE
# ============================================================
class StageClassifier:
    """
    Classifieur de stade basé sur ResNet50.

    Interface publique :
        predict(img) → dict {stage, stage_label, risk_score, refer_to_doctor}

    Le modèle est chargé UNE FOIS à la construction.
    """

    def __init__(self, model_path: str = "models/stage_classifier.pt"):
        """
        Args:
            model_path: chemin vers le fichier .pt des poids entraînés
        """
        # --- Étape 1 : choisir le device ---
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # GPU si dispo, sinon CPU
        # Sur le serveur de démo, c'est probablement CPU (suffit pour 1 image)

        # --- Étape 2 : construire l'architecture ResNet50 ---
        self.model = models.resnet50(weights=None)
        # ResNet50 : plus profond que ResNet18, meilleur pour des tâches fines
        # comme distinguer 5 stades de rétinopathie.
        # weights=None : pas de téléchargement ImageNet, on charge nos poids après.

        # --- Étape 3 : remplacer la dernière couche ---
        num_features = self.model.fc.in_features
        # in_features = 2048 pour ResNet50 (contre 512 pour ResNet18)

        self.model.fc = nn.Linear(num_features, 5)
        # Nouvelle couche : 2048 entrées → 5 sorties (une par stade)

        # --- Étape 4 : charger les poids entraînés ---
        try:
            state_dict = torch.load(model_path, map_location=self.device)
            # Charge le state_dict depuis le .pt

            self.model.load_state_dict(state_dict)
            # Remplit les paramètres du modèle

            print(f"[StageClassifier] Modèle chargé depuis {model_path}")
        except FileNotFoundError:
            # Pas de modèle entraîné
            print(f"[StageClassifier] WARN : {model_path} introuvable, "
                  f"le modèle est aléatoire (à entraîner !)")
        except Exception as e:
            # Autre erreur (corruption, incompatibilité)
            print(f"[StageClassifier] ERREUR au chargement : {e}")

        # --- Étape 5 : envoyer sur le device ---
        self.model = self.model.to(self.device)

        # --- Étape 6 : mode évaluation ---
        self.model.eval()
        # Désactive dropout/batchnorm. OBLIGATOIRE en inférence.

    # ========================================================
    # METHODE PRINCIPALE : predict
    # ========================================================
    @torch.no_grad()
    def predict(self, img: Image.Image) -> dict:
        """
        Prédit le stade de rétinopathie.

        Args:
            img: image PIL RGB (déjà validée comme œil par EyeChecker)

        Returns:
            dict {
                stage            : int 0..4
                stage_label      : str
                risk_score       : float 0.0..1.0
                refer_to_doctor  : bool
            }
        """
        # @torch.no_grad() : pas de gradients → rapide et léger

        # --- Étape 1 : convertir en tenseur ---
        x = to_tensor(img)
        # x : (1, 3, 224, 224)

        # --- Étape 2 : envoyer sur le device ---
        x = x.to(self.device)

        # --- Étape 3 : forward pass ---
        logits = self.model(x)
        # logits : (1, 5) — 5 valeurs brutes, une par stade

        # --- Étape 4 : softmax → probabilités ---
        probs = torch.softmax(logits, dim=1)
        # probs : (1, 5), chaque valeur ∈ [0,1], somme = 1

        # --- Étape 5 : passer sur CPU et convertir en numpy ---
        probs_np = probs[0].cpu().numpy()
        # probs[0] : enlève la dimension batch → (5,)
        # .cpu() : si on est sur GPU, on rapatrie sur CPU (numpy ne gère pas GPU)
        # .numpy() : convertit le tenseur en tableau numpy

        # --- Étape 6 : déterminer le stade prédit ---
        stage = int(probs_np.argmax())
        # argmax : indice de la probabilité maximale → 0, 1, 2, 3 ou 4
        # int() : convertit en int Python natif (pas numpy.int64)

        # --- Étape 7 : calculer le risk_score ---
        risk = float(probs_np[2:].sum())
        # probs_np[2:] = probabilités des stades 2, 3, 4
        # somme = P(stage >= 2) = seuil clinique de référence
        #
        # Pourquoi ce calcul et pas probs_np[stage] ?
        #   - probs_np[stage] = "à quel point on est sûrs du stade exact"
        #   - probs_np[2:].sum() = "probabilité que le patient ait besoin
        #     d'une consultation" → plus utile pour trier la file d'attente
        #
        # Le Master a figé : risk_score = P(stage >= 2). On respecte.

        # --- Étape 8 : construire la réponse ---
        return {
            "stage": stage,
            # stade prédit (0..4)

            "stage_label": STAGE_LABELS[stage],
            # libellé lisible

            "risk_score": round(risk, 4),
            # arrondi à 4 décimales pour un JSON propre

            "refer_to_doctor": stage >= 2,
            # règle clinique : on réfère dès le stade 2
        }