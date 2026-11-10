# Fichiers du service IA

| Fichier | Rôle |
|---------|------|
| `app.py` | Flask `/health` et `/predict`. |
| `core/rodium_client.py` | Client OpenAI vers Rodium AI. |
| `core/rodium_vision.py` | Détection œil + stade via modèle vision Rodium. |
| `core/inference_mode.py` | `rodium`, `local` ou `auto`. |
| `core/agent.py` | Recommandations via Rodium ou rule-based. |
| `core/eye_checker.py` | Mode local PyTorch. |
| `core/stage_classifier.py` | Mode local PyTorch. |
| `.env.example` | Modèle de configuration Rodium. |
