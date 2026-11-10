# ============================================================
# PACKAGE "tests"
# Ce fichier transforme le dossier "tests/" en package Python.
#
# Pourquoi est-ce utile ?
#   - pytest peut découvrir les tests sans ambiguïté
#   - on peut faire "from tests.helpers import ..." si besoin plus tard
#   - évite les collisions de noms entre test_api.py et d'autres fichiers
#
# Il peut rester vide, mais on va y mettre une petite chose utile :
# ============================================================

# --- Forcer le mode MOCK pour tous les tests ---
# On ne veut PAS que les tests dépendent de vrais modèles .pt
# (ils pourraient ne pas exister ou être lents à charger).
# On force donc IA_MODE=mock AVANT tout import de app.py.
import os
os.environ["IA_MODE"] = "mock"
# os.environ : dictionnaire des variables d'environnement
# On l'écrase AVANT que app.py ne soit importé → app.py lira "mock"


# --- Indiquer à pytest où est la racine du projet ---
# Sans ça, "from core.mock import ..." peut échouer selon le répertoire
# de lancement. On ajoute le dossier parent (ia/) au sys.path.
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
# __file__ = chemin de tests/__init__.py
# .parent = tests/
# .parent.parent = ia/     ← la racine du projet
# .resolve() = chemin absolu propre

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
# sys.path.insert(0, ...) : ajoute le dossier en PREMIER
# → Python trouvera "core/" et "app.py" depuis n'importe où