"""Analyse fond d'œil via modèle vision Rodium AI."""

import base64
import json
import re
from typing import Any

from .rodium_client import create_rodium_client, rodium_vision_model
from .stage_classifier import STAGE_LABELS

VISION_SYSTEM = """Tu analyses des images pour le dépistage de la rétinopathie diabétique.
Tu ne poses pas de diagnostic médical définitif ; tu estimes à partir de l'image.
Réponds UNIQUEMENT avec un objet JSON valide, sans markdown ni texte autour.

Règles:
- is_eye: true seulement si l'image ressemble à un fond d'œil (rétine).
- Si ce n'est pas un fond d'œil: is_eye=false, stage=-1, stage_label="Image non reconnue",
  risk_score=0.0, refer_to_doctor=false, prob_eye=0.0
- Sinon stage entier 0 à 4 (ETDRS simplifié), stage_label parmi les libellés français fournis.
- risk_score: float 0.0 à 1.0, interprété comme probabilité que stage >= 2.
- refer_to_doctor: true si stage >= 2.
- prob_eye: confiance 0.0 à 1.0 que l'image est un fond d'œil.

Libellés: 0 "Pas de rétinopathie", 1 "Légère", 2 "Modérée", 3 "Sévère", 4 "Proliférative"."""


def _mime_from_bytes(raw: bytes) -> str:
    if raw[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    return "image/jpeg"


def _parse_json_content(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def analyze_retina_bytes(raw: bytes) -> dict[str, Any]:
    """
    Appelle Rodium AI et renvoie le contrat aligné sur /predict.
    """
    b64 = base64.b64encode(raw).decode("ascii")
    mime = _mime_from_bytes(raw)
    client = create_rodium_client()
    model = rodium_vision_model()

    completion = client.chat.completions.create(
        model=model,
        temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": VISION_SYSTEM},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyse cette image de fond d'œil. "
                            "Clés JSON: is_eye, prob_eye, stage, stage_label, "
                            "risk_score, refer_to_doctor."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64}", "detail": "high"},
                    },
                ],
            },
        ],
    )
    content = completion.choices[0].message.content or "{}"
    data = _parse_json_content(content)

    is_eye = bool(data.get("is_eye", False))
    if not is_eye:
        return {
            "is_eye": False,
            "stage": -1,
            "stage_label": data.get("stage_label") or "Image non reconnue",
            "risk_score": 0.0,
            "refer_to_doctor": False,
            "vision_model": model,
        }

    stage = int(data.get("stage", 0))
    if stage < 0 or stage > 4:
        stage = max(0, min(4, stage))
    stage_label = data.get("stage_label") or STAGE_LABELS.get(stage, "Inconnu")
    if stage_label not in STAGE_LABELS.values():
        stage_label = STAGE_LABELS.get(stage, stage_label)

    risk = float(data.get("risk_score", 0.0))
    risk = max(0.0, min(1.0, risk))
    refer = bool(data.get("refer_to_doctor", stage >= 2))

    return {
        "is_eye": True,
        "stage": stage,
        "stage_label": stage_label,
        "risk_score": round(risk, 4),
        "refer_to_doctor": refer,
        "vision_model": model,
    }
