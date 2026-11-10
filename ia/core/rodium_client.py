"""Client HTTP Rodium AI (API compatible OpenAI)."""

import os

RODIUMAI_DEFAULT_BASE_URL = "https://api.rodiumai.io/v1"
RODIUMAI_DEFAULT_VISION_MODEL = "openai/gpt-4o"


def rodium_api_key() -> str:
    return os.getenv("RODIUMAI_API_KEY", "").strip()


def rodium_configured() -> bool:
    return bool(rodium_api_key())


def rodium_base_url() -> str:
    return os.getenv("RODIUMAI_BASE_URL", RODIUMAI_DEFAULT_BASE_URL).strip().rstrip("/")


def rodium_vision_model() -> str:
    return os.getenv("RODIUMAI_VISION_MODEL", RODIUMAI_DEFAULT_VISION_MODEL).strip()


def rodium_agent_model() -> str:
    return os.getenv(
        "RODIUMAI_AGENT_MODEL",
        os.getenv("RODIUMAI_VISION_MODEL", RODIUMAI_DEFAULT_VISION_MODEL),
    ).strip()


def create_rodium_client():
    from openai import OpenAI

    key = rodium_api_key()
    if not key:
        raise RuntimeError("RODIUMAI_API_KEY manquant.")
    return OpenAI(api_key=key, base_url=rodium_base_url())
