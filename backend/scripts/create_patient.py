import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy.orm import Session

from app.database.connection import Base, engine, SessionLocal
from app.models import Patient
from app.services.blockchain_service import BlockchainRegistrationError, register_patient_record


def main():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        code = input("Code patient (unique) : ").strip()
        first = input("Prénom : ").strip()
        last = input("Nom : ").strip()
        if not code or not first or not last:
            print("Tous les champs sont obligatoires.")
            return
        if db.query(Patient).filter(Patient.patient_code == code).first():
            print("Ce code patient existe déjà.")
            return
        patient = Patient(patient_code=code, first_name=first, last_name=last)
        db.add(patient)
        db.flush()
        try:
            register_patient_record(
                patient.id,
                patient.patient_code,
                patient.first_name,
                patient.last_name,
                None,
            )
        except BlockchainRegistrationError:
            db.rollback()
            print("Échec blockchain : le patient n'a pas été enregistré.")
            return
        db.commit()
        print("Patient créé et ancré sur la blockchain.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
