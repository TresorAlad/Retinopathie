"""
Classe Blockchain - Gestion de la chaîne de blocs.

Fonctionnalités :
- Création automatique du bloc Genesis
- Ajout de blocs avec Proof of Work
- Vérification d'intégrité complète
- Persistance locale (JSON)
- Thread-safety pour ajouts concurrents
"""

import json
import threading
from pathlib import Path
from typing import List, Optional, Dict, Any

from .config import get_blockchain_file, get_pow_difficulty
from .block import Block
from .utils import (
    compute_sha256,
    deterministic_json,
    print_error,
    print_info,
    print_success,
    print_warning,
)


class Blockchain:
    """
    Blockchain privée locale avec Proof of Work et persistance JSON.

    Attributes:
        chain: Liste des blocs (Block)
        difficulty: Difficulté du Proof of Work
        _lock: Verrou pour thread-safety
    """

    def __init__(
        self,
        difficulty: int | None = None,
        filepath: Optional[Path] = None,
    ):
        """
        Initialise la blockchain.

        Args:
            difficulty: Nombre de zéros initiaux pour le PoW
            filepath: Chemin du fichier de persistance (défaut: config.BLOCKCHAIN_FILE)
        """
        self.chain: List[Block] = []
        self.difficulty = difficulty if difficulty is not None else get_pow_difficulty()
        self.filepath = filepath or get_blockchain_file()
        self._lock = threading.Lock()

        # Charger ou créer la chaîne
        self._load_or_create()

    def _load_or_create(self) -> None:
        """Charge la blockchain depuis le fichier ou crée le bloc Genesis."""
        if self.filepath.exists():
            self._load_chain()
        else:
            self._create_genesis()
            self._save_chain()

    def _create_genesis(self) -> None:
        """Crée le bloc Genesis et l'ajoute à la chaîne."""
        genesis = Block.create_genesis()
        self.chain.append(genesis)
        print_success("Bloc Genesis créé.")

    def _load_chain(self) -> None:
        """Charge la blockchain depuis le fichier JSON."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Reconstruire les blocs
            self.chain = [Block.from_dict(block_data) for block_data in data]

            # Vérifier l'intégrité après chargement
            if not self.validate_chain():
                print_error("Chaîne corrompue détectée au chargement !")
                raise ValueError("Intégrité de la blockchain compromise")

            print_success(f"Blockchain chargée ({len(self.chain)} blocs).")

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print_error(f"Échec du chargement: {e}")
            print_warning("Création d'une nouvelle blockchain...")
            self._create_genesis()
            self._save_chain()

    def _save_chain(self) -> None:
        """Sauvegarde la blockchain dans le fichier JSON."""
        try:
            # Sérialisation déterministe pour cohérence
            data = [block.to_dict() for block in self.chain]
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print_error(f"Échec de la sauvegarde: {e}")
            raise

    def get_latest_block(self) -> Block:
        """
        Retourne le dernier bloc de la chaîne.

        Returns:
            Block: Dernier bloc
        """
        return self.chain[-1]

    def add_block(self, data: Dict[str, Any]) -> Block:
        """
        Ajoute un nouveau bloc à la chaîne (thread-safe).

        Args:
            data: Données chiffrées à inclure dans le bloc

        Returns:
            Block: Le bloc créé et ajouté
        """
        with self._lock:
            previous_block = self.get_latest_block()
            new_block = Block.create_block(
                index=len(self.chain),
                data=data,
                previous_hash=previous_block.hash,
                difficulty=self.difficulty,
            )
            self.chain.append(new_block)
            self._save_chain()
            print_success(f"Bloc #{new_block.index} ajouté (nonce: {new_block.nonce}).")
            return new_block

    def get_block(self, index: int) -> Optional[Block]:
        """
        Récupère un bloc par son index.

        Args:
            index: Index du bloc recherché

        Returns:
            Block ou None si index invalide
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def get_chain(self) -> List[Dict[str, Any]]:
        """
        Retourne toute la chaîne sous forme de liste de dictionnaires.

        Returns:
            List[dict]: Liste des blocs sérialisés
        """
        return [block.to_dict() for block in self.chain]

    def validate_chain(self) -> bool:
        """
        Vérifie l'intégrité complète de la blockchain.

        Contrôles :
        - Hash de chaque bloc valide
        - Lien previous_hash correct entre blocs
        - Proof of Work valide pour chaque bloc (sauf Genesis)

        Returns:
            bool: True si la chaîne est intacte, False sinon
        """
        if not self.chain:
            print_error("Chaîne vide.")
            return False

        # Vérifier le bloc Genesis
        genesis = self.chain[0]
        if not genesis.verify_integrity():
            print_error("Bloc Genesis corrompu.")
            return False
        if genesis.previous_hash != "0" * 64:
            print_error("Bloc Genesis: previous_hash invalide.")
            return False

        # Vérifier les blocs suivants
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1. Intégrité du hash du bloc courant
            if not current.verify_integrity():
                print_error(f"Bloc #{i}: hash invalide.")
                return False

            # 2. Lien avec le bloc précédent
            if current.previous_hash != previous.hash:
                print_error(f"Bloc #{i}: previous_hash ne correspond pas au hash du bloc #{i-1}.")
                return False

            # 3. Proof of Work valide
            if not current.verify_pow(self.difficulty):
                print_error(f"Bloc #{i}: Proof of Work invalide.")
                return False

        return True

    def display_chain(self) -> None:
        """Affiche tous les blocs de la chaîne dans le terminal."""
        from .utils import print_header
        print_header(f"Blockchain ({len(self.chain)} blocs)")
        for block in self.chain:
            block.display()
            print()

    def get_chain_length(self) -> int:
        """Retourne le nombre de blocs dans la chaîne."""
        return len(self.chain)

    def is_empty(self) -> bool:
        """Vérifie si la chaîne ne contient que le bloc Genesis."""
        return len(self.chain) == 1