import os
import sys
import tempfile
from pathlib import Path

import pytest
from cryptography.fernet import Fernet
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ["DATABASE_URL"] = "sqlite:///./test_backend.db"
os.environ["JWT_SECRET_KEY"] = "test-only-secret-key-not-for-production"
os.environ["FERNET_KEY"] = Fernet.generate_key().decode()
os.environ["STORAGE_DIR"] = "test_storage"
os.environ["BLOCKCHAIN_DATA_DIR"] = tempfile.mkdtemp(prefix="api_blockchain_")
os.environ["BLOCKCHAIN_POW_DIFFICULTY"] = "2"
os.environ["BLOCKCHAIN_ENABLED"] = "true"
os.environ["MOBILE_API_KEY"] = "test-mobile-key"
# Scénarios IA pour pytest : AI_TEST_SCENARIO=completed|rejected (voir ai_service.py)

from app.main import app
from app.database.connection import Base, engine, SessionLocal
from app.core.security import hash_password
from app.models import User, Patient

@pytest.fixture()
def client():
    from app.services.blockchain_service import reset_chain_for_tests

    reset_chain_for_tests()
    os.environ["BLOCKCHAIN_DATA_DIR"] = tempfile.mkdtemp(prefix="api_blockchain_")
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
