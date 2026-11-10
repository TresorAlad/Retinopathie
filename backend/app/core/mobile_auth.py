import os

from fastapi import Header, HTTPException, status


def verify_mobile_api_key(x_mobile_api_key: str | None = Header(default=None, alias="X-Mobile-Api-Key")) -> None:
    expected = os.getenv("MOBILE_API_KEY", "").strip()
    if not expected:
        if os.getenv("ALLOW_MOBILE_WITHOUT_KEY", "").lower() in ("1", "true", "yes"):
            return
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MOBILE_API_KEY non configurée sur le serveur.",
        )
    if not x_mobile_api_key or x_mobile_api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé mobile invalide.",
        )
