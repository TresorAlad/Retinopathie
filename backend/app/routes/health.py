from dataclasses import asdict

from fastapi import APIRouter, Depends

from app.core.security import require_doctor
from app.models.user import User
from app.services.blockchain_service import get_blockchain_health

router = APIRouter(prefix="/api/v1/health", tags=["Health"])


@router.get("/blockchain")
def blockchain_health(_: User = Depends(require_doctor)):
    return asdict(get_blockchain_health())
