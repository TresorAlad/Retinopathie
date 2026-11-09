"""
Programme de démonstration de la blockchain privée.

Scénario : Dépistage de la rétinopathie diabétique.
- Initialisation de la blockchain
- Génération clé AES-128
- Création de 3 dépistages fictifs
- Chiffrement et ajout à la blockchain
- Vérification d'intégrité
- Détection de fraude
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blockchain import Blockchain
from encryption import get_or_create_key, encrypt_data, decrypt_data, InvalidTag
from utils import print_header, print_info, print_success, print_warning, print_error


def create_sample_screening(patient_id: str, date: str, ai_result: str,
                            stage: str, risk_score: float, validated: bool) -> dict:
    """
    Crée un dictionnaire de données de dépistage (non chiffré).

    Args:
        patient_id: Identifiant pseudonymisé du patient
        date: Date du dépistage (YYYY-MM-DD)
        ai_result: Résultat de l'IA (ex: "Rétinopathie détectée")
        stage: Stade détecté (ex: "Stade 2 - Modérée")
        risk_score: Score de risque (0.0 à 1.0)
        validated: Statut de validation par le médecin

    Returns:
        dict: Données du dépistage
    """
    return {
        "patient_id": patient_id,
        "screening_date": date,
        "ai_result": ai_result,
        "stage": stage,
        "risk_score": risk_score,
        "validated_by_doctor": validated,
    }


def main():
    """Point d'entrée principal de la démonstration."""
    print_header("DÉMONSTRATION BLOCKCHAIN - DÉPISTAGE RÉTINOPATHIE DIABÉTIQUE")

    # 1. Initialiser la blockchain
    print_info("Initialisation de la blockchain...")
    blockchain = Blockchain()

    # 2. Afficher le bloc Genesis
    print_header("Bloc Genesis")
    genesis = blockchain.get_block(0)
    genesis.display()

    # 3. Générer/Récupérer la clé AES-128
    print_header("Clé de chiffrement AES-128")
    print_info("Récupération ou génération de la clé AES-128...")
    aes_key = get_or_create_key()
    print_success(f"Clé prête ({len(aes_key)} octets = {len(aes_key) * 8} bits)")
    print_info("Clé stockée dans data/encryption_key.bin (ne jamais la partager)")

    # 4. Créer trois exemples de dépistage fictifs
    print_header("Création des dépistages (données en clair)")

    screenings = [
        create_sample_screening(
            patient_id="PAT-2024-001",
            date="2024-01-15",
            ai_result="Rétinopathie diabétique détectée",
            stage="Stade 2 - Modérée",
            risk_score=0.72,
            validated=True,
        ),
        create_sample_screening(
            patient_id="PAT-2024-002",
            date="2024-01-16",
            ai_result="Aucune rétinopathie détectée",
            stage="Stade 0 - Aucune",
            risk_score=0.05,
            validated=False,
        ),
        create_sample_screening(
            patient_id="PAT-2024-003",
            date="2024-01-17",
            ai_result="Rétinopathie diabétique détectée",
            stage="Stade 3 - Sévère",
            risk_score=0.91,
            validated=True,
        ),
    ]

    for i, s in enumerate(screenings, 1):
        print_info(f"Dépistage #{i}: Patient {s['patient_id']} - {s['ai_result']} ({s['stage']})")

    # 5. Chiffrer les données et ajouter à la blockchain
    print_header("Chiffrement et ajout à la blockchain")

    for i, screening in enumerate(screenings, 1):
        print_info(f"Chiffrement du dépistage #{i}...")
        encrypted = encrypt_data(screening, aes_key)
        print_info(f"  Nonce: {encrypted['nonce'][:20]}...")
        print_info(f"  Tag:   {encrypted['tag'][:20]}...")

        print_info(f"Ajout du bloc #{i} (Proof of Work en cours)...")
        blockchain.add_block(encrypted)

    # 6. Afficher tous les blocs
    print_header("Blockchain complète")
    blockchain.display_chain()

    # 7. Vérifier l'intégrité de la chaîne
    print_header("Vérification d'intégrité")
    print_info("Validation complète de la chaîne...")
    is_valid = blockchain.validate_chain()
    if is_valid:
        print_success("Chaîne VALIDE - Tous les blocs sont intacts et liés correctement.")
    else:
        print_error("Chaîne INVALIDE - Problème détecté !")

    # 8. Déchiffrer et afficher un dépistage
    print_header("Récupération et déchiffrement d'un dépistage")
    print_info("Récupération du bloc #1 (index 1)...")
    block = blockchain.get_block(1)
    if block:
        print_info("Déchiffrement des données...")
        try:
            decrypted = decrypt_data(block.data, aes_key)
            print_success("Déchiffrement réussi !")
            print_info("Données du dépistage :")
            for key, value in decrypted.items():
                print(f"  {key}: {value}")
        except InvalidTag:
            print_error("Échec de l'authentification - Données modifiées ou clé incorrecte")
        except Exception as e:
            print_error(f"Erreur lors du déchiffrement: {e}")

    # 9. Simuler une modification frauduleuse
    print_header("Simulation de fraude - Modification du bloc #1")
    print_warning("Modification directe des données chiffrées dans le bloc #1...")

    # Corrompre le ciphertext du bloc 1
    original_ciphertext = blockchain.chain[1].data["ciphertext"]
    # Inverser quelques caractères pour corrompre
    corrupted = original_ciphertext[:10] + "X" + original_ciphertext[11:]
    blockchain.chain[1].data["ciphertext"] = corrupted

    print_warning("Données du bloc #1 modifiées (ciphertext corrompu).")

    # 10. Vérifier que la détection fonctionne
    print_header("Nouvelle vérification d'intégrité après fraude")
    print_info("Validation de la chaîne...")
    is_valid = blockchain.validate_chain()
    if is_valid:
        print_success("Chaîne VALIDE")
    else:
        print_error("Chaîne INVALIDE - Fraude détectée !")
        print_success("Le système a correctement détecté la modification frauduleuse.")

    # Restaurer pour finir proprement
    blockchain.chain[1].data["ciphertext"] = original_ciphertext
    blockchain._save_chain()

    print_header("FIN DE LA DÉMONSTRATION")
    print_info("Blockchain fonctionnelle et sécurisée.")


if __name__ == "__main__":
    main()