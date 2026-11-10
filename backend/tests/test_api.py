import io
from PIL import Image

def token_for(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "doctor@example.com",
        "password": "StrongPassword123!"
    })
    assert response.status_code == 200
    return response.json()["access_token"]

def make_png():
    buffer = io.BytesIO()
    Image.new("RGB", (32, 32), "white").save(buffer, format="PNG")
    return buffer.getvalue()

def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_login_and_profile(client):
    token = token_for(client)
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "doctor@example.com"

def test_patients_require_auth(client):
    assert client.get("/api/v1/patients").status_code == 401

def test_patient_list_and_detail(client):
    token = token_for(client)
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/api/v1/patients", headers=headers).status_code == 200
    response = client.get("/api/v1/patients/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["patient_code"] == "PAT-001"

def test_screening_upload_read_image_and_diagnosis(client):
    token = token_for(client)
    headers = {"Authorization": f"Bearer {token}"}
    upload = client.post(
        "/api/v1/screenings",
        headers=headers,
        data={"patient_id": "1"},
        files={"image": ("retina.png", make_png(), "image/png")},
    )
    assert upload.status_code == 201, upload.text
    screening = upload.json()
    screening_id = screening["id"]
    assert screening["ai_status"] == "pending"  # IA réelle non branchée à ce stade.
    assert screening["blockchain_status"].startswith("registered:")

    listed = client.get("/api/v1/screenings", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    detail = client.get(f"/api/v1/screenings/{screening_id}", headers=headers)
    assert detail.status_code == 200

    image_response = client.get(f"/api/v1/screenings/{screening_id}/image", headers=headers)
    assert image_response.status_code == 200
    assert image_response.headers["content-type"] == "image/png"
    assert image_response.content == make_png()

    diagnosis = client.patch(
        f"/api/v1/screenings/{screening_id}/diagnosis",
        headers=headers,
        json={"diagnosis": "mild", "note": "Validation de test"},
    )
    assert diagnosis.status_code == 200
    assert diagnosis.json()["diagnosis_status"] == "reviewed"
    assert diagnosis.json()["diagnosis"] == "mild"
    assert "review:" in diagnosis.json()["blockchain_status"]

def test_invalid_image_rejected(client):
    token = token_for(client)
    response = client.post(
        "/api/v1/screenings",
        headers={"Authorization": f"Bearer {token}"},
        data={"patient_id": "1"},
        files={"image": ("fake.png", b"not-an-image", "image/png")},
    )
    assert response.status_code == 400
