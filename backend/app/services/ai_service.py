def analyze_retinal_image(image_bytes: bytes) -> dict:
    '''
    Point d'intégration avec le module IA de l'équipe.
    Tant que le contrat IA (URL/fonction, format entrée/sortie) n'est pas fourni,
    aucune prédiction n'est inventée : le dépistage reste en attente.
    '''
    return {
        "status": "pending",
        "stage": None,
        "confidence": None,
        "image_quality": None,
        "retinal_image_valid": None,
    }
