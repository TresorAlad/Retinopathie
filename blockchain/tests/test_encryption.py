"""
Tests unitaires pour le module encryption.py
"""

import pytest
import os
import tempfile
from blockchain.encryption import (
    decrypt_data,
    encrypt_data,
    generate_aes_key,
    get_or_create_key,
    load_key,
    save_key,
)
from cryptography.exceptions import InvalidTag


class TestKeyGeneration:
    """Tests pour la génération et gestion des clés."""

    def test_generate_key_length(self):
        """La clé générée doit faire 16 octets (128 bits)."""
        key = generate_aes_key()
        assert len(key) == 16

    def test_generate_key_randomness(self):
        """Deux clés générées doivent être différentes."""
        key1 = generate_aes_key()
        key2 = generate_aes_key()
        assert key1 != key2

    def test_save_and_load_key(self):
        """Sauvegarde et chargement d'une clé."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            key = generate_aes_key()
            save_key(key, tmp_path)
            loaded = load_key(tmp_path)
            assert loaded == key
        finally:
            os.unlink(tmp_path)

    def test_load_nonexistent_key(self):
        """Chargement d'un fichier inexistant doit lever FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_key("/chemin/inexistant/key.bin")

    def test_load_wrong_size_key(self):
        """Chargement d'une clé de mauvaise taille doit lever ValueError."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(b"cle_trop_courte")
            tmp_path = tmp.name

        try:
            with pytest.raises(ValueError):
                load_key(tmp_path)
        finally:
            os.unlink(tmp_path)

    def test_get_or_create_key_creates_new(self):
        """get_or_create_key crée un fichier s'il n'existe pas."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        os.unlink(tmp_path)  # Supprimer pour tester la création

        try:
            key = get_or_create_key(tmp_path)
            assert len(key) == 16
            assert os.path.exists(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_get_or_create_key_loads_existing(self):
        """get_or_create_key charge la clé existante sans la remplacer."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Écrire d'abord une clé valide dans le fichier
            original_key = generate_aes_key()
            save_key(original_key, tmp_path)
            # Maintenant tester le chargement
            key1 = get_or_create_key(tmp_path)
            key2 = get_or_create_key(tmp_path)
            assert key1 == key2 == original_key  # Même clé retournée
        finally:
            os.unlink(tmp_path)


class TestEncryptionDecryption:
    """Tests pour le chiffrement et déchiffrement."""

    @pytest.fixture
    def key(self):
        """Clé de test."""
        return generate_aes_key()

    @pytest.fixture
    def sample_data(self):
        """Données de test typiques d'un dépistage."""
        return {
            "patient_id": "PAT-2024-001",
            "screening_date": "2024-01-15",
            "ai_result": "Rétinopathie détectée",
            "stage": "Stade 2",
            "risk_score": 0.72,
            "validated_by_doctor": True,
        }

    def test_encrypt_returns_dict_with_required_fields(self, key, sample_data):
        """Le chiffrement retourne un dict avec ciphertext, nonce, tag."""
        result = encrypt_data(sample_data, key)
        assert "ciphertext" in result
        assert "nonce" in result
        assert "tag" in result
        assert all(isinstance(v, str) for v in result.values())

    def test_decrypt_restores_original_data(self, key, sample_data):
        """Le déchiffrement restaure les données exactes."""
        encrypted = encrypt_data(sample_data, key)
        decrypted = decrypt_data(encrypted, key)
        assert decrypted == sample_data

    def test_encrypt_deterministic_with_same_nonce_not_possible(self, key, sample_data):
        """Deux chiffrements avec la même clé produisent des résultats différents (nonce aléatoire)."""
        enc1 = encrypt_data(sample_data, key)
        enc2 = encrypt_data(sample_data, key)
        # Nonce différent à chaque fois
        assert enc1["nonce"] != enc2["nonce"]
        # Donc ciphertext différent aussi
        assert enc1["ciphertext"] != enc2["ciphertext"]

    def test_decrypt_wrong_key_fails(self, key, sample_data):
        """Déchiffrement avec mauvaise clé lève InvalidTag."""
        encrypted = encrypt_data(sample_data, key)
        wrong_key = generate_aes_key()
        with pytest.raises(InvalidTag):
            decrypt_data(encrypted, wrong_key)

    def test_decrypt_modified_ciphertext_fails(self, key, sample_data):
        """Modification du ciphertext lève InvalidTag."""
        encrypted = encrypt_data(sample_data, key)
        # Corrompre le ciphertext
        encrypted["ciphertext"] = encrypted["ciphertext"][:-1] + "X"
        with pytest.raises(InvalidTag):
            decrypt_data(encrypted, key)

    def test_decrypt_modified_tag_fails(self, key, sample_data):
        """Modification du tag lève InvalidTag."""
        encrypted = encrypt_data(sample_data, key)
        encrypted["tag"] = encrypted["tag"][:-1] + "X"
        with pytest.raises(InvalidTag):
            decrypt_data(encrypted, key)

    def test_decrypt_modified_nonce_fails(self, key, sample_data):
        """Modification du nonce lève InvalidTag."""
        encrypted = encrypt_data(sample_data, key)
        encrypted["nonce"] = encrypted["nonce"][:-1] + "X"
        with pytest.raises(InvalidTag):
            decrypt_data(encrypted, key)

    def test_encrypt_invalid_key_size(self, sample_data):
        """Clé de mauvaise taille lève ValueError."""
        with pytest.raises(ValueError):
            encrypt_data(sample_data, b"cle_123")  # 7 octets au lieu de 16

    def test_decrypt_invalid_key_size(self, key, sample_data):
        """Clé de mauvaise taille au déchiffrement lève ValueError."""
        encrypted = encrypt_data(sample_data, key)
        with pytest.raises(ValueError):
            decrypt_data(encrypted, b"cle_123")

    def test_decrypt_invalid_base64(self, key):
        """Données base64 invalides lèvent InvalidTag (tampering détecté)."""
        with pytest.raises(InvalidTag):
            decrypt_data({"ciphertext": "!!!invalid!!!", "nonce": "abc", "tag": "def"}, key)

    def test_decrypt_missing_fields(self, key):
        """Champs manquants lèvent InvalidTag (données incomplètes = suspectes)."""
        with pytest.raises(InvalidTag):
            decrypt_data({"ciphertext": "abc"}, key)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])