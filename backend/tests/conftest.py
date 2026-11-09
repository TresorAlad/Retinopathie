import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Variables de test définies avant l'import des modules applicatifs.
os.environ["DATABASE_URL"] = "sqlite:///./test_backend.db"
os.environ["JWT_SECRET_KEY"] = "test-only-secret-key-not-for-production"
os.environ["FERNET_KEY"] = "2z5Yj4f3cQxg9dV6s8W1mK0pR7tN3aB5cE2hG6jL9uA="
os.environ["STORAGE_DIR"] = "test_storage"

from app.main import app
from app.database.connection import Base, engine, SessionLocal
from app.core.security import hash_password
from app.models import User, Patient

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.add(User(email="doctor@example.com", hashed_password=hash_password("StrongPassword123!"), role="doctor", is_active=True))
    db.add(Patient(patient_code="PAT-001", first_name="Awa", last_name="Test"))
    db.commit()
    db.close()
    Path(os.environ["STORAGE_DIR"]).mkdir(exist_ok=True)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)
    for file in Path(os.environ["STORAGE_DIR"]).glob("*"):
        file.unlink()
