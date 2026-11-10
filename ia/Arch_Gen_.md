# Architecture service IA

```
Mobile / Backend
       │
       ▼
  Flask app.py  (POST /predict)
       │
       ├── Rodium vision (openai/gpt-4o) → is_eye, stade 0-4
       └── Rodium agent → recommandations, patient_message
```

Clé : `RODIUMAI_API_KEY` (voir `ia/.env.example`).

Le backend consomme `AI_SERVICE_URL=http://ia:8001`.
