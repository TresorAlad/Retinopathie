# Service IA — Dépistage de la Rétinopathie Diabétique

Micro-service Flask qui reçoit une photo de rétine et renvoie un diagnostic IA :
- **Étape 1** : vérifier que l'image est un vrai fond d'œil
- **Étape 2** : classifier le stade de rétinopathie (0 à 4)
- **Sortie** : JSON avec `is_eye`, `stage`, `stage_label`, `risk_score`, `refer_to_doctor`

---

## 1. Prérequis

- Python 3.11+
- pip
- (optionnel) Docker

---

## 2. Installation locale

```bash
# Se placer dans le dossier ia/
cd ia

# Créer un environnement virtuel (recommandé)
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

---

## 3. Lancement

### Mode MOCK (par défaut — aucune IA, réponses simulées)

```bash
# Windows
set IA_MODE=mock
python app.py

# Linux / macOS
IA_MODE=mock python app.py
```

### Mode PROD (avec les vrais modèles)

```bash
# Nécessite models/eye_checker.pt et models/stage_classifier.pt
# Windows
set IA_MODE=prod
python app.py

# Linux / macOS
IA_MODE=prod python app.py
```

Le service écoute sur **http://localhost:8001**.

---

## 4. Endpoints

### `GET /health`
Vérifie que le service tourne.

```bash
curl http://localhost:8001/health
```

Réponse :
```json
{ "status": "ok", "service": "ia", "mode": "mock" }
```

---

### `POST /predict`
Reçoit une image (multipart/form-data, champ `image`) et renvoie le diagnostic.

```bash
curl -X POST http://localhost:8001/predict \
     -F "image=@data/samples/eye_stage2.jpg"
```

Réponse (image valide) :
```json
{
  "is_eye": true,
  "stage": 2,
  "stage_label": "Modérée",
  "risk_score": 0.72,
  "refer_to_doctor": true,
  "model_version": "1.0.0"
}
```

Réponse (image non reconnue) :
```json
{
  "is_eye": false,
  "stage": -1,
  "stage_label": "Image non reconnue",
  "risk_score": 0.0,
  "refer_to_doctor": false,
  "model_version": "1.0.0"
}
```

Erreurs possibles :
| Code | Cause |
|------|-------|
| 400  | champ `image` manquant / format non JPEG-PNG / image > 10 Mo / image illisible |

---

## 5. Structure du projet

```
ia/
├── app.py                    # Point d'entrée Flask
├── requirements.txt          # Dépendances Python
├── Dockerfile                # Image Docker
├── README.md                 # Ce fichier
│
├── core/                     # Logique IA (sans Flask)
│   ├── __init__.py
│   ├── image_utils.py        # Chargement + prétraitement image
│   ├── eye_checker.py        # Étape 1 : est-ce un œil ?
│   ├── stage_classifier.py   # Étape 2 : quel stade ?
│   └── mock.py               # Réponses simulées (mode mock)
│
├── models/                   # Modèles entraînés (.pt)
│   ├── eye_checker.pt
│   └── stage_classifier.pt
│
├── data/samples/             # Images de test manuelles
│
├── tests/                    # Tests pytest
│   ├── test_api.py
│   └── test_core.py
│
└── train/                    # Scripts d'entraînement (offline)
    ├── train_eye_checker.py
    └── train_stage_classifier.py
```

---

## 6. Variables d'environnement

| Variable | Valeur | Effet |
|----------|--------|-------|
| `IA_MODE` | `mock` (défaut) | Réponses simulées, aucune IA chargée |
| `IA_MODE` | `prod` | Charge les vrais modèles depuis `models/` |

---

## 7. Tests

```bash
# Depuis le dossier ia/, environnement activé
pytest tests/ -v
```

---

## 8. Docker

### Build

```bash
docker build -t rd-ia .
```

### Run (mode mock)

```bash
docker run -p 8001:8001 -e IA_MODE=mock rd-ia
```

### Run (mode prod, avec les modèles montés)

```bash
docker run -p 8001:8001 -e IA_MODE=prod \
           -v $(pwd)/models:/app/models rd-ia
```

---

## 9. Contrat API (rappel)

Le backend appelle **`POST http://ia:8001/predict`** avec :
- Content-Type : `multipart/form-data`
- Champ : `image` (fichier JPEG ou PNG, max 10 Mo)
- Timeout recommandé : 30 s

Champs de la réponse (tous obligatoires) :

| Champ | Type | Description |
|-------|------|-------------|
| `is_eye` | bool | L'image est-elle un fond d'œil ? |
| `stage` | int | 0..4 (ou -1 si `is_eye=false`) |
| `stage_label` | str | Libellé lisible du stade |
| `risk_score` | float | 0.0..1.0 — P(stade ≥ 2) |
| `refer_to_doctor` | bool | `true` si `stage >= 2` |
| `model_version` | str | Version du modèle (traçabilité) |

---

## 10. Équipe

- **Rôle** : partie IA (membre 6/6)
- **Contact** : via le Master du projet