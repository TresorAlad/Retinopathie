from sqlalchemy.orm import Session
from app.database.connection import Base, engine, SessionLocal
from app.models import Patient

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
        db.add(Patient(patient_code=code, first_name=first, last_name=last))
        db.commit()
        print("Patient créé.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
