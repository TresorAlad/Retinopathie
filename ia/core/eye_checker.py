# ============================================================
# ETAPE 1 : DETECTEUR D'OEIL (vrai modèle)
# Rôle : vérifier que l'image est bien un fond d'œil.
# Modèle : ResNet18 pré-entraîné, réentraîné sur 2 classes
#          (0 = not_eye, 1 = eye)
# Utilisé quand IA_MODE=prod dans app.py
# ============================================================

# --- Imports PyTorch ---
import torch
# torch : tenseurs, opérations, chargement du modèle

import torch.nn as nn
# nn : couches de réseaux de neurones (Linear, etc.)

from torchvision import models
# models : architectures pré-entraînées (resnet18, resnet50, etc.)

# --- Imports internes ---
from .image_utils import to_tensor
# to_tensor : convertit une image PIL en tenseur (1,3,224,224)

# --- Imports PIL ---
from PIL import Image
# Image : pour le typage (annotation de type)


# ============================================================
# CLASSE PRINCIPALE
# ============================================================
class EyeChecker:
    """
    Détecteur d'œil basé sur ResNet18.

    Interface publique :
        is_eye(img) → (bool, float)

    Le modèle est chargé UNE FOIS à la construction (pas à chaque appel).
    """

    def __init__(self, model_path: str = "models/eye_checker.pt"):
        """
        Args:
            model_path: chemin vers le fichier .pt des poids entraînés
        """
        # --- Étape 1 : choisir le device (GPU si dispo, sinon CPU) ---
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # En local sur PC / Colab avec GPU → "cuda"
        # En Docker sur serveur basique → "cpu"
        # Le code marche dans les deux cas

        # --- Étape 2 : construire l'architecture ResNet18 ---
        self.model = models.resnet18(weights=None)
        # weights=None : on ne charge PAS les poids ImageNet,
        # car on va charger NOS poids juste après (ceux du transfer learning)
        # (Sinon ça téléchargerait 45 Mo à chaque démarrage)

        # --- Étape 3 : remplacer la dernière couche ---
        # ResNet18 original : 1000 classes (ImageNet)
        # Nous on veut : 2 classes (not_eye / eye)
        num_features = self.model.fc.in_features
        # in_features = taille de l'entrée de la couche finale (512 pour ResNet18)

        self.model.fc = nn.Linear(num_features, 2)
        # Remplace fc (fully connected) par une nouvelle couche linéaire
        # 512 entrées → 2 sorties (logits pour not_eye et eye)

        # --- Étape 4 : charger les poids entraînés ---
        try:
            state_dict = torch.load(model_path, map_location=self.device)
            # map_location : place les tenseurs sur le bon device dès le chargement
            # évite un transfert inutile CPU → GPU après

            self.model.load_state_dict(state_dict)
            # load_state_dict : remplit les paramètres du modèle avec les poids
            # (les noms de couches doivent correspondre EXACTEMENT)

            print(f"[EyeChecker] Modèle chargé depuis {model_path}")
        except FileNotFoundError:
            # Le fichier n'existe pas encore (on n'a pas entraîné)
            print(f"[EyeChecker] WARN : {model_path} introuvable, "
                  f"le modèle est aléatoire (à entraîner !)")
            # On continue quand même pour ne pas planter le serveur au démarrage
        except Exception as e:
            # Autre erreur (fichier corrompu, architecture différente…)
            print(f"[EyeChecker] ERREUR au chargement : {e}")

        # --- Étape 5 : envoyer le modèle sur le bon device ---
        self.model = self.model.to(self.device)
        # .to(device) : déplace tous les paramètres sur GPU ou CPU

        # --- Étape 6 : passer en mode évaluation ---
        self.model.eval()
        # eval() : désactive dropout et batchnorm en mode train
        # INDISPENSABLE en inférence, sinon les résultats sont faux

    # ========================================================
    # METHODE PRINCIPALE : is_eye
    # ========================================================
    @torch.no_grad()
    def is_eye(self, img: Image.Image) -> tuple:
        """
        Vérifie si l'image est un fond d'œil.

        Args:
            img: image PIL RGB

        Returns:
            (ok_eye, prob_eye)
              ok_eye   : bool (True = c'est un œil)
              prob_eye : float (probabilité entre 0.0 et 1.0)
        """
        # @torch.no_grad() : désactive le calcul des gradients
        # → 2x plus rapide, 2x moins de mémoire (pas besoin en inférence)

        # --- Étape 1 : convertir l'image en tenseur ---
        x = to_tensor(img)
        # x : tenseur (1, 3, 224, 224)

        # --- Étape 2 : envoyer sur le device ---
        x = x.to(self.device)

        # --- Étape 3 : passer dans le modèle ---
        logits = self.model(x)
        # logits : tenseur (1, 2) — valeurs brutes (non normalisées)
        # [logit_not_eye, logit_eye]

        # --- Étape 4 : appliquer softmax ---
        probs = torch.softmax(logits, dim=1)
        # softmax : transforme les logits en probabilités qui somment à 1
        # dim=1 : applique sur la dimension des classes
        # probs : tenseur (1, 2)

        # --- Étape 5 : extraire la probabilité "œil" ---
        prob_eye = float(probs[0, 1])
        # probs[0, 1] = probabilité de la classe 1 (eye) pour le premier batch
        # float() : convertit le tenseur en float Python

        # --- Étape 6 : décider avec un seuil ---
        ok_eye = prob_eye > 0.5
        # Seuil 0.5 : si P(eye) > 0.5, on considère que c'est un œil
        # Tu peux ajuster à 0.3 (plus permissif) ou 0.7 (plus strict)
        # selon les faux positifs/négatifs constatés

        # --- Étape 7 : renvoyer ---
        return ok_eye, prob_eye