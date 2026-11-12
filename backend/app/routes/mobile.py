import hashlib
import io
import os
import uuid
from datetime import date

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError
from sqlalchemy.orm import Session

from app.core.mobile_auth import verify_mobile_api_key
from app.database.connection import get_db
from app.models.patient import Patient
from app.models.screening import Screening
from app.schemas.mobile import MobileScanResponse
from app.services.ai_service import ai_recommendations_json, analyze_retinal_image
from app.services.blockchain_service import BlockchainRegistrationError, register_mobile_scan
from app.services.encryption_service import delete_encrypted_image, store_encrypted_image
from app.services.system_user import ensure_mobile_system_user

router = APIRouter(prefix="/api/v1/mobile", tags=["Mobile"])
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


def _parse_birth_date(raw: str | None) -> date | None:
    if not raw or not raw.strip():
        return None
    try:
        return date.fromisoformat(raw.strip())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail="birth_date invalide (YYYY-MM-DD).") from exc


def _upsert_patient(
    db: Session,
    patient_code: str,
    first_name: str,
    last_name: str,
    birth_date: date | None,
) -> Patient:
    patient = db.query(Patient).filter(Patient.patient_code == patient_code).first()
    if patient:
        patient.first_name = first_name
        patient.last_name = last_name
        patient.birth_date = birth_date
        return patient
    patient = Patient(
        patient_code=patient_code,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
    )
    db.add(patient)
    db.flush()
    return patient


def _validate_patient_field(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise HTTPException(status_code=422, detail=f"{field_name} obligatoire.")
    if len(cleaned) > 60:
        raise HTTPException(status_code=422, detail=f"{field_name} : 60 caractères maximum.")
    return cleaned


@router.post("/scan", response_model=MobileScanResponse)
async def mobile_scan(
    patient_code: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    birth_date: str | None = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: None = Depends(verify_mobile_api_key),
):
    request_id = uuid.uuid4().hex
    system_user = ensure_mobile_system_user(db)

    cleaned_code = patient_code.strip()
    if not cleaned_code:
        raise HTTPException(status_code=422, detail="patient_code obligatoire.")
    if len(cleaned_code) > 50:
        raise HTTPException(status_code=422, detail="patient_code trop long.")
    validated_first = _validate_patient_field(first_name, "first_name")
    validated_last = _validate_patient_field(last_name, "last_name")
    parsed_birth = _parse_birth_date(birth_date)

    max_bytes = int(os.getenv("MAX_IMAGE_SIZE_MB", "10")) * 1024 * 1024
    content = await image.read(max_bytes + 1)
    if not content:
        raise HTTPException(status_code=400, detail="Fichier vide.")
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail="Image trop volumineuse.")

    ai = analyze_retinal_image(content)

    if ai.get("status") == "rejected" or ai.get("retinal_image_valid") is False:
        return MobileScanResponse(
            is_eye=False,
            patient_message=ai.get("patient_message")
            or "L'œil n'a pas été détecté. Reprenez la photo.",
            recommendations=list(ai.get("recommendations") or []),
        )

    if ai.get("status") in ("error", "pending"):
        raise HTTPException(
            status_code=503,
            detail="Service IA indisponible ou non configuré.",
        )

    image_format = _validate_image(content)
    digest = hashlib.sha256(content).hexdigest()
    filename = uuid.uuid4().hex
    store_encrypted_image(filename, content)

    patient = _upsert_patient(
        db,
        cleaned_code,
        validated_first,
        validated_last,
        parsed_birth,
    )

    screening = Screening(
        patient_id=patient.id,
        created_by_id=system_user.id,
        image_filename=filename,
        image_format=image_format,
        image_sha256=digest,
        ai_status=ai["status"],
        ai_stage=ai.get("stage"),
        ai_confidence=ai.get("confidence"),
        image_quality=ai.get("image_quality"),
        retinal_image_valid=ai.get("retinal_image_valid"),
        ai_recommendations=ai_recommendations_json(ai),
        ai_patient_message=ai.get("patient_message"),
        diagnosis_status="pending_review",
        blockchain_status="not_configured",
    )
    db.add(screening)
    db.flush()

    birth = patient.birth_date.isoformat() if patient.birth_date else None
    ai_payload = {
        "is_eye": True,
        "stage": ai.get("ia_raw_stage"),
        "stage_api": ai.get("stage"),
        "stage_label": ai.get("stage_label"),
        "risk_score": ai.get("confidence"),
        "refer_to_doctor": ai.get("refer_to_doctor"),
        "simulated_constants": ai.get("simulated_constants"),
        "recommendations": ai.get("recommendations"),
        "patient_message": ai.get("patient_message"),
        "agent_model": ai.get("agent_model"),
    }

    try:
        status_chain = register_mobile_scan(
            request_id=request_id,
            screening_id=screening.id,
            image_sha256=digest,
            patient_id=patient.id,
            patient_code=patient.patient_code,
            first_name=patient.first_name,
            last_name=patient.last_name,
            birth_date=birth,
            ai_payload=ai_payload,
        )
        screening.blockchain_status = status_chain
    except BlockchainRegistrationError as exc:
        db.rollback()
        delete_encrypted_image(filename)
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    db.commit()
    db.refresh(screening)

    block_index = None
    if status_chain.startswith("mobile:"):
        block_index = int(status_chain.split(":", 1)[1])

    return MobileScanResponse(
        screening_id=screening.id,
        patient_id=patient.id,
        is_eye=True,
        patient_message=ai.get("patient_message") or "",
        stage=ai.get("stage"),
        stage_label=ai.get("stage_label"),
        risk_score=ai.get("confidence"),
        refer_to_doctor=bool(ai.get("refer_to_doctor")),
        ai_constants=ai.get("simulated_constants"),
        recommendations=list(ai.get("recommendations") or []),
        blockchain_block_index=block_index,
        blockchain_status=screening.blockchain_status,
        image_sha256=digest,
    )
