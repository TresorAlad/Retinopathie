# Diabetic Retinopathy Backend

Backend FastAPI pour l'application de dépistage de la rétinopathie diabétique.

## État fonctionnel
- Authentification médecin par JWT et mot de passe Argon2.
- Patients : liste et détail.
- Dépistages : téléversement JPEG/PNG, contrôle de taille, chiffrement Fernet au repos, SHA-256, consultation, téléchargement autorisé, validation/correction par médecin.
- PostgreSQL via SQLAlchemy.
- Adaptateurs IA et blockchain présents mais volontairement non connectés : le résultat IA reste `pending` et la blockchain `not_configured` jusqu'à réception des contrats techniques des autres équipes. Aucune prédiction ni transaction fictive n'est produite.

## Installation Windows / PowerShell
Depuis la racine du projet :

```powershell
python -m venv venv
.env\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Modifie `.env` avec les paramètres PostgreSQL et les secrets.
Génère les secrets :

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Crée la base PostgreSQL `diabetic_retinopathy`, puis renseigne le mot de passe dans `DATABASE_URL`.

## Initialisation
```powershell
python -m scripts.create_doctor
python -m scripts.create_patient
```

## Lancement
```powershell
uvicorn app.main:app --reload
```

## Tests automatisés
```powershell
python -m pytest -q
```

## Routes prévues
- POST `/api/v1/auth/login`
- GET `/api/v1/auth/me` (route utilitaire protégée)
- POST `/api/v1/screenings`
- GET `/api/v1/screenings/{id}`
- GET `/api/v1/screenings`
- GET `/api/v1/patients`
- GET `/api/v1/patients/{id}`
- GET `/api/v1/screenings/{id}/image`
- PATCH `/api/v1/screenings/{id}/diagnosis`
- GET `/api/v1/health`

## Contrat d'envoi image
`multipart/form-data` avec :
- `patient_id` : identifiant numérique du patient existant.
- `image` : fichier JPEG ou PNG.

## Sécurité / limites
- Ne jamais committer `.env`, les clés, ni `storage/`.
- Les photos ne sont pas stockées dans PostgreSQL ni sur la blockchain.
- `create_all()` sert au démarrage initial ; adopter Alembic avant les évolutions de schéma partagées.
- Prévoir autorisations par patient/établissement, journal d'audit, sauvegardes, chiffrement des clés et stockage objet privé avant mise en production.
- Les stades utilisés dans l'API : `no_dr`, `mild`, `moderate`, `severe`, `proliferative`. À confirmer avec l'équipe médicale/IA.
