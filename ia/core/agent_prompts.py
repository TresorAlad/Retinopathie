"""Prompts pour l'agent de recommandation (démo, pas un dispositif médical)."""

SYSTEM_PROMPT = """Tu es un assistant pédagogique pour le dépistage de la rétinopathie diabétique.
Tu ne poses pas de diagnostic clinique définitif. Tu fournis une simulation de constantes
d'observation et des recommandations générales pour la démo technique.
Réponds UNIQUEMENT en JSON valide, sans markdown."""


def build_user_prompt(stage: int, stage_label: str, risk_score: float) -> str:
    return (
        f"Stade estimé par le classifieur: {stage} ({stage_label}), "
        f"score de risque: {risk_score:.4f}. "
        "Génère un JSON avec les clés: "
        "simulated_constants (objet avec 3 clés courtes en français snake_case), "
        "recommendations (liste de 2 à 4 chaînes courtes en français), "
        "refer_to_doctor (booléen, true si stade >= 2), "
        "patient_message (une phrase simple en français pour le patient)."
    )
