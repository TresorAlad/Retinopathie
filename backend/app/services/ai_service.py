import io
import os

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


def _pending() -> dict:
    return {
        "status": "pending",
        "stage": None,
        "confidence": None,
        "image_quality": None,
        "retinal_image_valid": None,
    }


def analyze_retinal_image(image_bytes: bytes) -> dict:
    '''
    Appelle le service IA (dossier `ia/`, POST /predict) si AI_SERVICE_URL est défini.
    Sinon le dépistage reste en attente (`pending`).
    '''
    base = _ia_base_url()
    if not base:
        return _pending()

    timeout = float(os.getenv("AI_SERVICE_TIMEOUT_SEC", "30"))
    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                f"{base}/predict",
                files={"image": ("retina.jpg", io.BytesIO(image_bytes), "image/jpeg")},
            )
        if response.status_code != 200:
            return {
                "status": "error",
                "stage": None,
                "confidence": None,
                "image_quality": None,
                "retinal_image_valid": None,
            }
        data = response.json()
    except httpx.HTTPError:
        return {
            "status": "error",
            "stage": None,
            "confidence": None,
            "image_quality": None,
            "retinal_image_valid": None,
        }

    if not data.get("is_eye", True):
        return {
            "status": "rejected",
            "stage": None,
            "confidence": data.get("risk_score"),
            "image_quality": "low",
            "retinal_image_valid": False,
        }

    stage_num = data.get("stage", 0)
    api_stage = STAGE_MAP.get(stage_num)
    confidence = data.get("risk_score")
    if confidence is not None:
        confidence = float(confidence)

    return {
        "status": "completed",
        "stage": api_stage,
        "confidence": confidence,
        "image_quality": "ok",
        "retinal_image_valid": True,
    }
