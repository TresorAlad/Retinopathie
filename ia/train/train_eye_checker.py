# ============================================================
# SCRIPT D'ENTRAINEMENT — DETECTEUR D'OEIL (ResNet18, 2 classes)
# ============================================================
# Objectif : entraîner un modèle qui dit "c'est un fond d'œil" ou pas.
#
# Entrée  : dossiers d'images (train/val), 2 classes : eye / not_eye
# Sortie  : models/eye_checker.pt
#
# Lancement : python train/train_eye_checker.py
# Recommandé : Google Colab (GPU gratuit)
# Durée      : ~5-10 min sur GPU, ~30 min sur CPU
# ============================================================

# --- Imports standards ---
import os
from pathlib import Path

# --- Imports PyTorch ---
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

# --- Imports pour métriques ---
from sklearn.metrics import classification_report, confusion_matrix


# ============================================================
# CONFIGURATION (à adapter selon ton dataset)
# ============================================================
DATA_DIR     = "data/eye_checker"
# Structure attendue :
#   data/eye_checker/train/eye/*.jpg
#   data/eye_checker/train/not_eye/*.jpg
#   data/eye_checker/val/eye/*.jpg
#   data/eye_checker/val/not_eye/*.jpg

MODEL_OUT    = "models/eye_checker.pt"
# Fichier de sortie (chargé par core/eye_checker.py)

IMG_SIZE     = 224
# Taille d'entrée (cohérente avec core/image_utils.py)

BATCH_SIZE   = 32
NUM_EPOCHS   = 5
LEARNING_RATE = 1e-3
# LR élevé : on entraîne ResNet18 sur une tâche binaire simple
# (si ça diverge, baisser à 1e-4)

NUM_WORKERS  = 2
# Nombre de threads pour charger les images (0 sur Windows si souci)


# ============================================================
# DEVICE
# ============================================================
device = "cuda" if torch.cuda.is_available() else "cpu"
# cuda : GPU (Colab, serveur avec GPU)
# cpu  : sinon (lent mais fonctionnel)
print(f"[TRAIN] Device : {device}")


# ============================================================
# TRANSFORMS
# ============================================================
# Train : avec augmentation (le modèle voit des variations)
train_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    # Redimensionne à 224x224

    transforms.RandomHorizontalFlip(),
    # 50% de chance de retourner l'image horizontalement
    # (un œil retourné reste un œil)

    transforms.RandomRotation(10),
    # Rotation aléatoire ±10° (les photos ne sont jamais parfaitement droites)

    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    # Variation légère de luminosité et contraste
    # (différents appareils photo, différentes conditions)

    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    # Mêmes stats ImageNet que core/image_utils.py
])

# Val : SANS augmentation (on mesure les vraies performances)
val_transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


# ============================================================
# DATASETS ET DATALOADERS
# ============================================================
# datasets.ImageFolder : lit automatiquement les sous-dossiers
# "eye" → classe 0, "not_eye" → classe 1 (ordre alphabétique)
train_ds = datasets.ImageFolder(os.path.join(DATA_DIR, "train"), transform=train_transform)
val_ds   = datasets.ImageFolder(os.path.join(DATA_DIR, "val"),   transform=val_transform)

print(f"[TRAIN] Classes      : {train_ds.classes}")
# Affiche ['eye', 'not_eye'] → index 0 = eye, 1 = not_eye
# ⚠️ IMPORTANT : core/eye_checker.py suppose classe 1 = eye !
# Si l'ordre est inversé (not_eye en premier), il faudra adapter
# le code d'inférence ou renommer les dossiers.

print(f"[TRAIN] Train size   : {len(train_ds)}")
print(f"[TRAIN] Val size     : {len(val_ds)}")

train_dl = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True,  num_workers=NUM_WORKERS)
val_dl   = DataLoader(val_ds,   batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)


# ============================================================
# MODELE
# ============================================================
model = models.resnet18(weights="IMAGENET1K_V1")
# weights="IMAGENET1K_V1" : charge les poids pré-entraînés ImageNet
# → le modèle sait déjà "voir" → transfer learning rapide
# (télécharge ~45 Mo la 1ère fois, puis cache)

model.fc = nn.Linear(model.fc.in_features, 2)
# Remplace la dernière couche : 1000 classes → 2 classes
# Même architecture que core/eye_checker.py

model = model.to(device)
print(f"[TRAIN] Modèle prêt : ResNet18 (2 classes)")


# ============================================================
# OPTIMISATION
# ============================================================
criterion = nn.CrossEntropyLoss()
# Loss standard pour classification multi-classes (2 classes ici)

optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
# Adam : converge vite sur du transfer learning

scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=2, gamma=0.5)
# Tous les 2 epochs, LR × 0.5 (1e-3 → 5e-4 → 2.5e-4...)
# Aide à stabiliser la fin de l'entraînement


# ============================================================
# BOUCLE D'ENTRAINEMENT
# ============================================================
best_val_acc = 0.0
# On sauvegarde le modèle seulement s'il bat le meilleur score

for epoch in range(NUM_EPOCHS):
    print(f"\n=== Epoch {epoch + 1}/{NUM_EPOCHS} ===")

    # ---------- PHASE TRAIN ----------
    model.train()
    # Active dropout et batchnorm en mode train

    train_loss = 0.0
    train_correct = 0
    train_total = 0

    for x, y in train_dl:
        x, y = x.to(device), y.to(device)
        # Envoie le batch sur le device

        optimizer.zero_grad()
        # Remet les gradients à zéro (sinon ils s'accumulent)

        logits = model(x)
        # Forward : (batch, 2)

        loss = criterion(logits, y)
        # Calcule la loss

        loss.backward()
        # Backprop : calcule les gradients

        optimizer.step()
        # Met à jour les poids

        # --- Stats ---
        train_loss += loss.item() * x.size(0)
        # .item() : extrait le float du tenseur
        # * x.size(0) : pondère par le nombre d'images du batch

        preds = logits.argmax(dim=1)
        # Prédiction : classe avec la plus grande logit

        train_correct += (preds == y).sum().item()
        train_total += y.size(0)

    train_loss /= train_total
    train_acc = train_correct / train_total
    print(f"  Train  loss={train_loss:.4f}  acc={train_acc:.4f}")

    # ---------- PHASE VALIDATION ----------
    model.eval()
    # Désactive dropout/batchnorm

    val_loss = 0.0
    val_correct = 0
    val_total = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        # Pas de gradients en validation (plus rapide)
        for x, y in val_dl:
            x, y = x.to(device), y.to(device)

            logits = model(x)
            loss = criterion(logits, y)

            val_loss += loss.item() * x.size(0)

            preds = logits.argmax(dim=1)
            val_correct += (preds == y).sum().item()
            val_total += y.size(0)

            all_preds.extend(preds.cpu().numpy().tolist())
            all_labels.extend(y.cpu().numpy().tolist())

    val_loss /= val_total
    val_acc = val_correct / val_total
    print(f"  Val    loss={val_loss:.4f}  acc={val_acc:.4f}")

    scheduler.step()
    # Ajuste le LR selon la stratégie

    # ---------- SAUVEGARDE DU MEILLEUR MODELE ----------
    if val_acc > best_val_acc:
        best_val_acc = val_acc

        os.makedirs("models", exist_ok=True)
        # Crée le dossier models/ s'il n'existe pas

        torch.save(model.state_dict(), MODEL_OUT)
        # state_dict() : dict {nom_couche: tenseur de poids}
        # C'est ce que core/eye_checker.py chargera

        print(f"  ✓ Nouveau meilleur modèle sauvegardé (val_acc={val_acc:.4f})")


# ============================================================
# RAPPORT FINAL
# ============================================================
print("\n" + "=" * 60)
print(f"Entraînement terminé. Meilleure val_acc : {best_val_acc:.4f}")
print(f"Modèle sauvegardé : {MODEL_OUT}")
print("=" * 60)

# Matrice de confusion + rapport détaillé
print("\n--- Rapport détaillé sur la validation ---")
print(f"Classes : {train_ds.classes}")
print("\nConfusion matrix :")
print(confusion_matrix(all_labels, all_preds))
print("\nClassification report :")
print(classification_report(all_labels, all_preds, target_names=train_ds.classes))