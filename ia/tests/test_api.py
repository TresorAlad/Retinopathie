import io
import os

import pytest
from PIL import Image

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def make_image():
    buffer = io.BytesIO()
    Image.new("RGB", (300, 300), (128, 60, 60)).save(buffer, format="JPEG")
    buffer.seek(0)
    return "test.jpg", buffer.read(), "image/jpeg"


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["inference"] == "rodium"


def test_predict_without_api_key_returns_503(client, monkeypatch):
    monkeypatch.delenv("RODIUMAI_API_KEY", raising=False)
    name, data, ct = make_image()
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
    )
    assert response.status_code == 503


def test_predict_missing_image_returns_400(client, monkeypatch):
    monkeypatch.setenv("RODIUMAI_API_KEY", "test-key-not-used")
    response = client.post("/predict", data={}, content_type="multipart/form-data")
    assert response.status_code == 400


def test_predict_bad_content_type_returns_400(client, monkeypatch):
    monkeypatch.setenv("RODIUMAI_API_KEY", "test-key-not-used")
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(b"x"), "f.txt", "text/plain")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


def test_predict_corrupt_image_returns_400(client, monkeypatch):
    monkeypatch.setenv("RODIUMAI_API_KEY", "test-key-not-used")
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(b"bad"), "fake.jpg", "image/jpeg")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 400


@pytest.mark.skipif(
    not os.getenv("RODIUMAI_API_KEY"),
    reason="RODIUMAI_API_KEY requis pour test live Rodium",
)
def test_predict_live_rodium(client):
    name, data, ct = make_image()
    response = client.post(
        "/predict",
        data={"image": (io.BytesIO(data), name, ct)},
        content_type="multipart/form-data",
    )
    assert response.status_code == 200
    body = response.get_json()
    assert "is_eye" in body
    assert "stage" in body
