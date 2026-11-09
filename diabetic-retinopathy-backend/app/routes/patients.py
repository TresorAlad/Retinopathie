from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.core.security import require_doctor
from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import PatientResponse

router = APIRouter(prefix="/api/v1/patients", tags=["Patients"])

@router.get("", response_model=list[PatientResponse])
def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_doctor),
):
    return db.query(Patient).order_by(Patient.id.desc()).offset(skip).limit(limit).all()

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_doctor),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient introuvable.")
    return patient
