from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.security import require_doctor
from app.models.user import User
from app.services.blockchain_service import get_decrypted_block, list_decrypted_blocks

router = APIRouter(prefix="/api/v1/blockchain", tags=["Blockchain"])


@router.get("/blocks")
def list_blocks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    _: User = Depends(require_doctor),
):
    return list_decrypted_blocks(skip=skip, limit=limit)


@router.get("/blocks/{index}")
def get_block(
    index: int,
    _: User = Depends(require_doctor),
):
    block = get_decrypted_block(index)
    if block is None:
        raise HTTPException(status_code=404, detail="Bloc introuvable.")
    return block
