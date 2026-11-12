-- Colonnes IA enrichies (recommandations + message patient) sur screenings.
-- Idempotent : safe sur une base déjà à jour.

ALTER TABLE screenings ADD COLUMN IF NOT EXISTS ai_recommendations TEXT;
ALTER TABLE screenings ADD COLUMN IF NOT EXISTS ai_patient_message TEXT;
