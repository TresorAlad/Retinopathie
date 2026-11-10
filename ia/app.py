from flask import Flask, jsonify, request

from core.image_utils import load_image
from core.rodium_client import (
    rodium_agent_model,
    rodium_base_url,
    rodium_configured,
    rodium_vision_model,
)

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "ia",
        "inference": "rodium",
        "rodium_configured": rodium_configured(),
        "rodium_base_url": rodium_base_url(),
        "rodium_vision_model": rodium_vision_model(),
        "rodium_agent_model": rodium_agent_model(),
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    if not rodium_configured():
        return jsonify({"error": "RODIUMAI_API_KEY non configurée."}), 503

    if "image" not in request.files:
        return jsonify({"error": "champ 'image' manquant"}), 400

    file = request.files["image"]
    if file.content_type not in ("image/jpeg", "image/png"):
        return jsonify({"error": "Format attendu : JPEG ou PNG"}), 400

    raw = file.read()
    if len(raw) > 10 * 1024 * 1024:
        return jsonify({"error": "Image trop lourde (max 10 Mo)"}), 400

    try:
        load_image(raw)
    except Exception:
        return jsonify({"error": "Image illisible"}), 400

    try:
        from core.rodium_vision import analyze_retina_bytes

        vision = analyze_retina_bytes(raw)
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
        "vision_model": vision.get("vision_model"),
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
