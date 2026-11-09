"""
Tests unitaires pour le module block.py
"""

import pytest
from block import Block
from utils import compute_sha256


class TestBlockCreation:
    """Tests pour la création de blocs."""

    def test_genesis_block_creation(self):
        """Le bloc Genesis a les propriétés attendues."""
        genesis = Block.create_genesis()

        assert genesis.index == 0
        assert genesis.previous_hash == "0" * 64
        assert genesis.nonce == 0
        assert genesis.hash is not None
        assert len(genesis.hash) == 64  # SHA-256 hex
        assert isinstance(genesis.data, dict)
        assert "message" in genesis.data

    def test_genesis_block_hash_valid(self):
        """Le hash du Genesis est correctement calculé."""
        genesis = Block.create_genesis()
        assert genesis.verify_integrity()

    def test_create_block_with_pow(self):
        """Création d'un bloc avec Proof of Work."""
        previous_hash = "a" * 64
        data = {"test": "data"}

        block = Block.create_block(index=1, data=data, previous_hash=previous_hash, difficulty=2)

        assert block.index == 1
        assert block.previous_hash == previous_hash
        assert block.data == data
        assert block.nonce > 0  # PoW a trouvé un nonce
        assert block.verify_integrity()
        assert block.verify_pow(difficulty=2)
        assert block.hash.startswith("00")

    def test_create_block_higher_difficulty(self):
        """Difficulté plus élevée nécessite plus de calcul."""
        previous_hash = "b" * 64
        data = {"test": "data"}

        block = Block.create_block(index=1, data=data, previous_hash=previous_hash, difficulty=4)
        assert block.hash.startswith("0000")
        assert block.verify_pow(difficulty=4)


class TestBlockVerification:
    """Tests pour la vérification d'intégrité."""

    def test_verify_integrity_valid_block(self):
        """Un bloc valide passe la vérification."""
        genesis = Block.create_genesis()
        assert genesis.verify_integrity() is True

    def test_verify_integrity_tampered_data(self):
        """Modification des données fait échouer la vérification."""
        genesis = Block.create_genesis()
        # Corrompre les données
        genesis.data = {"corrompu": True}
        assert genesis.verify_integrity() is False

    def test_verify_integrity_tampered_hash(self):
        """Modification du hash fait échouer la vérification."""
        genesis = Block.create_genesis()
        genesis.hash = "0" * 64
        assert genesis.verify_integrity() is False

    def test_verify_integrity_tampered_previous_hash(self):
        """Modification du previous_hash fait échouer la vérification."""
        genesis = Block.create_genesis()
        genesis.previous_hash = "1" * 64
        assert genesis.verify_integrity() is False

    def test_verify_integrity_tampered_nonce(self):
        """Modification du nonce fait échouer la vérification."""
        genesis = Block.create_genesis()
        genesis.nonce = 999
        assert genesis.verify_integrity() is False

    def test_verify_pow_valid(self):
        """Proof of Work valide pour un bloc miné."""
        block = Block.create_block(1, {"data": "test"}, "0" * 64, difficulty=3)
        assert block.verify_pow(difficulty=3) is True

    def test_verify_pow_invalid_difficulty(self):
        """Bloc miné avec difficulté 2 ne passe pas difficulté 4."""
        block = Block.create_block(1, {"data": "test"}, "0" * 64, difficulty=2)
        assert block.verify_pow(difficulty=4) is False


class TestBlockSerialization:
    """Tests pour la sérialisation/désérialisation."""

    def test_to_dict_contains_all_fields(self):
        """to_dict() inclut tous les champs."""
        block = Block.create_genesis()
        d = block.to_dict()

        assert set(d.keys()) == {"index", "timestamp", "data", "previous_hash", "hash", "nonce"}

    def test_from_dict_restores_block(self):
        """from_dict() restaure un bloc identique."""
        original = Block.create_genesis()
        restored = Block.from_dict(original.to_dict())

        assert restored.index == original.index
        assert restored.timestamp == original.timestamp
        assert restored.data == original.data
        assert restored.previous_hash == original.previous_hash
        assert restored.hash == original.hash
        assert restored.nonce == original.nonce

    def test_restored_block_verifies(self):
        """Bloc restauré passe la vérification d'intégrité."""
        original = Block.create_genesis()
        restored = Block.from_dict(original.to_dict())
        assert restored.verify_integrity()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])