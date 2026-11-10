import io
import os

from PIL import Image
import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def make_image(width=300, height=300, color=(128, 60, 60)):
    img = Image.new("RGB", (width, height), color)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return "test.jpg", buffer.read(), "image/jpeg"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "ia"
    assert "inference_mode" in data
    assert data["inference_mode"] == "local"


def test_predict_valid_image_returns_all_contract_fields(client):
    name, data, ct = make_image(300, 300)
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    body = response.get_json()
    required_fields = {
        "is_eye",
        "stage",
        "stage_label",
        "risk_score",
        "refer_to_doctor",
        "model_version",
        "simulated_constants",
        "recommendations",
        "patient_message",
        "agent_model",
    }
    for field in required_fields:
        assert field in body, f"Champ manquant : {field}"

    if body["is_eye"]:
        assert isinstance(body["stage"], int)
        assert 0 <= body["stage"] <= 4
        assert isinstance(body["risk_score"], float)
        assert 0.0 <= body["risk_score"] <= 1.0


@pytest.mark.skipif(
    not os.path.isfile("models/eye_checker.pt"),
    reason="Requiert models/eye_checker.pt pour valider le rejet non-œil",
)
def test_predict_non_eye_returns_rejection(client):
    name, data, ct = make_image(30, 30)
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    body = response.get_json()
    assert body["is_eye"] is False
    assert body["stage"] == -1


def test_predict_missing_image_returns_400(client):
    response = client.post("/predict", data={}, content_type="multipart/form-data")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_predict_bad_content_type_returns_400(client):
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(b"pas une image"), "f.txt", "text/plain")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


def test_predict_corrupt_image_returns_400(client):
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(b"\x00\x01\x02 fake bytes"), "fake.jpg", "image/jpeg")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


def test_refer_to_doctor_rule_consistency(client):
    name, data, ct = make_image(300, 300)
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
    )
    body = response.get_json()
    if body.get("is_eye") and body["stage"] >= 2:
        assert body["refer_to_doctor"] is True


def test_predict_is_deterministic(client):
    name, data, ct = make_image(300, 300, color=(50, 100, 150))
    r1 = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
    )
    r2 = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
    )
    body1 = r1.get_json()
    body2 = r2.get_json()
    assert body1["stage"] == body2["stage"]
    assert body1["risk_score"] == body2["risk_score"]
