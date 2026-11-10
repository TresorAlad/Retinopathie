from flask import Flask, jsonify, request
import os

from core.image_utils import load_image
from core.inference_mode import resolve_inference_mode
from core.rodium_client import (
    rodium_agent_model,
    rodium_base_url,
    rodium_configured,
    rodium_vision_model,
)

app = Flask(__name__)

EYE_MODEL_PATH = os.getenv("EYE_CHECKER_MODEL_PATH", "models/eye_checker.pt")
STAGE_MODEL_PATH = os.getenv("STAGE_CLASSIFIER_MODEL_PATH", "models/stage_classifier.pt")

_eye_checker = None
_stage_classifier = None


def _local_models_ready() -> bool:
    return os.path.isfile(EYE_MODEL_PATH) and os.path.isfile(STAGE_MODEL_PATH)


def _get_local_pipeline():
    global _eye_checker, _stage_classifier
    if _eye_checker is None:
        from core.eye_checker import EyeChecker
        from core.stage_classifier import StageClassifier

        _eye_checker = EyeChecker(EYE_MODEL_PATH)
        _stage_classifier = StageClassifier(STAGE_MODEL_PATH)
    return _eye_checker, _stage_classifier


@app.route("/health", methods=["GET"])
def health():
    try:
        mode = resolve_inference_mode()
    except RuntimeError as exc:
        return jsonify({"status": "error", "service": "ia", "detail": str(exc)}), 503

    payload = {
        "status": "ok",
        "service": "ia",
        "inference_mode": mode,
        "rodium_configured": rodium_configured(),
        "rodium_base_url": rodium_base_url(),
        "rodium_vision_model": rodium_vision_model(),
        "rodium_agent_model": rodium_agent_model(),
        "local_models_ready": _local_models_ready(),
    }
    return jsonify(payload), 200


@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "champ 'image' manquant"}), 400

    file = request.files["image"]
    if file.content_type not in ("image/jpeg", "image/png"):
        return jsonify({"error": "Format attendu : JPEG ou PNG"}), 400

    raw = file.read()
    if len(raw) > 10 * 1024 * 1024:
        return jsonify({"error": "Image trop lourde (max 10 Mo)"}), 400

    try:
        mode = resolve_inference_mode()
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503

    try:
        if mode == "rodium":
            from core.rodium_vision import analyze_retina_bytes

            vision = analyze_retina_bytes(raw)
        else:
            img = load_image(raw)
            eye_checker, stage_classifier = _get_local_pipeline()
            ok_eye, _prob = eye_checker.is_eye(img)
            if not ok_eye:
                vision = {
                    "is_eye": False,
                    "stage": -1,
                    "stage_label": "Image non reconnue",
                    "risk_score": 0.0,
                    "refer_to_doctor": False,
                }
            else:
                result = stage_classifier.predict(img)
                vision = {"is_eye": True, **result}
    except Exception as exc:
        return jsonify({"error": f"Échec inférence: {exc}"}), 502

    if not vision.get("is_eye"):
        return jsonify({
            "is_eye": False,
            "stage": -1,
            "stage_label": vision.get("stage_label", "Image non reconnue"),
            "risk_score": 0.0,
            "refer_to_doctor": False,
            "model_version": "1.0.0",
            "simulated_constants": {},
            "recommendations": [],
            "patient_message": (
                "L'œil n'a pas été détecté. Reprenez la photo en cadrant le fond d'œil."
            ),
            "agent_model": "n/a",
            "inference_mode": mode,
            "vision_model": vision.get("vision_model"),
        }), 200

    from core.agent import run_agent

    stage = int(vision["stage"])
    agent = run_agent(
        stage,
        vision["stage_label"],
        float(vision["risk_score"]),
    )
    refer = bool(agent.get("refer_to_doctor", vision.get("refer_to_doctor")))

    return jsonify({
        "is_eye": True,
        "stage": stage,
        "stage_label": vision["stage_label"],
        "risk_score": vision["risk_score"],
        "refer_to_doctor": refer,
        "model_version": "1.0.0",
        "simulated_constants": agent.get("simulated_constants", {}),
        "recommendations": agent.get("recommendations", []),
        "patient_message": agent.get("patient_message", ""),
        "agent_model": agent.get("agent_model", "unknown"),
        "inference_mode": mode,
        "vision_model": vision.get("vision_model"),
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
