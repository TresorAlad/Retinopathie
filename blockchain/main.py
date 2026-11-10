"""
Démonstration locale de la blockchain (contrat aligné avec le backend FastAPI).
"""

from blockchain import Blockchain
from blockchain.encryption import decrypt_data, get_or_create_key, encrypt_data
from blockchain.utils import print_error, print_header, print_info, print_success


def main() -> None:
    print_header("Démonstration blockchain - ancrage dépistage")
    chain = Blockchain()
    key = get_or_create_key()

    anchors = [
        {"type": "screening_anchor", "screening_id": 1, "image_sha256": "a" * 64},
        {"type": "screening_anchor", "screening_id": 2, "image_sha256": "b" * 64},
        {
            "type": "diagnosis_review",
            "screening_id": 1,
            "image_sha256": "a" * 64,
            "diagnosis": "mild",
            "reviewed_by_id": 10,
            "review_digest": "c" * 64,
        },
    ]

    for anchor in anchors:
        print_info(f"Ancrage {anchor['type']} pour screening_id={anchor['screening_id']}...")
        chain.add_block(encrypt_data(anchor, key))

    if chain.validate_chain():
        print_success("Chaîne valide.")
    else:
        print_error("Chaîne invalide.")

    block = chain.get_block(1)
    if block:
        decoded = decrypt_data(block.data, key)
        print_info(f"Bloc #1 déchiffré : type={decoded.get('type')}, screening_id={decoded.get('screening_id')}")


if __name__ == "__main__":
    main()
