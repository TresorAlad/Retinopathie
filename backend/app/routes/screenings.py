import hashlib
import io
import os
import uuid
from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import Response
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database.connection import get_db
from app.core.security import require_doctor
from app.models.patient import Patient
from app.models.screening import Screening
from app.models.user import User
from app.schemas.screening import ScreeningResponse, DiagnosisUpdate
from app.services.encryption_service import store_encrypted_image, read_encrypted_image, delete_encrypted_image
from app.services.ai_service import ai_recommendations_json, analyze_retinal_image
from app.services.blockchain_service import (
    BlockchainRegistrationError,
    merge_blockchain_status,
    register_diagnosis_review,
    register_screening,
)

router = APIRouter(prefix="/api/v1/screenings", tags=["Screenings"])
ALLOWED_FORMATS = {"JPEG": "jpeg", "PNG": "png"}

def _validate_image(content: bytes) -> str:
    try:
        with Image.open(io.BytesIO(content)) as image:
            image_format = image.format
            image.verify()
        if image_format not in ALLOWED_FORMATS:
            raise HTTPException(status_code=415, detail="Format accepté : JPEG ou PNG.")
        return ALLOWED_FORMATS[image_format]
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="Le fichier envoyé n'est pas une image valide.")

@router.post("", response_model=ScreeningResponse, status_code=status.HTTP_201_CREATED)
async def create_screening(
    patient_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient introuvable.")

    max_bytes = int(os.getenv("MAX_IMAGE_SIZE_MB", "10")) * 1024 * 1024
    content = await image.read(max_bytes + 1)
    if not content:
        raise HTTPException(status_code=400, detail="Fichier vide.")
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail="Image trop volumineuse.")
    image_format = _validate_image(content)

    filename = uuid.uuid4().hex
    digest = hashlib.sha256(content).hexdigest()
    store_encrypted_image(filename, content)

    try:
        ai = analyze_retinal_image(content)
        screening = Screening(
            patient_id=patient.id,
            created_by_id=current_user.id,
            image_filename=filename,
            image_format=image_format,
            image_sha256=digest,
            ai_status=ai["status"],
            ai_stage=ai["stage"],
            ai_confidence=ai["confidence"],
            image_quality=ai["image_quality"],
            retinal_image_valid=ai["retinal_image_valid"],
            ai_recommendations=ai_recommendations_json(ai),
            ai_patient_message=ai.get("patient_message"),
            diagnosis_status="pending_review",
            blockchain_status="not_configured",
        )
        db.add(screening)
        db.flush()
        try:
            birth = (
                patient.birth_date.isoformat() if patient.birth_date else None
            )
            screening.blockchain_status = register_screening(
                screening.id,
                digest,
                patient_id=patient.id,
                patient_code=patient.patient_code,
                first_name=patient.first_name,
                last_name=patient.last_name,
                birth_date=birth,
            )
        except BlockchainRegistrationError as exc:
            db.rollback()
            delete_encrypted_image(filename)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc
        db.commit()
        db.refresh(screening)
        return screening
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        delete_encrypted_image(filename)
        raise

@router.get("", response_model=list[ScreeningResponse])
def list_screenings(
    patient_id: int | None = Query(None, gt=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_doctor),
):
    query = db.query(Screening)
    if patient_id is not None:
        query = query.filter(Screening.patient_id == patient_id)
    return query.order_by(Screening.id.desc()).offset(skip).limit(limit).all()

@router.get("/{screening_id}", response_model=ScreeningResponse)
def get_screening(
    screening_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_doctor),
):
    screening = db.query(Screening).filter(Screening.id == screening_id).first()
    if screening is None:
        raise HTTPException(status_code=404, detail="Dépistage introuvable.")
    return screening

@router.get("/{screening_id}/image")
def get_screening_image(
    screening_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_doctor),
):
    screening = db.query(Screening).filter(Screening.id == screening_id).first()
    if screening is None:
        raise HTTPException(status_code=404, detail="Dépistage introuvable.")
    try:
        content = read_encrypted_image(screening.image_filename)
    except (FileNotFoundError, ValueError):
        raise HTTPException(status_code=404, detail="Image indisponible ou illisible.")
    media_type = "image/jpeg" if screening.image_format == "jpeg" else "image/png"
    return Response(content=content, media_type=media_type, headers={"Content-Disposition": "inline"})

@router.patch("/{screening_id}/diagnosis", response_model=ScreeningResponse)
def update_diagnosis(
    screening_id: int,
    payload: DiagnosisUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_doctor),
):
    screening = (
        db.query(Screening)
        .filter(Screening.id == screening_id)
        .first()
    )
    if screening is None:
        raise HTTPException(status_code=404, detail="Dépistage introuvable.")
    patient = db.query(Patient).filter(Patient.id == screening.patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient introuvable.")
    screening.diagnosis = payload.diagnosis
    screening.diagnosis_note = payload.note
    screening.diagnosis_status = "reviewed"
    screening.reviewed_by_id = current_user.id
    screening.reviewed_at = datetime.now(timezone.utc)
    try:
        birth = (
            patient.birth_date.isoformat() if patient.birth_date else None
        )
        review_status = register_diagnosis_review(
            screening.id,
            screening.image_sha256,
            payload.diagnosis,
            current_user.id,
            patient_id=patient.id,
            patient_code=patient.patient_code,
            first_name=patient.first_name,
            last_name=patient.last_name,
            birth_date=birth,
        )
        screening.blockchain_status = merge_blockchain_status(
            screening.blockchain_status,
            review_status,
        )
    except BlockchainRegistrationError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    db.commit()
    db.refresh(screening)
    return screening
