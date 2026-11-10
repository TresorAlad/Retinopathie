        ┌──────────────────────────────┐
        │  MOBILE (Flutter)            │
        │  → le patient prend la photo │
        └──────────────┬───────────────┘
                       │ envoie la photo
                       ▼
        ┌──────────────────────────────┐
        │  BACKEND (FastAPI/Flask)     │
        │  → reçoit la photo           │
        │  → l'envoie à l'IA           │
        │  → stocke (chiffré)          │
        │  → renvoie le résultat       │
        └──────┬─────────────────┬─────┘
               │                 │
               ▼                 ▼
    ┌──────────────────┐  ┌──────────────────┐
    │  IA (PyTorch)    │  │  BLOCKCHAIN      │
    │  → est-ce un œil │  │  → mobile_scan   │
    │  → quel stade ?  │  │    1 bloc/scan   │
    │  → agent OpenAI  │  │  → ancrages      │
    │    ou rule-based │  │    médecin       │
    └──────────────────┘  └──────────────────┘
               ▲
               │ le médecin valide
    ┌──────────────────────────────┐
    │  WEB DOCTEUR (React)         │
    │  → voit la liste des cas     │
    │  → valide ou corrige le      │
    │    diagnostic de l'IA        │
    └──────────────────────────────┘