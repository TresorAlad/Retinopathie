# ============================================================
# IMAGE DOCKER DU SERVICE IA
# Construit une image légère (slim) qui lance Flask sur le port 8001
# Build   : docker build -t rd-ia .
# Run     : docker run -p 8001:8001 -e IA_MODE=mock rd-ia
# ============================================================

# --- Image de base ---
FROM python:3.11-slim
# python:3.11-slim = Python 3.11 sans outils inutiles (image ~120 Mo)
# 3.11 est compatible avec torch 2.3 et torchvision 0.18

# --- Métadonnées (bonnes pratiques) ---
LABEL maintainer="equipe-ia"
LABEL description="Service IA de depistage de la retinopathie diabetique"

# --- Répertoire de travail dans le conteneur ---
WORKDIR /app
# Tous les ordres suivants (COPY, RUN, CMD) s'exécutent dans /app

# --- Variables d'environnement Python ---
ENV PYTHONDONTWRITEBYTECODE=1
# Empêche Python de créer des fichiers .pyc (inutiles en Docker)

ENV PYTHONUNBUFFERED=1
# Force les prints à sortir immédiatement dans les logs Docker
# (sinon ils sont bufferisés et on ne voit rien)

# --- Variables d'environnement du service ---
ENV IA_MODE=mock
# Mode par défaut : mock (remplaçable au run via -e IA_MODE=prod)

# --- Installation des dépendances système ---
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
# libgl1 et libglib2.0-0 : requis par Pillow et torch pour ouvrir les images
# --no-install-recommends : n'installe que le strict nécessaire
# rm -rf /var/lib/apt/lists/* : nettoie les index apt (image plus légère)

# --- Copier uniquement requirements.txt d'abord (cache Docker) ---
COPY requirements.txt .
# On copie requirements.txt SEUL avant le code :
# si le code change mais pas les dépendances, Docker réutilise le cache
# → build beaucoup plus rapide les fois suivantes

# --- Installer les dépendances Python ---
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
# --no-cache-dir : ne conserve pas les fichiers pip (image plus légère)
# --upgrade pip : s'assure d'avoir la dernière version de pip

# --- Copier le code de l'application ---
COPY app.py .
# Le fichier Flask principal

COPY core/ ./core/
# Le dossier core/ (eye_checker, stage_classifier, image_utils, mock)

COPY models/ ./models/
# Les modèles .pt (peuvent être vides en mode mock)
# En prod, il faut que models/ contienne eye_checker.pt et stage_classifier.pt

# --- Exposer le port ---
EXPOSE 8001
# Documente le port utilisé (n'ouvre pas réellement le port, c'est pour la doc)

# --- Commande de démarrage ---
CMD ["python", "app.py"]
# Lance Flask via python app.py (host=0.0.0.0, port=8001, debug=True dans app.py)
# En production réelle, on utiliserait plutôt :
#   CMD ["gunicorn", "-b", "0.0.0.0:8001", "-w", "2", "app:app"]
# Mais pour un hackathon, python app.py est suffisant et plus simple