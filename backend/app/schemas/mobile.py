from pydantic import BaseModel, Field


class MobileScanResponse(BaseModel):
    screening_id: int | None = None
    patient_id: int | None = None
    is_eye: bool
    patient_message: str
    stage: str | None = None
    stage_label: str | None = None
    risk_score: float | None = None
    refer_to_doctor: bool = False
    ai_constants: dict | None = None
    recommendations: list[str] = Field(default_factory=list)
    blockchain_block_index: int | None = None
    blockchain_status: str | None = None
    image_sha256: str | None = None
