#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ -f .env ]]; then
  echo ".env existe déjà, rien à faire."
  exit 0
fi

cp .env.example .env

python3 <<'PY'
import secrets
from pathlib import Path
from cryptography.fernet import Fernet

path = Path(".env")
text = path.read_text(encoding="utf-8")
text = text.replace("REPLACE_WITH_RANDOM_SECRET", secrets.token_urlsafe(48), 1)
text = text.replace("REPLACE_WITH_FERNET_KEY", Fernet.generate_key().decode(), 1)
path.write_text(text, encoding="utf-8")
print(".env créé avec des secrets générés.")
PY
