import io
import json
import os
from typing import Any

import httpx

STAGE_MAP = {
    0: "no_dr",
    1: "mild",
    2: "moderate",
    3: "severe",
    4: "proliferative",
}


def _ia_base_url() -> str | None:
    url = os.getenv("AI_SERVICE_URL", "").strip().rstrip("/")
    return url or None


def _pending() -> dict[str, Any]:
    return {
        "status": "pending",
        "stage": None,
        "stage_label": None,
        "confidence": None,
        "image_quality": None,
        "retinal_image_valid": None,
        "refer_to_doctor": None,
        "simulated_constants": None,
        "recommendations": None,
        "patient_message": None,
        "agent_model": None,
        "ia_raw_stage": None,
    }


def _error() -> dict[str, Any]:
    return {
        "status": "error",
        "stage": None,
        "stage_label": None,
        "confidence": None,
        "image_quality": None,
        "retinal_image_valid": None,
        "refer_to_doctor": None,
        "simulated_constants": None,
        "recommendations": None,
        "patient_message": None,
        "agent_model": None,
        "ia_raw_stage": None,
    }


def _analyze_test_scenario() -> dict[str, Any] | None:
    """Réponses figées pour pytest uniquement (variable AI_TEST_SCENARIO)."""
    scenario = os.getenv("AI_TEST_SCENARIO", "").strip().lower()
    if scenario == "rejected":
        return {
            "status": "rejected",
            "stage": None,
            "stage_label": "Image non reconnue",
            "confidence": 0.0,
            "image_quality": "low",
            "retinal_image_valid": False,
            "refer_to_doctor": False,
            "simulated_constants": {},
            "recommendations": [],
            "patient_message": "L'œil n'a pas été détecté.",
            "agent_model": "n/a",
            "ia_raw_stage": -1,
        }
    if scenario == "completed":
        return {
            "status": "completed",
            "stage": "mild",
            "stage_label": "Légère",
            "confidence": 0.42,
            "image_quality": "ok",
            "retinal_image_valid": True,
            "refer_to_doctor": False,
            "simulated_constants": {"clarte_papille": 0.8},
            "recommendations": ["Contrôle glycémie"],
            "patient_message": "Signes légers.",
            "agent_model": "rule-based",
            "ia_raw_stage": 1,
        }
    return None


def analyze_retinal_image(image_bytes: bytes) -> dict[str, Any]:
    '''
    Appelle le service IA (POST /predict) si AI_SERVICE_URL est défini.
    '''
    test_payload = _analyze_test_scenario()
    if test_payload is not None:
        return test_payload

    base = _ia_base_url()
    if not base:
        return _pending()

    timeout = float(os.getenv("AI_SERVICE_TIMEOUT_SEC", "60"))
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                f"{base}/predict",
                files={"image": ("retina.jpg", io.BytesIO(image_bytes), "image/jpeg")},
            )
        if response.status_code != 200:
            return _error()
        data = response.json()
    except httpx.HTTPError:
        return _error()

    if not data.get("is_eye", True):
        return {
            "status": "rejected",
            "stage": None,
            "stage_label": data.get("stage_label"),
            "confidence": data.get("risk_score"),
            "image_quality": "low",
            "retinal_image_valid": False,
            "refer_to_doctor": False,
            "simulated_constants": data.get("simulated_constants"),
            "recommendations": data.get("recommendations"),
            "patient_message": data.get("patient_message"),
            "agent_model": data.get("agent_model"),
            "ia_raw_stage": data.get("stage"),
        }

    stage_num = data.get("stage", 0)
    api_stage = STAGE_MAP.get(stage_num)
    confidence = data.get("risk_score")
    if confidence is not None:
        confidence = float(confidence)

    recommendations = data.get("recommendations")
    constants = data.get("simulated_constants")

    return {
        "status": "completed",
        "stage": api_stage,
        "stage_label": data.get("stage_label"),
        "confidence": confidence,
        "image_quality": "ok",
        "retinal_image_valid": True,
        "refer_to_doctor": bool(data.get("refer_to_doctor")),
        "simulated_constants": constants,
        "recommendations": recommendations,
        "patient_message": data.get("patient_message"),
        "agent_model": data.get("agent_model"),
        "ia_raw_stage": stage_num,
    }


def ai_recommendations_json(ai: dict[str, Any]) -> str | None:
    payload = {
        "simulated_constants": ai.get("simulated_constants"),
        "recommendations": ai.get("recommendations"),
        "refer_to_doctor": ai.get("refer_to_doctor"),
        "stage_label": ai.get("stage_label"),
        "agent_model": ai.get("agent_model"),
        "ia_raw_stage": ai.get("ia_raw_stage"),
    }
    if all(v is None for v in payload.values()):
        return None
    return json.dumps(payload, ensure_ascii=False)
