# ============================================================
# POINT D'ENTREE DU SERVICE IA
# Rôle : recevoir une image du backend et renvoyer un JSON
# Lancement : python app.py
# ============================================================

# --- Imports Flask ---
from flask import Flask, request, jsonify
# Flask     : le framework web
# request   : pour accéder aux fichiers envoyés (multipart/form-data)
# jsonify   : transforme un dict Python en réponse JSON

# --- Imports système ---
import os
# os : lire les variables d'environnement (ex: IA_MODE)

# --- Imports internes (nos propres modules) ---
from core.image_utils import load_image
# load_image : transforme des bytes en image PIL exploitable


# ============================================================
# CREATION DE L'APPLICATION FLASK
# ============================================================
app = Flask(__name__)
# __name__ = nom du module courant ("app")
# Flask s'en sert pour localiser les fichiers statiques, etc.


# ============================================================
# CHARGEMENT DES MODELES (UNE SEULE FOIS au démarrage)
# ============================================================
# On lit la variable d'environnement IA_MODE :
#   - "mock" : réponses simulées (jour 1, pour débloquer l'équipe)
#   - "prod" : vrais modèles entraînés (chargés depuis models/*.pt)
# Si la variable n'existe pas → "mock" par défaut (sécurisé).

IA_MODE = os.getenv("IA_MODE", "mock")

if IA_MODE == "mock":
    # --- Mode MOCK : pas de PyTorch, réponses simulées ---
    from core.mock import MockEyeChecker, MockStageClassifier
    eye_checker = MockEyeChecker()
    # eye_checker : instance qui répond "est-ce un œil ?"
    stage_classifier = MockStageClassifier()
    # stage_classifier : instance qui répond "quel stade ?"
    print("[IA] Mode MOCK activé (aucun modèle chargé)")
else:
    # --- Mode PROD : vrais modèles PyTorch ---
    from core.eye_checker import EyeChecker
    from core.stage_classifier import StageClassifier
    eye_checker = EyeChecker("models/eye_checker.pt")
    # charge le modèle binaire (œil / pas œil)
    stage_classifier = StageClassifier("models/stage_classifier.pt")
    # charge le modèle 5 classes (stade 0..4)
    print("[IA] Modèles réels chargés")


# ============================================================
# ROUTE 1 : GET /health
# Sert à vérifier que le service tourne (ping du backend / Docker)
# ============================================================
@app.route("/health", methods=["GET"])
def health():
    # @app.route : associe une URL à une fonction
    # methods=["GET"] : uniquement accessible en GET
    return jsonify({
        "status": "ok",       # toujours "ok" si on arrive ici
        "service": "ia",      # nom du service (utile dans les logs)
        "mode": IA_MODE,      # "mock" ou "prod" (visible pour debug)
    }), 200
    # 200 = succès HTTP


# ============================================================
# ROUTE 2 : POST /predict
# Reçoit une image de rétine, renvoie le diagnostic IA
# ============================================================
@app.route("/predict", methods=["POST"])
def predict():
    # ----- ETAPE A : vérifier qu'une image est bien envoyée -----
    if "image" not in request.files:
        # request.files contient les fichiers du multipart
        # Si "image" n'est pas présent → erreur client
        return jsonify({"error": "champ 'image' manquant"}), 400
        # 400 = Bad Request

    file = request.files["image"]
    # file = objet FileStorage (bytes + nom + content_type)

    # ----- ETAPE B : vérifier le type MIME -----
    if file.content_type not in ("image/jpeg", "image/png"):
        # On n'accepte que JPEG et PNG (formats d'appareil photo / mobile)
        return jsonify({"error": "Format attendu : JPEG ou PNG"}), 400

    # ----- ETAPE C : lire les bytes et vérifier la taille -----
    raw = file.read()
    # raw = contenu binaire de l'image (bytes)

    if len(raw) > 10 * 1024 * 1024:
        # 10 * 1024 * 1024 = 10 Mo
        # Au-delà, on refuse pour ne pas saturer le serveur
        return jsonify({"error": "Image trop lourde (max 10 Mo)"}), 400

    # ----- ETAPE D : convertir les bytes en image PIL -----
    try:
        img = load_image(raw)
        # img = objet PIL.Image en RGB, prêt pour les modèles
    except Exception:
        # Si Pillow n'arrive pas à ouvrir le fichier (corrompu, etc.)
        return jsonify({"error": "Image illisible"}), 400

    # ----- ETAPE E : ETAPE 1 - est-ce un vrai œil ? -----
    ok_eye, prob_eye = eye_checker.is_eye(img)
    # ok_eye   : True si c'est un fond d'œil, False sinon
    # prob_eye : probabilité entre 0.0 et 1.0 (pour debug / logs)

    if not ok_eye:
        # Si ce n'est pas un œil → on renvoie un rejet propre
        return jsonify({
            "is_eye": False,                      # signal clair au backend
            "stage": -1,                          # -1 = non applicable
            "stage_label": "Image non reconnue",  # libellé lisible
            "risk_score": 0.0,                    # pas de risque calculé
            "refer_to_doctor": False,             # pas de référence médecin
            "model_version": "1.0.0",             # traçabilité (obligatoire)
        }), 200

    # ----- ETAPE F : ETAPE 2 - quel stade de rétinopathie ? -----
    result = stage_classifier.predict(img)
    # result = dict contenant :
    #   stage            (0..4)
    #   stage_label      ("Légère", ...)
    #   risk_score       (P(stage >= 2))
    #   refer_to_doctor  (True si stage >= 2)

    # ----- ETAPE G : construire et renvoyer le JSON final -----
    return jsonify({
        "is_eye": True,           # oui, c'est un œil valide
        **result,                 # on "étale" le dict du classifieur
        "model_version": "1.0.0", # traçabilité du modèle
    }), 200
    # 200 = succès


# ============================================================
# LANCEMENT DU SERVEUR (uniquement si exécuté directement)
# ============================================================
if __name__ == "__main__":
    # host="0.0.0.0" : accepte les connexions externes (nécessaire en Docker)
    # port=8001       : port convenu avec le Master / backend
    # debug=True      : recharge auto + stack traces détaillées (DEV uniquement)
    app.run(host="0.0.0.0", port=8001, debug=True)