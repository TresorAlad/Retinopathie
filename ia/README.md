# Service IA — Dépistage de la Rétinopathie Diabétique

Micro-service Flask qui reçoit une photo de rétine et renvoie un diagnostic IA :
- **Étape 1** : vérifier que l'image est un vrai fond d'œil
- **Étape 2** : classifier le stade de rétinopathie (0 à 4)
- **Étape 3 (agent)** : recommandations et `patient_message` (OpenAI si clé, sinon règles métier)
- **Sortie** : JSON avec `is_eye`, `stage`, `stage_label`, `risk_score`, `refer_to_doctor`, champs agent

> **Avertissement** : démonstration pédagogique, pas un dispositif médical. Les constantes renvoyées par l'agent sont **simulées**, pas des mesures cliniques.

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

### Rodium AI (recommandé pour tester)

API compatible OpenAI : [rodiumai.io](https://www.rodiumai.io).

```bash
cd ia
cp .env.example .env
# Renseigner RODIUMAI_API_KEY dans .env

export RODIUMAI_API_KEY=rd_sk_votre_cle
export IA_INFERENCE_MODE=rodium
export IA_AGENT_MODE=rodium
python app.py
```

Test rapide :

```bash
curl http://localhost:8001/health
curl -X POST http://localhost:8001/predict -F "image=@chemin/vers/retine.jpg"
```

Variables principales : `RODIUMAI_API_KEY`, `RODIUMAI_BASE_URL`, `RODIUMAI_VISION_MODEL` (ex. `openai/gpt-4o`), `RODIUMAI_AGENT_MODEL` (ex. `openai/gpt-4o-mini`).

Avec `IA_INFERENCE_MODE=auto`, la clé Rodium suffit (pas besoin de fichiers `.pt`).

### PyTorch local (optionnel)

```bash
export IA_INFERENCE_MODE=local
# models/eye_checker.pt et models/stage_classifier.pt requis
python app.py
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
{
  "status": "ok",
  "service": "ia",
  "inference_mode": "rodium",
  "rodium_configured": true,
  "rodium_vision_model": "openai/gpt-4o"
}
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
│   ├── agent.py              # Étape 3 : enrichissement
│   └── agent_prompts.py
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
| `RODIUMAI_API_KEY` | (requis mode rodium) | Clé API Rodium |
| `RODIUMAI_BASE_URL` | `https://api.rodiumai.io/v1` | Point d'entrée compatible OpenAI |
| `RODIUMAI_VISION_MODEL` | `openai/gpt-4o` | Modèle vision (détection œil + stade) |
| `RODIUMAI_AGENT_MODEL` | `openai/gpt-4o-mini` | Modèle agent recommandations |
| `IA_INFERENCE_MODE` | `auto` | `rodium`, `local` ou `auto` |
| `IA_AGENT_MODE` | `rodium` | `rodium` ou `rule-based` |
| `EYE_CHECKER_MODEL_PATH` | `models/eye_checker.pt` | Mode local uniquement |
| `STAGE_CLASSIFIER_MODEL_PATH` | `models/stage_classifier.pt` | Mode local uniquement |

Fichiers agent : `core/agent.py`, `core/agent_prompts.py`.

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

```bash
docker run -p 8001:8001 -v $(pwd)/models:/app/models rd-ia
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
| `simulated_constants` | object | Constantes pédagogiques simulées (non cliniques) |
| `recommendations` | array | 2 à 5 actions suggérées |
| `patient_message` | str | Texte court pour l'écran mobile |
| `agent_model` | str | `rule-based`, modèle OpenAI, etc. |
| `model_version` | str | Version du pipeline (traçabilité) |

---

## 10. Équipe

- **Rôle** : partie IA (membre 6/6)
- **Contact** : via le Master du projet