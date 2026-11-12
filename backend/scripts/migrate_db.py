"""Applique les migrations SQL versionnées (dossier scripts/migrations/)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from sqlalchemy import create_engine, text

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def main() -> int:
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        print("DATABASE_URL manquant.", file=sys.stderr)
        return 1

    files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not files:
        print("Aucune migration trouvée.", file=sys.stderr)
        return 1

    engine = create_engine(database_url)
    for path in files:
        sql = path.read_text(encoding="utf-8")
        print(f"Application de {path.name}…")
        with engine.begin() as conn:
            conn.execute(text(sql))
        print(f"  OK")

    print("Migrations terminées.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
