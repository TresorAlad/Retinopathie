from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Stage = Literal["no_dr", "mild", "moderate", "severe", "proliferative"]

class ScreeningResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_id: int
    ai_status: str
    ai_stage: str | None
    ai_confidence: float | None
    image_quality: str | None
    retinal_image_valid: bool | None
    diagnosis: str | None
    diagnosis_status: str
    diagnosis_note: str | None
    blockchain_status: str
    image_sha256: str
    created_at: datetime

class DiagnosisUpdate(BaseModel):
    diagnosis: Stage
    note: str | None = Field(default=None, max_length=2000)
