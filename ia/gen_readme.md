
### Détail fichier par fichier

| Fichier | Rôle |
|---------|------|
| `app.py` | **Point d'entrée du service.** Crée l'application Flask, charge le bon jeu de modèles selon `IA_MODE` (mock ou prod), expose les routes `GET /health` et `POST /predict`, valide l'image reçue et renvoie le JSON du contrat. |
| `requirements.txt` | **Dépendances Python** du service, avec versions figées (Flask, Pillow, PyTorch, torchvision, pytest…). Sert à `pip install -r requirements.txt`. |
| `Dockerfile` | **Recette de construction de l'image Docker** du service. Expose le port 8001 et lance `python app.py`. Utilisé par `docker build` et `docker-compose`. |
| `README.md` | Ce fichier : documentation du service. |
| `core/__init__.py` | Transforme `core/` en package Python. Permet `from core.xxx import Yyy`. Version légère (n'importe pas PyTorch au démarrage). |
| `core/image_utils.py` | **Outils de prétraitement d'image.** `load_image(bytes)` convertit les bytes reçus en `PIL.Image` RGB ; `to_tensor(img)` applique resize 224×224, normalisation ImageNet et ajoute la dimension batch. Indépendant de Flask. |
| `core/eye_checker.py` | **Étape 1 : détecteur d'œil (vrai modèle).** Classe `EyeChecker` basée sur ResNet18 (2 classes : eye / not_eye). Charge `models/eye_checker.pt` et expose `is_eye(img) → (bool, prob_eye)`. Utilisé quand `IA_MODE=prod`. |
| `core/stage_classifier.py` | **Étape 2 : classifieur de stade (vrai modèle).** Classe `StageClassifier` basée sur ResNet50 (5 classes : stades 0 à 4). Charge `models/stage_classifier.pt` et expose `predict(img) → {stage, stage_label, risk_score, refer_to_doctor}`. Utilisé quand `IA_MODE=prod`. |
| `core/mock.py` | **Réponses simulées (mode mock).** Classes `MockEyeChecker` et `MockStageClassifier` qui renvoient des réponses déterministes (basées sur un hash de l'image). Permet de débloquer l'équipe sans modèle entraîné. Utilisé quand `IA_MODE=mock` (défaut). |
| `models/` | Dossier vide au départ. Recevra `eye_checker.pt` et `stage_classifier.pt` produits par les scripts `train/`. Nécessaire au mode `prod`. |
| `data/samples/` | Dossier vide au départ. À remplir avec des images de test (yeux normaux, yeux pathologiques, image non-œil) pour tester manuellement avec `curl`. |
| `tests/__init__.py` | Force `IA_MODE=mock` **avant** tout import de `app.py`, et ajoute la racine du projet au `sys.path` pour que `from core.xxx import ...` et `from app import app` fonctionnent depuis n'importe quel répertoire. |
| `tests/test_api.py` | **Tests HTTP de l'API Flask.** Vérifie `/health`, la présence de tous les champs du contrat, le rejet des non-yeux, les codes 400, la cohérence `stage >= 2 ⇒ refer_to_doctor` et le déterminisme des réponses. |
| `tests/test_core.py` | **Tests unitaires des modules `core/`.** Vérifie `load_image`, `to_tensor`, `MockEyeChecker`, `MockStageClassifier` : types, bornes, déterminisme, règle `refer_to_doctor`. |
| `train/train_eye_checker.py` | **Script d'entraînement de l'étape 1.** Charge les images `eye/` et `not_eye/`, entraîne ResNet18 (5 epochs), affiche matrice de confusion et rapport, sauvegarde `models/eye_checker.pt`. À lancer sur Colab. |
| `train/train_stage_classifier.py` | **Script d'entraînement de l'étape 2.** Charge les images APTOS (5 stades), calcule des poids de classe (déséquilibre), entraîne ResNet50 (15 epochs), affiche matrice de confusion et recall stade ≥ 2, sauvegarde `models/stage_classifier.pt`. À lancer sur Colab. |

---

## Prérequis

- Python 3.11
- pip
- (optionnel) Docker

---

## Installation locale

```bash
cd ia
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1     # Windows
# source venv/bin/activate      # Linux / macOS
pip install -r requirements.txt