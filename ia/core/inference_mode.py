import os

from .rodium_client import rodium_configured


def resolve_inference_mode() -> str:
    """
    rodium : API Rodium AI (vision hébergée).
    local  : PyTorch local (models/*.pt).
    auto   : rodium si RODIUMAI_API_KEY, sinon local.
    """
    mode = os.getenv("IA_INFERENCE_MODE", "auto").strip().lower()
    if mode == "rodium":
        if not rodium_configured():
            raise RuntimeError(
                "IA_INFERENCE_MODE=rodium mais RODIUMAI_API_KEY est vide."
            )
        return "rodium"
    if mode == "local":
        return "local"
    if rodium_configured():
        return "rodium"
    return "local"
