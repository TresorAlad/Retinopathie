"""
Classe Block - Structure d'un bloc de la blockchain.

Chaque bloc contient :
- index: numéro du bloc
- timestamp: date/heure de création
- data: données chiffrées (dictionnaire)
- previous_hash: hash du bloc précédent
- hash: empreinte SHA-256 du bloc
- nonce: valeur pour le Proof of Work
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

from .utils import compute_block_hash, current_timestamp, deterministic_json
from .config import get_pow_difficulty


@dataclass
class Block:
    """
    Représente un bloc dans la blockchain.

    Attributs:
        index: Position du bloc dans la chaîne (0 = Genesis)
        timestamp: Horodatage ISO 8601 de la création
        data: Données chiffrées (dict avec ciphertext, nonce, tag en base64)
        previous_hash: Hash SHA-256 du bloc précédent (64 chars hex)
        hash: Hash SHA-256 de ce bloc (64 chars hex)
        nonce: Entier utilisé pour le Proof of Work
    """
    index: int
    timestamp: str
    data: Dict[str, Any]
    previous_hash: str
    hash: str
    nonce: int

    @classmethod
    def create_genesis(cls) -> "Block":
        """
        Crée le bloc Genesis (premier bloc de la chaîne).

        Returns:
            Block: Bloc Genesis avec index 0 et previous_hash = "0" * 64
        """
        genesis_data = {"message": "Bloc Genesis - Initialisation de la blockchain"}
        timestamp = current_timestamp()
        previous_hash = "0" * 64
        nonce = 0

        # Calculer le hash sans Proof of Work pour le Genesis
        hash_value = compute_block_hash(0, timestamp, genesis_data, previous_hash, nonce)

        return cls(
            index=0,
            timestamp=timestamp,
            data=genesis_data,
            previous_hash=previous_hash,
            hash=hash_value,
            nonce=nonce,
        )

    @classmethod
    def create_block(
        cls,
        index: int,
        data: Dict[str, Any],
        previous_hash: str,
        difficulty: int | None = None,
    ) -> "Block":
        """
        Crée un nouveau bloc avec Proof of Work.

        Args:
            index: Index du bloc
            data: Données chiffrées à inclure
            previous_hash: Hash du bloc précédent
            difficulty: Nombre de zéros initiaux requis (défaut: config.POW_DIFFICULTY)

        Returns:
            Block: Nouveau bloc miné
        """
        resolved_difficulty = difficulty if difficulty is not None else get_pow_difficulty()
        timestamp = current_timestamp()
        nonce = 0
        target_prefix = "0" * resolved_difficulty

        # Proof of Work : trouver un nonce produisant un hash valide
        while True:
            hash_value = compute_block_hash(index, timestamp, data, previous_hash, nonce)
            if hash_value.startswith(target_prefix):
                break
            nonce += 1

        return cls(
            index=index,
            timestamp=timestamp,
            data=data,
            previous_hash=previous_hash,
            hash=hash_value,
            nonce=nonce,
        )

    def verify_integrity(self) -> bool:
        """
        Vérifie l'intégrité du bloc.

        Recalcule le hash à partir des données et compare avec le hash stocké.

        Returns:
            bool: True si le hash correspond, False sinon
        """
        computed_hash = compute_block_hash(
            self.index, self.timestamp, self.data, self.previous_hash, self.nonce
        )
        return computed_hash == self.hash

    def verify_pow(self, difficulty: int | None = None) -> bool:
        """
        Vérifie que le Proof of Work est valide.

        Args:
            difficulty: Difficulté attendue

        Returns:
            bool: True si le hash commence par le bon nombre de zéros
        """
        resolved_difficulty = difficulty if difficulty is not None else get_pow_difficulty()
        return self.hash.startswith("0" * resolved_difficulty)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit le bloc en dictionnaire pour sérialisation JSON.

        Returns:
            dict: Représentation du bloc
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Block":
        """
        Crée un Block à partir d'un dictionnaire.

        Args:
            data: Dictionnaire avec les champs du bloc

        Returns:
            Block: Instance de Block
        """
        return cls(
            index=data["index"],
            timestamp=data["timestamp"],
            data=data["data"],
            previous_hash=data["previous_hash"],
            hash=data["hash"],
            nonce=data["nonce"],
        )

    def display(self) -> None:
        """Affiche les informations du bloc dans le terminal."""
        from .utils import format_block_display, print_header
        print_header(f"Bloc #{self.index}")
        print(format_block_display(self.to_dict()))
        print(f"  Intégrité    : {'OK' if self.verify_integrity() else 'ÉCHEC'}")
        print(f"  Proof of Work: {'OK' if self.verify_pow() else 'ÉCHEC'}")