# ============================================================
# OUTILS DE MANIPULATION D'IMAGES
# Rôle : transformer des bytes (envoyés par le backend) en
#        tenseur PyTorch prêt pour les modèles.
# Ce fichier ne dépend PAS de Flask : il est réutilisable partout.
# ============================================================

# --- Imports standards ---
import io
# io : permet de transformer des bytes en flux lisible par Pillow

# --- Imports images ---
from PIL import Image
# Image : la classe principale de Pillow pour ouvrir/manipuler une image

# --- Imports PyTorch ---
import torch
from torchvision import transforms
# transforms : pipeline de prétraitement (resize, normalize, toTensor)


# ============================================================
# CONSTANTES
# ============================================================
IMG_SIZE = 224
# Taille d'entrée attendue par ResNet18 et ResNet50 (224x224 pixels)
# Si tu changes de modèle (EfficientNet, etc.), adapte cette valeur


# ============================================================
# PIPELINE DE PRETRAITEMENT
# ============================================================
# L'ordre est important : Resize → ToTensor → Normalize
preprocess = transforms.Compose([
    # --- Redimensionner à 224x224 ---
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    # (H, W) — les modèles pré-entraînés ImageNet attendent cette taille

    # --- Convertir PIL.Image (H,W,C) en tenseur (C,H,W) ---
    transforms.ToTensor(),
    # Transforme les valeurs 0-255 en float 0.0-1.0
    # Et réorganise les axes : (H,W,3) → (3,H,W)

    # --- Normaliser avec les moyennes/écarts d'ImageNet ---
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],   # moyenne par canal (R,G,B)
        std=[0.229, 0.224, 0.225],    # écart-type par canal
    ),
    # Indispensable car les modèles pré-entraînés ont été entraînés
    # avec ces statistiques. Ne pas le faire = chute de performance.
])


# ============================================================
# FONCTION 1 : charger une image depuis des bytes
# ============================================================
def load_image(data: bytes) -> Image.Image:
    """
    Transforme les bytes reçus du backend en image PIL RGB.

    Args:
        data: contenu binaire du fichier (ce que file.read() renvoie)

    Returns:
        Image PIL en mode RGB (3 canaux), prête pour to_tensor()

    Raises:
        Exception si le fichier n'est pas une image valide
    """
    # --- Étape 1 : transformer les bytes en flux ---
    buffer = io.BytesIO(data)
    # BytesIO : objet qui se comporte comme un fichier mais en mémoire
    # Pillow sait lire depuis un flux, pas depuis des bytes bruts

    # --- Étape 2 : ouvrir l'image ---
    img = Image.open(buffer)
    # Image.open lit l'en-tête (format, taille) sans décoder les pixels

    # --- Étape 3 : forcer le mode RGB ---
    img = img.convert("RGB")
    # Certaines images peuvent être :
    #   - "L"  (niveaux de gris, 1 canal)
    #   - "RGBA" (avec transparence, 4 canaux)
    #   - "P"  (palette, 1 canal indexé)
    # Les modèles attendent 3 canaux RGB → on force la conversion

    # --- Étape 4 : renvoyer ---
    return img


# ============================================================
# FONCTION 2 : convertir une image PIL en tenseur PyTorch
# ============================================================
def to_tensor(img: Image.Image) -> torch.Tensor:
    """
    Applique le pipeline de prétraitement et ajoute la dimension batch.

    Args:
        img: image PIL RGB

    Returns:
        Tenseur de forme (1, 3, 224, 224), prêt pour model(x)
    """
    # --- Étape 1 : appliquer le pipeline ---
    tensor = preprocess(img)
    # tensor a maintenant la forme (3, 224, 224)

    # --- Étape 2 : ajouter la dimension batch ---
    tensor = tensor.unsqueeze(0)
    # unsqueeze(0) ajoute une dimension au début
    # (3, 224, 224) → (1, 3, 224, 224)
    # Les modèles PyTorch attendent toujours un batch, même de taille 1

    # --- Étape 3 : renvoyer ---
    return tensor