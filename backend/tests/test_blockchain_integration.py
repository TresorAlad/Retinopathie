import io
import json
import os
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from app.services.blockchain_service import find_anchor_block, validate_chain_integrity
from tests.test_api import make_png, token_for


def test_e2e_anchor_in_blockchain_file(client):
    token = token_for(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/api/v1/screenings",
        headers=headers,
        data={"patient_id": "1"},
        files={"image": ("retina.png", make_png(), "image/png")},
    )
    assert response.status_code == 201, response.text
    body = response.json()
    screening_id = body["id"]
    image_sha256 = body["image_sha256"]
    assert body["blockchain_status"].startswith("registered:")

    chain_file = Path(os.environ["BLOCKCHAIN_DATA_DIR"]) / "blockchain.json"
    assert chain_file.is_file()
    saved = json.loads(chain_file.read_text(encoding="utf-8"))
    assert len(saved) >= 2

    anchor = find_anchor_block(screening_id, "screening_anchor")
    assert anchor is not None
    assert anchor["image_sha256"] == image_sha256
    assert "patient_id" not in anchor
    assert validate_chain_integrity() is True


def test_diagnosis_review_anchored(client):
    token = token_for(client)
    headers = {"Authorization": f"Bearer {token}"}
    upload = client.post(
        "/api/v1/screenings",
        headers=headers,
        data={"patient_id": "1"},
        files={"image": ("retina.png", make_png(), "image/png")},
    )
    screening_id = upload.json()["id"]
    diagnosis = client.patch(
        f"/api/v1/screenings/{screening_id}/diagnosis",
        headers=headers,
        json={"diagnosis": "moderate", "note": "OK"},
    )
    assert diagnosis.status_code == 200
    assert "review:" in diagnosis.json()["blockchain_status"]

    review = find_anchor_block(screening_id, "diagnosis_review")
    assert review is not None
    assert review["diagnosis"] == "moderate"


def test_get_screening_does_not_grow_chain(client):
    token = token_for(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post(
        "/api/v1/screenings",
        headers=headers,
        data={"patient_id": "1"},
        files={"image": ("retina.png", make_png(), "image/png")},
    )
    chain_file = Path(os.environ["BLOCKCHAIN_DATA_DIR"]) / "blockchain.json"
    length_before = len(json.loads(chain_file.read_text(encoding="utf-8")))
    client.get("/api/v1/screenings/1", headers=headers)
    client.get("/api/v1/screenings/1/image", headers=headers)
    length_after = len(json.loads(chain_file.read_text(encoding="utf-8")))
    assert length_before == length_after


def test_strict_rollback_when_blockchain_fails(client):
    token = token_for(client)
    headers = {"Authorization": f"Bearer {token}"}
    with patch(
        "app.services.blockchain_service._add_encrypted_payload",
        side_effect=RuntimeError("simulated"),
    ):
        response = client.post(
            "/api/v1/screenings",
            headers=headers,
            data={"patient_id": "1"},
            files={"image": ("retina.png", make_png(), "image/png")},
        )
    assert response.status_code == 503
    listed = client.get("/api/v1/screenings", headers=headers)
    assert listed.json() == []


def test_health_blockchain_requires_auth(client):
    assert client.get("/api/v1/health/blockchain").status_code == 401


def test_health_blockchain_payload(client):
    token = token_for(client)
    headers = {"Authorization": f"Bearer {token}"}
    health = client.get("/api/v1/health/blockchain", headers=headers)
    assert health.status_code == 200
    data = health.json()
    assert data["enabled"] is True
    assert data["chain_valid"] is True
    assert data["length"] >= 1


def test_blockchain_disabled_skips_anchor(monkeypatch, client):
    monkeypatch.setenv("BLOCKCHAIN_ENABLED", "false")
    from app.services.blockchain_service import reset_chain_for_tests

    reset_chain_for_tests()
    token = token_for(client)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/api/v1/screenings",
        headers=headers,
        data={"patient_id": "1"},
        files={"image": ("retina.png", make_png(), "image/png")},
    )
    assert response.status_code == 201
    assert response.json()["blockchain_status"] == "not_configured"
