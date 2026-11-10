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
    │  → est-ce un œil │  │  → enregistre    │
    │  → quel stade ?  │  │    la validation │
    │  → score risque  │  │  → garantit la   │
    └──────────────────┘  │    traçabilité   │
                          └──────────────────┘
               ▲
               │ le médecin valide
    ┌──────────────────────────────┐
    │  WEB DOCTEUR (React)         │
    │  → voit la liste des cas     │
    │  → valide ou corrige le      │
    │    diagnostic de l'IA        │
    └──────────────────────────────┘