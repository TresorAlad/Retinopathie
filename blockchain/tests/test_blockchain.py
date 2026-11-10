"""
Tests unitaires pour le module blockchain.py
"""

import pytest
import tempfile
import os
import json
from pathlib import Path

from blockchain import Blockchain
from blockchain.block import Block
from blockchain.encryption import encrypt_data, generate_aes_key


class TestBlockchainInitialization:
    """Tests pour l'initialisation de la blockchain."""

    def test_new_blockchain_creates_genesis(self):
        """Nouvelle blockchain crée automatiquement le bloc Genesis."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_chain.json"
            bc = Blockchain(filepath=filepath)

            assert len(bc.chain) == 1
            assert bc.chain[0].index == 0
            assert bc.chain[0].previous_hash == "0" * 64

    def test_load_existing_chain(self):
        """Chargement d'une chaîne existante depuis fichier."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_chain.json"

            # Créer et sauvegarder une chaîne
            bc1 = Blockchain(filepath=filepath)
            bc1.add_block({"data": "block1"})
            bc1.add_block({"data": "block2"})

            # Recharger
            bc2 = Blockchain(filepath=filepath)

            assert len(bc2.chain) == 3
            assert bc2.chain[0].index == 0
            assert bc2.chain[1].data == {"data": "block1"}
            assert bc2.chain[2].data == {"data": "block2"}

    def test_load_corrupted_chain_fails(self):
        """Fichier corrompu lève une erreur et crée nouvelle chaîne."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_chain.json"

            # Écrire JSON invalide
            with open(filepath, "w") as f:
                f.write("{ invalid json }")

            # Doit créer nouvelle chaîne (Genesis seulement)
            bc = Blockchain(filepath=filepath)
            assert len(bc.chain) == 1
            assert bc.chain[0].index == 0


class TestBlockchainOperations:
    """Tests pour les opérations sur la blockchain."""

    @pytest.fixture
    def blockchain(self):
        """Blockchain fraîche pour chaque test."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_chain.json"
            yield Blockchain(filepath=filepath)

    def test_add_block_increments_index(self, blockchain):
        """Chaque bloc ajouté a un index incrémenté."""
        blockchain.add_block({"data": "first"})
        blockchain.add_block({"data": "second"})

        assert blockchain.chain[1].index == 1
        assert blockchain.chain[2].index == 2

    def test_add_block_links_previous_hash(self, blockchain):
        """Le nouveau bloc référence le hash du précédent."""
        blockchain.add_block({"data": "first"})
        first_hash = blockchain.chain[1].hash

        blockchain.add_block({"data": "second"})

        assert blockchain.chain[2].previous_hash == first_hash

    def test_add_block_valid_pow(self, blockchain):
        """Les blocs ajoutés ont un Proof of Work valide."""
        blockchain.add_block({"data": "test"})

        assert blockchain.chain[1].verify_pow(blockchain.difficulty)

    def test_get_block_returns_correct_block(self, blockchain):
        """get_block retourne le bon bloc."""
        blockchain.add_block({"data": "block1"})
        blockchain.add_block({"data": "block2"})

        block1 = blockchain.get_block(1)
        block2 = blockchain.get_block(2)

        assert block1.data == {"data": "block1"}
        assert block2.data == {"data": "block2"}

    def test_get_block_invalid_index_returns_none(self, blockchain):
        """Index invalide retourne None."""
        assert blockchain.get_block(999) is None
        assert blockchain.get_block(-1) is None

    def test_get_chain_returns_serialized(self, blockchain):
        """get_chain retourne liste de dictionnaires."""
        blockchain.add_block({"data": "test"})

        chain = blockchain.get_chain()

        assert isinstance(chain, list)
        assert len(chain) == 2
        assert all(isinstance(b, dict) for b in chain)
        assert chain[1]["data"] == {"data": "test"}

    def test_get_latest_block(self, blockchain):
        """get_latest_block retourne le dernier bloc."""
        blockchain.add_block({"data": "first"})
        blockchain.add_block({"data": "second"})

        latest = blockchain.get_latest_block()
        assert latest.index == 2
        assert latest.data == {"data": "second"}


class TestBlockchainValidation:
    """Tests pour la validation de la chaîne."""

    @pytest.fixture
    def blockchain_with_blocks(self):
        """Blockchain avec quelques blocs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_chain.json"
            bc = Blockchain(filepath=filepath)
            bc.add_block({"data": "block1"})
            bc.add_block({"data": "block2"})
            bc.add_block({"data": "block3"})
            yield bc

    def test_validate_valid_chain(self, blockchain_with_blocks):
        """Chaîne valide passe la validation."""
        assert blockchain_with_blocks.validate_chain() is True

    def test_validate_detects_tampered_data(self, blockchain_with_blocks):
        """Modification des données détectée."""
        # Corrompre les données du bloc 1
        blockchain_with_blocks.chain[1].data = {"corrompu": True}

        assert blockchain_with_blocks.validate_chain() is False

    def test_validate_detects_tampered_hash(self, blockchain_with_blocks):
        """Modification du hash détectée."""
        blockchain_with_blocks.chain[1].hash = "0" * 64

        assert blockchain_with_blocks.validate_chain() is False

    def test_validate_detects_broken_link(self, blockchain_with_blocks):
        """Lien brisé (previous_hash) détecté."""
        blockchain_with_blocks.chain[2].previous_hash = "1" * 64

        assert blockchain_with_blocks.validate_chain() is False

    def test_validate_detects_invalid_pow(self, blockchain_with_blocks):
        """Proof of Work invalide détecté."""
        blockchain_with_blocks.chain[1].nonce = 0
        blockchain_with_blocks.chain[1].hash = "f" * 64  # Hash invalide

        assert blockchain_with_blocks.validate_chain() is False

    def test_validate_genesis_corruption(self, blockchain_with_blocks):
        """Corruption du Genesis détectée."""
        blockchain_with_blocks.chain[0].data = {"hacked": True}

        assert blockchain_with_blocks.validate_chain() is False


class TestBlockchainPersistence:
    """Tests pour la persistance."""

    def test_save_creates_valid_json(self):
        """Sauvegarde crée un JSON valide et rechargable."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_chain.json"
            bc = Blockchain(filepath=filepath)
            bc.add_block({"data": "test"})

            # Vérifier que le fichier existe et est du JSON valide
            assert filepath.exists()

            with open(filepath, "r") as f:
                data = json.load(f)

            assert isinstance(data, list)
            assert len(data) == 2

    def test_auto_save_after_add_block(self):
        """Sauvegarde automatique après ajout de bloc."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_chain.json"
            bc = Blockchain(filepath=filepath)

            bc.add_block({"data": "block1"})

            # Recharger et vérifier
            bc2 = Blockchain(filepath=filepath)
            assert len(bc2.chain) == 2
            assert bc2.chain[1].data == {"data": "block1"}


class TestBlockchainThreadSafety:
    """Tests basiques pour thread-safety."""

    def test_concurrent_add_blocks(self):
        """Ajouts concurrents ne corrompent pas la chaîne."""
        import threading

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test_chain.json"
            bc = Blockchain(filepath=filepath)

            errors = []

            def add_blocks(start_idx, count):
                try:
                    for i in range(count):
                        bc.add_block({"data": f"block_{start_idx + i}"})
                except Exception as e:
                    errors.append(e)

            threads = [
                threading.Thread(target=add_blocks, args=(0, 3)),
                threading.Thread(target=add_blocks, args=(10, 3)),
            ]

            for t in threads:
                t.start()
            for t in threads:
                t.join()

            assert len(errors) == 0
            # 1 genesis + 6 blocs = 7 total
            assert len(bc.chain) == 7
            assert bc.validate_chain()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])