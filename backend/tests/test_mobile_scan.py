from tests.test_api import make_png, token_for

MOBILE_HEADERS = {"X-Mobile-Api-Key": "test-mobile-key"}


def test_mobile_scan_rejects_overlong_names(client):
    long_name = "A" * 61
    response = client.post(
        "/api/v1/mobile/scan",
        headers=MOBILE_HEADERS,
        data={
            "patient_code": "M-003",
            "first_name": long_name,
            "last_name": "Mobile",
        },
        files={"image": ("retina.png", make_png(), "image/png")},
    )
    assert response.status_code == 422


def test_mobile_scan_requires_api_key(client):
    response = client.post(
        "/api/v1/mobile/scan",
        data={
            "patient_code": "M-001",
            "first_name": "Ada",
            "last_name": "Mobile",
        },
        files={"image": ("retina.png", make_png(), "image/png")},
    )
    assert response.status_code == 401


def test_mobile_scan_rejected_eye_no_blockchain_growth(client, monkeypatch):
    import json
    import os
    from pathlib import Path

    monkeypatch.setenv("AI_TEST_SCENARIO", "rejected")

    chain_path = os.environ["BLOCKCHAIN_DATA_DIR"]
    chain_file = Path(chain_path) / "blockchain.json"
    length_before = 0
    if chain_file.is_file():
        length_before = len(json.loads(chain_file.read_text(encoding="utf-8")))

    response = client.post(
        "/api/v1/mobile/scan",
        headers=MOBILE_HEADERS,
        data={
            "patient_code": "M-002",
            "first_name": "Ada",
            "last_name": "Rejet",
        },
        files={"image": ("retina.png", make_png(), "image/png")},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["is_eye"] is False
    assert body.get("screening_id") is None
    if chain_file.is_file():
        length_after = len(json.loads(chain_file.read_text(encoding="utf-8")))
        assert length_before == length_after


def test_mobile_scan_ok_creates_mobile_block(client, monkeypatch):
    from app.services.blockchain_service import find_anchor_block, validate_chain_integrity

    monkeypatch.setenv("AI_TEST_SCENARIO", "completed")

    response = client.post(
        "/api/v1/mobile/scan",
        headers=MOBILE_HEADERS,
        data={
            "patient_code": "M-100",
            "first_name": "Paul",
            "last_name": "Scan",
            "birth_date": "1985-06-15",
        },
        files={"image": ("retina.png", make_png(), "image/png")},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["is_eye"] is True
    assert body["screening_id"] is not None
    assert body["blockchain_status"].startswith("mobile:")
    assert body["blockchain_block_index"] is not None
    anchor = find_anchor_block(body["screening_id"], "mobile_scan")
    assert anchor is not None
    assert anchor["type"] == "mobile_scan"
    assert validate_chain_integrity() is True


def test_blockchain_blocks_listing_requires_doctor(client):
    assert client.get("/api/v1/blockchain/blocks").status_code == 401


def test_blockchain_blocks_listing_after_mobile_scan(client, monkeypatch):
    token = token_for(client)
    headers = {"Authorization": f"Bearer {token}"}
    monkeypatch.setenv("AI_TEST_SCENARIO", "completed")
    client.post(
        "/api/v1/mobile/scan",
        headers=MOBILE_HEADERS,
        data={
            "patient_code": "M-200",
            "first_name": "Léa",
            "last_name": "Liste",
        },
        files={"image": ("retina.png", make_png(), "image/png")},
    )
    blocks = client.get("/api/v1/blockchain/blocks", headers=headers)
    assert blocks.status_code == 200
    items = blocks.json()
    assert any(b.get("type") == "mobile_scan" for b in items)
