"""Agent de recommandations via Rodium AI ou enrichissement rule-based."""

import json
import os

from .agent_prompts import SYSTEM_PROMPT, build_user_prompt
from .rodium_client import (
    create_rodium_client,
    rodium_agent_model,
    rodium_configured,
)

_PATIENT_MESSAGES = {
    0: "Aucune anomalie majeure détectée sur cette image. Poursuivez le suivi habituel.",
    1: "Signes légers observés. Un contrôle régulier avec votre médecin est conseillé.",
    2: "Des signes modérés sont présents. Consultez rapidement un ophtalmologue.",
    3: "Signes sévères : consultez un spécialiste en priorité.",
    4: "Signes proliferatifs : consultation urgente recommandée.",
}

_BASE_RECOMMENDATIONS = [
    "Contrôler la glycémie selon l'avis de votre médecin traitant.",
    "Programmer un fond d'œil de contrôle.",
    "Consulter un ophtalmologue si vision floue ou symptômes oculaires.",
]


def _rule_based_enrichment(stage: int, stage_label: str, risk_score: float) -> dict:
    refer = stage >= 2 or risk_score >= 0.55
    return {
        "simulated_constants": {},
        "recommendations": _BASE_RECOMMENDATIONS[: 2 + min(stage, 2)],
        "refer_to_doctor": refer,
        "patient_message": _PATIENT_MESSAGES.get(stage, _PATIENT_MESSAGES[2]),
        "agent_model": "rule-based",
    }


def _rodium_agent(stage: int, stage_label: str, risk_score: float) -> dict:
    if not rodium_configured():
        return _rule_based_enrichment(stage, stage_label, risk_score)

    try:
        client = create_rodium_client()
        model = rodium_agent_model()
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": build_user_prompt(stage, stage_label, risk_score),
                },
            ],
            response_format={"type": "json_object"},
        )
        raw = completion.choices[0].message.content or "{}"
        data = json.loads(raw)
        data.setdefault("refer_to_doctor", stage >= 2)
        data.setdefault("patient_message", _PATIENT_MESSAGES.get(stage, _PATIENT_MESSAGES[2]))
        data.setdefault("simulated_constants", {})
        data.setdefault("recommendations", _BASE_RECOMMENDATIONS[:2])
        data["agent_model"] = model
        return data
    except Exception:
        fallback = _rule_based_enrichment(stage, stage_label, risk_score)
        fallback["agent_model"] = "rule-based-rodium-error"
        return fallback


def run_agent(stage: int, stage_label: str, risk_score: float) -> dict:
    use_rodium = os.getenv("IA_AGENT_MODE", "rodium").lower() in ("rodium", "openai")
    if use_rodium and rodium_configured():
        return _rodium_agent(stage, stage_label, risk_score)
    return _rule_based_enrichment(stage, stage_label, risk_score)
