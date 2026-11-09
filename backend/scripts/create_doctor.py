import getpass
from sqlalchemy.orm import Session
from app.database.connection import Base, engine, SessionLocal
from app.models import User
from app.core.security import hash_password

def main():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        email = input("Email du médecin : ").strip().lower()
        if db.query(User).filter(User.email == email).first():
            print("Cet email existe déjà.")
            return
        password = getpass.getpass("Mot de passe (12 caractères minimum) : ")
        confirmation = getpass.getpass("Confirmer : ")
        if password != confirmation:
            print("Les mots de passe ne correspondent pas.")
            return
        if len(password) < 12:
            print("Mot de passe trop court.")
            return
        db.add(User(email=email, hashed_password=hash_password(password), role="doctor", is_active=True))
        db.commit()
        print("Compte médecin créé.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
