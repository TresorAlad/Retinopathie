# Service IA

Flask sur le port **8001**. Toute l'inférence passe par **Rodium AI** (API compatible OpenAI).

## Installation

```bash
cd ia
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # RODIUMAI_API_KEY
python app.py
```

## Test

```bash
curl http://localhost:8001/health
curl -X POST http://localhost:8001/predict -F "image=@retine.jpg"
```

## Variables

| Variable | Défaut | Description |
|----------|--------|-------------|
| `RODIUMAI_API_KEY` | - | Obligatoire |
| `RODIUMAI_BASE_URL` | `https://api.rodiumai.io/v1` | Base API |
| `RODIUMAI_VISION_MODEL` | `openai/gpt-4o` | Analyse image |
| `RODIUMAI_AGENT_MODEL` | `openai/gpt-4o-mini` | Texte patient |

Catalogue : https://www.rodiumai.io/docs/models

## Tests

```bash
pytest tests/ -q
```

Le test live `/predict` ne s'exécute que si `RODIUMAI_API_KEY` est défini.

> Démonstration pédagogique, pas un dispositif médical.
