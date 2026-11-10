# ============================================================
# MODE MOCK — REPONSES SIMULEES
# Rôle : simuler le comportement des modèles SANS PyTorch.
# Utilisé quand IA_MODE=mock (par défaut).
#
# Pourquoi ? Pour débloquer l'équipe (backend, mobile) DÈS LE JOUR 1,
# avant que les vrais modèles soient entraînés.
#
# Les réponses sont DÉTERMINISTES (basées sur un hash de l'image) :
# la même image renvoie toujours la même réponse. C'est important
# pour que les tests et la démo soient reproductibles.
# ============================================================

# --- Imports standards ---
import hashlib
# hashlib : calcule un hash (empreinte) à partir des bytes de l'image
# On s'en sert pour rendre les réponses déterministes

import random
# random : pour générer des valeurs reproductibles (avec seed)


# ============================================================
# LIBELLES DES STADES (rappel du contrat API)
# ============================================================
STAGE_LABELS = {
    0: "Pas de rétinopathie",
    1: "Légère",
    2: "Modérée",
    3: "Sévère",
    4: "Proliférative",
}
# Ces libellés DOIVENT correspondre exactement au contrat figé par le Master


# ============================================================
# CLASSE 1 : MockEyeChecker
# Simule l'étape 1 (est-ce un œil ?)
# ============================================================
class MockEyeChecker:
    """
    Faux détecteur d'œil.
    - Renvoie toujours True (c'est un œil) SAUF si les bytes
      contiennent "not_eye" (pratique pour tester le rejet).
    """

    def is_eye(self, img):
        """
        Args:
            img: image PIL (ignorée ici, on ne fait pas de vraie IA)

        Returns:
            (ok_eye, prob_eye) : tuple (bool, float)
        """
        # --- Cas spécial : image de test pour le rejet ---
        # On regarde la taille de l'image comme heuristique simple :
        # une image très petite (< 50x50) est probablement un test de rejet.
        if img.size[0] < 50 or img.size[1] < 50:
            # img.size = (width, height)
            return False, 0.05
            # 0.05 = probabilité très faible que ce soit un œil

        # --- Cas normal : on dit que c'est un œil ---
        return True, 0.98
        # 0.98 = probabilité élevée (réaliste pour un vrai modèle)


# ============================================================
# CLASSE 2 : MockStageClassifier
# Simule l'étape 2 (quel stade 0..4 ?)
# ============================================================
class MockStageClassifier:
    """
    Faux classifieur de stade.
    - Renvoie un stade DÉTERMINISTE calculé à partir d'un hash de l'image.
    - La même image renvoie TOUJOURS le même stade.
    - Les valeurs restent réalistes (risk_score cohérent avec stage).
    """

    def predict(self, img):
        """
        Args:
            img: image PIL

        Returns:
            dict avec stage, stage_label, risk_score, refer_to_doctor
        """
        # --- Étape 1 : calculer un hash déterministe de l'image ---
        # On utilise les bytes bruts de l'image pour le hash.
        # img.tobytes() renvoie les pixels sous forme de bytes.
        pixels_bytes = img.tobytes()

        # --- Étape 2 : transformer en entier ---
        hash_hex = hashlib.md5(pixels_bytes).hexdigest()
        # md5 : rapide et suffisant pour du mock
        # hexdigest : renvoie une chaîne hexadécimale (ex: "a1b2c3...")

        # --- Étape 3 : utiliser le hash comme graine aléatoire ---
        seed = int(hash_hex[:8], 16)
        # On prend les 8 premiers caractères hex → int
        # Ça donne un entier stable pour cette image précise

        rng = random.Random(seed)
        # random.Random(seed) : générateur reproductible
        # La même seed donnera toujours la même séquence de nombres

        # --- Étape 4 : choisir un stade 0..4 ---
        # Distribution réaliste : plus de cas sains que de cas sévères
        # (comme dans la vraie population)
        stage = rng.choices(
            population=[0, 1, 2, 3, 4],
            weights=[40, 25, 20, 10, 5],
            # 40% stade 0, 25% stade 1, 20% stade 2, 10% stade 3, 5% stade 4
        )[0]
        # .choices() renvoie une liste → on prend l'élément [0]

        # --- Étape 5 : calculer un risk_score cohérent ---
        # risk_score = P(stade >= 2), donc :
        #   - stade 0 ou 1 → risque faible (0.05 à 0.35)
        #   - stade 2      → risque moyen (0.55 à 0.75)
        #   - stade 3      → risque élevé (0.75 à 0.90)
        #   - stade 4      → risque très élevé (0.90 à 0.99)
        risk_by_stage = {
            0: rng.uniform(0.02, 0.15),   # très faible
            1: rng.uniform(0.15, 0.35),   # faible
            2: rng.uniform(0.55, 0.75),   # moyen
            3: rng.uniform(0.75, 0.90),   # élevé
            4: rng.uniform(0.90, 0.99),   # très élevé
        }
        risk_score = round(risk_by_stage[stage], 4)
        # round(..., 4) : 4 décimales pour un JSON propre

        # --- Étape 6 : construire la réponse ---
        return {
            "stage": stage,
            # stage : entier 0..4

            "stage_label": STAGE_LABELS[stage],
            # libellé lisible depuis le dictionnaire

            "risk_score": risk_score,
            # float 0.0 à 1.0

            "refer_to_doctor": stage >= 2,
            # règle clinique : on réfère au médecin dès le stade 2
        }